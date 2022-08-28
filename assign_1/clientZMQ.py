import zmq
import sys
import time

# validate input arguments
if len(sys.argv) != 3:
    print("You must provide two arguments: FileReadSize and SocketWriteSize (in kB)")
    sys.exit(1)

fileRead = sys.argv[1]
socketWrite = sys.argv[2]

# create client with a Request-model socket type and connect to it
serverAddr = "tcp://localhost:43456"
context = zmq.Context()
print(f"Connecting to server on address: {serverAddr}")
socket = context.socket(zmq.REQ)
socket.connect(serverAddr)

# send a request and wait for the reply
#  Do 10 requests, waiting each time for a response
results = {"fileReadkB": fileRead, "socketWritekB": socketWrite}
for fileName in ["100k.txt", "1MB.txt", "100MB.txt"]:
    results.setdefault(fileName, [])
    print(f"Going to request file name: {fileName}")
    for _i in range(1, 11):
        totalBytes = 0
        totalChunks = 0
        socket.send_string(fileName)
        #  Get expected file size
        expectedSize = int(socket.recv())
        print(f"Client is expected to receive a file with size: {expectedSize} bytes")
        iniTime = time.time()
        while True:
            # request data to the server
            socket.send_string("OK")
            message = socket.recv()
            totalBytes += len(message)
            totalChunks += 1
            if totalBytes == expectedSize:
                break
        # confirm file has been fully received
        socket.send_string("EOF")
        endTime = time.time()
        elapsedT = format(endTime - iniTime, ".3f")
        results[fileName].append(elapsedT)

        junk = socket.recv()
        print(f"Received {totalBytes} bytes in a total of {totalChunks} chunks\n")
print(f"Final results:\n{results}")

