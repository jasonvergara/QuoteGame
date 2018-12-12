from bs4 import BeautifulSoup
from csv import DictWriter, DictReader
import requests
import random
import scrape_csv
import os.path


def is_right(guess, right_answer):
    if guess.lower() == right_answer.lower():
        print("You guessed correctly!")
        return True
    else:
        return False


def yes_or_no(game_prompt):
    valid = False
    while not valid:
        response = input(game_prompt)
        if response.lower() == 'y':
            return True
        elif response.lower() == 'n':
            return False
        else:
            print("Please input a valid response.")


def scrape_quotes():
    print('fetching data... please wait...')
    data = scrape_csv.scraped_quotes(base_url, url)
    with open('quotes.csv', 'w', newline='') as file:
        headers = ['quote', 'author', 'link']
        csv_writer = DictWriter(file, fieldnames=headers)
        csv_writer.writeheader()
        for quote in data:
            csv_writer.writerow(quote)


def read_quotes(filename):
    with open(filename, 'r') as file:
        csv_reader = DictReader(file)
        return list(csv_reader)



base_url = "http://quotes.toscrape.com"
url = '/page/1'

print('*** WHO SAID THAT? ***')

start_prompt = 'Would you like to update data (y/n)? '

if not os.path.isfile('quotes.csv'):
    scrape_quotes()
else:
    update = yes_or_no(start_prompt)
    if update:
        scrape_quotes()

data = read_quotes('quotes.csv')

play = True
count, score = 0, 0

while play:
    chance = 5
    count += 1
    check = False
    index = random.randrange(0, len(data))

    print(f"\n{count}. Who said this quote?\n{data[index]['quote']}")
    while chance > 0 and not check:
        if chance == 1:
            answer = input(f"You have {chance} remaining guess. ")
        else:
            answer = input(f"You have {chance} remaining guesses. ")

        check = is_right(answer, data[index]['author'])
        chance -= 1

        if check:
            score += 1
        else:
            if chance == 4:
                r = requests.get(f"{base_url}{data[index]['link']}")
                soup = BeautifulSoup(r.text, "html.parser")
                birth_date = soup.find('span', {'class', 'author-born-date'}).text
                birthplace = soup.find('span', {'class', 'author-born-location'}).text
                print(f"Hint #1: The author was born {birthplace} on {birth_date}.")
            elif chance == 3:
                print(f"Hint #2: The author's first name starts with {data[index]['author'][0]}.")
            elif chance == 2:
                print(f"Hint #3: The author's last name starts with {data[index]['author'].split(' ')[-1][0]}.")
            elif chance == 1:
                hint = ''
                name = data[index]['author']
                for char in name[1:len(name) - 1]:
                    if char == ' ':
                        hint += ' '
                    elif char == '.':
                        hint += '.'
                    else:
                        hint += '_'
                hint = name[0] + hint
                sliced = len(hint.split(' ')[-1])
                hint = hint[:-sliced] + name.split(' ')[-1][0] + hint[-sliced:]

                # names = data[index]['author'].split(' ')
                # hint = names[0][0]
                # for name in names[0:-1]:
                #     if name == names[0]:
                #         hint += '*' * (len(name) - 1) + ' '
                #     else:
                #         hint += '*' * (len(name)) + ' '
                # hint += names[-1][0] + '*' * (len(names[-1]) - 1)

                print(f"Hint #4: {hint}.")
            else:
                print(f"You've run out of guesses. The answer is {data[index]['author']}")

    print(f"Score: {score} out of {count}")
    prompt = "Would you like to play again (y/n)? "
    play = yes_or_no(prompt)
    if play:
        print('\nGet ready for the next round...')

print("Thank you for playing...")
