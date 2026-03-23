def data_types():
    integer = 1
    string = "This is string"
    floating = 1.0
    boolean = True
    its_a_list = ["This", "Is", "A", "List"]
    dictionary = {"It's": "A Dictionary"}
    its_a_tuple = ("One part of tuple", "Second part of tuple")
    its_a_set = {"This", "Is", "A", "Set"}
    print(f"[{type(integer).__name__}, {type(string).__name__}, {type(floating).__name__}, {type(boolean).__name__}, {type(its_a_list).__name__}, {type(dictionary).__name__}, {type(its_a_tuple).__name__}, {type(its_a_set).__name__}]")

if __name__ == '__main__':
      data_types()
