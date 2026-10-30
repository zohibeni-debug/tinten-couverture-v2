/**
 * Tinten Couverture : petit serveur Cloudflare.
 *
 * Les pages du site sont des fichiers statiques (dossier public/), servies directement par Cloudflare.
 * Ce script ne traite qu'une adresse : POST /api/devis, le formulaire de demande de devis.
 *
 * Envoi par Cloudflare Email Service (binding EMAIL, voir wrangler.jsonc).
 * Le domaine d'envoi doit être ajouté dans Compute > Email Service > Email Sending > Onboard Domain.
 *
 * Réglages facultatifs (Workers & Pages > tinten-couverture-v2 > Settings > Variables and Secrets) :
 *   DEVIS_TO        adresse(s) qui reçoivent les demandes, séparées par des virgules
 *                   (par défaut : contact@tinten-couverture.fr)
 *   DEVIS_FROM      expéditeur, ex. « Site Tinten Couverture <devis@tinten-couverture.fr> »
 *   RESEND_API_KEY  envoi de secours par Resend si Cloudflare échoue (facultatif)
 *
 * Si aucun envoi ne fonctionne, l'API répond une erreur et la page propose WhatsApp ou SMS.
 */

const DEFAULT_TO = "contact@tinten-couverture.fr";
const DEFAULT_FROM = "Site Tinten Couverture <devis@tinten-couverture.fr>";

const SECURITY_HEADERS = {
  "X-Content-Type-Options": "nosniff",
  "Referrer-Policy": "strict-origin-when-cross-origin",
  "Cache-Control": "no-store",
};

function json(body, status = 200, extra = {}) {
  return new Response(JSON.stringify(body), {
    status,
    headers: { "Content-Type": "application/json; charset=utf-8", ...SECURITY_HEADERS, ...extra },
  });
}

function clean(v, max) {
  return String(v ?? "").replace(/[\u0000-\u0008\u000B\u000C\u000E-\u001F\u007F]/g, "").trim().slice(0, max);
}

// « Nom <adresse> » ou « adresse » -> { email, name }
function parseAddress(v) {
  const s = String(v || "").trim();
  const m = s.match(/^(.*)<\s*([^<>\s]+@[^<>\s]+)\s*>$/);
  if (m) return { email: m[2], name: m[1].trim().replace(/^"|"$/g, "") || undefined };
  return { email: s };
}

function recipients(env) {
  return String(env.DEVIS_TO || DEFAULT_TO).split(",").map((s) => s.trim()).filter(Boolean);
}

async function sendCloudflare(env, mail) {
  const from = parseAddress(env.DEVIS_FROM || DEFAULT_FROM);
  const msg = { from, to: mail.to, subject: mail.subject, text: mail.text };
  if (mail.replyTo) msg.replyTo = mail.replyTo;
  await env.EMAIL.send(msg);
}

async function sendResend(env, mail) {
  const payload = {
    from: env.DEVIS_FROM || DEFAULT_FROM,
    to: mail.to,
    subject: mail.subject,
    text: mail.text,
  };
  if (mail.replyTo) payload.reply_to = mail.replyTo;
  const r = await fetch("https://api.resend.com/emails", {
    method: "POST",
    headers: { Authorization: `Bearer ${env.RESEND_API_KEY}`, "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!r.ok) throw new Error(`Resend ${r.status} ${await r.text()}`);
}

async function handleDevis(request, env) {
  if (request.method !== "POST") {
    return json({ ok: false, error: "Méthode non autorisée." }, 405, { Allow: "POST" });
  }
  const len = Number(request.headers.get("content-length") || 0);
  if (len > 20000) return json({ ok: false, error: "Message trop long." }, 413);

  let data;
  try {
    data = await request.json();
  } catch {
    return json({ ok: false, error: "Requête invalide." }, 400);
  }

  // Champ piège : rempli uniquement par les robots
  if (clean(data.site_web, 200)) return json({ ok: true });

  const d = {
    nom: clean(data.nom, 80),
    telephone: clean(data.telephone, 20),
    email: clean(data.email, 120),
    commune: clean(data.commune, 80),
    type: clean(data.type, 80),
    message: clean(data.message, 3000),
    rappel: clean(data.rappel, 30) || "Indifférent",
  };

  if (!d.nom || !d.commune || !d.type || !d.message) {
    return json({ ok: false, error: "Complétez le nom, la commune, le type de travaux et la description." }, 400);
  }
  if (!/^[+0-9 .()-]{8,20}$/.test(d.telephone)) {
    return json({ ok: false, error: "Le numéro de téléphone semble incomplet." }, 400);
  }
  if (d.email && !/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(d.email)) {
    return json({ ok: false, error: "L'adresse email semble incorrecte." }, 400);
  }
  if (data.consentement !== true) {
    return json({ ok: false, error: "Merci de cocher la case d'accord." }, 400);
  }

  const mail = {
    to: recipients(env),
    subject: `Devis : ${d.type} à ${d.commune} (${d.nom})`,
    replyTo: d.email || undefined,
    text: [
      "Nouvelle demande de devis depuis le site tinten-couverture.fr",
      "",
      `Nom : ${d.nom}`,
      `Téléphone : ${d.telephone}`,
      d.email ? `Email : ${d.email}` : "Email : non communiqué",
      `Commune : ${d.commune}`,
      `Travaux : ${d.type}`,
      `Rappel souhaité : ${d.rappel}`,
      "",
      d.message,
      "",
      d.email ? "Répondez directement à cet email pour écrire au client." : "Le client n'a pas laissé d'email : rappelez-le au numéro ci-dessus.",
    ].join("\n"),
  };

  const senders = [];
  if (env.EMAIL) senders.push(["cloudflare", sendCloudflare]);
  if (env.RESEND_API_KEY) senders.push(["resend", sendResend]);
  if (!senders.length) return json({ ok: false, reason: "not_configured" }, 503);

  for (const [name, send] of senders) {
    try {
      await send(env, mail);
      return json({ ok: true });
    } catch (e) {
      console.error("Envoi devis échoué", name, e && (e.code || ""), e && e.message);
    }
  }
  return json({ ok: false, reason: "send_failed" }, 502);
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (url.pathname === "/api/devis") return handleDevis(request, env);
    return env.ASSETS.fetch(request);
  },
};
