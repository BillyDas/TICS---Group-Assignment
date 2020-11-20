import time, struct, image
from pyb import UART

# Set UART pins and baudrate
uart = UART(1, 19200)

while not uart.any():
    time.sleep(10)    # wait for a message

data = uart.read()

# unpack the received data
w, h, pixformat, img_size, chunk_size = struct.unpack("<IIIII", data)

print("Received data. W: {0}, H:{1}, Format:{2}, size:{3}, chunk size:{4}".format(w, h, pixformat, img_size, chunk_size))

#image_bytes = bytearray()
img = image.Image(w, h, pixformat, copy_to_fb=True)


num_chunks = img_size/chunk_size
rounded_chunks = False
# the image doesn't neatly fit, we need to receive an additional chunk
if int(num_chunks) != num_chunks:
    num_chunks = int(num_chunks)
    rounded_chunks = True
chunk_pos = 0
# loop from 0 to our image size, incrementing by chunk size
for i in range(0, num_chunks):
    # wait for a new message
    while not uart.any():
        time.sleep(100)

    # read the chunk in
    chunk = uart.read()


    # calculate the starting position for the next chunk
    chunk_pos = i*chunk_size

    print("Reading chunk {0} of {1} - {2} bytes - starting at {3}".format(i+1, num_chunks, len(chunk), chunk_pos))

    # update our image object with the new bytes
    img.bytearray()[chunk_pos:chunk_pos+len(chunk)] = chunk

# save the image to the SD card
img.save('test.bmp')