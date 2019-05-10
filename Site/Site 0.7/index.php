<!DOCTYPE html>
<html lang="en">

<head>

  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
  <meta name="description" content="">
  <meta name="author" content="">

  <title>SFL8 - Yokoko</title>

  <!-- Bootstrap Core CSS -->
  <link href="vendor/bootstrap/css/bootstrap.min.css" rel="stylesheet">

  <!-- Custom Fonts -->
  <link href="vendor/fontawesome-free/css/all.min.css" rel="stylesheet" type="text/css">
  <link href="https://fonts.googleapis.com/css?family=Source+Sans+Pro:300,400,700,300italic,400italic,700italic" rel="stylesheet" type="text/css">
  <link href="vendor/simple-line-icons/css/simple-line-icons.css" rel="stylesheet">

  <!-- Custom CSS -->
  <link href="css/stylish-portfolio.min.css" rel="stylesheet">

    <!-- The line below is only needed for old environments like Internet Explorer and Android 4.x -->
    <link rel="stylesheet" href="https://openlayers.org/en/v4.6.5/css/ol.css" type="text/css">
    <script src="https://cdn.polyfill.io/v2/polyfill.min.js?features=requestAnimationFrame,Element.prototype.classList,URL"></script>
    <script src="https://openlayers.org/en/v4.6.5/build/ol.js"></script>
	<script src="http://code.jquery.com/jquery-1.11.0.min.js"></script>
	<!-- The line below is only needed for old environments like Internet Explorer and Android 4.x -->
	<?php
    require ("connexion.php");
  ?>
</head>

