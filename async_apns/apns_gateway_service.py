import socket
import struct
from tornado import ioloop
from tornado import iostream
import binascii

class ApnsGatewayService(object):

    def close_callback(self):
        ioloop.IOLoop.instance().stop()
        self.callback()

    def send_data(self):
        #  message format: COMMAND|TOKENLEN|TOKEN|PAYLOADLEN|PAYLOAD|
        #  from https://github.com/joymax/python-apns/tree/master/APNSWrapper
        device_token = binascii.unhexlify(self.device_token_hex)
        pack_format = "!BH" + str(len(device_token)) + "sH" + str(len(self.payload)) + "s"
        self.stream.write(struct.pack(pack_format, 0,
            len(device_token),
            device_token,
            len(self.payload),
            self.payload), self.on_write_complete)

    def on_write_complete(self):
        self.stream.close()

    def host_port(self):
        return ('gateway.sandbox.push.apple.com', 2195)

    def send_notification_async(self, device_token_hex, payload, callback=None):
        self.device_token_hex = device_token_hex
        self.payload = payload
        self.callback = callback
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        self.stream = iostream.SSLIOStream(s, ssl_options={ "keyfile" : "push_key.pem", "certfile" : "pushcert.pem"})
        self.stream.set_close_callback(self.close_callback)
        self.stream.connect(self.host_port(), self.send_data)
        ioloop.IOLoop.instance().start()