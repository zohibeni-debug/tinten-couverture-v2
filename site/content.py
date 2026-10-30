# -*- coding: utf-8 -*-
"""Contenus du site Tinten Couverture.

Tout le texte du site est ici. Le générateur (build.py) l'assemble en pages HTML.
Règle : n'écrire que des faits vérifiés ou vérifiables. Les points à confirmer
par le client sont listés dans A_CONFIRMER.
"""

SITE_URL = "https://tinten-couverture.fr"

BUSINESS = {
    "name": "Tinten Couverture",
    "tagline": "Couvreur, zingueur & ravalement",
    "phone": "06 69 57 82 88",
    "phone_e164": "+33669578288",
    "whatsapp": "33669578288",
    "email": "contact@tinten-couverture.fr",
    "street": "24 boulevard des Demoiselles",
    "postcode": "49400",
    "city": "Saumur",
    "region": "Maine-et-Loire",
    "siret": "484 147 327 00023",
    "since": 2009,
    "radius_km": 40,
    "hours_text": "Du lundi au vendredi, de 8 h à 18 h",
    "hours_schema": [{"days": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], "opens": "08:00", "closes": "18:00"}],
    "facebook": "https://www.facebook.com/tintencouverture/",
    "google_reviews": "https://www.google.com/search?q=Tinten+Couverture+Saumur+avis",
    "maps": "https://www.google.com/maps/search/?api=1&query=Tinten+Couverture+24+boulevard+des+Demoiselles+49400+Saumur",
}

A_CONFIRMER = [
    "Numéro de téléphone (06 69 57 82 88 retenu ; le 09 50 39 71 96 circule sur Bonjour Artisan)",
    "Adresse email contact@tinten-couverture.fr : la boîte existe-t-elle ?",
    "SIRET 484 147 327 00023 (relevé sur Bonjour Artisan)",
    "Nom du gérant (responsable de la publication)",
    "Assureur décennale (nom et zone de couverture)",
    "Médiateur de la consommation",
    "Horaires (le repo indique lundi-vendredi 8 h-18 h, les annuaires d'autres horaires)",
    "Certifications RGE / Qualibat (non affichées tant que non confirmées)",
    "Service d'urgence le soir et le week-end (non promis tant que non confirmé)",
]

# ---------------------------------------------------------------------------
# Prestations
# ---------------------------------------------------------------------------
# Chaque prestation : slug (adresse de la page), nav (nom court), h1, title, desc,
# lead, photo, sections [(titre, html)], steps (facultatif), faq [(q, r)], related.

