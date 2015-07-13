import bs4
import utils

text = ""
with open('/Users/arthurcarey/tmp/apa-temp/main-player-stats') as f:
    for line in f:
        text = text + line

soup = bs4.BeautifulSoup(text, 'html.parser')

payload = utils.get_hidden_fields(soup)

# Get Selected League
league_select_box = soup.find('select', {"name":"ctl00$ddlSelectedLeague"})
selected_league = league_select_box.find('option', selected=True).attrs['value']

# Get Selected Division
div_selected = soup.find('select', {'name' :
    'ctl00$cplhMainContent$ctrlPlayerStatsNewControl$ddlDivisionSelector'})
selected_division = div_selected.find('option', selected=True).attrs['value']

all_divisions = [o.attrs['value'] 
        for o in div_selected.find_all('option')
        if o.attrs['value'] != '0']

payload['__EVENTTARGET'] = "ctl00$cplhMainContent$ctrlPlayerStatsNewControl$lbtnDivisionRoster"
payload['ctl00$cplhMainContent$ctrlPlayerStatsNewControl$ddlDivisionSelector'] = selected_division
payload['ctl00$ddlSelectedLeague'] = selected_league

print selected_league, selected_division
print
print all_divisions
