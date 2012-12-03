from async_apns.apns_gateway_service import ApnsGatewayService

def callback():
    print "Done sending notification"

def test():
    token_hex = "......"
    payload = '{ "aps" : { "alert" : "This is a test" } }'
    ApnsGatewayService().send_notification_async(token_hex, payload, callback)

if __name__ == "__main__":
    test()