SERVICES = [
    {
        "slug": "renovation-toiture",
        "nav": "Rénovation de toiture",
        "short": "Réfection complète en ardoise ou en tuile, de la charpente au faîtage.",
        "h1": "Rénovation de toiture à Saumur",
        "title": "Rénovation de toiture à Saumur (49) | Tinten Couverture",
        "desc": "Réfection complète de toiture en ardoise ou en tuile à Saumur et dans le Saumurois : dépose, charpente, écran sous-toiture, couverture et zinguerie. Devis gratuit.",
        "photo": "ecran-sous-toiture-liteaux",
        "photo_alt": "Toiture en cours de réfection : écran sous-toiture, contre-liteaux et liteaux neufs avant la pose de la couverture",
        "lead": "Quand les fuites reviennent après chaque réparation, la réfection complète est souvent la solution la plus économique sur la durée. Nous reprenons la toiture dans son ensemble, en ardoise ou en tuile, en respectant le caractère de la maison.",
        "sections": [
            ("Quand faut-il refaire sa toiture ?",
             "<p>Une couverture ne s'use pas d'un coup. Plusieurs signes montrent qu'elle arrive en fin de vie :</p>"
             "<ul>"
             "<li>des ardoises qui glissent ou se cassent régulièrement, des crochets rouillés ;</li>"
             "<li>des tuiles poreuses qui s'effritent ou se fendent au gel ;</li>"
             "<li>des liteaux qui pourrissent, une toiture qui ondule ou s'affaisse ;</li>"
             "<li>des traces d'humidité dans les combles après la pluie ;</li>"
             "<li>une mousse installée en profondeur, qui revient aussitôt après un nettoyage.</li>"
             "</ul>"
             "<p>Lors de la visite, nous montons dans les combles et sur le toit pour faire la part des choses : une réparation ciblée suffit parfois, et nous vous le disons.</p>"),
            ("Ardoise ou tuile : garder le caractère de la maison",
             "<p>Dans le Saumurois, la plupart des maisons en tuffeau sont couvertes d'ardoise. Les tuiles se rencontrent surtout sur les dépendances, les anciennes fermes et les maisons plus récentes. Changer de matériau modifie l'aspect extérieur : cela passe par une déclaration préalable en mairie, et, dans les secteurs protégés comme le centre ancien de Saumur ou les abords des monuments historiques, par l'avis de l'Architecte des Bâtiments de France.</p>"
             "<p>Une réfection à l'identique est le cas le plus simple. Nous vous indiquons les démarches au moment du devis.</p>"),
            ("La charpente et l'isolation, au bon moment",
             "<p>Une toiture découverte est l'occasion de contrôler la charpente : chevrons fendus, pièces attaquées par les insectes ou l'humidité sont remplacés ou renforcés avant de refermer. C'est aussi le moment le plus favorable pour améliorer l'isolation des combles, puisque tout est accessible.</p>"),
        ],
        "steps_title": "Comment se déroule une réfection complète",
        "steps": [
            ("Visite et diagnostic", "Toiture, combles, charpente et zinguerie : nous relevons l'état de chaque élément et les mesures."),
            ("Devis détaillé", "Matériaux, quantités, délais et options sont écrits noir sur blanc. Le devis est gratuit."),
            ("Échafaudage et protection", "Mise en sécurité du chantier, protection des abords et des façades."),
            ("Dépose", "L'ancienne couverture est déposée par sections et les déchets sont évacués."),
            ("Charpente et écran", "Contrôle et reprise de la charpente, pose d'un écran sous-toiture, de contre-liteaux et de liteaux neufs."),
            ("Couverture et zinguerie", "Pose de l'ardoise ou des tuiles, des noues, des abergements, des rives et des gouttières."),
            ("Faîtage et réception", "Pose du faîtage, nettoyage du chantier et visite de fin de travaux avec vous."),
        ],
        "faq": [
            ("Combien de temps durent les travaux ?",
             "Pour une maison individuelle, comptez en général une à trois semaines selon la surface, le nombre de lucarnes et de cheminées, et la météo. Le planning prévu figure sur le devis."),
            ("Peut-on rester dans la maison pendant le chantier ?",
             "Oui. La toiture est découverte par sections et refermée ou bâchée chaque soir, pour que la maison reste hors d'eau."),
            ("Faut-il une autorisation pour refaire sa toiture ?",
             "Une réfection à l'identique ne demande en général pas d'autorisation. Si l'aspect change (matériau, couleur, ajout de fenêtres de toit), une déclaration préalable est nécessaire. En secteur protégé, l'avis de l'Architecte des Bâtiments de France s'ajoute. La mairie reste la référence."),
            ("Les travaux sont-ils garantis ?",
             "Les travaux de couverture relèvent de la garantie décennale. Les références de notre assurance figurent sur chaque devis et chaque facture."),
        ],
        "related": ["couverture-ardoise", "couverture-tuile", "zinguerie-gouttieres"],
    },
    {
        "slug": "couverture-ardoise",
        "nav": "Couverture en ardoise",
        "short": "Pose, remplacement et réparation d'ardoise naturelle, au crochet ou au clou.",
        "h1": "Couvreur ardoise à Saumur",
        "title": "Couvreur ardoise à Saumur : pose et réparation | Tinten Couverture",
        "desc": "Couverture en ardoise naturelle à Saumur : réfection, remplacement d'ardoises, lucarnes, noues et faîtages. Pose au crochet ou au clou. Devis gratuit après visite.",
        "photo": "toiture-ardoise-cheminees",
        "photo_alt": "Toiture en ardoise naturelle refaite, avec deux souches de cheminée en brique",
        "lead": "Le tuffeau blanc et l'ardoise bleutée font l'identité des maisons du Saumurois. Nous posons et réparons l'ardoise naturelle selon les règles du métier, pour des toitures qui durent plusieurs générations.",
        "sections": [
            ("L'ardoise, toit du Saumurois",
             "<p>Pendant des siècles, l'ardoise des carrières de Trélazé, près d'Angers, a couvert les maisons de la région. L'extraction y a cessé en 2014. Les chantiers se font aujourd'hui avec des ardoises naturelles sélectionnées pour leur épaisseur et leur tenue, et, pour les réparations, avec des ardoises de réemploi en bon état quand il faut s'accorder à une toiture ancienne.</p>"),
            ("Pose au crochet ou au clou",
             "<p>En Anjou, l'ardoise est le plus souvent posée au crochet inox sur liteaux : la fixation est solide et une ardoise cassée se remplace sans démonter ses voisines. Certaines toitures anciennes sont clouées sur voliges ; nous respectons la technique d'origine quand elle est en bon état.</p>"),
            ("Ce que nous réalisons",
             "<ul>"
             "<li>la réfection complète d'une couverture en ardoise ;</li>"
             "<li>le remplacement d'ardoises cassées ou glissées ;</li>"
             "<li>la reprise des faîtages, des rives et des égouts ;</li>"
             "<li>la couverture et la zinguerie des lucarnes ;</li>"
             "<li>les noues et les abergements en zinc ;</li>"
             "<li>la pose de fenêtres de toit dans une couverture en ardoise.</li>"
             "</ul>"),
            ("Entretenir une toiture en ardoise",
             "<p>Une ardoise naturelle n'a pas besoin de traitement hydrofuge. En revanche, une ardoise qui glisse laisse passer l'eau sur les liteaux : mieux vaut la remettre en place rapidement. Un contrôle visuel tous les quelques années, et après chaque coup de vent, évite la plupart des dégâts.</p>"),
        ],
        "faq": [
            ("Peut-on remplacer une seule ardoise ?",
             "Oui. Sur une couverture posée au crochet, l'ardoise cassée est retirée et remplacée par une ardoise de même format, fixée par un nouveau crochet."),
            ("Ardoise naturelle ou ardoise synthétique ?",
             "L'ardoise naturelle dure beaucoup plus longtemps et garde son aspect. L'ardoise en fibres-ciment coûte moins cher à l'achat mais vieillit plus vite, et elle peut être refusée en secteur protégé."),
            ("Combien coûte une couverture en ardoise ?",
             "Le prix dépend de la surface, de la pente, de l'accès, du nombre de lucarnes et de cheminées, et de l'état de la charpente. Nous le chiffrons après visite, sur un devis détaillé et gratuit."),
        ],
        "related": ["renovation-toiture", "zinguerie-gouttieres", "reparation-fuite-toiture"],
    },
    {
        "slug": "couverture-tuile",
        "nav": "Couverture en tuiles",
        "short": "Tuiles mécaniques, plates ou canal : réfection, remaniement et réparation.",
        "h1": "Couverture en tuiles à Saumur",
        "title": "Couverture en tuiles à Saumur et alentours | Tinten Couverture",
        "desc": "Couverture en tuiles à Saumur : réfection, remaniement, remplacement de tuiles, rives et faîtages. Tuiles mécaniques, plates ou canal. Devis gratuit.",
        "photo": "lucarne-tuiles-chantier",
        "photo_alt": "Lucarne couverte de tuiles en terre cuite pendant la réfection de la toiture",
        "lead": "Maisons récentes, longères, granges et dépendances : la tuile est très présente autour de Saumur. Nous refaisons, remanions et réparons les couvertures en tuiles avec les mêmes exigences que pour l'ardoise.",
        "sections": [
            ("Les tuiles que nous posons",
             "<ul>"
             "<li><strong>Tuiles mécaniques à emboîtement</strong>, en terre cuite, les plus courantes sur les maisons du XXe siècle et les constructions récentes ;</li>"
             "<li><strong>tuiles plates</strong>, posées à recouvrement sur les bâtiments anciens ;</li>"
             "<li><strong>tuiles canal</strong>, que l'on rencontre davantage en allant vers le sud de notre secteur.</li>"
             "</ul>"
             "<p>Pour une réparation, nous recherchons un modèle et une teinte compatibles avec la couverture existante.</p>"),
            ("Réfection ou remaniement ?",
             "<p>Quand les tuiles sont saines mais que les liteaux ou l'étanchéité ont vieilli, le remaniement suffit : les tuiles sont déposées, triées, puis reposées sur un support neuf, avec un écran sous-toiture. Les tuiles cassées sont remplacées. C'est moins coûteux qu'une réfection complète et cela conserve l'aspect de la toiture.</p>"
             "<p>Quand les tuiles elles-mêmes sont poreuses ou gélives, la réfection complète s'impose.</p>"),
            ("Faîtages et rives",
             "<p>Le faîtage et les rives sont les points les plus exposés au vent. Selon la toiture, nous les reprenons au mortier ou en pose à sec ventilée, avec closoirs, pour éviter que les tuiles ne se soulèvent.</p>"),
        ],
        "faq": [
            ("Faut-il traiter les tuiles avec un hydrofuge ?",
             "Ce n'est pas obligatoire. Sur des tuiles en bon état, un hydrofuge appliqué après démoussage limite la reprise des mousses et l'absorption d'eau. Sur des tuiles déjà poreuses, il ne remplace pas leur remplacement."),
            ("Une tuile cassée peut-elle provoquer une fuite ?",
             "Oui, surtout si l'écran sous-toiture est absent ou abîmé. Une tuile cassée se remplace rapidement : mieux vaut ne pas attendre l'hiver."),
            ("Peut-on passer de la tuile à l'ardoise ?",
             "C'est possible si la charpente le permet, mais l'aspect extérieur change : une déclaration préalable est nécessaire, et l'avis de l'Architecte des Bâtiments de France en secteur protégé."),
        ],
        "related": ["renovation-toiture", "entretien-demoussage-toiture", "reparation-fuite-toiture"],
    },
    {
        "slug": "zinguerie-gouttieres",
        "nav": "Zinguerie et gouttières",
        "short": "Gouttières, chéneaux, noues, abergements et bavettes en zinc.",
        "h1": "Zinguerie et gouttières à Saumur",
        "title": "Zinguerie et gouttières en zinc à Saumur | Tinten Couverture",
        "desc": "Zinguerie à Saumur : gouttières et descentes en zinc, chéneaux, noues, abergements, rives et bavettes d'appui. Pose et réparation. Devis gratuit.",
        "photo": "noue-zinc-ardoise",
        "photo_alt": "Noue en zinc neuve entre deux pans d'ardoise, posée sur liteaux",
        "lead": "Sur une toiture, l'eau passe par les points de zinc : noues, abergements, chéneaux et gouttières. Nous les façonnons et les soudons sur place, pour qu'ils durent aussi longtemps que la couverture.",
        "sections": [
            ("Nos travaux de zinguerie",
             "<ul>"
             "<li><strong>Gouttières et descentes</strong> en zinc, avec crochets, naissances et dauphins ;</li>"
             "<li><strong>chéneaux</strong> encaissés ou en bordure de toiture ;</li>"
             "<li><strong>noues</strong>, là où deux pans de toiture se rencontrent ;</li>"
             "<li><strong>abergements</strong> autour des cheminées, des lucarnes et des fenêtres de toit ;</li>"
             "<li><strong>rives et bandeaux</strong> qui protègent les pignons ;</li>"
             "<li><strong>bavettes d'appui</strong> sur les rebords de fenêtres.</li>"
             "</ul>"),
            ("Protéger le tuffeau",
             "<p>Le tuffeau est une pierre tendre qui craint les ruissellements : une gouttière qui déborde ou un appui de fenêtre sans protection finissent par noircir et effriter la façade. Des gouttières bien dimensionnées et des bavettes en zinc sur les appuis écartent l'eau de la pierre et prolongent la vie de la façade.</p>"),
            ("Pourquoi le zinc",
             "<p>Le zinc se façonne sur mesure, se soude à l'étain et dure plusieurs décennies quand il est bien posé et ventilé. Il s'accorde naturellement à l'ardoise. Il ne doit pas recevoir l'eau d'une couverture ou d'éléments en cuivre, qui le corrodent : nous en tenons compte lors du diagnostic.</p>"),
            ("Entretenir ses gouttières",
             "<p>Les feuilles et les mousses bouchent les naissances et font déborder les gouttières. Un nettoyage à l'automne, surtout près des arbres, évite la plupart des débordements. Une fuite à un raccord se traite le plus souvent par une ressoudure.</p>"),
        ],
        "faq": [
            ("Zinc, aluminium ou PVC ?",
             "Le zinc est le matériau traditionnel des toitures en ardoise de la région : il dure longtemps et se répare. L'aluminium laqué est une alternative sans soudure. Le PVC coûte moins cher mais vieillit plus vite au soleil et convient mal aux maisons de caractère."),
            ("Ma gouttière fuit à un raccord, faut-il tout changer ?",
             "Pas forcément. Un raccord décollé ou percé se ressoude. Nous remplaçons seulement les longueurs trop usées."),
            ("Pouvez-vous intervenir sur un chéneau encaissé ?",
             "Oui. Le chéneau est inspecté, puis réparé ou refait en zinc avec les pentes et les trop-pleins nécessaires."),
        ],
        "related": ["couverture-ardoise", "cheminees", "ravalement-facade"],
    },
    {
        "slug": "reparation-fuite-toiture",
        "nav": "Fuite de toiture",
        "short": "Recherche de fuite, mise hors d'eau et réparation durable.",
        "h1": "Fuite de toiture à Saumur : recherche et réparation",
        "title": "Fuite de toiture à Saumur : réparation | Tinten Couverture",
        "desc": "Fuite de toiture à Saumur : recherche de la cause, mise hors d'eau, bâchage et réparation durable des ardoises, tuiles et zingueries. Appelez le 06 69 57 82 88.",
        "photo": "rive-zinc-ardoise",
        "photo_alt": "Rive en zinc et ardoises posées sur écran sous-toiture, au bord d'un pan de toiture",
        "lead": "Une tache au plafond ou une goutte dans les combles ne disent pas toujours où l'eau entre. Nous cherchons la cause sur le toit et dans les combles, mettons la maison hors d'eau si besoin, puis réparons durablement.",
        "sections": [
            ("Les causes les plus fréquentes",
             "<ul>"
             "<li>une ardoise glissée ou cassée, une tuile fendue ;</li>"
             "<li>une noue en zinc percée ou mal recouverte ;</li>"
             "<li>un abergement de cheminée décollé ou un solin fissuré ;</li>"
             "<li>une fenêtre de toit mal raccordée à la couverture ;</li>"
             "<li>une gouttière ou un chéneau bouché qui déborde sous la toiture ;</li>"
             "<li>un faîtage ou une rive dégradés par le vent.</li>"
             "</ul>"),
            ("Que faire en attendant notre passage ?",
             "<ul>"
             "<li>placez un récipient sous l'écoulement et protégez les meubles ;</li>"
             "<li>si l'eau approche d'une installation électrique, coupez le circuit concerné ;</li>"
             "<li>prenez des photos des dégâts pour votre assureur ;</li>"
             "<li>ne montez pas sur le toit, surtout s'il est mouillé.</li>"
             "</ul>"),
            ("Notre intervention",
             "<p>Nous localisons l'entrée d'eau, sécurisons la toiture par un bâchage si la réparation ne peut pas être faite tout de suite, puis réparons l'élément en cause. Nous vous remettons des photos avant et après, utiles pour votre déclaration de sinistre.</p>"),
            ("Après une tempête",
             "<p>Déclarez le sinistre à votre assureur dans le délai prévu par votre contrat, souvent de cinq jours ouvrés. Gardez les photos et les éléments tombés. Nous établissons le devis de réparation à joindre à votre dossier.</p>"),
        ],
        "faq": [
            ("Sous quel délai pouvez-vous intervenir ?",
             "Cela dépend du planning et de l'urgence. En cas d'infiltration active, appelez-nous : nous cherchons d'abord à mettre la maison hors d'eau."),
            ("Mon assurance prend-elle en charge la réparation ?",
             "Les dégâts causés par une tempête ou un événement soudain sont généralement couverts, selon votre contrat. L'usure de la toiture ne l'est en général pas. Nous vous fournissons photos et devis pour votre dossier."),
            ("La fuite revient à chaque grosse pluie, pourquoi ?",
             "C'est souvent le signe d'un point de zinc ou d'un raccord en cause, plutôt que d'une ardoise. La recherche se fait alors en partant de l'endroit où l'eau apparaît et en remontant la pente."),
        ],
        "related": ["couverture-ardoise", "zinguerie-gouttieres", "cheminees"],
    },
    {
        "slug": "fenetres-de-toit",
        "nav": "Fenêtres de toit",
        "short": "Création et remplacement de fenêtres de toit, raccords étanches.",
        "h1": "Pose de fenêtres de toit à Saumur",
        "title": "Pose de fenêtre de toit (Velux) à Saumur | Tinten Couverture",
        "desc": "Pose et remplacement de fenêtres de toit à Saumur : création d'ouverture, raccord d'étanchéité adapté à l'ardoise ou à la tuile, habillage zinc. Devis gratuit.",
        "photo": "maison-toit-ardoise-fenetre-de-toit",
        "photo_alt": "Maison avec une toiture en ardoise neuve et une fenêtre de toit, camion de l'entreprise devant",
        "lead": "Une fenêtre de toit apporte de la lumière dans les combles, à condition d'être parfaitement raccordée à la couverture. Nous créons l'ouverture, posons la fenêtre et refaisons l'étanchéité autour, en ardoise comme en tuile.",
        "sections": [
            ("Création ou remplacement",
             "<p><strong>Création :</strong> nous ouvrons la couverture, renforçons la charpente autour de l'ouverture, posons la fenêtre avec son raccord d'étanchéité et reprenons l'ardoise ou les tuiles tout autour.</p>"
             "<p><strong>Remplacement :</strong> une fenêtre ancienne qui fuit ou laisse passer l'air se remplace, à dimensions identiques, souvent dans la journée. Si vous souhaitez une taille différente, la couverture est reprise en conséquence.</p>"),
            ("Bien placer la fenêtre",
             "<p>La hauteur de la fenêtre conditionne la vue et le confort : trop haute, on ne voit que le ciel ; trop basse, elle gêne le passage. Nous la positionnons avec vous en fonction de l'usage de la pièce, de la pente du toit et de l'emplacement des chevrons.</p>"),
            ("Les démarches",
             "<p>Créer une fenêtre de toit modifie l'aspect extérieur : une déclaration préalable est nécessaire en mairie. Dans le centre ancien de Saumur et aux abords des monuments historiques, l'Architecte des Bâtiments de France peut demander un modèle de type patrimoine, plus discret, à meneau central. Nous vous aidons à préparer les éléments techniques du dossier.</p>"),
        ],
        "faq": [
            ("Posez-vous uniquement des Velux ?",
             "Nous posons des fenêtres de toit de la marque Velux et des modèles équivalents, avec le raccord adapté à votre couverture."),
            ("Combien de temps dure la pose ?",
             "Un remplacement à l'identique se fait souvent dans la journée. Une création demande en général une à deux journées selon la couverture et les finitions intérieures."),
            ("Ma fenêtre de toit fuit, faut-il la changer ?",
             "Pas toujours. La fuite vient souvent du raccord d'étanchéité ou de la couverture autour. Nous vérifions avant de proposer un remplacement."),
        ],
        "related": ["couverture-ardoise", "renovation-toiture", "reparation-fuite-toiture"],
    },
    {
        "slug": "cheminees",
        "nav": "Souches de cheminée",
        "short": "Souches, couronnements, mitres, solins et abergements en zinc.",
        "h1": "Souches de cheminée : réparation et étanchéité",
        "title": "Souche de cheminée à Saumur : réparation | Tinten Couverture",
        "desc": "Réparation de souches de cheminée à Saumur : rejointoiement, couronnement, mitres, solins et abergements en zinc. Fin des fuites autour du conduit. Devis gratuit.",
        "photo": "ardoise-liteaux-cheminee",
        "photo_alt": "Pied de souche de cheminée en brique pendant la réfection de la couverture en ardoise",
        "lead": "La cheminée est l'un des points faibles d'une toiture : briques qui se délitent, couronnement fissuré, abergement qui se décolle. Nous réparons la souche et son étanchéité pour stopper les infiltrations autour du conduit.",
        "sections": [
            ("Les signes à surveiller",
             "<ul>"
             "<li>des joints creusés ou des briques qui s'effritent ;</li>"
             "<li>un couronnement fendu au sommet de la souche ;</li>"
             "<li>des mitres cassées ou absentes ;</li>"
             "<li>une tache d'humidité autour du conduit dans les combles ou au plafond ;</li>"
             "<li>des coulures noires sur la souche.</li>"
             "</ul>"),
            ("Nos interventions",
             "<ul>"
             "<li>rejointoiement et remplacement des briques abîmées ;</li>"
             "<li>réfection du couronnement ;</li>"
             "<li>remplacement des mitres et mitrons ;</li>"
             "<li>abergement en zinc neuf autour de la souche, ou reprise des solins ;</li>"
             "<li>démolition d'une souche inutilisée sous la couverture et reprise de l'ardoise ou des tuiles.</li>"
             "</ul>"
             "<p>Le ramonage reste l'affaire d'un ramoneur : nous intervenons sur la partie extérieure de la souche et son étanchéité.</p>"),
        ],
        "faq": [
            ("Peut-on supprimer une cheminée qui ne sert plus ?",
             "Oui. La souche est démolie jusque sous la couverture, le trou est refermé et la couverture reprise à l'identique. C'est une solution définitive contre les fuites autour d'un conduit inutilisé."),
            ("L'eau coule le long du conduit, d'où vient la fuite ?",
             "Le plus souvent de l'abergement ou des solins, parfois du couronnement qui laisse l'eau entrer dans la maçonnerie. Le diagnostic se fait sur le toit."),
        ],
        "related": ["zinguerie-gouttieres", "reparation-fuite-toiture", "couverture-ardoise"],
    },
    {
        "slug": "entretien-demoussage-toiture",
        "nav": "Nettoyage et démoussage",
        "short": "Démoussage doux, traitement, gouttières et contrôle de la toiture.",
        "h1": "Nettoyage et démoussage de toiture",
        "title": "Démoussage et nettoyage de toiture à Saumur | Tinten Couverture",
        "desc": "Démoussage de toiture à Saumur : nettoyage sans haute pression, traitement anti-mousse, hydrofuge sur tuiles, nettoyage des gouttières et contrôle de la couverture.",
        "photo": "couverture-ardoise-detail",
        "photo_alt": "Couverture en ardoise propre vue de près, sur une petite toiture",
        "lead": "La mousse retient l'eau, soulève les tuiles et bouche les gouttières. Un entretien régulier prolonge la vie de la couverture. Nous nettoyons sans abîmer et profitons du passage pour contrôler la toiture.",
        "sections": [
            ("Notre méthode",
             "<ul>"
             "<li>retrait des mousses par brossage ou à basse pression ;</li>"
             "<li>application d'un traitement anti-mousse, qui agit ensuite avec la pluie ;</li>"
             "<li>sur les tuiles en bon état, hydrofuge en option ;</li>"
             "<li>nettoyage des gouttières et des descentes ;</li>"
             "<li>contrôle des ardoises, des tuiles, du faîtage et des points de zinc, avec photos.</li>"
             "</ul>"
             "<p>Nous n'utilisons pas de nettoyeur haute pression sur les couvertures : il use la surface des tuiles et peut faire remonter l'eau sous les ardoises.</p>"),
            ("Ardoise ou tuile : pas le même entretien",
             "<p>L'ardoise naturelle n'absorbe presque pas l'eau : un démoussage doux suffit, sans hydrofuge. Les tuiles en terre cuite ou en béton sont plus poreuses : un hydrofuge peut limiter la reprise des mousses, à condition qu'elles soient saines.</p>"),
            ("À quelle fréquence ?",
             "<p>Cela dépend de l'exposition : un pan orienté au nord, à l'ombre d'arbres, se couvre plus vite qu'un pan au soleil. Un contrôle tous les quelques années permet de décider s'il faut intervenir. Le printemps et le début de l'automne, par temps sec, sont les meilleures périodes.</p>"),
        ],
        "faq": [
            ("Le démoussage abîme-t-il la toiture ?",
             "Pas avec une méthode douce. C'est la haute pression qui abîme les tuiles et déplace les ardoises."),
            ("L'hydrofuge est-il utile ?",
             "Sur des tuiles saines, il limite l'absorption d'eau et la reprise des mousses. Il est inutile sur l'ardoise naturelle et ne rattrape pas des tuiles déjà poreuses."),
            ("Combien de temps dure l'intervention ?",
             "Une à deux journées pour la plupart des maisons, selon la surface et l'accès."),
        ],
        "related": ["couverture-tuile", "zinguerie-gouttieres", "couverture-ardoise"],
    },
    # Pages reprises de l'ancien site (mêmes adresses), hors grille de l'accueil
    {
        "slug": "isolation-combles",
        "home": False,
        "nav": "Isolation des combles",
        "short": "Combles perdus ou aménagés : isolation au sol, sous les rampants ou par l'extérieur.",
        "h1": "Isolation des combles à Saumur",
        "title": "Isolation des combles à Saumur (49) | Tinten Couverture",
        "desc": "Isolation des combles perdus et aménagés à Saumur : laine soufflée ou en rouleaux, isolation des rampants ou par l'extérieur lors d'une réfection. Devis gratuit.",
        "photo": "ecran-sous-toiture-liteaux",
        "photo_alt": "Toiture ouverte au-dessus des combles : écran sous-toiture, contre-liteaux et liteaux",
        "lead": "Une toiture mal isolée laisse partir une grande part de la chaleur de la maison. Nous isolons les combles perdus et les combles aménagés, et nous profitons d'une réfection de toiture pour isoler par l'extérieur.",
        "sections": [
            ("Combles perdus ou combles aménagés",
             "<p>Les combles perdus, non habitables, s'isolent au sol : laine minérale ou ouate de cellulose soufflée, ou rouleaux posés en deux couches croisées. C'est la solution la plus simple et la plus rentable.</p>"
             "<p>Les combles aménagés s'isolent sous les rampants, entre et sous les chevrons, avec un pare-vapeur côté intérieur. Quand la couverture est refaite, l'isolant peut aussi se poser par l'extérieur, au-dessus des chevrons, sans perdre de place dans les pièces.</p>"),
            ("Pourquoi confier l'isolation à un couvreur",
             "<p>Une laine mouillée n'isole plus : isoler sous une toiture qui fuit, c'est gâcher l'isolant. Avant d'isoler, nous contrôlons la couverture, l'écran sous-toiture et la ventilation des combles. Une lame d'air ventilée sous la couverture et un pare-vapeur bien posé évitent la condensation, qui abîme la charpente.</p>"),
            ("Ce que nous vérifions avant les travaux",
             "<ul>"
             "<li>l'état de la couverture et de la charpente ;</li>"
             "<li>la ventilation de la toiture ;</li>"
             "<li>les gaines et les spots électriques à protéger ;</li>"
             "<li>l'accès aux combles et l'état du plancher ;</li>"
             "<li>l'épaisseur d'isolant à poser, indiquée sur le devis avec la résistance thermique visée.</li>"
             "</ul>"),
        ],
        "faq": [
            ("Quelle épaisseur d'isolant faut-il ?",
             "Elle dépend de l'isolant et de la performance visée. Pour des combles perdus, on vise couramment une résistance thermique d'au moins 7 m².K/W, soit une trentaine de centimètres de laine. Le devis indique l'isolant, l'épaisseur et la résistance obtenue."),
            ("Peut-on obtenir des aides ?",
             "Des aides publiques existent pour l'isolation, sous conditions de ressources et de performance. Elles exigent en général une entreprise certifiée RGE : renseignez-vous auprès de France Rénov' avant de signer un devis."),
            ("Faut-il refaire la toiture pour isoler les combles ?",
             "Non. Les combles perdus s'isolent par l'intérieur, sans toucher à la couverture. Si la toiture doit être refaite dans les prochaines années, il est en revanche intéressant de coupler les deux chantiers."),
        ],
        "related": ["renovation-toiture", "fenetres-de-toit", "reparation-fuite-toiture"],
    },
    {
        "slug": "etancheite-terrasse",
        "home": False,
        "nav": "Étanchéité de toit-terrasse",
        "short": "Toits plats de garages, d'extensions et de dépendances : membranes, relevés, évacuations.",
        "h1": "Étanchéité de toit-terrasse à Saumur",
        "title": "Étanchéité toit-terrasse et toit plat à Saumur | Tinten Couverture",
        "desc": "Étanchéité de toit-terrasse et de toit plat à Saumur : garages, extensions, dépendances. Recherche de fuite, membrane, relevés et évacuations. Devis gratuit.",
        "photo": "chenau-zinc",
        "photo_alt": "Chéneau en zinc le long d'un mur, pour l'évacuation des eaux de pluie",
        "lead": "Garages, extensions, dépendances : les toits plats sont les plus exposés aux infiltrations, car l'eau y stagne. Nous cherchons l'origine des fuites et refaisons l'étanchéité, des relevés jusqu'aux évacuations.",
        "sections": [
            ("D'où viennent les fuites d'un toit plat ?",
             "<ul>"
             "<li>une membrane fissurée, décollée ou boursouflée par l'âge et les écarts de température ;</li>"
             "<li>des relevés d'étanchéité décollés contre les murs et les acrotères ;</li>"
             "<li>des évacuations bouchées par les feuilles et les mousses, qui font stagner l'eau ;</li>"
             "<li>une pente insuffisante, qui laisse des flaques après la pluie ;</li>"
             "<li>des traversées mal reprises : ventilations, conduits, fixations de garde-corps.</li>"
             "</ul>"),
            ("Réparer ou refaire l'étanchéité",
             "<p>Une fuite localisée se répare par une reprise de la membrane et des relevés. Quand l'étanchéité est usée sur toute la surface, la réfection complète est plus sûre : dépose ou recouvrement de l'ancien revêtement selon son état, pose d'une membrane neuve adaptée au support, reprise des relevés, des évacuations et des finitions en zinc.</p>"),
            ("Entretenir pour durer",
             "<p>Un toit plat demande un contrôle régulier : nettoyage des évacuations et des chéneaux, surveillance des relevés et des joints. Un entretien simple, une à deux fois par an, évite la plupart des infiltrations.</p>"),
        ],
        "faq": [
            ("Que faire en cas de fuite sur un toit plat ?",
             "Vérifiez d'abord que les évacuations ne sont pas bouchées : c'est une cause fréquente. Si la fuite persiste, appelez-nous : nous localisons l'infiltration avant de proposer une réparation ou une réfection."),
            ("Peut-on marcher sur un toit-terrasse ?",
             "Seulement s'il est conçu pour : une terrasse accessible reçoit une protection adaptée, comme des dalles sur plots. Une toiture non accessible ne supporte que les passages d'entretien."),
            ("Faut-il refaire toute l'étanchéité pour une seule fuite ?",
             "Pas forcément. Si la membrane est saine autour de la fuite, une reprise localisée suffit. Nous vous le disons après la visite."),
        ],
        "related": ["reparation-fuite-toiture", "zinguerie-gouttieres", "entretien-demoussage-toiture"],
    },
    {
        "slug": "ravalement-facade",
        "nav": "Ravalement de façade",
        "short": "Nettoyage, réparation et enduits adaptés au tuffeau et aux façades anciennes.",
        "h1": "Ravalement de façade à Saumur",
        "title": "Ravalement de façade à Saumur et tuffeau | Tinten Couverture",
        "desc": "Ravalement de façade à Saumur : nettoyage, réparation, enduits à la chaux et peintures respirantes adaptés au tuffeau. Protection zinc des appuis. Devis gratuit.",
        "photo": "chantier-facade-echafaudage",
        "photo_alt": "Maison sous échafaudage pendant des travaux, camion de l'entreprise devant la façade",
        "lead": "Une façade en bon état protège les murs autant que la toiture protège la maison. Nous nettoyons, réparons et protégeons les façades, avec des matériaux compatibles avec le tuffeau et les maçonneries anciennes.",
        "sections": [
            ("Ce que comprend un ravalement",
             "<ul>"
             "<li>nettoyage adapté au support, sans décaper la pierre ;</li>"
             "<li>réparation des fissures et des parties dégradées ;</li>"
             "<li>reprise des enduits, de préférence à la chaux sur les murs anciens ;</li>"
             "<li>peinture ou badigeon perméable à la vapeur d'eau ;</li>"
             "<li>protection des appuis et des bandeaux par des bavettes en zinc.</li>"
             "</ul>"),
            ("Tuffeau et murs anciens : laisser respirer",
             "<p>Le tuffeau et les maçonneries anciennes ont besoin d'évacuer l'humidité. Un enduit au ciment ou une peinture étanche l'enferment dans le mur : la pierre se dégrade derrière. Nous utilisons des enduits à la chaux et des finitions respirantes sur ces supports.</p>"),
            ("Les démarches",
             "<p>Un ravalement demande une déclaration préalable dans les secteurs protégés, comme le centre ancien de Saumur et les abords des monuments historiques, ou lorsque la commune l'a décidé. Renseignez-vous en mairie ; nous vous fournissons la description technique des travaux.</p>"),
        ],
        "faq": [
            ("Combien de temps dure un ravalement ?",
             "De quelques jours à quelques semaines selon la surface, l'état de la façade et la météo. Le planning figure sur le devis."),
            ("Peut-on faire le ravalement en même temps que la toiture ?",
             "Oui, et c'est souvent plus économique : l'échafaudage sert aux deux chantiers et la zinguerie est reprise dans la foulée."),
            ("Quelle saison choisir ?",
             "Le printemps et l'automne, hors périodes de gel et de fortes chaleurs, conviennent le mieux aux enduits et aux peintures."),
        ],
        "related": ["zinguerie-gouttieres", "renovation-toiture", "cheminees"],
    },
    {
        "slug": "traitement-humidite",
        "home": False,
        "nav": "Traitement de l'humidité",
        "short": "Remontées capillaires, murs en tuffeau, façades qui boivent la pluie.",
        "h1": "Traitement de l'humidité des murs à Saumur",
        "title": "Traitement de l'humidité des murs à Saumur | Tinten Couverture",
        "desc": "Traitement de l'humidité des murs à Saumur : remontées capillaires, murs en tuffeau, zinguerie, enduits à la chaux et hydrofuge respirant. Visite et devis gratuits.",
        "photo": "bavette-zinc-appui-fenetre",
        "photo_alt": "Bavette en zinc posée sur l'appui d'une fenêtre pour éloigner l'eau de la façade",
        "lead": "Salpêtre, enduits qui cloquent, pierre qui s'effrite en pied de mur : l'humidité abîme les maisons en tuffeau. Avant de traiter, nous cherchons d'où vient l'eau, car le bon traitement dépend de la cause.",
        "sections": [
            ("D'où vient l'humidité ?",
             "<ul>"
             "<li><strong>Par le haut</strong> : gouttière percée, chéneau bouché, appui de fenêtre sans bavette, qui déversent l'eau sur la façade.</li>"
             "<li><strong>Par le sol</strong> : remontées capillaires, quand l'eau du terrain monte dans la base des murs.</li>"
             "<li><strong>Par la façade</strong> : enduit fissuré ou pierre poreuse qui absorbent la pluie battante.</li>"
             "<li><strong>Par l'intérieur</strong> : condensation dans une maison mal ventilée.</li>"
             "</ul>"
             "<p>Couvreurs et zingueurs, nous vérifions d'abord l'évacuation de l'eau de toiture, une cause fréquente, avant de toucher au mur.</p>"),
            ("Les traitements",
             "<ul>"
             "<li>reprise de la zinguerie et pose de bavettes pour éloigner l'eau des murs ;</li>"
             "<li>barrière contre les remontées capillaires, injectée à la base des murs ;</li>"
             "<li>remplacement des enduits au ciment par des enduits à la chaux, qui laissent le mur sécher ;</li>"
             "<li>traitement hydrofuge respirant des façades exposées à la pluie.</li>"
             "</ul>"),
            ("Tuffeau : ne pas enfermer l'eau",
             "<p>Le tuffeau est une pierre tendre et poreuse. Un enduit au ciment, une peinture étanche ou des joints trop durs bloquent l'humidité dans la pierre, qui finit par se déliter. Sur ces murs, chaque produit doit rester perméable à la vapeur d'eau.</p>"),
        ],
        "faq": [
            ("Un hydrofuge suffit-il contre l'humidité ?",
             "Non, s'il s'agit de remontées capillaires ou d'une gouttière qui fuit : l'hydrofuge protège seulement la façade de la pluie. Il doit aussi rester respirant, pour ne pas enfermer l'eau dans le mur."),
            ("Combien de temps faut-il pour qu'un mur sèche ?",
             "Souvent plusieurs mois après le traitement, selon l'épaisseur du mur et la saison. Les enduits intérieurs abîmés se refont une fois le mur sec."),
            ("La visite est-elle payante ?",
             "Non. Nous venons voir, nous cherchons l'origine de l'humidité et nous vous remettons un devis gratuit."),
        ],
        "related": ["ravalement-facade", "zinguerie-gouttieres", "reparation-fissures"],
    },
    {
        "slug": "reparation-fissures",
        "home": False,
        "nav": "Fissures de façade",
        "short": "Diagnostic et réparation des fissures, des enduits et des joints de façade.",
        "h1": "Réparation de fissures de façade à Saumur",
        "title": "Réparation de fissures de façade à Saumur | Tinten Couverture",
        "desc": "Réparation des fissures de façade à Saumur : diagnostic, fissures d'enduit, joints et tuffeau, enduits à la chaux, ravalement. Visite et devis gratuits.",
        "photo": "chantier-facade-echafaudage",
        "photo_alt": "Maison sous échafaudage pendant des travaux de façade",
        "lead": "Une fissure laisse entrer l'eau dans le mur, et l'eau l'agrandit à chaque hiver. Nous examinons chaque fissure pour savoir si elle touche l'enduit ou la structure, puis nous la réparons avec des matériaux compatibles avec le mur.",
        "sections": [
            ("Toutes les fissures ne se valent pas",
             "<ul>"
             "<li><strong>Le faïençage</strong> : un réseau de fines craquelures dans l'enduit, souvent lié à son séchage.</li>"
             "<li><strong>Les microfissures</strong>, de moins de 0,2 mm, qui restent superficielles.</li>"
             "<li><strong>Les fissures ouvertes</strong>, de 0,2 à 2 mm, qui laissent entrer l'eau et doivent être traitées.</li>"
             "<li><strong>Les lézardes</strong>, au-delà de 2 mm, qui peuvent signaler un mouvement du bâtiment.</li>"
             "</ul>"
             "<p>Une fissure qui s'élargit, traverse le mur ou part des angles des ouvertures demande l'avis d'un bureau d'études avant toute réparation de surface. Nous vous le disons lors de la visite.</p>"),
            ("Comment nous réparons",
             "<p>La fissure est ouverte et nettoyée, puis comblée avec un mortier ou un mastic adapté au support. Sur un enduit, une toile d'armature limite le risque de reprise. Sur le tuffeau, les joints sont refaits à la chaux et les pierres trop abîmées peuvent être remplacées. La finition se raccorde au reste de la façade ; quand les fissures sont nombreuses, un ravalement complet est souvent plus durable.</p>"),
            ("Traiter aussi la cause",
             "<p>Une gouttière qui déborde, un appui sans bavette ou une descente qui se déverse au pied du mur fragilisent la façade. Nous vérifions la zinguerie en même temps que les fissures.</p>"),
        ],
        "faq": [
            ("Une fissure sur la façade est-elle grave ?",
             "La plupart des fissures fines ne touchent que l'enduit. Une fissure large, qui s'agrandit ou qui traverse le mur peut révéler un problème de structure et doit être examinée avant d'être rebouchée."),
            ("Peut-on simplement reboucher une fissure ?",
             "Un rebouchage en surface, sans préparation ni traitement de la cause, ne tient pas : la fissure réapparaît. Elle doit être ouverte, nettoyée et comblée avec un produit compatible avec le mur."),
            ("Faut-il une autorisation ?",
             "Une réparation ponctuelle n'en demande en général pas. Un ravalement complet peut nécessiter une déclaration préalable, notamment en secteur protégé à Saumur."),
        ],
        "related": ["ravalement-facade", "traitement-humidite", "zinguerie-gouttieres"],
    },
]

