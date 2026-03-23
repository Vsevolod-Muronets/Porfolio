def get_name_from_email(email):
        emails_file = open('employees.tsv', 'r')
        lines = emails_file.readlines()
        emails_file.close()

        for line in lines[1:]:
            name, surn, email_adr = line.strip().split('\t')
            if email_adr == email:
                return name

def generate_letter():
    import sys

    if len(sys.argv) != 2:
        return

    email = sys.argv[1]
    name = get_name_from_email(email)
    if name:
        letter = f"Dear {name}, welcome to our team. We are sure that it will be a pleasure to work with you. That’s a precondition for the professionals that our company hires."
        print(letter)

if __name__ == "__main__":
    letter = generate_letter()
    
