---
title: Contrôler un robot à deux roues avec Raspberry Pi
tags:
    - raspberry-pi
---


Débutant en électronique, dans le cadre d'un projet, je viens juste de réaliser
un prototype d'un petit robot qui peut avancer, reculer, et tourner.

{% include toc title="Sommaire" %}

<iframe width="640" height="360" src="https://peertube.video/videos/embed/95bdd4f0-630a-4184-9754-33c9f9e8f4fb" frameborder="0" allowfullscreen></iframe>

Cet article est fait pour ceux qui partent de zéro, qui souhaitent contrôler un ou
deux moteurs afin de réaliser ce genre de robot, et comprendre comment ça marche !


## Le moteur électrique

Pour avoir un mouvement de rotation, le moteur, mis sous tension, va transformer
un courant électrique en mouvement de rotation.

Le sens du courant joue un rôle : selon le sens du courant, le moteur tourne
dans un sens ou dans l'autre.

Le moteur va donc tourner si on lui applique une tension à ses bornes, mais ca
marche aussi dans l'autre sens : si on fait tourner le moteur,
cela va générer une tension à ses bornes.

### Faites un arrêt rapide de votre moteur

Et donc, admettons qu'on court-circuite le moteur en reliant les bornes.
En faisant tourner le moteur à la main, le moteur va génerer une tension.
Mais vu que les bornes sont reliées, elles vont chacune recevoir de l'autre
un courant opposé. Cela va freiner le mouvement.

Vous pouvez faire cette expérience en reliant les bornes de votre moteur,
le faire tourner à la main. Vous constaterez que c'est plus difficile que quand
les bornes ne sont pas reliées.

### Le servomoteur

Il existe un type de moteur que l'on appelle un "servomoteur".
Ce type de moteur n'est pas plus intelligent (lol). Il tourne moins vite
mais délivre un couple (une poussée) supérieur.

On s'en sert donc pour des tâches comme ouvrir une porte : on a besoin de faire
qu'un tiers de tour, mais la porte est lourde, donc le moteur doit avoir un
couple conséquent. Il y a aussi parfois des butées dans ce type de moteur
lui évitant de tourner plus que nécessaire, mais on peut enlever cette butée
sans problème pour faire avancer notre robot sur la distance.

### On a vu

 - Le moteur transforme un courant en rotation
 - Il peut aussi transformer une rotation en courant
 - Si on court-circuite les bornes du moteur, ça le freine
 - Le sens du courant joue sur le sens de la rotation du moteur
 - Le servomoteur tourne moins vite mais a plus de couple


## Le pont en H

C'est un montage assez commun et que vous retrouverez sûrement dés qu'il faut
pouvoir faire tourner un moteur dans les deux sens.

Ce montage réutilise tous les principes vu dans le chapitre précédent, notamment
le fait qu'on puisse inverser le sens du moteur en changeant le sens du courant,
et le freiner en le court-circuitant.

Par exemple pour faire avancer ou reculer un robot, il faudra inverser le courant,
mais vous ne pourrez pas démonter le robot et inverser le branchement bornes pendant qu'il roule !

Le pont en H permet justement de contrôler un moteur sans changer le circuit.

{% include figure
    image_path="/assets/images/rpi-motors/pont-h.png"
    caption="Schéma du pont en H"
    alt="Schéma du pont en H"
%}

A l'aide des interrupteurs, on peut faire passer le courant dans le moteur
d'un sens ou dans l'autre en basculant deux interrupteurs.

{% include figure
    image_path="/assets/images/rpi-motors/pont-h-animated.gif"
    caption="Changer le sens de rotation du moteur avec le pont H"
    alt="Pont H animé"
%}

### Servez vous du pont H pour freiner votre robot

Avec le même montage, on peut également relier les deux bornes à la masse
en fermant les deux interrupteurs du bas.
Cela qui va court-circuiter le moteur et le freiner. C'est utile pour faire en
sorte que le robot s'arrête dés qu'on coupe le courant et éviter qu'il continu
avec son inertie.

