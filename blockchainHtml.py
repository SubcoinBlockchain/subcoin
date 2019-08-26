def parseHtml(file):
	htmlF = open(file+'.html','r')
	htmlD = htmlF.read()
	return str(htmlD)