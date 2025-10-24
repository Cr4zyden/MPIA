import time
import timeit
from typing import List, Set
from dataclasses import dataclass
import random

# Структура для представления процесса с начальным и конечным временем
@dataclass
class Activity:
    start: int
    finish: int
    
    def __eq__(self, other):
        if not isinstance(other, Activity):
            return False
        return self.start == other.start and self.finish == other.finish
    
    def __hash__(self):
        return hash((self.start, self.finish))
    
    def __repr__(self):
        return f"({self.start}, {self.finish})"

# Вспомогательная функция для преобразования в множество
def to_set(activities: List[Activity]) -> Set[Activity]:
    return set(activities)

# Жадный алгоритм для поиска максимального множества совместимых процессов
def get_max_activities(activities: List[Activity]) -> List[Activity]:
    """
    Жадный алгоритм находит максимально возможное по размеру совместимое 
    подмножество процессов более эффективным способом.
    """
    if not activities:
        return []
    
    # Сортируем процессы по возрастанию времени завершения
    sorted_activities = sorted(activities, key=lambda x: x.finish)
    
    result = []
    current_finish = 0
    
    # Проходим по отсортированным процессам, добавляя совместимые процессы в результат
    for activity in sorted_activities:
        if activity.start >= current_finish:
            result.append(activity)
            current_finish = activity.finish
    
    return result

# Полный перебор для сравнения (только для маленьких наборов)
def get_max_activities_brute_force(activities: List[Activity]) -> List[Activity]:
    """
    Полный перебор для поиска максимального множества совместимых процессов.
    Используется только для проверки корректности жадного алгоритма.
    """
    n = len(activities)
    max_subset = []
    
    # Перебираем все возможные подмножества процессов
    for mask in range(1 << n):
        subset = []
        compatible = True

        # Формируем подмножество и проверяем его на совместимость
        for i in range(n):
            if mask & (1 << i):
                # Проверяем совместимость с последним добавленным процессом
                if subset and subset[-1].finish > activities[i].start:
                    compatible = False
                    break
                subset.append(activities[i])

        # Если подмножество совместимо и его размер больше текущего максимума, обновляем результат
        if compatible and len(subset) > len(max_subset):
            max_subset = subset

    return max_subset

def measure_time(func, *args, number=1000):
    """Измерение времени выполнения функции с повышенной точностью"""
    return timeit.timeit(lambda: func(*args), number=number) / number

# Тесты из скриншота
def run_tests():
    """Запуск всех тестов из скриншота"""
    
    print("Running tests...")
    
    # TEST_CASE("Empty", "factivity!")
    def test_empty():
        I = []
        result = get_max_activities(I)
        assert to_set(result) == to_set(I), f"Empty test failed: {result}"
        print("✓ Empty test passed")
    
    # TEST_CASE("one activity", "factivity!")
    def test_one_activity():
        I = [Activity(2, 3)]
        result = get_max_activities(I)
        assert to_set(result) == to_set(I), f"One activity test failed: {result}"
        print("✓ One activity test passed")
    
    # TEST_CASE("two compatibles", "factivity!")
    def test_two_compatibles():
        I = [Activity(3, 4), Activity(2, 3)]
        result = get_max_activities(I)
        expected = [Activity(2, 3), Activity(3, 4)]
        assert to_set(result) == to_set(expected), f"Two compatibles test failed: {result}"
        print("✓ Two compatibles test passed")
    
    # TEST_CASE("two overlaps", "factivity!")
    def test_two_overlaps():
        I = [Activity(2, 5), Activity(3, 4)]
        result = get_max_activities(I)
        expected1 = [Activity(2, 5)]
        expected2 = [Activity(3, 4)]
        assert (to_set(result) == to_set(expected1) or 
                to_set(result) == to_set(expected2)), f"Two overlaps test failed: {result}"
        print("✓ Two overlaps test passed")
    
    # TEST_CASE("two incompatibles", "factivity!")
    def test_two_incompatibles():
        I = [Activity(3, 6), Activity(2, 5)]
        result = get_max_activities(I)
        expected1 = [Activity(2, 5)]
        expected2 = [Activity(3, 6)]
        assert (to_set(result) == to_set(expected1) or 
                to_set(result) == to_set(expected2)), f"Two incompatibles test failed: {result}"
        print("✓ Two incompatibles test passed")
    
    # TEST_CASE("three activities", "factivity!")
    def test_three_activities():
        I = [Activity(2, 6), Activity(1, 4), Activity(5, 8)]
        result = get_max_activities(I)
        expected = [Activity(1, 4), Activity(5, 8)]
        assert to_set(result) == to_set(expected), f"Three activities test failed: {result}"
        print("✓ Three activities test passed")
    
    # TEST_CASE("Four activities", "factivity!")
    def test_four_activities():
        I = [Activity(2, 6), Activity(1, 4), Activity(7, 10), Activity(5, 8)]
        result = get_max_activities(I)
        expected1 = [Activity(1, 4), Activity(5, 8)]
        expected2 = [Activity(2, 6), Activity(7, 10)]
        assert (to_set(result) == to_set(expected1) or 
                to_set(result) == to_set(expected2)), f"Four activities test failed: {result}"
        print("✓ Four activities test passed")
    
    # TEST_CASE("Five activities", "factivity!")
    def test_five_activities():
        I = [Activity(2, 6), Activity(1, 4), Activity(7, 10), Activity(5, 8), Activity(9, 12)]
        result = get_max_activities(I)
        expected = [Activity(1, 4), Activity(5, 8), Activity(9, 12)]
        assert to_set(result) == to_set(expected), f"Five activities test failed: {result}"
        print("✓ Five activities test passed")
    
    # TEST_CASE("Big one", "factivity!")
    def test_big_one():
        I = [
            Activity(3, 5), Activity(1, 4), Activity(5, 7), Activity(0, 6),
            Activity(3, 9), Activity(5, 9), Activity(0, 11), Activity(4, 10),
            Activity(8, 12), Activity(2, 14), Activity(12, 16)
        ]
        result = get_max_activities(I)
        expected1 = [Activity(1, 4), Activity(5, 7), Activity(8, 12), Activity(12, 16)]
        expected2 = [Activity(3, 5), Activity(5, 7), Activity(8, 12), Activity(12, 16)]
        assert (to_set(result) == to_set(expected1) or 
                to_set(result) == to_set(expected2)), f"Big one test failed: {result}"
        print("✓ Big one test passed")
    
    # Запуск всех тестов
    try:
        test_empty()
        test_one_activity()
        test_two_compatibles()
        test_two_overlaps()
        test_two_incompatibles()
        test_three_activities()
        test_four_activities()
        test_five_activities()
        test_big_one()
        print("\n🎉 All tests passed!")
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")

