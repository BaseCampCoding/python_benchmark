# this example COMPLETES THE ASSIGNMENT
# this is my solution to PASS the assignment
from json import load, dump
from datetime import datetime
# additional imports if needed

# global variables
SHOWS_FILE = './shows.json'
TRANSACTIONS_FILE = './transactions.txt'
TICKET_FILE = './ticket.txt'
SALES_TAX = 0.07  # 7% Sales Tax


def get_shows(SHOWS_FILE):
    with open(SHOWS_FILE, 'r') as file:
        shows = load(file)
    return shows


def display_options_and_get_valid_options(shows):
    valid_options = set()
    # iterating by index to make choices easier
    for i in range(len(shows)):
        show = shows[i]
        # displaying valid and invalid options
        if (show.get('tickets') != 'SOLD OUT'):
            option = str(i + 1)
            valid_options.add(option)
        else:
            option = 'X'
        print(f"{option} - {show.get('artist')} with {show.get('opener')}")
        print(
            f"\t${show.get('price')} on {show.get('date')} at {show.get('show')}\n")
    return valid_options


def get_user_choice(shows, valid_options):
    print('Choose the number of the artist you would like to see. (or q to quit)')
    while True:
        n = input('\t>>> ').strip().lower()
        if n in valid_options:
            index = int(n) - 1
            return index
        elif n == 'q':
            print('Sorry to see you go, please come back later!')
            exit()
        else:
            print('Sorry!', n, 'is not a valid option.')


def get_number_tickets(tickets_remaining):
    print('How many tickets would you like? there are',
          tickets_remaining, 'tickets left. (Maximum of 4, or q to quit)')
    while True:
        string_tickets = input('\t>>> ').lower().strip()
        if string_tickets.isdigit():
            tickets = int(string_tickets)
            if tickets <= 4 and tickets <= tickets_remaining:
                return tickets
            else:
                print('too many tickets selected')
        elif string_tickets == 'q':
            print('Sorry to see you leave. Please come back later!')
        else:
            print('invalid choice!')


def make_ticket(show, number_of_tickets):
    ticket = f"""==================================================
]                 THE JEFFERSON                  [
]                  featuring...                  [
]                                                [
]{show.get('artist').upper().center(48)}[
]{('with ' + show.get('opener')).center(48)}[
]{show.get('date').center(48)}[
]{('Doors: ' + show.get('doors') + ', Show: ' + show.get('show')).center(48)}[
]                                                [
]{('Admit: ' + str(number_of_tickets) + ', Code: ' + show.get('code')).center(48)}[
=================================================="""
    return ticket


def save_ticket(ticket):
    with open(TICKET_FILE, 'w') as file:
        file.write(ticket)


def save_transaction(user_name, artist_name, code, number_of_tickets, price, tax):
    line = f'\n{user_name}, {artist_name}, {code}, {number_of_tickets}, ${price:.2f}, ${tax:.2f}, {datetime.now()}'
    with open(TRANSACTIONS_FILE, 'a') as file:
        file.write(line)
    return None


def update_shows(show, number_of_tickets):
    show['tickets'] = show['tickets'] - number_of_tickets
    if show['tickets'] < 1:
        show['tickets'] = 'SOLD OUT'


def save_shows(shows, filename):
    with open(filename, 'w') as file:
        dump(shows, file)


def main():
    print('Welcome to The Jefferson venue ticket purchasing tool!\n')
    # this is where the code you write goes
    shows = get_shows(SHOWS_FILE)
    valid_options = display_options_and_get_valid_options(shows)
    user_name = input('What is your name? ')
    index = get_user_choice(shows, valid_options)
    show = shows[index]

    artist_name = show.get('artist')
    code = show.get('code')

    number_of_tickets = get_number_tickets(show.get('tickets'))
    price = number_of_tickets * show.get('price')
    tax = price * SALES_TAX
    print(f"${(price + tax):.2f} to see {artist_name}, thank you!")

    ticket = make_ticket(show, number_of_tickets)
    print(ticket)
    save_ticket(ticket)

    save_transaction(user_name, artist_name, code,
                     number_of_tickets, price, tax)
    update_shows(show, number_of_tickets)
    save_shows(shows, SHOWS_FILE)


if __name__ == '__main__':
    main()
