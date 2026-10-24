---
date: '2016-11-09'
summary: Things not to forget when starting and maintaining an open source project.
title: Starting an open source PHP project
tags:
- php
---

*This article was translated from French.*


Releasing an existing project, or creating a new one in a
collaborative way, is becoming a more and more obvious choice. Indeed, it's
a good way to share your solution, and therefore to share
the problems too, and the saying "A problem shared is a problem
half solved." then makes sense.

But it's also a set of methods and standards that can be
new and not so obvious for someone who would like to join
the movement.

In this article, which goes from the birth of a PHP project or
library to setting up continuous integration tools
to make outside contributions easier, I'll go through all
the steps and the questions you should ask yourself.

## The birth of your project

### Talk about the idea, challenge it, listen to the first feedback

We often like to keep an idea to ourselves, develop it and make it
known under our own name. If you want to make your project open
source and receive contributions, you'll have to accept that
others will "mess up" your beautiful source code, still free of any bug.

“Adding a Bundle means that you are ok with all members messing with it”

— Second rule of Friends of Symfony.
<https://friendsofsymfony.github.io>

And don't keep the idea to yourself, share it! Will others
use your project, or find it useless? Talking about it
will let you hear feedback and challenge
your own idea.

### Make an online presentation page

Even before starting any development, create a
presentation page for the project, or a page showing how to use the
library.

On top of showing users what the project is for, it will clarify your
ideas and help contributors head in the same
direction.

Also allow and organize comments and discussions by
using Github issues, or an external tool such as Gitter
(<https://gitter.im>), which provides a real-time
chat between contributors and users.

## Creating the repository

### Create an open repository from the start

The repository is where the most up-to-date version of your
project's source code is stored. It is often a version control system (git,
svn, …) installed on an online server (Github, Bitbucket, …) so that
everyone can get and modify the source code.

A trap to avoid is creating a closed repository, not open to the public, and
telling yourself you'll open it later, when the project is “presentable”,
“ready”, or even “finished”. In reality, a project is never finished,
and will always carry technical debt: bugs, code to
simplify... So starting with this mindset dooms the repository to stay
closed forever.

So open it right away, and keep it always working,
even if it doesn't do much yet!

### The first file of your project: the Readme

No, the first file of your PHP project is not an `index.php`, a
`.gitignore`, or a `composer.json`.

If you use Github, you'll notice that the Readme
file is no longer the ignored file it used to be on
CD-ROMs. Github displays the content of this file on the project's home
page, so it's the first file read by a newcomer
to the project.

The Readme file should contain the project's description, who it's
for, what it does… Personally, I often use an
elevator speech template. It's a very short description of a project
that should let someone else understand what it's
for. The idea was born in the USA, and the principle is to be able to
explain your project to a future customer during an
elevator ride.

### Choose an open source license

The license states whether you allow your project to be reused,
modified by other people and redistributed...

First of all, note that if you don't put a license on your project, it
will be private by default, and any reuse will be forbidden.

Open source licenses are complicated in their details, but you
can keep it simple. Until now, I've only used 2 licenses: MIT and
GNU-GPL.

MIT is a very permissive open source license that allows anything
with the source code: reusing it, integrating it in a closed project…
It's a useful license for a small library you want to make
available without worrying about how it is used afterwards.

GNU-GPL is an open source license that forces projects using
GNU-GPL code to be released under this same license as well. This makes it
contagious, and comes from the activist side of the Free Software Foundation.
I use this license for projects where I want everyone
who reuses them for public use to also make their project
open source.

So unless you have a very specific legal requirement, using
these two licenses is a quick and simple choice, and they are the
most used licenses for projects on Github according to these
statistics: <https://github.com/blog/1964-open-source-license-usage-on-github-com>.

