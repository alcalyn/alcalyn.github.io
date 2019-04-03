---
title: Sandstone explained to NodeJS, Python or PHP users
locale: en
tags:
    - php
excerpt: If you're a NodeJS, Python or PHP user, you may already know expressJS, Flask or Silex. I'll explain Sandstone assuming you already know one of these libraries.
---

{% include toc title="Summary" %}

[Sandstone](https://github.com/eole-io/sandstone) is a microframework
that allows you to mount a Rest API,
with also a real-time behaviour, thanks to its integrated websocket server.

I'm also describing it from scratch in [What is Sandstone]({{ site.baseurl }}{% link _projects/2017-01-01-sandstone.md %}).

But I'll try, in this post, to explain the benefit of Sandstone,
assuming you already use a microframework in any programming language.


## Rest API Microframeworks

If you're a NodeJS, Python or PHP user,
you may already know, respectively, [expressJS](http://expressjs.com/),
[Flask](http://flask.pocoo.org/), or [Silex](https://silex.symfony.com/).

These microframeworks have a similar logic,
and you can quickly bootstrap a Rest API in a minimalist way.

For example, here is how to create a POST route in every of these frameworks:

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

They are called microframework because they are designed
to easily add routes, and may contain a whole Rest API in a single file.

Now, let's talk about real-time Rest API.


## You said a real-time Rest API?

Rest API means only request and response, so no real-time.
Nonetheless, you often need real-time, even when you think you don't!

### Why may I need real time?

Let's say that you have a blog Rest API where you can POST new articles
by using the `POST /api/articles` route. In an other side, you want to display
on a web interface a push notification once a new article has just been published.

> A push notification is generally an asynchronous notification
> sent by the server to clients (web, mobile...), in order to notify them
> from an event that just happened.

You can use Ajax, and doing `GET /api/articles` every second, then check if a new article
has been published. But this is a wrong pattern as every web client will ajax
your server continuously, and may result as many useless requests per second.
Useless because most of the response will be the same as the last one: no new article.

### When to use a websocket connection

Generally, when you start to request every second your Rest Api to check
whether state has changed, it's time to reverse the connection direction:
**your server must send messages to client instead**.

This is what websockets are designed for: keeping a bidirectionnal connection open
so that both server and client can send messages to each other.

### Separate the websocket connection into multiple topics

Topics are like "channels" for your websocket connection.
Instead of sending a message through the single websocket connection
from server to every websockets clients, you can create as many topics as you want.
The websocket server has to send messages to a specific topic,
and websocket clients *subscribe* only to topics they want to receive messages.

Topics allows to send messages to clients only if they subscribed to.
You can define different callbacks for each topics,
as messages formats should be different between topics.

Example using AutobahnJS 0.8, a WAMP/Websocket Javascript client:

``` js
session.subscribe('article_created', function (topic, event) {
    console.log('New Article:', event.article.title);
});

session.subscribe('chat', function (topic, event) {
    console.log('chat message:', event.message);
});
```

> The [WAMP protocol](http://wamp-proto.org/) overlays the websocket protocol
> to add specifications on using topics in a websocket connection.


## Let's create my real time application!

Creating and running a websocket server is not as straitforward as mounting a
Rest API, which is nowadays something trivial in many languages.

Sending push notifications is also tricky when they are
triggered when someone requests the Rest API: it's impossible to
broadcast a websocket message from the Rest API stack as it is a different
processus.

### How Sandstone can help me to do that?

The main purpose of Sandstone is abstracting these two points:

- declare a topic the same way as declaring a Rest API route,
- uses the Symfony event dispatcher to send a push notification.

### Declare topics like a Rest API route

Now imagine you can also declare a websocket topic as easy as declaring a route
(here in a JavaScript-like language):

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

This way, web clients can subscribe to `chat/general` or `chat/news` topics
to receive messages sent by other web clients.

Then, by running your application, it also run a websocket server you can connect to.

This is the first purpose of Sandstone. It is designed to [declare websocket topics
the same way as declaring a route and using route arguments](https://eole-io.github.io/sandstone/topic-route-parameters.html):

``` php
<?php

$app->topic('chat/general', function ($topicPattern) {
    return new ChatTopic($topicPattern);
});
```

> See an [example of `ChatTopic` class here](https://eole-io.github.io/sandstone/examples/multichannel-chat.html).

### Sending push notification

Now, someone posts a new resource through the Rest API.
Then it calls the controller, which persists the resource to the database,
and returns a response.

Something trivial you can do with a microframework, illustrated by examples in
the beginning of this article in many languages.

Let's notify web clients that a new resource has been created. That means:

- my controller send this resource to the websocket processus,
- websocket server receive the resource and broadcast it to the right topic.

But your controllers shouldn't depend to any websocket processus,
or to a service that serialize a message to websocket server through a socket...

The second purpose of Sandstone is abstracting this workflow.

In fact, Sandstone uses the application event dispatcher.
You can [listen events from websocket server that your controller
dispatched](https://eole-io.github.io/sandstone/#send-push-notifications-from-restapi).
It looks like that:

- **Rest API**, controller:

``` php
<?php

$app->post('api/articles', function () use ($app) {
    $event = new ArticleEvent();

    $event->title = 'Unicorns spotted in Alaska';

    // Dispatch an event on article creation
    $app['dispatcher']->dispatch('article.created', $event);

    return new Response([], 201);
});
```

- **Websocket server**, topic instance:

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
        // Broadcast message on this topic when an article has been created.
        $this->broadcast([
            'message' => 'An article has just been published: '.$event->title,
        ]);
    }
}
```


## Get started

Well, that was the two main features of Sandstone, abstracting the creation
of a websocket server, topics, and push notifications from Rest API.

Building a real time application with PHP is then possible.
I'm showing in
[Creating a poker planning application with PHP and websockets]({{ site.baseurl }}{% post_url 2017-02-13-poker-planning-php-websockets %})
how to create a simple one with Sandstone.

If you want to get started:

- Sandstone documentation: <https://eole-io.github.io/sandstone/>
- Sandstone github: <https://github.com/eole-io/sandstone>
- Sandstone edition (a base application to start a real time Rest API): <https://github.com/eole-io/sandstone-edition>


{% include ccby %}
