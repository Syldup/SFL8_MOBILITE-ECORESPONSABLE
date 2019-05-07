<?php
$i=0; //Initialisation de la variable i

/*Ceci correspond à votre première base de donnée. Grâce à cette
méthode, vous pourrez aisément en ajouter, selon ce que vous avez
créé sur votre espace 1and1*/
$i++;
$cfg['Servers'][$i]['user']          = 'dbu192881'; // indiquez ici votre nom d'utilisateur (fourni par 1and1 dans la partie base de donnée)
$cfg['Servers'][$i]['password']      = '@SLF8_system'; //  ici votre mot de passe
$cfg['Servers'][$i]['host']          = 'db5000063389.hosting-data.io'; // Le serveur
$cfg['Servers'][$i]['pmadb']         = 'dbs58127'; // Et pour fini le nom de la base de donnée

?>