---
title: Initialisation d'un projet open source PHP
locale: fr
tags:
    - php
excerpt: Choses à ne pas oublier lorsqu'on démarre et maintient un projet open source.
---

{% include toc title="Summary" %}

Libérer un projet existant ou en créer un nouveau de manière
collaborative est une solution de plus en plus évidente. En effet, c’est
une bonne méthode pour partager votre solution, et donc partager aussi
les problèmes, et la citation "Un problème partagé est un problème à
moitié résolu." prend alors du sens.

Mais c’est aussi un ensemble de méthodes et de normes qui peuvent être
nouvelles et peu évidentes pour une personne qui souhaiterait se lancer
dans le mouvement.

Dans cet article, qui part de la naissance d'un projet ou d’une
librairie PHP, jusqu'à la mise en place d'outils d'intégration continus
pour faciliter les contributions extérieures, je vais détailler toutes
les étapes et les questions que vous devez vous poser.

## Naissance de votre projet

### Parlez de l'idée, confrontez la, soyez à l'écoute des premiers feedbacks

Bien souvent, on aime avoir une idée pour soi, la développer et la faire
connaître sous notre nom. Si vous souhaitez rendre votre projet open
source et recevoir des contributions, il va falloir accepter l'idée que
d'autres vont "salir" votre beau code source, encore vierge de tout bug.

“Adding a Bundle means that you are ok with all members messing with it”

— Second rule of Friends of Symfony.
<https://friendsofsymfony.github.io>

Et ne gardez pas l'idée pour vous, partagez là ! Est-ce que d'autres
vont utiliser votre projet, ou le trouver inutile ? Le fait d’en parler
va vous permettre d’entendre les feedbacks et de vous challenger sur
votre propre idée.

### Faites une page de présentation en ligne

Avant même de commencer tout développement, créez une page de
présentation du projet, ou une page d'exemple d'utilisation de la
librairie.

En plus de montrer aux utilisateurs l'utilité du projet, cela mettra vos
idées au clair et permettra aux contributeurs de partir dans la même
direction.

