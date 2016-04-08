import logging
from time import sleep
from serial import Serial 

class Serial3(Serial):
   def write(self, cmd):
        cmd = bytes(cmd.encode('utf-8'))
        self.ser.write(cmd)

   def read(self):
        data = self.ser.read()
        return data.decode('utf-8')


class spid(object):
    # get the Comm Port information
    # input_variable = raw_input ("Enter comm port: (Default /dev/cu.usbserial-A104FZJ8 ")
    # if len(input_variable) < 5:
    # input_variable="/dev/cu.usbserial-A104FZJ8"

    def write(self, cmd):
        cmd = bytes(cmd.encode('utf-8'))
        self.ser.write(cmd)

    def read(self):
        data = self.ser.read()
        return data.decode('utf-8')

    def __init__(self, pport="/dev/tty.usbserial-A104FZJ8", pspeed=1200, ptimeout=0):
        # define constants.
        self.loop = 1
        self.zero5 = chr(0) + chr(0) + chr(0) + chr(0) + chr(0)
        self.logger = logging.getLogger(__name__)

        # Open Comm Port
        try:
            self.logger.debug("Trying to Open Port " + pport)
            self.ser = serial.Serial(port=pport,speed= pspeed, timeout=ptimeout)
            self.logger.Info("Port " + pport + " With no error")
        except Exception as e:
            self.logger.error(str.format("Unable to open device {} Error is ", pport, str(e)))

    def stop(self):
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
        # Build the status command word.
        out = chr(87) + self.zero5 + self.zero5 + chr(31) + chr(32)
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
            print(("Rotator currently at %3d " % (azs) + "Degrees"))

    def moveto(self, az):
        # send command to rotator controller to move rotator
        # to the desired azimuth.
        self.logger.debug(str.format("Want to move to {}", az))
        az = int(float(az))
        # test to see if azimuth is in the range of 0 to 360 Degrees
        if (az < 0 or az > 360):
            self.logger.error("Invalid Azimuth")
            return
        else:
            # Convert Azimuth to number required by controller
            az = az + 360
            # Build message to be sent to controller
            self.logger.debug(str.format("Calculated move to {}", az))
            out = chr(87) + str(az) + chr(48) + chr(1) + self.zero5 + chr(47) + chr(32)
            # Send message to Controller
            try:
                x = self.ser.write(out)
                self.logger.debug(str.format("Move command successfully sent"))
            except:
                self.logger.error(str.format("Unable to write to Spid"))

    def __del__(self):
        try:
            self.ser.flushInput()
            self.ser.flushOutput()
            self.ser.close()
            sleep(3)
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
        except:
            self.logger.info("Spid Closed")


if __name__ == "__main__":
    import datetime

    s = spid()
    s.moveto(100)
    sleep(4)
    s.moveto(90)

