import urllib.request as request
from urllib.error import URLError, HTTPError
import json

def wordMeaning(word):
	# trying to read the URL
	try:
		x = request.urlopen('https://api.dictionaryapi.dev/api/v2/entries/en_US/'+word)
		source = x.read()
		data = json.loads(source)
		return data
		#show(data)   
	except HTTPError as e:
		return None
	except URLError as e:
		return None