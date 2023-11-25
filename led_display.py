from flask import Flask, request
import requests

app = Flask(__name__)


def runmonitoring_subscription():

    subscription_request_xml = """<?xml version="1.0" encoding="utf-8"?>
    <SubscribeRequest>
        <Client-IP-Address>10.0.9.208</Client-IP-Address>
        <ReplyPort>1698</ReplyPort>
        <ReplyPath>/RunMonitoringDeliveryReply/1</ReplyPath>
    </SubscribeRequest>"""
    print(subscription_request_xml)

    response = requests.post('http://10.0.9.227:8000/avms/runmonitoring', headers = {'Content-Type': 'application/xml'}, data=subscription_request_xml)
    response.raise_for_status()  # Raises HTTPError for bad responses


@app.route('/RunMonitoringDeliveryReply/1', methods=['POST'])   
def runmonitoring_reply():
    data = request.data.decode("utf-8")
    print("Received data:", data)
    # Add your logic to process the received data here
    return "Data received successfully"


if __name__ == '__main__':
    runmonitoring_subscription()
    # Start the Flask application first
    app.run(host='10.0.9.208', port=1698, debug=False)
