import mysql.connector

class Libro:
    def __init__(self, isbn, titulo, descripcion, editorial, coleccion, edicion, anio, pais, idioma, ubicacion):
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
            libro = Libro(*row)
            libros[libro.isbn] = libro
        return libros

    def agregar_libro(self, libro):
        self.libros[libro.isbn] = libro
        self.cursor.execute(
            "INSERT INTO Libros VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (libro.isbn, libro.titulo, libro.descripcion, libro.editorial, libro.coleccion, 
             libro.edicion, libro.anio, libro.pais, libro.idioma, libro.ubicacion)
        )
        self.conexion.commit()

    def modificar_libro(self, isbn, **datos):
        if isbn in self.libros:
            for clave, valor in datos.items():
                setattr(self.libros[isbn], clave, valor)
            set_clause = ", ".join([f"{k}=%s" for k in datos.keys()])
            query = f"UPDATE Libros SET {set_clause} WHERE isbn=%s"
            self.cursor.execute(query, list(datos.values()) + [isbn])
            self.conexion.commit()

    def eliminar_libro(self, isbn):
        if isbn in self.libros:
            del self.libros[isbn]
            self.cursor.execute("DELETE FROM Libros WHERE isbn=%s", (isbn,))
            self.conexion.commit()
    
    def cerrar(self):
        self.conexion.close()

def menu():
    biblioteca = Biblioteca("localhost", "usuario", "contraseña", "biblioteca")
    while True:
        print("\nMenú de Biblioteca")
        print("1. Agregar libro")
        print("2. Modificar libro")
        print("3. Eliminar libro")
        print("4. Mostrar libros")
        print("5. Salir")
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
            libro_nuevo = Libro(isbn, titulo, descripcion, editorial, coleccion, edicion, anio, pais, idioma, ubicacion)
            biblioteca.agregar_libro(libro_nuevo)
            print("Libro agregado exitosamente.")
        
        elif opcion == "2":
            isbn = input("ISBN del libro a modificar: ")
            if isbn in biblioteca.libros:
                print("Deje en blanco si no desea modificar un campo.")
                nuevos_datos = {}
                for campo in ["titulo", "descripcion", "editorial", "coleccion", "edicion", "anio", "pais", "idioma", "ubicacion"]:
                    valor = input(f"{campo.capitalize()}: ")
                    if valor:
                        nuevos_datos[campo] = int(valor) if campo == "anio" else valor
                biblioteca.modificar_libro(isbn, **nuevos_datos)
                print("Libro modificado exitosamente.")
            else:
                print("Libro no encontrado.")
        
        elif opcion == "3":
            isbn = input("ISBN del libro a eliminar: ")
            biblioteca.eliminar_libro(isbn)
            print("Libro eliminado exitosamente.")
        
        elif opcion == "4":
            for libro in biblioteca.libros.values():
                print(f"{libro.isbn} - {libro.titulo} ({libro.anio})")
        
        elif opcion == "5":
            biblioteca.cerrar()
            print("Saliendo del programa...")
            break
        else:
            print("Opción no válida. Intente nuevamente.")

if __name__ == "__main__":
    menu()

