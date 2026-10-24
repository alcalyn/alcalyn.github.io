---
title: Php Neural Network
date: '2017-06-01'
aliases:
- /../projects/2017-06-01-php-neural-network/
summary: Number recognition neural network.
featuredImage: /images/projects/php-neural-network/php-neural-network.png
project: true
tags:
- php
---

TLDR: [See project here !](https://github.com/alcalyn/number-recognition-neural-network)

I decided to implement a neural network (multilayer perceptron)
from scratch, and using PHP.

That was a fun project where I then used this neural network
to recognize hand written numbers.

The artificial intelligence reached a 97% success rate
on learning samples, and 95% on learning samples it never met before.

I developed the interface to write number and send it
to the neural network. I tested it, and unfortunately
it works not as good as I though. It is because
numbers we write on the interface generate images
with a number that does not looks like the samples:

 - the pencil is thiner and "harder" than the samples
 - the written number is not as centered as is samples

But it recognize most of numbers we write after 10 minutes of learning.

📖 [Interface to write numbers and recognize them](https://github.com/alcalyn/number-recognition-neural-network)

📖 [PHP neural network you can reuse](https://github.com/alcalyn/neural-network)


{{< ccby >}}
