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


def display_options(shows):
    for show in shows:
        if (show.get('tickets') != 'SOLD OUT'):
            # made the assumption that we will not show sold out shows
            print(f"{show.get('artist')} with {show.get('opener')}")
            print(
                f"\t${show.get('price')} on {show.get('date')} at {show.get('show')}\n")


def get_user_choice(shows):
    valid_options = []
    for show in shows:
        valid_options.append(show.get('artist'))

    print('Which artist would you like to see?')
    while True:
        name = input('>>> ').strip()
        if name in valid_options:
            return name
        else:
            print('Sorry!', name, 'is not a valid option.')


def get_single_show(shows, artist_name):
    # this could be done in main, but i extracted it for simplification
    for show in shows:
        if show.get('artist') == artist_name:
            return show


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
    display_options(shows)
    user_name = input('What is your name? ')
    artist_name = get_user_choice(shows)
    show = get_single_show(shows, artist_name)
    code = show.get('code')
    # explicitly naming this for clarity
    # single purchase to meets the requirements to pass
    number_of_tickets = 1
    price = number_of_tickets * show.get('price')
    tax = price * SALES_TAX
    print(f"${(price + tax):.2f} to see {artist_name}, thank you!")
    save_transaction(user_name, artist_name, code,
                     number_of_tickets, price, tax)
    update_shows(show, number_of_tickets)
    save_shows(shows, SHOWS_FILE)


if __name__ == '__main__':
    main()
