# import tornado.web
# import tornado.options
# import tornado.ioloop
# import tornado.httpserver
#
# from tornado.options import define,options
# define("port",default=8000,type=int,help="i o o")
#
# class AA(tornado.web.RequestHandler):
#     def get(self, *args, **kwargs):
#         pass
#     def post(self, *args, **kwargs):
#         pass
#
#
# if __name__ == '__main__':
#     tornado.options.parse_command_line()
#     app = tornado.web.Application(handlers=[(r'/',AA)],
#                                   template_path=os.path.join(BASE,'template'),
#                                   static_path=os.path.join(BASE,'static')
#                                   )
#     server = tornado.httpserver.HTTPServer(app)
#     server.listen(options.port)
#     tornado.ioloop.IOLoop.current().start()   #ioloop就是对I/O多路复用的封装

import time

r=time.time()
print(r)
r=time.localtime(r)
print(r)
regx="%Y-%m-%d:%H:%M:%S"
r=time.strftime(regx,r)
print(r)
# 1.获取时间戳 2.转换时间元祖 3.转换为时间字符串
