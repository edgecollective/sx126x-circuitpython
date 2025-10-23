from sx1262 import SX1262
import time
import board

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

while True:
    print("listening...")
    msg, err = sx.recv()
    if len(msg) > 0:
        error = SX1262.STATUS[err]
        rssi = sx.getRSSI()
        print("Message:", msg)
        print("Error:", error)
        print("RSSI:", rssi, "dBm")
        print("-" * 40)