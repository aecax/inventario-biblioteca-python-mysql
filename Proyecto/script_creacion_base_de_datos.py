import mysql.connector

def crear_base_datos():
    conexion = mysql.connector.connect(
        host="",
        user="",
        password=""
    )
    cursor = conexion.cursor()
    
    cursor.execute("CREATE DATABASE IF NOT EXISTS biblioteca;")
    cursor.execute("CREATE USER IF NOT EXISTS 'bibliotecario'@'localhost' IDENTIFIED BY 'Biblio2025#';")
    cursor.execute("GRANT ALL PRIVILEGES ON biblioteca.* TO 'bibliotecario'@'localhost';")
    cursor.execute("FLUSH PRIVILEGES;")
    
    conexion.commit()
    cursor.close()
    conexion.close()

def crear_tablas():
    conexion = mysql.connector.connect(
        host="localhost",
        user="bibliotecario",
        password="Biblio2025#",
        database="biblioteca"
    )
    cursor = conexion.cursor()
    
    tablas_sql = [
        """
        CREATE TABLE IF NOT EXISTS Autores (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nombre VARCHAR(100) NOT NULL,
            apellido VARCHAR(100) NOT NULL
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS Libros (
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
        """,
        """
        CREATE TABLE IF NOT EXISTS Clasificaciones (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nombre VARCHAR(100) NOT NULL
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS Subclasificaciones (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nombre VARCHAR(100) NOT NULL,
            clasificacion_id INT,
            FOREIGN KEY (clasificacion_id) REFERENCES Clasificaciones(id)
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS Libros_Autores (
            libro_isbn CHAR(13),
            autor_id INT,
            PRIMARY KEY (libro_isbn, autor_id),
            FOREIGN KEY (libro_isbn) REFERENCES Libros(isbn),
            FOREIGN KEY (autor_id) REFERENCES Autores(id)
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS Libros_Subclasificaciones (
            libro_isbn CHAR(13),
            subclasificacion_id INT,
            PRIMARY KEY (libro_isbn, subclasificacion_id),
            FOREIGN KEY (libro_isbn) REFERENCES Libros(isbn),
            FOREIGN KEY (subclasificacion_id) REFERENCES Subclasificaciones(id)
        );
        """
    ]
    
    for tabla in tablas_sql:
        cursor.execute(tabla)
    
    conexion.commit()
    cursor.close()
    conexion.close()

def main():
    crear_base_datos()
    crear_tablas()
    print("Base de datos y tablas creadas exitosamente.")

if __name__ == "__main__":
    main()

