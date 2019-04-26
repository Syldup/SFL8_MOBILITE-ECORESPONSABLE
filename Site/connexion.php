<?php
	// On définit les 4 variables nécessaires à la connexion MySQL :
	$hostname = "localhost";
	$port     = 3306;
	$user     = "user_mysql";
	$password = "password_mysql";
	$nom_base_donnees = "sfl8_bdd";


	// VIEILLE METHODE (sans PDO)
	// A ne plus utiliser normalement ...
	// compatible PHP <= 5.1
	//		$conn = mysql_connect($hostname, $user, $password) or die(mysql_error());

	//		// Choix de la base sur laquelle travailler
	//		mysql_select_db($nom_base_donnees, $conn);

	//		// pour ceux qui ont l'extension mysqli_* on peut remplacer tous les mysql_* par mysqli_*
	//



	// NOUVELLE METHODE (depuis PHP 5.1 et avec PDO)
	// depuis PHP 5.1 et a fortiori en PHP 7, on doit utiliser la classe "PDO" (PHP Data Object, un objet de connexion)
	// connexion au serveur MySQL avec PDO (la forme plus récente, et plus sécurisée : NOUVELLE METHODE
	try
	{
		$connexion = new PDO('mysql:host='.$hostname.';port='.$dbport.';dbname='.$nom_base_donnees, $user, $password,array(PDO::MYSQL_ATTR_INIT_COMMAND => "SET NAMES utf8"));
		$connexion->SetAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_WARNING);
	}
	catch(Exception $e)
	{
		echo 'Erreur : '.$e->getMessage().'<br />';
		echo 'N° : '.$e->getCode();
		exit();
	}

?>