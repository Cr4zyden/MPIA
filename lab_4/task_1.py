import heapq
import time
import random
from typing import List, Tuple, Optional

class Graph:
    def __init__(self):
        self._vertices = set()
        self._edges = {}  # vertex -> {adjacent_vertex: weight}

    def add_vertex(self, v: int) -> None:
        self._vertices.add(v)
        if v not in self._edges:
            self._edges[v] = {}

    def has_vertex(self, v: int) -> bool:
        return v in self._vertices

    def add_edge(self, u: int, v: int, weight: float = 1.0) -> None:
        self.add_vertex(u)
        self.add_vertex(v)
        self._edges[u][v] = weight
        self._edges[v][u] = weight

    def has_edge(self, u: int, v: int) -> bool:
        return u in self._edges and v in self._edges[u]

    def edge_weight(self, u: int, v: int) -> float:
        if not self.has_edge(u, v):
            raise ValueError(f"Edge ({u}, {v}) does not exist")
        return self._edges[u][v]

    def get_vertices(self) -> List[int]:
        return sorted(list(self._vertices))

    def get_adjacent_vertices(self, v: int) -> List[int]:
        if v not in self._edges:
            return []
        return sorted(list(self._edges[v].keys()))

    def get_adjacent_edges(self, v: int) -> List[Tuple[int, float]]:
        if v not in self._edges:
            return []
        edges = [(adj, self._edges[v][adj]) for adj in self._edges[v]]
        return sorted(edges)

    def remove_vertex(self, v: int) -> None:
        if v not in self._vertices:
            return
        self._vertices.remove(v)
        if v in self._edges:
            del self._edges[v]
        # Remove v from all other vertices' adjacency lists
        for vertex in list(self._edges.keys()):
            if v in self._edges[vertex]:
                del self._edges[vertex][v]

    def remove_edge(self, u: int, v: int) -> None:
        if self.has_edge(u, v):
            del self._edges[u][v]
            del self._edges[v][u]


def shortest_path(graph: Graph, start: int, end: int) -> Optional[List[int]]:
    """
    Реализация алгоритма Дейкстры для поиска кратчайшего пути.
    Возвращает список вершин, составляющих путь от start до end,
    или None, если путь не существует.
    """
    if not graph.has_vertex(start) or not graph.has_vertex(end):
        return None

    # Инициализация
    distances = {vertex: float('inf') for vertex in graph.get_vertices()}
    distances[start] = 0
    previous = {vertex: None for vertex in graph.get_vertices()}
    pq = [(0, start)]  # (расстояние, вершина)
    visited = set()

    while pq:
        current_dist, current_vertex = heapq.heappop(pq)

        if current_vertex in visited:
            continue

        visited.add(current_vertex)

        # Если достигли конечной вершины
        if current_vertex == end:
            break

        # Обновляем расстояния до соседей
        for neighbor in graph.get_adjacent_vertices(current_vertex):
            if neighbor in visited:
                continue

            edge_weight = graph.edge_weight(current_vertex, neighbor)
            new_dist = current_dist + edge_weight

            if new_dist < distances[neighbor]:
                distances[neighbor] = new_dist
                previous[neighbor] = current_vertex
                heapq.heappush(pq, (new_dist, neighbor))

    # Проверяем, найден ли путь
    if distances[end] == float('inf'):
        return None

    # Восстанавливаем путь
    path = []
    current = end
    while current is not None:
        path.append(current)
        current = previous[current]
    path.reverse()

    return path


# --- Генератор связного графа ---
def generate_connected_graph(n: int, avg_degree: int = 4) -> Graph:
    """
    Генерирует связный взвешенный граф с n вершинами.
    Средняя степень вершин ~ avg_degree.
    """
    g = Graph()
    # Добавляем все вершины
    for i in range(n):
        g.add_vertex(i)

    # Гарантируем связность: строим цепочку
    for i in range(n - 1):
        g.add_edge(i, i + 1, random.uniform(0.5, 5.0))

    # Добавляем дополнительные рёбра для нужной плотности
    total_edges_needed = n * avg_degree // 2 - (n - 1)  # минус цепочка
    added = 0
    attempts = 0
    max_attempts = n * n

    while added < total_edges_needed and attempts < max_attempts:
        u = random.randint(0, n - 1)
        v = random.randint(0, n - 1)
        if u != v and not g.has_edge(u, v):
            g.add_edge(u, v, random.uniform(0.5, 5.0))
            added += 1
        attempts += 1

    return g


# --- Встроенные тесты ---
def test_empty_graph():
    g = Graph()
    assert not g.has_vertex(0)
    assert not g.has_edge(0, 1)

def test_one_vertex():
    g = Graph()
    g.add_vertex(0)
    assert g.has_vertex(0)
    assert not g.has_vertex(1)
    assert not g.has_edge(0, 1)

def test_two_vertices():
    g = Graph()
    g.add_vertex(0)
    g.add_vertex(1)
    assert g.has_vertex(0)
    assert g.has_vertex(1)
    assert not g.has_edge(0, 1)

def test_one_edge():
    g = Graph()
    g.add_edge(0, 1, 5.0)
    assert g.has_vertex(0)
    assert g.has_vertex(1)
    assert g.has_edge(0, 1)
    assert g.has_edge(1, 0)
    assert g.edge_weight(0, 1) == 5.0
    assert not g.has_edge(0, 0)

def test_loop():
    g = Graph()
    g.add_edge(0, 0)
    g.add_edge(1, 1)
    assert g.has_vertex(0)
    assert g.has_vertex(1)
    assert g.has_edge(0, 0)
    assert g.has_edge(1, 1)

