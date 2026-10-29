# Site Tinten Couverture

Site de Tinten Couverture, couvreur à Saumur. Pages HTML complètes (lisibles par Google sans JavaScript), hébergées sur Cloudflare.

## Ce que contient ce dépôt

| Dossier | Rôle |
|---|---|
| `public/` | Le site tel qu'il est mis en ligne : pages, images, plan du site, redirections |
| `src/worker.js` | Le petit programme qui reçoit le formulaire de devis |
| `site/` | Les textes (`content.py`), le style (`site.css`) et le générateur de pages (`build.py`) |
| `wrangler.jsonc` | La configuration Cloudflare |

## Comment une modification arrive en ligne

1. Les textes ou le style sont modifiés dans `site/`, puis `python3 site/build.py` régénère `public/`.
2. La modification est envoyée sur GitHub, branche `main`.
3. Cloudflare détecte l'envoi, déploie, et le site est à jour en une à deux minutes.

## Brancher Cloudflare (une seule fois)

Dans Cloudflare : **Workers & Pages** > **Create application** > **GitHub**, puis choisir ce dépôt.

- Nom du projet : `tinten-couverture-v2` (il doit être identique au `name` de `wrangler.jsonc`)
- Build command : laisser vide
- Deploy command : `npx wrangler deploy`

Le site apparaît sur une adresse provisoire en `.workers.dev`, non indexée par Google.

## Formulaire de devis

Sans réglage, le formulaire propose d'envoyer la demande par WhatsApp ou par SMS. Pour recevoir les demandes par email, ajouter dans Cloudflare (**Settings** > **Variables and Secrets**, type *Secret*) :

- `RESEND_API_KEY` : clé API du compte Resend
- `DEVIS_TO` : adresse qui reçoit les demandes
- `DEVIS_FROM` (facultatif) : expéditeur vérifié chez Resend, par exemple `Site Tinten Couverture <devis@tinten-couverture.fr>`

## Avant de brancher le domaine tinten-couverture.fr

Points à confirmer avec le client (voir aussi `A_CONFIRMER` dans `site/content.py`) :

- numéro de téléphone, email, SIRET, horaires ;
- nom du gérant, assureur décennale, médiateur de la consommation (page Mentions légales) ;
- certifications RGE ou Qualibat, service d'urgence : non affichés tant qu'ils ne sont pas confirmés ;
- liste complète des adresses du site actuel, pour compléter les redirections de `REDIRECTS` dans `site/build.py`.
