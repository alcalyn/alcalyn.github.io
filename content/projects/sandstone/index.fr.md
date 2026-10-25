+++
date = '2017-01-01'
featuredImage = '/images/projects/sandstone/sandstone-teaser.png'
project = true
summary = 'Microframework PHP pour construire une RestApi temps réel.'
tags = ['php']
title = 'Sandstone'
+++

*Cet article a été traduit de l'anglais.*

TLDR : [Voir le projet ici !](https://eole-io.github.io/sandstone-doc/)

## Qu'est-ce que Sandstone

Sandstone est un microframework PHP.
Ses objectifs principaux sont :

 - Construire une RestApi
 - Monter un serveur websocket
 - Envoyer facilement des notifications push.

Sandstone est basé sur [Silex](https://silex.symfony.com/), le microframework de Symfony.

Si vous ne connaissez pas Silex, c'est un framework web minimaliste
similaire à [expressjs](http://expressjs.com/fr/) en nodejs,
ou à [flask](http://flask.pocoo.org/) en python.

## Que puis-je faire avec Sandstone

Vous pouvez facilement démarrer une RestApi, et y ajouter du temps réel, par exemple :

 - Notifier tous les clients web qu'un nouvel article vient d'être publié via la RestApi
 - Créer un chat qui fonctionne avec votre RestApi
 - Pour un serveur de jeu, diffuser les coups des joueurs dès que quelqu'un a joué

## Comment démarrer

Si vous démarrez un nouveau projet, la
[Sandstone edition](https://github.com/eole-io/sandstone-edition) devrait vous intéresser.

C'est une installation neuve de Sandstone, à partir de laquelle vous pouvez construire une RestApi temps réel,
et qui contient aussi des outils de debug.

Cette édition intègre :

 - [Sandstone](https://eole-io.github.io/sandstone/) (Silex avec des websockets)
 - un environnement **Docker** pour monter toute l'application (RestApi, serveur websocket, MariaDB, PHPMyAdmin)
 - **Doctrine ORM** et les commandes Doctrine
 - le **Symfony web profiler** pour débugger les requêtes de la RestApi et les événements Push
 - [Silex annotations](https://github.com/danadesrosiers/silex-annotation-provider) pour les annotations de contrôleurs et de routing

Jetez-y un œil :

💻 [Sandstone edition](https://github.com/eole-io/sandstone-edition)


Vous pouvez aussi partir de zéro, ou l'intégrer dans une application Silex existante :

💻 [Sandstone](https://github.com/eole-io/sandstone)

📖 [Documentation de Sandstone](https://eole-io.github.io/sandstone/)


{{< ccby >}}

{{< comments >}}
