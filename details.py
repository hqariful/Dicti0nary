import requests

def wordMeaning(word):
	# trying to read the URL https://api.dictionaryapi.dev/api/v2/entries/en/<word>
	try:
		x = requests.get('https://api.dictionaryapi.dev/api/v2/entries/en/'+'brothe')
		data = x.json()
		return data 
	except:
		return None