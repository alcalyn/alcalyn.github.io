---
title: Matomo Signup Plugin
date: '2019-04-20'
aliases:
- /../projects/2019-04-20-matomo-signup-plugin/2019-04-20-matomo-signup-plugin/
summary: Allow new users to signup to your Matomo instance
featuredImage: /images/projects/matomo-signup-plugin/land.png
project: true
tags:
- php
---

- Matomo marketplace Signup plugin: <https://plugins.matomo.org/Signup>
- Github repository: <https://github.com/alcalyn/matomo-plugin-signup>

## What is Matomo

Matomo is a free/libre alternative to Google analytics.

If you want to analyse users that are interacting with your website,
you can self-host your own Matomo instance and add js tracking on your website.

![Matomo dashboard screenshot](matomo-screenshot.png "Matomo dashboard screenshot")

This is what I'm using on this blog.

## Why this plugin?

So I self-host my own instance of Matomo.
But I use it only for this blog and a documentation site,
which let many unused bandwith to my dedicated server.

I wanted to share my instance with other people
that have a little blog and don't want to install their instance
or don't want to use google analytics.

So I needed to add a signup workflow.

When looking for something already done,
I just found a [not maintened plugin for an old version of Piwik](https://github.com/eristoddle/PiwikSignupPlugin),
and some discussion on Github issues on Matomo repository
([#8358](https://github.com/matomo-org/matomo/issues/8358),
[#7622](https://github.com/matomo-org/matomo/issues/7622)).

I read in these discussions that actually this plugin is really wanted and could also fit others uses cases.

So "why this plugin?":

- Share our instance plublicly (mine)
- In a private instance (i.e organization), allows new contributors to create their access instead of asking to the administrator

## What I needed to build this plugin

- [The Matomo developer documentation](https://developer.matomo.org/develop) helped me a lot to start develop my plugin.
- [All existing plugins from Matomo](https://github.com/matomo-org/matomo/tree/3.x-dev/plugins) also was a gold resources, I looked into plugins source code that does similar things.

This plugin is available on Matomo marketplace, or downloadable from github repository.
You can install it directly through your admin interface.

![Plugin installable from marketplace](plugin-marketplace.png "Plugin installable from marketplace")

{{< ccby >}}
