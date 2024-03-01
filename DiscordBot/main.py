import discord
import requests
import dotenv
import random
from quote_perser import get_ai_generated_quote_image


def get_inspiration():
    api = 'https://zenquotes.io/api/random'
    response = requests.get(api)
    json_data = response.json()
    if json_data[0]['a'] == 'zenquotes.io':
        return 'Too lazy to write a quote. Let me rest for 30 seconds. - najrubindro'
    return json_data[0]['q'] + ' -' + json_data[0]['a']


def parse_author_and_category(content):
    content = content.replace('$quote', '')
    start_index_of_author = content.find('$author:')
    if start_index_of_author == -1:
        # return f'To get a quote by a specific author, use the command "$quote $author:author_name"', 404
        return None, None, 404
    
    end_index_of_author = content.find('$cat:')
    if end_index_of_author == -1:
        # return f'Getting quote by "{content[start_index_of_author:]}". To get a quote by a specific author and category, use the command "$quote $author:author_name $cat:category_name"', 200
        return content[start_index_of_author+len('$author:'):].strip(), None, 200
    
    start_index_of_category = content.find('$cat:') + len('$cat:')
    end_index_of_category = len(content)
    # return f'Getting quote by "{content[start_index_of_author:end_index_of_author]}" on "{content[start_index_of_category:end_index_of_category]}"', 210
    return content[start_index_of_author+len('$author:'):end_index_of_author].strip(), content[start_index_of_category:end_index_of_category].strip(), 210


def get_quote_from_db(author, token, cat=''):
    url = f'http://127.0.0.1:8000/api/author/{author}'
    headers = {'Authorization': f'Bearer {token}'}
    if cat:
        url += f'/category/{cat}'
    response = requests.get(url, headers=headers)
    if response.status_code == 401:
        token = requests.post('http://127.0.0.1:8000/api/token/', json={"username":"admin", "password":"admin"}).json().get('access')
        print(token, 'auth response')
        headers = {'Authorization': f'Bearer {token}'}
        response = requests.get(url, headers=headers)
    json_data = response.json()
    print(json_data)
    print(type(json_data), type([]), 'types')
    if type(json_data) != type([]):
        return json_data, token
    index = random.randint(0, len(json_data)-1)
    print(index, 'random index ----')
    quote = json_data[index]
    # print(json_data, 'json data')
    # print(quote, 'quote')
    return quote, token



class MyClient(discord.Client):
    async def on_ready(self):
        self.TOKEN = requests.post('http://127.0.0.1:8000/api/token/', json={"username":"admin", "password":"admin"}).json().get('access')
        print('Logged on as', self.user)

    async def on_message(self, message):
        # don't respond to ourselves
        if message.author == self.user:
            return

        if message.content.strip() == '$hello':
            await message.channel.send(f'Hello! {message.author.mention}')
        
        if message.content.strip() == '$inspire':
            quote = get_inspiration()
            await message.channel.send(quote)

        if message.content.startswith('$quote'):
            author, category, status_code = parse_author_and_category(message.content)

            if status_code == 404:
                await message.channel.send(f'No author provided. To get a quote by a specific author, use the command "$quote $author:author_name"')
            elif status_code == 200:
                await message.channel.send(f'Getting quote by "{author}".')
                quote, token = get_quote_from_db(author, token=self.TOKEN)
                self.TOKEN = token
                await message.channel.send(f'"{quote.get("quote")}" - {quote.get("author")}')
                await message.channel.send(f'To get a quote by a specific author and category, use the command "$quote $author:author_name $cat:category_name"')

            elif status_code == 210:
                await message.channel.send(f'Getting quote by "{author}" on "{category}"')
                quote, token = get_quote_from_db(author, token=self.TOKEN, cat=category)
                self.TOKEN = token
                await message.channel.send(f'"{quote.get("quote")}" - {quote.get("author")}')
        
        if message.content.strip() == '$help':
            await message.channel.send("""
                    command     -----   description
                $hello    -----   Say hello to the bot,
                $inspire    -----    Get a random quote,
                $quote $author:author_name  -----   Get a quote by a specific author,
                $quote $author:author_name $cat:category_name   -----   Get a quote by a specific author and category,
                $help   -----   Get help
            """)
        
        if message.content.strip() == '$ai':
            # with open('./Moneky.jpeg', 'rb') as f:
            #     picture = discord.File(f)
            #     await message.channel.send(file=picture)
            await message.channel.send(get_ai_generated_quote_image())


intents = discord.Intents.default()
intents.message_content = True
client = MyClient(intents=intents)
auth_token = dotenv.get_key('.env', 'TOKEN')
client.run(auth_token)