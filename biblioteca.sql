-- Crear la base de datos
CREATE DATABASE IF NOT EXISTS biblioteca;

-- Usar la base de datos
USE biblioteca;

-- Tabla de Autores
CREATE TABLE Autores (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL
);

-- Tabla de Libros
CREATE TABLE Libros (
    isbn CHAR(13) PRIMARY KEY,
    titulo VARCHAR(255) NOT NULL,
    descripcion TEXT,
    editorial VARCHAR(100),
    coleccion VARCHAR(100),
    edicion VARCHAR(50),
    anio_publicacion INT,
    pais VARCHAR(100),
    idioma VARCHAR(50),
    ubicacion VARCHAR(100)
);

-- Tabla de Clasificaciones
CREATE TABLE Clasificaciones (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL
);

-- Tabla de Subclasificaciones
CREATE TABLE Subclasificaciones (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    clasificacion_id INT,
    FOREIGN KEY (clasificacion_id) REFERENCES Clasificaciones(id)
);

-- Tabla intermedia para la relación muchos a muchos entre Libros y Autores
CREATE TABLE Libros_Autores (
    libro_isbn CHAR(13),
    autor_id INT,
    PRIMARY KEY (libro_isbn, autor_id),
    FOREIGN KEY (libro_isbn) REFERENCES Libros(isbn),
    FOREIGN KEY (autor_id) REFERENCES Autores(id)
);

-- Tabla intermedia para la relación muchos a muchos entre Libros y Subclasificaciones
CREATE TABLE Libros_Subclasificaciones (
    libro_isbn CHAR(13),
    subclasificacion_id INT,
    PRIMARY KEY (libro_isbn, subclasificacion_id),
    FOREIGN KEY (libro_isbn) REFERENCES Libros(isbn),
    FOREIGN KEY (subclasificacion_id) REFERENCES Subclasificaciones(id)
);
