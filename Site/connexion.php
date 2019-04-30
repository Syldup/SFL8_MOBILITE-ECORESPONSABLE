<?php
  $host_name = 'db5000063389.hosting-data.io';
  $database = 'dbs58127';
  $user_name = 'dbu192881';
  $password = '@SLF8_system';
  $connect = mysql_connect($host_name, $user_name, $password, $database);

  if (mysql_errno()) {
    die('<p>La connexion au serveur MySQL a échoué: '.mysql_error().'</p>');
  } else {
    echo '<p>Connexion au serveur MySQL établie avec succès.</p >';
  }
?>