SERVICE_BY_SLUG = {s["slug"]: s for s in SERVICES}

# ---------------------------------------------------------------------------
# Communes
# ---------------------------------------------------------------------------

CITIES = [
    {
        "slug": "couvreur-saumur",
        "name": "Saumur",
        "cp": "49400",
        "dept": "Maine-et-Loire",
        "dist": None,
        "title": "Couvreur à Saumur (49400) | Tinten Couverture",
        "desc": "Couvreur à Saumur depuis 2009 : couverture ardoise et tuile, zinguerie, fuites, cheminées et ravalement. Basés boulevard des Demoiselles. Devis gratuit après visite.",
        "intro": "Tinten Couverture est installée à Saumur, au 24 boulevard des Demoiselles. Nous intervenons dans toute la commune, du centre ancien aux quartiers de Saint-Hilaire-Saint-Florent, Bagneux, Dampierre-sur-Loire et Saint-Lambert-des-Levées.",
        "local": [
            ("Les toitures de Saumur",
             "<p>Maisons de ville en tuffeau, hôtels particuliers, demeures des coteaux et pavillons plus récents : Saumur réunit presque tous les types de toitures de la région. L'ardoise domine, avec ses lucarnes, ses souches de cheminée et une zinguerie abondante. Les tuiles se retrouvent sur les dépendances et les constructions du XXe siècle.</p>"),
            ("Travaux en centre ancien",
             "<p>Une partie de Saumur est un secteur protégé, et la ville se trouve dans le périmètre du Val de Loire inscrit au patrimoine mondial de l'Unesco. Dans le centre ancien et aux abords des monuments historiques, les travaux qui modifient l'aspect d'une toiture ou d'une façade passent par une déclaration préalable et l'avis de l'Architecte des Bâtiments de France. Nous vous indiquons les démarches au moment du devis.</p>"),
        ],
        "works": ["renovation-toiture", "couverture-ardoise", "zinguerie-gouttieres", "fenetres-de-toit", "cheminees", "reparation-fuite-toiture"],
        "nearby": ["Saint-Hilaire-Saint-Florent", "Bagneux", "Dampierre-sur-Loire", "Saint-Lambert-des-Levées", "Varrains", "Chacé", "Distré", "Allonnes"],
        "photo": "toiture-ardoise-lucarne-saumur",
        "photo_alt": "Toiture en ardoise avec lucarne et souche de cheminée à Saumur",
    },
    {
        "slug": "couvreur-doue-en-anjou",
        "name": "Doué-en-Anjou",
        "cp": "49700",
        "dept": "Maine-et-Loire",
        "dist": 17,
        "title": "Couvreur à Doué-en-Anjou (49700) | Tinten Couverture",
        "desc": "Couvreur à Doué-en-Anjou et Doué-la-Fontaine : couverture ardoise et tuile, zinguerie, fuites et entretien de toiture. Entreprise de Saumur, à 17 km. Devis gratuit.",
        "intro": "Nous intervenons à Doué-la-Fontaine et dans les communes déléguées de Doué-en-Anjou, à une vingtaine de minutes de notre dépôt de Saumur.",
        "local": [
            ("Les toitures du Douessin",
             "<p>Le Douessin mêle maisons de bourg en pierre, anciennes fermes et pavillons récents. On y trouve de l'ardoise sur les maisons anciennes et beaucoup de tuiles sur les longères, les granges et les constructions plus récentes. Les bâtiments agricoles reconvertis demandent souvent une reprise complète de la charpente et de la couverture.</p>"),
            ("Ce qu'on nous demande le plus",
             "<p>Remaniement de couvertures en tuiles, réfection de toitures d'anciennes dépendances, remplacement de gouttières et démoussage des pans exposés au nord.</p>"),
        ],
        "works": ["couverture-tuile", "renovation-toiture", "entretien-demoussage-toiture", "zinguerie-gouttieres"],
        "nearby": ["Doué-la-Fontaine", "Les Verchers-sur-Layon", "Concourson-sur-Layon", "Louresse-Rochemenier", "Denezé-sous-Doué", "Les Ulmes"],
        "photo": "lucarne-tuiles-chantier",
        "photo_alt": "Lucarne couverte de tuiles en cours de réfection",
    },
    {
        "slug": "couvreur-montreuil-bellay",
        "name": "Montreuil-Bellay",
        "cp": "49260",
        "dept": "Maine-et-Loire",
        "dist": 17,
        "title": "Couvreur à Montreuil-Bellay (49260) | Tinten Couverture",
        "desc": "Couvreur à Montreuil-Bellay : ardoise, tuiles, zinguerie, souches de cheminée et fuites de toiture. Entreprise de Saumur, à 17 km au sud. Devis gratuit.",
        "intro": "Montreuil-Bellay se trouve à environ 17 km au sud de Saumur, sur les bords du Thouet. Nous y intervenons régulièrement, dans la ville comme dans les hameaux alentour.",
        "local": [
            ("Une ville au patrimoine protégé",
             "<p>Le château, les remparts et le centre ancien donnent à Montreuil-Bellay un caractère fort. Aux abords des monuments historiques, la réfection d'une toiture ou la création d'une fenêtre de toit demandent l'avis de l'Architecte des Bâtiments de France : nous vous indiquons les démarches au moment du devis.</p>"),
            ("Les toitures de Montreuil-Bellay",
             "<p>Ardoise et tuffeau dans le centre, tuiles plus fréquentes sur les maisons récentes et les bâtiments agricoles. Les souches de cheminée et la zinguerie des maisons anciennes font partie des réparations les plus demandées.</p>"),
        ],
        "works": ["couverture-ardoise", "cheminees", "zinguerie-gouttieres", "reparation-fuite-toiture"],
        "nearby": ["Le Puy-Notre-Dame", "Le Coudray-Macouard", "Artannes-sur-Thouet", "Distré", "Vaudelnay", "Épieds"],
        "photo": "toiture-ardoise-cheminees",
        "photo_alt": "Toiture en ardoise avec souches de cheminée en brique",
    },
    {
        "slug": "couvreur-longue-jumelles",
        "name": "Longué-Jumelles",
        "cp": "49160",
        "dept": "Maine-et-Loire",
        "dist": 16,
        "title": "Couvreur à Longué-Jumelles (49160) | Tinten Couverture",
        "desc": "Couvreur à Longué-Jumelles : réfection de toiture, ardoise, tuiles, zinguerie et démoussage. Entreprise de Saumur, à 16 km au nord. Devis gratuit après visite.",
        "intro": "Longué-Jumelles est à environ 16 km au nord de Saumur, de l'autre côté de la Loire. Nous y intervenons pour les particuliers comme pour les commerces du bourg.",
        "local": [
            ("Les toitures de Longué-Jumelles",
             "<p>Le bourg compte de nombreuses maisons anciennes couvertes d'ardoise, et des quartiers pavillonnaires en tuiles. Les anciennes fermes de la vallée de l'Authion ont souvent des dépendances dont la couverture est à reprendre.</p>"),
            ("Ce qu'on nous demande le plus",
             "<p>Réfection de couvertures en ardoise, remplacement de gouttières en zinc, démoussage et contrôle de toitures, pose de fenêtres de toit pour aménager les combles.</p>"),
        ],
        "works": ["renovation-toiture", "couverture-ardoise", "fenetres-de-toit", "entretien-demoussage-toiture"],
        "nearby": ["Blou", "Vivy", "Saint-Philbert-du-Peuple", "Vernantes", "Les Rosiers-sur-Loire", "Saint-Clément-des-Levées"],
        "photo": "maison-toit-ardoise-fenetre-de-toit",
        "photo_alt": "Maison à la toiture en ardoise neuve avec fenêtre de toit",
    },
    {
        "slug": "couvreur-gennes-val-de-loire",
        "name": "Gennes-Val-de-Loire",
        "cp": "49350",
        "dept": "Maine-et-Loire",
        "dist": 17,
        "title": "Couvreur à Gennes-Val-de-Loire (49350) | Tinten Couverture",
        "desc": "Couvreur à Gennes-Val-de-Loire : Gennes, Les Rosiers-sur-Loire, Chênehutte-Trèves-Cunault. Ardoise, tuffeau, zinguerie et fuites de toiture. Devis gratuit.",
        "intro": "En aval de Saumur, le long de la Loire, nous intervenons à Gennes, aux Rosiers-sur-Loire, à Chênehutte-Trèves-Cunault, au Thoureil et dans les autres communes déléguées de Gennes-Val-de-Loire.",
        "local": [
            ("Ardoise et tuffeau des bords de Loire",
             "<p>Les villages de la rive gauche, adossés au coteau, et ceux de la levée, sur la rive droite, sont presque tous couverts d'ardoise. Les maisons de bord de Loire subissent le vent et l'humidité : faîtages, rives et zinguerie y travaillent davantage qu'ailleurs.</p>"),
            ("Patrimoine et démarches",
             "<p>Le prieuré de Cunault et les nombreux édifices anciens créent des périmètres de protection. Nous vérifions avec vous si les travaux demandent l'avis de l'Architecte des Bâtiments de France.</p>"),
        ],
        "works": ["couverture-ardoise", "zinguerie-gouttieres", "reparation-fuite-toiture", "ravalement-facade"],
        "nearby": ["Gennes", "Les Rosiers-sur-Loire", "Chênehutte-Trèves-Cunault", "Le Thoureil", "Grézillé", "Saint-Georges-des-Sept-Voies"],
        "photo": "noue-zinc-ardoise",
        "photo_alt": "Noue en zinc entre deux pans d'ardoise",
    },
    {
        "slug": "couvreur-fontevraud-l-abbaye",
        "name": "Fontevraud-l'Abbaye",
        "cp": "49590",
        "dept": "Maine-et-Loire",
        "dist": 14,
        "title": "Couvreur à Fontevraud-l'Abbaye (49590) | Tinten Couverture",
        "desc": "Couvreur à Fontevraud-l'Abbaye, Montsoreau et Turquant : ardoise, tuffeau, zinguerie et fenêtres de toit en secteur protégé. Entreprise de Saumur. Devis gratuit.",
        "intro": "Fontevraud-l'Abbaye est à environ 14 km de Saumur. Nous intervenons dans le village et les communes voisines de Montsoreau, Turquant et Candes-Saint-Martin.",
        "local": [
            ("Toitures autour de l'abbaye",
             "<p>Maisons en tuffeau, toits d'ardoise et lucarnes : le village vit autour de l'abbaye royale. Aux abords du monument, les travaux de toiture et de façade sont soumis à l'avis de l'Architecte des Bâtiments de France, qui peut demander des matériaux et des fenêtres de toit adaptés au site.</p>"),
            ("Ce qu'on nous demande le plus",
             "<p>Réparation d'ardoises, zinguerie de lucarnes, souches de cheminée, et protection des façades en tuffeau par des gouttières et des bavettes en zinc.</p>"),
        ],
        "works": ["couverture-ardoise", "zinguerie-gouttieres", "cheminees", "fenetres-de-toit"],
        "nearby": ["Montsoreau", "Turquant", "Candes-Saint-Martin", "Parnay", "Souzay-Champigny", "Couziers"],
        "photo": "bavette-zinc-appui-fenetre",
        "photo_alt": "Bavette en zinc neuve posée sur l'appui d'une fenêtre",
    },
    {
        "slug": "couvreur-chinon",
        "name": "Chinon",
        "cp": "37500",
        "dept": "Indre-et-Loire",
        "dist": 30,
        "title": "Couvreur à Chinon (37500) | Tinten Couverture",
        "desc": "Couvreur intervenant à Chinon et dans le Chinonais : couverture ardoise, tuffeau, zinguerie, cheminées et fuites. Entreprise de Saumur, à 30 km. Devis gratuit.",
        "intro": "Chinon est à environ 30 km à l'est de Saumur, en Indre-et-Loire. Nous y intervenons, ainsi que dans les communes du Chinonais situées dans notre rayon de 40 km.",
        "local": [
            ("Les toitures de Chinon",
             "<p>Au pied de la forteresse, le centre ancien de Chinon aligne maisons en tuffeau, pans de bois et toits d'ardoise. Comme à Saumur, ce secteur est protégé : les travaux qui modifient l'aspect des toitures passent par l'Architecte des Bâtiments de France.</p>"),
            ("Ce qu'on nous demande le plus",
             "<p>Réfection et réparation de couvertures en ardoise, zinguerie des lucarnes et des souches, fenêtres de toit de type patrimoine.</p>"),
        ],
        "works": ["couverture-ardoise", "renovation-toiture", "zinguerie-gouttieres", "fenetres-de-toit"],
        "nearby": ["Beaumont-en-Véron", "Avoine", "Savigny-en-Véron", "Cinais", "Seuilly", "Huismes"],
        "photo": "toiture-ardoise-lucarne-saumur",
        "photo_alt": "Lucarne et couverture en ardoise refaites",
    },
    {
        "slug": "couvreur-loudun",
        "name": "Loudun",
        "cp": "86200",
        "dept": "Vienne",
        "dist": 30,
        "title": "Couvreur à Loudun (86200) | Tinten Couverture",
        "desc": "Couvreur intervenant à Loudun et dans le Loudunais : couverture ardoise et tuiles, réfection, zinguerie, démoussage. Entreprise de Saumur, à 30 km. Devis gratuit.",
        "intro": "Loudun, dans la Vienne, est à environ 30 km au sud-est de Saumur. Nous y intervenons ainsi que dans les communes du Loudunais proches.",
        "local": [
            ("Les toitures du Loudunais",
             "<p>Le Loudunais est une terre de transition : l'ardoise couvre les maisons anciennes de la ville et des bourgs, tandis que la tuile gagne du terrain sur les fermes et en allant vers le sud. Nous travaillons les deux matériaux, avec la zinguerie qui va avec.</p>"),
            ("Ce qu'on nous demande le plus",
             "<p>Remaniement et réfection de toitures en tuiles, réparation d'ardoises, démoussage et remplacement de gouttières.</p>"),
        ],
        "works": ["couverture-tuile", "couverture-ardoise", "entretien-demoussage-toiture", "zinguerie-gouttieres"],
        "nearby": ["Les Trois-Moutiers", "Ternay", "Bournand", "Roiffé", "Glénouze", "Saix"],
        "photo": "pignon-lucarne-tuiles",
        "photo_alt": "Pignon de lucarne couvert de tuiles avec rives en terre cuite",
    },
    {
        "slug": "couvreur-thouars",
        "name": "Thouars",
        "cp": "79100",
        "dept": "Deux-Sèvres",
        "dist": 37,
        "title": "Couvreur à Thouars (79100) | Tinten Couverture",
        "desc": "Couvreur intervenant à Thouars et dans le Thouarsais : couverture tuiles et ardoise, réfection, zinguerie et fuites de toiture. Entreprise de Saumur. Devis gratuit.",
        "intro": "Thouars, dans les Deux-Sèvres, est à environ 37 km au sud de Saumur, à la limite de notre secteur. Nous y intervenons pour les chantiers de couverture et de zinguerie.",
        "local": [
            ("Les toitures du Thouarsais",
             "<p>La vieille ville, perchée au-dessus du Thouet autour du château, garde de nombreuses toitures en ardoise. Dans les quartiers plus récents et les campagnes alentour, la tuile est majoritaire.</p>"),
            ("Ce qu'on nous demande le plus",
             "<p>Réfection de toitures en tuiles, reprise de faîtages et de rives après coup de vent, gouttières et descentes en zinc.</p>"),
        ],
        "works": ["couverture-tuile", "renovation-toiture", "reparation-fuite-toiture", "zinguerie-gouttieres"],
        "nearby": ["Saint-Jean-de-Thouars", "Louzy", "Sainte-Verge", "Mauzé-Thouarsais", "Loretz-d'Argenton", "Plaine-et-Vallées"],
        "photo": "chantier-toiture-echafaudage",
        "photo_alt": "Chantier de toiture sous échafaudage avec le camion de l'entreprise",
    },
    # Page reprise de l'ancien site (même adresse), au-delà du rayon habituel
    {
        "slug": "couvreur-angers",
        "name": "Angers",
        "cp": "49000",
        "dept": "Maine-et-Loire",
        "dist": 65,
        "title": "Couvreur à Angers (49000) | Tinten Couverture",
        "desc": "Couvreur intervenant à Angers : réfection de toiture en ardoise, zinguerie, fenêtres de toit et fuites. Entreprise de Saumur, sur rendez-vous. Devis gratuit.",
        "intro": "Angers est à environ 65 km de Saumur par la route, au-delà de notre secteur habituel de 40 km. Nous y intervenons sur rendez-vous pour des chantiers de toiture : appelez-nous pour vérifier nos disponibilités.",
        "local": [
            ("Les toitures d'Angers",
             "<p>Surnommée la « ville noire », Angers doit son allure à l'ardoise de Trélazé, extraite à ses portes, qui couvre la plupart de ses toits. Maisons de ville, hôtels particuliers du centre et pavillons des quartiers résidentiels partagent cette tradition de l'ardoise, avec une zinguerie abondante.</p>"),
            ("Patrimoine et démarches",
             "<p>Le centre ancien d'Angers compte de nombreux monuments historiques. À leurs abords, les travaux qui modifient l'aspect d'une toiture ou d'une façade demandent une autorisation d'urbanisme et l'avis de l'Architecte des Bâtiments de France. Nous vous indiquons les démarches au moment du devis.</p>"),
        ],
        "works": ["renovation-toiture", "couverture-ardoise", "zinguerie-gouttieres", "fenetres-de-toit"],
        "nearby": ["Trélazé", "Les Ponts-de-Cé", "Saint-Barthélemy-d'Anjou", "Loire-Authion", "Brissac Loire Aubance", "Mazé-Milon"],
        "photo": "couverture-ardoise-detail",
        "photo_alt": "Petite toiture en ardoise naturelle terminée",
    },
]

