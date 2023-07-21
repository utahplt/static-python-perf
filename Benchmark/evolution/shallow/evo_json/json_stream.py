import json

PACKET_SIZE = 1024
MAX_BUFFER = 1024 ** 2


class JSONStream(object):
    """ A class for sending and recieving JSON
    """

    def __init__(self, stream_socket):
        """
        :param stream_socket: the file to read and write from
        :return: None
        """
        self.stream_socket = stream_socket
        self.remainder = ""
        self.decoder = json.JSONDecoder()

    def receive_py_json(self):
        """
        Receive the next JSON as PyJSON or EndOfStream object
        :return: next PyJSON
        :rtype: PyJSON or EndOfStream
        """
        while len(self.remainder) < MAX_BUFFER:
            recieved_data = self.stream_socket.recv(PACKET_SIZE).decode("utf-8")
            if len(recieved_data) == 0:
                return EndOfStream()
            self.remainder += recieved_data.strip()
            try:
                py_json, index = self.decoder.raw_decode(self.remainder)
            except ValueError as e:
                pass # need more data (can't detect bad data)
            else:
                self.remainder = self.remainder[index:]
                return py_json

    def send_py_json(self, py_json):
        """
        Send the given py_json to the stream as JSON
        :param py_json: the PyJSON to be sent
        :type py_json: PyJSON
        :return: None
        """
        json_str = json.dumps(py_json)
        self.stream_socket.sendall(bytes(json_str + '\n', 'utf8'))


class EndOfStream:
    """
    Indicates the end of a stream
    """
    pass