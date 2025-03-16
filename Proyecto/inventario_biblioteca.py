import mysql.connector

class Libro:
    def __init__(self, isbn, titulo, descripcion, editorial, coleccion, edicion, anio, pais, idioma, ubicacion, autores=None, clasificaciones=None):
        self.isbn = isbn
        self.titulo = titulo
        self.descripcion = descripcion
        self.editorial = editorial
        self.coleccion = coleccion
        self.edicion = edicion
        self.anio = anio
        self.pais = pais
        self.idioma = idioma
        self.ubicacion = ubicacion
        self.autores = autores or []
        self.clasificaciones = clasificaciones or []

class Biblioteca:
    def __init__(self, host, user, password, database):
        self.conexion = mysql.connector.connect(
            host='localhost',
            user='bibliotecario',
            password='Biblio2025#',
            database='biblioteca'
        )
        self.cursor = self.conexion.cursor()
        self.libros = self.cargar_libros()
    
    def cargar_libros(self):
        self.cursor.execute("SELECT * FROM Libros")
        libros = {}
        for row in self.cursor.fetchall():
            isbn = row[0]
            autores = self.obtener_autores(isbn)
            clasificaciones = self.obtener_clasificaciones(isbn)
            libro = Libro(*row, autores, clasificaciones)
            libros[isbn] = libro
        return libros

    def obtener_autores(self, isbn):
        self.cursor.execute("""
            SELECT A.nombre, A.apellido FROM Autores A
            JOIN Libros_Autores LA ON A.id = LA.autor_id
            WHERE LA.libro_isbn = %s
        """, (isbn,))
        return [f"{nombre}, {apellido}" for nombre, apellido in self.cursor.fetchall()]

    def obtener_clasificaciones(self, isbn):
        self.cursor.execute("""
            SELECT C.nombre, S.nombre FROM Clasificaciones C
            JOIN Subclasificaciones S ON C.id = S.clasificacion_id
            JOIN Libros_Subclasificaciones LS ON S.id = LS.subclasificacion_id
            WHERE LS.libro_isbn = %s
        """, (isbn,))
        return [f"{clasificacion}, {subclasificacion}" for clasificacion, subclasificacion in self.cursor.fetchall()]

    def agregar_libro(self, libro):
        self.libros[libro.isbn] = libro
        self.cursor.execute(
            "INSERT INTO Libros VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (libro.isbn, libro.titulo, libro.descripcion, libro.editorial, libro.coleccion, 
             libro.edicion, libro.anio, libro.pais, libro.idioma, libro.ubicacion)
        )
        self.conexion.commit()
        self.agregar_autores(libro.isbn, libro.autores)
        self.agregar_clasificaciones(libro.isbn, libro.clasificaciones)

    def agregar_autores(self, isbn, autores):
        for autor in autores:
            nombre, apellido = autor.split(", ")
            self.cursor.execute("SELECT id FROM Autores WHERE nombre=%s AND apellido=%s", (nombre, apellido))
            resultado = self.cursor.fetchone()
            if resultado:
                autor_id = resultado[0]
            else:
                self.cursor.execute("INSERT INTO Autores (nombre, apellido) VALUES (%s, %s)", (nombre, apellido))
                self.conexion.commit()
                autor_id = self.cursor.lastrowid
            self.cursor.execute("INSERT IGNORE INTO Libros_Autores (libro_isbn, autor_id) VALUES (%s, %s)", (isbn, autor_id))
            self.conexion.commit()
    
    def agregar_clasificaciones(self, isbn, clasificaciones):
        for clasificacion in clasificaciones:
            clasif, subclasif = clasificacion.split(", ")
            self.cursor.execute("SELECT id FROM Clasificaciones WHERE nombre=%s", (clasif,))
            resultado = self.cursor.fetchone()
            if resultado:
                clasif_id = resultado[0]
            else:
                self.cursor.execute("INSERT INTO Clasificaciones (nombre) VALUES (%s)", (clasif,))
                self.conexion.commit()
                clasif_id = self.cursor.lastrowid
            
            self.cursor.execute("SELECT id FROM Subclasificaciones WHERE nombre=%s AND clasificacion_id=%s", (subclasif, clasif_id))
            resultado = self.cursor.fetchone()
            if resultado:
                subclasif_id = resultado[0]
            else:
                self.cursor.execute("INSERT INTO Subclasificaciones (nombre, clasificacion_id) VALUES (%s, %s)", (subclasif, clasif_id))
                self.conexion.commit()
                subclasif_id = self.cursor.lastrowid
            
            self.cursor.execute("INSERT IGNORE INTO Libros_Subclasificaciones (libro_isbn, subclasificacion_id) VALUES (%s, %s)", (isbn, subclasif_id))
            self.conexion.commit()
    
    def editar_libro(self, isbn, campo, nuevo_valor):
        self.cursor.execute(f"UPDATE Libros SET {campo} = %s WHERE isbn = %s", (nuevo_valor, isbn))
        self.conexion.commit()
    
    def eliminar_libro(self, isbn):
        self.cursor.execute("DELETE FROM Libros_Autores WHERE libro_isbn = %s", (isbn,))
        self.cursor.execute("DELETE FROM Libros_Subclasificaciones WHERE libro_isbn = %s", (isbn,))
        self.cursor.execute("DELETE FROM Libros WHERE isbn = %s", (isbn,))
        self.conexion.commit()
    
    def buscar_libro(self, campo, valor):
        self.cursor.execute(f"SELECT * FROM Libros WHERE {campo} LIKE %s", (f"%{valor}%",))
        return self.cursor.fetchall()

    def cerrar(self):
        self.conexion.close()