# Communes citées sur la page zone, sans page dédiée
ZONE_EXTRA = {
    "Autour de Saumur": ["Allonnes", "Brain-sur-Allonnes", "Varennes-sur-Loire", "Vivy", "Varrains", "Chacé", "Distré", "Artannes-sur-Thouet", "Le Coudray-Macouard", "Vaudelnay", "Bellevigne-les-Châteaux"],
    "Vers l'est et la Touraine": ["Montsoreau", "Turquant", "Parnay", "Souzay-Champigny", "Candes-Saint-Martin", "Bourgueil", "Avoine"],
    "Vers le nord et la vallée": ["Vernantes", "Blou", "Beaufort-en-Anjou", "Les Rosiers-sur-Loire"],
}

# ---------------------------------------------------------------------------
# Accueil
# ---------------------------------------------------------------------------

HOME = {
    "title": "Couvreur à Saumur (49) – Ardoise, tuile, zinguerie | Tinten Couverture",
    "desc": "Couvreur à Saumur depuis 2009 : ardoise, tuile, zinguerie, fuites, cheminées, fenêtres de toit et ravalement, dans un rayon de 40 km. Devis gratuit.",
    "h1": "Couvreur à Saumur",
    "lead": "Couverture en ardoise et en tuile, zinguerie et ravalement, pour les maisons du Saumurois depuis 2009.",
    "faq": [
        ("Le devis est-il gratuit ?",
         "Oui. Nous venons voir la toiture, puis nous vous remettons un devis détaillé, gratuit et sans engagement."),
        ("Dans quelles communes intervenez-vous ?",
         "À Saumur et dans un rayon d'environ 40 km : Doué-en-Anjou, Montreuil-Bellay, Longué-Jumelles, Gennes-Val-de-Loire, Fontevraud-l'Abbaye, Chinon, Loudun, Thouars et les communes voisines."),
        ("Quand faut-il refaire sa toiture plutôt que la réparer ?",
         "Quand les fuites se multiplient, que les ardoises glissent ou que les tuiles deviennent poreuses sur l'ensemble des pans. Une réparation ciblée suffit souvent pour un problème localisé : nous vous le disons lors de la visite."),
        ("Les travaux sont-ils couverts par une garantie ?",
         "Les travaux de couverture relèvent de la garantie décennale. Les références de notre assurance figurent sur chaque devis et chaque facture."),
        ("Faut-il une autorisation pour des travaux de toiture à Saumur ?",
         "Une réfection à l'identique n'en demande en général pas. Un changement d'aspect (matériau, fenêtre de toit) passe par une déclaration préalable, avec l'avis de l'Architecte des Bâtiments de France en secteur protégé."),
    ],
}

