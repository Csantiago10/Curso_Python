import json
import uuid

# ==============================
# CONFIGURACIÓN Y CONSTANTES
# ==============================
RED = "\033[91m"
GREEN = "\033[92m"
BLUE = "\033[94m"
RESET = "\033[0m"
ARCHIVO_DB = "biblioteca.json"

# ==============================
# CLASE LIBRO
# ==============================
class Libro:
    def __init__(self, nombre: str, categoria: str, autor: str, editorial: str, paginas: int, cantidad: int, id: str = None):
        
        #Si me pasan un id, lo uso; si no, genero uno nuevo
        self.id = id if id else str(uuid.uuid4())

        self.nombre = nombre
        self.categoria = categoria
        self.autor = autor
        self.editorial = editorial
        self.paginas = paginas
        self.id = id if id is not None else str(uuid.uuid4())
        self.cantidad = cantidad

    def mostrar_info(self):
        return (self.nombre, self.autor, self.editorial, self.categoria, self.paginas, self.cantidad, self.id)

# ==============================
# VARIABLES GLOBALES
# ==============================
biblioteca = []

# ==============================
# LÓGICA DE NEGOCIO (Backend)
# ==============================
def sanitizar_biblioteca():
    global biblioteca
    diccionario_unico = {}
    duplicados = 0
    
    # print(f"{BLUE}Verificando integridad...{RESET}") # Comentado para no molestar tanto
    for libro in biblioteca:
        clave = f"{libro.nombre.lower().strip()}|{libro.editorial.lower().strip()}"
        if clave in diccionario_unico:
            diccionario_unico[clave].cantidad += libro.cantidad
            duplicados += 1
        else:
            diccionario_unico[clave] = libro
            
    if duplicados > 0:
        biblioteca = list(diccionario_unico.values())
        print(f"{GREEN}Limpieza: {duplicados} libros fusionados.{RESET}")
        guardar_biblioteca()

# ### NUEVO: FUNCIÓN MAESTRA DE BÚSQUEDA ###
def filtrar_libros(criterio: str, valor_busqueda: str) -> list[Libro]:
    """
    Busca libros según un criterio específico.
    criterio: '1' (Nombre), '2' (Categoría), '3' (Editorial)
    """
    valor_busqueda = valor_busqueda.lower().strip()
    resultados = []

    for libro in biblioteca:
        coincidencia = False
        # Aquí decidimos "dónde alumbrar con la linterna"
        if criterio == "1": # Nombre
            if valor_busqueda in libro.nombre.lower(): coincidencia = True
        elif criterio == "2": # Categoría
            if valor_busqueda in libro.categoria.lower(): coincidencia = True
        elif criterio == "3": # Editorial
            if valor_busqueda in libro.editorial.lower(): coincidencia = True
        
        if coincidencia:
            resultados.append(libro)
            
    return resultados

# ### NUEVO: BUSCADOR DE UN SOLO LIBRO (Para eliminar/editar) ###
def buscar_libro_exacto(nombre: str) -> Libro | None:
    """Retorna el OBJETO libro si lo encuentra por nombre exacto (o parecido)."""
    for libro in biblioteca:
        if libro.nombre.lower() == nombre.lower().strip():
            return libro
    return None

# ### NUEVO: ACTUALIZAR STOCK ###
def actualizar_stock(libro: Libro, nueva_cantidad: int) -> bool:
    """
    Actualiza el stock de un libro sumando o restando cantidad.
    nueva_cantidad puede ser positiva (suma) o negativa (resta).
    Retorna True si se actualizó correctamente, False si quedaría negativo.
    """
    if libro.cantidad + nueva_cantidad >= 0:
        libro.cantidad += nueva_cantidad
        return True
    else:
        return False
    
