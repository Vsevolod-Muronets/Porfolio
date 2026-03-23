def nested_classes():
    import sys
    import os

    if len(sys.argv) != 2:
        print("Wrong number of arguments. Correct usage: python3 first_nest.py <file_pth>")
        return

    file_pth = sys.argv[1]
    
    class Research:

        def __init__(self, file_pth):
            self.file_pth = file_pth

        def file_reader(self, has_header=True): 
            data = []
            try:
                if not os.path.exists(self.file_pth):
                    raise FileNotFoundError(f"Not found: {self.file_pth}")
                file = open(self.file_pth, 'r')
                lines = file.readlines()
                if len(lines) < 1:
                    raise ValueError("Not enough lines")
                first_line = lines[0].strip().split(',')
                if all(v in ['0', '1'] for v in first_line):
                    has_header = False
                start_line = 1 if has_header else 0
                for line in lines[start_line:]:
                    values = line.strip().split(',')
                    if len(values) != 2 or not all(v in ['0', '1'] for v in values) \
                            or all(v in ['0', '0'] for v in values) or all (v in ['1', '1'] for v in values):
                        raise ValueError("Wrong data format")
                    data.append([int(values[0]), int(values[1])])
                file.close()

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

            def counts(self,data):
                heads = sum(row[0] for row in data if row[0] == 1)
                tails = sum(row[1] for row in data if row[1] == 1)
                return heads, tails

            def fractions(self, heads, tails):
                total = heads + tails
                return (heads / total * 100, tails / total * 100)


    research = Research(file_pth)            
    data = research.file_reader()
    print(data)

    calc = Research.Calculations()
    heads, tails = calc.counts(data)
    print(heads, tails)

    head_fraction, tail_fraction = calc.fractions(heads, tails)
    print(head_fraction, tail_fraction)


if __name__ == "__main__":
   nested_classes() 
