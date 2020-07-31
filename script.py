import bs4
import pandas as pd
from urllib import request

df = pd.read_csv("NEW_new_zealand_databasesdb.csv")
dfresult = pd.DataFrame(columns=['URLS'])

fileList = open("ListOfWords.txt" ,"r")

ListOfWords = []

for term in fileList.read().split(","):
	ListOfWords.append(term.lower())


for site in df['Website']:
	try:
		print(site)
		src = request.urlopen("http://" + site + "/").read()
		soup = bs4.BeautifulSoup(src, 'lxml')
		for url in soup.find_all('a'):
			if str(str(url.get('href')).replace("https://", "").replace("http://", "").replace("www.", "").replace(site, "").replace("/", "")) in ListOfWords:
				
				if site in url.get('href'):
					dfresult = dfresult.append({'URLS' : str(url.get('href')).replace("https://", "").replace("http://", "").replace("www.", "")}, ignore_index=True)
				else:
					dfresult = dfresult.append({'URLS' : str(site + "/" + url.get('href')).replace("//", "/")}, ignore_index=True)

	except:
		pass

dfresult = pd.DataFrame.drop_duplicates(dfresult).reset_index(drop=True)
dfresult.dropna(inplace=True, subset=['URLS'])

print(dfresult)
dfresult.to_excel("results.xlsx")