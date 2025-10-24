import time
import timeit
from typing import List, Tuple
import random

def lcs_brute_force(X: str, Y: str) -> str:
    """
    Функция полного перебора для поиска LCS
    """
    max_length = 0
    longest_subsequence = ""
    
    n = len(X)
    # Перебираем все возможные подпоследовательности X
    for mask in range(1, 1 << n):
        subsequence = ""
        # Формируем подпоследовательность на основе битовой маски
        for i in range(n):
            if mask & (1 << i):
                subsequence += X[i]
        
        # Проверяем, является ли полученная подпоследовательность подпоследовательностью Y
        pos = 0
        valid = True
        for ch in subsequence:
            pos = Y.find(ch, pos)
            if pos == -1:
                valid = False
                break
            pos += 1
        
        # Если подпоследовательность валидна и ее длина больше максимальной, обновляем результат
        if valid and len(subsequence) > max_length:
            max_length = len(subsequence)
            longest_subsequence = subsequence
    
    return longest_subsequence

def lcs_dynamic_programming(X: str, Y: str) -> str:
    """
    Функция динамического программирования для поиска LCS
    """
    N = len(X)
    M = len(Y)
    
    # Создаем таблицу для хранения длин подпоследовательностей
    LCS = [[0] * (M + 1) for _ in range(N + 1)]
    
    # Заполняем таблицу LCS по формуле
    for i in range(1, N + 1):
        for j in range(1, M + 1):
            if X[i - 1] == Y[j - 1]:
                LCS[i][j] = LCS[i - 1][j - 1] + 1
            else:
                LCS[i][j] = max(LCS[i - 1][j], LCS[i][j - 1])
    
    # Восстанавливаем LCS из таблицы
    result = []
    i, j = N, M
    while i > 0 and j > 0:
        if X[i - 1] == Y[j - 1]:
            result.append(X[i - 1])
            i -= 1
            j -= 1
        elif LCS[i - 1][j] > LCS[i][j - 1]:
            i -= 1
        else:
            j -= 1
    
    # Поскольку мы добавляли символы с конца, переворачиваем строку
    return ''.join(reversed(result))

def generate_random_string(length: int, chars: str = "ABCD") -> str:
    """Генерация случайной строки заданной длины"""
    return ''.join(random.choice(chars) for _ in range(length))

def measure_time(func, *args, number=1):
    """Измерение времени выполнения функции с повышенной точностью"""
    timer = timeit.Timer(lambda: func(*args))
    time_taken = timer.timeit(number=number) / number
    return time_taken

