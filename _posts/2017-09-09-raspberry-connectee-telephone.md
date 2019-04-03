---
title: Contrôlez votre Raspberry Pi depuis votre téléphone pour la rendre plus portable
locale: fr
excerpt: Vous utilisez déjà SSH pour contrôler votre Raspberry en ligne de commande. Mais si vous vous déplacez avec votre Raspberry ?
tags:
    - raspberry-pi

workflow-configure:
  - url: /assets/images/rpi-wifi-phone/a-configure-1.png
    image_path: /assets/images/rpi-wifi-phone/a-configure-1.png
    alt: "Capture d'écran Android point d'accès wi-fi"
    title: "Paramètres Android"
  - url: /assets/images/rpi-wifi-phone/a-configure-2.png
    image_path: /assets/images/rpi-wifi-phone/a-configure-2.png
    alt: "Capture d'écran Android point d'accès wi-fi"
    title: "Paramètres Android avancés"
  - url: /assets/images/rpi-wifi-phone/a-configure-3.png
    image_path: /assets/images/rpi-wifi-phone/a-configure-3.png
    alt: "Capture d'écran Android point d'accès wi-fi"
    title: "Partage réseau mobile"
  - url: /assets/images/rpi-wifi-phone/a-configure-4.png
    image_path: /assets/images/rpi-wifi-phone/a-configure-4.png
    alt: "Configuration point d'accès wi-fi"
    title: "Configuration point d'accès wi-fi"

workflow-connect:
  - url: /assets/images/rpi-wifi-phone/c-connect-1.png
    image_path: /assets/images/rpi-wifi-phone/c-connect-1.png
    alt: "La Raspberry Pi s'est connectée à notre téléphone"
    title: "La Raspberry Pi s'est connectée à notre téléphone"
  - url: /assets/images/rpi-wifi-phone/c-connect-2.png
    image_path: /assets/images/rpi-wifi-phone/c-connect-2.png
    alt: "Liste des clients connéctés à notre point d'accès wi-fi"
    title: "Liste des clients connéctés à notre point d'accès wi-fi"
  - url: /assets/images/rpi-wifi-phone/c-connect-3.png
    image_path: /assets/images/rpi-wifi-phone/c-connect-3.png
    alt: "Capture d'écran Android point d'accès wi-fi"
    title: "Adresse IP attribuée à la Raspberry par le téléphone"

workflow-console:
  - url: /assets/images/rpi-wifi-phone/d-console-1.png
    image_path: /assets/images/rpi-wifi-phone/d-console-1.png
    alt: "Capture d'écran Android ConnectBot Raspberry Pi"
    title: "Connexion à la Raspberry Pi avec ConnectBot"
  - url: /assets/images/rpi-wifi-phone/d-console-2.png
    image_path: /assets/images/rpi-wifi-phone/d-console-2.png
    alt: "Capture d'écran Android ConnectBot Raspberry Pi"
    title: "Saisir le mot de passe demandé par SSH"
  - url: /assets/images/rpi-wifi-phone/d-console-3.png
    image_path: /assets/images/rpi-wifi-phone/d-console-3.png
    alt: "Capture d'écran Android ConnectBot Raspberry Pi"
    title: "On a pris la main de notre Raspberry"
---

{% include toc title="Sommaire" %}

Vous utilisez déjà SSH pour contrôler votre Raspberry en ligne de commande.

Pour cela, vous la connectez en Ethernet directement à votre PC,
ou à distance en la connectant en wi-fi à votre box/router pour y accéder en réseau local.

Mais si vous vous déplacez avec votre Raspberry Pi car :

 - vous l'avez branchée à une batterie et vous voulez y accéder en voiture
 - vous l'avez embarquée dans un objet portable que vous emmenez hors de chez vous

vous n'aurez plus le réseau local de votre box, et vous n'allez pas garder
votre PC avec vous pour la brancher.

J'ai récemment embarqué ma Raspberry dans un objet physique
et voulu le transporter ailleurs que chez moi, en dehors de mon wi-fi.

Je vais expliquer dans cet article comment j'ai pu accéder
à la Raspberry en SSH dans cette condition.

