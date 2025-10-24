import time
import random
UNIT_TESTS = [[1, 2, 3],  [4, -5, 1, 0, 3], [-5, -5, 0, 2, 3, 3, 8], [4, 2, 4, -1, 0, 3, -1], [4, -2, 5, 0, 2, 120, 11, 6, -3, -67, 9, -21, 11]]
N = [10, 100, 1000, 10000, 100000]
def measure_time(func):
    start = time.perf_counter()
    result = func()
    end = time.perf_counter()
    return end - start

def generate_tests(n):
    return [random.randint(-100, 100) for _ in range(n)]

def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])

    right = merge_sort(arr[mid:])
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    
    return result + left[i:] + right[j:]

def check_unit_tests():
    if all(merge_sort(arr) == sorted(arr) for arr in UNIT_TESTS):
        print("Все предложенные юнит-тесты пройдены успешно")

def check_n_tests(n):
    merge_time = 0
    sort_time = 0
    arr = generate_tests(n)
    merge_time = measure_time(lambda: merge_sort(arr))
    sort_time = measure_time(lambda:sorted (arr))
    print(f'{str(n):<8} {str(sort_time):<50} {str(merge_time):<50}')
if __name__ == '__main__':
    print(f'{"N":<8} {"Время стандартной сортировки":<50} {"Время сортировки слиянием":<50}')
    print("-" * 100)
    for n in N:
        check_n_tests(n)
    check_unit_tests()