
def read_csv_with_class():
    class Must_read:
        file = 'data.csv'

        try:
            csv_file = open(file, 'r')
            try:
                for line in csv_file:
                    print(line.strip())
            except Exception as e:
                print("Could not read:", e)
            finally:
                csv_file.close()
        except FileNotFoundError:
            print("Not found:", file)
        except PermissionError:
            print("No permission for:", file)
        except Exception as e:
            print("Unexpected error:", e)

if __name__ == '__main__':
    read_csv_with_class()
