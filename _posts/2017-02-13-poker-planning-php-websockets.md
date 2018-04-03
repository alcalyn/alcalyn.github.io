---
title: Creating a poker planning application with PHP and websockets
tags:
    - php
excerpt: Are you sure that PHP is not able to use websockets, send push notifications, and make a real-time application ?
---

{% include toc title="Summary" %}

{% include figure
    image_path="/assets/images/poker-planning-php-websockets/app-screenshot.png"
    caption="Poker planning application screenshot"
    alt="Poker planning application screenshot"
%}

When searching in Github for real-time poker planning application,
there is already multiple repositories using websockets on Github:

 - [Wizehive/Firepoker](https://github.com/Wizehive/Firepoker) (Javascript)
 - [WASdev/sample.planningpoker](https://github.com/WASdev/sample.planningpoker) (JAVA)
 - [WayneYe/ScrumPoker](https://github.com/WayneYe/ScrumPoker) (Javascript)
 - [dctse/ScrumPoker](https://github.com/dctse/ScrumPoker) (Javascript)
 - [simbo1905/sprint-planning](https://github.com/simbo1905/sprint-planning) (Scala)
 - [qJake/planning-poker](https://github.com/qJake/planning-poker) (C#)
 - [richarcher/Hatjitsu](https://github.com/richarcher/Hatjitsu) (Javascript)
 - [inovex/planning-poker](https://github.com/inovex/planning-poker) (Javascript)

Written in Javascript (and nodejs in many cases), JAVA, Scala, C#...

The one written in PHP I can find on the first Github search page
uses ajax requests every seconds [Toxantron/scrumonline](https://github.com/Toxantron/scrumonline):

{% include figure
    image_path="/assets/images/poker-planning-php-websockets/ajax.png"
    caption="Firebug network tab showing ajax polling"
    alt="Firebug network tab showing ajax polling"
%}

But does it means that PHP is not able to use websockets and make a real-time application ?

I often hear that PHP is not good for websockets, that it's better to use nodejs blablabla

In fact, if I want to build a real-time application,
I don't care about using PHP or nodejs, or using websockets or something like long-polling...

But if you are already in a PHP eco-system, or if you love PHP,
you may want to build your real-time application using PHP.

I'm not saying that PHP is a secondary choice, "because I don't have the choice",
but this article will proove that it is possible to build
a real time application using websockets over PHP.

I also do it in a structured code, and not only a `websocket-server.php` file
you can find in all the "PHP chat with websockets" tutorials on the web.


## Let's build a real-time application

I'll do it with Sandstone.
This library extends Silex, so if you know Silex,
you know already the half part of this tuto (the RestApi part).

Sandstone also adds websockets support,
and provide some abstraction tools to create websocket topics the more simple way,
or the more "Silex way".

### What are the application needs

My need is to build a planning poker application, where we can start a poker session, let teammates join it, and let them vote.

So, in a first part, I will build a RestApi with resources:

 - `/teams`: create a team, get a list of existing teams, join a team
 - `/users`: create an user with a pseudo, make an user vote (1, 2, 3, 5, 8, ...).

Then, I will build the second part of the application, the real time vote using websockets.

> I mean by *real time vote* the fact by once an user votes,
> all others user interfaces will be updated instantly:
> the user send the vote information to the server,
> then the server broadcast the vote information to others users in the team
> (no Ajax request every seconds).

### Technical stack

- Server:
    - Sandstone:
        - RestApi: create/join rooms
        - Websocket server: be notified when someone join our team, vote, or team vote is finished to refresh the view in real-time.
- Client:
    - Bootstrap 4 + jQuery + Js app which uses api

I'll use Docker and docker-compose, so that you don't have to install PHP, ZMQ and ZMQ PHP extension.

> **Note**:
> The application I'll build in this article is available on Github:
> [alcalyn/poker-planning](https://github.com/alcalyn/poker-planning)


## Part I: Rest Api with Silex

If you know Silex, you already know this part.
We use Silex to build a light RestApi which handle the `/teams` and `/users` resources.

> [Silex](http://silex.sensiolabs.org/) is a microframework which allows to mount a web application easily,
> with a light router, a light service container ([Pimple](http://pimple.sensiolabs.org/))...

### Install Sandstone

Let's bootstrap a Silex application, but not from scratch.

I will use here the [Sandstone edition](https://github.com/eole-io/sandstone-edition).

Sandstone edition is a Silex skeleton with websockets, Doctrine, JMS Serializer, web profiler...

Using Docker, following [the documentation](https://github.com/eole-io/sandstone-edition):

``` bash
curl -L https://github.com/eole-io/sandstone-edition/archive/dev.tar.gz | tar xz
cd sandstone-edition-dev/

make
```

> Docker helps us to mount our application web server, websocket server, ...
> so we don't have to install all that stuff.

Let's check that it's well installed by going to the diagnostic page:
[http://0.0.0.0:8480/hello/world.html](http://0.0.0.0:8480/hello/world.html).

> If there is still orange or red boxes,
> you may just need to `chmod -R 777 var/*` or `chown -R USER:GROUP .`

I also have an access to the **Symfony web profiler** here:
[http://0.0.0.0:8480/index-dev.php/_profiler/](http://0.0.0.0:8480/index-dev.php/_profiler/).


### The Sandstone edition structure

The edition has in fact 2 stacks:

 - The **RestApi** stack (`app/RestApiApplication`),
 - The **websocket** stack (`app/WebsocketApplication`).

These 2 stacks extend a **common stack** (`app/Application`).

By this way, we do not load RestApi controllers in the websocket server,
and we do not load websocket topics in RestApi stack.

**Application**, the common stack, contains:
 - services
 - Doctrine mappings
 - serializer metadata


{% include fa icon="long-arrow-right" %} **RestApiApplication**, the RestApi stack, contains:
 - controllers
 - converters
 - events to forward


{% include fa icon="long-arrow-right" %} **WebsocketApplication**, the Websocket stack, contains:
 - websocket topics


### Create database schema and entities with Doctrine

The basic scenario is:

The user enters his pseudo, then see the list of the teams.
He selects a team, then see the users and can vote.

{% include figure
    image_path="/assets/images/poker-planning-php-websockets/uml.png"
    caption="Poker planning DCM"
    alt="Poker planning DCM"
%}

So let's map `User` and `Team` entities with Doctrine, in yaml format:

`src/App/Resources/doctrine/App.Entity.User.dcm.yml`:
``` yaml
App\Entity\User:
    type: entity
    repositoryClass: App\Repository\UserRepository
    id:
        id:
            type: integer
            generator:
                strategy: AUTO
    fields:
        pseudo:
            type: string
        vote:
            type: smallint
            nullable: true
    manyToOne:
        team:
            targetEntity: Team
            reversedBy: users
```

`src/App/Resources/doctrine/App.Entity.Team.dcm.yml`:
``` yaml
App\Entity\Team:
    type: entity
    repositoryClass: App\Repository\TeamRepository
    id:
        id:
            type: integer
            generator:
                strategy: AUTO
    fields:
        title:
            type: string
        voteInProgress:
            type: boolean
    oneToMany:
        users:
            targetEntity: User
            mappedBy: team
```

> **Note**:
> I don't want to generate php model classes manually,
> so using yaml mapping allows me to generate them automatically.

Let's tell Doctrine to use our yaml files (replace the `'annotation'` one):

`src/App/HelloProvider.php`:
``` php
<?php

        $app->extend('doctrine.mappings', function ($mappings, $app) {
            $mappings []= [
                'type' => 'yml',
                'namespace' => 'App\\Entity',
                'path' => $app['project.root'].'/src/App/Resources/doctrine',
                'alias' => 'App',
            ];

            return $mappings;
        });
```

Then auto generate entities, and update the database schema:

``` bash
# Entering in php container
make bash

# Generate php model classes
bin/console orm:generate-entities src/

# Update database schema
bin/console orm:schema-tool:update --force
```

You should see the generated entities in `src/App/Entity/`,
and the tables in your phpmyadmin interface [http://0.0.0.0:8481/](http://0.0.0.0:8481/).


### Create Rest controllers

We now want a lot of routes such as:
 - `POST /users` route when a new user comes and enter his pseudo,
 - `GET /teams` for the teams list,
 - `PUT /teams/{team}/users/{user}` when an user joins a team,
 - `POST /users/{user}/vote` to allow a player vote...

#### Team controller

I won't expose all controllers, but just the `POST /users/{user}/vote` one as an example.

> **Note**: The whole application is available on Github,
> so check on Github [src/App/Controller](https://github.com/alcalyn/poker-planning/tree/master/src/App/Controller)
> to see all others controllers.

Let's implement the `POST /users/{user}/vote` route:

`src/App/Controller/UserController.php`

``` php
<?php

namespace App\Controller;

use Pimple\Container;
use Symfony\Component\HttpKernel\Exception\BadRequestHttpException;
use Symfony\Component\HttpKernel\Exception\ConflictHttpException;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\Response;
use Alcalyn\SerializableApiResponse\ApiResponse;
use DDesrosiers\SilexAnnotations\Annotations as SLX;
use App\Entity\User;
use App\Event\UserEvent;

/**
 * @SLX\Controller(prefix="/api")
 */
class UserController
{
    /**
     * @var Container
     */
    private $container;

    /**
     * @param Container $container
     */
    public function __construct(Container $container)
    {
        $this->container = $container;
    }

    /**
     * Vote. Vote number must be in body, and number in Fibonacci sequence.
     *
     * @SLX\Route(
     *      @SLX\Request(method="POST", uri="/users/{user}/vote"),
     *      @SLX\Convert(variable="user", callback="app.converter.user:convert")
     * )
     *
     * @param Request $request
     * @param User $user
     *
     * @throws BadRequestHttpException If vote is not in Fibonacci sequence.
     * @throws ConflictHttpException When trying to vote once the team has finished voting.
     *
     * @return ApiResponse
     */
    public function postVote(Request $request, User $user)
    {
        $pokerPlanning = $this->container['app.poker_planning'];
        $vote = intval($request->getContent());
        $team = $user->getTeam();

        if (!$pokerPlanning->isVoteFibonacci($vote)) {
            throw new BadRequestHttpException('Vote must be in Fibonacci sequence.');
        }

        if (!$team->getVoteInProgress()) {
            throw new ConflictHttpException('Cannot vote now, votes are closed.');
        }

        $user->setVote($vote);

        if ($pokerPlanning->hasTeamVoted($team)) {
            $team->setVoteInProgress(false);
        }

        $this->container['orm.em']->persist($user);
        $this->container['orm.em']->flush();

        return new ApiResponse(null, Response::HTTP_NO_CONTENT);
    }
}
```


### Tiny controllers, thanks to converters

I don't want to do a `->getRepository('Team')->findById($id)` in my controllers.

So I can use converters (see [Silex converters](http://silex.sensiolabs.org/doc/2.0/usage.html#route-variable-converters)).

For example, `src/App/Converter/TeamConverter.php`:

``` php
<?php

namespace App\Converter;

use Symfony\Component\HttpKernel\Exception\NotFoundHttpException;
use App\Repository\TeamRepository;

class TeamConverter
{
    /**
     * @var TeamRepository
     */
    private $teamRepository;

    /**
     * @param TeamRepository $teamRepository
     */
    public function __construct(TeamRepository $teamRepository)
    {
        $this->teamRepository = $teamRepository;
    }

    public function convert($id)
    {
        $team = $this->teamRepository->find($id);

        if (null === $team) {
            throw new NotFoundHttpException('Team not found.');
        }

        return $team;
    }
}
```

Then I magically get my instances in my controllers from arguments when I do:

``` php
<?php

    /**
     * Make an user joins a team.
     *
     * @SLX\Route(
     *      @SLX\Request(method="PUT", uri="/teams/{team}/users/{user}"),
     *      @SLX\Convert(variable="team", callback="app.converter.team:convert"),
     *      @SLX\Convert(variable="user", callback="app.converter.user:convert")
     * )
     *
     * @param Team $team
     * @param User $user
     *
     * @return ApiResponse
     */
    public function addUser(Team $team, User $user)
    {
        $team->addUser($user);
        $user->setTeam($team);

        $this->container['orm.em']->persist($team);
        $this->container['orm.em']->flush();

        return new ApiResponse($team, Response::HTTP_OK);
    }
```

where `app.converter.team:convert` and `app.converter.user:convert`
are callbacks to the `convert` method in TeamConverter and UserConverter.

Sure, converters need to be registered first as a service in RestApi stack:

`src/App/HelloRestApiProvider.php`

``` php
<?php

use App\Converter\TeamConverter;
use App\Converter\UserConverter;

// ...

        $app['app.converter.team'] = function () use ($app) {
            return new TeamConverter($app['orm.em']->getRepository('App:Team'));
        };

        $app['app.converter.user'] = function () use ($app) {
            return new UserConverter($app['orm.em']->getRepository('App:User'));
        };
```

### Move some logic from controller to service

As you know, business logic should be in services.

The service `app.poker_planning` contains some logic relative to Poker Planning voting.

`src/App/Service/PokerPlanning.php`:

``` php
<?php

namespace App\Service;

use App\Entity\Team;

class PokerPlanning
{
    /**
     * Check is a vote is in Fibonacci sequence.
     *
     * @param int $vote
     *
     * @return boolean
     */
    public function isVoteFibonacci($vote)
    {
        return in_array($vote, [1, 2, 3, 5, 8, 13, 21, 34]);
    }

    /**
     * Check whether all users voted.
     *
     * @param Team $team
     *
     * @return boolean
     */
    public function hasTeamVoted(Team $team)
    {
        foreach ($team->getUsers() as $user) {
            if (null === $user->getVote()) {
                return false;
            }
        }

        return true;
    }
}
```

Let's register the service in common stack:

In `src/App/HelloProvider.php`:
``` php
<?php

use App\Service\PokerPlanning;

// ...

        $app['app.poker_planning'] = function () {
            return new PokerPlanning();
        };
```

Check your API by retriving all teams: <http://0.0.0.0:8480/index-dev.php/api/teams>

I also provide a Postman collection, so that you can play pre-saved requests.
The collection is available here: [poker-planning-postman-collection.json](https://github.com/alcalyn/poker-planning/blob/master/poker-planning-postman-collection.json).


## Part II: Real-time stuff with websocket

Well, we now have a working RestApi where we can retrieve teams,
and post users votes.

Now, when someone votes, I want to keep updated all web clients
and display that an user voted in real-time.

But I don't want to request my RestApi every second to check if state has changed.


### Display user vote in real time

**The need**: I want the RestApi notifies me when an user votes and when all users voted
so I can reveal votes as soon as it is available.

How we will achieve that ?

The logic is:

1. Someone votes, then calls `PUT /users/1/vote`.
1. The RestApi handles the request,
1. persist to user vote,
1. then sends the 204 response to the client which has sent the vote.

But I also want that the RestApi notifies all my teammates that I voted.

**The websocket solution**:

All users should connect to a websocket,
which is a connection that stays open
so that both client and server can use it to send messages.

Then the RestApi will notify through this websocket that I voted.

Sandstone uses the WAMP protocol. So instead of connect to the websocket
and listen all messages through an unique channel,
we can create multiple channels, or "topics", and **subscribe** to a topic.

Users will then receive messages from this topic only.

I want to create a topic for each team, `teams/1`, `teams/2`, ...

And I will dispatch messages relative to the team on the team channel.

Then, every user who joins a team must also subscribes to the team channel
in order to receive real-time notifications (someone joined my team, someone voted).


#### Creating the websocket topic

Once you understand the logic, let's implement it with Sandstone.

A `Eole\Sandstone\Websocket\Topic` class is responsible of the logic behind a websocket topic.

It implements for example the method `onSubscribe`, called when an user subscribes to this topic.

> **Use case**: Send a message to new subscribing users, for example last messages sent.


It also implements the `onPublish` method, when an user send a message to this topic.

> **Use case**: For chats: broadcast back the message to every users who subscribed to this topic.


It also provides a `broadcast` method to broadcast a message to every subscribing users.

First create the topic class `src/App/Topic/TeamTopic.php`:

``` php
<?php

namespace App\Topic;

use Eole\Sandstone\Websocket\Topic;
use App\Event\UserEvent;

class TeamTopic extends Topic
{
    /**
     * @var int
     */
    private $teamId;

    /**
     * @param string $topicPattern
     * @param int $teamId
     */
    public function __construct($topicPattern, $teamId)
    {
        parent::__construct($topicPattern);

        $this->teamId = $teamId;
    }
}
```

And register the topic in websocket stack, in `src/App/HelloWebsocketProvider.php`:

``` php
<?php

namespace App;

use Pimple\ServiceProviderInterface;
use Pimple\Container;
use App\Topic\TeamTopic;

class HelloWebsocketProvider implements ServiceProviderInterface
{
    /**
     * {@InheritDoc}
     */
    public function register(Container $app)
    {
        $app
            ->topic('teams/{teamId}', function ($topicPattern, $arguments) {
                $teamId = intval($arguments['teamId']);

                return new TeamTopic($topicPattern, $teamId);
            })
            ->assert('teamId', '\d+')
        ;
    }
}
```

Web client in my team #1 can now subscribe to `teams/1`, but nothing will happens for now.


#### Forward vote event to websocket topic

I want my topic to listen to the `UserEvent::VOTED`,
which should be dispatched from the RestApi controller when someone voted.

But this event is dispatched in the RestApi stack,
whereas my topic is in the websocket stack,
this is to different processus.

Sandstone allows to dispatch event from RestApi processus to the websocket processus by *forwarding* it.

So we will need to create an event class, in `src/App/Event/UserEvent.php`:

``` php
<?php

namespace App\Event;

use Symfony\Component\EventDispatcher\Event;
use App\Entity\User;

class UserEvent extends Event
{
    /**
     * An user voted or changed his vote.
     * The listener receives an instance of UserEvent.
     *
     * @var string
     */
    const VOTED = 'event.user.voted';

    /**
     * @var User
     */
    private $user;

    /**
     * @param User $user
     */
    public function __construct(User $user)
    {
        $this->user = $user;
    }

    /**
     * @return User
     */
    public function getUser()
    {
        return $this->user;
    }
}
```

Then, disptach the event from the controller, in `src/App/Controller/UserController.php`:

``` php
<?php

namespace App\Controller;

use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\Response;
use Alcalyn\SerializableApiResponse\ApiResponse;
use App\Entity\User;
use App\Event\UserEvent;

class UserController
{
    public function postVote(Request $request, User $user)
    {
        // ...

        // Upate the user vote
        $user->setVote($vote);

        // Persist the user
        $this->container['orm.em']->persist($user);
        $this->container['orm.em']->flush();

        // + Add this line, dispatch an event with the user entity
        $this->container['dispatcher']->dispatch(UserEvent::VOTED, new UserEvent($user));

        // Return the RestApi response
        return new ApiResponse(null, Response::HTTP_NO_CONTENT);
    }
}
```

Nothing new here, just dispatching an event using Symfony EventDispatcher.

Now, we want to listen this event from the Topic class.
To make the event dispatch from RestApi processus to Websocket one,
Sandstone allows us to **forward** it:

`src/App/HelloRestApiProvider.php`:

``` php
<?php

namespace App;

use Pimple\ServiceProviderInterface;
use Pimple\Container;
use App\Event\UserEvent;

class HelloRestApiProvider implements ServiceProviderInterface
{
    /**
     * {@InheritDoc}
     */
    public function register(Container $app)
    {
        // ...

        $app->forwardEventsToPushServer([
            UserEvent::VOTED,
        ]);
    }
}
```

Then magically listen it in the `TeamTopic` class:

> By magically I mean that the event instance is serialized,
> sent to the websocket server thread through a Push server (ZeroMQ),
> then deserialized and redispatched in the websocket server application event dispatcher.
>
> By this way you're able to *magically* listen an event from another PHP thread.

``` php
<?php

namespace App\Topic;

use Symfony\Component\EventDispatcher\EventSubscriberInterface;
use Eole\Sandstone\Websocket\Topic;
use App\Event\UserEvent;

class TeamTopic extends Topic implements EventSubscriberInterface
{
    /**
     * {@InheritDoc}
     */
    public static function getSubscribedEvents()
    {
        return [
            UserEvent::VOTED => 'onUserVoted',
        ];
    }

    /**
     * @param UserEvent $event
     */
    public function onUserVoted(UserEvent $event)
    {
        // Check if the event is relative to this team
        if ($event->getUser()->getTeam()->getId() !== $this->teamId) {
            return;
        }

        // Broadcast to every websocket clients
        $this->broadcast([
            'type' => 'user_voted',
            'user' => $event->getUser(),
        ]);
    }
}
```

> **Note**:
> Don't forget to restart the websocket server
> when the source code changed with:
>
> `make restart_websocket_server`

#### Connect to websocket server from your Javascript application

You'll need to test this with a websocket Javascript client.

A JS library that can be used with Sandstone (WAMPv1/Websocket protocol)
is AutobahnJS 0.8.

> **Note**: Another one could be [wamp1](https://www.npmjs.com/package/wamp1),
> which can be loaded with npm, but I don't tested it yet.

To be short, it will be something like:

``` js
console.log('connecting to websocket server...');

ab.connect(
    'ws://0.0.0.0:8482',
    function (session) {
        console.log('connected to websocket server.');

        console.log('listening team topic');

        session.subscribe('teams/'+myTeam.id, function (topic, event) {
            console.log('something happens in my team');
            console.log(event.user.pseudo+' votes '+event.user.vote);
        });
    },
    function (code, reason, detail) {
        console.warn(code, reason, detail);
    }
);
```

The full front and back application can be installed and tested here:

{% include fa icon="github" classes="fa-lg" %} [Poker Planning](https://github.com/alcalyn/poker-planning)


{% include ccby %}
