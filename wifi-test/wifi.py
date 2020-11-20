# WiFi Connect Example
import network, usocket, time

SSID='' # Network SSID
KEY=''  # Network key
PORT = 80 # web server port
HOST = "www.google.com" # web server address


# Init wlan module and connect to network
print("Trying to connect... (may take a while)...")
wlan = network.WLAN(network.STA_IF)
wlan.active(True)

wlan.connect(SSID,KEY)

#make sure to wait for connection
while not wlan.isconnected():
    time.sleep(100) # wait a little

# We should have a valid IP now via DHCP
print(wlan.ifconfig())

# Get addr info via DNS
addr = usocket.getaddrinfo(HOST, PORT)[0][4]
print(addr)

# Create a new socket and connect to addr
client = usocket.socket(usocket.AF_INET, usocket.SOCK_STREAM)
client.connect(addr)

# Set timeout
client.settimeout(3.0)

# Send HTTP request and recv response
# note that any standard HTTP request will function - GET, POST, PUT, DELETE, etc.
client.send("GET / HTTP/1.1\r\nHost: %s\r\n\r\n"%(HOST))
print(client.recv(1024))

# Close socket
client.close()
