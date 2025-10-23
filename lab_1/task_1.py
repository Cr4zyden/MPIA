import time
import random
from collections import deque

# === Генерация данных ===
def generate_shuffled_sequence(n: int) -> list:
    """Генерирует перемешанную последовательность от 1 до n."""
    seq = list(range(1, n + 1))
    random.shuffle(seq)
    return seq

def generate_random_queries(count: int, max_val: int = 50000) -> list:
    """Генерирует k случайных чисел для поиска."""
    return [random.randint(1, max_val) for _ in range(count)]

# === Измерение времени ===
def measure_time(func):
    start = time.perf_counter()
    result = func()
    end = time.perf_counter()
    return result, end - start

# === Основной бенчмарк ===
def main():
    print(" BENCHMARK: ALL DATA STRUCTURES")
    print("=" * 160)

    # Значения N
    N_VALUES = [10, 100, 1000, 10000, 100000]
    SEARCH_COUNT = 500  # k = 500

    # Заголовок таблицы
    print(f"{'N':<8} {'Структура':<20} {'append':<20} {'insert':<20} {'Обход':<20} {'Поиск':<20}")
    print("-" * 160)

    for N in N_VALUES:
        data = generate_shuffled_sequence(N)
        search_queries = generate_random_queries(SEARCH_COUNT)

        # --- 1. vector (list) ---
        container_list = []
        _, append_time_list = measure_time(lambda: container_list.extend(data))

        container_list_insert = []
        _, insert_time_list = measure_time(lambda: [container_list_insert.insert(0, x) for x in data])

        _, traverse_time_list = measure_time(lambda: sum(container_list))

        hits_list = 0
        start_search = time.perf_counter()
        for q in search_queries:
            if q in container_list:
                hits_list += 1
        search_time_list = time.perf_counter() - start_search

        print(f"{N:<8} {'list (vector)':<20} "
              f"{append_time_list:<20.6e} "
              f"{insert_time_list:<20.6e} "
              f"{traverse_time_list:<20.6e} "
              f"{search_time_list:<20.6e}k = {SEARCH_COUNT}")

        # --- 2. list (deque) — двусвязный список ---
        container_deque = deque()
        _, append_time_deque = measure_time(lambda: [container_deque.append(x) for x in data])

        container_deque_insert = deque()
        _, insert_time_deque = measure_time(lambda: [container_deque_insert.appendleft(x) for x in data])

        _, traverse_time_deque = measure_time(lambda: sum(container_deque))

        hits_deque = 0
        start_search = time.perf_counter()
        for q in search_queries:
            if q in container_deque:
                hits_deque += 1
        search_time_deque = time.perf_counter() - start_search

        print(f"{N:<8} {'deque (list)':<20} "
              f"{append_time_deque:<20.6e} "
              f"{insert_time_deque:<20.6e} "
              f"{traverse_time_deque:<20.6e} "
              f"{search_time_deque:<20.6e}k = {SEARCH_COUNT}")

        # --- 3. set (упорядоченное множество — на самом деле неупорядоченное, но с O(log n)) ---
        container_set = set()
        _, insert_time_set = measure_time(lambda: [container_set.add(x) for x in data])

        # Для set нет "append", так как он неупорядоченный — используем insert
        append_time_set = insert_time_set  # условно

        _, traverse_time_set = measure_time(lambda: sum(container_set))

        hits_set = 0
        start_search = time.perf_counter()
        for q in search_queries:
            if q in container_set:
                hits_set += 1
        search_time_set = time.perf_counter() - start_search

        print(f"{N:<8} {'set':<20} "
              f"{append_time_set:<20.6e} "
              f"{'—':<20} "
              f"{traverse_time_set:<20.6e} "
              f"{search_time_set:<20.6e}k = {SEARCH_COUNT}")

        # --- 4. unordered_set (dict) — хеш-таблица ---
        container_dict = {}
        _, insert_time_dict = measure_time(lambda: [container_dict.setdefault(x, None) for x in data])

        append_time_dict = insert_time_dict  # условно

        _, traverse_time_dict = measure_time(lambda: sum(container_dict.keys()))

        hits_dict = 0
        start_search = time.perf_counter()
        for q in search_queries:
            if q in container_dict:
                hits_dict += 1
        search_time_dict = time.perf_counter() - start_search

        print(f"{N:<8} {'dict (unordered_set)':<20} "
              f"{append_time_dict:<20.6e} "
              f"{'—':<20} "
              f"{traverse_time_dict:<20.6e} "
              f"{search_time_dict:<20.6e}k = {SEARCH_COUNT}")

        print()  # пустая строка между N

    # === Теоретическая часть ===
    print("=" * 160)
    print("📌 ТЕОРЕТИЧЕСКАЯ ОЦЕНКА ВРЕМЕННОЙ СЛОЖНОСТИ:")
    print()
    print("• list (vector):")
    print("   - append: O(1) амортизированно → O(N)")
    print("   - insert(0): O(n) → O(N²)")
    print("   - обход: O(N)")
    print("   - поиск: O(N)")
    print()
    print("• deque (list):")
    print("   - append: O(1)")
    print("   - insert(0): O(1)")
    print("   - обход: O(N)")
    print("   - поиск: O(N)")
    print()
    print("• set:")
    print("   - insert: O(log n)")
    print("   - обход: O(N)")
    print("   - поиск: O(log n)")
    print()
    print("• dict (unordered_set):")
    print("   - insert: O(1) среднее")
    print("   - обход: O(N)")
    print("   - поиск: O(1) среднее")
    print()
    print("Выводы:")
    print("   - list: append быстро, insert(0) медленно при больших N.")
    print("   - deque: insert(0) и append — оба O(1), но поиск всё ещё O(N).")
    print("   - set: вставка и поиск — O(log n), эффективнее list при поиске.")
    print("   - dict: вставка и поиск — O(1) среднее, самый быстрый для поиска.")
    print("   - Для частого поиска — всегда выбирайте set или dict.")

if __name__ == "__main__":
    main()