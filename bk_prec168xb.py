# Referenece:
#  https://bkpmedia.s3.amazonaws.com/downloads/programming_manuals/en-us/168xB_programming_manual.pdf
#  https://pymotw.com/2/argparse/
#  https://pythonhosted.org/pyserial/

# Import
import argparse
import serial

# Commands
#  Power ON
BK_PRE_168XB_CMD_PWR_ON = 'SOUT0'

#  Power OFF
BK_PRE_168XB_CMD_PWR_OFF = 'SOUT1'

#  Voltage Configuration
BK_PRE_168XB_CMD_VLTLVL = 'SOVP'
BK_PRE_168XB_MAX_VLTLVL = 180


# Serial port configuration
BK_PRE_168XB_BAUDRATE = 9600
BK_PRE_168XB_BYTE_SIZE = serial.EIGHTBITS
BK_PRE_168XB_PARITY = serial.PARITY_NONE
BK_PRE_168XB_STOP_BITS = serial.STOPBITS_ONE
#BK_PRE_168XB_FLOW_CTRL

# Command sending
def sendCMD(serialPort, cmd, param = 0):
    # Open Serial Port
    try:
        serialIO = serial.Serial(serialPort,
                                    BK_PRE_168XB_BAUDRATE,
                                    bytesize=BK_PRE_168XB_BYTE_SIZE,
                                    parity=BK_PRE_168XB_PARITY,
                                    stopbits=BK_PRE_168XB_STOP_BITS)
    
        if BK_PRE_168XB_CMD_VLTLVL == cmd:
            if (BK_PRE_168XB_MAX_VLTLVL > param) and (0 < param):
                cmdStr = '%(cmdPrefix)s%(voltageLvl)03d' % {"cmdPrefix" : BK_PRE_168XB_CMD_VLTLVL, "voltageLvl" : param}
                
        else:
            # Power ON/OFF
            cmdStr = cmd
        
        print('Command String: %(arg1)s' % {"arg1" : cmdStr})
        serialIO.write(cmdStr + '\r')
        
        # Close Serial Port
        serialIO.close()
    
    except serial.SerialException:
        print('Failed to open Serial Port: ' + serialPort)
    

def main():
    # Initialize ArgumentParser
    parser = argparse.ArgumentParser('Controller for BK Precision Power Supply 168xB')
    
    # Define arguments
    parser.add_argument('-p',
                        action='store',
                        dest='serialPort',
                        required=True,
                        help='Virtual COM port connected to the device')
    
    parser.add_argument('-s',
                        action='store',
                        dest='state',
                        help='Turn \'ON\' or \'OFF\'')
    
    parser.add_argument('-v',
                        action='store',
                        dest='voltageLvl',
                        type=int,
                        help='Configure Output Voltage Level')
    
    # Parse input arguments
    args = parser.parse_args()
    
    # Configure Serial Port
    cfgSerialPort(args.serialPort)
    
    if 'ON' == args.state:
        sendCMD(BK_PRE_168XB_CMD_PWR_ON)
        
    elif 'OFF' == args.state:
        sendCMD(BK_PRE_168XB_CMD_PWR_OFF)
        
    if args.voltageLvl:
        sendCMD(BK_PRE_168XB_CMD_VLTLVL, args.voltageLvl)
        
    
if __name__ == "__main__":
    main()
