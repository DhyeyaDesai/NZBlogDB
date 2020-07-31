import requests
import pandas as pd

df = pd.read_csv("new_zealand_databases.csv")
for site in df['Website']:
	# print(site)
	try:
		r = requests.get(site, allow_redirects=False)
		if r.status_code == 404:
			print(site + " gave 404")
			df['Website'] = df['Website'].replace([site], "")
		else:
			if r.headers['Location'] != None:
				redirect = str(r.headers['Location']).replace("https://","").replace("http://","").replace("www.", "").replace("/","")
				siteName = site.replace("https://","").replace("http://","").replace("www.", "").replace("/","")
				if str(redirect) != str(siteName) and ".co" in str(r.headers['Location']):
					print(siteName)
					print(redirect)
					df['Website'] = df['Website'].replace([site], redirect)
	except Exception as e:
		pass

df.dropna(inplace=True, subset=['Website'])

for website in df['Website']:
	df['Website'] = df['Website'].replace(website, str(website).replace("https://", "").replace("http://", "").replace("www.", ""))


df = df.drop_duplicates(subset='Website').reset_index(drop=True)
print(df)
df.to_csv("NEW_new_zealand_databasesdb.csv")