Il vous faudra :

 - un bon riz
 - votre Raspberry
 - un téléphone qui fait point d'accès wi-fi
 - une application sur votre téléphone qui fait terminal, par exemple [ConnectBot](https://play.google.com/store/apps/details?id=org.connectbot&hl=fr).


## Le point d'accès wi-fi

Actuellement, beaucoup de téléphones font point d'accès Wifi, ou "hot-spot".
Habituellement, on se sert du point d'accès pour diffuser un accès à Internet
en l'utilisant en même temps que l'accès aux données mobiles.

En activant votre point d'accès wi-fi, votre téléphone devient une sorte de routeur,
et permet à d'autres téléphones de s'y connecter en wi-fi, comme à une box,
en connaissant le nom du réseau wi-fi, le SSID, et l'éventuel mot de passe.

Lorsqu'un téléphone se connecte à votre point d'accès,
votre téléphone va lui attribuer une adresse IP locale,
exactement comme le ferait votre box.
Le téléphone peut donc rejoindre le réseau local créé par votre téléphone hôte.

## Configurez votre point d'accès

Vous devez d'abord connaître ou définir le SSID du point d'accès wi-fi de votre téléphone.
Avec un système Android, il faut aller dans les paramètres, saisir un nom (ou garder celui déjà en place),
et configurer la sécurité, WPA ou aucun.

{% include
    gallery id="workflow-configure"
    caption="Manipulation pour activer son point d'accès wi-fi sur Android"
%}

> Je n'ai pas mis de mot de passe car j'en ai pas besoin :
> je n'activerai le point d'accès que ponctuellement.

Vous connaissez maintenant votre SSID et votre éventuel mot de passe.

Configurez maintenant votre Raspberry.

## Configurez votre Raspberry Pi

Vous avez donc mis votre téléphone en mode point d'accès wi-fi.

Ici, ce n'est pas pour offrir un accès Internet à d'autres personnes,
mais pour que votre Raspberry s'y connecte. Elle sera donc
dans le réseau local de votre téléphone, aura une adresse IP,
et vous pourrez y accéder depuis votre téléphone.

Le but sera de faire en sorte que votre Raspberry Pi s'y connecte toute seule,
et savoir quelle adresse IP votre téléphone lui a attribué pour s'y connecter en SSH
avec l'application qui fait terminal.

Vous avez peut-être déjà fait cette manipulation quand vous avez configuré
votre Raspberry pour qu'elle se connecte en wi-fi à votre box.

Il suffit, dans votre Raspberry, d'aller dans le fichier
`/etc/wpa_supplicant/wpa_supplicant.conf`,
et d'ajouter le SSID de votre téléphone :

``` bash
sudo nano /etc/wpa_supplicant/wpa_supplicant.conf
```

Ajoutez votre téléphone avec le bon SSID dans le fichier :

```
network={
	ssid="JUJU"
	proto=RSN
	key_mgmt=NONE
}
```

Si vous avez déjà un autre `network`, par exemple celui de votre box,
c'est pas grave. Ajoutez votre téléphone en dessous, et il faut ajouter un `id_str`
pour différencier les deux `network`. Cet `id_str` est nécessaire lorsqu'il
y en a plusieurs.

Voilà mon `wpa_supplicant.conf` complet :

```
country=GB
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1

network={
	ssid="MaBox"
	psk="xxxxxxxx"
	id_str="maison"
}

network={
	ssid="JUJU"
	proto=RSN
	key_mgmt=NONE
	id_str="telephone"
}
```

Ça devrait être bon. Maintenant :

- démarrez votre point d'accès wi-fi sur votre téléphone.
- faîtes en sorte que votre Raspberry ne se connecte pas au wi-fi de votre box à la place de votre téléphone.
- redémarrez votre Raspberry Pi.

> Pour empêcher votre Raspberry de se connecter à votre box, plusieurs options :
>
> - soit vous coupez le wi-fi de votre box (plus de wi-fi chez vous)
> - soit, dans le fichier `wpa_supplicant.conf` de votre Raspberry, vous renommez le SSID de votre box en le suffixant par exemple avec `_old` (il faura le remettre pour avoir à nouveau Internet sur la Raspberry)
> - soit vous sortez de votre couverture wi-fi (ah, là, il faudra marcher)

Attendez qu'elle se démarre et qu'elle s'y connecte.
Vous devrez voir votre Raspberry se connecter à votre point d'accès dans le menu :

{% include figure
    image_path="/assets/images/rpi-wifi-phone/c-connect-1.png"
    caption="La Raspberry vient de se connecter à notre point d'accès wi-fi"
    alt="Capture écran point d'accès wi-fi Android"
%}

## Connectez vous en SSH

Votre téléphone a dû attribuer une adresse IP à la Raspberry.
Vous en avez besoin pour s'y connecter.
Il est possible de la connaître en listant les périphériques connectés :

{% include
    gallery id="workflow-connect"
    caption="Connaître l'address IP attribué à la Raspberry par le téléphone"
%}

Ensuite, il n'y a plus qu'à s'y connecter avec l'application terminal
(ici [ConnectBot](https://play.google.com/store/apps/details?id=org.connectbot&hl=fr)),
en saisissant l'adresse IP que j'ai récupéré et le nom d'utilisateur SSH (par défaut `pi`).
Je saisis donc `pi@192.168.43.113` dans le champ `utilisateur@hôte port`,
je laisse les autres champs par défaut et je valide.

La Raspberry nous demande ensuite le mot de passe SSH,
par défaut `raspberry` si vous ne l'avez pas changé.

{% include
    gallery id="workflow-console"
    caption="Connexion SSH à la Raspberry Pi avec ConnectBot"
%}

Voilà, vous avez pris la main sur votre Raspberry Pi depuis votre téléphone.

## Aller plus loin

On se sert dans cet article de la connexion wi-fi pour juste se connecter en SSH,
mais on pourrait imaginer que la Raspberry héberge une application serveur,
par exemple un serveur web, et la faire marcher avec le téléphone avec un simple
navigateur web, ou une application qui se connecte à la Raspberry.

En embarquant la Raspberry dans un objet, on pourrait contrôler cet objet
depuis notre téléphone, lui envoyer des ordres, récupérer des données des capteurs
de la Raspberry.

### Et si la Raspberry fournissait le point d'accès

Au lieu de configurer votre Raspberry pour qu'elle se connecte à votre téléphone,
elle pourrait elle-même fournir le point d'accès.
Je n'ai pas réussi à le faire, mais en suivant cet article,
[Créer un hotspot Wi-Fi en moins de 10 minutes avec la Raspberry Pi](https://raspbian-france.fr/creer-un-hotspot-wi-fi-en-moins-de-10-minutes-avec-la-raspberry-pi/),
on pourrait se connecter à son objet connecté depuis son téléphone,
plutôt que l'inverse.

Cela serait plus simple d'un point de vue utilisateur,
et vous pourriez même avoir un SSID du nom de votre objet connecté.

Un premier pas vers la domotique...


{% include ccby %}
