import tornado.web
from async_apns.notification_handler import NotificationHandler

class Application(tornado.web.Application):

    def __init__(self):
        handlers = [
            (r"/notifications/(?P<device_token>[\w\d]+)", NotificationHandler)
        ]
        tornado.web.Application.__init__(self, handlers)

def main():
    app =Application()
    app.listen(9001)

    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()