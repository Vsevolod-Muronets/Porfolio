def r_lines(f_pth):
    with open(f_pth, 'r') as file:
        lines = file.readlines()
    return lines
    
def check_if_cheaper():
    import sys
    import os
    import resource
    if len(sys.argv) != 2:
        print("Корректное использование: python3 <путь>/ordinary.py <путь к файлу с данными>")
        return
    f_pth = sys.argv[1]
    if not os.path.exists(f_pth):
        print(f"Файл не найден: {f_pth}")
        return
    try:
        for _ in r_lines(f_pth):
            pass
        usage = resource.getrusage(resource.RUSAGE_SELF)
        mem = usage.ru_maxrss / (1024 ** 2)
        cpu = usage.ru_utime + usage.ru_stime
        print(f"Peak Memory Usage = {mem: .3f} GB")
        print(f"User Mode Time + System Mode Time = {cpu: .2f}s")
    except MemoryError:
        print("Ошибка: не хватает памяти")
        return
    except KeyboardInterrupt:
        print("\nПрервано пользователем (Ctrl+C).")
        return
    except Exception as e:
        print(f"Произошла непредвиденная ошибка: {e}")
        return
    

if __name__ == '__main__':
    check_if_cheaper()