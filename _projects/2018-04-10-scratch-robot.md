---
tags:
    - php
    - raspberry-pi
excerpt: "Control a robot with scratch blocks language."
header:
    teaser: /assets/images/scratch-robot/fond.jpg
    overlay_image: /assets/images/scratch-robot/fond.jpg
    overlay_filter: rgba(0, 0, 0, 0.25)
---

TLDR, see it in action:

<video width="640" height="360" controls>
    <source src="{{ "/assets/images/scratch-robot/scratch-robot-720.mp4" | absolute_url }}" type="video/mp4">
    <source src="{{ "/assets/images/scratch-robot/scratch-robot-720.webm" | absolute_url }}" type="video/webm">
    Your browser seems to not support video html5 tag.
</video>

{% include fa icon="book" classes="fa-lg" %} [Scratch Robot on Github](https://github.com/alcalyn/scratch-robot).

The goal of this proof of concept was
to play with [blockly](https://developers.google.com/blockly/).

This library allows to let users create a program
using scratch language. This way, you don't need
to know any programming language, but plug logic blocks
together.

Blockly allows to define and program our own blocks.

For example, here is how I defined "forward" block:

``` js
Blockly.defineBlocksWithJsonArray([
  {
    "type": "move_forward",
    "message0": "avance",
    "previousStatement": null,
    "nextStatement": null,
    "colour": "%{BKY_PROCEDURES_HUE}",
    "tooltip": "%{BKY_ROBOT_FORWARD_TOOLTIP}"
  }
]);
```

{% include figure
    image_path="/assets/images/scratch-robot/forward-block.png"
    caption="Generated block"
    alt="Forward block"
%}

And here is how I program it:

``` js
Blockly.JavaScript['move_forward'] = function (block) {
  return 'Robot_forward();\n';
};
```

*It is a "generator", and you can also define one for python, php...*

I developed 3 blocks: "forward", "turn left/right", "wait N seconds".
Each block return generated Javascript that send and an order to the Raspberry Pi robot.

I also used [Js-Interpreter](https://github.com/NeilFraser/JS-Interpreter)
to not run all the generated Javascript directly,
but halt the generated Javascript, and wait the robot to move.

Finally, for the robot, I re-used an API I already worked on for another project:
[Darkmira/drop-robotapi](https://github.com/Darkmira/drop-robotapi).
The readme contains the wiring schema to mount your own robot.

{% include fa icon="book" classes="fa-lg" %} [Scratch Robot on Github](https://github.com/alcalyn/scratch-robot).


{% include ccby %}
