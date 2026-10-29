/* Tinten Couverture : menu mobile, sous-menu et formulaire de devis. */
(function () {
  "use strict";

  var PHONE = "+33669578288";
  var WHATSAPP = "33669578288";

  // Menu mobile
  var header = document.querySelector(".site-header");
  var toggle = document.querySelector(".menu-toggle");
  if (header && toggle) {
    toggle.addEventListener("click", function () {
      var open = header.classList.toggle("open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
  }

  // Sous-menu Prestations : fermeture au clic extérieur et avec Échap
  var sub = document.querySelector(".sub");
  if (sub) {
    document.addEventListener("click", function (e) {
      if (sub.open && !sub.contains(e.target)) sub.open = false;
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && sub.open) {
        sub.open = false;
        sub.querySelector("summary").focus();
      }
    });
  }

  // Formulaire de devis
  var form = document.getElementById("devis-form");
  if (!form) return;
  var status = document.getElementById("form-status");

  function el(tag, attrs, text) {
    var n = document.createElement(tag);
    Object.keys(attrs || {}).forEach(function (k) { n.setAttribute(k, attrs[k]); });
    if (text) n.textContent = text;
    return n;
  }

  function show(kind, nodes) {
    status.className = "form-status " + kind;
    status.textContent = "";
    nodes.forEach(function (n) { status.appendChild(n); });
    status.focus && status.setAttribute("tabindex", "-1");
    status.focus();
  }

  function summary(d) {
    return "Demande de devis\n" +
      "Nom : " + d.nom + "\n" +
      "Téléphone : " + d.telephone + "\n" +
      (d.email ? "Email : " + d.email + "\n" : "") +
      "Commune : " + d.commune + "\n" +
      "Travaux : " + d.type + "\n" +
      "Rappel : " + d.rappel + "\n\n" + d.message;
  }

  function fallback(d) {
    var text = summary(d);
    var actions = el("div", { "class": "fallback-actions" });
    actions.appendChild(el("a", { "class": "btn btn-primary", href: "https://wa.me/" + WHATSAPP + "?text=" + encodeURIComponent(text), rel: "noopener" }, "Envoyer sur WhatsApp"));
    actions.appendChild(el("a", { "class": "btn btn-ghost", href: "sms:" + PHONE + "?&body=" + encodeURIComponent(text) }, "Envoyer par SMS"));
    actions.appendChild(el("a", { "class": "btn btn-ghost", href: "tel:" + PHONE }, "Appeler"));
    show("err", [
      el("p", {}, "L'envoi par le site n'a pas abouti. Votre demande est prête : envoyez-la en un geste par WhatsApp ou par SMS, ou appelez-nous."),
      actions
    ]);
  }

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    var fields = form.querySelectorAll("[required]");
    var firstInvalid = null;
    fields.forEach(function (f) {
      var ok = f.type === "checkbox" ? f.checked : f.value.trim() !== "" && f.checkValidity();
      f.setAttribute("aria-invalid", ok ? "false" : "true");
      if (!ok && !firstInvalid) firstInvalid = f;
    });
    if (firstInvalid) {
      show("err", [el("p", {}, "Complétez les champs signalés : nom, téléphone, commune, type de travaux, description du projet et accord.")]);
      firstInvalid.focus();
      return;
    }

    var d = {
      nom: form.nom.value.trim(),
      telephone: form.telephone.value.trim(),
      email: form.email.value.trim(),
      commune: form.commune.value.trim(),
      type: form.type.value,
      message: form.message.value.trim(),
      rappel: form.rappel.value,
      site_web: form.site_web.value,
      consentement: form.consentement.checked
    };

    var button = form.querySelector("button[type=submit]");
    button.disabled = true;
    button.textContent = "Envoi en cours…";

    fetch("/api/devis", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(d)
    }).then(function (r) {
      return r.json().catch(function () { return {}; }).then(function (j) { return { status: r.status, body: j }; });
    }).then(function (res) {
      if (res.status === 200 && res.body.ok) {
        form.reset();
        show("ok", [el("p", {}, "Demande envoyée. Nous vous recontactons pour convenir d'une visite.")]);
      } else if (res.status === 400 && res.body.error) {
        show("err", [el("p", {}, res.body.error)]);
      } else {
        fallback(d);
      }
    }).catch(function () {
      fallback(d);
    }).then(function () {
      button.disabled = false;
      button.textContent = "Envoyer ma demande";
    });
  });
})();
