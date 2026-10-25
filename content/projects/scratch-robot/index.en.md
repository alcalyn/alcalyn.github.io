+++
aliases = ['/../projects/2018-04-10-scratch-robot/']
date = '2018-04-10'
featuredImage = '/images/projects/scratch-robot/fond.jpg'
project = true
summary = 'Control a robot with scratch blocks language.'
tags = ['php', 'raspberry-pi']
title = 'Scratch Robot'
+++

TLDR, see it in action:

{{< video src="scratch-robot-720.mp4,scratch-robot-720.webm" >}}Your browser seems to not support video html5 tag.{{< /video >}}

📖 [Scratch Robot on Github](https://github.com/alcalyn/scratch-robot).

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

![Forward block](forward-block.png "Generated block")

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

📖 [Scratch Robot on Github](https://github.com/alcalyn/scratch-robot).


{{< ccby >}}
