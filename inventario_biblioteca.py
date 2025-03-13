import mysql.connector

class Libro:
    def __init__(self, isbn, titulo, ubicacion, subtitulo=None, autores=None, descripcion=None, categoria=None,
                 tematica=None, editorial=None, coleccion=None, edicion=None, anio_publicacion=None,
                 pais=None, idioma=None):
        self.isbn = isbn
        self.titulo = titulo
        self.subtitulo = subtitulo
        self.autores = autores
        self.descripcion = descripcion
        self.categoria = categoria
        self.tematica = tematica
        self.editorial = editorial
        self.coleccion = coleccion
        self.edicion = edicion
        self.anio_publicacion = anio_publicacion
        self.pais = pais
        self.idioma = idioma
        self.ubicacion = ubicacion


class BDBiblioteca:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host='localhost',
            user='bibliotecario',
            password='Biblio2025#',
            database='biblioteca'
        )
        self.cursor = self.conn.cursor()

    def consultar_libros(self):
        sql = "SELECT * FROM libros"
        self.cursor.execute(sql)
        libros = self.cursor.fetchall()
        for libro in libros:
            print(libro)

    def terminar_conexion(self):
        self.cursor.close()
        self.conn.close()

if __name__ == '__main__':
    bd = BDBiblioteca()
    while True:
        print("\n--- Gestión de Libros ---")
        print("1. Busca un libro")
        print("2. Añade un libro")
        print("3. Edita un libro")
        print("4. Elimina un libro")
        print("5. Mostrar todos los libros")
        print("6. Salir")
        opcion = input("Selecciona una opción: ")

        if opcion == '1':
            bd.terminar_conexion()
            print("Conexión cerrada. Adiós!")
            break

        elif opcion == '2':
            bd.terminar_conexion()
            print("Conexión cerrada. Adiós!")
            break

        elif opcion == '3':
            bd.terminar_conexion()
            print("Conexión cerrada. Adiós!")
            break

        elif opcion == '4':
            bd.terminar_conexion()
            print("Conexión cerrada. Adiós!")
            break

        elif opcion == '5':
            bd.consultar_libros()

        elif opcion == '6':
            bd.terminar_conexion()
            print("Conexión cerrada. Adiós!")
            break

        else:
            print("Opción no válida. Inténtalo de nuevo.")
