/* Tinten Couverture : en-tête, menu, animations au défilement, galerie, visionneuse et formulaire de devis. */
(function () {
  "use strict";

  var PHONE = "+33669578288";
  var WHATSAPP = "33669578288";
  var doc = document;
  var reduced = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var hasIO = "IntersectionObserver" in window;

  function $(sel, root) { return (root || doc).querySelector(sel); }
  function $$(sel, root) { return Array.prototype.slice.call((root || doc).querySelectorAll(sel)); }

  // Apparition au défilement : appelle fn(el) une fois quand l'élément entre à l'écran
  function onView(els, fn, opts) {
    if (!els.length) return;
    if (!hasIO) { els.forEach(fn); return; }
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { io.unobserve(e.target); fn(e.target); }
      });
    }, opts || { rootMargin: "0px 0px -8% 0px", threshold: 0.12 });
    els.forEach(function (el) { io.observe(el); });
  }

  // En-tête : fond plein après défilement, barre d'appel mobile
  var header = $("[data-header]");
  var callbar = $(".callbar");
  var ticking = false;
  var scrollers = [];

  function onScroll() {
    if (ticking) return;
    ticking = true;
    window.requestAnimationFrame(function () {
      var y = window.scrollY || window.pageYOffset;
      if (header) header.classList.toggle("scrolled", y > 30);
      if (callbar) callbar.classList.toggle("show", y > 420);
      scrollers.forEach(function (fn) { fn(y); });
      ticking = false;
    });
  }
  window.addEventListener("scroll", onScroll, { passive: true });
  window.addEventListener("resize", onScroll, { passive: true });

  // Menu mobile plein écran
  var toggle = $(".menu-toggle");
  function setMenu(open) {
    header.classList.toggle("open", open);
    toggle.setAttribute("aria-expanded", open ? "true" : "false");
    toggle.setAttribute("aria-label", open ? "Fermer le menu" : "Ouvrir le menu");
    doc.body.classList.toggle("no-scroll", open);
  }
  if (header && toggle) {
    toggle.addEventListener("click", function () { setMenu(!header.classList.contains("open")); });
    $$(".nav a").forEach(function (a) {
      a.addEventListener("click", function () { if (header.classList.contains("open")) setMenu(false); });
    });
    window.matchMedia("(min-width: 1100px)").addEventListener("change", function (m) { if (m.matches) setMenu(false); });
  }

  // Sous-menu Prestations : fermeture au clic extérieur et avec Échap
  var sub = $(".sub");
  doc.addEventListener("click", function (e) {
    if (sub && sub.open && !sub.contains(e.target) && window.innerWidth >= 1100) sub.open = false;
  });
  doc.addEventListener("keydown", function (e) {
    if (e.key !== "Escape") return;
    if (sub && sub.open) { sub.open = false; $("summary", sub).focus(); }
    if (header && header.classList.contains("open")) { setMenu(false); toggle.focus(); }
  });

  // Blocs qui apparaissent
  onView($$("[data-reveal]"), function (el) { el.classList.add("in"); });

  // Léger effet de profondeur sur la photo d'en-tête
  var heroMedia = $(".hero-media, .page-hero-media");
  if (heroMedia && !reduced) {
    scrollers.push(function (y) {
      if (y > window.innerHeight * 1.2) return;
      heroMedia.style.setProperty("transform", "translate3d(0," + (y * 0.28).toFixed(1) + "px,0)");
    });
  }

  // Schéma de la toiture : les couches se posent une à une, puis la légende s'allume
  var anatomy = $("[data-anatomy]");
  if (anatomy) {
    var grid = anatomy.closest(".anatomy-grid") || anatomy;
    var items = $$(".anatomy-legend li[data-step]", grid);
    var marks = $$(".mk[data-step]", grid);
    var current = 0, timer = null, userActive = false;

    function highlight(step) {
      items.forEach(function (li) { li.classList.toggle("hl", li.getAttribute("data-step") === String(step)); });
      marks.forEach(function (m) { m.classList.toggle("hl", m.getAttribute("data-step") === String(step)); });
    }
    function cycle() {
      if (userActive) return;
      current = current % items.length + 1;
      highlight(current);
    }
    items.concat(marks).forEach(function (el) {
      var step = el.getAttribute("data-step");
      el.addEventListener("mouseenter", function () { userActive = true; highlight(step); });
      el.addEventListener("mouseleave", function () { userActive = false; });
    });
    $$("a", grid).forEach(function (a) {
      a.addEventListener("focus", function () {
        var li = a.closest("li[data-step]");
        if (li) { userActive = true; highlight(li.getAttribute("data-step")); }
      });
      a.addEventListener("blur", function () { userActive = false; });
    });

    onView([anatomy], function () {
      grid.classList.add("play");
      window.setTimeout(function () {
        grid.classList.add("done");
        if (!reduced && items.length) { cycle(); timer = window.setInterval(cycle, 2600); }
      }, reduced ? 0 : 4000);
    }, { threshold: 0.3 });
  }

  // Compteurs
  onView($$("[data-count]"), function (el) {
    var end = parseInt(el.getAttribute("data-count"), 10);
    if (reduced || !end) return;
    var start = null, dur = 1600;
    el.textContent = "0";
    function step(t) {
      if (start === null) start = t;
      var k = Math.min(1, (t - start) / dur);
      el.textContent = String(Math.round(end * (1 - Math.pow(1 - k, 3))));
      if (k < 1) window.requestAnimationFrame(step);
    }
    window.requestAnimationFrame(step);
  }, { threshold: 0.6 });

  // Étapes du chantier : la ligne se remplit au défilement
  var track = $("[data-progress]");
  if (track) {
    var steps = $$(".steps li", track);
    scrollers.push(function () {
      var r = track.getBoundingClientRect();
      var vh = window.innerHeight;
      var p = Math.max(0, Math.min(1, (vh * 0.8 - r.top) / (r.height + vh * 0.25)));
      track.style.setProperty("--p", p.toFixed(3));
      steps.forEach(function (li, i) { li.classList.toggle("lit", p >= (i + 0.35) / steps.length); });
    });
  }

  // Zone d'intervention : les communes apparaissent autour de Saumur
  onView($$("[data-radar]"), function (el) { el.classList.add("play"); }, { threshold: 0.25 });

  // Galerie défilante : flèches et glisser à la souris
  var gTrack = $("[data-g-track]");
  if (gTrack) {
    var prev = $("[data-g-prev]"), next = $("[data-g-next]");
    function stepSize() {
      var card = $(".g-card", gTrack);
      return card ? card.getBoundingClientRect().width + 19 : 400;
    }
    function updateNav() {
      var max = gTrack.scrollWidth - gTrack.clientWidth - 4;
      if (prev) prev.disabled = gTrack.scrollLeft <= 4;
      if (next) next.disabled = gTrack.scrollLeft >= max;
    }
    if (prev) prev.addEventListener("click", function () { gTrack.scrollBy({ left: -stepSize(), behavior: reduced ? "auto" : "smooth" }); });
    if (next) next.addEventListener("click", function () { gTrack.scrollBy({ left: stepSize(), behavior: reduced ? "auto" : "smooth" }); });
    gTrack.addEventListener("scroll", updateNav, { passive: true });
    window.addEventListener("resize", updateNav);
    updateNav();

    var down = false, moved = false, sx = 0, sl = 0;
    gTrack.addEventListener("pointerdown", function (e) {
      if (e.pointerType !== "mouse" || e.button !== 0) return;
      down = true; moved = false; sx = e.clientX; sl = gTrack.scrollLeft;
    });
    window.addEventListener("pointermove", function (e) {
      if (!down) return;
      var dx = e.clientX - sx;
      if (!moved && Math.abs(dx) > 6) { moved = true; gTrack.classList.add("drag"); }
      if (moved) { gTrack.scrollLeft = sl - dx; e.preventDefault(); }
    });
    window.addEventListener("pointerup", function () {
      if (!down) return;
      down = false;
      if (moved) {
        gTrack.classList.remove("drag");
        var w = stepSize();
        gTrack.scrollTo({ left: Math.round(gTrack.scrollLeft / w) * w, behavior: "smooth" });
      }
    });
    gTrack.addEventListener("click", function (e) { if (moved) { e.preventDefault(); e.stopPropagation(); moved = false; } }, true);
    gTrack.addEventListener("dragstart", function (e) { e.preventDefault(); });
  }

  // Visionneuse photo
  var lb = $("[data-lightbox]");
  var links = $$("a[data-lb]");
  if (lb && links.length && typeof lb.showModal === "function") {
    var lbImg = $("[data-lb-img]", lb), lbCap = $("[data-lb-cap]", lb), idx = 0;
    function openAt(i) {
      idx = (i + links.length) % links.length;
      var a = links[idx];
      lbImg.src = a.getAttribute("href");
      lbImg.alt = a.getAttribute("data-cap") || "";
      lbCap.textContent = a.getAttribute("data-cap") || "";
      if (!lb.open) lb.showModal();
    }
    links.forEach(function (a, i) {
      a.addEventListener("click", function (e) { e.preventDefault(); openAt(i); });
    });
    lb.addEventListener("click", function (e) { if (e.target === lb) lb.close(); });
    lb.addEventListener("keydown", function (e) {
      if (e.key === "ArrowRight") openAt(idx + 1);
      if (e.key === "ArrowLeft") openAt(idx - 1);
    });
    lb.addEventListener("close", function () { lbImg.removeAttribute("src"); });
  }

  onScroll();

  // Formulaire de devis
  var form = doc.getElementById("devis-form");
  if (!form) return;
  var status = doc.getElementById("form-status");

  function el(tag, attrs, text) {
    var n = doc.createElement(tag);
    Object.keys(attrs || {}).forEach(function (k) { n.setAttribute(k, attrs[k]); });
    if (text) n.textContent = text;
    return n;
  }

  function show(kind, nodes) {
    status.className = "form-status " + kind;
    status.textContent = "";
    nodes.forEach(function (n) { status.appendChild(n); });
    status.setAttribute("tabindex", "-1");
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
      nom: form.elements.nom.value.trim(),
      telephone: form.elements.telephone.value.trim(),
      email: form.elements.email.value.trim(),
      commune: form.elements.commune.value.trim(),
      type: form.elements.type.value,
      message: form.elements.message.value.trim(),
      rappel: form.elements.rappel.value,
      site_web: form.elements.site_web.value,
      consentement: form.elements.consentement.checked
    };

    var button = form.querySelector("button[type=submit]");
    var label = button.querySelector("span");
    button.disabled = true;
    if (label) label.textContent = "Envoi en cours…";

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
      if (label) label.textContent = "Envoyer ma demande";
    });
  });
})();
