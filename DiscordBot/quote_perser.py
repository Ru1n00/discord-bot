import requests
from bs4 import BeautifulSoup
import random

def get_quote_by_author_and_category(author, category):
    """
    This function takes in the name of a author and a category of quotes, and returns a random quote from BrainyQuote that matches the criteria.
    """
    # Create the URL for the search
    url = f"https://www.brainyquote.com/search_results?q={author}+{category}"

    # Send a GET request to the URL
    response = requests.get(url)

    # Parse the HTML content of the page using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all the quotes on the page
    quotes = soup.find_all('a', {'title': 'view quote'})
    authors = soup.find_all('a', {'title': 'view author'})

    # If there are no quotes, return an error message
    if not quotes:
        return {'quote': f"Sorry, I couldn't find any {category} quotes by {author}.", 'author': 'Najrubindro'}

    # Choose a random quote from the list of quotes
    # random_quote = random.choice(quotes).text.strip()
    random_index = random.randint(0, len(quotes)-1)
    random_quote = {'quote': quotes[random_index].text.strip(), 'author': authors[random_index].text.strip()}

    # Return the quote
    return random_quote


def get_quote_by_author(author):
    """
    This function takes in the name of a author of quotes, and returns a random quote from BrainyQuote that matches the criteria.
    """
    # Create the URL for the search
    url = f"https://www.brainyquote.com/search_results?q={author}"

    # Send a GET request to the URL
    response = requests.get(url)

    # Parse the HTML content of the page using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all the quotes on the page
    quotes = soup.find_all('a', {'title': 'view quote'})
    authors = soup.find_all('a', {'title': 'view author'})


    # If there are no quotes, return an error message
    if not quotes:
        return {'quote': f"Sorry, I couldn't find any quotes by {author}.", 'author': 'Najrubindro'}

    random_index = random.randint(0, len(quotes)-1)
    # Choose a random quote from the list of quotes
    # random_quote = random.choice(quotes).text.strip()
    random_quote = {'quote': quotes[random_index].text.strip(), 'author': authors[random_index].text.strip()}

    # Return the quote
    return random_quote

print(get_quote_by_author("Van gogh",))



def get_random_quotes_from_goodreads():
    """
    This function takes in the name of a person and a category of quotes, and returns a random quote from BrainyQuote that matches the criteria.
    """
    # Create the URL for the search
    url = f"https://www.goodreads.com/quotes/tag/random?page=5"

    # Send a GET request to the URL
    response = requests.get(url)

    # Parse the HTML content of the page using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')
    print(soup)

    # Find all the quotes on the page
    quotes = soup.find_all('div', {'class': 'quoteText'})
    list_quotes = [i.text.strip() for i in quotes]

    # If there are no quotes, return an error message
    if not quotes:
        return f"Sorry, I couldn't find any  quotes by ."

    # Choose a random quote from the list of quotes
    random_quote = random.choice(quotes).text

    # Return the quote
    return list_quotes

# quotes = get_random_quotes_from_goodreads()
# quotes = [i.replace('\n', "") for i in quotes]
# quotes = [i.split('”')[0] for i in quotes]
# quotes = [i.replace("“", "") for i in quotes]
# print(quotes, len(quotes))


def get_ai_generated_quote_image():
    url = 'https://boredhumans.com/quotes.php'
    response = requests.get(url)

     # Parse the HTML content of the page using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all the quotes on the page
    quote_image = soup.find('img', {'alt': 'quotes'})
    # print(quote_image)
    quote_image_url = quote_image['src']
    # print(quote_image_url)
    return quote_image_url
# get_ai_generated_quote_image()