def compare_algorithms_small():
    """Сравнение жадного алгоритма с полным перебором на маленьких наборах"""
    print("\n" + "="*50)
    print("Сравнение алгоритмов на маленьких наборах:")
    
    test_cases = [
        ([Activity(2, 3)], "Один процесс"),
        ([Activity(3, 4), Activity(2, 3)], "Два совместимых"),
        ([Activity(2, 5), Activity(3, 4)], "Два перекрывающихся"),
        ([Activity(1, 4), Activity(2, 6), Activity(5, 8)], "Три процесса"),
        ([Activity(1, 3), Activity(2, 4), Activity(3, 5), Activity(4, 6)], "Четыре процесса"),
    ]
    
    print(f"{'Тест':<15} {'Размер':<8} {'Жадный (сек)':<15} {'Перебор (сек)':<15} {'Ускорение':<12} {'Совпадают'}")
    print("-" * 80)
    
    for i, (activities, description) in enumerate(test_cases, 1):
        n = len(activities)
        
        # Жадный алгоритм (много итераций для точного измерения)
        greedy_time = measure_time(get_max_activities, activities, number=10000)
        result_greedy = get_max_activities(activities)
        
        # Полный перебор
        if n <= 15:  # Ограничиваем размер для полного перебора
            start_brute = time.perf_counter()
            result_brute = get_max_activities_brute_force(activities)
            end_brute = time.perf_counter()
            brute_time = end_brute - start_brute
            results_match = to_set(result_greedy) == to_set(result_brute)
        else:
            brute_time = float('inf')
            results_match = "N/A"
        
        speedup = brute_time / greedy_time if brute_time != float('inf') and greedy_time > 0 else float('inf')
        
        print(f"{description:<15} {n:<8} {greedy_time:<15.8f} ", end="")
        if brute_time != float('inf'):
            print(f"{brute_time:<15.6f} {speedup:<12.1f} {results_match}")
        else:
            print(f"{'∞':<15} {'∞':<12} {results_match}")

