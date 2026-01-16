print("Factura de compra + propina")

monto_total_cuenta = float(input("Ingrese el monto total de la cuenta: "))

propina = float(input("Ingrese el porcentaje de propina que desea dejar: "))

valor_propina = monto_total_cuenta * (propina / 100)

monto_final = monto_total_cuenta + valor_propina

print(f"El monto final a pagar, incluyendo el valor de la propina es de {monto_final:.2f}")