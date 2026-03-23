def filter_loop(emails):
    result=[]
    for email in emails:
        if email.endswith("@gmail.com"):
            result.append(email)
    return result

def filter_lcompr(emails):
    return [email for email in emails if email.endswith("gmail.com")]

def filter_map(emails):
    return list(map(lambda e: e if e.endswith("@gmail.com") else None, emails))

def filter_f(emails):
    return list(filter(lambda e: e.endswith("@gmail.com"), emails))

def check_if_faster():
    import timeit
    import sys
    filters = {"loop": filter_loop, "list_comprehension": filter_lcompr, 
               "map": filter_map, "filter": filter_f}
    initial = ['john@gmail.com', 'james@gmail.com', 'alice@yahoo.com', 'anna@live.com', 'philipp@gmail.com']
    emails = [em for em in initial for _ in range(5)]
    if len(sys.argv) != 3:
        print("Корректное использование: python3 <путь>/benchmark.py <предпочитаемый фильтр> <количество повторений>")
        return
    f_name = sys.argv[1]
    if f_name not in filters:
        print(f"Фильтр {f_name} не найден")
        return
    try:
        num = int(sys.argv[2])
        if num <=0 : 
            raise ValueError
    except ValueError:
        print("Некорректное количество повторений (меньше 0)")
    pref_filt = filters[f_name]
    try:
        time = timeit.timeit(lambda: pref_filt(emails), number=num)
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
