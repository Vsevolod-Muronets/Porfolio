def call_center(clients, recipients):
    cl_set = set(clients)
    recip_set = set(recipients)
    return list(cl_set - recip_set)

def potential_clients(participants, clients):
    partic_set = set(participants)
    cl_set = set(clients)
    return list(partic_set - cl_set)

def loyalty_program(clients, participants):
    cl_set = set(clients)
    partic_set = set(participants)
    return list(cl_set - partic_set)

def working_on_sets():
    import sys

    if len(sys.argv) != 2:
        return

    task = sys.argv[1]
    clients = ['andrew@gmail.com', 'jessica@gmail.com', 'ted@mosby.com',
               'john@snow.is', 'bill_gates@live.com', 'mark@facebook.com',
               'elon@paypal.com', 'jessica@gmail.com']
    participants = ['walter@heisenberg.com', 'vasily@mail.ru',
                    'pinkman@yo.org', 'jessica@gmail.com', 'elon@paypal.com',
                    'pinkman@yo.org', 'mr@robot.gov', 'eleven@yahoo.com']
    recipients = ['andrew@gmail.com', 'jessica@gmail.com', 'john@snow.is']
    error_flag = 1
    if task == "call_center":
        result = call_center(clients, recipients)
    elif task == "potential_clients":
        result = potential_clients(participants, clients)
    elif task == "loyalty_program":
        result = loyalty_program(clients, participants)
    else:
        raise ValueError("Invalid task name was given. You can use only: 'call_center', 'potential_clients', or 'loyalty_program'")
        error_flag = 0

    if error_flag == 1:
        print(result)

if __name__ == "__main__":
    working_on_sets()
