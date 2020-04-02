from protocole1.models import Idea, IdeasGroup

groupe = {}
items = {}
groupe["A"] = "amortir le choc"
items["A"] = [
    "lancer l'œuf sur un matelas posé au sol",
    "lancer l'œuf sur de la mousse posée au sol",
    "Lancer l'œuf sur un amas de plumes posées au sol",
    "lancer l'œuf sur beaucoup de coton posé au sol",
    "lancer l'œuf sur beaucoup d'oreillers",
    "Mettre plein de ressorts au sol de manière à ce que la chute de l'œuf soit amortie",
    "Mettre des trampolines au sol pour amortir la chute de l'œuf",
    "Lancer l'œuf dans une piscine",
    "Lancer l'œuf dans un jacuzzi",
    "Lancer l'œuf dans une piscine de balles",
]
groupe["B"] = "protéger l'oeuf"
items["B"] = [
    "Envelopper l'œuf de plusieurs draps et couvertures pour le proteger",
    "Protège l'œuf en le mettant dans une boite",
    "Entouler l'œuf de papier bull pour le proteger",
    "Entourer l'œuf de mousse pour le proteger",
    "Mettre des ressorts tout autour de l'œuf pour faire une protection rebondissante",
    "Mettre l'œuf dans une balle en caoutchouc pour faire une protection rebondissante",
    "Mettre l'œuf dans un ballon de foot pour faire une protection rebondissante",
]
groupe["C"] = "Ralentir la chute"
items["C"] = [
    "Mettre l'œuf dans un avion télécommandé pour qu'il descende doucement",
    "Mettre l'œuf dans un hélicoptère télécommandé pour qu'il descende doucement",
    "Mettre l'œuf dans un drone pour qu'il descende doucement",
    "Lancer l'œuf sur un grand nombre de linges étendus les uns en dessous des autres qui ralentiront sa chute au fur et à mesure",
    "Lancer l'œuf sur un grand nombre de feuilles placés les unes en dessous des autres qui ralentiront sa chute au fur et à mesure",
    "Attacher un petit moteur à l'œuf de manière à ce qu'il descende doucement",
    "lancer l'œuf au dessus d'une turbine qui souffle de l'air et dont la force diminue progressivement",
    "lancer l'œuf dans un tourbillon d'air",
    "lancer l'œuf en dessous d'un aspirateur surpuissant qui diminue progressivement sa descente",
    "Faire descendre doucement l'œuf grâce à un ascenseur",
    "lancer l'œuf sous un tube qui aspire vers le haut qui diminue progressivement sa descente",
    "lancer l'œuf sur un geyser d'eau qui diminue progressivement sa descente",
    "Lancer l'œuf au dessus d'un caisson de basses, ce qui le fera leviter grâce aux ondes acoustiques",
    "Lancer l'œuf au dessus de plein de caissons de basses, ce qui le fera leviter grâce aux ondes acoustiques",
    "Lancer l'œuf au cours d'un tremblement de terre de manière à ce qu'il levite grâce aux ondes sismiques",
    "Accrocher un parachute à l'œuf pour ralentir sa chute",
    "Accrocher un sac plasitique à l'œuf pour qu'il ait une sorte de parachute pour ralentir sa chute",
    "Accrocher l'œuf a un élastique pour qu'il fasse un saut à l'elastique",
    "Accrocher l'œuf a plusieurs élastiques pour qu'il fasse un saut à l'elastique",
    "Poser l'œuf sur un deltaplane pour qu'il ralentisse sa chute",
    "Poser l'œuf sur un avion en papier pour qu'il atterisse en planant",
    "lancer l'œuf dans un mini planeur en toile de cerf volant",
    "lancer l'œuf dans un grand entonnoir en mousse",
    "lancer l'œuf dans un toboggan en mousse qui se ressert au fur et à mesure de la chute",
    "lancer l'œuf au dessus d'un grand nombre de ventilateurs dirigés vers le ciel pour ralentir sa chute",
    "lancer l'œuf au dessus d'un grand ventilateur pour ralentir sa chute",
    "lancer l'œuf dans un toboggan de 10 mètres",
    "lancer l'œuf sur une rampe de 10 mètres",
    "lancer l'œuf dans un panier attaché à une corde",
    "faire descendre l'œuf grâce à un système de poulie",
    "lancer l'œuf attaché à des ballons gonflés à l'hélium pour ralentir sa chute",
    "lancer l'œuf dans un ballon gonflé d'air",
    "Faire descendre doucement l'œuf grâce à un ascenseur de service",
]
groupe["D"] = "Interrompre la chute"
items["D"] = [
    "L'œuf se casse au fur et à mesure de la chute. Il est donc cassé avant son arrivée au sol",
    "Lancer l'œuf au dessus d'un filet",
    "Lancer l'œuf au dessus d'un filet de pompier",
    "On le lance et on le rattrappe avec son autre main 2 cm plus bas",
]
groupe["E"] = "Avant la chute"
items["E"] = [
    "Lancer l'œuf a partir de 11 mètres, comme ça au bout de 10 mètres il ne sera pas cassé",
    "Casser l'œuf avant de le lancer (il ne cassera pas à cause de l'impact)",
    "Lancer uniquement le jaune et le blanc de l'œuf (la coquille ne se cassera pas puisqu'elle ne sera pas lancée)",
    "Lancer l'œuf doucement",
    "Lancer l'œuf au dessus d'une pente",
    "lancer l'œuf en faisant des gestes aériens",
    "Lâcher l'œuf doucement",
    "Ne pas lancer l'œuf ",
    "Prendre l'œuf avec soi et descendre par les escaliers",
]
groupe["F"] = "Après la chute"
items["F"] = ["Remplacer l'œuf cassé après l'atterissage par un œuf intact"]
groupe["G"] = "Dispositif vivant"
items["G"] = [
    "Demander à un champion de baseball de sauter pour ratrapper l'œuf ",
    "Demander à quelqu'un de se placer au point d'impact pour récuperer l'œuf",
    "Lancer l'œuf sur une personne qui le gobera",
    "Lancer la poule qui n'a pas encore pondu, et faire en sorte qu'elle dépose l'œuf au sol",
    "Faire en sorte qu'une girafe attrappe l'œuf et le fasse descendre doucement",
    "Demander à un aigle de voler jusqu'à récuperer l'œuf pour le poser doucement au sol",
    "Sauter avec l'œuf pour le proteger",
    "Gober l'œuf, puis sauter de 10 mètres",
    "Demander à quelqu'un d'autre de trouver une solution pour répondre à ce problème",
]
groupe["H"] = "Modifier les propriétés de l'oeuf"
items["H"] = [
    "Modifier les propriétés génétiques de la poule pour qu'elle ponde des œufs incassables",
    "Modifier les propriétés génétiques de la poule pour qu'elle ponde des œufs élastiques",
    "la poule pond un nouvel œuf à chaque fois que l'œuf se casse",
    "cuire l'œuf pour le rendre dur avant de le faire tomber",
    "cuire l'œuf pour le rendre dur et retirer sa coquille avant de le faire tomber",
    "lancer un œuf en plastique",
    "lancer un ballon en plastique en forme d'œuf",
    "lancer un œuf dur parce qu'il sera congelé",
    "lancer l'œuf après l'avoir laissé tremper dans du vinaigre de manière à ce qu'il devienne élastique",
    "lancer un œuf dans lequel on a injecter un produit qui consolide la coquille",
    "lancer un œuf dont l'intérieur est fait de gélatine élastique",
]
groupe["I"] = "Utiliser les propriétés naturelles de l'oeuf"
items["I"] = [
    "Faire en sorte que le poussin sorte de l'œuf pendant la chute, puis qu'il s'envole",
    "Lancer l'œuf en le faisant tomber sur son axe oval, sachant que cet axe est incassable",
]
groupe["J"] = "Modifier les propriétés de l'environnement"
items["J"] = [
    "Arrêter l'expérience avant que l'œuf ne se casse",
    "Croiser les doigts pour que l'œuf ne se casse pas",
    "Lancer l'œuf dans une pièce de la NASA qui serait vide (c'est à dire qu'il n'y a pas de gravité)",
    "Lancer l'œuf sur des sables mouvants",
    "Utiliser une machine qui inverse la force de gravité pour que l'œuf ne soit pas attiré par le sol",
    "Lancer l'œuf au dessus d'une peinture trompe l'œil, qui donne l'impression qu'il y a 10 mètres de profondeur au sol",
    "Faire l'expérience en réalité virtuelle, dans un monde où l'œuf ne se casse pas",
]


for group_name, group_desc in groupe.items():
    group = IdeasGroup(name=group_name, description=group_desc)
    group.save()

    for idea in items[group_name]:
        idea = Idea(value=idea)
        idea.save()
        group.ideas.add(idea)

    print("Created group", group)
