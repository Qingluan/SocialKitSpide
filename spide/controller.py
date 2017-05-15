
## this is write by qingluan 
# just a inti handler 
# and a tempalte offer to coder
import json
import tornado
import tornado.web
from tornado.websocket import WebSocketHandler
from qlib.net import to
from SocialKit.phantomjs import WebDriver
from chardet import detect


class BaseHandler(tornado.web.RequestHandler):
    def prepare(self):
        self.db = self.settings['db']
        # self.L = self.settings['L']
    def get_current_user(self):
        return (self.get_cookie('user'),self.get_cookie('passwd'))
    def get_current_secure_user(self):
        return (self.get_cookie('user'),self.get_secure_cookie('passwd'))
    def set_current_seccure_user_cookie(self,user,passwd):
        self.set_cookie('user',user)
        self.set_secure_cookie("passwd",passwd)

    def json_reply(self, msg):
        self.write(json.dumps(msg))
        self.finish()


class SocketHandler(WebSocketHandler):
    """ Web socket """
    clients = set()
    con = dict()
         
    @staticmethod
    def send_to_all(msg):
        for con in SocketHandler.clients:
            con.write_message(json.dumps(msg))
         
    @staticmethod
    def send_to_one(msg, id):
        SocketHandler.con[id(self)].write_message(msg)

    def json_reply(self, msg):
        self.write_message(json.dumps(msg))

    def open(self):
        SocketHandler.clients.add(self)
        SocketHandler.con[id(self)] = self
         
    def on_close(self):
        SocketHandler.clients.remove(self)
         
    def on_message(self, msg):
        SocketHandler.send_to_all(msg)





class IndexHandler(BaseHandler):
    
    def prepare(self):
        super(IndexHandler, self).prepare()
        self.template = "template/index.html"

    def get(self):
        # L is log function , which include ok , info , err , fail, wrn
        # self.L.ok('got')
        return self.render(self.template, post_page="/")

    @tornado.web.asynchronous
    def post(self):
        # you should get some argument from follow
        post_args = self.get_argument("some_argument")
        # .....
        # for parse json post
        # post_args = json.loads(self.request.body.decode("utf8", "ignore"))['msg']
        
        # redirect or reply some content
        # self.redirect()  
        self.write("hello world")
        self.finish()
    


class GeturiHandler(BaseHandler):
    
    def prepare(self):
        super(GeturiHandler, self).prepare()
        self.template = "template/geturi.html"

    def get(self):
        # L is log function , which include ok , info , err , fail, wrn
        # self.L.ok('got')
        return self.render(self.template, post_page="/geturi")

    def async_post(self,method, url, kargs, charset):
        if method == 'browser':
            driver = WebDriver(**kargs)
            driver.get(url)
            print("got it ",url)
            return ({
                'data':driver.page,
                'url':url,
                'code':200,
                },)


        elif method == 'requests':
            res = to(url, **kargs)
            print("got it:" , url)
            if res.status_code == 200:
                if charset:
                    encoding = charset
                else:
                    if len(res.content) > 2000:
                        test_con = res.content[:2000]
                    else:
                        test_con = res.content

                    encoding = detect(test_con).get('encoding')
                print(encoding)
                return ({
                    'data':res.content.decode(encoding, 'ignore'),
                    'url':url,
                    'code':200,
                },)
            else:
                return ({
                    'url':url,
                    'code':400,
                },)

    @tornado.web.asynchronous
    def post(self):
        
        # action = self.get_argument("action")
        # args = self.get_argument('url')
        # print(args)
        method = self.get_argument("method")
        url = self.get_argument("url")
        kargs = json.loads(self.get_argument("options"))
        charset = self.get_argument('charset')
        
        self.settings['exe'].done(self.async_post, self.json_reply, method, url, kargs, charset)
        
    