#include <iostream>
#include <vector>
#include <string>
#include <random>
#include <algorithm>
#include <numeric>
#include <chrono>
#include <iomanip>

// Настройки
#define DEFAULT_SIZE 256  

// Выберите ОДИН из контейнеров при компиляции:
// -DVECTOR   или   -DLIST   или   -DSET   или   -DU_SET

#ifdef LIST
    #include <list>
#endif
#ifdef SET
    #include <set>
#endif
#ifdef U_SET
    #include <unordered_set>
#endif

using namespace std;
using namespace std::chrono;

// === Генерация данных ===
vector<int> random_sequence(int size, int max_val);
vector<unsigned long> shuffled_sequence(unsigned long size, unsigned long start = 1);

int main() {
    cout << fixed << setprecision(8);

    // === Вывод информации о контейнере ===
#if defined(VECTOR)
    vector<unsigned long> container;
    cout << "\nVECTOR TESTING\n\n";
    cout << "PUSH_BACK: O(1) amortized [realloc: O(n)]\n";
    cout << "PUSH_FRONT: O(n)\n";
    cout << "FIND (std::find): O(n)\n\n";

#elif defined(LIST)
    list<unsigned long> container;
    cout << "\nLIST TESTING\n\n";
    cout << "PUSH_BACK: O(1)\n";
    cout << "PUSH_FRONT: O(1)\n";
    cout << "FIND (std::find): O(n)\n\n";

#elif defined(SET)
    set<unsigned long> container;
    cout << "\nSET TESTING\n\n";
    cout << "INSERT: O(log n)\n";
    cout << "FIND: O(log n)\n\n";

#elif defined(U_SET)
    unordered_set<unsigned long> container;
    cout << "\nUNORDERED_SET TESTING\n\n";
    cout << "INSERT: O(1) average, O(n) worst case\n";
    cout << "FIND: O(1) average, O(n) worst case\n\n";
#endif

    cout << string(80, '-') << endl;

    // === Параметры тестирования ===
    unsigned long size = DEFAULT_SIZE;
    bool insert_done = false, search_done = false;
    const auto elems_to_search = random_sequence(1000, 50000);  // 1000 случайных чисел для поиска
    vector<unsigned long> elems_to_add;

    // === Объявление типа для времени ===
    using duration_t = duration<double>;

#if defined(VECTOR) || defined(LIST)
    cout << "=== PUSH_BACK AND SEARCH TEST ===\n\n";
    cout << setw(12) << "N"
         << setw(18) << "INSERT_TIME (s)"
         << setw(18) << "SEARCH_TIME (s)"
         << setw(10) << "HITS" << endl;
    cout << string(60, '-') << endl;

    while (!insert_done) {
        elems_to_add = shuffled_sequence(size);

        // --- Тест: вставка в конец ---
        auto t1 = steady_clock::now();
        for (const auto& elem : elems_to_add) {
            container.push_back(elem);
        }
        auto t2 = steady_clock::now();
        double insert_time = duration_cast<duration_t>(t2 - t1).count();

        cout << setw(12) << size
             << setw(18) << insert_time;

        // --- Тест: поиск ---
        if (!search_done && insert_time < 4.0) {
            int hits = 0;
            t1 = steady_clock::now();
            for (const auto& elem : elems_to_search) {
                auto it = find(container.begin(), container.end(), elem);
                if (it != container.end()) {
                    hits++;
                }
            }
            t2 = steady_clock::now();
            double search_time = duration_cast<duration_t>(t2 - t1).count();

            cout << setw(18) << search_time
                 << setw(10) << hits << endl;

            if (search_time >= 4.0) {
                search_done = true;
            }
        } else {
            cout << setw(18) << "SKIPPED"
                 << setw(10) << "-" << endl;
        }

        // --- Подготовка к следующей итерации ---
        container.clear();
        elems_to_add.clear();

#if defined(VECTOR)
        vector<unsigned long>().swap(container);  // Полная очистка памяти
#else
        // Для list clear() уже освобождает всю память
#endif

        if (insert_time >= 2.0) {
            insert_done = true;
        } else {
            size *= 2;
        }
    }

    // === PUSH_FRONT TEST (только для vector и list) ===
    cout << "\n" << string(80, '-') << endl;
    cout << "=== PUSH_FRONT TEST ===\n\n";
    cout << setw(12) << "N" << setw(18) << "TIME (s)" << endl;
    cout << string(30, '-') << endl;

    insert_done = false;
    size = DEFAULT_SIZE;
    while (!insert_done) {
        elems_to_add = shuffled_sequence(size);

        auto t1 = steady_clock::now();
        for (const auto& elem : elems_to_add) {
            container.insert(container.begin(), elem);  // push_front аналог
        }
        auto t2 = steady_clock::now();
        double time = duration_cast<duration_t>(t2 - t1).count();

        cout << setw(12) << size << setw(18) << time << endl;

        container.clear();
#if defined(VECTOR)
        vector<unsigned long>().swap(container);
#endif

        if (time >= 2.0) {
            insert_done = true;
        } else {
            size *= 2;
        }
    }

#elif defined(SET) || defined(U_SET)
    cout << "=== INSERT AND FIND TEST ===\n\n";
    cout << setw(12) << "N"
         << setw(18) << "INSERT_TIME (s)"
         << setw(18) << "SEARCH_TIME (s)"
         << setw(10) << "HITS" << endl;
    cout << string(60, '-') << endl;

    while (!insert_done) {
        elems_to_add = shuffled_sequence(size);

        // --- Тест: вставка ---
        auto t1 = steady_clock::now();
        for (const auto& elem : elems_to_add) {
            container.insert(elem);
        }
        auto t2 = steady_clock::now();
        double insert_time = duration_cast<duration_t>(t2 - t1).count();

        cout << setw(12) << size
             << setw(18) << insert_time;

        // --- Тест: поиск ---
        if (!search_done && insert_time < 4.0) {
            int hits = 0;
            t1 = steady_clock::now();
            for (const auto& elem : elems_to_search) {
                auto it = container.find(elem);
                if (it != container.end()) {
                    hits++;
                }
            }
            t2 = steady_clock::now();
            double search_time = duration_cast<duration_t>(t2 - t1).count();

            cout << setw(18) << search_time
                 << setw(10) << hits << endl;

            if (search_time >= 4.0) {
                search_done = true;
            }
        } else {
            cout << setw(18) << "SKIPPED"
                 << setw(10) << "-" << endl;
        }

        // --- Очистка ---
        container.clear();
#if defined(SET)
        set<unsigned long>().swap(container);
#elif defined(U_SET)
        unordered_set<unsigned long>().swap(container);
#endif
        elems_to_add.clear();

        if (insert_time >= 2.0) {
            insert_done = true;
        } else {
            size *= 2;
        }
    }
#endif

    cout << "\n✅ Testing completed.\n";
    return 0;
}

// === Реализация функций генерации ===

vector<int> random_sequence(int size, int max_val) {
    static mt19937 rng(random_device{}());
    uniform_int_distribution<int> dist(1, max_val);
    vector<int> result;
    result.reserve(size);
    for (int i = 0; i < size; ++i) {
        result.push_back(dist(rng));
    }
    return result;
}

vector<unsigned long> shuffled_sequence(unsigned long size, unsigned long start) {
    vector<unsigned long> result(size);
    iota(result.begin(), result.end(), start);
    static mt19937 rng(random_device{}());
    shuffle(result.begin(), result.end(), rng);
    return result;
}