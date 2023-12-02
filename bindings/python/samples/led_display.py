from flask import Flask, request
import requests
import xml.etree.ElementTree as ET

app = Flask(__name__)


def runmonitoring_subscription():

    subscription_request_xml = """<?xml version="1.0" encoding="utf-8"?>
    <SubscribeRequest>
        <Client-IP-Address>192.168.1.110</Client-IP-Address>
        <ReplyPort>1698</ReplyPort>
        <ReplyPath>/RunMonitoringDeliveryReply/1</ReplyPath>
    </SubscribeRequest>"""
    print(subscription_request_xml)

    response = requests.post('http://192.168.1.101:8000/avms/runmonitoring', headers = {'Content-Type': 'application/xml'}, data=subscription_request_xml)
    response.raise_for_status()  # Raises HTTPError for bad responses


@app.route('/RunMonitoringDeliveryReply/1', methods=['POST'])   
def runmonitoring_reply():
    data = request.data.decode("utf-8")

    try:
        # Parse the XML data
        root = ET.fromstring(data)

        # Find the VehicleJourneyRef element and extract its value
        vehicle_journey_ref = root.find(".//VehicleJourneyRef").text

        # Print the extracted value
        print(vehicle_journey_ref)

        # Add your logic to process the received data here

        return vehicle_journey_ref

    except ET.ParseError as e:
        print("Error parsing XML:", str(e))
        return "Error parsing XML"


if __name__ == '__main__':
    runmonitoring_subscription()
    # Start the Flask application first
    app.run(host='192.168.1.110', port=1698, debug=False)