def buscar_libro_unico(nombre: str, editorial: str) -> Libro | None:
    """
    Busca un libro específico coincidiendo Nombre Y Editorial.
    Es necesario para eliminar o modificar sin errores.
    """
    nombre_busqueda = nombre.lower().strip()
    editorial_busqueda = editorial.lower().strip()

    for libro in biblioteca:
        # Verificamos las DOS condiciones
        if (libro.nombre.lower().strip() == nombre_busqueda and 
            libro.editorial.lower().strip() == editorial_busqueda):
            return libro # ¡Encontrado el exacto!
            
    return None # No existe esa combinación

# ==============================
# PERSISTENCIA
# ==============================
def guardar_biblioteca():
    lista_datos = [libro.__dict__ for libro in biblioteca]
    try:
        with open(ARCHIVO_DB, "w", encoding="utf-8") as archivo:
            json.dump(lista_datos, archivo, indent=4)
        # print(f"{GREEN}Guardado exitoso.{RESET}") # Comentado para limpiar consola
    except Exception as e:
        print(f"{RED}Error guardando: {e}{RESET}")

def cargar_biblioteca() -> list[Libro]:
    try:
        with open(ARCHIVO_DB, "r", encoding="utf-8") as archivo:
            datos = json.load(archivo)
            return [Libro(**d) for d in datos]
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []

# ==============================
# INTERFAZ DE USUARIO (Frontend)
# ==============================
def obtener_datos_libro() -> tuple:
    print(f"\n{BLUE}--- Nuevo Libro ---{RESET}")
    while True:
        nombre = input("Nombre: ").strip()
        if nombre:
            break
        print("El nombre no puede estar vacío.")

    while True:        
        categoria = input("Categoría: ").strip()
        if categoria:
            break
        print("La categoría no puede estar vacía.")

    while True:
        autor = input("Autor: ").strip()
        if autor:
            break
        print("El autor no puede estar vacío.")

    while True:
        editorial = input("Editorial: ").strip()
        if editorial:
            break
        print("La editorial no puede estar vacía.")

    while True:
        try:
            paginas = int(input("Páginas: "))
            cantidad = int(input("Cantidad: "))
            if paginas > 0 and cantidad >= 0: break
            print("Valores deben ser positivos.")
        except ValueError:
            print("Ingrese números enteros.")
            
    return (nombre, categoria, autor, editorial, paginas, cantidad)

def mostrar_resultados_tabla(lista_libros: list[Libro]):
    """Función auxiliar para imprimir tablas bonitas sin repetir código"""
    if not lista_libros:
        print(f"{RED}No se encontraron libros.{RESET}")
        return

    print(f"\n{'TÍTULO':<35} | {'AUTOR':<15} | {'CATEGORÍA':<15} | {'EDITORIAL':<15} | {'PÁGINAS':<10} | {'STOCK':<5}  |")
    print("-" * 115)
    for libro in lista_libros:
        print(f"{libro.nombre:<35} | {libro.autor:<15} | {libro.categoria:<15} | {libro.editorial:<15} | {libro.paginas:<10} | {libro.cantidad:<5} |")
    print("-" * 115)

def mostrar_menu() -> str:
    print("\n" + "="*30)
    print("      📚 BIBLIOTECA")
    print("-" * 30)
    print("1. Registrar libro")
    print("2. Ver catálogo completo")
    print("3. Búsqueda Avanzada (Filtros)") # <--- MEJORADO
    print("4. Modificar Stock")             # <--- NUEVO
    print("5. Eliminar Libro")              # <--- NUEVO
    print("6. Guardar y Salir")
    print("="*30)
    return input(">>> Opción: ")

