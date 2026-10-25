+++
date = '2026-10-25T20:08:16+01:00'
draft = true
title = "Création de l'éditeur de puzzle pour le jeu de Hex"
series = 'playhex'
+++

## Introduction

C'est quoi un puzzle de hex, parler des 500 puzzles de Matthew Seymour, montrer un exemple.

Je veux permettre à la communauté de créer leurs propres puzzles et les publier. Il faut donc créer un éditeur du puzzle.

## Première version

Mes objectifs :
- pouvoir créer un puzzle sur une vraie partie, comme il peut y avoir des puzzles sur une position d'échec.

Simple, un puzzle c'est "juste" un arbre de décision.

Sortie de la première version des puzzles et de l'éditeur : `9c226da0` (2 oct.)
    - Jouer un puzzle, éditeur de puzzle, créer un puzzle depuis une vraie partie (depuis Hexplorer)
    - Modèle : un arbre de décision (position initiale, coups du joueur / réponse de l'ordinateur, `result`, messages)
    - Une seule réponse de l'ordinateur par coup du joueur (les autres enfants sont ignorés)
    - Continuation après la fin du puzzle
    - Nœud "else" : réponse de l'ordinateur à n'importe quel autre coup

## Problème : trop de coups forcés possible

Du fait qu'un puzzle puisse être un plateau entier.

Même une position très linéaire, avec peu de choix, il est possible de jouer beaucoup de coups forcés en dehors, menacer de couper une connection virtuelle, gagnant mais qui n'apporte rien à la position.

### Cases désactivées pour isoler le puzzle

Solution : `cd530c50` (5 oct.)

Permettre de "griser", désactiver des régions pour isoler le problème.

On ne peut plus cliquer dans les regions qui sont connectée.

Afficher https://playhex.org/puzzles/5906f6ed-3f25-4038-a289-b4613fa2815f

## Collections

`a3e78f4f` (5 oct.)

Afficher un exemple https://playhex.org/puzzles/collections/03c068c7-22e5-405d-954b-33678d45be41

Regrouper les puzzles dans un "dossier", pour les ranger.

Pas grand chose, mais permet notamment de réorganiser l'ordre des puzzles de la collection,
et passer au "puzzle suivant" quand on a résolu un puzzle.

## Problème : on peut jouer de nombreux coups dans un ordre différent

Plusieurs ordres de coups qui finissent sur une même position.

On doit pouvoir faire "converger" les lignes et continuer l'arbre sur une seule de ces lignes.

### Transpositions

`995bae6d` (5 oct.)

Détection des transpositions, quand une même position, peu importe l'ordre des coups joués,
existe déjà dans l'arbre.

Les coups sont triés par ordre alphabétique et indéxés.

Si on trouve une transposition, on "rejoint" et continue sur la même branche.

## Problème : un coup forcé qui peut être joué n'importe quand fait dupliquer les branches

Montrer un exemple avec un pont

### Solution

Séquence parallèle.

Attention à ce que les coups de la séquence parallèle ne soient pas ailleur dans l'arbre,
pour éviter d'être bloqué.

Différence avec les transpositions : même avec une transposition, on aurait autant de branches que la séquence initiale, ca ferait un triangle.

Idée future : on s'en sert souvent pour un pont, mais de manière générale, ca peut permettre "d'automatiser" un template. Permettre de rendre une partie du puzzle indépendant, identifier un template et automatiser sa défense.

## Modération

Les puzzles permettent aux éditeur d'ajouter un message libre : surveiller, modération.

`f135314e` (6 oct.)

## Problème : l'UI devient vite complexe

Ajout d'un mode expert.

Un nouvel éditeur ne doit pas être submergé de fonctionnalité, et va probablement créer un puzzle simple.

L'UI ne doit pas le noyer : on retire le plus gros des features avancées, et on permet de les rajouter avec un switch, en affichant une aide pour chaque feature.

Afficher popin mode expert.

9. **Éval Katahex dans l'éditeur** : `5cd64525` (7 oct.)
    - Voir si on a oublié une ligne probable
    - `1b16b1ac` (7 oct.) : limite, Katahex MCTS ne marche pas sur les plateaux de 4x4 ou moins

10. **Vérifier un puzzle avec Katahex** : `9639a1c5` (8 oct.)
    - Vérification côté serveur, cache des analyses de position, commande `validatePuzzle`
    - `a4591430` (8 oct.) : bug, enfants des séquences parallèles comptés comme vrais enfants

11. **Puzzles dans le tutoriel / onboarding** : `587cb173` (8 oct.)
    - Les puzzles du tutoriel réutilisent le format `PuzzleDefinition`

12. **Solveur MoHex** : `bb02f5fd` (9 oct.)
    - Katahex estime, MoHex prouve : pourquoi avoir les deux
    - Cache des résolutions (Redis ou mémoire), validation des résultats des workers

13. **Plateaux partiels** (13 oct.)
    - `5d783175` : dans pixi-board, masque de cases, recadrage du plateau (`boardFit`), tests visuels
    - `6a114f74` : dans les puzzles, cacher les cases désactivées pour n'afficher qu'un coin du plateau

14. **Afficher `*` sur les cases couvertes par "else"** : `75de2f43` (13 oct.)

15. **Variantes "Et qu'auriez-vous joué en e9 ?"** : `5ab5de89` (14 oct.)
    - L'ordinateur joue en premier (`computerPlaysFirst`)
    - Alternatives : plusieurs réponses possibles de l'ordinateur. La première est jouée, les autres sont rejouées une fois la ligne résolue, et le joueur doit aussi les résoudre
    - Adapter les vérificateurs Katahex et MoHex, et les puzzles du tutoriel
    - `2eb5a656` (16 oct.) : afficher le nombre de variantes dans l'éditeur

16. **Faciliter la création** (15 oct.)
    - `c74f2c02` : importer n'importe quelle partie de Hex comme position initiale
    - `9bc2f173` : cloner un puzzle

17. **Connexions au bord à travers les cases désactivées** (22 oct.)
    - Problème : un plateau partiel ou isolé perd l'information "cette pierre est déjà connectée à son bord"
    - `a9d7b617` : nouvelle marque flèche dans pixi-board
    - `c2fd05ba` : remplissage des cases désactivées pour que MoHex résolve la bonne position, prévisualisation du remplissage
    - Pas encore commité : travail en cours

18. **Bilan / suite**
