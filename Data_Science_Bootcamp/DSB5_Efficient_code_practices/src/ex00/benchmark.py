def filter_loop(emails):
    result=[]
    for email in emails:
        if email.endswith("@gmail.com"):
            result.append(email)
    return result

def filter_lcompr(emails):
    return [email for email in emails if email.endswith("@gmail.com")]

def check_if_faster(number=90000000):
    import timeit
    initial = ['john@gmail.com', 'james@gmail.com', 'alice@yahoo.com', 'anna@live.com', 'philipp@gmail.com']
    emails = [em for em in initial for _ in range(5)]
    try:
        time_l = timeit.timeit(lambda: filter_loop(emails), number=number)
        time_lcomp = timeit.timeit(lambda: filter_lcompr(emails), number=number)
    except MemoryError:
        print("Ошибка: не хватает памяти для проверки")
        return
    except KeyboardInterrupt:
        print("\nПрервано пользователем (Ctrl+C).")
        return
    except Exception as e:
        print(f"Произошла непредвиденная ошибка во время проверки: {e}")
        return
    if time_lcomp <= time_l:
        print(f"It is better to use a list comprehension\n{time_lcomp} vs {time_l}")
    else:
        print(f"It is better to use a loop\n{time_l} vs {time_lcomp}")

if __name__ == '__main__':
    check_if_faster()
