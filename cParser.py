# cparse v0.2
#
# A python-based static-webpage-generator using markdown-syntax.
#
#
# The MIT License (MIT)
#
# Copyright (c) 2013 Timm Albers
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
#
# PREREQUIREMENTS
#
# Please make sure to have Python-Markdown installed.
# Use pip install markdown to install the modul or see 
# http://pythonhosted.org/Markdown for additional infos.
#
# Furthermore, you need watchdog.
# Use pip install watchdog to install the modul or see
# https://github.com/gorakhargosh/watchdog for additional infos.
#
# It is recommended (but not necessary), to install LibYAML.
# Use brew install libyaml (on Mac OSX) to do so or see 
# http://pyyaml.org/wiki/LibYAML for additional infos.
#
#
# INSTALLATION
#
# Add the following lines to .profile in your user-folder.
#		cparse() {
#			python /path/to/cParser.py "$1"
#		}
#
#
# USAGE
#
# cparse folder
# The folder has to look something like this:
#
#		folder
#		|- content
#		   |- pages
#		      '- Example page.md
#		   '- posts
#		      '- Example post.md
#		'- template
#		   |- index.html
#		   |- page.html
#		   '- post.html
#
# The content-folder contains all content of the page in markdown-format.
# cparse will use the last-modified-date of each post/*.md-file to sort the entrys.
# The template folder contains all templates. index.html is the main-template, which is used for each page.
# The page.html and post.html will be included in index.html when they are needed.
#
# Have a look in the demo-folder!
#
# 
# TEMPLATING
#
# You can use the following shortcuts in every file placed in the template-folder.
#
#		{{posts}}					Include all posts.
#
#		{{pages}}					Loop through all pages.
#			{{page.title}}			Include page.title.
#			{{page.url}}			Include page.url.
#			{{page.time}}			Include page.time.
#			{{page.content}}		Include page.content.
#		{{/pages}}					End of loop.
#
# You can use the following shortcuts in page.html.
#
#		{{page.title}}				Include page.title.
#		{{page.url}}				Include page.url.
#		{{page.time}}				Include page.time.
#		{{page.content}}			Include page.content.
#
# And the following in post.html.
#
#		{{post.title}}				Include post.title.
#		{{post.time}}				Include post.time.
#		{{post.content}}			Include post.content.

import sys
import os
import time
import shutil
import markdown
#from watchdog.observers import Observer
#from watchdog.events import FileSystemEventHandler

class Post:
	def __init__(self, title, time, content):
		self.title = title
		self.time = time
		self.content = content

class Page:
	def __init__(self, title, url, time, content):
		self.title = title
		self.url = url
		self.time = time
		self.content = content

