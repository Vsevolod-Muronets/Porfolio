def sum_loop(num_sq):
    tot_sum = 0
    for i in range(1, num_sq+1):
        tot_sum += i*i
    return tot_sum

def sum_reduce(num_sq):
    from functools import reduce
    return reduce(lambda a, i: a + i*i, range(1, num_sq+1), 0)

def check_if_faster():
    import timeit
    import sys
    sums = {"loop": sum_loop, "reduce": sum_reduce}
    if len(sys.argv) != 4:
        print("Корректное использование: python3 <путь>/benchmark.py <предпочитаемый фильтр> <количество повторений> <количество квадратов>")
        return
    s_name = sys.argv[1]
    if s_name not in sums:
        print(f"Метод суммирования {s_name} не найден")
        return
    try:
        num_it = int(sys.argv[2])
        if num_it <=0 : 
            raise ValueError
    except ValueError:
        print("Некорректное количество повторений (меньше 0)")
    try:
        num_sq = int(sys.argv[3])
        if num_sq<=0:
            raise ValueError
    except ValueError:
        print("Некорректное количество квадратов (меньше 0)")
        return
    pref_sum= sums[s_name]
    try:
        time = timeit.timeit(lambda: pref_sum(num_sq), number=num_it)
    except MemoryError:
        print("Ошибка: не хватает памяти для проверки")
        return
    except KeyboardInterrupt:
        print("\nПрервано пользователем (Ctrl+C).")
        return
    except Exception as e:
        print(f"Произошла непредвиденная ошибка во время проверки: {e}")
        return
    print(time)

if __name__ == '__main__':
    check_if_faster()