You can still discover all the other open source licenses
on [opensource.org](https://opensource.org/), and the Free Software
licenses on [fsf.org](http://www.fsf.org/). There are more
than a hundred of them, and some may suit your
project better. Example with the AGPL vs GPL license:
<https://www.gnu.org/licenses/why-affero-gpl.fr.html>.

There is also a website that can help you choose a license:
<http://choosealicense.com/>.

### Creating a PHP library? Add it to Packagist!

Your project or library will probably depend on other libraries, and
could also be a building block of another project.

To avoid installing dependencies by hand, use a
dependency manager.

In PHP, you'll need [Composer](https://getcomposer.org/) to
list the libraries your project uses, and Composer will take
care of installing them, along with the dependencies of the dependencies…

You'll also be able to update them, and so avoid having outdated
dependencies in which vulnerabilities have been
discovered.

If your project is a library meant to be used as a
building block in other PHP projects, add it to
[Packagist](https://packagist.org/)!

Packagist is the main repository of libraries using
Composer.

Putting it on Packagist lets your library's users
easily add it as a dependency of their project. It also
makes it easier to install, a plus for getting started
with it.

## Start the development

### Don't get stuck in a never-ending project start

A good approach is to use the MVP (Minimum Viable Product). This
method was developed by Eric Ries, in his book The Lean Startup.
The goal is to start with the most important features
of your project, the ones people will adopt quickly. And for
that, you need to know which ones they are.

So don't hesitate to release first versions very quickly, and
understand the feedback.

### Don't forget to set a coding standard from the start

Everyone has a different coding style. This can make it hard
to read someone else's code, and make
contributions harder when it's difficult to agree on a way
to write the same code.

#### Settle how code is written

One of the benefits of coding standards is to normalize the coding
style. Standards contain rules, such as the number of spaces
used for indentation, whether opening braces go on the
same line or on a new line…

These rules make code reviews smoother by avoiding long
discussions about the best way to code.

#### Limit careless mistakes

But coding standards do more. They also help
limit careless mistakes. For example, I want to test whether a
variable equals 5:

``` php
if ($a = 5) {}
```

Notice that I accidentally forgot an “=”.

This will assign 5 to the variable \$a, and enter the
if. It won't raise any error because the syntax is correct, even though
I made a typo.

It's a hard bug to track down because it is silent, and we've all
made it at least once.

Some coding standards require putting the value on the left of the
variable. This rule is called the “Yoda condition”
(<https://en.wikipedia.org/wiki/Yoda_conditions>),
I'll let you guess the reference ;)

If I had followed this rule, I would have written:

``` php
if (5 = $a) {}
```

Which would have raised a syntax error, that I would have immediately
fixed with:

``` php
if (5 == $a) {}
```

So as this example shows, another benefit of coding standards
is to enforce a writing style that makes some careless
mistakes obvious.

#### What about PHP?

In PHP, the most used standard is the one from the PHP standards,
PSR-2
(<http://www.php-fig.org/psr/psr-2/>).

### Set up unit tests and integration tests

Every new feature you add to your application
may cause regressions, and break other features. So
besides testing your new feature, you would also need to test
all the other features already implemented: that's the
famous cycle that must not be named.

This quickly becomes impossible because, first, your application will offer
more and more features, and second, a new contributor
won't know your whole application, and won't be able to check whether they
broke a part of the code developed by another contributor.

This is where automated tests come in. They call
very targeted functions of the code, or simulate the use of a
feature, and check that the result is still the
expected one. These automated tests can be run on every code
change, to check that our new piece of code doesn't break anything.

Automated tests are important in an open source project, because they
prevent other contributors from causing regressions, and so
make contributing easier.

More details about tests, and a list of PHP tools here:
<http://www.hongkiat.com/blog/automated-php-test/>.

### Keep the documentation up to date, it must work at all times!

At any time, new users will come to your project.
They'll want to try it, or install the library. If at that
moment your documentation is not up to date and the user can't
try it, they'll think the project doesn't work.

That's why the installation documentation must always
work. For the user, if the installation doesn't work,
the project doesn't work; if the installation documentation is too
complicated, the project is too complicated…

Keep a working installation and usage documentation,
but also a clear and simple one, meaning as few
installation steps and odd parameters as possible.

Moreover, it can be a warning sign: if you see your
documentation getting complicated, there may be a design
problem, or something to simplify in the code itself.

If you can't simplify your usage documentation
because your library is itself complicated, try documentation
first. Put yourself in the user's shoes, and write
the docs with code examples in the way that seems the most
obvious. Then implement your library so that
the examples work.

## Welcome your contributors

### Think about the branching model

Are you a fan of everything-on-master (or everything-on-trunk for the old-timers)?
Fine, then you've often noticed a bug
long after it was committed, or committed by mistake a
feature that wasn't finished yet.

Using branches, or making different versions of the project, lets you
develop a feature and merge it once it's tested, reviewed,
and properly finished.

But don't create branches randomly: think about a suitable model that
matches the way you release new versions of your
application.

A simple and well-known model is git flow, which includes the
master branch, the stable version of your project, a development branch, where
the latest features are merged, feature branches
for big features, and a few other branches that
you can discover here:
<https://www.occitech.fr/blog/2014/12/un-modele-de-branches-git-efficace/> (in French).

This model doesn't allow several stable versions of the project
(there is only master); if you want to maintain several
versions, as Symfony does for example with 2.7, 2.8, 3.0, ...
then you'll have to choose another model with the other
contributors, and clearly communicate the branching model you
chose.

### Use Pull Requests

Using a branch to create a new feature is a
good practice. You'll be able to merge it once it's finished.

But instead of merging your branch right away and *imposing* your
changes, rather choose to *propose* your changes by
creating a pull request, especially if it's not your project and
you're contributing to someone else's.

A tool like Github or Gitlab lists pull requests, lets you
comment on them, or on a specific line of code, update the
pull request, and merge it after taking into account feedback from other
contributors.

This lets other contributors review the code,
see what you've built, get your code and run it on their
own machine.

Another good practice is to never merge your own
code, and to always let at least one other person review and
merge it. This practice is inspired by extreme programming,
and works quite well with a tool like Github or Gitlab.

## Showcase continuous integration tools

You have now set up your project: it's online, it has
documentation, a coding standard, unit tests and integration
tests.

There are tools you can integrate into
your project's environment. The tools I'll present here
are free and suited to open source projects. They automate
running unit and integration tests, check compliance with
the coding standard, or inspect code quality and report
some potential bugs.

### Travis

Travis is a very well-known integration tool. It is linked to Github, and
runs a script, or “job”, after a push on a branch of the
project, or even when a pull request is created.

So you can run unit tests, integration tests, or
even a job that checks the coding standard has been followed.

Thanks to its Github integration, Travis then sends the build status
(no broken test, correct code style), and Github directly displays
a green check or a red cross in the pull request depending on
the status.

So it's a free tool for open source projects that checks,
on every contribution, that the modified code doesn't break anything and that the
project can still be installed.

### Scrutinizer

Scrutinizer is a continuous quality tool. It inspects the source
code, evaluates its complexity, detects potential bugs,
duplication, syntax errors… And outputs a score out of 10, along
with a list of recommendations to improve this
score.

However, to me it's not a bible, and the score is just a
landmark. This tool shows whether a code change may
introduce a bug or contains functions that are too
complex.

So this tool lets us follow how code quality evolves,
by knowing the impact of each PR on the score, and whether it introduces
issues.

You can even get emails when a commit makes the score drop, with
the author of that commit...

### SensioLabsInsight

SensioLabs also offers a code inspection tool, but this one
is Symfony-oriented. It means that, on top of the
PHP recommendations, it suggests good practices for
Symfony and Silex projects, or even for a Symfony bundle.

### Badges

If you use tools like the ones above, note that they
also provide badges. These are small dynamic images,
tied to the result of the build or the inspection, that you can
add to your project's Readme. The badges then show in
real time whether the project build is broken, whether tests still
pass, the code quality…

Badges also show that you care about code quality,
and make sure contributions don't cause regressions.

![Various badges on a PHP project README.](badges.png "Various badges on a PHP project README.")

## Summary

You've seen in this article that an open source project is not
just an open repository. It's also maintaining the code, reviewing the
code proposals and feedback from the community, having
documentation, a readme...

There is an organization, [The PHP
League](https://thephpleague.com/), which created a skeleton for a
PHP library. It's a good project base containing several
files usually found in a PHP project. It's
available on Github:
[thephpleague/skeleton](https://github.com/thephpleague/skeleton).

### Going further

You can read one of Richard Stallman's articles, “Free
Software Is Even More Important Now”:
<https://www.gnu.org/philosophy/free-software-even-more-important.html>,
and then browse the website and the FAQ, which detail
many free software concepts.

To see how things currently go inside an open source
project, you can watch the talk by Jordi Boggiano, creator of
composer and packagist, about what goes on behind an open source project,
“Behind the Scenes of Maintaining an Open Source Project”:
<https://www.youtube.com/watch?v=hRZhYSiSfaY>


{{< ccby >}}
