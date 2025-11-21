import time
import random
import unittest

class TSPGraph:
    """Взвешенный граф для задачи коммивояжера"""
    
    def __init__(self, vertices=[], edges_with_weights=[]):
        self.vertices = vertices # Список вершин (городов)
        self.n = len(vertices) # Количество вершин
        self.dist_matrix = [[float('inf')] * self.n for _ in range(self.n)]
        
        #расстояние от города i к j
        for i in range(self.n):
            self.dist_matrix[i][i] = 0
        
        for (v1, v2, weight) in edges_with_weights:
            i = self.vertices.index(v1)
            j = self.vertices.index(v2)
            # Записываем расстояние в матрицу в обе стороны (неорграф)
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
    
    n = tsp_graph.get_size() # Получаем количество городов
    visited = [False] * n # Массив посещённых городов
    path = [start_city] 
    visited[start_city] = True # Отмечаем стартовый город как посещённый
    total_distance = 0
    current = start_city
    
    # Посещаем все оставшиеся города
    for _ in range(n - 1):
        min_dist = float('inf')
        next_city = -1
        
        for neighbor in range(n):
            if not visited[neighbor]: # Если город ещё не посещён
                dist = tsp_graph.get_distance(current, neighbor)
                if dist < min_dist: # Если нашли ближайший город
                    min_dist = dist
                    next_city = neighbor
        
        # Добавляем ближайший город в маршрут
        path.append(next_city)
        visited[next_city] = True
        total_distance += min_dist
        current = next_city # Переходим в следующий город
    
    # Возвращаемся в начальный город
    return_distance = tsp_graph.get_distance(current, start_city)
    total_distance += return_distance
    path.append(start_city) # Замыкаем цикл
    
    # Завершаем замер времени
    end_time = time.perf_counter()
    return path, total_distance, end_time - start_time

def tsp_2opt(tsp_graph, initial_path=None):
    """Локальный поиск с 2-opt улучшением"""
    start_time = time.perf_counter()
    
    n = tsp_graph.get_size()
    
    if initial_path is None:
        path = list(range(n))
        random.shuffle(path)
        path.append(path[0])
    else:
        path = initial_path.copy()
    
    improved = True
    while improved:
        improved = False
        # Перебираем все пары рёбер (i-1, i) и (j, j+1)
        for i in range(1, n - 1):
            for j in range(i + 1, n):
                if j - i == 1:
                    continue
                
                # Считаем длину текущих двух рёбер
                old_distance = (tsp_graph.get_distance(path[i-1], path[i]) + tsp_graph.get_distance(path[j], path[j+1]))
                # Считаем длину новых рёбер после перестановки
                new_distance = (tsp_graph.get_distance(path[i-1], path[j]) + tsp_graph.get_distance(path[i], path[j+1]))
                
                if new_distance < old_distance:
                    # Переворачиваем сегмент между i и j
                    path[i:j+1] = reversed(path[i:j+1])
                    improved = True
                    break
            if improved:
                break
    
    # Вычисляем общую длину улучшенного маршрута
    total_distance = 0
    for i in range(len(path) - 1):
        total_distance += tsp_graph.get_distance(path[i], path[i+1])
    
    end_time = time.perf_counter()
    return path, total_distance, end_time - start_time

# ТЕСТЫ
class TSPTests(unittest.TestCase):
    def test_small_graph(self):
        vertices = ["A", "B", "C", "D"]
        edges = [
            ("A", "B", 10), ("A", "C", 15), ("A", "D", 20),
            ("B", "C", 35), ("B", "D", 25), ("C", "D", 30)
        ]
        
        graph = TSPGraph(vertices, edges)
        path, length, time_taken = tsp_greedy(graph, 0)
        self.assertEqual(len(path), len(vertices) + 1)
        self.assertEqual(path[0], path[-1])
        self.assertTrue(length > 0)

# БЕНЧМАРКИ
def generate_test_graphs():
    test_graphs = {}
    
    # Маленькие графы: 5, 10, 15, 20 городов
    small_sizes = [5, 10, 15, 20]
    for size in small_sizes:
        vertices = [f"city_{i}" for i in range(size)]
        graph = TSPGraph(vertices, [])
        graph.generate_complete_graph(max_weight=100)
        test_graphs[size] = graph
    
    # Большие графы: 50, 100, 200 городов
    large_sizes = [50, 100, 200]
    for size in large_sizes:
        vertices = [f"city_{i}" for i in range(size)]
        graph = TSPGraph(vertices, [])
        graph.generate_complete_graph(max_weight=100)
        test_graphs[size] = graph
    
    return test_graphs

def run_benchmarks():
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
    print("\n" + "="*50)
    print("АНАЛИЗ РЕЗУЛЬТАТОВ")
    print("="*50)
    
    for result in results:
        size = result['size']
        improvement = ((result['greedy_length'] - result['local_length']) / 
                      result['greedy_length'] * 100) if result['greedy_length'] > 0 else 0
        
        # ИСПРАВЛЕНИЕ: проверяем деление на ноль
        if result['greedy_time'] > 0.000001:  # учитываем очень маленькие значения
            time_ratio = result['local_time'] / result['greedy_time']
        else:
            time_ratio = float('inf')  # бесконечность если greedy_time почти 0
        
        print(f"\nРазмер {size}:")
        print(f"  Улучшение качества: {improvement:.2f}%") #на сколько 2-opt алгоритм улучшил решение жадного алгоритма
        print(f"  Время 2-opt / Жадный: {time_ratio:.2f}x") #насколько 2-opt медленнее жадного алгоритма
        
        # Дополнительная информация для очень быстрых алгоритмов
        if result['greedy_time'] < 0.0001:
            print(f"  Примечание: время жадного алгоритма < 0.1ms")

# ЗАПУСК
if __name__ == "__main__":
    print("ЗАПУСК ТЕСТОВ И СРАВНЕНИЯ ПРОИЗВОДИТЕЛЬНОСТИ TSP")
    print("="*50)
    
    # Запуск тестов
    print("\nЗапуск тестов...")
    unittest.main(argv=[''], exit=False, verbosity=1)
    
    print("\n" + "="*50)
    print("ЗАПУСК СРАВНЕНИЯ")
    print("="*50)
    
    # Запуск бенчмарков
    results = run_benchmarks()
    analyze_results(results)

    #качество решения - длина маршрута
    print("\n" + "="*50)
    print("ВЫВОДЫ:")
    print("="*50)
    print("1. Жадный алгоритм работает очень быстро даже для больших графов")
    print("2. 2-opt значительно улучшает качество решения (особенно для больших графов)")
    print("3. Для маленьких графов время работы может быть меньше 1ms")
    print("4. 2-opt требует больше времени, но даёт лучшие результаты")