def ejecutar_opcion(opcion: str) -> bool:
    if opcion == "1":
        datos = obtener_datos_libro()
        biblioteca.append(Libro(*datos))
        print(f"{GREEN}Registrado.{RESET}")

    elif opcion == "2":
        mostrar_resultados_tabla(biblioteca)

    # ### NUEVO: LÓGICA DE FILTRADO ###
    elif opcion == "3":
        print(f"\n{BLUE}¿Por qué criterio desea filtrar?{RESET}")
        print("1. Título")
        print("2. Categoría")
        print("3. Editorial")
        sub_opcion = input(">>> Elija (1-3): ")
        
        if sub_opcion in ["1", "2", "3"]:
            termino = input("Ingrese el término a buscar: ")
            resultados = filtrar_libros(sub_opcion, termino)
            mostrar_resultados_tabla(resultados)
        else:
            print(f"{RED}Opción de filtro no válida.{RESET}")

    # ### NUEVO: MODIFICAR STOCK ###
    elif opcion == "4":
        nombre_buscar = input("Ingrese el nombre exacto del libro: ")
        libro_encontrado = buscar_libro_exacto(nombre_buscar)
        
        if libro_encontrado:
            print(f"Libro: {libro_encontrado.nombre} | Stock Actual: {libro_encontrado.cantidad}")
            print("\n1. Establecer stock a una cantidad específica")
            print("2. Añadir/Restar cantidad")
            sub_opcion = input(">>> Elige (1-2): ")
            
            try:
                if sub_opcion == "1":
                    nuevo_stock = int(input("Ingrese la NUEVA cantidad total: "))
                    if nuevo_stock >= 0:
                        libro_encontrado.cantidad = nuevo_stock
                        print(f"{GREEN}Stock actualizado a {nuevo_stock}.{RESET}")
                    else:
                        print(f"{RED}El stock no puede ser negativo.{RESET}")
                        
                elif sub_opcion == "2":
                    cambio = int(input("Ingrese cantidad a sumar (positivo) o restar (negativo): "))
                    if actualizar_stock(libro_encontrado, cambio):
                        print(f"{GREEN}Stock actualizado. Nuevo stock: {libro_encontrado.cantidad}{RESET}")
                    else:
                        print(f"{RED}Error: El stock no puede ser negativo.{RESET}")
                else:
                    print(f"{RED}Opción no válida.{RESET}")
                    
            except ValueError:
                print(f"{RED}Error: Ingrese un número.{RESET}")
        else:
            print(f"{RED}Libro no encontrado.{RESET}")

    # --- OPCIÓN 5: ELIMINAR LIBRO (CORREGIDO) ---
    elif opcion == "5":
        print(f"\n{RED}--- Eliminar Libro ---{RESET}")
        print("Para eliminar, necesitamos identificar el libro exacto.")
        
        nombre_buscar = input("Ingrese el nombre del libro: ")
        editorial_buscar = input("Ingrese la editorial del libro: ") # <--- Nuevo Input
        
        # Usamos la nueva función precisa
        libro_encontrado = buscar_libro_unico(nombre_buscar, editorial_buscar)
        
        if libro_encontrado:
            print(f"\n{RED}¡ADVERTENCIA! Va a eliminar:{RESET}")
            print(f"- Título: {libro_encontrado.nombre}")
            print(f"- Editorial: {libro_encontrado.editorial}")
            print(f"- Stock actual: {libro_encontrado.cantidad}")
            
            confirmar = input("¿Está seguro de borrarlo permanentemente? (si/no): ").lower()
            
            if confirmar == "si":
                biblioteca.remove(libro_encontrado)
                print(f"{GREEN}Libro eliminado exitosamente.{RESET}")
            else:
                print(f"{BLUE}Operación cancelada.{RESET}")
        else:
            print(f"{RED}Error: No se encontró un libro con ese Nombre y esa Editorial.{RESET}")

    elif opcion == "6":
        sanitizar_biblioteca()
        guardar_biblioteca()
        print("¡Adiós!")
        return False

    else:
        print("Opción no válida.")
    
    return True

# ==============================
# MAIN
# ==============================
def main():
    global biblioteca
    biblioteca = cargar_biblioteca()
    sanitizar_biblioteca()
    
    ejecutando = True
    while ejecutando:
        opcion = mostrar_menu()
        ejecutando = ejecutar_opcion(opcion)

if __name__ == "__main__":
    main()