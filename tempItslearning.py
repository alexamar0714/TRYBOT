#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# itslearning CLI
# https://github.com/grafi/itslearningCLI
#
# http://peak.telecommunity.com/DevCenter/EasyInstall
# easy_install beautifulsoup4
# easy_install mechanize
#


config = {
	'username': '',
	'password': '',
	'use_cookie': True,
	'format_course_name': False,
	'organization': 'ntnu.no',
}





###############################################################################################
NAME = 'itslearning CLI'
VERSION = '0.1.1'
###############################################################################################

import mechanize, cookielib, urllib, re, getpass, sys, os, time, string
from bs4 import BeautifulSoup


#
# API class
#
class itslearningAPI:

	cfg = {
		'username': '',
		'password': '',
		'debug': False,
		'show_status': True,
		'use_cookie': False,
		'format_course_name': False,
		'show_filenames': False,
		#'filenames_from': 'original', # original, header, itslearning 
		'organization': 'ntnu.no',
		'cookie_file': 'cookie.txt',
		'loop_delay': 0.2,
		'user_agent': 'Mozilla/5.0 (Windows NT 5.2; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.47 Safari/536.11',
		'feidestring': 'ctl00$ContentPlaceHolder1$federatedLoginButtons$ctl00$ctl00',
	}

	url = {
		'main': 'https://ntnu.itslearning.com',
		'course': 'https://ntnu.itslearning.com/main.aspx?CourseID=',
		'folder': 'https://ntnu.itslearning.com/Folder/processfolder.aspx?FolderID=',
		'file': 'https://ntnu.itslearning.com/File/fs_folderfile.aspx?FolderFileID=',
		'tool': 'https://ntnu.itslearning.com/LearningToolElement/ViewLearningToolElement.aspx?LearningToolElementId=',
		'note': 'https://ntnu.itslearning.com/note/View_Note.aspx?NoteID=',
		'essay': 'https://ntnu.itslearning.com/essay/read_essay.aspx?EssayID=',
		'essay_download': 'https://ntnu.itslearning.com/File/download.aspx?FileID=',
		'download': 'https://ntnu.itslearning.com/file/download.aspx?FileVersionID=-1&FileID=',
		'dashboard': 'https://ntnu.itslearning.com/DashboardMenu.aspx?LocationId=105&LocationType=Hierarchy',
		'logout': 'https://ntnu.itslearning.com/elogin/logout.aspx'
	}

	courses = []
	courses_data = { 'max_num': 0, 'max_len': 0, 'max_new': 0 }
	current_course_num = 0
	resources = {}
	sync_data = { 'overwrite': False }
	loggedin = False


	def __init__(self, options={}):
		self.cfg = dict(self.cfg.items() + options.items())
		
		# browser init
		br = mechanize.Browser()

		# use cookie
		if self.cfg['use_cookie']:
			cj = cookielib.LWPCookieJar()
			br.set_cookiejar(cj)
			try:
				cj.load(self.cfg['cookie_file'], ignore_discard=True, ignore_expires=True)
			except IOError:
				pass
			self.cj = cj

		# browser config
		br.set_handle_equiv(True)
		br.set_handle_redirect(True)
		br.set_handle_referer(True)
		br.set_handle_robots(False)
		br.set_debug_http(False)
		br.set_debug_responses(False)
		br.set_debug_redirects(False)
		br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
		br.addheaders = [('User-agent', self.cfg['user_agent'])]
		self.br = br 

		if self.checkLogin(): ####### useless
			print ' * Logget inn'
		else:
			print ' * Ikke innlogget'


	# check if logged in
	def checkLogin(self):

		response = self.br.open(self.url['dashboard']).read()

		if self.checkResponse(response, 'Dashboard'):
			self.loggedin = True
			self.getCourses(response)
		else:		
			self.loggedin = False
			if not self.login():
				sys.exit()#'Login failed')
			self.getCourses()		

		return self.loggedin


	# login using feide
	def login(self):
		br = self.br
		self.loggedin = False

		# open feide-login
		print ' * Åpner feide-login...'
		br.open(self.url['main'])
		for form in br.forms():
		    if form.attrs['id'] == 'aspnetForm':
		        br.form = form
		        break

		params = {
			'__LASTFOCUS': '',
			'__EVENTTARGET': self.cfg['feidestring'], 
			'__EVENTARGUMENT': '',
			'__VIEWSTATE': br.form['__VIEWSTATE'],
			'__EVENTVALIDATION': br.form['__EVENTVALIDATION']
		}
		post_data = urllib.urlencode(params)
		response = br.open(self.url['main'], post_data).read()

		if not (self.checkResponse(response, 'orgframe') 
			or self.checkResponse(response, 'feidename')
			or self.checkResponse(response, 'press the button below')):
				print response
				print ' *!* Feil ved åpning av feide-login'		
				return False

		# select institution
		if self.checkResponse(response, 'orgframe'):
			print ' * Velger skole...'
			br.select_form(name='f')
			br.form.set_all_readonly(False)
			br.form['org'] = [self.cfg['organization']]
			response = br.submit().read()

			if not self.checkResponse(response, 'feidename'):
				print ' *!* Feil ved valg av instutisjon'
				return False

		# login credentials
		if self.checkResponse(response, 'feidename'):
			print ' * Logger inn'
			br.select_form(name='f')
			br.form.set_all_readonly(False)

			username = self.cfg['username']
			password = self.cfg['password']

			if username == '':
				username = raw_input(' -> Brukernavn: ').strip()
			if password == '':
				password = getpass.getpass(' -> Passord: ')

			br.form['feidename'] = username
			br.form['password'] = password
			response = br.submit().read()

			if self.checkResponse(response, 'errorframe'):
				print ' *!* Feil brukernavn/passord'
				return False

		# javascript bypass
		if self.checkResponse(response, 'press the button below'):
			print ' * Redirecter...'
			br.select_form(nr=0)
			response = br.submit().read()

			if not self.checkResponse(response, "name='form'"):
				print ' *!* Feil med cookie/blokkert/endring'
				return False

		# redirect to itslearning
		if self.checkResponse(response, "name='form'"):
			print ' * Åpner itslearning'
			br.select_form(name='form')
			response = br.submit().read()

			if not self.checkResponse(response, 'Dashboard'):
				print ' *!* Feil med innlogging/redirect'
				return False
	
		# save if using cookie
		if self.cfg['use_cookie']:
			self.cj.save(self.cfg['cookie_file'], ignore_discard=True, ignore_expires=True)
		

		self.loggedin = True 
		return self.loggedin


	# logout
	# todo: confirm logut
	def logout(self):
		br = self.br
		response = br.open(self.url['logout']).read()
		br.select_form(nr=0)
		response = br.submit().read()
		os.remove(self.cfg['cookie_file'])

		if self.checkResponse(response, 'LogoutResult=success'):
			return True
		return False


	def getCourses(self, data=None):
		if not data:
			data = self.br.open(self.url['dashboard']).read()

		self.toFile(data.decode('utf-8'), 'dashboard.html')

		bs = BeautifulSoup(data, 'html.parser')
		#data = soup.find('div', {'data-courses-dropdown': ''})
		ddc = bs.find('div', attrs={'data-courses-dropdown' : True})
		
		courses = []

		max_len = 0
		max_new = 0

		#fav_courses = ddc.find_all('li', attrs={'role': 'presentation'})
		fav_courses = ddc.find_all('a', attrs={'role': 'menuitem'})
		for course in fav_courses:
			#link = course.find('a', href=re.compile('^/main.aspx\?CourseID=[0-9]+$'))
			name = course.get('title')
			max_len = max(max_len, len(name))

			cid = re.findall(r'\d+', course.get('href'))[0]
			date = course.find('span', {'class': 'itsl-widget-extrainfo'}).text

			updates = 0
			is_updated = course.find('span', {'class': 'itsl-counter-badge'})
			if is_updated: updates = int(is_updated.text)

			max_new = max(max_new, updates)
			
			#print name, cid, ' - ', updates, ' - ', date

			course_data = { 
				'name': name, 'id': cid, 'date': date, 'updates': updates, 'updates_id': [],
				'max_item_len': 0, 'tree_depth': 0, 'num_items': 0, 'num_folders': 0
			}

			courses.append(course_data)

		self.courses = courses
		self.courses_data['max_len'] = max_len
		self.courses_data['max_num'] = len(courses)-1
		self.courses_data['max_new'] = max_new

		return courses



	# list courses
	# format: [{ name, id, date, updates, updates_id, max_item_len, tree_depth, num_items, num_folders }, ...]
	def getCoursesOld(self, data=None):
		if not data:
			data = self.br.open(self.url['dashboard']).read()

		#res_soup = BeautifulSoup(data)
		res_soup = BeautifulSoup(data, 'html.parser')
		data = res_soup.findAll('li', {'class': 'h-dsp-ib h-width-100 h-box-sizing-bb'})

		courses = []
		max_len = 0
		max_new = 0

		for block in data:
			soup = BeautifulSoup(str(block), 'html.parser')
			link = soup.find('a', href=re.compile('^/main.aspx\?CourseID=[0-9]+$'))
			if not link:
				continue

			name = link.text
			max_len = max(max_len, len(name))
			cid = re.findall(r'\d+', link.get('href'))[0]

			meta = soup.find_all('span')
			date = ''
			updates = 0
			updates_id = []

			if len(meta) > 1:
				date = meta[1].text.strip() #replace('siden', '').strip()

			if len(meta) > 2:
				updates = int(meta[-1].text.strip())
				new_data = res_soup.findAll('a', href=re.compile('com/main.aspx\?CourseID='+cid+'.*ElementID=[0-9]+'))
				for new in new_data:
					new_id = re.findall(r'\d+', new.get('href'))[1]
					updates_id.append(new_id) 

			max_new = max(max_new, updates)

			course = { 
				'name': name, 'id': cid, 'date': date, 'updates': updates, 'updates_id': updates_id,
				'max_item_len': 0, 'tree_depth': 0, 'num_items': 0, 'num_folders': 0
			}
			courses.append(course)

		self.courses = courses
		self.courses_data['max_len'] = max_len
		self.courses_data['max_num'] = len(courses)-1
		self.courses_data['max_new'] = max_new

		return courses


	# list courses
	# format: [{ name, id }, ...]
	# todo: get changes
	#def getCoursesOld(self, data=''):
	#	if data == '':
	#		data = self.br.open(self.url['dashboard']).read()
	#
	#	soup = BeautifulSoup(data)
	#
	#	courseslinks = soup.findAll('a', href=re.compile('^/main.aspx\?CourseID=[0-9]+$'))
	#	courses = []
	#	for (counter, link) in enumerate(courseslinks):
	#		href = link.get('href')
	#		cid = re.findall(r'\d+', href)[0]
	#		name = link.text
	#		courses.append({ 'name':name, 'id': cid })
	#
	#	self.courses = courses
	#	self.courses_max = len(courses)-1
	#
	#	return courses


	def getCourse(self, course_num):
		if 0 <= course_num < len(self.courses):
			return self.courses[course_num]
		return False

	# get course num from id
	def getCourseNum(self, course_id):
		for counter, val in enumerate(self.courses):
			if val['id'] == course_id:
				return counter
		return False

	# get course id from num
	def getCourseID(self, course_num):
		if len(self.courses) > course_num:
			#return int(self.courses[course_num]['id'])
			return self.courses[course_num]['id']
		return False

	# get course id from array
	def getCourseName(self, course_num, nice=True):
		#print 0, '<', course_num, '<', len(self.courses)
		#print self.courses[course_num]
		if 0 <= course_num < len(self.courses):
			name = self.courses[course_num]['name']
			if nice: name = self.formatCourseName(name)
			return name
		return False

	# try to remove course code from name
	def formatCourseName(self, name):
		name = name.split()
		digits = re.compile('\d')
		for n, val in enumerate(name):
			if not digits.search(val):
				break
		return ' '.join(name[n:]).strip()


	# list course resources 
	# format: { course_id: { data: [name, resource_type], child_id: { data: [], ... } , ...}, ...}
	def getResources(self, course_id, update=False):

		#course_id = str(course_id)

		if course_id in self.resources and (not update):
			return self.resources[course_id]

		self.current_course_num = self.getCourseNum(course_id)

		response = self.br.open('%s%s' % (self.url['course'], course_id)).read()
		#self.toFile(response)

		root_folder_id = re.findall('FolderID=([0-9]+)', response)[0]

		items = self.openFolder(root_folder_id)

		self.resources[course_id] = items
		
		return items


	# recursive function
	# todo: version control
	def openFolder(self, folder_id, path='', parent='root'):

		response = self.br.open('%s%s' % (self.url['folder'], folder_id)).read()

		soup = BeautifulSoup(response, 'html.parser')
		data = soup.findAll('a', href=re.compile('^/(Folder|File|note|essay|LearningToolElement)/'))

		course_num = self.current_course_num
		course_data = self.courses[course_num]

		items = {}

		for item in data:
			item_link = item.get('href')
			item_name = item.text.strip()
			item_id = re.findall(r'\d+', item_link)[0]
			
			if item_id == parent:
				continue

			item_type = 'unknown'
			if 'Folder' in item_link: item_type = 'folder'
			if 'File' in item_link: item_type = 'file'
			if 'note' in item_link: item_type = 'note'
			if 'essay' in item_link: item_type = 'essay'
			if 'LearningToolElement' in item_link: item_type = 'tool'

			more_info = False

			if item_type == 'folder':
				course_data['num_folders'] = course_data['num_folders'] + 1
				new_path = path + '/' + item_name
				more_info = self.openFolder(item_id, new_path, folder_id)
			elif item_type == 'file':
				more_info = self.getFile(item_id)
			elif item_type == 'tool':
				more_info = self.getTool(item_id)
			elif item_type == 'note':
				more_info = self.getNote(item_id)
			elif item_type == 'essay':
				more_info = self.getEssay(item_id)
			
			act = u'Åpner' if item_type == 'folder' else 'Leser'
			stat = '%s \'%s\' (%s)' % (act, item_name, item_type)

			if not more_info:
				self.printStatus(stat + ' [' + color.yellow + 'uten innhold' + color.end + ']')
				continue
			
			self.printStatus(stat)

			items[item_id] = { 'data': [item_name, item_type], 'path': path }

			if len(more_info) > 0:
				items[item_id] = dict(items[item_id].items() + more_info.items())

			course_data['max_item_len'] = max(course_data['max_item_len'], len(u''+item_name))
			course_data['tree_depth'] = max(course_data['tree_depth'], path.count('/'))
			if item_type in ['file', 'note', 'essay', 'tool']:
				course_data['num_items'] = course_data['num_items'] + 1

			time.sleep(self.cfg['loop_delay'])

		self.courses[course_num] = course_data
		
		return items


	# retrieve essay/exercise download id, filename
	# False if no file exists
	# todo: return submission link
	def getEssay(self, essay_id): ################useless
		br = self.br
	
		response = br.open('%s%s' % (self.url['essay'], essay_id)).read()

		soup = BeautifulSoup(response, 'html.parser')

		data = soup.findAll('a', href=re.compile('/File/download.aspx\?FileID=[0-9]+'))#[0]
		if len(data) == 0:
			return False #{ 'download_id': 0, 'name': 'innlevering' }
		data = data[0]

		file_link = data.get('href')
		file_name = data.text
		download_id = re.findall(r'\d+', file_link)[0]

		file_info = { 'download_id': download_id.strip(), 'name': file_name.strip() }
		return file_info


	# retrieve download id, filename, size
	def getFile(self, file_id):
		br = self.br
	
		response = br.open('%s%s' % (self.url['file'], file_id)).read()
		#self.toFile(response)
		
		soup = BeautifulSoup(response, 'html.parser')

		data = soup.findAll('a', href=re.compile('^../file/download.aspx\?FileID=[0-9]+'))
		if len(data) == 0:
			return False
		data = data[0]



		file_link = data.get('href')
		file_size = re.findall(r'\((.*)\)', data.text)[0]
		file_name = re.findall(r'Last ned (.*)\(', data.text)[0]
		download_id = re.findall(r'\d+', file_link)[0]

		file_info = { 'download_id': download_id.strip(), 'name': file_name.strip(), 'size': file_size.strip() }
		return file_info


	# retrieve note
	# assuming its always tekst wrapped in a div[class=userinput] tag
	def getNote(self, note_id):
		br = self.br

		response = br.open('%s%s' % (self.url['note'], note_id)).read()

		soup = BeautifulSoup(response, 'html.parser')
		data = soup.findAll('div', { 'class': 'userinput' })

		note_info = { 'notes': data }

		return note_info


	# retrieve learning tool
	# assuming link wrapped in an iframe
	def getTool(self, tool_id):#####################################????????????????????????
		try:
			br = self.br

			response = br.open('%s%s' % (self.url['tool'], tool_id)).read()

			#self.toFile(response, 'tool1.html')

			soup = BeautifulSoup(response, 'html.parser')
			tool_url = soup.find('iframe')['src']

			response = br.open(tool_url).read()

			#self.toFile(response, 'tool2.html')
			
			soup = BeautifulSoup(response, 'html.parser')
			tool_link = soup.find('a')['href']

			tool_info = { 'link': tool_link }

			return tool_info
		except:
			self.printStatus(color.red + 'Error retrieving tool data' + color.end)
			return False
		

	# download course resources
	# todo: optional root folder
	# todo: version control
	# todo: return True/False
	def syncCourse(self, course_num):
		course_name = self.courses[int(course_num)]['name']
		course_id = self.getCourseID(course_num)
		data = self.getResources(course_id)

		if self.cfg['format_course_name']:
			course_name = self.formatCourseName(course_name)

		self.sync_data['root'] = course_name
		if not os.path.exists(course_name):
		    os.makedirs(course_name)

		self.syncFileFolder(data)

		self.printStatus('\'' + course_name + '\' lastet ned', False, True)


	# recursive function for downloading
	def syncFileFolder(self, data, dir=[]):
		if len(data) == 0:
			return 

		for key, value in data.iteritems():
			#if 'data' in value:
			if type(value) is dict and 'data' in value.keys():
				item_type = value['data'][1]

				path = self.sync_data['root'] + value['path'].replace('/', os.sep) + os.sep
				if not os.path.exists(path):
					os.makedirs(path)

				if item_type == 'folder':
					makefolder = path + value['data'][0]
					if not os.path.isdir(makefolder):
						self.printStatus('Oppretter mappe \'%s\' ...' % makefolder, True)
						os.makedirs(makefolder)
	 					self.printStatus(color.green + 'ok' + color.end)

				elif item_type == 'file':
					savefile = path + value['name']
					self.printStatus('Laster ned fil \'%s\' (%s) ...' % (savefile, value['size']), True)
					if os.path.isfile(savefile) and (not self.sync_data['overwrite']):
						self.printStatus(color.yellow + 'skipped' + color.end)
					else:
						header = self.br.retrieve(('%s%s' % (self.url['download'], value['download_id'])), savefile)[1]
						if 'filename' in str(header): self.printStatus(color.green + 'ok' + color.end)
						else: self.printStatus(color.red + 'error' + color.end)

				# todo: create submission link
				elif item_type == 'essay':
					savefile = path + value['name']
					self.printStatus('Laster ned oppgave \'%s\' ...' % savefile, True)
					if os.path.isfile(savefile) and (not self.sync_data['overwrite']):
						self.printStatus(color.yellow + 'skipped' + color.end)
					else:
						header = self.br.retrieve(('%s%s' % (self.url['essay_download'], value['download_id'])), savefile)[1]
						if 'filename' in str(header): self.printStatus(color.green + 'ok' + color.end)
						else: self.printStatus(color.red + 'error' + color.end)

				elif item_type == 'note':
					savefile = path + self.validFilename(value['data'][0] + '.html')
					self.printStatus('Lager notat \'%s\' ...' % savefile, True)
					f = open(savefile, 'w')
					for note in value['notes']:
						f.write(str(note)) #.encode('utf-8'))
					f.close()
 					self.printStatus(color.green + 'ok' + color.end)

				elif item_type == 'tool':
					savefile = path + self.validFilename(value['data'][0] + '.url')
					self.printStatus('Lager snarvei \'%s\' ...' % savefile, True)
					content = '[InternetShortcut]\r\nURL=' + value['link']
					f = open(savefile, 'w+')
					f.write(content.encode('utf-8'))
					f.close()
 					self.printStatus(color.green + 'ok' + color.end)

				time.sleep(self.cfg['loop_delay'])

			if type(value) is dict:
				self.syncFileFolder(value)

	def validFilename(self, s):
		valid_chars = unicode("-_.() %s%s%s" % (string.ascii_letters, string.digits, u'æøåÆØÅ'))
		filename = ''.join(c for c in s if c in valid_chars)
		return filename.strip()

	# check if string is in string
	def checkResponse(self, response, expected):
		if expected in response:
			return True
		return False


	def printStatus(self, string, nonl=False, xtranl=False): ######################useless
		if self.cfg['show_status'] or self.cfg['debug']:
			if nonl: print string,
			else: print string
			if xtranl: print ' '
			sys.stdout.flush()


	# debug
	def toFile(self, data, file='cli.html'):
		f = open(file, 'w')
		f.write(data.encode('utf-8'))
		f.close()



