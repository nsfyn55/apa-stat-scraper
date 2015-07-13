import requests
import bs4
import utils

#get credentials
username, password = utils.get_credentials()

# get a response body from initial request
session = requests.Session()
resp = session.get("https://members.poolplayers.com")

# ------ Process Main Page Response ---------
soup = bs4.BeautifulSoup(resp.text, 'html.parser')
payload = utils.get_hidden_fields(soup)

# Decorate with Login Specific Fields
payload["DES_Group"] = ''
payload["DES_JSE"] = 1
payload["ctl00$cplhPublicContent$Login1$txtUserID"] = username
payload["ctl00$cplhPublicContent$Login1$txtPassword"] = password
payload["ctl00$cplhPublicContent$Login1$btnLogin"] = ""

resp = session.post('https://members.poolplayers.com/Default.aspx', data=payload)
payload = {}

# ------ Process Login Response ---------
soup = bs4.BeautifulSoup(resp.text, 'html.parser')
payload = utils.get_hidden_fields(soup)

# Get League Selection
league_select_box = soup.find('select', {"name":"ddlSelectedLeague"})
selected_league = league_select_box.find('option', selected=True).attrs['value']

payload['ddlSelectedLeague'] = selected_league

# Get Constant Contact stuff
payload['llr'] = soup.find('input', {'name':'llr'}).attrs['value']
payload['m'] = soup.find('input', {'name':'m'}).attrs['value']
payload['p'] = soup.find('input', {'name':'p'}).attrs['value']
payload['ea'] = soup.find('input', {'name':'ea'}).attrs['value']

# Navigate to Stats
payload['__EVENTTARGET'] = "lbtnStatistics"

# Process Statistics Page
resp = session.post('https://members.poolplayers.com/Main/Main.aspx', data=payload)

# ------ Process Main Stats Response ---------
soup = bs4.BeautifulSoup(resp.text, 'html.parser')

payload = utils.get_hidden_fields(soup)

# Get Selected League
league_select_box = soup.find('select', {"name":"ctl00$ddlSelectedLeague"})
selected_league = league_select_box.find('option', selected=True).attrs['value']

# Get Selected Division
div_selected = soup.find('select', {'name' :
    'ctl00$cplhMainContent$ctrlPlayerStatsNewControl$ddlDivisionSelector'})

selected_division = div_selected.find('option', selected=True).attrs['value']

payload['__EVENTTARGET'] = "ctl00$cplhMainContent$ctrlPlayerStatsNewControl$lbtnDivisionRoster"
payload['ctl00$cplhMainContent$ctrlPlayerStatsNewControl$ddlDivisionSelector'] = selected_division
payload['ctl00$ddlSelectedLeague'] = selected_league

resp = session.post('https://members.poolplayers.com/Stats/PlayerStatsNew.aspx',
        data=payload)

# ------ Process Division Roster Response ---------
print resp.text
