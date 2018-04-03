---
tags:
    - php
---

Build a real-time RestApi.

## What is Sandstone

Sandstone is a PHP microframework.
The main purposes of this microframework are:

 - Building a RestApi
 - Mount a websocket server
 - Easily send push notifications.

Sandstone is based on [Silex](https://silex.symfony.com/), the Symfony microframework.

If you don't know Silex, it is a minimalist web framework
similar to [expressjs](http://expressjs.com/fr/) in nodejs,
or [flask](http://flask.pocoo.org/) in python.

## What can I do with Sandstone

You can easily bootstrap a RestApi, and add real-time stuff, such as:

 - Notify all web clients that a new article has just been published through the RestApi
 - Create a chat working with your RestApi
 - For a game server, broadcasting players moves as soon as someone played

## How to get started

If you're starting a new project, you should be interested
in the [Sandstone edition](https://github.com/eole-io/sandstone-edition).

It is a fresh installation of Sandstone you can start from to build a real-time RestApi,
and also contains debug features.

This edition integrates:

 - [Sandstone](https://eole-io.github.io/sandstone/) (Silex with websockets)
 - **Docker** environment to mount the whole application (RestApi, websocket server, MariaDB, PHPMyAdmin)
 - **Doctrine ORM** and Doctrine commands
 - **Symfony web profiler** for debugging RestApi requests and Push events
 - [Silex annotations](https://github.com/danadesrosiers/silex-annotation-provider) for controllers and routing annotations

Check it out:

{% include fa icon="github" classes="fa-lg" %} [Sandstone edition](https://github.com/eole-io/sandstone-edition)


Or you can start from scratch or integrate it in an existing Silex application:

{% include fa icon="github" classes="fa-lg" %} [Sandstone](https://github.com/eole-io/sandstone)

{% include fa icon="book" classes="fa-lg" %} [Sandstone documentation](https://eole-io.github.io/sandstone/)


{% include ccby %}
