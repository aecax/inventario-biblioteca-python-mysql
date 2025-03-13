CREATE DATABASE IF NOT EXISTS biblioteca;
USE biblioteca;

CREATE TABLE libros (
    isbn VARCHAR(17) PRIMARY KEY,
    titulo VARCHAR(100) NOT NULL,
    subtitulo VARCHAR(100),
    autores VARCHAR(100),
    descripcion TEXT,
    categoria VARCHAR(50),
    tematica VARCHAR(50),
    editorial VARCHAR(50),
    coleccion VARCHAR(50),
    edicion INT(3),
    anio_publicacion YEAR,
    pais VARCHAR(20),
    idioma VARCHAR(20),
    ubicacion VARCHAR(10) NOT NULL
);

INSERT INTO libros (isbn, titulo, subtitulo, autores, descripcion, categoria, tematica, editorial, coleccion, edicion, anio_publicacion, pais, idioma, ubicacion)
VALUES 
    ('970-07-7235-7', 'La justicia constitucional en las entidades federativas', '', 'Manuel González Oropeza y Eduardo Ferrer Mac-Gregor',
	'Doctrina', 'Derecho', '', 'Editorial Porrúa', '', 1, 2006, 'México', 'Español', 'K0001'),
    ('970-07-0965-5', 'El juicio de amparo', '', 'Ignacio Burgoa O.', 
	'Doctrina', 'Derecho', 'Amparo', 'Editorial Porrúa', '', 33, 1997, 'México', 'Español', 'K0002'),
    ('978-84-1056-734-4', 'Tratado sobre principios registrales', '', 'Francisco José Visoso Del Valle', 
	'Doctrina', 'Derecho', '', 'Editorial Tirant lo Blanch', '', 1, 2024, 'México', 'Español', 'K0003'),
    ('978-607-09-2990-8', 'Derecho Civil', 'Obligaciones', 'Jorge Alfredo Domínguez Martínez',
	'Doctrina', 'Derecho', 'Derecho Civil', 'Editorial Porrúa', 'Derecho Civil', 1, 2018, 'México', 'Español', 'K0004'),
    ('978-970-07-7721-4', 'Fraude Procesal', '', 'Raúl F. Cárdenas Rioseco',
	'Doctrina', 'Derecho', '', 'Editorial Porrúa', '', 1, 2008, 'México', 'Español', 'K0005'),
    ('978-607-09-4502-1', 'El delito de despojo', '', 'Víctor Oléa Peláez',
	'Doctrina', 'Derecho', '', 'Editorial Porrúa', '', 1, 2025, 'México', 'Español', 'K0006'),
    ('0-651637-574916', 'Colección Fiscal 2025', '', '',
	'Ley', 'Derecho', '', 'Lechuga y Bolaños Editores', '', 3, 2025, 'México', 'Español', 'K0007'),
    ('978-607-541-585-7', 'Agenda de seguridad pública 2025', '', '',
	'Ley', 'Derecho', '', 'Editorial ISEF', '', 1, 2025, 'México', 'Español', 'K0008');
