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
    # Используем timeit для более точных измерений
    timer = timeit.Timer(lambda: func(*args))
    time_taken = timer.timeit(number=number) / number
    return time_taken

def test_lcs(X: str, Y: str) -> None:
    """
    Тестирование и замер времени выполнения с улучшенными измерениями
    """
    print(f"X = '{X}' (длина: {len(X)}), Y = '{Y}' (длина: {len(Y)})")
    
    # Для коротких строк используем больше итераций
    if len(X) <= 10:
        iterations = 10
    else:
        iterations = 1
    
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
    print("Тестирование LCS с различными длинами строк:")
    print("=" * 50)
    
    # Тест 1: Оригинальные короткие строки
    print("Тест 1: Короткие строки")
    X1 = "ABCBDAB"
    Y1 = "BDCAB"
    test_lcs(X1, Y1)
    
    # Тест 2: Средние строки
    print("Тест 2: Средние строки")
    X2 = generate_random_string(12, "ABCD")
    Y2 = generate_random_string(10, "ABCD")
    test_lcs(X2, Y2)
    
    # Тест 3: Длинные строки (только динамическое программирование)
    print("Тест 3: Длинные строки")
    X3 = generate_random_string(100, "ABCD")
    Y3 = generate_random_string(100, "ABCD")
    print(f"X = [строка длиной {len(X3)}], Y = [строка длиной {len(Y3)}]")
    
    start_dp = time.perf_counter()
    result_dp = lcs_dynamic_programming(X3, Y3)
    end_dp = time.perf_counter()
    dp_time = end_dp - start_dp
    
    print(f"Dynamic Programming LCS: [результат длиной {len(result_dp)}], Time: {dp_time:.6f} seconds")
    print(f"LCS: '{result_dp[:50]}...'")  # Показываем только первые 50 символов
    
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

