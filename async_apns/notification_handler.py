from async_apns.apns_gateway_service import ApnsGatewayService
from tornado.web import asynchronous, RequestHandler

class NotificationHandler(RequestHandler):

    @asynchronous
    def post(self, device_token):
        payload = self.request.body
        ApnsGatewayService().send_notification_async(device_token, payload, self.on_completion)
        self.set_status(200)
        self.finish()

    def on_completion(self):
        print "Sent async notification to APNS"