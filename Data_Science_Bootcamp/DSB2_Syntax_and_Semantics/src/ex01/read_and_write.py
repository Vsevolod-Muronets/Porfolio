def csv_to_tsv():
    inp_file = 'ds.csv'
    outp_file = 'ds.tsv'
    inp_from_file =  open(inp_file, mode='r')
    outp_from_file =  open(outp_file, mode='w')
    for line in inp_from_file:
        in_quotes = False
        new_line = []
        for char in line:
            if char == '"':
                in_quotes = not in_quotes
            elif char == ',' and not in_quotes:
                char = '\t'
            new_line.append(char)
        outp_from_file.write(''.join(new_line) + '\n')
    inp_from_file.close()
    outp_from_file.close()

if __name__ == '__main__':
    csv_to_tsv()