PROCESS = [
    ("Vous nous appelez", "Par téléphone ou avec le formulaire. Décrivez le problème, une photo aide beaucoup."),
    ("Nous venons voir", "Visite de la toiture et des combles, prise de mesures, explications sur place."),
    ("Vous recevez le devis", "Détaillé, gratuit, sans engagement, avec les démarches éventuelles en mairie."),
    ("Nous réalisons les travaux", "Chantier protégé chaque soir, nettoyé à la fin, photos avant et après."),
]

# Schéma « anatomie d'une toiture en ardoise » : légende, du dessus vers la charpente.
ANATOMY = [
    ("Ardoise naturelle", "Posée au crochet inox, chaque ardoise recouvre les deux rangs inférieurs.", "couverture-ardoise"),
    ("Liteaux", "Tasseaux horizontaux qui portent les ardoises, à espacement régulier.", "renovation-toiture"),
    ("Contre-liteaux", "Ils créent une lame d'air qui ventile la couverture et évacue l'humidité.", "renovation-toiture"),
    ("Écran sous-toiture", "Membrane respirante : seconde barrière contre l'eau et la poussière.", "renovation-toiture"),
    ("Chevrons", "La charpente, contrôlée et reprise à chaque réfection.", "renovation-toiture"),
    ("Gouttière en zinc", "À l'égout du toit, elle éloigne l'eau des façades en tuffeau.", "zinguerie-gouttieres"),
]