Permettez et organisez également les commentaires et les échanges en
utilisant les issues de Github, ou un outil externe comme Gitter
(<https://gitter.im>) qui permet un chat en temps
réel entre les contributeurs et les utilisateurs.

## Création du dépôt

### Créez un dépôt ouvert dès le début

Le dépôt est là où la version la plus à jour du code source de votre
projet sera sauvegardée. C’est souvent un gestionnaire de versions (git,
svn, …) installé sur un serveur en ligne (Github, Bitbucket, …) pour
permettre à tous de récupérer et modifier le code source.

Un piège à éviter est de créer un dépôt fermé, interdit au public, et de
se dire qu’on l’ouvrira plus tard, quand le projet sera “présentable”,
“prêt”, ou encore “terminé”. En réalité, un projet n’est jamais terminé,
et contiendra toujours de la dette technique : des bugs, du code à
simplifier... Donc partir dans cette optique condamne le dépôt à être
toujours fermé.

Alors ouvrez le tout de suite, faîtes qu’il soit toujours opérationnel,
même s’il ne fait pas encore grand chose !

### Le premier fichier de votre projet : Le Readme

Non, le premier fichier de votre projet PHP n’est pas un `index.php`, un
`.gitignore`, ou un `composer.json`.

Si vous êtes utilisateur de Github, vous constaterez que le fichier
Readme n’est plus le fichier ignoré d’antan qu’il y avait sur les
CD-ROM. Github affiche le contenu de ce fichier sur la page d’accueil du
projet, et c’est donc le premier fichier lu par une nouvelle personne
qui arrive sur le projet.

Le fichier Readme doit contenir la description du projet, à qui il
s’adresse, à quoi il sert… Personnellement, je me sers souvent d’un
modèle d’elevator speech. C’est une description très courte d’un projet
qui doit permettre à une tierce personne de comprendre l’utilité de
celui-ci. L’idée est née aux USA, et le principe est de pouvoir
expliquer son projet à un futur client pendant le temps de trajet de
l’ascenseur.

### Choisissez une licence open source

La licence indique si vous autorisez que votre projet soit réutilisé,
modifié par d’autres personnes et redistribué...

Notez avant tout que si vous ne mettez pas de licence à votre projet, il
sera par défaut privé, et interdit de toute réutilisation.

Les licences open source sont compliquées de part leurs détails, mais on
peut faire simple. Jusque là, je n’utilisais que 2 licences : MIT et
GNU-GPL.

MIT est une licence open source très laxiste et permet de tout faire
avec le code source : Le réutiliser, l’intégrer dans un projet fermé…
C’est une licence utile pour une petite librairie qu’on souhaite mettre
à disposition sans se préoccuper de l’usage fait ensuite.

GNU-GPL est une licence open source qui force les projets utilisants du
code GNU-GPL à être eux aussi sous cette même licence. Cela la rend
contagieuse, et vient du trait militant de la Free Software Foundation.
J’utilise cette licence pour les projets dont je souhaite que tous ceux
qui les réutilisent pour un usage public mettent aussi leur projet en
open source.

Donc à moins d’avoir une exigence juridique très spécifique, utiliser
ces deux licences reste un choix simple et rapide, et ce sont les
licences les plus utilisées pour les projets sur Github selon ces
statistiques : <https://github.com/blog/1964-open-source-license-usage-on-github-com>.

Vous pouvez tout de même découvrir toutes les autres licences open
source sur [opensource.org](https://opensource.org/), et les licences
Free Software sur [fsf.org](http://www.fsf.org/). Il en existe plus
d’une centaine, et certaines seront peut-être plus adaptées à votre
projet. Exemple avec la licence AGPL vs GPL :
<https://www.gnu.org/licenses/why-affero-gpl.fr.html>.

Il existe aussi un site qui peut vous aider quant au choix de la licence :
<http://choosealicense.com/>.

### Vous créez une librairie PHP ? Ajoutez là sur Packagist !

Votre projet ou librairie va peut-être dépendre d’autres librairies, et
pourrait aussi être une brique d’un autre projet.

Pour éviter d’installer les dépendances à la main, utilisez un
gestionnaire de dépendances.

En PHP, vous aurez besoin de [Composer](https://getcomposer.org/) pour
lister les librairies que votre projet va utiliser, et Composer va se
charger de les installer, ainsi que les dépendances des dépendances…

Vous pourrez aussi les mettre à jour et ainsi éviter d’avoir des
dépendances obsolètes dans lesquelles des vulnérabilités auront été
découvertes.

Si votre projet est une librairie destinée à être utilisée comme une
brique dans d’autres projets PHP, ajoutez là à
[Packagist](https://packagist.org/) !

Packagist est le référentiel principal des librairies utilisant
Composer.

La mettre sur Packagist va permettre aux utilisateurs de votre librairie
de l’ajouter facilement en tant que dépendance de leur projet. De plus,
cela va faciliter l’installation de celle-ci, un plus pour la prise en
main.

## Entamez le développement

### Ne vous embarquez pas dans un début de projet interminable

Une bonne approche est d’utiliser le MVP (Minimum Viable Product). Cette
méthode a été développée par Eric Ries, dans son livre The Lean Startup.
L’objectif est de commencer par les fonctionnalités les plus importantes
de votre projet, celles que les gens vont adopter rapidement. Et pour
cela, il est nécessaire de savoir quelles sont-elles.

Pour cela, n’hésitez pas à très vite proposer des premières versions, et
comprendre les feedbacks.

### N'oubliez pas d'instaurer une norme de codage dès le début

Chaque personne a un style de code différent. Cela peut rendre difficile
la lecture d’un code d’une autre personne, et compliquer les
contributions en ayant du mal à se mettre d’accord sur une façon
d’écrire un même code.

#### Trancher sur la façon d’écrire le code

Un des avantages des normes de codage est de normaliser le style de
code. Les normes contiennent des règles, comme le nombre d’espaces
utilisé pour l’indentation, le placement des accolades ouvrantes sur la
même ligne ou sur une nouvelle ligne…

Ces règles vont fluidifier les revues de code en évitant de longues
discussions sur la meilleure façon de coder.

#### Limiter le nombre d’erreurs d’inattention

Mais les normes de codage permettent plus. Elles permettent aussi de
limiter les erreurs d’inattention. Un exemple, je veux tester si une
variable vaut 5 :

``` php
if ($a = 5) {}
```

Notez que j’ai malencontreusement oublié un “=”.

Cela aura pour effet d’affecter 5 à la variable \$a, et d’entrer dans le
if. Cela ne lèvera pas d’erreur car la syntaxe est correcte, bien que
j’ai fait une erreur de typo.

C’est une erreur difficile à débugger car silencieuse, et qu’on a tous
fait au moins une fois.

Certaines normes de codage imposent de placer la valeur à gauche de la
variable. On appelle cette règle la “condition Yoda”
(<https://fr.wikipedia.org/wiki/Condition_Yoda>),
je vous laisse trouver la référence ;)

Si j’avais suivi cette règle, j’aurai dû écrire :

``` php
if (5 = $a) {}
```

Ce qui aurait levé une erreur de syntaxe, et que j’aurai tout de suite
corrigé en :

``` php
if (5 == $a) {}
```

Donc comme le montre cet exemple, un autre avantage des normes de codage
est d’imposer un style d’écriture qui va mettre certaines erreurs
d’inattention en évidence.

#### Et en PHP ?

En PHP, la norme la plus utilisée est celle des PHP standards, la norme
PSR-2
(<http://www.php-fig.org/psr/psr-2/>).

### Mettez en place les tests unitaire et les tests d'intégration

Chaque nouvelle fonctionnalité que vous ajoutez à votre application
risque de causer des régressions, de casser d’autres fonctionnalités. Il
faudrait donc, en plus de tester votre nouvelle fonctionnalité, tester
aussi toutes les autres fonctionnalité déjà implémentées, c’est le
fameux cycle dont on ne prononce pas le nom.

Cela devient très vite impossible car d’une, votre application va offrir
de plus en plus de fonctionnalité, et de deux, un nouveau contributeur
ne connaîtra pas toute votre application, et ne pourra pas vérifier s’il
a cassé une partie du code développé par un autre contributeur.

C’est là que les tests automatisés interviennent. Ils vont appeler des
fonctions très ciblées du code, ou simuler l’utilisation d’une
fonctionnalité, et vérifier que le résultat obtenu est toujours celui
attendu. On pourra lancer ces tests automatisés à chaque modification de
code, et vérifier que notre nouvelle portion de code ne casse rien.

Les tests automatisés sont important dans un projet open source, car ils
vont empêcher d’autres contributeurs de causer des régressions, et donc
faciliter les contributions.

Plus de détails à propos des tests, et une liste d’outils PHP ici :
<http://www.hongkiat.com/blog/automated-php-test/>.

### Gardez à jour la documentation, elle doit être opérationnelle à tout moment !

À tout moment, de nouveau utilisateurs vont arriver sur votre projet.
Ils vont vouloir le tester, ou installer la librairie. Si à ce moment
là, votre documentation n’est pas à jour et l’utilisateur ne peut pas
tester, il pensera que le projet ne marche pas.

C’est pour cela que la documentation d’installation doit toujours être
opérationnelle. Pour l’utilisateur, si l’installation ne fonctionne pas,
le projet ne fonctionne pas, si la documentation d’installation est trop
compliquée, le projet est trop compliqué…

Gardez à jour une documentation d’installation et d’utilisation
fonctionnelle, mais aussi claire et simple, c’est à dire le minimum
d’étapes d’installation, et de paramètres farfelus.

De plus, cela pourra lever une alerte si vous voyez que votre
documentation devient compliquée, c’est qu’il y a peut-être un problème
de conception, ou quelque chose à simplifier dans le code même.

Si vous n’arrivez pas à simplifier votre documentation sur l’utilisation
car votre librairie est elle-même compliquée, essayez de faire de la
documentation first. Mettez-vous à la place de l’utilisateur, et écrivez
la doc avec des exemples de code de la manière qui semble la plus
évidente. Implémentez ensuite votre librairie en faisant en sorte que
les exemples fonctionnent.

## Accueillez vos contributeurs

### Pensez au modèle de branches

Vous êtes adepte du tout-sur-master (ou tout-sur-trunk pour les anciens)
? Très bien, vous avez souvent eu l’occasion de constater un bug
longtemps après qu’il ait été commité, ou alors commité par erreur une
fonctionnalité pas encore finie.

Faire des branches, ou faire différentes version du projet, permet de
développer une fonctionnalité et de la fusionner une fois testée, revue,
et bien terminée.

Mais ne faites pas des branches au hasard, pensez à un modèle adapté qui
correspond à votre manière de sortir des nouvelles versions de votre
application.

Un modèle simple et assez connu est git flow, qui intègre la branche
master, la version stable de votre projet, une branche développement, là
ou les dernières fonctionnalités sont fusionnées, des branches feature
pour les fonctionnalités importantes, et quelques autres branches que
vous pourrez découvrir ici :
<https://www.occitech.fr/blog/2014/12/un-modele-de-branches-git-efficace/>.

Si ce modèle ne permet pas d’avoir plusieurs versions stable du projet
(il y a seulement master), et que vous souhaitez maintenir plusieurs
versions comme le ferait par exemple Symfony avec 2.7, 2.8, 3.0, ...
C’est là qu’il faudra choisir un autre modèle avec les autres
contributeurs, et bien communiquer le modèle de branches que vous aurez
choisi.

### Utilisez les Pull Request

Utiliser une branche pour créer une nouvelle fonctionnalité est une
bonne pratique. Vous pourrez la fusionner une fois terminée.

Mais au lieu de fusionner votre branche tout de suite et d’*imposer* vos
modifications, choisissez plutôt de *proposer* vos modifications en
créant une pull request, surtout si ce n’est pas votre projet et que
vous contribuez à un autre projet.

Un outil comme Github ou Gitlab liste les pull request, permet de les
commenter, ou commenter une ligne précise du code, de mettre à jour la
pull request, et de la fusionner en intégrant les feedbacks des autres
contributeurs.

Cela permettra aux autres contributeurs d’effectuer une revue de code,
voir ce que vous avez créé, récupérer votre code et l'exécuter sur sa
propre machine.

Une autre bonne pratique veut qu’on ne fusionne jamais notre propre
code, et de s’obliger à laisser au moins une autre personne le relire et
le fusionner. C’est une pratique qui s’inspire de l’extreme programming,
et qui est assez efficace si on utilise un outil comme Github ou Gitlab.

## Mettez en avant les outils d'intégration continue

Vous avez maintenant initialisé votre projet, il est en ligne, il y a
une documentation, une norme de codage, des tests unitaire et des tests
d’intégration.

Il existe certains outils que vous allez pouvoir intégrer à
l'environnement de votre projet. Les outils que je vais présenter ici
sont gratuits et adaptés à des projets open source. Ils vont automatiser
le lancement des tests unitaires et d’intégration, vérifier le respect
de la norme de codage, ou inspecter la qualité du code et remonter
quelques bugs potentiels.

### Travis

Travis est un outil d’intégration très connu. Il est lié à Github, et
permet de lancer un script, ou “job”, après un push sur une branche du
projet, ou même lorsqu’une pull request est créée.

On peut donc lancer des tests unitaires, des tests d’intégration, ou
même lancer un job qui vérifie que la norme de codage a été respectée.

Grâce à son intégration à Github, Travis envoi ensuite l’état du build
(aucun test cassé, code style correct), et Github affiche directement
dans la pull request une coche verte ou une croix rouge en fonction de
l’état.

C’est donc un outil gratuit pour les projets open source qui va pouvoir
vérifier à chaque contribution si le code modifié ne casse rien et si le
projet peut toujours s’installer.

### Scrutinizer

Scrutinizer est un outil de qualité continue. Il va inspecter le code
source, évaluer sa complexité, détecter les bugs potentiels,
duplications, erreurs de syntaxe… Et va en sortir une note sur 10, ainsi
qu’une liste de recommandations qui va nous permettre d’améliorer cette
note.

Cependant, ce n’est pour moi pas une bible, et la note est juste un
repère. Cet outil va indiquer si une modification de code risque
d’intégrer un bug ou contient des fonctions avec une complexité trop
élevée.

Cet outil nous permet donc de suivre l’évolution de la qualité du code
en connaissant l’impact de chaque PR sur la note, et si elle introduit
des issues.

On peut même recevoir des mails si un commit fait chuter la note, qui
est l’auteur de ce commit...

### SensioLabsInsight

SensioLabs propose aussi un outil d’inspection de code, mais celui-ci
est orienté Symfony. C’est à dire qu’il propose, en plus des
recommandations PHP, des bonnes pratiques à suivre sur des projets
Symfony, Silex, ou même sur un bundle Symfony.

### Badges

Si vous utilisez des outils comme ceux cités ci-dessus, notez qu’ils
proposent ensuite des badges. Ce sont des petites images dynamiques,
liées au résultat du build ou de l’inspection, que vous allez pouvoir
ajouter dans le Readme de votre projet. Les badges indiqueront donc en
temps réel si le build du projet n’est pas cassé, si les tests passent
toujours, la qualité du code…

Les badges montrent en plus que vous vous souciez de la qualité du code,
et veillez que les contributions ne causent pas de régressions.

{% include figure
    image_path="/assets/images/initialiser-projet-open-source-php/badges.png"
    caption="Différents badges sur le README d'un projet PHP."
    alt="Différents badges sur le README d'un projet PHP."
%}

## Résumé

Vous avez vu dans cet article qu’un projet open source n’est pas
seulement un dépôt ouvert. C’est aussi maintenir le code, relire les
propositions de code et feedbacks proposés par la communauté, avoir une
documentation, un readme...

Il existe une organisation, [The PHP
League](https://thephpleague.com/fr/), qui a créé un squelette pour une
librairie PHP. C’est une bonne base de projet qui contient plusieurs
fichiers qu’on retrouve généralement dans un projet PHP. C’est
accessible sur Github :
[thephpleague/skeleton](https://github.com/thephpleague/skeleton).

### Aller plus loin

Vous pouvez consulter un des articles de Richard Stallman, “Le logiciel
libre est encore plus essentiel maintenant” :
<https://www.gnu.org/philosophy/free-software-even-more-important.html>,
et naviguer ensuite sur le site et la foire aux questions qui détaillent
de nombreux concept du logiciel libre.

Pour voir comment ca se passe actuellement au sein d’un projet open
source, vous pouvez voir la conférence de Jordi Boggiano, initiateur de
composer et packagist, sur les coulisses d’un projet open source,
“Behind the Scenes of Maintaining an Open Source Project” :
<https://www.youtube.com/watch?v=hRZhYSiSfaY>


{% include ccby %}
