def analysis():
    from random import randint
    import os
    import sys

    if len(sys.argv) != 2:
        print("Wrong number of arguments. Correct usage: python3 make_report.py <file_path>")
        return None, None
    file_pth = sys.argv[1]

    class Research:
        def __init__(self, file_pth):
            self.file_pth = file_pth

        def file_reader(self, has_header=True):
            data = []
            try:
                if not os.path.exists(self.file_pth):
                    raise FileNotFoundError(f"Not found: {self.file_pth}")
                with open(self.file_pth, 'r') as file:
                    lines = file.readlines()
                    if len(lines) < 1:
                        raise ValueError("Not enough lines")

                    start_line = 1 if has_header else 0

                    for line in lines[start_line:]:
                        values = line.strip().split(',')
                        if len(values) != 2 or not all(v in ['0', '1'] for v in values) \
                            or all(v in ['0', '0'] for v in values) or all (v in ['1', '1'] for v in values):
                            raise ValueError("Wrong data format")
                        data.append([int(values[0]), int(values[1])])

            except FileNotFoundError as exc:
                return [str(exc)]
            except PermissionError:
                return [f"No permission: {self.file_pth}"]
            except ValueError as exc:
                return [f"File format error: {str(exc)}"]
            except Exception as exc:
                return [f"Unexpected error: {str(exc)}"]

            return data

        class Calculations:
            def __init__(self, data):
                self.data = data

            def counts(self):
                heads = sum(row[0] for row in self.data if row[0] == 1)
                tails = sum(row[1] for row in self.data if row[1] == 1)
                return heads, tails

            def fractions(self, heads, tails):
                total = heads + tails
                return (heads / total * 100, tails / total * 100)

        class Analytics(Calculations):
            def predict_random(self, n):
                predictions = []
                for _ in range(n):
                    rand = randint(0, 1)
                    predictions.append([rand, 1 - rand])
                return predictions

            def predict_last(self):
                return self.data[-1]

            def save_file(self, data, filename, extension):
                try:
                    file = open(f"{filename}.{extension}", 'w')
                    for line in data:
                        file.write(str(line) + "\n")
                    file.close()
                except Exception as exc:
                    print(f"Error saving file: {exc}")
    
    return Research, file_pth 
