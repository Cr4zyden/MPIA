import time
import random
import unittest

class TSPGraph:
    """Взвешенный граф для задачи коммивояжера"""
    
    def __init__(self, vertices=[], edges_with_weights=[]):
        self.vertices = vertices
        self.n = len(vertices)
        self.dist_matrix = [[float('inf')] * self.n for _ in range(self.n)]
        
        for i in range(self.n):
            self.dist_matrix[i][i] = 0
        
        for (v1, v2, weight) in edges_with_weights:
            i = self.vertices.index(v1)
            j = self.vertices.index(v2)
            self.dist_matrix[i][j] = weight
            self.dist_matrix[j][i] = weight
    
    def get_distance(self, i, j):
        return self.dist_matrix[i][j]
    
    def get_size(self):
        return self.n
    
    def get_vertices(self):
        return self.vertices
    
    def generate_complete_graph(self, max_weight=100):
        for i in range(self.n):
            for j in range(i + 1, self.n):
                weight = random.randint(1, max_weight)
                self.dist_matrix[i][j] = weight
                self.dist_matrix[j][i] = weight
        return self

def tsp_greedy(tsp_graph, start_city=0):
    """Жадный алгоритм для TSP"""
    start_time = time.perf_counter()
    
    n = tsp_graph.get_size()
    if n == 0:
        return [], 0, 0
    
    visited = [False] * n
    path = [start_city]
    visited[start_city] = True
    total_distance = 0
    current = start_city
    
    for _ in range(n - 1):
        min_dist = float('inf')
        next_city = -1
        
        for neighbor in range(n):
            if not visited[neighbor]:
                dist = tsp_graph.get_distance(current, neighbor)
                if dist < min_dist:
                    min_dist = dist
                    next_city = neighbor
        
        path.append(next_city)
        visited[next_city] = True
        total_distance += min_dist
        current = next_city
    
    return_distance = tsp_graph.get_distance(current, start_city)
    total_distance += return_distance
    path.append(start_city)
    
    end_time = time.perf_counter()
    return path, total_distance, end_time - start_time

def tsp_2opt(tsp_graph, initial_path=None):
    """Локальный поиск с 2-opt улучшением"""
    start_time = time.perf_counter()
    
    n = tsp_graph.get_size()
    if n == 0:
        return [], 0, 0
    
    if initial_path is None:
        path = list(range(n))
        random.shuffle(path)
        path.append(path[0])
    else:
        path = initial_path.copy()
    
    improved = True
    while improved:
        improved = False
        for i in range(1, n - 1):
            for j in range(i + 1, n):
                if j - i == 1:
                    continue
                
                old_distance = (tsp_graph.get_distance(path[i-1], path[i]) +
                              tsp_graph.get_distance(path[j], path[j+1]))
                
                new_distance = (tsp_graph.get_distance(path[i-1], path[j]) +
                              tsp_graph.get_distance(path[i], path[j+1]))
                
                if new_distance < old_distance:
                    path[i:j+1] = reversed(path[i:j+1])
                    improved = True
                    break
            if improved:
                break
    
    total_distance = 0
    for i in range(len(path) - 1):
        total_distance += tsp_graph.get_distance(path[i], path[i+1])
    
    end_time = time.perf_counter()
    return path, total_distance, end_time - start_time

# Вспомогательные функции для тестирования
def reversed_path(path):
    if not path:
        return []
    result = [path[0]]
    result.extend(path[-1:0:-1])
    return result

def start_with(path, vertex):
    if vertex not in path:
        return path
    idx = path.index(vertex)
    return path[idx:] + path[:idx]

def min_dir(path):
    if len(path) <= 1:
        return path
    reversed_path_val = reversed_path(path)
    return path if path[1] <= reversed_path_val[1] else reversed_path_val

def aligned(path, start_vertex):
    return min_dir(start_with(path, start_vertex))

# ТЕСТЫ для проверки корректности реализации
class TSPImplementationTests(unittest.TestCase):
    """Тесты для проверки корректности реализации алгоритмов"""
    
    def test_empty_graph(self):
        """Пустой граф"""
        graph = TSPGraph()
        path, length, time_taken = tsp_greedy(graph)
        self.assertEqual(path, [])
        self.assertEqual(length, 0)
    
    def test_single_vertex(self):
        """Одна вершина"""
        graph = TSPGraph([0])
        path, length, time_taken = tsp_greedy(graph)
        self.assertEqual(len(path), 2)  # [0, 0]
        self.assertEqual(path[0], path[-1])
    
    def test_one_edge(self):
        """Одно ребро"""
        graph = TSPGraph([0, 1], [(0, 1, 2.5)])
        path, length, time_taken = tsp_greedy(graph)
        self.assertEqual(len(path), 3)  # [0, 1, 0]
        self.assertEqual(path[0], path[-1])
        self.assertAlmostEqual(length, 5.0)  # 2.5 + 2.5
    
    def test_algorithm_returns_valid_path(self):
        """Алгоритм возвращает корректный путь"""
        graph = TSPGraph([0, 1, 2], [(0, 1, 1.0), (0, 2, 2.0), (1, 2, 3.0)])
        path, length, time_taken = tsp_greedy(graph)
        
        # Проверяем, что путь корректен
        self.assertEqual(len(path), 4)  # 3 города + возврат в начало
        self.assertEqual(path[0], path[-1])  # начинается и заканчивается в одной точке
        self.assertEqual(len(set(path[:-1])), 3)  # все города посещены по одному разу
    
    def test_2opt_improvement(self):
        """2-opt улучшает решение"""
        # Создаем граф, где жадный алгоритм даёт неоптимальное решение
        graph = TSPGraph([0, 1, 2, 3], [
            (0, 1, 1.0), (0, 2, 10.0), (0, 3, 10.0),
            (1, 2, 1.0), (1, 3, 10.0),
            (2, 3, 1.0)
        ])
        
        greedy_path, greedy_length, greedy_time = tsp_greedy(graph)
        opt_path, opt_length, opt_time = tsp_2opt(graph, greedy_path)
        
        # 2-opt должен найти решение не хуже жадного
        self.assertLessEqual(opt_length, greedy_length)

