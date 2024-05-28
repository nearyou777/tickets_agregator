from bs4 import BeautifulSoup
html =  "<h2><strong>Atlanta (ATL)</strong><br>Antigua (ANU) - 37k*<br>Aruba (AUA) - 37k*<br>Bermuda (BDA) - 33k*<br>George Town (GGT) - 22k*<br>Grand Cayman (GCM) - 33k*<br>Kingston (KIN) - 33k*<br>Marsh Harbour (MHH) - 22k*<br>Montego Bay (MBJ) - 33k*<br>Nassau (NAS) - 22k*<br>North Eleuthera (ELH) - 22k*<br>Punta Cana (PUJ) - 33k*<br>San Juan (SJU) - 37k*<br>Santo Domingo (SDQ) - 33k*<br>St. Croix (STX) - 37k*<br>St. Maarten (SXM) - 37k*<br>St. Thomas (STT) - 37k*<br>Turks &amp; Caicos (PLS) - 33k*</h2>\r\n<h2>&nbsp;</h2>\r\n<h2><strong>Boston (BOS)</strong></h2>\r\n<h2>Montego Bay (MBJ) - 37k*<br>Nassau (NAS) - 33k*<br>San Juan (SJU) - 37k*</h2>\r\n<h2><br><strong>Detroit (DTW)</strong></h2>\r\n<h2>Montego Bay (MBJ) - 37k*<br>Punta Cana (PUJ) - 37k*<br>San Juan (SJU) - 37k*</h2>\r\n<p>&nbsp;</p>\r\n<hr>\r\n<h2><strong>Minneapolis (MSP)</strong></h2>\r\n<h2>Grand Cayman (GCM) - 37k*<br>Montego Bay (MBJ) - 44k*<br>Punta Cana (PUJ) - 44k*<br>Turks &amp; Caicos (PLS) - 37k*</h2>\r\n<h2>&nbsp;</h2>\r\n<h2><strong>New York (JFK)</strong><br>Aruba (AUA) - 37k*</h2>\r\n<h2>Bermuda (BDA) - 22k*<br>Montego Bay (MBJ) - 37k*<br>Nassau (NAS) - 33k*<br>Punta Cana (PUJ) - 37k*<br>San Juan (SJU) - 37k*<br>Santiago (STI) - 33k*<br>Santo Domingo (SDQ) - 37k*<br>St. Maarten (SXM) - 37k*<br>St. Thomas (STT) - 37k*<br>Turks &amp; Caicos (PLS) - 33k*<br><br><strong>New York (LGA)</strong></h2>\r\n<h2>Nassau (NAS) - 33k*</h2>"

soup = BeautifulSoup(html, 'html.parser')
d = []
for i in soup.find_all('h2'):
    if i.find('strong'):
        strong = i.find("strong").text
        # print(strong)
        normal = i.text.replace(f"{strong}", "").replace("<br>", "\n")
        msg = f'<b>{strong}</b>\n{normal}'
        d.append(msg)

print('\n'.join(d))