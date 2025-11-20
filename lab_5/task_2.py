import heapq
import random
import time

def edges_to_matrix(edges):
    if not edges:
        return [], 0

    max_vertex = max(max(u, v) for u, v, _ in edges)
    n = max_vertex + 1
    graph = [[float('inf')] * n for _ in range(n)]

    for u, v, w in edges:
        graph[u][v] = w
        graph[v][u] = w

    for i in range(n):
        graph[i][i] = 0

    return graph, n

class TSPNode:
    def __init__(self, level, path, cost, bound, remaining_vertices):
        self.level = level
        self.path = path
        self.cost = cost
        self.bound = bound
        self.remaining_vertices = remaining_vertices

    def __lt__(self, other):
        return self.bound < other.bound

def calculate_bound(node, graph):
    n = len(graph)
    bound = node.cost
    visited = set(node.path)

    for v in range(n):
        if v not in visited:
            min_edges = []
            for u in range(n):
                if u != v and u not in visited:
                    min_edges.append(graph[v][u])
            if len(min_edges) >= 2:
                min_edges.sort()
                bound += min_edges[0] + min_edges[1]
            elif len(min_edges) == 1:
                bound += min_edges[0]

    if len(node.path) > 1:
        last = node.path[-1]
        start = node.path[0]
        min_to_start = graph[last][start]
        bound += min_to_start

    return bound

def tsp_branch_and_bound(edges):
    if not edges:
        return []

    graph, n = edges_to_matrix(edges)

    all_vertices = set()
    for u, v, _ in edges:
        all_vertices.add(u)
        all_vertices.add(v)

    if len(all_vertices) == 1:
        return []

    start_vertex = min(all_vertices)

    pq = []
    initial_path = [start_vertex]
    initial_cost = 0
    initial_bound = calculate_bound(TSPNode(0, initial_path, initial_cost, 0, set(range(n)) - {start_vertex}), graph)
    root = TSPNode(0, initial_path, initial_cost, initial_bound, set(range(n)) - {start_vertex})
    heapq.heappush(pq, root)

    min_cost = float('inf')
    best_path = None

    while pq:
        node = heapq.heappop(pq)

        if node.level == n - 1:
            last_vertex = node.path[-1]
            return_to_start = graph[last_vertex][start_vertex]
            total_cost = node.cost + return_to_start

            if total_cost < min_cost:
                min_cost = total_cost
                best_path = node.path
            continue

        if node.bound >= min_cost:
            continue

        for next_vertex in node.remaining_vertices:
            new_path = node.path + [next_vertex]
            new_cost = node.cost + graph[node.path[-1]][next_vertex]
            new_remaining = node.remaining_vertices - {next_vertex}
            new_node = TSPNode(
                level=node.level + 1,
                path=new_path,
                cost=new_cost,
                bound=calculate_bound(TSPNode(node.level + 1, new_path, new_cost, 0, new_remaining), graph),
                remaining_vertices=new_remaining
            )
            heapq.heappush(pq, new_node)

    return best_path if best_path else []

def aligned(route, start):
    if not route:
        return route
    try:
        idx = route.index(start)
    except ValueError:
        return route
    return route[idx:] + route[:idx]

def cycles_equal(cycle1, cycle2):
    """Проверяет, являются ли два цикла эквивалентными (с точностью до сдвига и направления)"""
    if len(cycle1) != len(cycle2):
        return False
    if len(cycle1) == 0:
        return True

    n = len(cycle1)
    rotations = []
    for i in range(n):
        rotated = cycle1[i:] + cycle1[:i]
        rotations.append(rotated)
        rotations.append(rotated[::-1])

    for rot in rotations:
        if rot == cycle2:
            return True

    return False

def route_weight(route, edges):
    """Вычисляет вес маршрута (включая замыкание)"""
    if len(route) < 2:
        return 0.0
    graph, n = edges_to_matrix(edges)
    total = 0.0
    for i in range(len(route) - 1):
        u, v = route[i], route[i+1]
        total += graph[u][v]
    total += graph[route[-1]][route[0]]  # замыкание
    return total

def generate_random_complete_graph(n, min_weight=1.0, max_weight=10.0):
    """Генерирует полный неориентированный граф с n вершинами"""
    edges = []
    for i in range(n):
        for j in range(i+1, n):
            weight = round(random.uniform(min_weight, max_weight), 1)
            edges.append([i, j, weight])
    return edges