class Main: 
	def __init__(self):
		self.folder = sys.argv[1]
		if self.folder == "":
			print "usage: cparse folder"
		else:
			sys.argv.remove(sys.argv[0])
			sys.argv.remove(sys.argv[0])

			self.options = []

			append = False
			for arg in sys.argv:
				if append:
					tmp.append(arg)
					self.options.append(tmp)
					append = False
				elif arg[0] == '-':
					tmp = []
					tmp.append(arg)
					append = True

	def parse(self):
		if os.path.isdir(self.folder):
			if os.path.isdir(self.folder + "/template"):
				if os.path.isdir(self.folder + "/content"):
					if os.path.isdir(self.folder + "/content/posts") or os.path.isdir(self.folder + "/content/pages"):
						if os.path.isdir(self.folder + "/output"):
							shutil.rmtree(self.folder + "/output")
						os.mkdir(self.folder + "/output")
						
						posts = self.getPosts()
						pages = self.getPages()

						if os.path.isfile(self.folder + "/template/index.html"):
							f = open(self.folder + "/template/index.html")
							mainTemplate = f.read()
							f.close()



							# pages loop
							startPagesLoop = mainTemplate.find("{{pages}}")
							endPagesLoop = mainTemplate.find("{{/pages}}")
							pagesLoopTemplate = mainTemplate[startPagesLoop+len("{{pages}}"):endPagesLoop]

							pagesLoopHTML = ""
							for page in pages:
								tmp = pagesLoopTemplate
								tmp = tmp.replace("{{page.title}}", page.title)
								tmp = tmp.replace("{{page.url}}", "../" + page.url + "/index.html")
								tmp = tmp.replace("{{page.time}}", time.ctime(page.time))
								tmp = tmp.replace("{{page.content}}", page.content)
								pagesLoopHTML += tmp

							mainTemplate = mainTemplate[:startPagesLoop] + pagesLoopHTML + mainTemplate[endPagesLoop+len("{{/pages}}"):]
							mainTemplate = mainTemplate.replace("{{global.home}}", "../index.html")



							if os.path.isfile(self.folder + "/template/post.html"):
								f = open(self.folder + "/template/post.html")
								postTemplate = f.read()
								f.close()

								if os.path.isfile(self.folder + "/template/page.html"):
									f = open(self.folder + "/template/page.html")
									pageTemplate = f.read()
									f.close()

									mainTemplate = self.__parsePosts(posts, postTemplate, mainTemplate)

									print "parsing...",
									# create index.html
									f = open(self.folder + "/output/index.html", "w")
									indexHTML = mainTemplate
									indexHTML = indexHTML.replace("../", "")
									indexHTML = indexHTML.replace("{{content}}", "")
									f.write(indexHTML)
									f.close()

									self.__parseFiles(posts, pages, mainTemplate, postTemplate, pageTemplate)
									self.__parsePages(posts, pages, mainTemplate, postTemplate, pageTemplate)
									print "finished!"
								else:
									print "error: " + self.folder + "/template/page.html does not exist."
							else:
								print "error: " + self.folder + "/template/post.html does not exist."
						else:
							print "error: " + self.folder + "/template/index.html does not exist."
					else:
						print "error: neither " + self.folder + "/content/posts nor " + self.folder + "/content/pages does exist."
				else:
					print "error: " + self.folder + "/content does not exist."
			else: 
				print "error: " + self.folder + "/template does not exist."
		else:
			print "error: given name is not a directory or does not exist."

	def __parseFiles(self, posts, pages, mainTemplate, postTemplate, pageTemplate, subdir = ""):
		if subdir != "":
			subdir += "/"
		templatePath = self.folder + "/template/" + subdir

		items = os.listdir(templatePath)
		for item in items:
			if os.path.isdir(templatePath + "/" + item):
				self.__parseFiles(posts, pages, mainTemplate, postTemplate, pageTemplate, item)
			elif not (subdir == "" and (item == "index.html" or item == "page.html" or item == "post.html")) and item != ".DS_Store":
				f = open(templatePath + item)
				data = f.read()
				f.close()

				data = self.__parsePosts(posts, postTemplate, data)

				dst = self.folder + "/output/" + subdir
				if not os.path.isdir(dst):
					os.makedirs(dst)
				f = open(dst + item, "w")
				f.write(data)
				f.close

	def __parsePages(self, posts, pages, mainTemplate, postTemplate, pageTemplate):
		for page in pages:
			if not os.path.isdir(self.folder + "/output/" + page.url):
				os.mkdir(self.folder + "/output/" + page.url)

			data = pageTemplate
			data = data.replace("{{page.title}}", page.title)
			data = data.replace("{{page.url}}", page.url)
			data = data.replace("{{page.time}}", time.ctime(page.time))
			data = data.replace("{{page.content}}", page.content)

			data = mainTemplate.replace("{{content}}", data)

			data = self.__parsePosts(posts, postTemplate, data)

			f = open(self.folder + "/output/" + page.url + "/index.html", "w")
			f.write(data)
			f.close()


	def __parsePosts(self, posts, postTemplate, data):
		postsHTML = ""
		for post in posts:
			tmp = postTemplate
			tmp = tmp.replace("{{post.title}}", post.title)
			tmp = tmp.replace("{{post.time}}", time.ctime(post.time))
			tmp = tmp.replace("{{post.content}}", post.content)
			postsHTML += tmp

		data = data.replace("{{posts}}", postsHTML)

		return data

	def getPosts(self):
		posts = []

		if os.path.isdir(self.folder + "/content/posts"):
			items = os.listdir(self.folder + "/content/posts")
			for item in items:
				if os.path.isfile(self.folder + "/content/posts/" + item):
					parts = item.split(".")
					ext = parts[len(parts)-1]
					title = item.replace("." + ext, "")
					time = os.path.getmtime(self.folder + "/content/posts/" + item)

					if ext == "md":
						f = open(self.folder + "/content/posts/" + item)
						data = f.read()
						f.close()
						posts.append(Post(title, time, markdown.markdown(data)))
						
		else:
			print "warning: " + self.folder + "/content/posts does not exist."

		return posts

	def getPages(self):
		pages = []

		if os.path.isdir(self.folder + "/content/pages"):
			items = os.listdir(self.folder + "/content/pages")
			for item in items:
				if os.path.isfile(self.folder + "/content/pages/" + item):
					parts = item.split(".")
					ext = parts[len(parts)-1]
					title = item.replace("." + ext, "")
					url = title.lower().replace(" ", "-")
					time = os.path.getmtime(self.folder + "/content/pages/" + item)

					if ext == "md":
						f = open(self.folder + "/content/pages/" + item)
						data = f.read()
						f.close()
						pages.append(Page(title, url, time, markdown.markdown(data)))
		else:
			print "warning: " + self.folder + "/content/pages does not exist."

		return pages

print "cparse v0.2"

main = Main()
main.parse()