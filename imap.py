from socket import *
from Email import Email
import ssl
import re


class Commands(enumerate):
    LOGIN = 'LOGIN'
    SELECT = 'SELECT'
    SEARCH = 'SEARCH'
    FETCH = 'FETCH'


class IMAP():

    def __init__(self, debug=False):
        self._server = 'imap.gmail.com'
        self._port = 993
        self.socket = None
        self.debug = debug
        self.msg_id = 0
        self._connect()

    def login(self, user, passwd=None):
        response = self._msg_send(Commands.LOGIN, '{0} {1}'.format(user, passwd))
        try:
            self._fetch_response_ok(self._get_msg_id(), response)
        except Exception as error:
            print(repr(error))

    def select(self, folder):
        response = self._msg_send(Commands.SELECT, folder)
        try:
            self._fetch_response_ok(self._get_msg_id(), response)
        except Exception as error:
            print(repr(error))

    def search(self, criteria):
        response = self._msg_send(Commands.SEARCH, criteria)
        try:
            self._fetch_response_ok(self._get_msg_id(), response)
        except Exception as error:
            print(repr(error))

    def fetch_email(self, email_id):
        email_headers = "(FLAGS BODY[HEADER.FIELDS (DATE FROM SUBJECT CC BCC FWD)])"
        formatted_command = email_id + " " + email_headers
        response_header = self._msg_send(Commands.FETCH, formatted_command)

        email_body = "(BODY[1])"
        formatted_command = email_id + " " + email_body
        response_body = self._msg_send(Commands.FETCH, formatted_command)

        email = Email()
        email.receive(response_header, response_body)
        return email

    def _fetch_response_ok(self, msg_id, response):
        pattern = re.compile(r'{0} OK'.format(msg_id))
        result = re.findall(pattern, response)
        if not result:
            raise Exception('Invalid response: {} in {}'.format(pattern, response));

    def _msg_send(self, msg_type, msg_body):
        msg = '{0} {1} {2}\r\n'.format(self._gen_msg_id(), msg_type, msg_body)
        msg = msg.encode()
        self.socket.send(msg)
        msg = msg.decode()
        if self.debug:
            print('\n\nClient: {}'.format(msg))

        # response:
        # if msg is not completed (did not returned OK Success), query again
        pattern = re.compile(r'Success|BAD')
        response = ''

        while True:
            recv = self.socket.recv(2000)
            response = response + recv.decode()
            if self.debug:
                print('Server: {}'.format(recv))

            result = re.findall(pattern, response)
            if result:
                break

        return response

    def _gen_msg_id(self):
        self.msg_id += 1
        return 'A{0:04}'.format(self.msg_id)

    def _get_msg_id(self):
        return 'A{0:04}'.format(self.msg_id)

    def _connect(self):
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.socket = ssl.wrap_socket(self.socket, ssl_version=ssl.PROTOCOL_SSLv23)
        self.socket.connect((self._server, self._port))
        recv = self.socket.recv(4024).decode()
        if self.debug:
            print('Server: {}'.format(recv))