{% include figure
    image_path="/assets/images/rpi-motors/pont-h-stop.png"
    caption="Freiner le moteur avec le pont H"
    alt="Pont H court-circuit"
%}

Attention tout de même à ne pas fermer les mauvais interrupteurs
et causer un court-circuit !

### On a vu

 - Le pont en H est un montage commun pour contrôler un moteur
 - Il permet d'inverser facilement le sens du moteur
 - Il permet de freiner le moteur


## Le circuit intégré L293D

Nous avons vu que le pont H permet de contrôler un moteur avec des interrupteurs.
Mais nous n'allons pas courir derrière notre robot
pour le contrôler en appuyant sur des interrupteurs !

Le circuit intégré L293D contient deux ponts H, et permet de contrôler
jusqu'à deux moteurs bidirectionnels indépendamment sans se préoccuper
de basculer les interrupteurs.

{% include figure
    image_path="/assets/images/rpi-motors/l293d.jpg"
    caption="Circuit intégré L293D"
    alt="Circuit intégré L293D"
%}

Ce circuit intégré permet également d'alimenter les moteurs
par une autre source d'alimentation que la Raspberry Pi.

### Ne branchez pas les moteurs sur la Raspberry Pi

En effet, si vous connectez le moteur sur les pins de la Raspberry Pi,
il va consommer tellement de courant qu'il mettra la Raspberry à plat,
et elle se redémarrera toutes les secondes.
De plus, votre moteur a peut-être besoin de plus de 5V pour fonctionner.
Vous devrez donc à la fois alimenter le circuit logique de la L293D
avec les 5V de la Raspberry, et le circuit dédié aux moteurs avec des piles.

Il y a donc deux circuits différents avec deux tensions différentes,
`Vcc1` pour le circuit logique (par exemple 5V) et `Vcc2` pour les moteurs (par exemple 9V),
que nous devrons fournir sur deux pattes différentes.
Nous verrons le montage plus tard.

