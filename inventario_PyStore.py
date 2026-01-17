import json


# ==========================================
# CONFIGURACIÓN DE ESTILO (Colores ANSI)
# ==========================================
VERDE = '\033[92m'
ROJO = '\033[91m'
BLUE = '\033[94m'
RESET = '\033[0m'  # Restablece el color de la consola

# ==========================================
# FUNCIONES AUXILIARES
# ==========================================
def formato_pesos_colombianos(precio):
    """Formatea un número como pesos colombianos: $1.234.567,89"""
    texto = f"${precio:,.2f}"
    return texto.replace(",", "_").replace(".", ",").replace("_", ".")

# ==========================================
# CLASES (Modelos de Datos)
# ==========================================
class Producto:
    """Clase que representa un producto individual en el almacén."""
    
    def __init__(self, nombre, precio, cantidad):
        self.nombre = nombre
        self.precio = precio
        self.cantidad = cantidad

    def mostrar_info(self):
        """Devuelve una tupla con los datos del producto para formato tabla."""
        return (self.nombre, formato_pesos_colombianos(self.precio), self.cantidad)
    
    def actualizar_stock(self, cantidad_cambio):
        """
        Modifica el stock. 
        Recibe: cantidad_cambio (int). Positivo para comprar, negativo para vender.
        Retorna: True si la operación fue exitosa, False si no hay stock suficiente.
        """
        if self.cantidad + cantidad_cambio < 0:
            return False  # Validación de negocio: No stock negativo
        self.cantidad += cantidad_cambio
        return True

# ==========================================
# FUNCIONES DE PERSISTENCIA (Manejo de Archivos)
# ==========================================
def guardar_datos():
    """Serializa la lista de objetos a JSON y la guarda en disco."""
    
    # 1. Transformación (RAM): Convertimos Objetos -> Lista de Diccionarios
    # Optimizamos: Creamos la lista en memoria ANTES de abrir el archivo.
    lista_datos = []
    for item in inventario:
        lista_datos.append({
            "nombre": item.nombre, 
            "precio": item.precio, 
            "cantidad": item.cantidad
        })
    
    # 2. Escritura (Disco): Abrimos el archivo solo el tiempo necesario
    try:
        with open("inventario.json", "w") as archivo:
            json.dump(lista_datos, archivo, indent=4) # indent=4 lo hace legible para humanos
        print(f"\n{VERDE}Datos guardados exitosamente en 'inventario.json'.{RESET}")
    except Exception as e:
        print(f"{ROJO}Error al guardar datos: {e}{RESET}")

def cargar_datos():
    """Lee el JSON del disco y reconstruye los objetos en memoria."""
    try:
        with open("inventario.json", "r") as archivo:
            lista_datos = json.load(archivo) # Carga la lista de diccionarios
            
            for dato in lista_datos:
                # Reconstrucción: Diccionario -> Objeto Producto
                prod = Producto(dato["nombre"], dato["precio"], dato["cantidad"])
                inventario.append(prod)
        print(f"{VERDE}Datos cargados exitosamente desde 'inventario.json'{RESET}")
    
    except FileNotFoundError:
        # Esto es normal la primera vez que se ejecuta el programa
        print(f"{BLUE}Archivo 'inventario.json' no encontrado. Iniciando con inventario vacío.{RESET}")
    except json.JSONDecodeError:
        print(f"{ROJO}Error: El archivo de datos está corrupto.{RESET}")

# ==========================================
# INICIO DEL SISTEMA
# ==========================================
inventario = [] # Base de datos en memoria (RAM)

# Cargar datos al arrancar (Recuperar memoria)
cargar_datos()

# ==========================================
# BUCLE PRINCIPAL (Interfaz de Usuario)
# ==========================================
while True:
    print("\n" + "="*30)
    print("      MENÚ INVENTARIO")
    print("-"*30)
    print("1. Registrar nuevo producto")
    print("2. Ver Inventario")
    print("3. Actualizar Stock de un Producto")
    print("4. Salir")
    print("="*30)

    menu_principal = input(">>> Selecciona una opción (1-4): ")

    # --- OPCIÓN 1: CREAR (Create) ---
    if menu_principal == "1":
        nombre = input("Ingrese el nombre del producto: ")
        
        # Validación de Precio
        while True:
            try:
                precio = float(input("Ingrese el precio del producto: "))
                if precio >= 0:
                    break
                else:
                    print("Por favor, ingrese un precio válido (mayor o igual a 0).")
            except ValueError:
                print("Entrada inválida. Por favor, ingrese un número válido.")
                continue

        # Validación de Cantidad
        while True:
            try:
                cantidad = int(input("Ingrese la cantidad del producto: "))
                if cantidad >= 0:
                    break
                else:
                    print("Por favor, ingrese una cantidad válida (mayor o igual a 0).")
            except ValueError:
                print("Entrada inválida. Por favor, ingrese un número entero.")
                continue

        # Instancia y guardado en RAM
        nuevo_producto = Producto(nombre, precio, cantidad)
        inventario.append(nuevo_producto)
        print(f"Producto registrado exitosamente.")

    # --- OPCIÓN 2: LEER (Read) ---
    elif menu_principal == "2":
        if not inventario:
            print("El inventario está vacío.")
        else:
            print("\n" + "="*60)
            print("                            INVENTARIO")
            print("="*60)
            print(f"{'Producto':<20} | {'Precio':<12} | {'Cantidad':<10}")
            print("-"*60)
            for item in inventario:
                nombre, precio, cantidad = item.mostrar_info()
                print(f"{nombre:<20} | {precio:<12} | {cantidad:<10}")
            print("="*60)

    # --- OPCIÓN 3: ACTUALIZAR (Update) ---
    elif menu_principal == "3":
        nombre_buscar = input("Ingrese el nombre del producto a actualizar: ")
        producto_encontrado = None
        
        # Búsqueda Lineal
        for item in inventario:
            if item.nombre.lower() == nombre_buscar.lower():
                producto_encontrado = item
                nombre, precio, cantidad = producto_encontrado.mostrar_info()
                print(f"\nProducto encontrado:")
                print(f"{'Nombre':<15}: {nombre}")
                print(f"{'Precio':<15}: {precio}")
                print(f"{'Cantidad':<15}: {cantidad}")

                while True:
                    try:
                        cambio = int(input("Ingrese la cantidad a agregar (positivo) o vender (negativo): "))
                        if producto_encontrado.actualizar_stock(cambio):
                            print(f"{VERDE}Stock actualizado exitosamente.{RESET}")
                        else:
                            print(f"{ROJO}ERROR{RESET}: Stock insuficiente para realizar la venta.")
                        break
                    except ValueError:
                        print("Entrada inválida. Por favor, ingrese un número entero.")
                        continue
                break # Rompe el for una vez encontrado
                    
        if not producto_encontrado:
            print(f"{ROJO}ERROR{RESET}: Producto no encontrado en el inventario.")       

    # --- OPCIÓN 4: SALIR Y GUARDAR ---
    elif menu_principal == "4":
        guardar_datos() # Llamada a la función de persistencia
        print("\nSaliendo del sistema de inventario. ¡Hasta luego!")
        break
    
    else:
        print("Opción no válida. Intente de nuevo.")