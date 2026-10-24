---
date: '2017-10-05'
summary: Si vous utilisez NodeJS, Python ou PHP, vous connaissez peut-être déjà expressJS, Flask ou Silex. Je vais expliquer Sandstone en partant du principe que vous connaissez l'une de ces bibliothèques.
title: Sandstone expliqué aux utilisateurs de NodeJS, Python ou PHP
tags:
- php
---

*Cet article a été traduit de l'anglais.*


[Sandstone](https://github.com/eole-io/sandstone) est un microframework
qui permet de monter une Rest API,
avec en plus un comportement temps réel, grâce à son serveur websocket intégré.

Je le présente aussi à partir de zéro dans [Qu'est-ce que Sandstone]({{< relref "/projects/sandstone" >}}).

Mais je vais essayer, dans cet article, d'expliquer l'intérêt de Sandstone,
en partant du principe que vous utilisez déjà un microframework, dans n'importe quel langage.


## Les microframeworks de Rest API

Si vous utilisez NodeJS, Python ou PHP,
vous connaissez peut-être déjà, respectivement, [expressJS](http://expressjs.com/),
[Flask](http://flask.pocoo.org/) ou [Silex](https://silex.symfony.com/).

Ces microframeworks ont une logique similaire,
et permettent de démarrer rapidement une Rest API de manière minimaliste.

Par exemple, voici comment créer une route POST dans chacun de ces frameworks :

- NodeJS

``` js
app = express()

app.post('/api/articles', function (request, response) {
    response.status(201).send('Article created')
})
```

- Flask Python

``` python
@app.route('/api/articles', methods=['POST'])
def post_article():
    return 'Article created', 201
```

- Silex PHP

``` php
<?php
$app = new Silex\Application();

$app->post('/api/articles', function () {
    return new Response('Article created', 201);
});
```

On les appelle microframeworks parce qu'ils sont conçus
pour ajouter facilement des routes, et qu'ils peuvent contenir toute une Rest API dans un seul fichier.

Maintenant, parlons de Rest API temps réel.


## Vous avez dit Rest API temps réel ?

Une Rest API, c'est uniquement des requêtes et des réponses, donc pas de temps réel.
Pourtant, on a souvent besoin de temps réel, même quand on pense que non !

### Pourquoi aurais-je besoin de temps réel ?

Disons que vous avez la Rest API d'un blog, sur laquelle vous pouvez publier de nouveaux articles
avec la route `POST /api/articles`. D'un autre côté, vous voulez afficher
sur une interface web une notification push dès qu'un nouvel article vient d'être publié.

> Une notification push est en général une notification asynchrone
> envoyée par le serveur aux clients (web, mobile...), afin de les prévenir
> d'un événement qui vient de se produire.

Vous pouvez utiliser de l'Ajax et faire `GET /api/articles` toutes les secondes, puis vérifier si un nouvel article
a été publié. Mais c'est un mauvais pattern : chaque client web va interroger
votre serveur en Ajax en continu, ce qui peut représenter beaucoup de requêtes inutiles par seconde.
Inutiles parce que la plupart des réponses seront identiques à la précédente : pas de nouvel article.

### Quand utiliser une connexion websocket

En général, quand on commence à interroger sa Rest Api toutes les secondes pour vérifier
si l'état a changé, il est temps d'inverser le sens de la connexion :
**c'est votre serveur qui doit envoyer des messages au client**.

C'est exactement ce pour quoi les websockets sont conçues : garder une connexion bidirectionnelle ouverte
pour que le serveur et le client puissent s'envoyer des messages.

### Séparer la connexion websocket en plusieurs topics

Les topics sont comme des « canaux » pour votre connexion websocket.
Au lieu d'envoyer un message par l'unique connexion websocket
du serveur vers tous les clients websocket, vous pouvez créer autant de topics que vous voulez.
Le serveur websocket envoie les messages à un topic précis,
et les clients websocket ne s'*abonnent* qu'aux topics dont ils veulent recevoir les messages.

Les topics permettent de n'envoyer des messages qu'aux clients qui y sont abonnés.
Vous pouvez définir des callbacks différents pour chaque topic,
puisque le format des messages sera sûrement différent d'un topic à l'autre.

Exemple avec AutobahnJS 0.8, un client Javascript WAMP/Websocket :

``` js
session.subscribe('article_created', function (topic, event) {
    console.log('New Article:', event.article.title);
});

session.subscribe('chat', function (topic, event) {
    console.log('chat message:', event.message);
});
```

> Le [protocole WAMP](http://wamp-proto.org/) se superpose au protocole websocket
> pour ajouter des spécifications sur l'utilisation des topics dans une connexion websocket.


## Créons mon application temps réel !

Créer et faire tourner un serveur websocket n'est pas aussi simple que de monter une
Rest API, ce qui est aujourd'hui trivial dans de nombreux langages.

Envoyer des notifications push est aussi délicat quand elles sont
déclenchées par une requête sur la Rest API : impossible de
diffuser un message websocket depuis la pile de la Rest API, car c'est un
processus différent.

### Comment Sandstone peut m'aider ?

Le but principal de Sandstone est d'abstraire ces deux points :

- déclarer un topic de la même manière qu'une route de Rest API,
- utiliser l'event dispatcher de Symfony pour envoyer une notification push.

### Déclarer des topics comme une route de Rest API

Imaginez maintenant que vous puissiez déclarer un topic websocket aussi facilement qu'une route
(ici dans un langage proche du JavaScript) :

``` js
app.topic('/chat/{channel}', function (request, response) {
    return new function (channel) {
        this.onSubscribe = function () {
            this.send('Welcome on '+channel);
        }

        this.onPublish = function (message) {
            this.broadcast(message);
        }
    }
})
```

Ainsi, les clients web peuvent s'abonner aux topics `chat/general` ou `chat/news`
pour recevoir les messages envoyés par les autres clients web.

Ensuite, lancer votre application lance aussi un serveur websocket auquel vous pouvez vous connecter.

C'est le premier objectif de Sandstone. Il est conçu pour [déclarer des topics websocket
de la même manière qu'une route, avec des arguments de route](https://eole-io.github.io/sandstone/topic-route-parameters.html) :

``` php
<?php

$app->topic('chat/general', function ($topicPattern) {
    return new ChatTopic($topicPattern);
});
```

> Voir un [exemple de classe `ChatTopic` ici](https://eole-io.github.io/sandstone/examples/multichannel-chat.html).

### Envoyer une notification push

Maintenant, quelqu'un publie une nouvelle ressource via la Rest API.
Cela appelle le contrôleur, qui enregistre la ressource en base de données
et renvoie une réponse.

C'est quelque chose de trivial avec un microframework, comme l'illustrent les exemples
en plusieurs langages au début de cet article.

Prévenons les clients web qu'une nouvelle ressource a été créée. Cela signifie :

- mon contrôleur envoie cette ressource au processus websocket,
- le serveur websocket reçoit la ressource et la diffuse sur le bon topic.

Mais vos contrôleurs ne devraient dépendre ni d'un processus websocket,
ni d'un service qui sérialise un message vers le serveur websocket à travers une socket...

Le second objectif de Sandstone est d'abstraire ce fonctionnement.

En fait, Sandstone utilise l'event dispatcher de l'application.
Vous pouvez [écouter depuis le serveur websocket des événements que votre contrôleur
a dispatchés](https://eole-io.github.io/sandstone/#send-push-notifications-from-restapi).
Ça ressemble à ça :

- **Rest API**, contrôleur :

``` php
<?php

$app->post('api/articles', function () use ($app) {
    $event = new ArticleEvent();

    $event->title = 'Unicorns spotted in Alaska';

    // Dispatche un événement à la création d'un article
    $app['dispatcher']->dispatch('article.created', $event);

    return new Response([], 201);
});
```

- **Serveur websocket**, instance du topic :

``` php
<?php

class MyWebsocketTopic extends Eole\Sandstone\Websocket\Topic implements EventSubscriberInterface
{
    public static function getSubscribedEvents()
    {
        return [
            'article.created' => 'onArticleCreated',
        ];
    }

    public function onArticleCreated(ArticleEvent $event)
    {
        // Diffuse un message sur ce topic quand un article a été créé.
        $this->broadcast([
            'message' => 'An article has just been published: '.$event->title,
        ]);
    }
}
```


## Pour démarrer

Voilà pour les deux fonctionnalités principales de Sandstone : abstraire la création
d'un serveur websocket, des topics, et des notifications push depuis la Rest API.

Construire une application temps réel en PHP devient alors possible.
Je montre dans
[Créer une application de poker planning avec PHP et les websockets]({{< relref "/posts/poker-planning-php-websockets" >}})
comment en créer une simple avec Sandstone.

Si vous voulez démarrer :

- Documentation de Sandstone : <https://eole-io.github.io/sandstone/>
- Sandstone sur github : <https://github.com/eole-io/sandstone>
- Sandstone edition (une application de base pour démarrer une Rest API temps réel) : <https://github.com/eole-io/sandstone-edition>


{{< ccby >}}
