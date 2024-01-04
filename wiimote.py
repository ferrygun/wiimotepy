import cwiid
import time
import paho.mqtt.client as mqtt

# Define the MQTT broker address, port, username, and password
broker_address = "192.168.50.88"
port = 1883
username = "mqtt"
password = ""

# Create a unique client ID
client_id = "wiimote18"

button_delay = 0.5

def handle_event(mesg_list, time):
    main()


def main():
    while True:
        print('Please press buttons 1 + 2 on your Wiimote now ...')

        # Keep trying to connect to the Wiimote until successful
        '''
        while True:
            try:
                wii = cwiid.Wiimote()
                break
            except RuntimeError:
                print("Cannot connect to your Wiimote. Make sure you are holding buttons 1 + 2!")
                time.sleep(1)
            except cwiid.BluetoothError:
                print("Cannot connect to your Wiimote. Make sure you are holding buttons 1 + 2!")
                time.sleep(1)
        '''


        wii = None 
        while not wii: 
          try: 
            wii = cwiid.Wiimote() 
          except RuntimeError: 
            print("Cannot connect to your Wiimote. Make sure you are holding buttons 1 + 2!")
            time.sleep(0.5)


        
        # Create an MQTT client instance
        client = mqtt.Client(client_id)
        # Set username and password
        client.username_pw_set(username, password)
        # Connect to the broker
        client.connect(broker_address, port)

        print('Wiimote connection established!\n')
        print('Press + and - together to disconnect and quit.\n')

        wii.rumble = 1
        time.sleep(0.5)
        wii.rumble = 0

        wii.rpt_mode = cwiid.RPT_BTN
        wii.mesg_callback = handle_event

        try:
            while True:
                buttons = wii.state['buttons']


                # Detects whether + and - are held down, and if they are, it quits the program
                if (buttons - cwiid.BTN_PLUS - cwiid.BTN_MINUS == 0):
                    print('\nClosing connection ...')
                    # NOTE: This is how you RUMBLE the Wiimote
                    wii.rumble = 1
                    time.sleep(1)
                    wii.rumble = 0
                    # Disconnect from the broker
                    client.disconnect()
                    wii.close()
                    break
                    #exit(wii)

                # The following code detects whether any of the Wiimote's buttons have been pressed and then prints a statement to the screen!
                if (buttons & cwiid.BTN_LEFT):
                    print('Left pressed')
                    time.sleep(button_delay)

                if(buttons & cwiid.BTN_RIGHT):
                    print('Right pressed')
                    time.sleep(button_delay)

                if (buttons & cwiid.BTN_UP):
                    print('Up pressed')
                    time.sleep(button_delay)

                if (buttons & cwiid.BTN_DOWN):
                    print('Down pressed')
                    time.sleep(button_delay)

                if (buttons & cwiid.BTN_1):
                    print('Button 1 pressed')
                    time.sleep(button_delay)

                if (buttons & cwiid.BTN_2):
                    print('Button 2 pressed')
                    time.sleep(button_delay)

                if (buttons & cwiid.BTN_A):
                    print('Button A pressed')
                    time.sleep(button_delay)

                if (buttons & cwiid.BTN_B):
                    print('Button B pressed')
                    message = "Hello, MQTT!"
                    client.publish("test/topic", message)
                    print(f"Published: {message}")
                    time.sleep(button_delay)

                if (buttons & cwiid.BTN_HOME):
                    wii.rpt_mode = cwiid.RPT_BTN | cwiid.RPT_ACC
                    check = 0
                    while check == 0:
                        print(wii.state['acc'])
                        time.sleep(0.01)
                        check = (buttons & cwiid.BTN_HOME)
                    time.sleep(button_delay)

                if (buttons & cwiid.BTN_MINUS):
                    print('Minus Button pressed')
                    time.sleep(button_delay)

                if (buttons & cwiid.BTN_PLUS):
                    print('Plus Button pressed')
                    time.sleep(button_delay)


        except RuntimeError: 
            print("Runtime Error")
            time.sleep(0.5)

if __name__ == "__main__":
    main()