def measure_time(func, *args):
    start = time.perf_counter()
    result = func(*args)
    end = time.perf_counter()
    return result, end - start

# --- Тесты ---
if __name__ == "__main__":
    # [TSP] Empty graph
    g = []
    result = tsp_branch_and_bound(g)
    expected = []
    print(f"Empty graph: result={result}, expected={expected}")
    assert cycles_equal(result, expected)
    print("✓ Empty graph")

    # [TSP] Single vertex
    g = []
    result = tsp_branch_and_bound(g)
    expected = []
    print(f"Single vertex: result={result}, expected={expected}")
    assert cycles_equal(result, expected)
    print("✓ Single vertex")

    # [TSP] One edge
    g = [[0, 1, 2.5]]
    result = tsp_branch_and_bound(g)
    expected = [0, 1]
    print(f"One edge: result={result}, expected={expected}, weight={route_weight(result, g):.1f}")
    assert cycles_equal(result, expected)
    print("✓ One edge")

    # [TSP] Three vertices, three edges
    g = [[0, 1, 2.5], [0, 2, 0.5], [1, 2, 1.0]]
    result = tsp_branch_and_bound(g)
    expected = [0, 1, 2]
    print(f"Three vertices: result={result}, expected={expected}, weight={route_weight(result, g):.1f}")
    assert cycles_equal(result, expected)
    print("✓ Three vertices")

    # [TSP] Four vertices
    g = [[0, 1, 6.0], [0, 2, 4.0], [0, 3, 1.0],
         [1, 2, 3.5], [1, 3, 2.0],
         [2, 3, 5.0]]
    result = tsp_branch_and_bound(g)
    expected = [0, 2, 1, 3]
    print(f"Four vertices: result={result}, expected={expected}, weight={route_weight(result, g):.1f}")
    assert cycles_equal(result, expected)
    print("✓ Four vertices")

    # [TSP] Five vertices
    g = [[0, 1, 2.0], [0, 2, 4.0], [0, 3, 1.0], [0, 4, 2.5],
         [1, 2, 3.6], [1, 3, 6.0], [1, 4, 3.0],
         [2, 3, 7.0], [2, 4, 5.0],
         [3, 4, 9.0]]
    result = tsp_branch_and_bound(g)
    expected = [0, 3, 2, 1, 4]
    print(f"Five vertices: result={result}, expected={expected}, weight={route_weight(result, g):.1f}")
    assert cycles_equal(result, expected)
    print("✓ Five vertices")

    # [TSP] Six vertices
    g = [[0, 1, 2.0], [0, 2, 4.0], [0, 3, 1.0], [0, 4, 2.5], [0, 5, 3.2],
         [1, 2, 3.6], [1, 3, 6.0], [1, 4, 3.0], [1, 5, 0.1],
         [2, 3, 7.0], [2, 4, 5.0], [2, 5, 9],
         [3, 4, 9.0], [3, 5, 0.5],
         [4, 5, 1.0]]
    result = tsp_branch_and_bound(g)
    expected = [0, 3, 2, 1, 5, 4]
    print(f"Six vertices: result={result}, expected={expected}, weight={route_weight(result, g):.1f}")
    assert cycles_equal(result, expected)
    print("✓ Six vertices")

    print("\n✅ Все тесты пройдены для метода ветвей и границ!")

    # --- Замер времени на случайных графах ---
    print("\n" + "="*60)
    print("ЗАМЕР ВРЕМЕНИ РАБОТЫ АЛГОРИТМОВ")
    print("="*60)

    for size in [3, 4, 5, 6, 7, 8, 9, 10]:
        print(f"\n--- Граф из {size} вершин ---")
        g = generate_random_complete_graph(size)

        # Полный перебор — можно вызвать, если скопировать функцию
        # Но лучше запустить a_complete_bust.py отдельно
        print("Полный перебор: см. файл a_complete_bust.py")

        # Метод ветвей и границ
        result_bb, time_bb = measure_time(tsp_branch_and_bound, g)
        weight_bb = route_weight(result_bb, g) if result_bb else 0.0
        print(f"Ветви и границы: маршрут={result_bb}, вес={weight_bb:.1f}, время={time_bb:.4f} сек")

    print("\n💡 Для сравнения с полным перебором — запустите a_complete_bust.py")
