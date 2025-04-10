import math
from tkinter import Tk, filedialog


# --------------------------
# FUNCIÓN PARA MOSTRAR INFORMACIÓN DEL ARCHIVO
# --------------------------
def mostrar_info_archivo(nodes, vehicle_capacity):
    """Muestra información clave del archivo cargado"""
    num_clientes = len(nodes) - 1  # Excluye el depósito
    demanda_total = sum(nodes[i]["demand"] for i in nodes if i != 0)
    min_demanda = min(nodes[i]["demand"] for i in nodes if i != 0)
    max_demanda = max(nodes[i]["demand"] for i in nodes if i != 0)

    print("\n" + "=" * 50)
    print("INFORMACIÓN DEL ARCHIVO CARGADO")
    print("=" * 50)
    print(f"- Capacidad por vehículo: {vehicle_capacity}")
    print(f"- Número de clientes: {num_clientes}")
    print(f"- Demanda total: {demanda_total}")
    print(f"- Demanda mínima: {min_demanda}")
    print(f"- Demanda máxima: {max_demanda}")
    print("- Depósito (coordenadas):", f"({nodes[0]['x']}, {nodes[0]['y']})")
    print("=" * 50 + "\n")


# --------------------------
# FUNCIÓN PARA CARGAR ARCHIVOS VRPLIB
# --------------------------
def load_vrplib(file_path):
    """Carga archivos en formato VRPLIB (ej: R103.txt)"""
    nodes = {}
    capacity = 0
    with open(file_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

        # Extraer capacidad
        for i, line in enumerate(lines):
            if "CAPACITY" in line:
                capacity = int(lines[i + 1].split()[1])
                break

        # Extraer nodos
        in_section = False
        for line in lines:
            if "CUST NO." in line:
                in_section = True
                continue
            if in_section and line[0].isdigit():
                parts = line.split()
                node_id = int(parts[0])
                nodes[node_id] = {
                    "x": float(parts[1]),
                    "y": float(parts[2]),
                    "demand": float(parts[3])
                }

    mostrar_info_archivo(nodes, capacity)
    return nodes, capacity


# --------------------------
# ALGORITMO "MINIMIZAR DISTANCIAS"
# --------------------------
def minimizar_distancias_vrp(nodes, vehicle_capacity, distance_matrix):
    """Algoritmo que minimiza distancias en rutas VRP"""
    depot = 0
    unassigned = [i for i in nodes if i != depot]
    routes = []

    while unassigned:
        route = [depot]
        current_capacity = 0

        while True:
            closest = None
            min_dist = float('inf')

            for customer in unassigned:
                dist = distance_matrix[route[-1]][customer]
                if dist < min_dist and current_capacity + nodes[customer]["demand"] <= vehicle_capacity:
                    closest = customer
                    min_dist = dist

            if closest is None:
                break  # No hay clientes factibles

            route.append(closest)
            current_capacity += nodes[closest]["demand"]
            unassigned.remove(closest)

        route.append(depot)
        routes.append(route)

    return routes


# --------------------------
# FUNCIONES AUXILIARES
# --------------------------
def calculate_distances(nodes):
    """Calcula matriz de distancias euclidianas"""
    dist_matrix = {}
    for i in nodes:
        dist_matrix[i] = {}
        for j in nodes:
            dx = nodes[i]["x"] - nodes[j]["x"]
            dy = nodes[i]["y"] - nodes[j]["y"]
            dist_matrix[i][j] = math.sqrt(dx ** 2 + dy ** 2)
    return dist_matrix


def print_solution(routes, dist_matrix, nodes, vehicle_capacity):
    """Imprime resultados detallados"""
    total_dist = 0
    print("\n" + "=" * 50)
    print("SOLUCIÓN ENCONTRADA")
    print("=" * 50)
    for i, route in enumerate(routes, 1):
        route_dist = sum(dist_matrix[route[j]][route[j + 1]] for j in range(len(route) - 1))
        total_dist += route_dist
        demand = sum(nodes[node]["demand"] for node in route[1:-1])
        print(f"\nRuta {i}:")
        print(f"- Secuencia: {route}")
        print(f"- Distancia: {route_dist:.2f}")
        print(f"- Demanda: {demand}/{vehicle_capacity}")
    print("\n" + "=" * 50)
    print(f"RESUMEN FINAL")
    print(f"- Distancia total: {total_dist:.2f}")
    print(f"- Vehículos usados: {len(routes)}")
    print(
        f"- Capacidad promedio usada: {sum(sum(nodes[node]['demand'] for node in route[1:-1]) for route in routes) / len(routes):.1f}/{vehicle_capacity}")
    print("=" * 50)


def select_file():
    """Selecciona archivo interactivamente"""
    root = Tk()
    root.withdraw()
    file = filedialog.askopenfilename(
        title="Selecciona tu archivo VRP",
        filetypes=[("Text files", "*.txt"), ("Todos los archivos", "*.*")]
    )
    root.destroy()
    return file


# --------------------------
# EJECUCIÓN PRINCIPAL
# --------------------------
def main():
    while True:
        print("=== ALGORITMO PARA MINIMIZAR DISTANCIAS EN VRP ===")
        print("Selecciona tu archivo de instancia (ej: R103.txt)\n")

        file_path = select_file()
        if not file_path:
            print("No se seleccionó archivo. Saliendo...")
            break

        # Cargar datos y mostrar información
        nodes, vehicle_capacity = load_vrplib(file_path)

        # Calcular distancias
        distance_matrix = calculate_distances(nodes)

        # Ejecutar algoritmo
        routes = minimizar_distancias_vrp(nodes, vehicle_capacity, distance_matrix)

        # Mostrar solución
        print_solution(routes, distance_matrix, nodes, vehicle_capacity)

        # Preguntar si desea procesar otro archivo
        continuar = input("\n¿Desea procesar otro archivo? (1 = Sí, otro número = No): ")
        if continuar != "1":
            print("Finalizando ejecución...")
            break


if __name__ == "__main__":
    main()