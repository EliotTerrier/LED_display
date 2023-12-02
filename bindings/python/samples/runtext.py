#!/usr/bin/env python
# Display a runtext with double-buffering.
from samplebase import SampleBase
from rgbmatrix import graphics
import time
from flask import Flask, request
import requests
import xml.etree.ElementTree as ET
from threading import Thread, Condition
from lxml import etree

app = Flask(__name__)
global_text = "Waiting for data..."
text_updated = Condition()

def runmonitoring_subscription():

    subscription_request_xml = """<?xml version="1.0" encoding="utf-8"?>
    <SubscribeRequest>
        <Client-IP-Address>192.168.1.110</Client-IP-Address>
        <ReplyPort>1698</ReplyPort>
        <ReplyPath>/RunMonitoringDeliveryReply/1</ReplyPath>
    </SubscribeRequest>"""
    print(subscription_request_xml)

    response = requests.post('http://192.168.1.103:8000/avms/runmonitoring', headers = {'Content-Type': 'application/xml'}, data=subscription_request_xml)
    response.raise_for_status()  # Raises HTTPError for bad responses

@app.route('/RunMonitoringDeliveryReply/1', methods=['POST'])   
def runmonitoring_reply():
    global global_text
    data = request.data.decode("utf-8")
    try:
        # Parse the XML data
        root = ET.fromstring(data)
        new_vehicle_journey_ref = root.find(".//VehicleJourneyRef").text
        if new_vehicle_journey_ref != global_text:
            with text_updated:
                global_text = new_vehicle_journey_ref
                text_updated.notify()
        return global_text
        # Print the extracted value
    except ET.ParseError as e:
        print("Error parsing XML:", str(e))
        return "Error parsing XML"
    
  
class RunText(SampleBase):
    def __init__(self, *args, **kwargs):
        super(RunText, self).__init__(*args, **kwargs)


    def run(self):
        global global_text
        offscreen_canvas = self.matrix.CreateFrameCanvas()
        font = graphics.Font()
        font.LoadFont("../../../fonts/7x13.bdf")
        textColor = graphics.Color(255, 255, 0)
        pos = offscreen_canvas.width
        my_text = "waiting for data..."

        
        while True:
            with text_updated:
               #text_updated.wait(timeout=1.0)
               my_text = global_text
            offscreen_canvas.Clear()
            len = graphics.DrawText(offscreen_canvas, font, pos, 10, textColor, my_text)
            pos -= 1
            if (pos + len < 0):
                pos = offscreen_canvas.width

            time.sleep(0.05)
            offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)
  
def run_text_process(run_text):
    if not run_text.process():
        run_text.print_help()
          
# Main function
if __name__ == "__main__":
    runmonitoring_subscription()
    flask_thread = Thread(target=app.run, kwargs={'host': '192.168.1.110', 'port': 1698, 'debug': False, 'load_dotenv': False})
    flask_thread.start()

    run_text = RunText()
    run_text_thread = Thread(target=run_text_process, args=(run_text,))
    run_text_thread.start()
    
    
