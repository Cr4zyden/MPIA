import time
import random

# === Генерация данных ===
def generate_random_array(n: int, max_val: int = 10000) -> list:
    """Генерирует массив из n случайных целых чисел."""
    return [random.randint(1, max_val) for _ in range(n)]

# === Медленные функции (O(N²)) ===
def has_duplicates_slow(arr: list) -> bool:
    """Проверяет наличие дубликатов полным перебором пар."""
    n = len(arr)
    for i in range(n):
        for j in range(i + 1, n):
            if arr[i] == arr[j]:
                return True
    return False

def get_duplicates_slow(arr: list) -> list:
    """Возвращает список всех уникальных дубликатов (по одному на значение)."""
    duplicates = []
    n = len(arr)
    for i in range(n):
        for j in range(i + 1, n):
            if arr[i] == arr[j]:
                # Если ещё не добавляли этот дубликат
                if arr[i] not in duplicates:
                    duplicates.append(arr[i])
                break  # Не нужно искать другие вхождения этого элемента
    return duplicates

# === Быстрые функции (O(N)) ===
def has_duplicates_fast(arr: list) -> bool:
    """Проверяет наличие дубликатов через set."""
    seen = set()
    for x in arr:
        if x in seen:
            return True
        seen.add(x)
    return False

def get_duplicates_fast(arr: list) -> list:
    """Возвращает список всех уникальных дубликатов через set."""
    seen = set()
    duplicates = set()
    for x in arr:
        if x in seen:
            duplicates.add(x)
        else:
            seen.add(x)
    return list(duplicates)

# === Юнит-тесты ===
def run_tests():
    print("Running unit tests...")

    # Тест 1: нет дубликатов
    a1 = [1, 2, 3, 4, 5]
    assert not has_duplicates_slow(a1)
    assert not has_duplicates_fast(a1)
    assert get_duplicates_slow(a1) == []
    assert get_duplicates_fast(a1) == []

    # Тест 2: есть дубликаты
    a2 = [1, 2, 3, 2, 4, 3]
    assert has_duplicates_slow(a2)
    assert has_duplicates_fast(a2)
    d_slow = sorted(get_duplicates_slow(a2))
    d_fast = sorted(get_duplicates_fast(a2))
    assert d_slow == d_fast

    # Тест 3: все одинаковые
    a3 = [5, 5, 5, 5]
    assert has_duplicates_slow(a3)
    assert has_duplicates_fast(a3)
    assert len(get_duplicates_slow(a3)) == 1
    assert len(get_duplicates_fast(a3)) == 1

    # Тест 4: пустой массив
    a4 = []
    assert not has_duplicates_slow(a4)
    assert not has_duplicates_fast(a4)
    assert get_duplicates_slow(a4) == []
    assert get_duplicates_fast(a4) == []

    print("All tests passed.\n")

# === Измерение времени ===
def measure_time(func, *args):
    start = time.perf_counter()
    result = func(*args)
    end = time.perf_counter()
    return result, end - start

# === Основной бенчмарк ===
def main():
    print("DUPLICATES ALGORITHM BENCHMARK")
    print("=" * 80)

    run_tests()

    # Значения N
    N_VALUES = [10, 100, 1000, 10000]

    # Заголовок таблицы
    print(f"{'N':<8} {'has_slow (s)':<15} {'has_fast (s)':<15} {'get_slow (s)':<15} {'get_fast (s)':<15}")
    print("-" * 80)

    for N in N_VALUES:
        data = generate_random_array(N)

        # --- has_duplicates_slow ---
        _, time_has_slow = measure_time(has_duplicates_slow, data)

        # --- has_duplicates_fast ---
        _, time_has_fast = measure_time(has_duplicates_fast, data)

        # --- get_duplicates_slow ---
        _, time_get_slow = measure_time(get_duplicates_slow, data)

        # --- get_duplicates_fast ---
        _, time_get_fast = measure_time(get_duplicates_fast, data)

        print(f"{N:<8} "
              f"{time_has_slow:<15.6e} "
              f"{time_has_fast:<15.6e} "
              f"{time_get_slow:<15.6e} "
              f"{time_get_fast:<15.6e}")

    # === Теоретическая часть ===
    print("\n" + "=" * 80)
    print("ТЕОРЕТИЧЕСКАЯ ОЦЕНКА ВРЕМЕННОЙ СЛОЖНОСТИ:")
    print()
    print("• has_duplicates_slow / get_duplicates_slow: O(N²)")
    print("   - Перебор всех пар → N*(N-1)/2 операций")
    print("   - При увеличении N в 10 раз — время растёт в ~100 раз")
    print()
    print("• has_duplicates_fast / get_duplicates_fast: O(N)")
    print("   - Используется set → каждая операция O(1) среднее")
    print("   - При увеличении N в 10 раз — время растёт в ~10 раз")
    print()
    print("Выводы:")
    print("   - Медленные алгоритмы работают хорошо при малых N (<100), но становятся неприемлемыми при N>1000.")
    print("   - Быстрые алгоритмы масштабируются линейно — даже при N=10000 работают за доли секунды.")

if __name__ == "__main__":
    main()