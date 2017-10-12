import socket
import threading
import queue


class ClientCommand:
    """ A command to the client thread.
        Each command type has it's associated data:

        CONNECT:    (host, port) tuple
        SEND:       Data byte array
        RECEIVE:    None
        CLOSE:      None
    """
    CONNECT, SEND, RECEIVE, CLOSE = range(4)

    def __init__(self, type, data=None):
        self.type = type
        self.data = data


class ClientReply(object):
    """ A reply from the client thread.
        Each reply has it's associated data:

        ERROR:      The error string.
        SUCCESS:    Depends on the command, For RECEIVE it's the received
                    data string, for others, None.
    """
    ERROR, SUCCESS = range(2)

    def __init__(self, type, data=None):
        self.type = type
        self.data = data


class SocketClientThread(threading.Thread):
    """ Implements the threading.Thread interface (start, join, etc..) and
        can be controlled by the cmd_q Queue attribute. Replies are placed
        in the reply_q Queue attribute.
    """
    def __init__(self, cmd_q=None, reply_q=None):
        super(SocketClientThread, self).__init__()
        self.cmd_q = cmd_q or queue.Queue()
        self.reply_q = reply_q or queue.Queue()
        self.alive = threading.Event()
        self.alive.set()
        self.socket = None

        self.handlers = {
            ClientCommand.CONNECT: self._handle_CONNECT,
            ClientCommand.CLOSE:   self._handle_CLOSE,
            ClientCommand.SEND:    self._handle_SEND,
            ClientCommand.RECEIVE: self._handle_RECEIVE,
        }

    def run(self):
        while self.alive.isSet():
            try:
                # Queue.get with timeout to allow checking self.alive
                cmd = self.cmd_q.get(True, 0.1)
                self.handlers[cmd.type](cmd)
            except queue.Empty as e:
                continue

    def join(self, timeout=None):
        self.alive.clear()
        threading.Thread.join(self, timeout)

    def _handle_CONNECT(self, cmd):
        try:
            self.socket = socket.socket(
                socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(5)
            self.socket.connect((cmd.data[0], cmd.data[1]))
            self.reply_q.put(self._success_reply())
        except IOError as e:
            self.reply_q.put(self._error_reply(str(e)))

    def _handle_CLOSE(self, cmd):
        self.socket.shutdown(socket.SHUT_RDWR)
        self.socket.close()
        reply = ClientReply(ClientReply.SUCCESS)
        self.reply_q.put(reply)

    def _handle_SEND(self, cmd):
        try:
            self.socket.sendall(cmd.data)
            self.reply_q.put(self._success_reply())
        except IOError as e:
            self.reply_q.put(self._error_reply(str(e)))

    def _handle_RECEIVE(self, cmd):
        try:
            header_data = self._recv_n_bytes(4)
            if len(header_data) == 4:
                msg_len = ((header_data[2] & 0xFF) << 8 | (header_data[3] & 0xFF) << 0)
                data = self._recv_n_bytes(msg_len - 4)
                payload = header_data + data
                if len(payload) == msg_len:
                    self.reply_q.put(self._success_reply(payload))
                    return
            self.reply_q.put(self._error_reply('Socket Closed Prematuerly'))
        except IOError as e:
            self.reply_q.put(self._error_reply(str(e)))

    def _recv_n_bytes(self, n):
        """ Convenience method for receiving excactly n bytes from
            self.socket (assuming it's open and connected).
        """
        data = bytearray()
        while len(data) < n:
            chunk = self.socket.recv(n - len(data))
            if chunk == b'':
                break
            data += chunk
        return data

    def _error_reply(self, errstr):
        return ClientReply(ClientReply.ERROR, errstr)

    def _success_reply(self, data=None):
        return ClientReply(ClientReply.SUCCESS, data)
