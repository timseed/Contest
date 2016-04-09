# required libraries
import logging
from time import sleep

import serial


class Serial3(serial.Serial):
    def write(self, cmd):
        cmd = bytes(cmd.encode('utf-8'))
        super(Serial3, self).write(cmd)

    def read(self):
        data = super(Serial3,self).read()
        return data.decode('utf-8')

class spid(object):
    def __init__(self):
        # get the Comm Port information
        # input_variable = raw_input ("Enter comm port: (Default /dev/cu.usbserial-A104FZJ8 ")
        # if len(input_variable) < 5:
        # input_variable="/dev/cu.usbserial-A104FZJ8"
        self.logger=logging.getLogger(__name__)
        input_variable = "/dev/tty.usbserial-A104FZJ8"
        port = input_variable
        # define constants.
        self.loop = 1
        self.zero5 = chr(0) + chr(0) + chr(0) + chr(0) + chr(0)

        # Open Comm Port
        try:
            self.ser = Serial3(port, 1200, timeout=0)
            self.logger.info("Spid Device opened correctly")
        except Exception as e:
            self.logger.error("Error opening Spid device error is "+str(e))

    def moveto(self,az):
         # test to see if azimuth is in the range of 0 to 360 Degrees
        az=int(float(az))
        if (az < 0 or az > 360):
            self.logger.error("Invalid Azimuth")
            return
        else:
            # Convert Azimuth to number required by controller
            az = az + 360
            # Build message to be sent to controller
            out = chr(87) + str(az) + chr(48) + chr(1) + self.zero5 + chr(47) + chr(32)
            # Send message to Controller
            x = self.ser.write(out)
            self.logger.info(str.format("Spid moved to {}",az))

    def stop(self):
        # Build the stop command word.
        out = chr(87) + self.zero5 + self.zero5 + chr(15) + chr(32)
        x = self.ser.write(out)
        # Wait for answer from controller
        sleep(0.5)

        data = self.ser.read()
        # once all 5 characters are received, decode location.
        if len(data) >= 5:
            s1 = ord(data[1].encode('latin-1'))
            s2 = ord(data[2].encode('latin-1'))
            s3 = ord(data[3].encode('latin-1'))
            azs = s1 * 100 + s2 * 10 + s3
            # Since the controller sends the status based on 0 degrees = 360
            # remove the 360 here
            azs = azs - 360
            print(("Rotator stopped at %3d " % (azs) + "Degrees"))

    def status(self):
        # Build the stop command word.
        out = chr(87) + self.zero5 + self.zero5 + chr(15) + chr(32)
        x = self.ser.write(out)
        # Wait for answer from controller
        sleep(0.5)

        data = self.ser.read()
        # once all 5 characters are received, decode location.
        if len(data) >= 5:
            s1 = ord(data[1].encode('latin-1'))
            s2 = ord(data[2].encode('latin-1'))
            s3 = ord(data[3].encode('latin-1'))
            azs = s1 * 100 + s2 * 10 + s3
            # Since the controller sends the status based on 0 degrees = 360
            # remove the 360 here
            azs = azs - 360
            print(("Rotator stopped at %3d " % (azs) + "Degrees"))

    def __del__(self):
        try:
            if self.ser.is_open():
                print("Trying to close for 2nd time")
                self.ser.flushInput()
                self.ser.flushOutput()
                self.ser.close()
            if self.ser.is_open():
                print("Failed to correctly close the serial Port - a machine restart will probably be needed.")
        except:
            print('Closing ')



if __name__ == "__main__":
    s = spid()
    sleep(2)
    s.moveto(340)
    sleep(2)
    s.moveto(350)
    sleep(4)
