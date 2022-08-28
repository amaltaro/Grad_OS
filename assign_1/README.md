# Assignment 1
Create a client/server program (actually one script for each) that uses ZMQ to send a file over localhost socket.
It uses a Request-Reply model, thus each request generates a reply.

We will measure communication with different read and write rates, and with 3 different file sizes.

To create 3 files with a specific size, one can:

```commandline
dd if=/dev/urandom of=100k.txt bs=100*1024 count=1
dd if=/dev/urandom of=1MB.txt bs=1*1024*1024 count=1
dd if=/dev/urandom of=100MB.txt bs=100*1024*1024 count=1
```

Server is executed with:
```commandline
python serverZMQ.py FileReadSize SocketWriteSize
```
where:
* `FileReadSize`: amount of kB to read (chunk size of the file to be read from disk)
* `SocketWriteSize`: amount of kB written to the socket in each operation.

Client is executed with:
```commandline
python clientZMQ.py FileReadSize SocketWriteSize
```
where the arguments have the same meaning as of in the server, but here they are simply used to provide a json dump of the metrics.


## Measurements
For each of the 3 files, we transfer it 10 times from the server to the client and measure tha elapsed time on the client.
We are varying the read rate and the write rate to see the impact to transfer such files.