GALLERY = [
    ("toiture-ardoise-lucarne-saumur", "Couverture en ardoise et lucarne habillée de zinc"),
    ("maison-toit-ardoise-fenetre-de-toit", "Toiture en ardoise refaite avec fenêtre de toit"),
    ("toiture-ardoise-cheminees", "Ardoise naturelle et souches de cheminée en brique"),
    ("noue-zinc-ardoise", "Noue en zinc sur liteaux, avant la pose de l'ardoise"),
    ("ecran-sous-toiture-liteaux", "Écran sous-toiture, contre-liteaux et liteaux neufs"),
    ("bavette-zinc-appui-fenetre", "Bavette en zinc protégeant un appui de fenêtre"),
    ("lucarne-tuiles-chantier", "Lucarne en tuiles pendant la réfection"),
    ("rive-zinc-ardoise", "Rive en zinc et ardoises sur écran sous-toiture"),
    ("ardoise-liteaux-cheminee", "Reprise de couverture au pied d'une souche"),
    ("couverture-ardoise-detail", "Petite toiture en ardoise terminée"),
    ("pignon-lucarne-tuiles", "Pignon de lucarne et rives en tuiles"),
    ("chenau-zinc", "Chéneau en zinc le long d'un mur"),
    ("chantier-facade-echafaudage", "Chantier sous échafaudage"),
    ("chantier-toiture-echafaudage", "Réfection de toiture d'une longère"),
]
