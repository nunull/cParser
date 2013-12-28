# cparse v0.2

A python-based static-webpage-generator using markdown-syntax.


## The MIT License (MIT)

> Copyright (c) 2013 Timm Albers
> 
> Permission is hereby granted, free of charge, to any person obtaining a copy
> of this software and associated documentation files (the "Software"), to deal
> in the Software without restriction, including without limitation the rights
> to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
> copies of the Software, and to permit persons to whom the Software is
> furnished to do so, subject to the following conditions:
> 
> The above copyright notice and this permission notice shall be included in
> all copies or substantial portions of the Software.
> 
> THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
> IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
> FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
> AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
> LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
> OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
> THE SOFTWARE.


## PREREQUIREMENTS

Please make sure to have *Python-Markdown* installed.
Use pip install markdown to install the modul or see 
[markdown](http://pythonhosted.org/Markdown) for additional infos.

Furthermore, you need *watchdog*.
Use pip install watchdog to install the modul or see
[watchdog](https://github.com/gorakhargosh/watchdog) for additional infos.

It is recommended (but not necessary), to install *LibYAML*.
Use brew install libyaml (on Mac OSX) to do so or see 
[LibYAML](http://pyyaml.org/wiki/LibYAML) for additional infos.


## INSTALLATION

Add the following lines to .profile in your user-folder.
	cparse() {
	    python /path/to/cParser.py "$1"
	}


## USAGE

	cparse folder
The folder has to look something like this:

	folder
	|- content
	   |- pages
	      '- Example page.md
	   '- posts
	      '- Example post.md
	'- template
	   |- index.html
	   |- page.html
	   '- post.html

The content-folder contains all content of the page in *markdown*-format.
*cparse* will use the last-modified-date of each *post/\**.md-file to sort the entrys.
The template folder contains all templates. index.html is the main-template, which is used for each page.
The page.html and post.html will be included in index.html when they are needed.

 
## TEMPLATING

You can use the following shortcuts in every file placed in the template-folder.

	{{ posts }}					Include all posts. (Use without the withespaces)

	{{pages}}					Loop through all pages.
		{{page.title}}			Include page.title.
		{{page.url}}			Include page.url.
		{{page.time}}			Include page.time.
		{{page.content}}		Include page.content.
	{{/pages}}					End of loop.

You can use the following shortcuts in page.html.

	{{page.title}}				Include page.title.
	{{page.url}}				Include page.url.
	{{page.time}}				Include page.time.
	{{page.content}}			Include page.content.

And the following in post.html.

	{{post.title}}				Include post.title.
	{{post.time}}				Include post.time.
	{{post.content}}			Include post.content.