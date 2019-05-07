-- phpMyAdmin SQL Dump
-- version 4.6.4
-- https://www.phpmyadmin.net/
--
-- Client :  127.0.0.1
-- Généré le :  Mar 30 Avril 2019 à 07:44
-- Version du serveur :  5.7.14
-- Version de PHP :  5.6.25

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données :  `sfl8_bdd`
--

-- --------------------------------------------------------

--
-- Structure de la table `anomalie`
--

CREATE TABLE `anomalie` (
  `id` int(11) NOT NULL,
  `type` enum('DECHET','DEFAUT') DEFAULT NULL,
  `idGps` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Contenu de la table `anomalie`
--

INSERT INTO `anomalie` (`id`, `type`, `idGps`) VALUES
(1, 'DECHET', 1);

-- --------------------------------------------------------

--
-- Structure de la table `gps`
--

CREATE TABLE `gps` (
  `id` int(11) NOT NULL,
  `x` float DEFAULT NULL,
  `y` float DEFAULT NULL,
  `time` datetime DEFAULT NULL,
  `idTrajet` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Contenu de la table `gps`
--

INSERT INTO `gps` (`id`, `x`, `y`, `time`, `idTrajet`) VALUES
(1, 47.215, -1.56343, '2019-03-22 08:21:18', 1),
(2, 47.211, -1.56343, '2019-03-22 08:45:18', 1),
(4, 47.2451, -1.55942, '2019-03-22 08:37:18', 1),
(5, 47.2325, -1.55942, '2019-03-22 08:19:18', 1),
(7, 47.2325, -1.55942, '2019-03-22 08:41:18', 1);

-- --------------------------------------------------------

--
-- Structure de la table `releve`
--

CREATE TABLE `releve` (
  `id` int(11) NOT NULL,
  `pollution` float DEFAULT NULL,
  `co2` float DEFAULT NULL,
  `idGps` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Contenu de la table `releve`
--

INSERT INTO `releve` (`id`, `pollution`, `co2`, `idGps`) VALUES
(1, 150, 6000, 1);

-- --------------------------------------------------------

--
-- Structure de la table `session`
--

CREATE TABLE `session` (
  `idSession` int(11) NOT NULL,
  `Identifiant` varchar(45) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Contenu de la table `session`
--

INSERT INTO `session` (`idSession`, `Identifiant`) VALUES
(0, 'djessy');

-- --------------------------------------------------------

--
-- Structure de la table `trajet`
--

CREATE TABLE `trajet` (
  `id` int(11) NOT NULL,
  `date` date DEFAULT NULL,
  `nom` varchar(65) DEFAULT NULL,
  `idSession` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Contenu de la table `trajet`
--

INSERT INTO `trajet` (`id`, `date`, `nom`, `idSession`) VALUES
(1, '2019-03-15', 'promenade', 0);

--
-- Index pour les tables exportées
--

--
-- Index pour la table `anomalie`
--
ALTER TABLE `anomalie`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idGps_idx` (`idGps`);

--
-- Index pour la table `gps`
--
ALTER TABLE `gps`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idTrajet_idx` (`idTrajet`);

--
-- Index pour la table `releve`
--
ALTER TABLE `releve`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idGps_idx` (`idGps`);

--
-- Index pour la table `session`
--
ALTER TABLE `session`
  ADD PRIMARY KEY (`idSession`);

--
-- Index pour la table `trajet`
--
ALTER TABLE `trajet`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idSession_idx` (`idSession`);

--
-- AUTO_INCREMENT pour les tables exportées
--

--
-- AUTO_INCREMENT pour la table `anomalie`
--
ALTER TABLE `anomalie`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;
--
-- AUTO_INCREMENT pour la table `gps`
--
ALTER TABLE `gps`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;
--
-- AUTO_INCREMENT pour la table `releve`
--
ALTER TABLE `releve`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;
--
-- AUTO_INCREMENT pour la table `trajet`
--
ALTER TABLE `trajet`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;
--
-- Contraintes pour les tables exportées
--

--
-- Contraintes pour la table `anomalie`
--
ALTER TABLE `anomalie`
  ADD CONSTRAINT `idGps_anomalie` FOREIGN KEY (`idGps`) REFERENCES `gps` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- Contraintes pour la table `gps`
--
ALTER TABLE `gps`
  ADD CONSTRAINT `idTrajet` FOREIGN KEY (`idTrajet`) REFERENCES `trajet` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- Contraintes pour la table `releve`
--
ALTER TABLE `releve`
  ADD CONSTRAINT `idGps_releve` FOREIGN KEY (`idGps`) REFERENCES `gps` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- Contraintes pour la table `trajet`
--
ALTER TABLE `trajet`
  ADD CONSTRAINT `idSession` FOREIGN KEY (`idSession`) REFERENCES `session` (`idSession`) ON DELETE NO ACTION ON UPDATE NO ACTION;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
