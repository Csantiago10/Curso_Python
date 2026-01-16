notas_sucias = [85, "90", "Aprobado", 70, "100", "N/A", 55]
notas_limpias = []

for nota in notas_sucias:
    try:
        nota_entero = int(nota)
        notas_limpias.append(nota_entero)
    except ValueError:
        print(f"Dato corrupto encontrado: {nota}")

print("Notas limpias: ", notas_limpias)