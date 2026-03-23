def class_and_method():
    class Research:
        file_pth = '../ex00/data.csv'

        def file_reader(self):
            content = []
            try:
                file = open(self.file_pth, 'r')
                try:
                    for line in file:
                        content.append(line.strip())  
                except Exception as exc:
                    return ["Could not read: " + str(exc)]
                finally:
                    file.close()
            except FileNotFoundError:
                return ["Not found: " + self.file_pth]
            except PermissionError:
                return ["No permission for: " + self.file_pth]
            except Exception as exc:
                return ["Unexpected error: " + str(exc)]
            return content
    
    research = Research()
    csv_content = research.file_reader()
    for line in csv_content:
        print(line)

if __name__ == '__main__':
    class_and_method()