On peux voir dans sa documentation (<http://www.ti.com/lit/ds/symlink/l293.pdf>) :

{% include figure
    image_path="/assets/images/rpi-motors/l293d-complet.png"
    caption="Schéma complet du circuit L293D"
    alt="schéma L293D"
%}

Le schéma ci-dessus provient de la documentation du circuit.
On peut y distinguer sur le schéma exhaustif les deux ponts H
(si, en tournant la tête ça fait H).

Mais on n'a pas besoin de tout connaître de ce circuit, et on va se contenter du
schéma simplifié fourni également dans la doc :

{% include figure
    image_path="/assets/images/rpi-motors/l293d-simple.png"
    caption="Schéma simplifié du circuit L293D"
    alt="schéma L293D"
%}

Dans ce schéma simplifié, on voit à gauche les entrées logique (les `A` et `EN`).
Elles seront connectés à des pins GPIO de la Raspberry et permettent de contrôler les moteurs.
Les connexions de droite (les `Y`) sont les sorties du circuit.
On y branchera les bornes des deux moteurs.
Ils auront la tension fournie par les piles, `Vcc2`,
en fonction des tensions logiques (`Vcc1`) qu'on met en entrée.

Les triangles sont des portes logiques `ET`.
Ce qui veux dire qu'il y aura de la tension dans `1Y`
seulement si il y a une tension logique haute dans `1,2EN` **et** `1A`.

Pour savoir quelles pattes du circuit intégré correspondent à quelles entrées/sorties,
nous pouvons nous fier à ce schéma qui provient de la documentation :

{% include figure
    image_path="/assets/images/rpi-motors/l293d-pins.png"
    caption="Les entrées et sorties de la L293D"
    alt="Schéma L293D"
%}

L'encoche sur le circuit intégré permet de connaître le sens.

Nous pouvons donc relier un moteur au circuit intégré
en branchant ses bornes aux sorties `1Y` et `2Y`.

{% include figure
    image_path="/assets/images/rpi-motors/1-motor-l293d-rasp.png"
    caption="Schéma de montage pour contrôler un moteur avec Raspberry Pi et le circuit intégré L293D"
    alt="Schéma de montage pour contrôler un moteur avec Raspberry Pi et le circuit intégré L293D"
%}

> Note sur la planche expérimentale : si vous ne connaissez pas encore,
> cette planche permet de prototyper des montages facilement sans rien souder.
> Les trous sont reliés d'une façon qu'il est simple de relier des composants
> et faire des dérivations. Les lignes sont reliées entre elles,
> et les deux colonnes des deux côtés sont également reliées.
> Cet article détail encore plus son utilisation :
> <https://learn.sparkfun.com/tutorials/how-to-use-a-breadboard>

Ensuite, pour faire tourner le moteur, on doit activer l'entrée `1,2EN` ("enable 1 and 2"),
et soit mettre une tension haute dans `1A` et une tension basse dans `2A`, soit l'inverse.
Cela fera tourner le moteur dans un sens ou dans l'autre : cela dépend dans quel
sens le moteur est branché sur les sorties `1Y` et `2Y` du circuit.

Si nous mettons la même tension logique dans `1A` et `2A` (haut/haut ou bas/bas),
il n'y aura pas de tension aux bornes du moteur, il sera donc en roue libre.
Or nous avons vu que le pont H permet de court-circuiter les bornes du moteur
pour lui faire faire un arrêt rapide. Ceci est prévu par la L293D,
il faut mettre une tension basse dans `1,2EN`.

Pour résumer le contrôle d'un moteur :

Action            | `1,2EN` | `1A`   | `2A` |   |
------------------|---------|--------|------|---|
Tourne d'un côté  | haut    | haut   | bas  |   |
Tourne de l'autre | haut    | bas    | haut |   |
Arrêt rapide      | bas     | -      | -    | peut importe les entrées en `1A` et `2A` |
Rotation libre    | haut    | bas    | bas  | ou alors haut/haut                       |

### Attention au problème de surchauffe !

Notez que le circuit logique de la L293D doit être alimenté par les 5V de la Raspberry Pi,
mais que le courant provenant des piles et destiné aux moteurs traverse aussi le circuit L293D.
Cela va faire que le circuit peut dissiper beaucoup d'énergie
pour sa pauvre petite taille, et le faire chauffer.
Ce n'est pas un problème si les moteurs ne tournent pas longtemps et en continu,
en revanche, il faudra penser à équiper la L293D de son radiateur si il est prévu
de faire tourner les moteurs à temps plein.

{% include figure
    image_path="/assets/images/rpi-motors/l293d-radiateur.png"
    caption="L293D avec un radiateur"
    alt="L293D radiateur"
%}

### Contrôlez un deuxième moteur

Pour contrôler deux moteurs, il suffit d'en brancher un deuxième
sur les sorties `3Y` et `4Y` du circuit, et d'appliquer la même logique
sur les entrées `3A`, `4A` et `3,4EN`.

Nous allons faire ce montage dans la dernière partie.

### On a vu

 - On ne peut pas brancher un moteur directement sur la Raspberry Pi
 - Le circuit intégré L293D contient deux ponts H
 - Cela permet de contrôler deux moteurs en mettant sous tension certaines entrées du circuit
 - Comment contrôler un moteur bidirectionnel avec ce circuit
 - Il permet aussi d'alimenter les moteurs avec une autre source d'alimentation


## C'est parti pour le montage de notre robot

### Le matériel

- Le châssis

Nous avons acheté un châssis de voiture pour 15€.
Il comprend les deux roues et moteurs, boîtier de piles,
et tout pour monter le châssis.

{% include figure
    image_path="/assets/images/rpi-motors/chassis.jpg"
    caption="Chassis de robot à trois roues"
    alt="Chassis robot"
%}

- L'alimentation

Nous avons vu qu'il y a deux tensions différentes.
Une pour les piles et moteurs (peut aller de 4V à plus de 30V),
l'autre pour les circuits logiques (souvent 5V ou 3.3V).
Il faut donc une batterie pour le circuit logique de la Raspberry Pi et de la L293D.
Notez qu'il existe un battery hat concu pour la Raspberry
et qu'on peut monter facilement dessus.
On peut la voir sur l'image ci-dessous, en dessous de la Raspberry Pi :

{% include figure
    image_path="/assets/images/rpi-motors/battery-hat.jpg"
    caption="Raspberry Pi avec un battery hat"
    alt="Raspberry Pi battery hat"
%}

- Le contrôleur des moteurs

Nous avons vu plus haut que le circuit L293D permet de contrôler deux moteurs.
Dans le cadre de notre projet, nous avons opté pour un contrôleur
plus complet qui contient un circuit similaire, le L298N.

{% include figure
    image_path="/assets/images/rpi-motors/motor-driver.jpg"
    caption="Motor driver L298N"
    alt="L298N"
%}

Mais ce contrôleur contient surtout :
 - de quoi brancher les fils du boîtier de piles avec des vis
 - des pins mâle pour brancher les entrées logiques du L298N à la Raspberry
 - le radiateur, utile si vous souhaitez utiliser les moteurs longuement
 - de protéger le circuit avec des diodes et condensateurs empêchant le reflux de courant
des moteurs vers le circuit intégré (lorsque les moteurs génèrent du courant en tournant encore)

Nous avons donc choisi ce modèle car il est plus robuste, plus simple à brancher,
et permet de se passer de la breadboard.
Vous en trouverez facilement pour moins de 5€ avec les mots clés "motor driver controller L298".

### Réalisez votre montage

Je vais réaliser le montage suivant sur breadboard
qui permet de contrôler deux moteurs avec Raspberry Pi et le circuit L293D.

> Pour le faire avec le contrôleur L298N, voir plus bas.

{% include figure
    image_path="/assets/images/rpi-motors/2-motors-l293d-rasp.png"
    caption="Schéma de montage pour contrôler deux moteurs avec Raspberry Pi et la L293D"
    alt="Schéma montage pour contrôler deux moteurs avec Raspberry Pi et la L293D"
%}

Étapes et explications :

 - Tout doit être hors de tension

Il est recommandé de faire le montage hors tension. Pour cela,
débranchez la Raspberry et retirer au moins une pile du boîtier.

 - Je place la L293D au milieu

Il est commun de placer les circuits de cette façon :
dans ce sens, les pins ne seront pas reliés à leurs voisins d'en face par la planche.
On peut ensuite connecter les pins avec les trous de la même ligne.

 - J'alimente les deux lignes d'alimentation de la planche en reliant le rouge à 5V et bleu à la terre.

Utiliser les lignes d'alimentation va permettre de n'utiliser que deux pins de la Raspberry (5V et terre).
Je pourrais n'utiliser qu'une ligne, mais en utiliser deux va permettre
de faire moins survoler les fils d'un côté à l'autre.

 - J'alimente le circuit logique de la L293D

Les circuits logiques ont souvent besoin d'être sous tension (3.3V ou 5V, mais ici 5V) pour fonctionner.
Ici, c'est le pin `Vcc1` et les 4 pins `GROUND` au milieu.
Les pins sont expliqués dans la documentation : <http://www.ti.com/lit/ds/symlink/l293.pdf>

{% include figure
    image_path="/assets/images/rpi-motors/l293d-pins.png"
    caption="Les entrées et sorties de la L293D"
    alt="Schéma L293D"
%}

 - Connectez les sorties des 2 ponts H sur les deux moteurs

Les 4 pins de sortie, `1Y`, `2Y`, `3Y` et `4Y` sont autours des pins terre.
Connectez le premier moteur à `1Y` et `2Y`, et l'autre à `3Y`, `4Y`.
Le sens de rotation du moteur va dépendre du sens de branchement.
Le plus simple est de brancher au hasard, vous pourrez de toutes façons
ajuster lors de la programmation.

 - Connectez les entrées des 2 ponts H sur la Raspberry Pi

La Raspberry Pi va contrôler les ponts H, je connecte donc `1,2EN`, `1A` et `2A`
sur 3 pins GPIO pour le premier pont H.
Ensuite je fais de même de l'autre côté, pour `3,4EN`, `3A` et `4A`.
J'utilise donc 6 pins GPIO pour contrôler les moteurs.

 - Branchez l'alimentation des moteurs

Il faut alimenter le circuit dédié aux moteurs sur `Vcc2`.
Il faut aussi relier le pôle négatif des piles à la ligne terre
pour que les deux circuits partagent la même masse.

### Et avec le contrôleur L298N

On peut remplacer la L293D par ce contrôleur, et ainsi se passer de la breadboard.
Le montage est le même, les entrées et sorties sont les suivantes :

{% include figure
    image_path="/assets/images/rpi-motors/l298n-schema.jpg"
    caption="Entrées et sorties du contrôleur L298N par rapport à la L293D"
    alt="L298N"
%}

- 1 : Les entrées logiques. `IN1` et `IN2` contrôlent le premier moteur, `IN3` et `IN4` le deuxième.
Il faudra connecter ces 4 entrées à la Raspberry Pi.

Notez aussi `ENA` et `ENB`. Ce sont des entrées logiques optionnelles.
Elles correspondent à `1,2EN` et `3,4EN`, qui doivent être sous tension logique haute
pour pouvoir utiliser les moteurs, mais qu'on peux aussi mettre sous tension basse
pour faire faire un arrêt rapide au moteur en le freinant.

Par défaut, il y a un jumper dessus qui les connectent à une tension logique haute.
Donc par défaut, les moteurs sont toujours activés.
Mais vous pouvez décider de retirer les jumpers
et brancher les pins `ENA` et `ENB` à la Raspberry.

- 2 : Les sorties qui correspondent à `1Y`, `2Y`, `3Y` et `4Y`.
Il faut les connecter aux bornes des moteurs.

- 3 : La mise sous tension. Il faut connecter aux 3 vis :

    - `+5V` qui correspond à `Vcc1`, il faut y mettre le `5V` de la Raspberry
    - `+12V` qui correspond à `Vcc2`, il faut y brancher le pôle positif des piles (peut importe si ca ne fait pas 12V)
    - `GND`, la masse commune, il faut y mettre à la fois le `0V` de la Raspberry et le pôle négatif des piles.

- 4 : Le circuit intégré L298N et son radiateur.

- 5 : Le régulateur

L'utilisation du régulateur est optionnelle. Il peut servir dans un cas :
si votre alimentation externe pour les moteurs (ici les piles) fournit entre 5V et 12V,
vous pouvez vous en servir pour alimenter également le circuit logique de la L298N.

Dans ce cas, il faut mettre le jumper dessus (par défaut il y est déjà),
et vous économisez le fil `5V` entre la Raspberry et le contrôleur.

Sinon, si votre alimentation externe fournit moins de 5V,
ce sera pas suffisant, et si elle fournit plus de 12V, le régulateur risque de griller.

Dans tous les cas, étant donné que le régulateur n'a pas un rendement parfait,
il est toujours mieux de ne pas s'en servir,
de **retirer le jumper** et de connecter la vis `5V` à un pin `5V` de la Raspberry.
Cela évitera de la perte lorsque le régulateur transformera 9V ou 12V en 5V :
le reste est juste dissipé.

{% include figure
    image_path="/assets/images/rpi-motors/rasp-l298n.png"
    caption="Schéma de montage avec le contrôleur L298N"
    alt="L298N RaspbberyPi motors"
%}

### Procédez au smoke test

Une fois les piles insérées et la Raspberry Pi sous tension, procédez au smoke test.
Si il y a une erreur de branchement, il est possible que le circuit intégré se mette à chauffer.
Dans ce cas il sera vite chaud au bout de quelques dizaine de secondes.
Surveillez-le pendant les deux premières minutes après la mise sous tension.

> Anecdote : j'ai grillée une L293D en la confondant avec un autre circuit très ressemblant, la SN74HC595N.
> En fait le circuit L293D était déjà sur la breadboard, et j'ai fait le montage
> en pensant que c'était la SN74HC595N.
> C'est environ deux minutes plus tard après la mise sous tension
> que j'ai commencé à sentir une odeur de plastique fondu.
> Le circuit intégré était tellement brulant qu'il a fait fondre la breadboard.
>
> Donc oui, la L293D peut, mal connectée, causer des dégâts.

### C'est parti pour la programmation

On va maintenant pouvoir activer les pins de la Raspberry avec un peu de programmation.
Le but sera de faire avancer le robot et le faire tourner.

Créez un fichier sur la Raspberry, par exemple `my-script.py`, et codez le mouvement :

``` python
from time import sleep
import RPi.GPIO as GPIO

# Modifiez pour mettre les pins sur lesquels sont branchés les entrées de la L293D
MOTOR1_EN = 14
MOTOR1_A = 18
MOTOR1_B = 15

MOTOR2_EN = 25
MOTOR2_A = 8
MOTOR2_B = 7

try:

    # Configure les pins
    GPIO.setmode(GPIO.BCM)

    GPIO.setup(MOTOR1_EN, GPIO.OUT)
    GPIO.setup(MOTOR1_A, GPIO.OUT)
    GPIO.setup(MOTOR1_B, GPIO.OUT)

    GPIO.setup(MOTOR2_EN, GPIO.OUT)
    GPIO.setup(MOTOR2_A, GPIO.OUT)
    GPIO.setup(MOTOR2_B, GPIO.OUT)

    # AVANCE

    # Fais avancer le robot en faisant tourner les deux moteurs du même sens
    GPIO.output(MOTOR1_EN, GPIO.HIGH)
    GPIO.output(MOTOR1_A, GPIO.HIGH)
    GPIO.output(MOTOR1_B, GPIO.LOW)

    GPIO.output(MOTOR2_EN, GPIO.HIGH)
    GPIO.output(MOTOR2_A, GPIO.HIGH)
    GPIO.output(MOTOR2_B, GPIO.LOW)

    # Continu d'avancer pendant une seconde
    sleep(1)

    # Stoppe et freine les moteurs pendant une seconde
    GPIO.output(MOTOR1_EN, GPIO.LOW)
    GPIO.output(MOTOR2_EN, GPIO.LOW)
    sleep(1)

    # TOURNE A GAUCHE

    # Fais tourner le robot à gauche  en faisant tourner les deux moteurs à sens opposé
    GPIO.output(MOTOR1_EN, GPIO.HIGH)
    GPIO.output(MOTOR1_A, GPIO.LOW)
    GPIO.output(MOTOR1_B, GPIO.HIGH)

    GPIO.output(MOTOR2_EN, GPIO.HIGH)
    GPIO.output(MOTOR2_A, GPIO.HIGH)
    GPIO.output(MOTOR2_B, GPIO.LOW)

    sleep(0.5)

    # Stoppe et freine les moteurs pendant une seconde
    GPIO.output(MOTOR1_EN, GPIO.LOW)
    GPIO.output(MOTOR2_EN, GPIO.LOW)

    # On stoppe après une seconde
    sleep(1)

    GPIO.output(MOTOR1_EN, GPIO.LOW)
    GPIO.output(MOTOR2_EN, GPIO.LOW)

except KeyboardInterrupt:
    pass
except:
    GPIO.cleanup()
    raise

GPIO.cleanup()
```

> Vous aurez probablement besoin d'inverser les numéros des pins
> `A` et `B` dans le code source en fonction de comment vous aurez
> branché les moteurs et les entrées du contrôleur.

### Lancez la bête !

Lancez en ligne de commande sur la Raspberry :

``` bash
python my-script.py
```

### Et pour changer la vitesse des moteurs

Pour l'instant, on a mis seulement `GPIO.HIGH` ou `GPIO.LOW` en entrée,
ce qui permet de soit faire tourner le moteur à 100%, soit l'arrêter complètement.

Pour faire tourner un moteur à par exemple 75%, on peut mettre une tension discontinue
en entrée des pins `EN`. Cela veut dire que la Raspberry va activer le pin `EN` pendant
75% du temps, et le désactiver pendant 25%. En faisant ça très rapidement, le moteur
semblera tourner en continu, mais moins vite.

On peut pour cela utiliser l'objet `GPIO.PWM`, qui va s'occuper du cycle de travail.

> Le mode PWM permet de faire fonctionner un composant moins fort.
> Étant donné qu'on ne peut pas faire ca en envoyant moins de Volts,
> on le fait en alternant entre tension haute et tension basse rapidement.
> On peut faire ca sur la Raspberry en utilisant le mode PWM :
> <https://fr.wikipedia.org/wiki/Modulation_de_largeur_d%27impulsion>

En suivant [la documentation de GPIO python](https://sourceforge.net/p/raspberry-gpio-python/wiki/PWM/),
on peut par exemple faire sur le pin 14 :

``` python
import RPi.GPIO as GPIO

# Déclarer notre pin en mode sortie
GPIO.setmode(GPIO.BCM)
GPIO.setup(14, GPIO.OUT)

# Utiliser GPIO.PWM sur notre pin avec une fréquence de 100hz (100 cycles de travail par seconde)
pinGPIO = GPIO.PWM(14, 100)

# Démarrer les cycles de travail à 80%, donc le pin est activé 8ms, puis désactivé 2ms.
pinGPIO.start(80)
```

On peut donc faire tourner un des deux moteurs moins vite pour faire avancer
le robot en le faisant tourner légèrement, ou faire tourner les deux moteurs
moins vite pour que le robot avance moins vite en ligne droite :

``` python
from time import sleep
import RPi.GPIO as GPIO

# Modifiez pour mettre les pins sur lesquels sont branchés les entrées de la L293D
MOTOR1_EN = 14
MOTOR1_A = 18
MOTOR1_B = 15

MOTOR2_EN = 25
MOTOR2_A = 8
MOTOR2_B = 7

try:

    # Configure les pins
    GPIO.setmode(GPIO.BCM)

    GPIO.setup(MOTOR1_EN, GPIO.OUT)
    GPIO.setup(MOTOR1_A, GPIO.OUT)
    GPIO.setup(MOTOR1_B, GPIO.OUT)

    GPIO.setup(MOTOR2_EN, GPIO.OUT)
    GPIO.setup(MOTOR2_A, GPIO.OUT)
    GPIO.setup(MOTOR2_B, GPIO.OUT)

    motor1GPIO = GPIO.PWM(MOTOR1_EN, 100)
    motor2GPIO = GPIO.PWM(MOTOR2_EN, 100)

    # AVANCE

    # Fais avancer le robot lentement (50%) en ligne droite
    motor1GPIO.start(50)
    GPIO.output(MOTOR1_A, GPIO.HIGH)
    GPIO.output(MOTOR1_B, GPIO.LOW)

    motor2GPIO.start(50)
    GPIO.output(MOTOR2_A, GPIO.HIGH)
    GPIO.output(MOTOR2_B, GPIO.LOW)

    # Continu d'avancer pendant une seconde et demi
    sleep(1.5)

    # RECULE EN TOURNANT

    # Fais reculer le robot en dessinant une courbe
    motor1GPIO.start(100)
    GPIO.output(MOTOR1_A, GPIO.LOW)
    GPIO.output(MOTOR1_B, GPIO.HIGH)

    motor2GPIO.start(60)
    GPIO.output(MOTOR2_A, GPIO.LOW)
    GPIO.output(MOTOR2_B, GPIO.HIGH)

    # Continu de reculer pendant 2 secondes
    sleep(2)

    # Arrêt des moteurs en arrêtant les cycles de travail
    motor1GPIO.stop()
    motor2GPIO.stop()


except KeyboardInterrupt:
    pass
except:
    GPIO.cleanup()
    raise

GPIO.cleanup()
```


{% include ccby %}
