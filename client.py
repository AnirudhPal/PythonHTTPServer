# Import Standard Libs
import socket		# Used for Socket Programming
import sys			# Used to get Command Line Arguments

# Config Vars
VERBOSE = False  				# Controls Print Statements
HOST = 'xinu01.cs.purdue.edu'	# Default Host
DPORT = 2200					# Default Port
CLARGS = True					# Force use CL Arquments
FILE = "index.html"				# Default File

# Argument Check
if not len(sys.argv) == 4:
	# Usage
	print("Usage:\npython client.py [sever_host] [server_port] [filename]\n")
	print("sever_host: Set the address of server to test.")
	print("server_port: Set the port of server to test.")
	print("filename: Set the filename to be downloaded.\n")
	print("All arguments are required.")
	# Exit
	sys.exit()

# Reassing File
if CLARGS:
	FILE = sys.argv[3]

# Make Socket Object
socketObj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to Server
try:
	if CLARGS:
		socketObj.connect((sys.argv[1], int(sys.argv[2])))
	else:
		socketObj.connect((HOST, DPORT))
except socket.error as msg:
	if VERBOSE:
    		print(str(msg))

# Process Request
def sendHTTP(server, filename):
	# Build and Send Request
	request = "GET /" + filename +" HTTP/1.1\r\n\r\n"
	server.send(request)
	if VERBOSE:
		print("Request: " + request + '\n')

	# Parse Resonse
	result = server.recv(1024)
	if VERBOSE:
		print("Response: " + result + '\n')
	if result.find("HTTP/1.1 200 Document follows") == -1:
		if VERBOSE:
			print("Bad Response\n")
		return

	# Parse File
	if VERBOSE:
		print("Getting File")
	file = open("Download/" + filename, "wb")
	file.write(result[(result.find("\r\n\r\n") + len("\r\n\r\n")):])
	buf = server.recv(1024)
	while buf:
		file.write(buf)
		buf = server.recv(1024)
	file.close()
	if VERBOSE:
		print("Got File")\

# Send Request
sendHTTP(socketObj, FILE)
