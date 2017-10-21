from flask import request, Flask, render_template, redirect
import wikipedia

app = Flask(__name__)

class Commands(object):
	def fb(arg=None):
		"""'fb [insert query]' searching on facebook. defaults on fb homepage"""
		if arg:
			return 'http://www.facebook.com/s.php?q={0}&init=q'.format(arg)
		else:
			return 'http://www.facebook.com'
	
	def g(arg=None):
		"""'g [insert query]' searching google"""
		if arg:
			return 'http://www.google.com/search?q={0}'.format(arg)
		else:
			return 'http://www.google.com'

	def gm(arg=None):
		"""'gm [insert number from 0-n where n = number of gmail accounts - 1] opens up gmail. If no argument specificed, opens up the first account. Can open up alternative accounts with arguments"""
		if arg:
			return 'https://mail.google.com/mail/u/{0}/#inbox'.format(arg)
		else:
			return 'https://mail.google.com/mail/u/0/#inbox'

	def w(arg=None):
		"""'w [insert query]' searches wikipedia, defaults on english wikipedia page"""
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

	def cpp(arg=None):
		"""'cpp [insert query]' searches for syntactical cpp terms on cppreference.com"""
		if arg:
			return 'http://en.cppreference.com/mwiki/index.php?title=Special%3ASearch&search={0}'.format(arg)
		else:
			return 'http://en.cppreference.com/w/'

	def p(arg=None):
		"""'p [insert class number]' make a piazza search, kinda personalized just for jack lol"""
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
		"""'yt [insert query]' make a youtube search. If not query is passed in, defaults to the youtube homepage"""
		if arg:
			return 'http://www.youtube.com/results?search_query={0}&search_type=&aq=-1&oq='.format(arg)
		else:
			return 'http://www.youtube.com'

	def help(arg=None):
		"""'help' returns a list of usable commands """
		help_list = []
		for values in Commands.__dict__.values():
			if callable(values):
				help_list.append(values.__doc__)
		return help_list

@app.route('/')
def index():
	return render_template('home.html')

@app.route('/q/')
def route():
	#process the query
	try:
		query = str(request.args.get('query', ''))
		tokenized_query = query.split(' ', 1)
		search_command = tokenized_query[0].lower()
		option_args = None
		if len(tokenized_query) == 2:
			option_args = tokenized_query[1]
	except Exception as e:
		print(e)
		search_command = query
		option_args = None

	try:
		command = getattr(Commands, search_command)
		if search_command == 'help':
			return render_template('help.html', command_list = command(None))
		url = command(option_args)
		return redirect(url)
	except Exception as e:
		# fallback option is to google search
		print(e)
		return redirect(Commands.g(query))

if __name__ == '__main__':
	app.run() 
