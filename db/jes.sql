-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 02-08-2024 a las 06:00:37
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.1.25

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `jes`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `admin`
--

CREATE TABLE `admin` (
  `id_admin` int(4) NOT NULL,
  `nombre_admin` varchar(40) NOT NULL,
  `a_apellido` varchar(40) NOT NULL,
  `a_email` varchar(140) NOT NULL,
  `a_genero` char(10) NOT NULL,
  `a_direccion` text NOT NULL,
  `a_telefono` char(14) NOT NULL,
  `a_img_perfil` longblob NOT NULL,
  `matricula` varchar(20) NOT NULL,
  `contraseña` varchar(40) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish2_ci;

--
-- Volcado de datos para la tabla `admin`
--

INSERT INTO `admin` (`id_admin`, `nombre_admin`, `a_apellido`, `a_email`, `a_genero`, `a_direccion`, `a_telefono`, `a_img_perfil`, `matricula`, `contraseña`) VALUES
(1, 'Jhon Mike', 'Peña Ramos', 'jhonmip2@gmail.com', 'Masculino', 'Calle 16 de Agosto #01', '809-101-0000', 0x68747470733a2f2f706c75732e756e73706c6173682e636f6d2f7072656d69756d5f70686f746f2d313637313635363334393332322d3431646539343464323539623f713d383026773d31383837266175746f3d666f726d6174266669743d63726f702669786c69623d72622d342e302e3326697869643d4d3377784d6a4133664442384d48787761473930627931775957646c664878386647567566444238664878386641253344253344, 'a-0002231', 'admin2330');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `asignaturas`
--

CREATE TABLE `asignaturas` (
  `id_asignatura` int(10) NOT NULL,
  `nom_asignatura` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_spanish_ci;

--
-- Volcado de datos para la tabla `asignaturas`
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
(2409, 'Formacion Humana');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `asistencias`
--

CREATE TABLE `asistencias` (
  `id_asistencia` int(10) NOT NULL,
  `id_estudiante` int(11) NOT NULL,
  `Sect - Oct` char(4) NOT NULL,
  `Nov - Dic` char(4) NOT NULL,
  `Ene - Feb` char(4) NOT NULL,
  `Marz - Abril` char(4) NOT NULL,
  `May - Jun` char(4) NOT NULL,
  `Total de asistencias` int(4) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_spanish_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `calificaciones`
--

CREATE TABLE `calificaciones` (
  `id_calificacion` int(10) NOT NULL,
  `id_estudiante` int(10) NOT NULL,
  `id_asignatura` int(10) NOT NULL,
  `C1` int(3) NOT NULL,
  `C2` int(3) NOT NULL,
  `C3` int(3) NOT NULL,
  `C4` int(3) NOT NULL,
  `C. Final` int(3) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_spanish_ci;

--
-- Volcado de datos para la tabla `calificaciones`
--

INSERT INTO `calificaciones` (`id_calificacion`, `id_estudiante`, `id_asignatura`, `C1`, `C2`, `C3`, `C4`, `C. Final`) VALUES
(1, 2, 2403, 100, 100, 100, 100, 100);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `cursos`
--

CREATE TABLE `cursos` (
  `id_curso` int(10) NOT NULL,
  `nombre` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_spanish_ci;

--
-- Volcado de datos para la tabla `cursos`
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
-- Estructura de tabla para la tabla `dias`
--

CREATE TABLE `dias` (
  `id_dias` int(10) NOT NULL,
  `dia` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_spanish_ci;

--
-- Volcado de datos para la tabla `dias`
--

INSERT INTO `dias` (`id_dias`, `dia`) VALUES
(100, 'Lunes'),
(101, 'Martes'),
(102, 'Miercoles'),
(103, 'Jueves'),
(104, 'Viernes');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `estudiantes`
--

CREATE TABLE `estudiantes` (
  `id_estudiante` int(11) NOT NULL,
  `id_curso` int(10) NOT NULL,
  `matricula` char(10) NOT NULL,
  `nombre` varchar(30) NOT NULL,
  `apellidos` varchar(50) NOT NULL,
  `direccion` text NOT NULL,
  `fecha_nacimiento` date NOT NULL,
  `genero` varchar(10) NOT NULL,
  `email` varchar(50) NOT NULL,
  `telefono` char(12) NOT NULL,
  `imagen_perfil` longblob NOT NULL,
  `contraseña` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_spanish_ci;

--
-- Volcado de datos para la tabla `estudiantes`
--

INSERT INTO `estudiantes` (`id_estudiante`, `id_curso`, `matricula`, `nombre`, `apellidos`, `direccion`, `fecha_nacimiento`, `genero`, `email`, `telefono`, `imagen_perfil`, `contraseña`) VALUES
(2, 1, 'e-9990', 'Albiery', 'Rodriguez', 'calle 16 de agosto #1', '2010-10-19', 'masculino', 'albieryr@gmail.com', '8095889924', 0x68747470733a2f2f696d616765732e756e73706c6173682e636f6d2f70686f746f2d313532313131393938393635392d6138336565653438383030343f713d383026773d31393233266175746f3d666f726d6174266669743d63726f702669786c69623d72622d342e302e3326697869643d4d3377784d6a4133664442384d48787761473930627931775957646c664878386647567566444238664878386641253344253344, 'estudiante123');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `hora`
--

CREATE TABLE `hora` (
  `id_hora` int(10) NOT NULL,
  `hora` varchar(12) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_spanish_ci;

--
-- Volcado de datos para la tabla `hora`
--

INSERT INTO `hora` (`id_hora`, `hora`) VALUES
(1, '7:30-8:30'),
(2, '8:30-9:30'),
(3, '9:30-10:00'),
(4, '10:00-11:00'),
(5, '11:00-12:00');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `horario`
--

CREATE TABLE `horario` (
  `id_horario` int(10) NOT NULL,
  `id_estudiante` int(11) NOT NULL,
  `id_hora` int(10) NOT NULL,
  `id_curso` int(10) NOT NULL,
  `id_asignatura` int(10) NOT NULL,
  `id_dias` int(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_spanish_ci;

--
-- Volcado de datos para la tabla `horario`
--

INSERT INTO `horario` (`id_horario`, `id_estudiante`, `id_hora`, `id_curso`, `id_asignatura`, `id_dias`) VALUES
(1, 2, 1, 1, 2403, 100);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `libros`
--

CREATE TABLE `libros` (
  `id_libro` int(11) NOT NULL,
  `id_asignatura` int(11) NOT NULL,
  `id_curso` int(10) NOT NULL,
  `titulo` varchar(60) NOT NULL,
  `subir_libro` longblob NOT NULL,
  `portada` longblob NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish2_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `material_estudio`
--

CREATE TABLE `material_estudio` (
  `id_material` int(11) NOT NULL,
  `id_curso` int(10) NOT NULL,
  `titulo` varchar(60) NOT NULL,
  `material_subido` longblob NOT NULL,
  `fondo` longblob NOT NULL,
  `descripcion` text NOT NULL,
  `id_asignatura` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish2_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `profesores`
--

CREATE TABLE `profesores` (
  `id_profesor` int(10) NOT NULL,
  `id_asignatura` int(10) NOT NULL,
  `matricula` char(10) NOT NULL,
  `nombre` varchar(50) NOT NULL,
  `apellido` varchar(50) NOT NULL,
  `direccion` text NOT NULL,
  `cedula` char(14) NOT NULL,
  `genero` varchar(10) NOT NULL,
  `email` varchar(50) NOT NULL,
  `telefono` char(12) NOT NULL,
  `contraseña` varchar(20) NOT NULL,
  `imagen_perfil` longblob NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_spanish_ci;

--
-- Volcado de datos para la tabla `profesores`
--

INSERT INTO `profesores` (`id_profesor`, `id_asignatura`, `matricula`, `nombre`, `apellido`, `direccion`, `cedula`, `genero`, `email`, `telefono`, `contraseña`, `imagen_perfil`) VALUES
(10011, 2401, 'p001', 'Juan', ' Gonzalez Perez', '', '001-1234567-1', 'Masculino', 'juangonzales@gmail.com', '809-458-1265', 'juan123', ''),
(10012, 2402, 'p002', 'Maria', 'Lopez Garcia', '', '002-2345678-2', 'Femenino', 'mARIlopez@gmail.com', '809-234-5678', 'maria123', ''),
(10013, 2403, 'p003', 'Carlos', 'Dominguez Fernandez', '', '003-3456789-3', 'Masculino', 'carlos.dominguezfernandez@gmail.com', '809-345-6789', 'carlos123', ''),
(10014, 2404, 'p004', 'Ana', 'Sanchez Ruiz', '', '004-4567890-4', 'Femenino', 'anaruiz@gmail.com', '809-456-7890', 'ana123', ''),
(10015, 2405, 'p005', 'Luis Mario ', 'Martinez Gomez', '', '005-5678901-5', 'Masculino', 'luismartinez@gmail.com', '809-567-8901', 'luismario123', ''),
(10016, 2406, 'p006', 'Macarena', 'Ramirez Torres', '', ' 006-6789012-6', 'Femenino', 'ramireztorresMac@gmail.com', '809-678-9012', 'macarena123', ''),
(10017, 2407, 'p007', 'Javier', 'Dias Morales', '', ' 007-7890123-7', 'Masculino', 'javiDiazmorales@gmail.com', '809-789-0123', 'javier123', ''),
(10018, 2408, 'p008', 'Maria Elena', 'Hernandez Castro', '', '008-8901234-8', 'Femenino', 'elenahernandezcastro@example.com', '809-890-1234', 'mariaElena123', ''),
(10019, 2409, 'p009', 'Isabel', ' Navarro Vá\\azquez', '', '010-0123456-0', 'Femenino', 'isabelvazquez@example.com', '809-456-6461', 'isabel123', '');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `profesor_asignado`
--

CREATE TABLE `profesor_asignado` (
  `id_profesor-asignado` int(10) NOT NULL,
  `id_profesor` int(10) NOT NULL,
  `id_curso` int(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_spanish_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `videos`
--

CREATE TABLE `videos` (
  `id` int(10) NOT NULL,
  `titulo` varchar(60) NOT NULL,
  `id_curso` int(10) NOT NULL,
  `id_asignatura` int(10) NOT NULL,
  `video` longblob NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish2_ci;

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `admin`
--
ALTER TABLE `admin`
  ADD PRIMARY KEY (`id_admin`);

--
-- Indices de la tabla `asignaturas`
--
ALTER TABLE `asignaturas`
  ADD PRIMARY KEY (`id_asignatura`);

--
-- Indices de la tabla `asistencias`
--
ALTER TABLE `asistencias`
  ADD PRIMARY KEY (`id_asistencia`),
  ADD KEY `id_estudiante` (`id_estudiante`);

--
-- Indices de la tabla `calificaciones`
--
ALTER TABLE `calificaciones`
  ADD PRIMARY KEY (`id_calificacion`),
  ADD KEY `id_estudiante` (`id_estudiante`),
  ADD KEY `id_asignatura` (`id_asignatura`);

--
-- Indices de la tabla `cursos`
--
ALTER TABLE `cursos`
  ADD PRIMARY KEY (`id_curso`);

--
-- Indices de la tabla `dias`
--
ALTER TABLE `dias`
  ADD PRIMARY KEY (`id_dias`);

--
-- Indices de la tabla `estudiantes`
--
ALTER TABLE `estudiantes`
  ADD PRIMARY KEY (`id_estudiante`),
  ADD KEY `id_curso_seccion` (`id_curso`);

--
-- Indices de la tabla `hora`
--
ALTER TABLE `hora`
  ADD PRIMARY KEY (`id_hora`);

--
-- Indices de la tabla `horario`
--
ALTER TABLE `horario`
  ADD PRIMARY KEY (`id_horario`),
  ADD KEY `id_horas` (`id_hora`),
  ADD KEY `id_cursos` (`id_curso`),
  ADD KEY `id_asignaturas` (`id_asignatura`),
  ADD KEY `id_dias` (`id_dias`),
  ADD KEY `id_curso_seccion` (`id_curso`),
  ADD KEY `id_estudiante` (`id_estudiante`);

--
-- Indices de la tabla `libros`
--
ALTER TABLE `libros`
  ADD PRIMARY KEY (`id_libro`),
  ADD KEY `id_asignatura` (`id_asignatura`),
  ADD KEY `id_curso` (`id_curso`);

--
-- Indices de la tabla `material_estudio`
--
ALTER TABLE `material_estudio`
  ADD PRIMARY KEY (`id_material`),
  ADD KEY `id_curso` (`id_curso`),
  ADD KEY `id_asignatura` (`id_asignatura`);

--
-- Indices de la tabla `profesores`
--
ALTER TABLE `profesores`
  ADD PRIMARY KEY (`id_profesor`),
  ADD KEY `id_asignatura` (`id_asignatura`);

--
-- Indices de la tabla `profesor_asignado`
--
ALTER TABLE `profesor_asignado`
  ADD PRIMARY KEY (`id_profesor-asignado`),
  ADD KEY `id_profesor` (`id_profesor`),
  ADD KEY `id_curso_seccion` (`id_curso`);

--
-- Indices de la tabla `videos`
--
ALTER TABLE `videos`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id_curso` (`id_curso`),
  ADD KEY `id_asignatura` (`id_asignatura`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `admin`
--
ALTER TABLE `admin`
  MODIFY `id_admin` int(4) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `asignaturas`
--
ALTER TABLE `asignaturas`
  MODIFY `id_asignatura` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2410;

--
-- AUTO_INCREMENT de la tabla `asistencias`
--
ALTER TABLE `asistencias`
  MODIFY `id_asistencia` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `calificaciones`
--
ALTER TABLE `calificaciones`
  MODIFY `id_calificacion` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `cursos`
--
ALTER TABLE `cursos`
  MODIFY `id_curso` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT de la tabla `dias`
--
ALTER TABLE `dias`
  MODIFY `id_dias` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=105;

--
-- AUTO_INCREMENT de la tabla `estudiantes`
--
ALTER TABLE `estudiantes`
  MODIFY `id_estudiante` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `hora`
--
ALTER TABLE `hora`
  MODIFY `id_hora` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de la tabla `horario`
--
ALTER TABLE `horario`
  MODIFY `id_horario` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `libros`
--
ALTER TABLE `libros`
  MODIFY `id_libro` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `material_estudio`
--
ALTER TABLE `material_estudio`
  MODIFY `id_material` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `profesores`
--
ALTER TABLE `profesores`
  MODIFY `id_profesor` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10020;

--
-- AUTO_INCREMENT de la tabla `profesor_asignado`
--
ALTER TABLE `profesor_asignado`
  MODIFY `id_profesor-asignado` int(10) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `videos`
--
ALTER TABLE `videos`
  MODIFY `id` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `asistencias`
--
ALTER TABLE `asistencias`
  ADD CONSTRAINT `asistencias_ibfk_1` FOREIGN KEY (`id_estudiante`) REFERENCES `estudiantes` (`id_estudiante`);

--
-- Filtros para la tabla `calificaciones`
--
ALTER TABLE `calificaciones`
  ADD CONSTRAINT `calificaciones_ibfk_1` FOREIGN KEY (`id_asignatura`) REFERENCES `asignaturas` (`id_asignatura`),
  ADD CONSTRAINT `calificaciones_ibfk_2` FOREIGN KEY (`id_estudiante`) REFERENCES `estudiantes` (`id_estudiante`);

--
-- Filtros para la tabla `estudiantes`
--
ALTER TABLE `estudiantes`
  ADD CONSTRAINT `estudiantes_ibfk_1` FOREIGN KEY (`id_curso`) REFERENCES `cursos` (`id_curso`);

--
-- Filtros para la tabla `horario`
--
ALTER TABLE `horario`
  ADD CONSTRAINT `horario_ibfk_1` FOREIGN KEY (`id_hora`) REFERENCES `hora` (`id_hora`),
  ADD CONSTRAINT `horario_ibfk_2` FOREIGN KEY (`id_dias`) REFERENCES `dias` (`id_dias`),
  ADD CONSTRAINT `horario_ibfk_4` FOREIGN KEY (`id_asignatura`) REFERENCES `asignaturas` (`id_asignatura`),
  ADD CONSTRAINT `horario_ibfk_6` FOREIGN KEY (`id_estudiante`) REFERENCES `estudiantes` (`id_estudiante`),
  ADD CONSTRAINT `horario_ibfk_7` FOREIGN KEY (`id_curso`) REFERENCES `cursos` (`id_curso`);

--
-- Filtros para la tabla `libros`
--
ALTER TABLE `libros`
  ADD CONSTRAINT `libros_ibfk_1` FOREIGN KEY (`id_asignatura`) REFERENCES `asignaturas` (`id_asignatura`),
  ADD CONSTRAINT `libros_ibfk_2` FOREIGN KEY (`id_curso`) REFERENCES `cursos` (`id_curso`);

--
-- Filtros para la tabla `material_estudio`
--
ALTER TABLE `material_estudio`
  ADD CONSTRAINT `material_estudio_ibfk_1` FOREIGN KEY (`id_curso`) REFERENCES `cursos` (`id_curso`),
  ADD CONSTRAINT `material_estudio_ibfk_2` FOREIGN KEY (`id_asignatura`) REFERENCES `asignaturas` (`id_asignatura`);

--
-- Filtros para la tabla `profesores`
--
ALTER TABLE `profesores`
  ADD CONSTRAINT `profesores_ibfk_1` FOREIGN KEY (`id_asignatura`) REFERENCES `asignaturas` (`id_asignatura`);

--
-- Filtros para la tabla `profesor_asignado`
--
ALTER TABLE `profesor_asignado`
  ADD CONSTRAINT `profesor_asignado_ibfk_2` FOREIGN KEY (`id_profesor`) REFERENCES `profesores` (`id_profesor`),
  ADD CONSTRAINT `profesor_asignado_ibfk_3` FOREIGN KEY (`id_curso`) REFERENCES `cursos` (`id_curso`);

--
-- Filtros para la tabla `videos`
--
ALTER TABLE `videos`
  ADD CONSTRAINT `videos_ibfk_1` FOREIGN KEY (`id_curso`) REFERENCES `cursos` (`id_curso`),
  ADD CONSTRAINT `videos_ibfk_2` FOREIGN KEY (`id_asignatura`) REFERENCES `asignaturas` (`id_asignatura`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
