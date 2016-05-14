import os
import sys
from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.wsgi import wsgiapp

TOP = "<div class='top'>Middleware TOP</div>"
BOTTOM =  "<div class='botton'>Middleware BOTTOM</div>"

class MyMiddleWare(object):
		def __init__(self, app):
			self.app = app

		def __call__(self, environ, start_response):
			response = self.app(environ, start_response)[0].decode()
			if response.find('<body>') == True:
				beforeBody,remainder = response.split('<body>')
				body,footer = remainder.split('</body>')
				bodycontent = '<body>'+ TOP + bodycontent + BOTTOM+'</body>'
				return [beforeBody.encode() + body.encode() + footer.encode()]
			else:
				return [TOP + response.encode() + BOTTOM]


@wsgiapp
def app(environ, start_response):
		res = environ['PATH_INFO']
		path = "."+res
		if not os.path.isfile(path):
			path ='./index.html' 
		print('...path: ', path)
		file = open(path,'rb')
		fileContent = file.read()
		file.close() 	
 		
		start_response('200 OK', [('Content-Type', 'text/html')])
		return [fileContent.encode()]



if __name__ == '__main__':
        config = Configurator()
    
        config.add_route('index', '/index.html')
        config.add_route('default', '/')
        config.add_route('aboutme', '/about/aboutme.html')

        config.add_view(app, route_name='index')
        config.add_view(app, route_name='default')
        config.add_view(app, route_name='aboutme')

        pyramid_app = config.make_wsgi_app()
        answer = MyMiddleWare(pyramid_app)

        server = make_server('0.0.0.0', 8000, answer)
        server.serve_forever()