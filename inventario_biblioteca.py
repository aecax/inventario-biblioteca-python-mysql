import mysql.connector
import re

class Libro:
    def __init__(self, isbn, titulo, descripcion, editorial, coleccion, edicion, anio_publicacion, pais, idioma, ubicacion, autores=None, subclasificaciones=None):
        self.isbn = isbn
        self.titulo = titulo
        self.descripcion = descripcion
        self.editorial = editorial
        self.coleccion = coleccion
        self.edicion = edicion
        self.anio_publicacion = anio_publicacion
        self.pais = pais
        self.idioma = idioma
        self.ubicacion = ubicacion
        self.autores = autores or []
        self.subclasificaciones = subclasificaciones or []

    def __str__(self):
        return (f"ISBN: {self.isbn}, Título: {self.titulo}, Autores: {', '.join(self.autores)}, "
                f"Descripción: {self.descripcion}, Subclasificaciones: {', '.join(self.subclasificaciones)}, "
                f"Editorial: {self.editorial}, Colección: {self.coleccion}, Edición: {self.edicion}, "
                f"Año: {self.anio_publicacion}, País: {self.pais}, Idioma: {self.idioma}, "
                f"Ubicación: {self.ubicacion}")

class Biblioteca:
    def __init__(self):
        self.conexion = mysql.connector.connect(
            host='localhost',
            user='bibliotecario',
            password='Biblio2025#',
            database='biblioteca'
        )
        self.cursor = self.conexion.cursor()
        self.libros = {}

    def cargar_libros(self):
        sql = "SELECT * FROM Libros"
        self.cursor.execute(sql)
        libros_data = self.cursor.fetchall()

        for libro_data in libros_data:
            isbn = libro_data[0]
            titulo = libro_data[1]
            descripcion = libro_data[2]
            editorial = libro_data[3]
            coleccion = libro_data[4]
            edicion = libro_data[5]
            anio_publicacion = libro_data[6]
            pais = libro_data[7]
            idioma = libro_data[8]
            ubicacion = libro_data[9]

            # Obtener autores
            self.cursor.execute("SELECT a.nombre, a.apellido FROM Autores a "
                                "JOIN Libros_Autores la ON a.id = la.autor_id "
                                "WHERE la.libro_isbn = %s", (isbn,))
            autores = [f"{nombre} {apellido}" for nombre, apellido in self.cursor.fetchall()]

            # Obtener subclasificaciones
            self.cursor.execute("SELECT s.nombre FROM Subclasificaciones s "
                                "JOIN Libros_Subclasificaciones ls ON s.id = ls.subclasificacion_id "
                                "WHERE ls.libro_isbn = %s", (isbn,))
            subclasificaciones = [nombre for (nombre,) in self.cursor.fetchall()]

            # Crear objeto Libro y almacenarlo en memoria
            libro = Libro(isbn, titulo, descripcion, editorial, coleccion, edicion, anio_publicacion, pais, idioma, ubicacion, autores, subclasificaciones)
            self.libros[isbn] = libro

    def validar_isbn(self, isbn):
        return re.match(r'^\d{10}$', isbn) or re.match(r'^\d{13}$', isbn)

    def convertir_isbn_10_a_13(self, isbn):
        if len(isbn) == 10:
            isbn = '978' + isbn[:-1]  # Añadir el prefijo 978
            suma = 0
            for i, digit in enumerate(isbn):
                if i % 2 == 0:
                    suma += int(digit)
                else:
                    suma += int(digit) * 3
            digito_control = (10 - (suma % 10)) % 10
            return isbn + str(digito_control)
        return isbn

    def validar_datos(self, libro):
        if not isinstance(libro.titulo, str) or not libro.titulo.strip():
            raise ValueError("El título no puede estar vacío.")
        if not isinstance(libro.descripcion, str):
            raise ValueError("La descripción debe ser una cadena.")
        if not isinstance(libro.editorial, str) or not libro.editorial.strip():
            raise ValueError("La editorial no puede estar vacía.")
        if not isinstance(libro.coleccion, str):
            raise ValueError("La colección debe ser una cadena.")
        if not isinstance(libro .edicion, str):
            raise ValueError("La edición debe ser una cadena.")
        if not isinstance(libro.anio_publicacion, int) or libro.anio_publicacion < 0:
            raise ValueError("El año de publicación debe ser un número positivo.")
        if not isinstance(libro.pais, str) or not libro.pais.strip():
            raise ValueError("El país no puede estar vacío.")
        if not isinstance(libro.idioma, str) or not libro.idioma.strip():
            raise ValueError("El idioma no puede estar vacío.")
        if not isinstance(libro.ubicacion, str) or not libro.ubicacion.strip():
            raise ValueError("La ubicación no puede estar vacía.")

    def guardar_libro_en_db(self, libro):
        sql = """INSERT INTO Libros (isbn, titulo, descripcion, editorial, coleccion, edicion, anio_publicacion, pais, idioma, ubicacion)
                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        self.cursor.execute(sql, (libro.isbn, libro.titulo, libro.descripcion, libro.editorial, libro.coleccion,
                                   libro.edicion, libro.anio_publicacion, libro.pais, libro.idioma, libro.ubicacion))
        self.conexion.commit()

    def añadir_libro(self, libro):
        try:
            self.validar_datos(libro)
            if self.validar_isbn(libro.isbn):
                if len(libro.isbn) == 10:
                    libro.isbn = self.convertir_isbn_10_a_13(libro.isbn)
                self.libros[libro.isbn] = libro
                self.guardar_libro_en_db(libro)
            else:
                print("El ISBN debe ser un número de 10 o 13 dígitos.")
        except ValueError as e:
            print(f"Error al añadir el libro: {e}")

    def mostrar_menu(self):
        while True:
            print("\n--- Menú de Biblioteca ---")
            print("1. Añadir libro")
            print("2. Buscar libro")
            print("3. Editar libro")
            print("4. Eliminar libro")
            print("5. Salir")
            opcion = input("Selecciona una opción: ")

            if opcion == '1':
                self.añadir_libro_interactivo()
            elif opcion == '2':
                self.buscar_libro_interactivo()
            elif opcion == '3':
                self.editar_libro_interactivo()
            elif opcion == '4':
                self.eliminar_libro_interactivo()
            elif opcion == '5':
                self.cerrar_conexion()
                break
            else:
                print("Opción no válida. Intenta de nuevo.")

    def añadir_libro_interactivo(self):
        isbn = input("Ingrese el ISBN: ")
        titulo = input("Ingrese el título: ")
        descripcion = input("Ingrese la descripción: ")
        editorial = input("Ingrese la editorial: ")
        coleccion = input("Ingrese la colección: ")
        edicion = input("Ingrese la edición: ")
        anio_publicacion = int(input("Ingrese el año de publicación: "))
        pais = input("Ingrese el país: ")
        idioma = input("Ingrese el idioma: ")
        ubicacion = input("Ingrese la ubicación: ")

        nuevo_libro = Libro(isbn, titulo, descripcion, editorial, coleccion, edicion, anio_publicacion, pais, idioma, ubicacion)
        self.añadir_libro(nuevo_libro)

    def buscar_libro_interactivo(self):
        isbn = input("Ingrese el ISBN del libro a buscar: ")
        libro = self.libros.get(isbn)
        if libro:
            print(libro)
        else:
            print("Libro no encontrado.")

    def editar_libro_interactivo(self):
        isbn = input("Ingrese el ISBN del libro a editar: ")
        libro = self.libros.get(isbn)
        if libro:
            print("Ingrese los nuevos datos (deje en blanco para no cambiar):")
            nuevo_titulo = input(f"Título ({libro.titulo}): ") or libro.titulo
            nuevo_descripcion = input(f"Descripción ({libro.descripcion}): ") or libro.descripcion
            nuevo_editorial = input(f"Editorial ({libro.editorial}): ") or libro.editorial
            nuevo_coleccion = input(f"Colección ({libro.coleccion}): ") or libro.coleccion
            nuevo_edicion = input(f"Edición ({libro.edicion}): ") or libro.edicion
            nuevo_anio_publicacion = input(f"Año de publicación ({libro.anio_publicacion}): ") or libro.anio_publicacion
            nuevo_pais = input(f"País ({libro.pais}): ") or libro.pais
            nuevo_idioma = input(f"Idioma ({libro.idioma}): ") or libro.idioma
            nueva_ubicacion = input(f"Ubicación ({libro.ubicacion}): ") or libro.ubicacion

            libro.titulo = nuevo_titulo
            libro.descripcion = nuevo_descripcion
            libro.editorial = nuevo_editorial
            libro.coleccion = nuevo_coleccion
            libro.edicion = nuevo_edicion
            libro.anio_publicacion = int(nuevo_anio_publicacion) if nuevo_anio_publicacion else libro.anio_publicacion
            libro.pais = nuevo_pais
            libro.idioma = nuevo_idioma
            libro.ubicacion = nueva_ubicacion

            self.guardar_libro_en_db(libro)
            print("Libro actualizado.")
        else:
            print("Libro no encontrado.")

    def eliminar_libro_interactivo(self):
        isbn = input("Ingrese el ISBN del libro a eliminar: ")
        if isbn in self.libros:
            del self.libros[isbn]
            sql = "DELETE FROM Libros WHERE isbn = %s"
            self.cursor.execute(sql, (isbn,))
            self.conexion.commit()
            print("Libro eliminado.")
        else:
            print("Libro no encontrado.")

# Ejecución del menú
biblioteca = Biblioteca()
biblioteca.cargar_libros()
biblioteca.mostrar_menu()
