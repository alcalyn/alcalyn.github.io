+++
date = '2017-06-01'
featuredImage = '/images/projects/php-neural-network/php-neural-network.png'
project = true
summary = 'Réseau de neurones de reconnaissance de chiffres.'
tags = ['php']
title = 'Réseau de neurones en PHP'
+++

*Cet article a été traduit de l'anglais.*

TLDR : [Voir le projet ici !](https://github.com/alcalyn/number-recognition-neural-network)

J'ai décidé d'implémenter un réseau de neurones (perceptron multicouche)
à partir de zéro, et en PHP.

C'était un projet amusant, dans lequel j'ai ensuite utilisé ce réseau de neurones
pour reconnaître des chiffres écrits à la main.

L'intelligence artificielle a atteint un taux de réussite de 97 %
sur les échantillons d'apprentissage, et de 95 % sur des échantillons qu'elle n'avait jamais vus.

J'ai développé l'interface pour écrire un chiffre et l'envoyer
au réseau de neurones. Je l'ai testée, et malheureusement
elle ne fonctionne pas aussi bien que je le pensais. C'est parce que
les chiffres que l'on écrit dans l'interface génèrent des images
dont le chiffre ne ressemble pas aux échantillons :

 - le crayon est plus fin et plus « dur » que dans les échantillons
 - le chiffre écrit n'est pas aussi bien centré que dans les échantillons

Mais il reconnaît la plupart des chiffres qu'on écrit après 10 minutes d'apprentissage.

📖 [Interface pour écrire des chiffres et les reconnaître](https://github.com/alcalyn/number-recognition-neural-network)

📖 [Réseau de neurones PHP réutilisable](https://github.com/alcalyn/neural-network)


{{< ccby >}}
