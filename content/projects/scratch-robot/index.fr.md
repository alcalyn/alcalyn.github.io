---
title: Scratch Robot
date: '2018-04-10'
summary: Contrôler un robot avec le langage de blocs Scratch.
featuredImage: /images/projects/scratch-robot/fond.jpg
project: true
tags:
- php
- raspberry-pi
---

*Cet article a été traduit de l'anglais.*

TLDR, voyez-le en action :

{{< video src="scratch-robot-720.mp4,scratch-robot-720.webm" >}}Votre navigateur ne semble pas supporter la balise video html5.{{< /video >}}

📖 [Scratch Robot sur Github](https://github.com/alcalyn/scratch-robot).

Le but de cette preuve de concept était
de jouer avec [blockly](https://developers.google.com/blockly/).

Cette bibliothèque permet aux utilisateurs de créer un programme
avec le langage Scratch. Ainsi, pas besoin
de connaître un langage de programmation : il suffit d'assembler
des blocs logiques.

Blockly permet de définir et de programmer nos propres blocs.

Par exemple, voici comment j'ai défini le bloc « avance » :

``` js
Blockly.defineBlocksWithJsonArray([
  {
    "type": "move_forward",
    "message0": "avance",
    "previousStatement": null,
    "nextStatement": null,
    "colour": "%{BKY_PROCEDURES_HUE}",
    "tooltip": "%{BKY_ROBOT_FORWARD_TOOLTIP}"
  }
]);
```

![Bloc avance](forward-block.png "Bloc généré")

Et voici comment je le programme :

``` js
Blockly.JavaScript['move_forward'] = function (block) {
  return 'Robot_forward();\n';
};
```

*C'est un « générateur », et on peut aussi en définir un pour python, php...*

J'ai développé 3 blocs : « avance », « tourne à gauche/droite », « attends N secondes ».
Chaque bloc renvoie du Javascript généré qui envoie un ordre au robot Raspberry Pi.

J'ai aussi utilisé [Js-Interpreter](https://github.com/NeilFraser/JS-Interpreter)
pour ne pas exécuter directement tout le Javascript généré,
mais le mettre en pause et attendre que le robot ait bougé.

Enfin, pour le robot, j'ai réutilisé une API sur laquelle j'avais déjà travaillé pour un autre projet :
[Darkmira/drop-robotapi](https://github.com/Darkmira/drop-robotapi).
Le readme contient le schéma de câblage pour monter votre propre robot.

📖 [Scratch Robot sur Github](https://github.com/alcalyn/scratch-robot).


{{< ccby >}}
