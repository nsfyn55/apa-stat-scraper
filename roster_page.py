import bs4
import utils

text = ""
with open('/Users/arthurcarey/tmp/apa-temp/roster-page') as f:
    for line in f:
        text = text + line

soup = bs4.BeautifulSoup(text, 'html.parser')

payload = utils.get_hidden_fields(soup)

print payload
