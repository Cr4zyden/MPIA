
import time
import timeit
from typing import List, Set
from dataclasses import dataclass

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
    
    #print("Running tests...")
    
    # TEST_CASE("Empty", "factivity!")
    def test_empty():
        I = []
        result = get_max_activities(I)
        assert to_set(result) == to_set(I), f"Empty test failed: {result}"
        #print("✓ Empty test passed")
    
    # TEST_CASE("one activity", "factivity!")
    def test_one_activity():
        I = [Activity(2, 3)]
        result = get_max_activities(I)
        assert to_set(result) == to_set(I), f"One activity test failed: {result}"
        #print("✓ One activity test passed")
    
    # TEST_CASE("two compatibles", "factivity!")
    def test_two_compatibles():
        I = [Activity(3, 4), Activity(2, 3)]
        result = get_max_activities(I)
        expected = [Activity(2, 3), Activity(3, 4)]
        assert to_set(result) == to_set(expected), f"Two compatibles test failed: {result}"
        #print("✓ Two compatibles test passed")
    
    # TEST_CASE("two overlaps", "factivity!")
    def test_two_overlaps():
        I = [Activity(2, 5), Activity(3, 4)]
        result = get_max_activities(I)
        expected1 = [Activity(2, 5)]
        expected2 = [Activity(3, 4)]
        assert (to_set(result) == to_set(expected1) or 
                to_set(result) == to_set(expected2)), f"Two overlaps test failed: {result}"
        #print("✓ Two overlaps test passed")
    
    # TEST_CASE("two incompatibles", "factivity!")
    def test_two_incompatibles():
        I = [Activity(3, 6), Activity(2, 5)]
        result = get_max_activities(I)
        expected1 = [Activity(2, 5)]
        expected2 = [Activity(3, 6)]
        assert (to_set(result) == to_set(expected1) or 
                to_set(result) == to_set(expected2)), f"Two incompatibles test failed: {result}"
        #print("✓ Two incompatibles test passed")
    
    # TEST_CASE("three activities", "factivity!")
    def test_three_activities():
        I = [Activity(2, 6), Activity(1, 4), Activity(5, 8)]
        result = get_max_activities(I)
        expected = [Activity(1, 4), Activity(5, 8)]
        assert to_set(result) == to_set(expected), f"Three activities test failed: {result}"
        #print("✓ Three activities test passed")
    
    # TEST_CASE("Four activities", "factivity!")
    def test_four_activities():
        I = [Activity(2, 6), Activity(1, 4), Activity(7, 10), Activity(5, 8)]
        result = get_max_activities(I)
        expected1 = [Activity(1, 4), Activity(5, 8)]
        expected2 = [Activity(2, 6), Activity(7, 10)]
        assert (to_set(result) == to_set(expected1) or 
                to_set(result) == to_set(expected2)), f"Four activities test failed: {result}"
        #print("✓ Four activities test passed")
    
    # TEST_CASE("Five activities", "factivity!")
    def test_five_activities():
        I = [Activity(2, 6), Activity(1, 4), Activity(7, 10), Activity(5, 8), Activity(9, 12)]
        result = get_max_activities(I)
        expected = [Activity(1, 4), Activity(5, 8), Activity(9, 12)]
        assert to_set(result) == to_set(expected), f"Five activities test failed: {result}"
        #print("✓ Five activities test passed")
    
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
        #print("✓ Big one test passed")
    
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
        #print("\n🎉 All tests passed!")
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")

def compare_algorithms():
    """Сравнение жадного алгоритма с полным перебором на маленьких наборах"""
    print("\n" + "="*50)
    print("Сравнение алгоритмов на маленьких наборах:")
    
    test_cases = [
        ([Activity(2, 3)], "Один процесс"),
        ([Activity(3, 4), Activity(2, 3)], "Два совместимых"),
        ([Activity(2, 5), Activity(3, 4)], "Два перекрывающихся"),
        ([Activity(1, 4), Activity(2, 6), Activity(5, 8)], "Три процесса"),
    ]
    
    for i, (activities, description) in enumerate(test_cases, 1):
        print(f"\nТест {i}: {description}")
        print(f"Процессы: {activities}")
        
        # Жадный алгоритм (много итераций для точного измерения)
        greedy_time = measure_time(get_max_activities, activities, number=10000)
        result_greedy = get_max_activities(activities)
        
        # Полный перебор (меньше итераций т.к. медленнее)
        if len(activities) <= 4:  # Только для маленьких наборов
            brute_time = measure_time(get_max_activities_brute_force, activities, number=10)
            result_brute = get_max_activities_brute_force(activities)
        else:
            brute_time = float('inf')
            result_brute = "N/A"
        
        print(f"Жадный алгоритм: {result_greedy}")
        print(f"Время жадного: {greedy_time:.8f} секунд")
        
        if brute_time != float('inf'):
            print(f"Полный перебор: {result_brute}")
            print(f"Время перебора: {brute_time:.6f} секунд")
            print(f"Результаты совпадают: {to_set(result_greedy) == to_set(result_brute)}")
            if brute_time > 0:
                speedup = brute_time / greedy_time
                print(f"Ускорение: {speedup:.1f} раз")
        else:
            print("Полный перебор: слишком долго для этого набора")

def performance_test():
    """Тест производительности на больших наборах данных"""
    print("\n" + "="*50)
    print("Тест производительности на больших наборах:")
    
    # Генерация больших наборов данных
    import random
    
    sizes = [10, 50, 100, 500, 1000]
    
    for size in sizes:
        # Генерируем случайные активности
        activities = []
        for _ in range(size):
            start = random.randint(0, size * 2)
            finish = start + random.randint(1, 10)
            activities.append(Activity(start, finish))
        
        print(f"\nРазмер набора: {size} процессов")
        
        # Измеряем время выполнения жадного алгоритма
        start_time = time.perf_counter()
        result = get_max_activities(activities)
        end_time = time.perf_counter()
        
        execution_time = end_time - start_time
        print(f"Выбрано процессов: {len(result)}")
        print(f"Время выполнения: {execution_time:.6f} секунд")
        
        # Показываем несколько выбранных процессов для примера
        if len(result) > 0:
            sample = result[:3] if len(result) > 3 else result
            print(f"Пример выбранных: {sample}")

def main():
    """Основная функция"""
    print("Тестирование алгоритма выбора максимального множества совместимых процессов")
    print("=" * 60)
    
    # Запуск тестов из скриншота
    run_tests()
    
    # Сравнение алгоритмов
    compare_algorithms()
    
    # Тест производительности
    performance_test()
    
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
