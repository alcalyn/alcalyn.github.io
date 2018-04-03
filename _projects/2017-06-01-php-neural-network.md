---
tags:
    - php
excerpt: "Number recognition neural network."
header:
    teaser: /assets/images/projects/php-neural-network.png
    overlay_image: /assets/images/projects/php-neural-network.png
    overlay_filter: 0.25
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

{% include fa icon="book" classes="fa-lg" %} [Interface to write numbers and recognize them](https://github.com/alcalyn/number-recognition-neural-network)

{% include fa icon="book" classes="fa-lg" %} [PHP neural network you can reuse](https://github.com/alcalyn/neural-network)


{% include ccby %}
