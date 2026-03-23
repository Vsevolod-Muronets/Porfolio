def making_constructor():
    import sys
    import os
    
    if len(sys.argv) != 2:
        print("Wrong number of arguments. Correct usage: python3 first_constructor.py <file_path>")
        return

    file_pth = sys.argv[1]

    class Research:
        def __init__(self, file_pth):
            self.file_pth = file_pth

        def file_reader(self):
            content = []
            try:
                if not os.path.exists(self.file_pth):
                    raise FileNotFoundError(f"Not found: {self.file_path}")
                file = open(self.file_pth, 'r')
                lines = file.readlines()
                if len(lines) < 2:
                    raise ValueError("Not enough lines for .csv")
                header = lines[0].strip().split(',')
                if len(header) != 2 or not all(isinstance(h, str) for h in header) \
                        or all(h.isdigit() for h in header):
                    raise ValueError("Wrong header format")
                content.append(lines[0].strip())
                for line in lines[1:]:
                    values = line.strip().split(',')
                    if len(values) != 2 or not all(v in ['0', '1'] for v in values) \
                            or all(v in ['0', '0'] for v in values) or all(v in ['1', '1'] for v in values):
                        raise ValueError("Wrong data format")
                    content.append(line.strip())
                file.close()

            except FileNotFoundError as e:
                return [str(e)]
            except PermissionError:
                return [f"No permission: {self.file_path}"]
            except ValueError as e:
                return [f"File format error: {str(e)}"]
            except Exception as e:
                return [f"Unexpected error: {str(e)}"]
            
            return content

    research = Research(file_pth)
    csv_content = research.file_reader()
    for line in csv_content:
        print(line)

if __name__ == "__main__":
    making_constructor()
