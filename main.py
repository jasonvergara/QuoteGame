from bs4 import BeautifulSoup
import requests
import random


def is_right(guess, right_answer):
    if guess.lower() == right_answer.lower():
        print("You guessed correctly!")
        return True
    else:
        return False


def play_again():
    valid = False
    while not valid:
        response = input("Would you like to play again (y/n)? ")
        if response.lower() == 'y':
            return True
        elif response.lower() == 'n':
            return False
        else:
            print("Please input a valid response.")


base_url = "http://quotes.toscrape.com"
url = '/page/1'
r = requests.get(f"{base_url}{url}")
soup = BeautifulSoup(r.text, "html.parser")
quotes = soup.find_all('div', {'class': 'quote'})

data = []

for quote in quotes:
    quote_text = quote.find('span', {'class': 'text'}).text
    quote_author = quote.find('small', {'class': 'author'}).text
    author_link = quote.find('a')['href']
    data.append({'quote': quote_text,
                 'author': quote_author,
                 'link': author_link})

play = True

while play:
    chance = 5
    check = False
    index = random.randrange(0, len(data))

    print(f"Who said this quote?\n{data[index]['quote']}")
    while chance > 0 and not check:
        if chance == 1:
            answer = input(f"You have {chance} remaining guess. ")
        else:
            answer = input(f"You have {chance} remaining guesses. ")

        check = is_right(answer, data[index]['author'])
        chance -= 1

        if not check:
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

    play = play_again()
    if play:
        print('\nGet ready for the next round...\n')

print("Thank you for playing...")