<body id="page-top">

  <!-- Navigation -->
  <a class="menu-toggle rounded" href="#">
    <i class="fas fa-bars"></i>
  </a>
  <nav id="sidebar-wrapper">
    <ul class="sidebar-nav">
      <li class="sidebar-brand">
        <a class="js-scroll-trigger" href="#page-top">Yokoko</a>
      </li>
      <li class="sidebar-nav-item">
        <a class="js-scroll-trigger" href="#page-top">Accueil</a>
      </li>
      <li class="sidebar-nav-item">
        <a class="js-scroll-trigger" href="#about">projet</a>
      </li>
      <li class="sidebar-nav-item">
        <a class="js-scroll-trigger" href="#services">Services</a>
      </li>
      <li class="sidebar-nav-item">
        <a class="js-scroll-trigger" href="#portfolio">Tâches</a>
      </li>
      <li class="sidebar-nav-item">
        <a class="js-scroll-trigger" href="#contact">Final</a>
      </li>
    </ul>
  </nav>

  <!-- Header -->
  <header class="masthead d-flex">
    <div class="container text-center my-auto">
      <h1 class="mb-1">SFL8 - Yokoko</h1>
      <h3 class="mb-5">
        <em>Le projet Sfl8 permet une prise de</br>conscience de la qualité de la route et de l'environnement.</em>
      </h3>
      <a class="btn btn-primary btn-xl js-scroll-trigger" href="#about">En savoir plus</a>
    </div>
    <div class="overlay"></div>
  </header>

  <!-- A propos -->
  <section class="content-section bg-light" id="about">
    <div class="container text-center">
      <div class="row">
        <div class="col-lg-10 mx-auto">
          <h2>Le projet</h2>
          <p class="lead mb-5">le projet est constitué ............</p>
          <a class="btn btn-dark btn-xl js-scroll-trigger" href="#services">Tâches</a>
        </div>
      </div>
    </div>
  </section>

  <!-- Services -->
  <section class="content-section bg-primary text-white text-center" id="services">
    <div class="container">
      <div class="content-section-heading">
        <h3 class="text-secondary mb-0">Services</h3>
        <h2 class="mb-5">Tous les services disponibles</h2>
      </div>
      <div class="row">
        <div class="col-lg-3 col-md-6 mb-5 mb-lg-0">
          <span class="service-icon rounded-circle mx-auto mb-3">
            <i class="icon-power"></i>
          </span>
          <h4>
            <strong>Systèmes embarqués</strong>
          </h4>
          <p class="text-faded mb-0">Un système embarquant tous les capteurs.</p>
        </div>
        <div class="col-lg-3 col-md-6 mb-5 mb-lg-0">
          <span class="service-icon rounded-circle mx-auto mb-3">
            <i class="icon-rocket"></i>
          </span>
          <h4>
            <strong>Base de données</strong>
          </h4>
          <p class="text-faded mb-0">Une base de données actualiser toutes les 5 minutes.</p>
        </div>
        <div class="col-lg-3 col-md-6 mb-5 mb-md-0">
          <span class="service-icon rounded-circle mx-auto mb-3">
            <i class="icon-map"></i>
          </span>
          <h4>
            <strong>Cartographie</strong>
          </h4>
          <p class="text-faded mb-0">Une map sous openlayers dynamique et fluide !</p>
        </div>
        <div class="col-lg-3 col-md-6">
          <span class="service-icon rounded-circle mx-auto mb-3">
            <i class="icon-screen-desktop"></i>
          </span>
          <h4>
            <strong>Site web</strong>
          </h4>
          <p class="text-faded mb-0">Un site web design et responsive !</p>
        </div>
      </div>
    </div>
  </section>

  <!-- Callout -->
  <section class="callout">
    <div class="container text-center">
      <h2 class="mx-auto mb-5">Bienvenue dans
        <em>notre</em>
        projet!</h2>
      <a class="btn btn-primary btn-xl" href="https://startbootstrap.com/template-overviews/stylish-portfolio/">Download Now!</a>
    </div>
  </section>

  <!-- Portfolio -->
  <section class="content-section" id="portfolio">
    <div class="container">
      <div class="content-section-heading text-center">
        <h3 class="text-secondary mb-0">TÂCHES</h3>
        <h2 class="mb-5">Les différentes tâches</h2>
      </div>
      <div class="row no-gutters">
        <div class="col-lg-6">
          <a class="portfolio-item" href="#">
            <span class="caption">
              <span class="caption-content">
                <h2>Communes</h2>
                <p class="mb-0">A yellow pencil with envelopes on a clean, blue backdrop!</p>
              </span>
            </span>
            <img class="img-fluid" src="img/portfolio-1.jpg" alt="">
          </a>
        </div>
        <div class="col-lg-6">
          <a class="portfolio-item" href="#">
            <span class="caption">
              <span class="caption-content">
                <h2>Romain</h2>
                <p class="mb-0">A dark blue background with a colored pencil, a clip, and a tiny ice cream cone!</p>
              </span>
            </span>
            <img class="img-fluid" src="img/portfolio-2.jpg" alt="">
          </a>
        </div>
        <div class="col-lg-6">
          <a class="portfolio-item" href="#">
            <span class="caption">
              <span class="caption-content">
                <h2>Djessy</h2>
                <p class="mb-0">Strawberries are such a tasty snack, especially with a little sugar on top!</p>
              </span>
            </span>
            <img class="img-fluid" src="img/portfolio-3.jpg" alt="">
          </a>
        </div>
        <div class="col-lg-6">
          <a class="portfolio-item" href="#">
            <span class="caption">
              <span class="caption-content">
                <h2>Sylvain</h2>
                <p class="mb-0">A yellow workspace with some scissors, pencils, and other objects.</p>
              </span>
            </span>
            <img class="img-fluid" src="img/portfolio-4.jpg" alt="">
          </a>
        </div>
      </div>
    </div>
  </section>

  <!-- Map -->
  <section id="contact" class="map">
		<div id="map" class="map"><div id="popup"></div></div>
  </section>

  <!-- Footer -->
  <footer class="footer text-center">
    <div class="container">
      <ul class="list-inline mb-5">
        <li class="list-inline-item">
          <a class="social-link rounded-circle text-white mr-3" href="#">
            <i class="icon-social-facebook"></i>
          </a>
        </li>
        <li class="list-inline-item">
          <a class="social-link rounded-circle text-white" href="https://github.com/Syldup/SFL8_MOBILITE-ECORESPONSABLE" onclick="window.open(this.href); return false;">
            <i class="icon-social-github"></i>
          </a>
        </li>
      </ul>
      <p class="text-muted small mb-0">Copyright &copy; Yokoko 2019</p>
    </div>
  </footer>

  <!-- Scroll to Top Button-->
  <a class="scroll-to-top rounded js-scroll-trigger" href="#page-top">
    <i class="fas fa-angle-up"></i>
  </a>

  <!-- Bootstrap core JavaScript -->
  <script src="vendor/jquery/jquery.min.js"></script>
  <script src="vendor/bootstrap/js/bootstrap.bundle.min.js"></script>

  <!-- Plugin JavaScript -->
  <script src="vendor/jquery-easing/jquery.easing.min.js"></script>

  <!-- Custom scripts for this template -->
  <script src="js/stylish-portfolio.min.js"></script>

  <script src="script.js" type="text/javascript" language="javascript" charset="utf-8"></script>
  <script>
    var transform = ol.proj.getTransform('EPSG:4326', 'EPSG:3857');
    <?php
      $anomalies = $bdd->query('SELECT a.type, gps.x, gps.y, gps.time
                                FROM anomalie a
                                INNER JOIN gps
                                ON a.idGps = gps.id');
      $releves = $bdd->query('SELECT r.co2, r.pollution, gps.x, gps.y, gps.time
                              FROM releve r
                              INNER JOIN gps
                              ON r.idGps = gps.id');
      while ($donnees = $anomalies->fetch())
        {
          ?>
             var geom = new ol.geom.Point(transform([<?= $donnees['y'].", ".$donnees['x'] ?>]));
             var feature = new ol.Feature(geom);

             var msg = "<?= "<strong>Anomalie<br/>Type</strong> = ".$donnees['type']."<br/><strong>Date</strong> = ".$donnees['time'] ?>";
             feature.set("msg", msg);
             feature.setStyle(styles['a']);
             vectorSource.addFeature(feature);
             <?php
        }
        $anomalies->closeCursor();

        while ($donnees = $releves->fetch())
        {
          ?>
             var geom = new ol.geom.Point(transform([<?= $donnees['y'].", ".$donnees['x'] ?>]));
             var feature = new ol.Feature(geom);
             var msg = "<?= "<strong>Qualitée de l'air<br/>CO2</strong> =".$donnees['co2']."<br/><strong>Pollution</strong> =".$donnees['pollution']."<br/><strong>Il y a </strong>".$donnees['time'] ?>";
             feature.set("msg", msg);
             feature.setStyle(styles['b']);

             vectorSource.addFeature(feature);
            <?php

        }

      $releves->closeCursor(); // Termine le traitement de la requête
      ?>
    </script>



</body>

</html>
