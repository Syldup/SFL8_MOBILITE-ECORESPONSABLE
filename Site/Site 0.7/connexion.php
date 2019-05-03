<?php
try
{
	$bdd = new PDO('mysql:host=db5000063389.hosting-data.io;dbname=dbs58127;charset=utf8', 'dbu192881', '@SLF8_system');
}
catch (Exception $e)
{
        die('Erreur : ' . $e->getMessage());
}
?>