def compare_algorithms_large():
    """Сравнение времени на больших наборах данных"""
    print("\n" + "="*50)
    print("Сравнение алгоритмов на больших наборах:")
    print(f"{'Размер':<8} {'Жадный (сек)':<15} {'Перебор (сек)':<20} {'Ускорение':<15} {'Выбрано':<10}")
    print("-" * 80)
    
    # Тестируем на разных размерах
    sizes = [5, 10, 12, 15, 18, 20, 25]
    
    for size in sizes:
        # Генерируем случайные активности
        activities = []
        for i in range(size):
            start = random.randint(0, size * 3)
            finish = start + random.randint(1, size // 2 + 2)
            activities.append(Activity(start, finish))
        
        # Жадный алгоритм
        start_greedy = time.perf_counter()
        result_greedy = get_max_activities(activities)
        end_greedy = time.perf_counter()
        greedy_time = end_greedy - start_greedy
        
        # Полный перебор (только для небольших размеров)
        if size <= 20:
            start_brute = time.perf_counter()
            result_brute = get_max_activities_brute_force(activities)
            end_brute = time.perf_counter()
            brute_time = end_brute - start_brute
            selected = len(result_greedy)
        else:
            brute_time = float('inf')
            selected = len(result_greedy)
        
        speedup = brute_time / greedy_time if brute_time != float('inf') and greedy_time > 0 else float('inf')
        
        print(f"{size:<8} {greedy_time:<15.8f} ", end="")
        if brute_time != float('inf'):
            print(f"{brute_time:<20.6f} {speedup:<15.1f} {selected:<10}")
        else:
            print(f"{'∞ (>60 сек)':<20} {'∞':<15} {selected:<10}")

def performance_analysis():
    """Анализ производительности с теоретическими расчетами"""
    print("\n" + "="*50)
    print("Теоретический анализ производительности:")
    print(f"{'Размер':<8} {'2^n':<15} {'n*log(n)':<15} {'Отношение':<15} {'Ожидаемое время':<20}")
    print("-" * 80)
    
    sizes = [5, 10, 15, 20, 25, 30, 50, 100]
    
    for size in sizes:
        # Теоретическая сложность
        brute_complexity = 2 ** size
        greedy_complexity = size * (size.bit_length() if size > 0 else 1)  # n*log(n) для сортировки
        
        if size <= 30:
            ratio = brute_complexity / greedy_complexity if greedy_complexity > 0 else float('inf')
            
            # Оценочное время (предполагая 1 наносекунда на операцию)
            est_brute_sec = brute_complexity * 1e-9
            est_greedy_sec = greedy_complexity * 1e-9
            
            print(f"{size:<8} {brute_complexity:<15} {greedy_complexity:<15} {ratio:<15.1f} ", end="")
            
            if est_brute_sec < 60:
                print(f"{est_brute_sec:<8.3f} сек / {est_greedy_sec:<8.3f} сек")
            elif est_brute_sec < 3600:
                print(f"{est_brute_sec/60:<8.3f} мин / {est_greedy_sec:<8.3f} сек")
            elif est_brute_sec < 86400:
                print(f"{est_brute_sec/3600:<8.3f} час / {est_greedy_sec:<8.3f} сек")
            else:
                print(f"{est_brute_sec/86400:<8.3f} дн / {est_greedy_sec:<8.3f} сек")
        else:
            ratio = brute_complexity / greedy_complexity if greedy_complexity > 0 else float('inf')
            print(f"{size:<8} {brute_complexity:<15} {greedy_complexity:<15} {ratio:<15.1e} {'∞':<20}")

def performance_test_large_greedy():
    """Тест производительности жадного алгоритма на очень больших наборах"""
    print("\n" + "="*50)
    print("Тест производительности жадного алгоритма на больших наборах:")
    print(f"{'Размер':<10} {'Время (сек)':<15} {'Выбрано':<10} {'Плотность (%)':<15}")
    print("-" * 60)
    
    sizes = [100, 500, 1000, 5000, 10000, 50000, 100000]
    
    for size in sizes:
        # Генерируем случайные активности
        activities = []
        for i in range(size):
            start = random.randint(0, size)
            finish = start + random.randint(1, min(100, size // 10 + 5))
            activities.append(Activity(start, finish))
        
        start_time = time.perf_counter()
        result = get_max_activities(activities)
        end_time = time.perf_counter()
        
        execution_time = end_time - start_time
        selected_count = len(result)
        density = (selected_count / size) * 100
        
        print(f"{size:<10} {execution_time:<15.6f} {selected_count:<10} {density:<15.2f}")

def main():
    """Основная функция"""
    print("Тестирование алгоритма выбора максимального множества совместимых процессов")
    print("=" * 80)
    
    # Запуск тестов из скриншота
    run_tests()
    
    # Сравнение алгоритмов на маленьких наборах
    compare_algorithms_small()
    
    # Сравнение алгоритмов на больших наборах
    compare_algorithms_large()
    
    # Теоретический анализ
    performance_analysis()
    
    # Тест производительности жадного алгоритма на очень больших наборах
    performance_test_large_greedy()
    
    # Демонстрация на оригинальном примере
    print("\n" + "="*50)
    print("Демонстрация на оригинальном примере:")
    activities = [
        Activity(1, 4), Activity(3, 5), Activity(0, 6), Activity(5, 7), 
        Activity(3, 8), Activity(5, 9), Activity(6, 10), Activity(8, 11), 
        Activity(8, 12), Activity(2, 13), Activity(12, 14)
    ]
    
    start_time = time.perf_counter()
    result = get_max_activities(activities)
    end_time = time.perf_counter()
    
    print(f"Всего процессов: {len(activities)}")
    print(f"Выбрано процессов: {len(result)}")
    print(f"Время выполнения: {(end_time - start_time):.8f} секунд")
    print("Выбранные процессы:")
    for activity in result:
        print(f"  Start: {activity.start}, Finish: {activity.finish}")

if __name__ == "__main__":
    main()
