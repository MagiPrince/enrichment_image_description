# Enrichment_image_description

Réalisé par David Nogueiras Blanco et Jean-Marc Boutay.

## Description

Il s'agit d'un projet pour le cours Knowledge organisation system de l'Université de Genève.  
Ce projet a pour but de permettre d'inférer de nouveaux tags à une image trouvée sur Flickr, à l'aide des tags déjà présents sur l'image et des coordonnées géographiques de l'image.  
Il suffit d'indiquer l'identifiant de l'image pour obtenir les informations des tags et des coordonnées géographiques de l'image. Ensuite il est possible d'inférer directement de nouveaux tags à partir des tags existants, ainsi que d'en ajouter et d'en supprimer manuellement.  
Ce système se base sur différentes races de chiens, il est donc nécessaire de choisir des images de chiens pour que des tags soient inférés.  

## Comment lancer le projet

Dans un premier temps il faut vous assurer d'avoir toutes les librairies nécessaires pour le lancement (et de préférence la même version afin d'éviter tout problème de compatibilité).
Pour ce faire vous trouverez le fichier ```requirements.txt``` qui contient toutes les références. La bonne pratique est de le lancer depuis un environnement python virtuel avec ```pip3 install -r requirement.txt```.

Lorsque cela est fait, il est nécessaire de vous rendre dans le repertoire : ```enrichment_image_description/enrichment_image_description```, vous y trouverez le fichier ```local_settings_example.py``` qu'il vous faudra renommé en ```local_settings.py``` et dans lequel vous indiquerez vos identifiants pour utiliser l'api flickr.

Lorsque cela est fait assurez-vous que GraphDB tourne et modifiez dans le fichier ```enrichment_image_description/enrichment_image_description_app/sparql_requests.py``` la variable ```sparql_url_endpoint``` pour que celle-ci corresponde avec l'url de votre "endpoint".

Normalement tout devrait fonctionner !
