from sx1262 import SX1262
import time
import board
import busio

import adafruit_gps
import terminalio
import displayio
from adafruit_display_text import label
import adafruit_displayio_ssd1306

uart = busio.UART(board.P0_20, board.P0_22, baudrate=9600, timeout=10)

gps = adafruit_gps.GPS(uart, debug=False)  # Use UART/pyserial
gps.send_command(b"PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0")
gps.send_command(b"PMTK220,1000")

# Define pin assignments for CircuitPython
# These are example pins - adjust according to your specific board layout
# For nRF52-based boards, use P pins. For other boards, try board.SCK, board.MOSI, board.MISO
CLK_PIN = board.P1_11      # SPI clock (or board.SCK)
MOSI_PIN = board.P1_15    # SPI MOSI (or board.MOSI)
MISO_PIN = board.P0_02    # SPI MISO (or board.MISO)
CS_PIN = board.P1_13        # Chip select
IRQ_PIN = board.P0_10       # Interrupt/DIO1
RST_PIN = board.P0_09       # Reset
GPIO_PIN = board.P0_29     # GPIO/Busy

sx = SX1262(spi_bus=1, clk=CLK_PIN, mosi=MOSI_PIN, miso=MISO_PIN, 
            cs=CS_PIN, irq=IRQ_PIN, rst=RST_PIN, gpio=GPIO_PIN)

# LoRa
sx.begin(freq=923, bw=500.0, sf=12, cr=8, syncWord=0x12,
         power=-5, currentLimit=60.0, preambleLength=8,
         implicit=False, implicitLen=0xFF,
         crcOn=True, txIq=False, rxIq=False,
         tcxoVoltage=1.7, useRegulatorLDO=False, blocking=True)

# FSK
##sx.beginFSK(freq=923, br=48.0, freqDev=50.0, rxBw=156.2, power=-5, currentLimit=60.0,
##            preambleLength=16, dataShaping=0.5, syncWord=[0x2D, 0x01], syncBitsLength=16,
##            addrFilter=SX126X_GFSK_ADDRESS_FILT_OFF, addr=0x00, crcLength=2, crcInitial=0x1D0F, crcPolynomial=0x1021,
##            crcInverted=True, whiteningOn=True, whiteningInitial=0x0100,
##            fixedPacketLength=False, packetLength=0xFF, preambleDetectorLength=SX126X_GFSK_PREAMBLE_DETECT_16,
##            tcxoVoltage=1.6, useRegulatorLDO=False,
##            blocking=True)

try:
    from i2cdisplaybus import I2CDisplayBus
except ImportError:
    from displayio import I2CDisplay as I2CDisplayBus
    
displayio.release_displays()
i2c = busio.I2C(board.P0_11, board.P1_04)
#i2c = board.I2C()
display_bus = I2CDisplayBus(i2c, device_address=0x3C)
display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=128, height=64)

splash = displayio.Group()
display.root_group = splash

text="startup..."
ta = label.Label(terminalio.FONT, text=text, color=0xFFFF00, x=5, y=5)
splash.append(ta)

tb = label.Label(terminalio.FONT, text=text, color=0xFFFF00, x=5, y=20)
splash.append(tb)

tc = label.Label(terminalio.FONT, text=text, color=0xFFFF00, x=5, y=35)
splash.append(tc)

td = label.Label(terminalio.FONT, text=text, color=0xFFFF00, x=5, y=50)
splash.append(td)


print("listening...")

last_print = time.monotonic()

lat=0
lon=0

while True:
    #print("listening...")
    
    #print("gps update")
    gps.update()
        
    current = time.monotonic()
    if current - last_print >= 1.0:
        last_print = current
        if not gps.has_fix:
            print("no fix")
            tc.text=f"lat:"
            td.text=f"lon:"
            lat=0.
            lon=0.
        else:
            #print(f"lat: {gps.latitude:.6f}, lon: {gps.longitude:.6f}")
            tc.text=f"lat: {gps.latitude:.6f}"
            td.text=f"lon: {gps.longitude:.6f}"
            lat=gps.latitude
            lon=gps.longitude
            print(f"lat: {gps.latitude:.6f}",f"lon: {gps.longitude:.6f}")
            
            msg, err = sx.recv()
            #msg, err = sx.recv(timeout_en=True, timeout_ms=1000)
            if len(msg) > 0:
                # Update GPS when message is received
                #gps.update()
                
                error = SX1262.STATUS[err]
                rssi = sx.getRSSI()
                msg_str = str(msg, 'utf-8') if isinstance(msg, bytes) else str(msg)
                
              
                 
                #print("Message:", msg)
                ta.text="-> "+msg_str
                #print("Error:", error)
                #print("RSSI:", rssi, "dBm")
                tb.text="RSSI: "+str(rssi)
                #print("-" * 40)
                
                # Convert message to string before combining into outstring
                outstring=msg_str+","+str(rssi)+","+str(lat)+","+str(lon)
                print(outstring)