################################################################### USELESS


#
# CLI class
# todo rewrite
class itslearningCLI:

	current_course = {}
	#api = 0

	def __init__(self, config={}):
		self.printSplash()
		self.api = itslearningAPI(config)
		self.prompt = ''
		self.cfg = self.api.cfg

		print ' '

		#self.printHelp()
		if self.api.loggedin:
			self.cmdListCourses()

		while True:
			self.commandInput()


	# command parser
	# todo: rewrite
	def commandInput(self):
		sys.stdout.write('itslearning> ')
		cmd = raw_input(self.prompt).strip().split(' ')

		if 'exit' in cmd[0] or 'quit' in cmd[0] or 'q' == cmd[0][0]:
			sys.exit()
		elif 'logout' in cmd[0]:
			self.cmdLogout()
		elif 'list' in cmd[0]:
			if (len(cmd) > 1) and ('u' == cmd[1][0]):
				self.api.getCourses()
			self.cmdListCourses()
		elif 'ver' in cmd[0]:
			print NAME, VERSION

		elif cmd[0] == 'files':
			courses_max = self.api.courses_data['max_num']
			if (len(cmd) >= 2) and (0 <= int(cmd[1]) <= courses_max):
				update = False
				if (len(cmd) > 2) and ('u' == cmd[2][0]):
					update = True
				self.cmdListFiles(int(cmd[1]), update)
				num = int(cmd[1])
			else:
				self.cmdListCourses(False)
				allowed = list(xrange(courses_max+1))
				allowed = map(str, allowed)
				num = int(self.commandInputSpecial(('Velg fag [0-%s]: ' % courses_max), allowed))
				self.cmdListFiles(num)
			current_course = num

		elif cmd[0] == 'sync':
			courses_max = self.api.courses_data['max_num']
			if (len(cmd) > 1) and ('all' == cmd[1]):
				self.cmdSyncAllCourses()
				num = 0
			elif (len(cmd) >= 2) and (0 <= int(cmd[1]) <= courses_max):
				self.api.sync_data['overwrite'] = False
				if (len(cmd) >= 3) and ('f' == cmd[2][0]): 
					self.api.sync_data['overwrite'] = True
				self.cmdSyncCourse(int(cmd[1]))
				num = int(cmd[1])
			else:
				self.cmdListCourses(False)
				allowed = list(xrange(courses_max+1))
				allowed = map(str, allowed)
				num = int(self.commandInputSpecial(('Velg fag [0-%s]: ' % courses_max), allowed))
				self.cmdSyncCourse(num)
			current_course = num
	
		elif cmd[0] == 'help':
			self.printHelp()

		elif 'clear' in cmd[0] or 'clr' in cmd[0] or 'cls' in cmd[0]:
			os.system('cls' if os.name == 'nt' else 'clear')
		
		elif cmd[0] == 'set':
			if len(cmd) >= 2 and cmd[1] in self.api.cfg:
				val = str(' '.join(cmd[2:]).strip())
				bools = ['use_cookie', 'format_course_name', 'debug', 'show_status', 'show_filenames']
				ints = ['loop_delay']
				if len(cmd) > 2:
					if cmd[1] in bools: val = bool(cmd[2].lower() in ('yes', 'true', 't', '1', 'y'))
					elif cmd[1] in ints: val = int(cmd[2])
					self.api.cfg[cmd[1]] = val
					self.cfg = self.api.cfg
				print cmd[1], '=', self.api.cfg[cmd[1]]
			else:
				print 'set <variable> [arg]\n'
				for key, val in self.cfg.iteritems():
					print key, '=', val

		elif cmd[0] == 'print':
			val = ['resources', 'courses', 'courses_data', 'sync_data']
			if len(cmd) > 1 and cmd[1] in val:
				if cmd[1] == 'resources': print self.api.resources
				elif cmd[1] == 'courses': print self.api.courses
				elif cmd[1] == 'courses_data': print self.api.courses_data
				elif cmd[1] == 'sync_data': print self.api.sync_data 
			else: print 'print <' + '|'.join(val) + '>'

		else:
			print 'Ukjent kommando\n'
			self.printHelp()


	def commandInputSpecial(self, prompt, allowed):
		sys.stdout.write('itslearning> ')
		while True:
			cmd = raw_input(prompt)
			for c in allowed:
				if cmd == c:
					return cmd

	def cmdSyncAllCourses(self):
		mnc = self.api.courses_data['max_num']
		print 'Synkroniserer alle kurs...'
		for course_num in range(0, mnc+1):
			self.api.syncCourse(course_num)
			if course_num < mnc:
				print 'Venter 5 sekunder...\n'
				time.sleep(5)
			else: print 'Alle kurs synkronisert.'

	def cmdSyncCourse(self, course_num):
		self.api.syncCourse(course_num)

	def cmdFile(self, file_id):
		self.api.getFile(file_id)

	def cmdListCourses(self, info=True):
		print ' '

		max_new = self.api.courses_data['max_new']
		new_spacing = 11 if max_new > 9 else 10 if max_new > 1 else 9 if max_new > 0 else 0

		for (counter, course) in enumerate(self.api.courses):
			new = ' '
			spacing = (self.api.courses_data['max_len'] - len(course['name'])) * ' '
			if course['updates'] > 0:
				new = ' [%s ny%s] ' % (course['updates'], ('e' if course['updates'] > 1 else ''))
			new = new + ((new_spacing - len(new)) * ' ') 
			if info:
				line = '   %s.  %s %s%s%s' % (counter, course['name'], spacing, new, course['date'])
			else:
				line = '   %s.  %s' % (counter, course['name'])
			if self.cfg['debug']: line = line + ' (id: %s) (updates_id: %s)' % (course['id'], str(course['updates_id']))
			print line 
		print ' '

	def cmdListFiles(self, course_num, update=False):
		self.current_course = self.api.getCourse(course_num)
		course_name = self.api.getCourseName(course_num)
		data = self.api.getResources(self.current_course['id'], update)
		print ' '
		print '   ' + color.bold + course_name + color.end
		print '   ' + color.bold + ('‾' * len(course_name)) + color.end
		if self.cfg['debug']: print '   ', self.api.courses[course_num], '\n'
		#print '\n\n' + str(data) + '\n\n'
		self.printFileTree(data)
		print ' '

	def cmdLogout(self):
		if not self.api.logout():
			print 'Feil ved utlogging..?'
		sys.exit()

	# recursive 
	def printFileTree(self, d, indent=2):
		if len(d) == 0:
			print ('   ' * indent), '<ingen filer funnet>'
			return 

		for item_id, data in d.iteritems():

			if type(data) is dict and 'data' in data.keys():
				#print 'DATA', fdata['data']
				item_name = data['data'][0]
				item_type = data['data'][1]

				ind = ('   ' * indent)
				if item_id in self.current_course['updates_id']:
					ind = ('   ' * (indent-2)) + color.red + 'NY -> ' + color.end
				print ind,

				max_len = 9 + self.current_course['max_item_len'] + self.current_course['tree_depth'] * 3
				spacing = ((max_len - (3 * indent + len(item_name))) * '.')
				if item_type == 'file':
					filename = '\'' + data['name'] + '\''
					if not self.api.cfg['show_filenames']: filename = os.path.splitext(data['name'])[1][1:]
					line = '%s %s [%s: %s, %s]' % (item_name, spacing, item_type, data['size'], filename)
				elif item_type == 'essay':
					filename = '\'' + data['name'] + '\''
					if not self.api.cfg['show_filenames']: filename = os.path.splitext(data['name'])[1][1:]
					line = '%s %s [%s: %s]' % (item_name, spacing, item_type, filename)
				else:
					line = '%s %s [%s]' % (item_name, spacing, item_type)
					
				if self.cfg['debug']:
					line = line + ' (id: %s) (path: %s)' % (item_id, data['path'])
				
				print line
			#else:
			#	print fdata

			if type(data) is dict:
				self.printFileTree(data, indent+1)

	def printHelp(self):
		mnc = self.api.courses_data['max_num']
		hlp = [
			'list [update]',
			'files <0-%s> [update]' % mnc,
			'sync <0-%s|all> [force]' % mnc,
			'clear',
			'logout',
			'help',
			'exit' 
		]
		print ' '
		#for h in hlp: print '   ' + h
		print '   ' + ',  '.join(hlp)
		if self.cfg['debug']: print '\n   debug: set <var> [arg],  print <var>'
		print ' '


	def printSplash(self):
		s = NAME #+ str(VERSION)
 		print '\n ' + s + '\n ' + '‾' * len(s)


class color:
	purple = '\033[95m'
	cyan = '\033[96m'
	darkcyan = '\033[36m'
	blue = '\033[94m'
	green = '\033[92m'
	yellow = '\033[93m'
	red = '\033[91m'
	bold = '\033[1m'
	underline = '\033[4m'
	end = '\033[0m'



# init CLI
itslearningCLI(config)


#EOF