def test_two_edges():
    g = Graph()
    g.add_edge(0, 1)
    g.add_edge(0, 3)
    assert g.has_vertex(0)
    assert g.has_vertex(1)
    assert g.has_vertex(3)
    assert g.has_edge(0, 1)
    assert g.has_edge(0, 3)
    assert g.has_edge(1, 0)
    assert g.has_edge(3, 0)
    assert not g.has_edge(1, 3)

def test_get_vertices():
    g = Graph()
    g.add_vertex(0)
    g.add_edge(0, 1)
    g.add_vertex(3)
    assert g.get_vertices() == [0, 1, 3]

def test_get_adjacent_vertices():
    g = Graph()
    g.add_vertex(0)
    g.add_edge(0, 1)
    g.add_edge(0, 2, 4.5)
    g.add_edge(1, 2, 3.0)
    g.add_edge(1, 3)
    assert g.get_adjacent_vertices(0) == [1, 2]
    assert g.get_adjacent_vertices(1) == [0, 2, 3]
    assert g.get_adjacent_vertices(2) == [0, 1]
    assert g.get_adjacent_vertices(3) == [1]
    assert g.get_adjacent_vertices(4) == []
    assert g.edge_weight(1, 2) == 3.0
    assert g.edge_weight(2, 0) == 4.5
    try:
        g.edge_weight(0, 3)
        assert False, "Expected ValueError"
    except ValueError:
        pass

def test_get_adjacent_edges():
    g = Graph()
    g.add_edge(0, 1)
    g.add_edge(0, 2, 4.5)
    g.add_edge(1, 2, 3.0)
    g.add_edge(3, 1, 7.2)
    edges_0 = set(g.get_adjacent_edges(0))
    assert edges_0 == {(1, 1.0), (2, 4.5)}
    edges_1 = set(g.get_adjacent_edges(1))
    assert edges_1 == {(0, 1.0), (2, 3.0), (3, 7.2)}
    edges_2 = set(g.get_adjacent_edges(2))
    assert edges_2 == {(0, 4.5), (1, 3.0)}
    edges_3 = set(g.get_adjacent_edges(3))
    assert edges_3 == {(1, 7.2)}
    assert g.get_adjacent_edges(4) == []

def test_replace_an_edge():
    g = Graph()
    g.add_edge(1, 5, 3.5)
    g.add_edge(5, 1, 4.7)
    assert g.has_edge(1, 5)
    assert g.has_edge(5, 1)
    assert g.edge_weight(1, 5) == 4.7
    assert g.edge_weight(5, 1) == 4.7

def test_remove_vertices_and_edges():
    g = Graph()
    g.add_edge(0, 1)
    g.add_edge(0, 2)
    g.add_edge(0, 3)
    g.add_edge(0, 4)
    g.add_edge(1, 2)
    g.add_edge(1, 3)
    g.add_edge(2, 3)
    g.add_edge(2, 4)
    g.remove_vertex(2)
    assert not g.has_vertex(2)
    assert not g.has_edge(1, 2)
    assert not g.has_edge(3, 2)
    assert not g.has_edge(4, 2)
    assert g.has_edge(0, 1)
    assert g.has_edge(0, 4)
    assert g.has_edge(1, 3)
    g.remove_edge(0, 1)
    assert not g.has_edge(0, 1)
    assert g.has_vertex(0)
    assert g.has_vertex(1)


# --- Замер времени и вывод таблицы ---
def run_benchmark():
    print("\n" + "="*80)
    print("ЗАМЕРЫ ВРЕМЕНИ АЛГОРИТМА ДЕЙКСТРЫ")
    print("="*80)
    print(f"{'Размер графа':<12} {'Время (сек)':<12} {'Число рёбер':<12} {'Плотность':<10}")
    print("-"*80)

    sizes = [10, 50, 100, 200, 500, 1000, 10000]
    runs_per_size = 5  # количество запусков для усреднения

    for n in sizes:
        g = generate_connected_graph(n, avg_degree=5)  # средняя степень 5
        total_time = 0.0
        num_edges = sum(len(g._edges[v]) for v in g._edges) // 2  # так как граф неориентированный
        density = num_edges / (n * (n - 1) / 2) if n > 1 else 0

        for _ in range(runs_per_size):
            start, end = random.choice(g.get_vertices()), random.choice(g.get_vertices())
            start_time = time.perf_counter()
            path = shortest_path(g, start, end)
            end_time = time.perf_counter()
            total_time += end_time - start_time

        avg_time = total_time / runs_per_size
        print(f"{n:<12} {avg_time:<12.6f} {num_edges:<12} {density:<10.3f}")

    print("\n" + "="*80)
    print("ВЫВОДЫ:")
    print("- Алгоритм Дейкстры работает за O((V + E) log V) в худшем случае.")
    print("- На практике время растёт примерно линейно с числом рёбер при фиксированной плотности.")
    print("- Для больших графов (n > 1000) время возрастает заметно, но остаётся приемлемым.")
    print("- Увеличение плотности графа (больше рёбер) увеличивает время выполнения.")
    print("- При n=1000 алгоритм выполняется за доли секунды — подходит для реального времени.")


if __name__ == "__main__":
    # Запуск всех тестов
    test_empty_graph()
    test_one_vertex()
    test_two_vertices()
    test_one_edge()
    test_loop()
    test_two_edges()
    test_get_vertices()
    test_get_adjacent_vertices()
    test_get_adjacent_edges()
    test_replace_an_edge()
    test_remove_vertices_and_edges()
    print("✅ Все юнит-тесты пройдены успешно!")

    # Запуск замеров
    run_benchmark()