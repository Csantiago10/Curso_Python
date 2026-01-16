# Códigos de colores ANSI
VERDE = '\033[92m'
ROJO = '\033[91m'
RESET = '\033[0m'  # Este es importante para quitar el color

class Producto:
    def __init__(self, nombre, precio, cantidad):
        self.nombre = nombre
        self.precio = precio
        self.cantidad = cantidad

    def mostrar_info(self):
        return f"Producto: {self.nombre}, Precio: ${self.precio}, Cantidad: {self.cantidad}"
    
    def actualizar_stock(self, cantidad_cambio):
        if self.cantidad + cantidad_cambio < 0:
            return False  # No se puede vender más de lo que hay en stock
        self.cantidad += cantidad_cambio
        return True
    


def guardar_datos():
    with open("inventario.txt", "w") as archivo:
        for item in inventario:
            archivo.write(f"{item.nombre},{item.precio},{item.cantidad}\n")
    print(f"\n{VERDE}Datos guardados exitosamente en inventario.txt{RESET}")

def cargar_datos():
    try:
        with open("inventario.txt", "r") as archivo:
            for linea in archivo:
                nombre, precio, cantidad = linea.strip().split(",")
                producto = Producto(nombre, float(precio), int(cantidad))
                inventario.append(producto)
            print(f"{VERDE}Datos cargados exitosamente desde inventario.txt{RESET}")
    except FileNotFoundError:
        print(f"{ROJO}Archivo inventario.txt no encontrado. Iniciando con inventario vacío.{RESET}")

inventario = []

cargar_datos()

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
    if menu_principal == "1":
        nombre = input("Ingrese el nombre del producto: ")
        
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

        nuevo_producto = Producto(nombre, precio, cantidad)
        inventario.append(nuevo_producto)
        print(f"Producto registrado exitosamente.")

    elif menu_principal == "2":
        if not inventario:
            print("El inventario está vacío.")
        else:
            print("\n" + "="*30)
            print("       INVENTARIO")
            print("-"*30)
        for item in inventario:
            print(item.mostrar_info())
    elif menu_principal == "3":
        nombre_buscar = input("Ingrese el nombre del producto a actualizar: ")
        producto_encontrado = None
        for item in inventario:
            if item.nombre.lower() == nombre_buscar.lower():
                producto_encontrado = item
                print(f"Producto encontrado: {producto_encontrado.mostrar_info()}")

                while True:
                    try:
                        cambio = int(input("Ingrese la cantidad a agregar (positivo) o vender (negativo): "))
                        if producto_encontrado.actualizar_stock(cambio):
                            print("Stock actualizado exitosamente.")
                        else:
                            print(f"{ROJO}ERROR{RESET}: Stock insuficiente para realizar la venta.")
                        break
                    except ValueError:
                        print("Entrada inválida. Por favor, ingrese un número entero.")
                        continue
                break
                    
        if not producto_encontrado:
            print(f"{ROJO}ERROR{RESET}: Producto no encontrado en el inventario.")       
    elif menu_principal == "4":
        guardar_datos()

        print("\nSaliendo del sistema de inventario. ¡Hasta luego!")
        break

