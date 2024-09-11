-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Sep 11, 2024 at 05:25 AM
-- Server version: 8.0.30
-- PHP Version: 8.1.10

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `jes`
--

-- --------------------------------------------------------

--
-- Table structure for table `admin`
--

CREATE TABLE `admin` (
  `id_admin` int NOT NULL,
  `nombre_admin` varchar(40) CHARACTER SET utf8mb4 COLLATE utf8mb4_spanish2_ci NOT NULL,
  `a_apellido` varchar(40) CHARACTER SET utf8mb4 COLLATE utf8mb4_spanish2_ci NOT NULL,
  `a_email` varchar(140) CHARACTER SET utf8mb4 COLLATE utf8mb4_spanish2_ci NOT NULL,
  `a_genero` char(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_spanish2_ci NOT NULL,
  `a_direccion` text CHARACTER SET utf8mb4 COLLATE utf8mb4_spanish2_ci NOT NULL,
  `a_telefono` char(14) CHARACTER SET utf8mb4 COLLATE utf8mb4_spanish2_ci NOT NULL,
  `a_img_perfil` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_spanish2_ci NOT NULL,
  `matricula` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_spanish2_ci NOT NULL,
  `contraseña` varchar(40) CHARACTER SET utf8mb4 COLLATE utf8mb4_spanish2_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish2_ci;

--
-- Dumping data for table `admin`
--

INSERT INTO `admin` (`id_admin`, `nombre_admin`, `a_apellido`, `a_email`, `a_genero`, `a_direccion`, `a_telefono`, `a_img_perfil`, `matricula`, `contraseña`) VALUES
(1, 'Jhon Mike', 'Peña Ramos', 'jhonmip2@gmail.com', 'Masculino', 'Calle 16 de Agosto #01', '809-101-0000', 'static\\documentos\\boy5.jpg', 'a-0223', 'admin2330');

-- --------------------------------------------------------

--
-- Table structure for table `asignaturas`
--

CREATE TABLE `asignaturas` (
  `id_asignatura` int NOT NULL,
  `nom_asignatura` varchar(20) CHARACTER SET utf8mb3 COLLATE utf8mb3_spanish_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_spanish_ci;

--
-- Dumping data for table `asignaturas`
--

INSERT INTO `asignaturas` (`id_asignatura`, `nom_asignatura`) VALUES
(2401, 'Lengua Española'),
(2402, 'Matematicas'),
(2403, 'Ciencias Sociales'),
(2404, 'Ciencias Naturales'),
(2405, 'Ingles'),
(2406, 'Frances'),
(2407, 'Educacion Fisica'),
(2408, 'Arte '),
(2409, 'Formacion Humana'),
(2410, 'Informática'),
(2411, 'Robotica'),
(2412, 'Liderazgo'),
(2413, 'Biología'),
(2414, 'Física'),
(2415, 'Humanidades'),
(2416, 'Literatura');

-- --------------------------------------------------------

--
-- Table structure for table `asignatura_curso`
--

CREATE TABLE `asignatura_curso` (
  `id` int NOT NULL,
  `id_curso` int NOT NULL,
  `id_asignatura` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish2_ci;

-- --------------------------------------------------------

--
-- Table structure for table `asistencias`
--

CREATE TABLE `asistencias` (
  `id_asistencia` int NOT NULL,
  `id_estudiante` int NOT NULL,
  `id_curso` int NOT NULL,
  `id_asignatura` int NOT NULL,
  `Sect_Oct` char(4) CHARACTER SET utf8mb3 COLLATE utf8mb3_spanish_ci NOT NULL,
  `Nov_Dic` char(4) CHARACTER SET utf8mb3 COLLATE utf8mb3_spanish_ci NOT NULL,
  `Ene_Feb` char(4) CHARACTER SET utf8mb3 COLLATE utf8mb3_spanish_ci NOT NULL,
  `Marz_Abril` char(4) CHARACTER SET utf8mb3 COLLATE utf8mb3_spanish_ci NOT NULL,
  `May_Jun` char(4) CHARACTER SET utf8mb3 COLLATE utf8mb3_spanish_ci NOT NULL,
  `Total_de_asistencias` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_spanish_ci;

--
-- Dumping data for table `asistencias`
--

INSERT INTO `asistencias` (`id_asistencia`, `id_estudiante`, `id_curso`, `id_asignatura`, `Sect_Oct`, `Nov_Dic`, `Ene_Feb`, `Marz_Abril`, `May_Jun`, `Total_de_asistencias`) VALUES
(1, 2, 1, 2404, '90', '90', '90', '90', '90', 90),
(2, 2, 1, 2403, '90', '0', '0', '0', '0', 0),
(3, 2, 1, 2401, '100', '100', '100', '100', '100', 100),
(4, 4, 7, 2401, '100', '100', '100', '100', '100', 100);

-- --------------------------------------------------------

--
-- Table structure for table `calificaciones`
--

CREATE TABLE `calificaciones` (
  `id_calificacion` int NOT NULL,
  `id_estudiante` int NOT NULL,
  `id_curso` int NOT NULL,
  `id_asignatura` int NOT NULL,
  `C1` int NOT NULL,
  `C2` int NOT NULL,
  `C3` int NOT NULL,
  `C4` int NOT NULL,
  `c_final` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_spanish_ci;

--
-- Dumping data for table `calificaciones`
--

INSERT INTO `calificaciones` (`id_calificacion`, `id_estudiante`, `id_curso`, `id_asignatura`, `C1`, `C2`, `C3`, `C4`, `c_final`) VALUES
(4, 2, 1, 2401, 100, 100, 100, 100, 100),
(5, 3, 1, 2401, 100, 100, 100, 100, 100),
(6, 2, 1, 2405, 100, 100, 100, 100, 100),
(7, 4, 7, 2401, 90, 90, 90, 90, 90),
(8, 2, 1, 2404, 100, 90, 98, 97, 96);

-- --------------------------------------------------------

--
-- Table structure for table `cursos`
--

CREATE TABLE `cursos` (
  `id_curso` int NOT NULL,
  `nombre` varchar(30) CHARACTER SET utf8mb3 COLLATE utf8mb3_spanish_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_spanish_ci;

--
-- Dumping data for table `cursos`
--

INSERT INTO `cursos` (`id_curso`, `nombre`) VALUES
(1, '1ro A'),
(2, '2do A'),
(3, '3ro A'),
(4, '4to A'),
(5, '5to A'),
(6, '6to A'),
(7, '1ro B'),
(8, '2do B'),
(9, '3ro B'),
(10, '4to B'),
(11, '5to B'),
(12, '6to B');

-- --------------------------------------------------------

--
-- Table structure for table `dias`
--

CREATE TABLE `dias` (
  `id_dias` int NOT NULL,
  `dia` varchar(10) CHARACTER SET utf8mb3 COLLATE utf8mb3_spanish_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_spanish_ci;

--
-- Dumping data for table `dias`
--

INSERT INTO `dias` (`id_dias`, `dia`) VALUES
(100, 'Lunes'),
(101, 'Martes'),
(102, 'Miercoles'),
(103, 'Jueves'),
(104, 'Viernes');

-- --------------------------------------------------------

--
-- Table structure for table `estudiantes`
--

CREATE TABLE `estudiantes` (
  `id_estudiante` int NOT NULL,
  `id_curso` int NOT NULL,
  `matricula` char(10) CHARACTER SET utf8mb3 COLLATE utf8mb3_spanish_ci NOT NULL,
  `nombre` varchar(30) CHARACTER SET utf8mb3 COLLATE utf8mb3_spanish_ci NOT NULL,
  `apellidos` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_spanish_ci NOT NULL,
  `direccion` text CHARACTER SET utf8mb3 COLLATE utf8mb3_spanish_ci NOT NULL,
  `fecha_nacimiento` date NOT NULL,
  `genero` varchar(10) CHARACTER SET utf8mb3 COLLATE utf8mb3_spanish_ci NOT NULL,
  `email` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_spanish_ci NOT NULL,
  `telefono` char(12) CHARACTER SET utf8mb3 COLLATE utf8mb3_spanish_ci NOT NULL,
  `imagen_perfil` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_spanish_ci NOT NULL,
  `contraseña` varchar(30) CHARACTER SET utf8mb3 COLLATE utf8mb3_spanish_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_spanish_ci;

--
-- Dumping data for table `estudiantes`
--

INSERT INTO `estudiantes` (`id_estudiante`, `id_curso`, `matricula`, `nombre`, `apellidos`, `direccion`, `fecha_nacimiento`, `genero`, `email`, `telefono`, `imagen_perfil`, `contraseña`) VALUES
(2, 1, 'e-9990', 'Albiery', 'Rodriguez', 'calle 16 de agosto #1', '2010-10-19', 'Masculino', 'albieryr@gmail.com', '8494649924', 'static/documentos\\boy11.jpg', 'e123'),
(3, 1, 'e-2233', 'Laura', 'Cabrera Francisco', 'calle del sol #255', '2008-05-10', 'Femenino', 'lauracab@gmail.com', '809-962-1230', 'static/documentos\\girl14.jpg', 'lau222'),
(4, 7, 'e-2020', 'Juana', 'Ramirez pena', 'calle su casa detras de su casa #223', '2008-05-10', 'Femenino', 'juanitab@gmail.com', '809-889-9966', 'static/documentos\\girl20.jpg', 'juana122'),
(5, 2, 'e-1001', 'Massiel', 'Rodriguez', 'Calle 24 #58, La Herradura, Santiago', '2002-12-31', 'femenino', 'massielrodriguez990@gmail.com', '809-464-5458', 'static/documentos\\girl8.jpg', 'massiel990'),
(6, 2, 'e-1002', 'Jose Miguel', 'Bello Acosta', 'Castañuelas, Montecristi', '2003-09-04', 'masculino', 'josemiguelbello@gmail.com', '829-477-2269', 'static/documentos\\boy17.jpg', 'elbello90'),
(7, 3, 'e-1003', 'Milton Javier', 'Valerio', 'Santiago de los Caballeros', '2005-05-02', 'masculino', 'miltonpro01@gmail.com', '829-968-1952', 'static/documentos\\boy15.jpg', 'miltonesnoob'),
(8, 3, 'e-1004', 'Tiara', 'Peña', 'Santiago de los Caballeros', '2004-08-23', 'femenino', 'penatiara@gmail.com', '829-842-7894', 'static/documentos\\girl15.jpg', 'tiara123'),
(9, 4, 'e-1005', 'Smailyn', 'Burgos', 'Licey al medio, Santiago', '2003-12-12', 'femenino', 'smaburgos2003@gmail.com', '829-973-7188', 'static/documentos\\girl2.jpg', 'smailyn29'),
(10, 4, 'e-1006', 'Faury', 'Garcia Rodriguez', 'Calle 16 de Agosto #236, La Joya, Santiago', '2004-09-17', 'masculino', 'faury227@gmail.com', '809-297-8213', 'static/documentos\\boy2.jpg', 'faury1700'),
(11, 5, 'e-1007', 'Esmeralda', 'Estrella', 'Calle 67 #123, Villa Liberación, Santiago', '2006-12-12', 'femenino', 'starsh23@gmail.com', '829-959-7816', 'static/documentos\\girl13.jpg', 'esmeralda123'),
(12, 5, 'e-1008', 'Yohan', 'Perez', 'Calle 2 #4, La Otra Banda, Santiago', '2006-02-23', 'masculino', 'yohanpedra@gmail.com', '849-854-4639', 'static/documentos\\boy3.jpg', 'yohanelmejor'),
(13, 6, 'e-1009', 'Yerman', 'Espinal', 'Calle 34 #43, Navarrete, Santiago', '2006-07-23', 'masculino', 'yerman04@gmail.com', '849-861-7224', 'static/documentos\\boy8.jpg', 'yerman888'),
(14, 6, 'e-1100', 'Wilfry', 'Mendez', 'Calle principal #4, Villa Liberación, La Otra Banda, Santiago', '2004-09-13', 'masculino', 'bellako0023@gmail.com', '809-202-7990', 'static/documentos\\boy19.jpg', 'bellako23'),
(15, 7, 'e-1101', 'Steveen', 'Rodriguez', 'Calle 16 de Agosto #236, La Joya, Santiago', '2006-02-13', 'masculino', 'steveen23@gmail.com', '809-415-9924', 'static/documentos\\boy13.jpg', 'lagargola'),
(16, 7, 'e-1102', 'Alberto', 'Rodriguez', 'Calle 2 #23, La Otra Banda, Santiago', '2005-09-23', 'masculino', 'albertorodriguez@gmail.com', '829-631-1919', 'static/documentos\\boy12.jpg', 'alberto01'),
(17, 8, 'e-1103', 'Henry', 'Rodriguez', 'Calle 1 #8, La Otra Banda, Santiago', '2005-12-12', 'masculino', 'henryrod@gmail.com', '809-250-8308', 'static/documentos\\boy4.jpg', 'fariseo23'),
(18, 8, 'e-1104', 'Jeison', 'Ventura', 'Villa Olga, Santiago', '2006-05-23', 'masculino', 'jeirer44@gmail.com', '809-557-1523', 'static/documentos\\boy16.jpg', 'jeison2024'),
(19, 9, 'e-1105', 'Carla', 'Morales García', 'Calle Luna, 45, Madrid', '2005-02-10', 'femenino', 'carla.morales@gmail.com', '829-555-1234', 'static/documentos\\girl19.jpg', 'Carla2005!'),
(20, 9, 'e-1106', 'Javier', 'Rodríguez López', 'Avenida Sol, 12, Barcelona', '2006-08-15', 'masculino', 'javier.rodriguez@gmail.com', '809-555-5678', 'static/documentos\\boy7.jpg', 'Javi2023#'),
(21, 10, 'e-1107', 'Lucía', 'Fernández Ruiz', 'Calle Mar, 23, Valencia', '2007-11-22', 'femenino', 'lucia.fernandez@gmail.com', '849-555-8765', 'static/documentos\\girl5.jpg', 'Lucia@2007'),
(22, 10, 'e-1108', 'Miguel', 'Pérez Martínez', 'Plaza Mayor, 7, Sevilla', '2005-03-05', 'masculino', 'miguel.perez@gmail.com', '809-555-4321', 'static/documentos\\boy1.jpg', 'Miguel2005!'),
(23, 11, 'e-1109', 'Ana', 'Gómez Sánchez', 'Calle del Rey, 19, Bilbao', '2006-01-18', 'femenino', 'ana.gomez@gmail.com', '829-555-2345', 'static/documentos\\girl9.jpg', 'Ana2006@#'),
(24, 11, 'e-1110', 'Daniel', 'Martínez Ortega', 'Avenida del Norte, 34, Zaragoza', '2008-06-12', 'masculino', 'daniel.martinez01@gmail.com', '829-555-6789', 'static/documentos\\boy14.jpg', 'Dani2008!'),
(25, 12, 'e-1111', 'Valeria', 'Castillo Morales', 'Calle del Sol, 50, Granada', '2009-10-25', 'femenino', 'valeria.castillo21@gmail.com', '849-555-3456', 'static/documentos\\girl21.jpg', 'Vale2009@'),
(26, 12, 'e-1112', 'Roberto', 'Soto Fernández', 'Calle de la Luna, 3, Salamanca', '2005-04-30', 'masculino', 'roberto.soto888@gmail.com', '849-555-7890', 'static/documentos\\boy18.jpg', 'Rober2005!');

-- --------------------------------------------------------

--
-- Table structure for table `hora`
--

CREATE TABLE `hora` (
  `id_hora` int NOT NULL,
  `hora` varchar(12) CHARACTER SET utf8mb3 COLLATE utf8mb3_spanish_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_spanish_ci;

--
-- Dumping data for table `hora`
--

INSERT INTO `hora` (`id_hora`, `hora`) VALUES
(1, '7:30-8:30'),
(2, '8:30-9:30'),
(3, '9:30-10:00'),
(4, '10:00-11:00'),
(5, '11:00-12:00');

-- --------------------------------------------------------

--
-- Table structure for table `horario`
--

CREATE TABLE `horario` (
  `id_horario` int NOT NULL,
  `id_hora` int NOT NULL,
  `id_curso` int NOT NULL,
  `id_asignatura` int NOT NULL,
  `id_dias` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_spanish_ci;

--
-- Dumping data for table `horario`
--

INSERT INTO `horario` (`id_horario`, `id_hora`, `id_curso`, `id_asignatura`, `id_dias`) VALUES
(33, 1, 1, 2402, 100),
(34, 1, 1, 2403, 101),
(35, 1, 1, 2414, 102),
(36, 1, 1, 2401, 103),
(37, 1, 1, 2416, 104),
(38, 2, 1, 2401, 100),
(39, 2, 1, 2413, 101),
(40, 2, 1, 2408, 102),
(41, 2, 1, 2403, 103),
(42, 2, 1, 2413, 104),
(43, 3, 1, 2405, 100),
(44, 3, 1, 2411, 101),
(45, 3, 1, 2410, 102),
(46, 3, 1, 2402, 103),
(47, 3, 1, 2405, 104),
(48, 4, 1, 2404, 100),
(49, 4, 1, 2407, 101),
(50, 4, 1, 2406, 102),
(51, 4, 1, 2404, 103),
(52, 4, 1, 2410, 104),
(53, 5, 1, 2409, 100),
(54, 5, 1, 2416, 101),
(55, 5, 1, 2415, 102),
(56, 5, 1, 2412, 103),
(57, 5, 1, 2411, 104),
(83, 1, 2, 2403, 100),
(84, 1, 2, 2401, 101),
(85, 1, 2, 2407, 102),
(86, 1, 2, 2401, 103),
(87, 1, 2, 2413, 104),
(88, 2, 2, 2405, 100),
(89, 2, 2, 2414, 101),
(90, 2, 2, 2413, 102),
(91, 2, 2, 2402, 103),
(92, 2, 2, 2411, 104),
(93, 3, 2, 2402, 100),
(94, 3, 2, 2410, 101),
(95, 3, 2, 2411, 102),
(96, 3, 2, 2403, 103),
(97, 3, 2, 2407, 104),
(98, 4, 2, 2408, 100),
(99, 4, 2, 2416, 101),
(100, 4, 2, 2406, 102),
(101, 4, 2, 2404, 103),
(102, 4, 2, 2410, 104),
(103, 5, 2, 2404, 100),
(104, 5, 2, 2409, 101),
(105, 5, 2, 2415, 102),
(106, 5, 2, 2416, 103),
(107, 5, 2, 2408, 104),
(108, 1, 3, 2404, 100),
(109, 1, 3, 2405, 101),
(110, 1, 3, 2407, 102),
(111, 1, 3, 2401, 103),
(112, 1, 3, 2411, 104),
(113, 2, 3, 2401, 100),
(114, 2, 3, 2413, 101),
(115, 2, 3, 2414, 102),
(116, 2, 3, 2402, 103),
(117, 2, 3, 2416, 104),
(118, 3, 3, 2402, 100),
(119, 3, 3, 2411, 101),
(120, 3, 3, 2410, 102),
(121, 3, 3, 2403, 103),
(122, 3, 3, 2404, 104),
(123, 4, 3, 2416, 100),
(124, 4, 3, 2415, 101),
(125, 4, 3, 2403, 102),
(126, 4, 3, 2413, 103),
(127, 4, 3, 2407, 104),
(128, 5, 3, 2409, 100),
(129, 5, 3, 2408, 101),
(130, 5, 3, 2406, 102),
(131, 5, 3, 2410, 103),
(132, 5, 3, 2405, 104),
(133, 1, 4, 2403, 100),
(134, 1, 4, 2405, 101),
(135, 1, 4, 2411, 102),
(136, 1, 4, 2401, 103),
(137, 1, 4, 2414, 104),
(138, 2, 4, 2402, 100),
(139, 2, 4, 2413, 101),
(140, 2, 4, 2404, 102),
(141, 2, 4, 2403, 103),
(142, 2, 4, 2407, 104),
(143, 3, 4, 2401, 100),
(144, 3, 4, 2408, 101),
(145, 3, 4, 2415, 102),
(146, 3, 4, 2402, 103),
(147, 3, 4, 2410, 104),
(148, 4, 4, 2409, 100),
(149, 4, 4, 2410, 101),
(150, 4, 4, 2406, 102),
(151, 4, 4, 2416, 103),
(152, 4, 4, 2411, 104),
(153, 5, 4, 2414, 100),
(154, 5, 4, 2416, 101),
(155, 5, 4, 2407, 102),
(156, 5, 4, 2413, 103),
(157, 5, 4, 2415, 104);

-- --------------------------------------------------------

--
-- Table structure for table `libros`
--

CREATE TABLE `libros` (
  `id_libro` int NOT NULL,
  `id_asignatura` int NOT NULL,
  `id_curso` int NOT NULL,
  `titulo` varchar(60) CHARACTER SET utf8mb4 COLLATE utf8mb4_spanish2_ci NOT NULL,
  `subir_libro` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_spanish2_ci NOT NULL,
  `portada` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_spanish2_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish2_ci;

-- --------------------------------------------------------

--
-- Table structure for table `material_estudio`
--

CREATE TABLE `material_estudio` (
  `id_material` int NOT NULL,
  `id_curso` int NOT NULL,
  `titulo` varchar(60) CHARACTER SET utf8mb4 COLLATE utf8mb4_spanish2_ci NOT NULL,
  `material_subido` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_spanish2_ci NOT NULL,
  `descripcion` text CHARACTER SET utf8mb4 COLLATE utf8mb4_spanish2_ci NOT NULL,
  `id_asignatura` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish2_ci;

--
-- Dumping data for table `material_estudio`
--

INSERT INTO `material_estudio` (`id_material`, `id_curso`, `titulo`, `material_subido`, `descripcion`, `id_asignatura`) VALUES
(1, 1, 'Investigacion', '', 'Ciencia de la Naturales es una asignatura que se enfoca en comprender los procesos y fenómenos que ocurren en nuestro entorno natural. Los estudiantes aprenden sobre la estructura y funcionamiento de los seres vivos, las sustancias químicas que componen el mundo, las fuerzas físicas y los procesos geológicos que modelan nuestro planeta.', 2404);

-- --------------------------------------------------------

--
-- Table structure for table `profesores`
--

CREATE TABLE `profesores` (
  `id_profesor` int NOT NULL,
  `id_asignatura` int NOT NULL,
  `matricula` char(10) CHARACTER SET utf8mb3 COLLATE utf8mb3_spanish_ci NOT NULL,
  `nombre` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_spanish_ci NOT NULL,
  `apellido` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_spanish_ci NOT NULL,
  `direccion` text CHARACTER SET utf8mb3 COLLATE utf8mb3_spanish_ci NOT NULL,
  `cedula` char(14) CHARACTER SET utf8mb3 COLLATE utf8mb3_spanish_ci NOT NULL,
  `genero` varchar(10) CHARACTER SET utf8mb3 COLLATE utf8mb3_spanish_ci NOT NULL,
  `email` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_spanish_ci NOT NULL,
  `telefono` char(12) CHARACTER SET utf8mb3 COLLATE utf8mb3_spanish_ci NOT NULL,
  `contraseña` varchar(20) CHARACTER SET utf8mb3 COLLATE utf8mb3_spanish_ci NOT NULL,
  `imagen_perfil` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_spanish_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_spanish_ci;

--
-- Dumping data for table `profesores`
--

INSERT INTO `profesores` (`id_profesor`, `id_asignatura`, `matricula`, `nombre`, `apellido`, `direccion`, `cedula`, `genero`, `email`, `telefono`, `contraseña`, `imagen_perfil`) VALUES
(10011, 2401, 'p001', 'Juan', ' Gonzalez Perez', 'calle la española #233', '001-1234567-1', 'Masculino', 'juangonzales@gmail.com', '809-458-1265', 'juan123', 'static\\documentos\\20 Reasons Freddie Prinze Jr_ Was Your Favorite 90s Heartthrob (Photos).jpg'),
(10012, 2402, 'p002', 'Maria', 'Lopez Garcia', 'Calle 20 #65, Donde Milton', '002-2345678-2', 'Femenino', 'mARIlopez@gmail.com', '809-234-5678', 'maria123', 'static\\documentos\\Alessia Santoro.jpg'),
(10013, 2403, 'p003', 'Carlos', 'Dominguez Fernandez', 'Calle 5 El hoyo de puchula', '003-3456789-3', 'Masculino', 'carlos.dominguezfernandez@gmail.com', '809-345-6789', 'carlos123', 'static\\documentos\\10 Reasons Why Chandler Bing Is My Spirit Animal.jpg'),
(10014, 2404, 'p004', 'Ana', 'Sanchez Ruiz', 'Calle principal Don Lindo', '004-4567890-4', 'Femenino', 'anaruiz@gmail.com', '809-456-7890', 'ana123', 'static\\documentos\\Corporate Headshot Photographer in Los Angeles.jpg'),
(10015, 2405, 'p005', 'Luis Mario ', 'Martinez Gomez', 'Calle principal, Juan Dolio', '005-5678901-5', 'Masculino', 'luismartinez@gmail.com', '809-567-8901', 'luismario123', 'static\\documentos\\21 Sexy and Comfortable Swimsuits Perfect For Women With Small Chests.jpg'),
(10016, 2412, 'p006', 'Macarena', 'Ramirez Torres', 'Licey al medio, Residencial los profesores', ' 006-6789012-6', 'Femenino', 'ramireztorresMac@gmail.com', '809-678-9012', 'macarena123', 'static\\documentos\\descarga (1).jpg'),
(10017, 2414, 'p007', 'Javier', 'Dias Morales', 'Licey al medio #5', ' 007-7890123-7', 'Masculino', 'javiDiazmorales@gmail.com', '809-789-0123', 'javier123', 'static\\documentos\\21 Fine-As-Hell Asian Men Who Will Make You Swoon And Then Some.jpg'),
(10018, 2408, 'p008', 'Maria Elena', 'Hernandez Castro', 'Avenida Estrella Sadhalá #30', '008-8901234-8', 'Femenino', 'elenahernandezcastro@example.com', '809-890-1234', 'mariaElena123', 'static\\documentos\\descarga (3).jpg'),
(10019, 2409, 'p620', 'Marisbel', 'Almonte Acosta', 'Licey al medio, La Chiva 1', '493-29339-2', 'femenino', 'Marisbel62@gmail.com', '809-486-7234', 'marisbel62', 'static\\documentos\\descarga (4).jpg'),
(10020, 2403, 'p360', 'Luis Angel', 'Fermin Perez', 'Calle 2 #1, Los Salados', '031-29120-1', 'masculino', 'momo360lol@gmail.com', '829-819-9212', 'unacabra', 'static\\documentos\\Get Smarter, Sleep Better and Laugh More With the 56 Best Podcasts You Can Listen to in 2024.jpg'),
(10021, 2405, 'p456', 'Rosio', 'Garcia Gil', 'Calle 20 #65, San Juan de la Maguana', '402-78944-7', 'femenino', 'roci789@gmail.com', '809-486-2534', 'roci123', 'static\\documentos\\descarga (6).jpg'),
(10022, 2409, 'p889', 'Yandel', 'Mendez Guzman', 'Calle 4 #7, Villa Liberación, La Otra Banda', '402-30213-0', 'masculino', 'yazelumet04@gmail.com', '849-121-8921', 'yandeleslapara', 'static\\documentos\\The Goldfinch Is Surrounded By True Stories & Strange Coincidences.jpg'),
(10023, 2406, 'p452', 'Samantha', 'Luciano Vasquez ', 'Calle las palomas #8', '402-789564-8', 'femenino', 'samLuciano@gmail.com', '809-526-7234', 's123', 'static\\documentos\\descarga (7).jpg'),
(10024, 2407, 'p788', 'Miguel', 'Herrera', 'Calle 18 #6, La Joya', '031-39323-1', 'masculino', 'mybestofrendo@gmail.com', '849-081-2781', 'agustin51', 'static\\documentos\\Let\'s Take a Moment to Appreciate the Perfectly Preppy Style Choices of Stranger Things\' Nancy Wheeler.jpg'),
(10025, 2409, 'p754', 'Tessia', 'Rea Garcia', 'Licey al medio / la reina ', '402-758664-8', 'femenino', 'tessia452@gmail.com', '829-819-5266', 'tassia123', 'static\\documentos\\descarga (8).jpg'),
(10026, 2402, 'p777', 'Hendry', 'Rodriguez Valdez', 'Calle principal #6, La Otra Banda', '402-117921-0', 'masculino', 'pobobabosha@gmail.com', '809-192-9182', 'babosha', 'static\\documentos\\descarga.jpg'),
(10027, 2406, 'p897', 'Angelica', 'Burgos Paulino ', 'Licey al medio, Residencial Joel Arturo #4', '402-123664-7', 'femenino', 'angelica745@gmail.com', '849-851-8921', 'angelica123', 'static\\documentos\\descarga (9).jpg'),
(10028, 2403, 'p126', 'Emma ', 'Jimenez Torres', 'Entrada las palmas #5 ', '402-123894-7', 'femenino', 'emma456@gmail.com', '809-526-7845', 'emma123', 'static\\documentos\\descarga.jpg'),
(10029, 2405, 'p712', 'Teresa ', 'Paulino Rojas ', 'Entrada Borojoi #9', '402-458664-5', 'femenino', 'teresa45@gmail.com', '809-486-5236', 'teresa123', 'static\\documentos\\Dulce Amélia Nott.jpg'),
(10030, 2408, 'p736', 'Angel', 'Feliz', 'Boca Chica, Santo Domingo', '402-183910-0', 'masculino', 'claudioangel01@gmail.com', '829-091-2901', 'elpicapila', 'static\\documentos\\The Trailer For Netflix\'s Daredevil Includes a Nod to Iron Man and Thor.jpg'),
(10031, 2409, 'p757', 'Eric', 'Mena', 'Boca Chica, Santo Domingo', '031-293101-2', 'masculino', 'ericmena71@gmail.com', '849-129-9320', 'elprofesor', 'static\\documentos\\descarga (2).jpg');

-- --------------------------------------------------------

--
-- Table structure for table `profesor_asignado`
--

CREATE TABLE `profesor_asignado` (
  `id_profesor_asignado` int NOT NULL,
  `id_profesor` int NOT NULL,
  `id_curso` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_spanish_ci;

--
-- Dumping data for table `profesor_asignado`
--

INSERT INTO `profesor_asignado` (`id_profesor_asignado`, `id_profesor`, `id_curso`) VALUES
(1, 10011, 1),
(2, 10014, 1),
(3, 10011, 7),
(4, 10031, 2),
(5, 10030, 2),
(6, 10029, 3),
(7, 10028, 3),
(8, 10027, 4),
(9, 10026, 4),
(10, 10025, 5),
(11, 10024, 5),
(12, 10023, 6),
(13, 10022, 6),
(14, 10021, 7),
(15, 10020, 8),
(16, 10019, 8),
(17, 10018, 9),
(18, 10017, 9),
(19, 10016, 10),
(20, 10015, 10),
(21, 10014, 11),
(22, 10013, 11),
(23, 10012, 12),
(24, 10011, 12),
(25, 10015, 1),
(26, 10013, 1),
(27, 10017, 1),
(28, 10016, 1);

-- --------------------------------------------------------

--
-- Table structure for table `reporte_profesor`
--

CREATE TABLE `reporte_profesor` (
  `id_report` int NOT NULL,
  `id_profesor-asignado` int NOT NULL,
  `asistencia` varchar(600) CHARACTER SET utf8mb4 COLLATE utf8mb4_spanish2_ci NOT NULL,
  `calificaciones` varchar(600) CHARACTER SET utf8mb4 COLLATE utf8mb4_spanish2_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish2_ci;

-- --------------------------------------------------------

--
-- Table structure for table `tareas_estudiante`
--

CREATE TABLE `tareas_estudiante` (
  `id_tarea` int NOT NULL,
  `id_material` int NOT NULL,
  `id_estudiante` int NOT NULL,
  `id_curso` int NOT NULL,
  `tarea` varchar(300) CHARACTER SET utf8mb4 COLLATE utf8mb4_spanish2_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish2_ci;

--
-- Dumping data for table `tareas_estudiante`
--

INSERT INTO `tareas_estudiante` (`id_tarea`, `id_material`, `id_estudiante`, `id_curso`, `tarea`) VALUES
(1, 1, 2, 1, 'ejemplo-espanol.pdf');

-- --------------------------------------------------------

--
-- Table structure for table `videos`
--

CREATE TABLE `videos` (
  `id` int NOT NULL,
  `titulo` varchar(60) CHARACTER SET utf8mb4 COLLATE utf8mb4_spanish2_ci NOT NULL,
  `id_curso` int NOT NULL,
  `id_asignatura` int NOT NULL,
  `video` text CHARACTER SET utf8mb4 COLLATE utf8mb4_spanish2_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish2_ci;

--
-- Dumping data for table `videos`
--

INSERT INTO `videos` (`id`, `titulo`, `id_curso`, `id_asignatura`, `video`) VALUES
(2, 'Don quijote', 1, 2408, '<iframe width=\"560\" height=\"315\" src=\"https://www.youtube.com/embed/ir6A-Ns5Em8?si=y-I8_Uain9fbW5vZ\" title=\"YouTube video player\" frameborder=\"0\" allow=\"accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share\" referrerpolicy=\"strict-origin-when-cross-origin\" allowfullscreen></iframe>'),
(3, 'La naturaleza', 1, 2404, '<iframe width=\"560\" height=\"315\" src=\"https://www.youtube.com/embed/j6LunB9d2Bo?si=JaIb5RaXyWx1I_-p\" title=\"YouTube video player\" frameborder=\"0\" allow=\"accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share\" referrerpolicy=\"strict-origin-when-cross-origin\" allowfullscreen></iframe>'),
(4, 'Diptongos', 1, 2401, '<iframe width=\"560\" height=\"315\" src=\"https://www.youtube.com/embed/mvmYv3iYsq4?si=TWrpcwbHc6ug9vLC\" title=\"YouTube video player\" frameborder=\"0\" allow=\"accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share\" referrerpolicy=\"strict-origin-when-cross-origin\" allowfullscreen></iframe>');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `admin`
--
ALTER TABLE `admin`
  ADD PRIMARY KEY (`id_admin`);

--
-- Indexes for table `asignaturas`
--
ALTER TABLE `asignaturas`
  ADD PRIMARY KEY (`id_asignatura`);

--
-- Indexes for table `asignatura_curso`
--
ALTER TABLE `asignatura_curso`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id_curso` (`id_curso`),
  ADD KEY `id_asignatura` (`id_asignatura`);

--
-- Indexes for table `asistencias`
--
ALTER TABLE `asistencias`
  ADD PRIMARY KEY (`id_asistencia`),
  ADD KEY `id_estudiante` (`id_estudiante`),
  ADD KEY `id_curso` (`id_curso`),
  ADD KEY `id_asignatura` (`id_asignatura`);

--
-- Indexes for table `calificaciones`
--
ALTER TABLE `calificaciones`
  ADD PRIMARY KEY (`id_calificacion`),
  ADD KEY `id_estudiante` (`id_estudiante`),
  ADD KEY `id_asignatura` (`id_asignatura`),
  ADD KEY `id_curso` (`id_curso`);

--
-- Indexes for table `cursos`
--
ALTER TABLE `cursos`
  ADD PRIMARY KEY (`id_curso`);

--
-- Indexes for table `dias`
--
ALTER TABLE `dias`
  ADD PRIMARY KEY (`id_dias`);

--
-- Indexes for table `estudiantes`
--
ALTER TABLE `estudiantes`
  ADD PRIMARY KEY (`id_estudiante`),
  ADD KEY `id_curso_seccion` (`id_curso`);

--
-- Indexes for table `hora`
--
ALTER TABLE `hora`
  ADD PRIMARY KEY (`id_hora`);

--
-- Indexes for table `horario`
--
ALTER TABLE `horario`
  ADD PRIMARY KEY (`id_horario`),
  ADD KEY `id_horas` (`id_hora`),
  ADD KEY `id_cursos` (`id_curso`),
  ADD KEY `id_asignaturas` (`id_asignatura`),
  ADD KEY `id_dias` (`id_dias`),
  ADD KEY `id_curso_seccion` (`id_curso`);

--
-- Indexes for table `libros`
--
ALTER TABLE `libros`
  ADD PRIMARY KEY (`id_libro`),
  ADD KEY `id_asignatura` (`id_asignatura`),
  ADD KEY `id_curso` (`id_curso`);

--
-- Indexes for table `material_estudio`
--
ALTER TABLE `material_estudio`
  ADD PRIMARY KEY (`id_material`),
  ADD KEY `id_curso` (`id_curso`),
  ADD KEY `id_asignatura` (`id_asignatura`);

--
-- Indexes for table `profesores`
--
ALTER TABLE `profesores`
  ADD PRIMARY KEY (`id_profesor`),
  ADD KEY `id_asignatura` (`id_asignatura`);

--
-- Indexes for table `profesor_asignado`
--
ALTER TABLE `profesor_asignado`
  ADD PRIMARY KEY (`id_profesor_asignado`),
  ADD KEY `id_profesor` (`id_profesor`),
  ADD KEY `id_curso_seccion` (`id_curso`);

--
-- Indexes for table `reporte_profesor`
--
ALTER TABLE `reporte_profesor`
  ADD PRIMARY KEY (`id_report`),
  ADD KEY `id_profesor-asignado` (`id_profesor-asignado`);

--
-- Indexes for table `tareas_estudiante`
--
ALTER TABLE `tareas_estudiante`
  ADD PRIMARY KEY (`id_tarea`),
  ADD KEY `id_estudiante` (`id_estudiante`),
  ADD KEY `id_curso` (`id_curso`),
  ADD KEY `id_material` (`id_material`);

--
-- Indexes for table `videos`
--
ALTER TABLE `videos`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id_curso` (`id_curso`),
  ADD KEY `id_asignatura` (`id_asignatura`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `admin`
--
ALTER TABLE `admin`
  MODIFY `id_admin` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `asignaturas`
--
ALTER TABLE `asignaturas`
  MODIFY `id_asignatura` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2417;

--
-- AUTO_INCREMENT for table `asignatura_curso`
--
ALTER TABLE `asignatura_curso`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `asistencias`
--
ALTER TABLE `asistencias`
  MODIFY `id_asistencia` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `calificaciones`
--
ALTER TABLE `calificaciones`
  MODIFY `id_calificacion` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT for table `cursos`
--
ALTER TABLE `cursos`
  MODIFY `id_curso` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT for table `dias`
--
ALTER TABLE `dias`
  MODIFY `id_dias` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=105;

--
-- AUTO_INCREMENT for table `estudiantes`
--
ALTER TABLE `estudiantes`
  MODIFY `id_estudiante` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=27;

--
-- AUTO_INCREMENT for table `hora`
--
ALTER TABLE `hora`
  MODIFY `id_hora` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `horario`
--
ALTER TABLE `horario`
  MODIFY `id_horario` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=158;

--
-- AUTO_INCREMENT for table `libros`
--
ALTER TABLE `libros`
  MODIFY `id_libro` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `material_estudio`
--
ALTER TABLE `material_estudio`
  MODIFY `id_material` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `profesores`
--
ALTER TABLE `profesores`
  MODIFY `id_profesor` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10032;

--
-- AUTO_INCREMENT for table `profesor_asignado`
--
ALTER TABLE `profesor_asignado`
  MODIFY `id_profesor_asignado` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=29;

--
-- AUTO_INCREMENT for table `tareas_estudiante`
--
ALTER TABLE `tareas_estudiante`
  MODIFY `id_tarea` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `videos`
--
ALTER TABLE `videos`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `asignatura_curso`
--
ALTER TABLE `asignatura_curso`
  ADD CONSTRAINT `asignatura_curso_ibfk_1` FOREIGN KEY (`id_curso`) REFERENCES `cursos` (`id_curso`),
  ADD CONSTRAINT `asignatura_curso_ibfk_2` FOREIGN KEY (`id_asignatura`) REFERENCES `asignaturas` (`id_asignatura`);

--
-- Constraints for table `asistencias`
--
ALTER TABLE `asistencias`
  ADD CONSTRAINT `asistencias_ibfk_1` FOREIGN KEY (`id_estudiante`) REFERENCES `estudiantes` (`id_estudiante`),
  ADD CONSTRAINT `asistencias_ibfk_2` FOREIGN KEY (`id_curso`) REFERENCES `cursos` (`id_curso`),
  ADD CONSTRAINT `asistencias_ibfk_3` FOREIGN KEY (`id_asignatura`) REFERENCES `asignaturas` (`id_asignatura`);

--
-- Constraints for table `calificaciones`
--
ALTER TABLE `calificaciones`
  ADD CONSTRAINT `calificaciones_ibfk_1` FOREIGN KEY (`id_asignatura`) REFERENCES `asignaturas` (`id_asignatura`),
  ADD CONSTRAINT `calificaciones_ibfk_2` FOREIGN KEY (`id_estudiante`) REFERENCES `estudiantes` (`id_estudiante`),
  ADD CONSTRAINT `calificaciones_ibfk_3` FOREIGN KEY (`id_curso`) REFERENCES `cursos` (`id_curso`);

--
-- Constraints for table `estudiantes`
--
ALTER TABLE `estudiantes`
  ADD CONSTRAINT `estudiantes_ibfk_1` FOREIGN KEY (`id_curso`) REFERENCES `cursos` (`id_curso`);

--
-- Constraints for table `horario`
--
ALTER TABLE `horario`
  ADD CONSTRAINT `horario_ibfk_1` FOREIGN KEY (`id_hora`) REFERENCES `hora` (`id_hora`),
  ADD CONSTRAINT `horario_ibfk_2` FOREIGN KEY (`id_dias`) REFERENCES `dias` (`id_dias`),
  ADD CONSTRAINT `horario_ibfk_4` FOREIGN KEY (`id_asignatura`) REFERENCES `asignaturas` (`id_asignatura`),
  ADD CONSTRAINT `horario_ibfk_7` FOREIGN KEY (`id_curso`) REFERENCES `cursos` (`id_curso`);

--
-- Constraints for table `libros`
--
ALTER TABLE `libros`
  ADD CONSTRAINT `libros_ibfk_1` FOREIGN KEY (`id_asignatura`) REFERENCES `asignaturas` (`id_asignatura`),
  ADD CONSTRAINT `libros_ibfk_2` FOREIGN KEY (`id_curso`) REFERENCES `cursos` (`id_curso`);

--
-- Constraints for table `material_estudio`
--
ALTER TABLE `material_estudio`
  ADD CONSTRAINT `material_estudio_ibfk_1` FOREIGN KEY (`id_curso`) REFERENCES `cursos` (`id_curso`),
  ADD CONSTRAINT `material_estudio_ibfk_2` FOREIGN KEY (`id_asignatura`) REFERENCES `asignaturas` (`id_asignatura`);

--
-- Constraints for table `profesores`
--
ALTER TABLE `profesores`
  ADD CONSTRAINT `profesores_ibfk_1` FOREIGN KEY (`id_asignatura`) REFERENCES `asignaturas` (`id_asignatura`);

--
-- Constraints for table `profesor_asignado`
--
ALTER TABLE `profesor_asignado`
  ADD CONSTRAINT `profesor_asignado_ibfk_2` FOREIGN KEY (`id_profesor`) REFERENCES `profesores` (`id_profesor`),
  ADD CONSTRAINT `profesor_asignado_ibfk_3` FOREIGN KEY (`id_curso`) REFERENCES `cursos` (`id_curso`);

--
-- Constraints for table `reporte_profesor`
--
ALTER TABLE `reporte_profesor`
  ADD CONSTRAINT `reporte_profesor_ibfk_1` FOREIGN KEY (`id_profesor-asignado`) REFERENCES `profesor_asignado` (`id_profesor_asignado`);

--
-- Constraints for table `tareas_estudiante`
--
ALTER TABLE `tareas_estudiante`
  ADD CONSTRAINT `tareas_estudiante_ibfk_1` FOREIGN KEY (`id_estudiante`) REFERENCES `estudiantes` (`id_estudiante`),
  ADD CONSTRAINT `tareas_estudiante_ibfk_2` FOREIGN KEY (`id_curso`) REFERENCES `cursos` (`id_curso`),
  ADD CONSTRAINT `tareas_estudiante_ibfk_3` FOREIGN KEY (`id_material`) REFERENCES `material_estudio` (`id_material`);

--
-- Constraints for table `videos`
--
ALTER TABLE `videos`
  ADD CONSTRAINT `videos_ibfk_1` FOREIGN KEY (`id_curso`) REFERENCES `cursos` (`id_curso`),
  ADD CONSTRAINT `videos_ibfk_2` FOREIGN KEY (`id_asignatura`) REFERENCES `asignaturas` (`id_asignatura`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
