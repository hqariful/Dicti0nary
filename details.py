import requests

def wordMeaning(word):
	# trying to read the URL https://api.dictionaryapi.dev/api/v2/entries/en/<word>
	try:
		x = requests.get('https://api.dictionaryapi.dev/api/v2/entries/en/'+word)
		data = x.json()
		if x.status_code == 404:
			return None
		else:
			return data 
	except :
		return None
	
