import serial
import re


class IBeamSmart:

    def __init__(self, USB_port):
        print(USB_port)
        connection_parameters = {
            # connection parameters for the IBeamSmart (taken from the manual)
            # manuals recommand Direct connection via COMx with "115200,8,N,1"
            # and serial interface handshake “none“
            'port': USB_port,
            'baudrate': 115200,
            'bytesize':  serial.EIGHTBITS,
            'parity': serial.PARITY_NONE,
            'stopbits': serial.STOPBITS_ONE,
            'rtscts': False,
            'xonxoff': False
        }
        # first establish connection
        print('Connection to the laser')
        self.ser = serial.Serial(**connection_parameters)
        print('Connection successful')
        self.set_power(1, channel=1)
        self.set_power(1, channel=2)

    def __del__(self):
        # clsoe the serial connection before the object gets deleted
        self.set_power(0, channel=1)
        self.set_power(0, channel=2)
        self.off()
        if self.ser.is_open:
            self.ser.close()

    def on(self) -> None:
        self.ser.write(b'la on\r')
        self.ser.readline()
        print('status: ' + self.get_laser_status())
        print('power: {} mW'.format(self.get_power()))

    def off(self) -> None:
        self.ser.write(b'la off\r')
        self.ser.readline()
        print('status: ' + self.get_laser_status())

    def set_power(self, pow: float, channel=1) -> None:
        """Return the power of the laser in mW on a given channel"""
        self.ser.write('ch {} pow {}\r'.format(channel, pow).encode())
        self.ser.readline()
        print('power: {} mW'.format(self.get_power()))

    def get_power(self) -> int:
        """Return the power of the laser in mW"""
        self.ser.write(b'sh pow\r')
        self.ser.readline()
        response = self.ser.readline().decode('unicode_escape')
        # a regular expression is used to find all the digit in the response
        # from the response format, we know there is only one match
        # output the power in uW, we convert it to mW
        pow_mW = int(re.findall(r'\d+', response)[0]) / 1e3
        return pow_mW

    def get_laser_status(self) -> str:
        self.ser.write(b'sta la\r')
        self.ser.readline()
        response = self.ser.readline().decode('unicode_escape')[:-2]
        return response
