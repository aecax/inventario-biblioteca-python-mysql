import mysql.connector

#Se definen los atributos del objeto libro.
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

#Se definen todas las funciones para manipular los libros.
class Biblioteca:
    #Se establecen los parametros para la conexión con la base de datos y se guardan en un cursor.
    def __init__(self, host, user, password, database):
        self.conexion = mysql.connector.connect(
            host='localhost',
            user='bibliotecario',
            password='Biblio2025#',
            database='biblioteca'
        )
        self.cursor = self.conexion.cursor()
        self.libros = self.cargar_libros()
    
    #Se consulta la base de datos y se crea un objeto libro por cada libro en la base de datos. Para esto se hace uso de las funciones obtener_autores() y obtener_clasificaciones().
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
    
    #Se consulta la tabla autores y obtiene los nombre y apellidos del autor.
    def obtener_autores(self, isbn):
        self.cursor.execute("""
            SELECT A.nombre, A.apellido FROM Autores A
            JOIN Libros_Autores LA ON A.id = LA.autor_id
            WHERE LA.libro_isbn = %s
        """, (isbn,))
        return [f"{nombre}, {apellido}" for nombre, apellido in self.cursor.fetchall()]

    #Se consultan las tablas clasificaciones y subclasificaciones, y obtiene los datos correspondientes.
    def obtener_clasificaciones(self, isbn):
        self.cursor.execute("""
            SELECT C.nombre, S.nombre FROM Clasificaciones C
            JOIN Subclasificaciones S ON C.id = S.clasificacion_id
            JOIN Libros_Subclasificaciones LS ON S.id = LS.subclasificacion_id
            WHERE LS.libro_isbn = %s
        """, (isbn,))
        return [f"{clasificacion}, {subclasificacion}" for clasificacion, subclasificacion in self.cursor.fetchall()]

    #Crea un objeto libro e inserta los valores proporcionados por el usuario en la base de datos. 
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

    #Inserta el nombre del autor en la tabla autores
    def agregar_autores(self, isbn, autores):
        #Por cada autor en la tabla autores evalua si el nombre proporcionado por el usuario ya se encuentra dentro de la tabla
        for autor in autores:
            nombre, apellido = autor.split(", ")
            #Busca en la tabla Autores si el autor ya existe
            self.cursor.execute("SELECT id FROM Autores WHERE nombre=%s AND apellido=%s", (nombre, apellido))
            resultado = self.cursor.fetchone()
            #Si el autor existe entonces obtiene el id
            if resultado:
                autor_id = resultado[0]
            #Si el autor no existe entonces la crea
            else:
                self.cursor.execute("INSERT INTO Autores (nombre, apellido) VALUES (%s, %s)", (nombre, apellido))
                self.conexion.commit()
                autor_id = self.cursor.lastrowid
            self.cursor.execute("INSERT IGNORE INTO Libros_Autores (libro_isbn, autor_id) VALUES (%s, %s)", (isbn, autor_id))
            self.conexion.commit()
    
    #Inserta clasificaciones y subclasificaciones en sus respectivas tablas
    def agregar_clasificaciones(self, isbn, clasificaciones):
        for clasificacion in clasificaciones:
            clasif, subclasif = clasificacion.split(", ")
            #Busca en la tabla Clasificaciones si la clasificación ya existe
            self.cursor.execute("SELECT id FROM Clasificaciones WHERE nombre=%s", (clasif,))
            resultado = self.cursor.fetchone()
            #Si la clasificación existe entonces obtiene el id
            if resultado:
                clasif_id = resultado[0]
            #Si la clasificación no existe entonces la crea
            else:
                self.cursor.execute("INSERT INTO Clasificaciones (nombre) VALUES (%s)", (clasif,))
                self.conexion.commit()
                clasif_id = self.cursor.lastrowid
            #Busca en la tabla Subclasificaciones si la subclasificación ya existe
            self.cursor.execute("SELECT id FROM Subclasificaciones WHERE nombre=%s AND clasificacion_id=%s", (subclasif, clasif_id))
            resultado = self.cursor.fetchone()
            #Si la subclasificación existe entonces obtiene el id
            if resultado:
                subclasif_id = resultado[0]
            #Si la subclasificación no existe entonces la crea
            else:
                self.cursor.execute("INSERT INTO Subclasificaciones (nombre, clasificacion_id) VALUES (%s, %s)", (subclasif, clasif_id))
                self.conexion.commit()
                subclasif_id = self.cursor.lastrowid
            
            self.cursor.execute("INSERT IGNORE INTO Libros_Subclasificaciones (libro_isbn, subclasificacion_id) VALUES (%s, %s)", (isbn, subclasif_id))
            self.conexion.commit()

    #Actualiza un libro en la base de datos
    def editar_libro(self, isbn, campo, nuevo_valor):
        self.cursor.execute(f"UPDATE Libros SET {campo} = %s WHERE isbn = %s", (nuevo_valor, isbn))
        self.conexion.commit()

    #Elimina un libro en la base de datos
    def eliminar_libro(self, isbn):
        self.cursor.execute("DELETE FROM Libros_Autores WHERE libro_isbn = %s", (isbn,))
        self.cursor.execute("DELETE FROM Libros_Subclasificaciones WHERE libro_isbn = %s", (isbn,))
        self.cursor.execute("DELETE FROM Libros WHERE isbn = %s", (isbn,))
        self.conexion.commit()

    #Busca un libro por el campo seleccionado
    def buscar_libro(self, campo, valor):
        self.cursor.execute(f"SELECT * FROM Libros WHERE {campo} LIKE %s", (f"%{valor}%",))
        return self.cursor.fetchall()

    #Termina la conexión con la base de datos
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
            autores = input("Autores (nombre, apellido separados por comas y múltiples autores por puntos): ").split(". ")
            descripcion = input("Descripción: ")
            editorial = input("Editorial: ")
            coleccion = input("Colección: ")
            clasificaciones = input("Clasificaciones y subclasificaciones (separadas por comas y puntos para diferentes clasificaciones): ").split(". ")
            edicion = input("Edición: ")
            anio = int(input("Año de publicación: "))
            pais = input("País: ")
            idioma = input("Idioma: ")
            ubicacion = input("Ubicación: ")
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

