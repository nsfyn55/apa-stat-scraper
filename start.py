import requests
import bs4


def get_hidden_fields(soup):
    base_payload = {}

    etarg = soup.find('input', {'name': '__EVENTTARGET'})
    earg = soup.find('input', {'name': '__EVENTARGUMENT'})
    lastfocus= soup.find('input', {'name': '__LASTFOCUS'})

    base_payload['__EVENTTARGET'] = etarg.attrs['value'] if hasattr(etarg, 'attrs') else ''
    base_payload['__EVENTARGUMENT'] = earg.attrs['value'] if hasattr(earg, 'attrs') else ''
    base_payload['__VIEWSTATE'] = soup.find('input', {'name': '__VIEWSTATE'}).attrs['value']
    base_payload['__EVENTVALIDATION'] = soup.find('input', {'name': '__EVENTVALIDATION'}).attrs['value']
    base_payload['__LASTFOCUS'] = lastfocus.attrs['value'] if hasattr(lastfocus, 'attrs') else ''

    return base_payload

with open('creds') as creds:
    for i,line in enumerate(creds):
        if i == 0:
            username = line.rstrip()
        if i == 1:
            password = line.rstrip()

# get a response body from initial request
session = requests.Session()
resp = session.get("https://members.poolplayers.com")

# Process Login Page
soup = bs4.BeautifulSoup(resp.text, 'html.parser')
payload = get_hidden_fields(soup)

payload["DES_Group"] = ''
payload["DES_JSE"] = 1
payload["ctl00$cplhPublicContent$Login1$txtUserID"] = username
payload["ctl00$cplhPublicContent$Login1$txtPassword"] = password
payload["ctl00$cplhPublicContent$Login1$btnLogin"] = ""

resp = session.post('https://members.poolplayers.com/Default.aspx', data=payload)
payload = {}

#Process Login
soup = bs4.BeautifulSoup(resp.text, 'html.parser')
payload = get_hidden_fields(soup)

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

print resp.text