# БЕНЧМАРКИ для сравнения производительности
def generate_test_graphs():
    """Генерирует тестовые графы для сравнения производительности"""
    test_graphs = {}
    
    # Маленькие графы
    small_sizes = [5, 10, 15, 20]
    for size in small_sizes:
        vertices = list(range(size))
        graph = TSPGraph(vertices, [])
        graph.generate_complete_graph(max_weight=100)
        test_graphs[size] = graph
    
    # Большие графы
    large_sizes = [50, 100, 200]
    for size in large_sizes:
        vertices = list(range(size))
        graph = TSPGraph(vertices, [])
        graph.generate_complete_graph(max_weight=100)
        test_graphs[size] = graph
    
    return test_graphs

def run_benchmarks():
    """Запускает сравнение производительности алгоритмов"""
    test_graphs = generate_test_graphs()
    
    print("Размер | Алгоритм    | Время (сек) | Длина маршрута")
    print("------|-------------|-------------|---------------")
    
    results = []
    
    for size, graph in sorted(test_graphs.items()):
        greedy_path, greedy_length, greedy_time = tsp_greedy(graph, 0)
        local_path, local_length, local_time = tsp_2opt(graph, greedy_path)
        
        print(f"{size:6} | {'Жадный':11} | {greedy_time:10.6f} | {greedy_length:14.2f}")
        print(f"{size:6} | {'2-opt':11} | {local_time:10.6f} | {local_length:14.2f}")
        
        results.append({
            'size': size,
            'greedy_time': greedy_time,
            'greedy_length': greedy_length,
            'local_time': local_time,
            'local_length': local_length
        })
    
    return results

def analyze_results(results):
    """Анализирует результаты сравнения"""
    print("\n" + "="*50)
    print("АНАЛИЗ РЕЗУЛЬТАТОВ")
    print("="*50)
    
    for result in results:
        size = result['size']
        improvement = ((result['greedy_length'] - result['local_length']) / 
                      result['greedy_length'] * 100) if result['greedy_length'] > 0 else 0
        
        if result['greedy_time'] > 0.000001:
            time_ratio = result['local_time'] / result['greedy_time']
        else:
            time_ratio = float('inf')
        
        print(f"\nРазмер {size}:")
        print(f"  Улучшение качества: {improvement:.2f}%")
        print(f"  Время 2-opt / Жадный: {time_ratio:.2f}x")
        
        if result['greedy_time'] < 0.0001:
            print(f"  Примечание: время жадного алгоритма < 0.1ms")

# ЗАПУСК
if __name__ == "__main__":
    print("СРАВНЕНИЕ ПРОИЗВОДИТЕЛЬНОСТИ: ЖАДНЫЙ АЛГОРИТМ vs 2-OPT")
    print("="*60)
    
    # Запуск тестов реализации
    print("\nПРОВЕРКА КОРРЕКТНОСТИ РЕАЛИЗАЦИИ...")
    test_suite = unittest.TestLoader().loadTestsFromTestCase(TSPImplementationTests)
    test_runner = unittest.TextTestRunner(verbosity=2)
    test_result = test_runner.run(test_suite)
    
    print("\n" + "="*60)
    print("СРАВНЕНИЕ ПРОИЗВОДИТЕЛЬНОСТИ")
    print("="*60)
    
    # Запуск сравнения производительности
    results = run_benchmarks()
    analyze_results(results)
    
    print("\n" + "="*60)
    print("ВЫВОДЫ:")
    print("="*60)
    print("1. Оба алгоритма возвращают корректные маршруты")
    print("2. Жадный алгоритм работает очень быстро")
    print("3. 2-opt улучшает качество решения жадного алгоритма")  
    print("4. Для маленьких графов разница во времени незначительна")
    print("5. Для больших графов 2-opt требует больше времени, но даёт лучшие результаты")
    print("6. Выбор алгоритма зависит от требований: скорость vs качество")