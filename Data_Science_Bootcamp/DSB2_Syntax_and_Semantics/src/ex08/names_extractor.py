def extract_name():
    import sys

    if len(sys.argv) != 2:
        return

    file_with_emails = sys.argv[1]
    file_opened = open(file_with_emails, 'r')
    emails = file_opened.readlines()
    file_opened.close()
    outp_file = open('employees.tsv', 'w')
    outp_file.write("Name\tSurname\tE-mail\n")    
    for email in emails:
            email = email.strip()  
            if email:
                username, mail = email.split('@')
                name, surn = username.split('.')
                name = name.capitalize()
                surn = surn.capitalize()
                outp_file.write(f"{name}\t{surn}\t{email}\n")
    outp_file.close()

if __name__ == "__main__":
    extract_name()