def compare_algorithms_table():
    """Красивая таблица сравнения алгоритмов"""
    print("\n" + "="*80)
    print("ТАБЛИЦА СРАВНЕНИЯ АЛГОРИТМОВ ПОИСКА LCS")
    print("="*80)
    print(f"{'Длина X':<8} {'Длина Y':<8} {'Brute Force (сек)':<20} {'Dynamic Prog (сек)':<20} {'Ускорение':<15} {'Длина LCS':<10}")
    print("-"*80)
    
    test_cases = [
        (5, 5),
        (8, 8),
        (10, 10),
        (12, 12),
        (15, 15),
        (20, 20),
        (50, 50),
        (100, 100),
        (500, 500),
        (1000, 1000),
    ]
    
    for len_x, len_y in test_cases:
        # Генерируем случайные строки
        X = generate_random_string(len_x, "ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        Y = generate_random_string(len_y, "ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        
        # Динамическое программирование
        start_dp = time.perf_counter()
        result_dp = lcs_dynamic_programming(X, Y)
        end_dp = time.perf_counter()
        dp_time = end_dp - start_dp
        lcs_length = len(result_dp)
        
        # Полный перебор (только для маленьких строк)
        if len_x <= 15:
            start_brute = time.perf_counter()
            result_brute = lcs_brute_force(X, Y)
            end_brute = time.perf_counter()
            brute_time = end_brute - start_brute
            speedup = brute_time / dp_time if dp_time > 0 else float('inf')
        else:
            brute_time = float('inf')
            speedup = float('inf')
        
        print(f"{len_x:<8} {len_y:<8} ", end="")
        if brute_time != float('inf'):
            print(f"{brute_time:<20.6f} {dp_time:<20.8f} {speedup:<15.1f} {lcs_length:<10}")
        else:
            print(f"{'∞ (>60 сек)':<20} {dp_time:<20.8f} {'∞':<15} {lcs_length:<10}")

def performance_analysis_lcs():
    """Теоретический анализ производительности LCS"""
    print("\n" + "="*80)
    print("ТЕОРЕТИЧЕСКИЙ АНАЛИЗ ПРОИЗВОДИТЕЛЬНОСТИ LCS")
    print("="*80)
    print(f"{'Длина':<8} {'2^n':<20} {'n*m':<15} {'Отношение':<20} {'Ожидаемое время':<25}")
    print("-"*80)
    
    sizes = [5, 10, 15, 20, 25, 30, 50, 100, 500, 1000]
    
    for size in sizes:
        # Теоретическая сложность
        brute_complexity = 2 ** size
        dp_complexity = size * size  # n*m для динамического программирования
        
        ratio = brute_complexity / dp_complexity if dp_complexity > 0 else float('inf')
        
        # Оценочное время (предполагая 1 наносекунда на операцию)
        est_brute_sec = brute_complexity * 1e-9
        est_dp_sec = dp_complexity * 1e-9
        
        print(f"{size:<8} {brute_complexity:<20} {dp_complexity:<15} {ratio:<20.1e} ", end="")
        
        if est_brute_sec < 60:
            print(f"{est_brute_sec:<10.3f} сек / {est_dp_sec:<10.3f} сек")
        elif est_brute_sec < 3600:
            print(f"{est_brute_sec/60:<10.3f} мин / {est_dp_sec:<10.3f} сек")
        elif est_brute_sec < 86400:
            print(f"{est_brute_sec/3600:<10.3f} час / {est_dp_sec:<10.3f} сек")
        else:
            print(f"{est_brute_sec/86400:<10.3f} дн / {est_dp_sec:<10.3f} сек")

def test_extreme_cases_table():
    """Таблица тестирования крайних случаев"""
    print("\n" + "="*80)
    print("ТЕСТИРОВАНИЕ КРАЙНИХ СЛУЧАЕВ")
    print("="*80)
    print(f"{'Тест':<15} {'X':<20} {'Y':<20} {'LCS':<20} {'Время DP (сек)':<15}")
    print("-"*80)
    
    test_cases = [
        ("Пустые строки", "", ""),
        ("X пустая", "", "qwer"),
        ("Y пустая", "qwer", ""), 
        ("Идентичные", "qwer", "qwer"), 
        ("X содержит Y", "erer", "er"),  
        ("Нет общих", "erfgvb", "ythgnb"),
        ("Случайные 1", "banderol", "hlopyshkaa"),
        ("Случайные 2", "dj1udjrua", "au21ea"),
        ("Частичное совпад.", "sury21aieyhd", "au21ea"),
        ("Разные длины", "iuytrew", "rewpoiuohy"),
    ]
    
    for test_name, test_X, test_Y in test_cases:
        start_time = time.perf_counter()
        result = lcs_dynamic_programming(test_X, test_Y)
        end_time = time.perf_counter()
        dp_time = end_time - start_time
        
        # Обрезаем длинные строки для красивого вывода
        x_display = test_X if len(test_X) <= 15 else test_X[:12] + "..."
        y_display = test_Y if len(test_Y) <= 15 else test_Y[:12] + "..."
        lcs_display = result if len(result) <= 15 else result[:12] + "..."
        
        print(f"{test_name:<15} {x_display:<20} {y_display:<20} {lcs_display:<20} {dp_time:<15.8f}")

def performance_large_scale():
    """Тест производительности на очень больших строках"""
    print("\n" + "="*80)
    print("ТЕСТ ПРОИЗВОДИТЕЛЬНОСТИ НА БОЛЬШИХ СТРОКАХ")
    print("="*80)
    print(f"{'Длина X':<10} {'Длина Y':<10} {'Время DP (сек)':<15} {'Длина LCS':<10} {'Память (MB)':<12}")
    print("-"*80)
    
    large_cases = [
        (500, 500),
        (1000, 1000),
        (2000, 2000),
        (5000, 5000),
        (10000, 10000),
    ]
    
    for len_x, len_y in large_cases:
        X = generate_random_string(len_x, "ACGT")  # ДНК-последовательности
        Y = generate_random_string(len_y, "ACGT")
        
        start_time = time.perf_counter()
        result = lcs_dynamic_programming(X, Y)
        end_time = time.perf_counter()
        
        execution_time = end_time - start_time
        lcs_length = len(result)
        
        # Оценка использования памяти (n * m * 4 байта для int)
        memory_mb = (len_x + 1) * (len_y + 1) * 4 / (1024 * 1024)
        
        print(f"{len_x:<10} {len_y:<10} {execution_time:<15.6f} {lcs_length:<10} {memory_mb:<12.2f}")

def test_lcs(X: str, Y: str) -> None:
    """
    Тестирование и замер времени выполнения с улучшенными измерениями
    """
    print(f"X = '{X}' (длина: {len(X)}), Y = '{Y}' (длина: {len(Y)})")
    
    # Замер времени для полного перебора
    try:
        if len(X) > 15:  # Полный перебор слишком медленный для длинных строк
            print("Brute Force: слишком долго для строк такой длины")
            brute_time = float('inf')
            result_brute = "N/A"
        else:
            start_brute = time.perf_counter()
            result_brute = lcs_brute_force(X, Y)
            end_brute = time.perf_counter()
            brute_time = end_brute - start_brute
            print(f"Brute Force LCS: '{result_brute}', Time: {brute_time:.6f} seconds")
    except Exception as e:
        print(f"Brute Force error: {e}")
        brute_time = float('inf')
        result_brute = "N/A"
    
    # Замер времени для динамического программирования
    start_dp = time.perf_counter()
    result_dp = lcs_dynamic_programming(X, Y)
    end_dp = time.perf_counter()
    dp_time = end_dp - start_dp
    
    print(f"Dynamic Programming LCS: '{result_dp}', Time: {dp_time:.9f} seconds")
    
    # Сравнение производительности
    if brute_time != float('inf') and brute_time > 0:
        speedup = brute_time / dp_time if dp_time > 0 else float('inf')
        print(f"Динамическое программирование быстрее в {speedup:.1f} раз")
    print()

def main():
    """Основная функция"""
    print("ТЕСТИРОВАНИЕ АЛГОРИТМОВ ПОИСКА НАИБОЛЬШЕЙ ОБЩЕЙ ПОДПОСЛЕДОВАТЕЛЬНОСТИ")
    print("="*80)
    
    # 1. Сравнительная таблица алгоритмов
    compare_algorithms_table()
    
    # 2. Теоретический анализ
    performance_analysis_lcs()
    
    # 3. Тестирование крайних случаев
    test_extreme_cases_table()
    
    # 4. Производительность на больших строках
    performance_large_scale()
    
    # 5. Детальные тесты из оригинального кода
    print("\n" + "="*80)
    print("ДЕТАЛЬНЫЕ ТЕСТЫ ИЗ ОРИГИНАЛЬНОГО КОДА")
    print("="*80)
    
    # Тест 1: Оригинальные короткие строки
    print("\nТест 1: Короткие строки")
    X1 = "ABCBDAB"
    Y1 = "BDCAB"
    test_lcs(X1, Y1)
    
    # Тест 2: Средние строки
    print("Тест 2: Средние строки")
    X2 = generate_random_string(12, "ABCD")
    Y2 = generate_random_string(10, "ABCD")
    test_lcs(X2, Y2)
    
    # Тест 3: Крайние случаи
    print("\nТест 3: Крайние случаи")
    test_cases = [
        ("", ""),
        ("", "qwer"),
        ("qwer", ""), 
        ("qwer", "qwer"), 
        ("erer", "er"),  
        ("erfgvb", "ythgnb"),
        ("banderol", "hlopyshkaa"),
        ("dj1udjrua", "au21ea"),
        ("sury21aieyhd", "au21ea"),
        ("iuytrew", "rewpoiuohy"),
    ]
    
    for i, (test_X, test_Y) in enumerate(test_cases, 1):
        print(f"\nКрайний случай {i}:")
        test_lcs(test_X, test_Y)

if __name__ == "__main__":
    main()
