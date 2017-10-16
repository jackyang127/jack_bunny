from flask import Flask, url_for, redirect
import wikipedia

app = Flask(__name__)

class Commands(object):
	def fb(arg=None):
		"""searching on facebook"""
		if arg:
			return 'http://www.facebook.com/s.php?q={0}&init=q'.format(arg)
		else:
			return 'http://www.facebook.com'
	
	def g(arg=None):
		"""searching google"""
		if arg:
			return 'http://www.google.com/search?q={0}'.format(arg)
		else:
			return 'http://www.google.com'

	def w(arg=None):
		"""searches wikipedia, defaults on english wikipedia page"""
		try:
			if arg:
				# access the wikipedia api, first look for suggestions, then get
				# the page
				suggestion = wikipedia.search(arg, results=1, suggestion=True)
				if len(suggestion[0]) > 0:
					page = wikipedia.page(suggestion[0][0])
				else:
					page = wikipedia.page(arg)

				return page.url
			else:
				return 'https://en.wikipedia.org/wiki/Main_Page'
		except:
			return 'https://en.wikipedia.org/wiki/Main_Page'	

	def p(arg=None):
		"""make a piazza search, kinda personalized just for jack lol"""
		# should update to use piazza api for more generalized case
		mapping = {
			'189': 'j2ji31rkkl2og',
			'168': 'j628emf1ted4r2',
			'101': 'hyq0br1u3kx7dg'
		}
		if arg in mapping.keys():
			return 'https://piazza.com/class/{0}'.format(mapping[arg])
		else:
			return 'https://piazza.com'

	def yt(arg=None):
		"""make a youtube search"""
		if arg:
			return 'http://www.youtube.com/results?search_query={0}&search_type=&aq=-1&oq='.format(arg)
		else:
			return 'http://www.youtube.com'


@app.route('/')
def index():
	return 'Defualt index here'

@app.route('/q/<string:query>')
def route(query):
	#process the query
	try:
		tokenized_query = query.split(' ', 1)
		search_command = tokenized_query[0]
		option_args = None
		if len(tokenized_query) == 2:
			option_args = tokenized_query[1]
	except:
		search_command = query
		option_args = None

	try:
		command = getattr(Commands, search_command)
		url = command(option_args)
		return redirect(url)
	except:
		# fallback option is to google search
		return redirect(Commands.g(query))

if __name__ == '__main__':
	app.run() 
