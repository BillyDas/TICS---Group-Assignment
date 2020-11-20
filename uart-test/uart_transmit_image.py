import sensor, struct, pyb

sensor.reset()                      # Reset and initialize the sensor.
sensor.set_pixformat(sensor.RGB565) # Set pixel format to RGB565 (or GRAYSCALE)
sensor.set_framesize(sensor.QVGA)   # Set frame size to QVGA (320x240)
sensor.skip_frames(time = 2000)     # Wait for settings take effect.


# Set UART pins and baudrate
uart = pyb.UART(1, 19200)

# set the chunk size to transfer. Through testing, the Portenta can only receive chunks of 256 bytes
chunk_size = (1 << 8)

img = sensor.snapshot()         # Take a picture and return the image.

# compressed image *should* work but through testing the image was consistently corrupted
#img = sensor.snapshot().compress()         # Take a picture and compress the image.

# pack the data about the image we are going to transmit
data = struct.pack("<IIIII", sensor.width(), sensor.height(), sensor.get_pixformat(), img.size(), chunk_size)
uart.write(data)

# get the raw bytes of data for the image
img_data = img.bytearray()

# get the number of chunks we need
num_chunks = img.size()/chunk_size

# the image doesn't neatly fit within our chunk size, we need to receive an additional chunk
if int(num_chunks) != num_chunks:
    num_chunks = int(num_chunks+1)

chunk_pos = 0

# loop from 0 to our image size, incrementing by chunk size
for i in range(0, num_chunks):
    # set the starting point of our chunk
    chunk_pos = i*chunk_size

    # get the chunk of bytes between chunk_pos and chunk_pos+chunk_size
    chunk = img_data[chunk_pos:chunk_pos+chunk_size]

    print("Writing chunk {0} of {1} - {2} bytes - starting at {3}".format(i+1, num_chunks, len(chunk), chunk_pos))

    uart.write(chunk)
