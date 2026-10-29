/**
 * Tinten Couverture : petit serveur Cloudflare.
 *
 * Les pages du site sont des fichiers statiques (dossier public/), servies directement par Cloudflare.
 * Ce script ne traite qu'une adresse : POST /api/devis, le formulaire de demande de devis.
 *
 * Envoi par email via Resend si ces secrets sont définis dans Cloudflare
 * (Workers & Pages > tinten-couverture-v2 > Settings > Variables and Secrets) :
 *   RESEND_API_KEY  clé API Resend
 *   DEVIS_TO        adresse qui reçoit les demandes
 *   DEVIS_FROM      expéditeur vérifié chez Resend (facultatif)
 * Sans ces secrets, l'API répond 503 et la page propose l'envoi par WhatsApp ou SMS.
 */

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

  if (!env.RESEND_API_KEY || !env.DEVIS_TO) {
    return json({ ok: false, reason: "not_configured" }, 503);
  }

  const text = [
    "Nouvelle demande de devis depuis le site",
    "",
    `Nom : ${d.nom}`,
    `Téléphone : ${d.telephone}`,
    d.email ? `Email : ${d.email}` : "Email : non communiqué",
    `Commune : ${d.commune}`,
    `Travaux : ${d.type}`,
    `Rappel souhaité : ${d.rappel}`,
    "",
    d.message,
  ].join("\n");

  const payload = {
    from: env.DEVIS_FROM || "Site Tinten Couverture <onboarding@resend.dev>",
    to: [env.DEVIS_TO],
    subject: `Devis : ${d.type} à ${d.commune} (${d.nom})`,
    text,
  };
  if (d.email) payload.reply_to = d.email;

  const r = await fetch("https://api.resend.com/emails", {
    method: "POST",
    headers: { Authorization: `Bearer ${env.RESEND_API_KEY}`, "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });

  if (!r.ok) {
    console.error("Resend", r.status, await r.text());
    return json({ ok: false, reason: "send_failed" }, 502);
  }
  return json({ ok: true });
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (url.pathname === "/api/devis") return handleDevis(request, env);
    return env.ASSETS.fetch(request);
  },
};
