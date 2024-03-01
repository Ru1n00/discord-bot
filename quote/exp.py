# import necessary libraries
import requests
from bs4 import BeautifulSoup
import random
import lxml

# function to get a quote by a popular person
def get_quote(person, category):
    # get quote by the given person
    url = f'https://en.wikipedia.org/wiki/{person}' # to check if the article exists for the given person
    response = requests.get(url)
    print(response)
    if response.status_code == 200:
        # if the article exists, extract quotes
        soup = BeautifulSoup(response.content, 'lxml')
        quotes = []
        for quote_div in soup.find_all(class_='summary'):
            quote = quote_div.find('p', {'class': 'lead'})
            if quote:
                quotes.append(quote.text)
        print(quotes)
        if category in quotes:
            # if the quote contains the given category, print it
            print(quotes[len(quotes) - 1])
        else:
            print("The category {} not found in the article's quotes.".format(category))
    else:
        print("The person {} does not have a Wikipedia article.".format(person))

# function to get a random category
def get_random_category():
    categories = ['motivation', 'success', 'life', 'love']
    return random.choice(categories)

# example usage
person = 'Kazi Nazrul Islam'
category = get_random_category()
a = get_quote(person, category)

print(a)