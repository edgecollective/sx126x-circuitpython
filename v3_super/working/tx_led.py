from sx1262 import SX1262
import time
import board
import digitalio

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
         power=22, currentLimit=60.0, preambleLength=8,
         implicit=False, implicitLen=0xFF,
         crcOn=True, txIq=False, rxIq=False,
         tcxoVoltage=1.7, useRegulatorLDO=False, blocking=True)


led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT


    
    
i = 0

while True:
    sendstring=str(i)
    sx.send(sendstring.encode())
    print("sent", i)
    led.value = True
    time.sleep(0.1)
    led.value = False
    time.sleep(0.1)
    
    i=i+1
    time.sleep(2)
