inventario = []

# esto esta mal hecho porque gasta memoria ineccesariamente
"""
producto1 ={
    "producto": "Laptop",
    "precio": 500,
    "stock": 10

}
"""
# De esta manera se optimiza el uso de memoria

inventario.append({"producto": "Laptop", "precio": 500, "stock": 10})
inventario.append({"producto": "Mouse", "precio": 20, "stock": 50})



print(inventario[1]["precio"])
print(inventario[0].get("color", "No especificado"))