def menu():
    biblioteca = Biblioteca("localhost", "usuario", "contraseña", "biblioteca")
    while True:
        print("\nMenú de Biblioteca")
        print("1. Agregar libro")
        print("2. Editar libro")
        print("3. Eliminar libro")
        print("4. Buscar libro")
        print("5. Mostrar libros")
        print("6. Salir")
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            isbn = input("ISBN: ")
            titulo = input("Título: ")
            descripcion = input("Descripción: ")
            editorial = input("Editorial: ")
            coleccion = input("Colección: ")
            edicion = input("Edición: ")
            anio = int(input("Año de publicación: "))
            pais = input("País: ")
            idioma = input("Idioma: ")
            ubicacion = input("Ubicación: ")
            autores = input("Autores (nombre, apellido separados por comas y múltiples autores por puntos): ").split(". ")
            clasificaciones = input("Clasificaciones y subclasificaciones (separadas por comas y puntos para diferentes clasificaciones): ").split(". ")
            libro_nuevo = Libro(isbn, titulo, descripcion, editorial, coleccion, edicion, anio, pais, idioma, ubicacion, autores, clasificaciones)
            biblioteca.agregar_libro(libro_nuevo)
            print("Libro agregado exitosamente.")
        
        elif opcion == "2":
            isbn = input("Ingrese el ISBN del libro a editar: ")
            campo = input("Campo a editar: ")
            nuevo_valor = input("Nuevo valor: ")
            biblioteca.editar_libro(isbn, campo, nuevo_valor)
            print("Libro editado exitosamente.")
        
        elif opcion == "3":
            isbn = input("Ingrese el ISBN del libro a eliminar: ")
            biblioteca.eliminar_libro(isbn)
            print("Libro eliminado exitosamente.")
        
        elif opcion == "4":
            campo = input("Buscar por (isbn, titulo, autor, clasificacion, subclasificacion): ")
            valor = input("Ingrese el valor de búsqueda: ")
            resultados = biblioteca.buscar_libro(campo, valor)
            for libro in resultados:
                print(libro)

        elif opcion == "5":
            for libro in biblioteca.libros.values():
                print(f"{libro.isbn} - {libro.titulo} ({libro.anio})")

        elif opcion == "6":
            biblioteca.cerrar()
            print("Saliendo del programa...")
            break
        else:
            print("Opción no válida. Intente nuevamente.")

if __name__ == "__main__":
    menu()

