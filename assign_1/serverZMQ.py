import zmq
import time
import os
import sys


def chunker(seq, size):
    return (seq[pos:pos + size] for pos in range(0, len(seq), size))


if len(sys.argv) != 3:
    print("You must provide two argument: FileReadSize and SocketWriteSize (in kB)")
    sys.exit(1)

fileRead = int(sys.argv[1]) * 1024
writeSize = int(sys.argv[2]) * 1024
print(f"Server configured to read file in chunks of {fileRead} bytes")
print(f"Server configured to write to the socket chunks of {writeSize} bytes")
# create server with a Reply-model socket type and connect to it
context = zmq.Context()
socket = context.socket(zmq.REP)
serverAddr = "tcp://*:43456"
socket.bind(serverAddr)
print(f"Server listening on: {serverAddr}\n")

# block on recv to get a client request
filePrefix = "/Users/amaltar2/Master/Grad_OS"
while True:
    totalReads = 0
    totalWrites = 0
    # Receive file name from the client (and decode it to unicode)
    fileName = socket.recv().decode("utf-8")
    fullPath = f"{filePrefix}/{fileName}"
    print(f"Received request to open file: {fileName}")
    # first, send file size to the client
    totalFileSize = os.stat(fullPath).st_size
    socket.send_string(f"{totalFileSize}")

    # now, send the file itself in chunks
    # one recv for each send (!!!)
    with open(fullPath, "rb") as fOjb:
        # client requesting data
        clientMsg = socket.recv().decode("utf-8")
        while True:
            if clientMsg == "EOF":
                print("Client confirms the file has been transferred")
                socket.send_string("OK")
                break
            # same size for read and write
            if fileRead == writeSize:
                data = fOjb.read(fileRead)
                totalReads += 1
                socket.send(data)
                totalWrites += 1
                clientMsg = socket.recv().decode("utf-8")
            # read once for every few writes
            elif fileRead > writeSize:
                data = fOjb.read(fileRead)
                totalReads += 1
                for thisChunk in chunker(data, writeSize):
                    socket.send(thisChunk)
                    totalWrites += 1
                    clientMsg = socket.recv().decode("utf-8")
            # read few times for every write
            else:
                data = b""
                while len(data) < writeSize:
                    thisData = fOjb.read(fileRead)
                    if not thisData:
                        break
                    data = data + thisData
                    totalReads += 1
                socket.send(data)
                totalWrites += 1
                clientMsg = socket.recv().decode("utf-8")

    print(f"File {fileName} sent with {totalReads} reads and {totalWrites} write operations\n")