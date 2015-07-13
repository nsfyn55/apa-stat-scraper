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


def get_credentials():
    with open('creds') as creds:
        for i,line in enumerate(creds):
            if i == 0:
                username = line.rstrip()
            if i == 1:
                password = line.rstrip()
    return username, password
