def inheritance():
    import sys
    from random import randint
    
    if len(sys.argv) != 2:
        print("Wrong number of arguments. Correct usage: python3 first_nest.py <file_path>")
        return

    file_pth = sys.argv[1]
    class Research:
        def __init__(self, file_pth):
            self.file_pth = file_pth

        def file_reader(self, has_header=True):
            data = []
            try:
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
                for i in range(n):
                    rand = randint(0, 1)
                    predictions.append([rand, 1 - rand])
                return predictions

            def predict_last(self):
                return self.data[-1]

    research = Research(file_pth)
    
    data = research.file_reader()
    
    if not data or isinstance(data[0], str):
        print(data)
        return

    print(data)

    analytics = research.Analytics(data)
    heads, tails = analytics.counts()
    print(heads, tails)

    head_fraction, tail_fraction = analytics.fractions(heads, tails)
    print(head_fraction, tail_fraction)

    predictions = analytics.predict_random(3)
    print(predictions)

    last = analytics.predict_last()
    print(last)

if __name__ == "__main__":
    inheritance()
