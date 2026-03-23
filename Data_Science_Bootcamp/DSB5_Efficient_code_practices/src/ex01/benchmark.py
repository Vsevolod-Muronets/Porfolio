def filter_loop(emails):
    result=[]
    for email in emails:
        if email.endswith("@gmail.com"):
            result.append(email)
    return result

def filter_lcompr(emails):
    return [email for email in emails if email.endswith("@gmail.com")]

def filter_map(emails):
    return list(map(lambda e: e if e.endswith("@gmail.com") else None, emails))

def check_if_faster(number=90000000):
    import timeit
    initial = ['john@gmail.com', 'james@gmail.com', 'alice@yahoo.com', 'anna@live.com', 'philipp@gmail.com']
    emails = [em for em in initial for _ in range(5)]
    try:
        time_l = timeit.timeit(lambda: filter_loop(emails), number=number)
        time_lcomp = timeit.timeit(lambda: filter_lcompr(emails), number=number)
        time_map = timeit.timeit(lambda: filter_map(emails), number=number)
    except MemoryError:
        print("Ошибка: не хватает памяти для проверки")
        return
    except KeyboardInterrupt:
        print("\nПрервано пользователем (Ctrl+C).")
        return
    except Exception as e:
        print(f"Произошла непредвиденная ошибка во время проверки: {e}")
        return
    if time_lcomp <= time_l and time_lcomp <= time_map:
            print("It is better to use a list comprehension")
    elif time_lcomp >= time_l and time_l <= time_map:
        print("It is better to use a loop")
    else:
        print("It is better to use a map")

    fastest = sorted([time_l, time_lcomp, time_map])
    print(f"{fastest[0]} vs {fastest[1]} vs {fastest[2]}")

if __name__ == '__main__':
    check_if_faster()
