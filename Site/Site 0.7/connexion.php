<?php
	$hostname = "db5000063389.hosting-data.io";
	$user     = "dbu192881";
	$password = "@SLF8_system";
	$nom_base_donnees = "dbs58127";

$link = mysqli_connect($hostname, $user, $password, $nom_base_donnees);

if (!$link) {
    echo "Erreur : Impossible de se connecter à MySQL." . PHP_EOL;
    echo "Errno de débogage : " . mysqli_connect_errno() . PHP_EOL;
    echo "Erreur de débogage : " . mysqli_connect_error() . PHP_EOL;
    exit;
}

echo "Succès : Une connexion correcte à MySQL a été faite! La base de donnée my_db est génial." . PHP_EOL;
echo "Information d'hôte : " . mysqli_get_host_info($link) . PHP_EOL;

mysqli_close($link);
?>