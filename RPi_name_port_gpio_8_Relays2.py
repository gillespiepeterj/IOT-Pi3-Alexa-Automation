""" name_port_gpio.py
 
    This is a demo python file showing how to take paramaters
    from command line for device name, port, and GPIO.
    All credit goes to https://github.com/toddmedema/echo/
    for making the first working versions of this code.
"""
 
import fauxmo
import logging
import time
import sys
import RPi.GPIO as GPIO ## Import GPIO library
 
from debounce_handler import debounce_handler
 
logging.basicConfig(level=logging.DEBUG)
 
class device_handler(debounce_handler):
    """Publishes the on/off state requested,
       and the IP address of the Echo making the request.
    """
    #TRIGGERS = {str(sys.argv[1]): int(sys.argv[2])}
    #TRIGGERS = {"office": 52000}
    TRIGGERS = {"robot": 52000, "servos": 51000, "operation rights": 53000, "pause": 52002, "demo": 52003, "pack": 52004,
                "unpack": 52005, "available": 52006}

    def act(self, client_address, state, name):
        print("State", state, "from client @", client_address)
        # GPIO.setmode(GPIO.BOARD) ## Use board pin numbering
        # GPIO.setup(int(7), GPIO.OUT)   ## Setup GPIO Pin to OUTPUT
        # GPIO.output(int(7), state) ## State is true/false

        ############# Uncomment this code to revers the relay polarity ############
        if state==True:
            state = False
        else:
            state = True
        ############# Uncomment this code to revers the relay polarity ############

        if name=="robot":
            GPIO.setmode(GPIO.BOARD) ## Use board pin numbering
            GPIO.setup(int(7), GPIO.OUT)   ## Setup GPIO Pin to OUTPUT
            GPIO.output(int(7), state) ## State is true/false
            time.sleep(1)
            state = True
            GPIO.output(int(7), state)
        elif name =="servos":
            GPIO.setmode(GPIO.BOARD) ## Use board pin numbering
            GPIO.setup(int(11), GPIO.OUT)   ## Setup GPIO Pin to OUTPUT
            GPIO.output(int(11), state) ## State is true/false
            time.sleep(1)
            state = True
            GPIO.output(int(11), state)
        elif name =="operation rights":
            GPIO.setmode(GPIO.BOARD) ## Use board pin numbering
            GPIO.setup(int(13), GPIO.OUT)   ## Setup GPIO Pin to OUTPUT
            GPIO.output(int(13), state) ## State is true/false
        elif name == "pause":
            GPIO.setmode(GPIO.BOARD)  ## Use board pin numbering
            GPIO.setup(int(5), GPIO.OUT)  ## Setup GPIO Pin to OUTPUT
            GPIO.output(int(5), state)  ## State is true/false
            time.sleep(1)
            state = True
            GPIO.output(int(5), state)
        elif name == "demo":
            GPIO.setmode(GPIO.BOARD)  ## Use board pin numbering
            GPIO.setup(int(16), GPIO.OUT)  ## Setup GPIO Pin to OUTPUT
            GPIO.output(int(16), state)  ## State is true/false
        elif name == "pack":
            GPIO.setmode(GPIO.BOARD)  ## Use board pin numbering
            GPIO.setup(int(8), GPIO.OUT)  ## Setup GPIO Pin to OUTPUT
            GPIO.output(int(8), state)  ## State is true/false
        elif name == "unpack":
            GPIO.setmode(GPIO.BOARD)  ## Use board pin numbering
            GPIO.setup(int(12), GPIO.OUT)  ## Setup GPIO Pin to OUTPUT
            GPIO.output(int(12), state)  ## State is true/false
        elif name == "available":
            GPIO.setmode(GPIO.BOARD)  ## Use board pin numbering
            GPIO.setup(int(10), GPIO.OUT)  ## Setup GPIO Pin to OUTPUT
            GPIO.output(int(10), state)  ## State is true/false
        else:
            print("Device not found!")




        return True
 
if __name__ == "__main__":
    # Startup the fauxmo server
    fauxmo.DEBUG = True
    p = fauxmo.poller()
    u = fauxmo.upnp_broadcast_responder()
    u.init_socket()
    p.add(u)
 
    # Register the device callback as a fauxmo handler
    d = device_handler()
    for trig, port in d.TRIGGERS.items():
        fauxmo.fauxmo(trig, u, p, None, port, d)
 
    # Loop and poll for incoming Echo requests
    logging.debug("Entering fauxmo polling loop")
    while True:
        try:
            # Allow time for a ctrl-c to stop the process
            p.poll(100)
            time.sleep(0.1)
        except Exception as e:
            logging.critical("Critical exception: "+ e.args  )
            break
