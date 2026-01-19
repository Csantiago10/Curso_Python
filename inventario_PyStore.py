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

def sanitizar_inventario():
    """
    Fusiona productos duplicados en la lista global inventario.
    Suma las cantidades y deja un solo registro por nombre.
    """
    global inventario # Necesario para modificar la lista principal
    diccionario_unico = {}
    duplicados_corregidos = 0

    print(f"{BLUE}Verificando duplicados en la base de datos...{RESET}")

    for producto in inventario:
        # Normalizamos el nombre (minusculas y sin espacios extra)
        clave_nombre = producto.nombre.lower().strip()

        if clave_nombre in diccionario_unico:
            # ¡DUPLICADO DETECTADO!
            # Sumamos la cantidad del duplicado al que ya guardamos
            diccionario_unico[clave_nombre].cantidad += producto.cantidad
            duplicados_corregidos += 1
        else:
            # Es el primero que encontramos, lo guardamos
            diccionario_unico[clave_nombre] = producto

    # Si encontramos errores, actualizamos la lista real
    if duplicados_corregidos > 0:
        # Reemplazamos la lista vieja con los valores únicos del diccionario
        inventario = list(diccionario_unico.values())
        print(f"{VERDE}¡Limpieza completada! Se fusionaron {duplicados_corregidos} registros repetidos.{RESET}")
        guardar_datos() # Guardamos inmediatamente el arreglo en el JSON
    else:
        print(f"{VERDE}Base de datos limpia. No se encontraron duplicados.{RESET}")

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

# Pasar la escoba (Limpiar duplicados y sumar cantidades)
sanitizar_inventario()

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
    print("4. Eliminar un Producto")
    print("5. Salir")
    print("="*30)

    menu_principal = input(">>> Selecciona una opción (1-5): ")
    # --- OPCIÓN 1: CREAR (Create) ---
    # --- OPCIÓN 1: CREAR O ACTUALIZAR (Create / Upsert) ---
    if menu_principal == "1":
        nombre = input("Ingrese el nombre del producto: ").strip() # .strip() quita espacios accidentales al inicio/final
        
        # 1. BÚSQUEDA PREVIA: ¿Ya existe?
        producto_existente = None
        for item in inventario:
            if item.nombre.lower() == nombre.lower():
                producto_existente = item
                break # ¡Lo encontramos! Dejamos de buscar.

        # 2. DECISIÓN: CAMINO A (Actualizar) o CAMINO B (Crear)
        
        if producto_existente:
            # --- CAMINO A: EL PRODUCTO YA EXISTE ---
            print(f"\n{BLUE}¡Aviso! El producto '{producto_existente.nombre}' ya está registrado.{RESET}")
            print(f"Precio: {formato_pesos_colombianos(producto_existente.precio)} | Stock actual: {producto_existente.cantidad}")
            
            while True:
                try:
                    sumar_stock = int(input("Ingrese la cantidad ADICIONAL a sumar al inventario: "))
                    if sumar_stock >= 0:
                        producto_existente.actualizar_stock(sumar_stock)
                        print(f"{VERDE}Stock actualizado. Nuevo total: {producto_existente.cantidad}{RESET}")
                        break
                    else:
                        print("Por favor, ingrese un número positivo.")
                except ValueError:
                    print("Error: Ingrese un número entero.")
                    continue

        else:
            # --- CAMINO B: EL PRODUCTO ES NUEVO (Tu lógica original) ---
            print(f"{BLUE}Producto nuevo detectado. Procediendo al registro...{RESET}")
            
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
                    cantidad = int(input("Ingrese la cantidad INICIAL del producto: "))
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
            print(f"{VERDE}Producto '{nombre}' registrado exitosamente.{RESET}")
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
    # --- OPCIÓN 4: ELIMINAR (Delete) ---
    elif menu_principal == "4":
        nombre_eliminar = input("Ingrese el nombre del producto a eliminar: ").strip()
        producto_encontrado = None

        # 1. Buscamos el objeto
        for item in inventario:
            if item.nombre.lower() == nombre_eliminar.lower():
                producto_encontrado = item
                break # Lo encontramos, dejamos de buscar

        # 2. Confirmamos y Borramos
        if producto_encontrado:
            print(f"\n{ROJO}¡ADVERTENCIA! Va a eliminar el siguiente producto:{RESET}")
            # Mostramos info para que esté seguro
            nombre, precio, cantidad = producto_encontrado.mostrar_info()
            print(f" - {nombre} (Stock: {cantidad})")
            
            confirmacion = input(f"¿Está seguro de borrarlo permanentemente? ({VERDE}si{RESET}/{ROJO}no{RESET}): ").lower()
            
            if confirmacion == "si":
                inventario.remove(producto_encontrado) # <--- AQUÍ OCURRE LA MUERTE DEL DATO
                print(f"\n{VERDE}Producto eliminado exitosamente.{RESET}")
                guardar_datos() # Guardado automático por seguridad
            else:
                print(f"\n{BLUE}Operación cancelada. El producto está a salvo.{RESET}")
        else:
            print(f"{ROJO}Error: El producto '{nombre_eliminar}' no existe en el inventario.{RESET}")

    # --- OPCIÓN 4: SALIR Y GUARDAR ---
    elif menu_principal == "5":
        guardar_datos() # Llamada a la función de persistencia
        print("\nSaliendo del sistema de inventario. ¡Hasta luego!")
        break
    
    else:
        print("Opción no válida. Intente de nuevo.")