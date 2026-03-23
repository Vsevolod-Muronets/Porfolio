def my_func(nums):
    counts = {}
    for num in nums:
        if num in counts:
            counts[num]+=1
        else:
            counts[num]=1
    return counts

def top_10(nums):
    counts = my_func(nums)
    sorting = sorted(counts.items(), key=lambda x: x[1], reverse=True)
    return sorting[:10]

def check_if_faster():
    import timeit
    import random
    from collections import Counter
    try:
        nums = [random.randint(0, 100) for _ in range(10**6)]
        t_my_count = timeit.timeit(lambda: my_func(nums), number = 1)
        t_counter = timeit.timeit(lambda: Counter(nums), number = 1)
        t_top10_mine = timeit.timeit(lambda: top_10(nums), number = 1)
        t_top10_counter = timeit.timeit(lambda: Counter(nums).most_common(10), number = 1)
    except MemoryError:
        print("Ошибка: не хватает памяти для проверки")
        return
    except KeyboardInterrupt:
        print("\nПрервано пользователем (Ctrl+C).")
        return
    except Exception as e:
        print(f"Произошла непредвиденная ошибка во время проверки: {e}")
        return
    print(f"my function: {t_my_count}\nCounter: {t_counter}\nmy top: {t_top10_mine}\nCounter's top: {t_top10_counter}")

if __name__ == '__main__':
    check_if_faster()
