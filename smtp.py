from socket import *
import base64
import ssl
import re


class Commands(enumerate):
    LOGIN = 'AUTH LOGIN'
    MAILFROM = 'MAIL FROM:'
    RCPTO = 'RCPT TO:'
    DATA = 'DATA'
    QUIT = 'QUIT'
    HELO = 'EHLO localhost'


class Responses(enumerate):
    AUTH = '334'
    USER = '334'
    PASSWD = '235'
    MAILFROM = '250'
    RCPTO = '250'
    DATA = '354'
    SEND = '250'
    QUIT = '221'


class SMTP():

    def __init__(self, debug=False):
        self._server = 'smtp.gmail.com'
        self._port = 465
        self.socket = None
        self.debug = debug
        self._connect()

    def login(self, user, passwd=None):
        try:
            response = self._msg_send(Commands.LOGIN)
            self._fetch_response_ok(Responses.AUTH, response)

            user = base64.b64encode(user.encode()).decode()
            response = self._msg_send(user)
            self._fetch_response_ok(Responses.USER, response)

            passwd = base64.b64encode(passwd.encode()).decode()
            response = self._msg_send(passwd)
            self._fetch_response_ok(Responses.PASSWD, response)
        except Exception as error:
            print(repr(error))

    def send_email(self, email):
        try:
            send_list = []
            if email.send_to:
                send_list.append(email.send_to)
            if email.send_cc:
                send_list.append(email.send_cc)
            if email.send_bcc:
                send_list.append(email.send_bcc)

            mail_from = '<{}>'.format(email.send_from)
            response = self._msg_send(Commands.MAILFROM, mail_from)
            self._fetch_response_ok(Responses.MAILFROM, response)

            for mail in send_list:
                mail_to = '<{}>'.format(mail)
                response = self._msg_send(Commands.RCPTO, mail_to)
                self._fetch_response_ok(Responses.RCPTO, response)

            response = self._msg_send(Commands.DATA)
            self._fetch_response_ok(Responses.DATA, response)

            email_body = 'From:<{0}>\n' \
                         'To:<{1}>\n' \
                         'CC:<{2}>\n' \
                         'Subject:{3}\n' \
                         '{4}'.format(email.send_from, email.send_to, email.send_cc, email.subject, email.body)
            response = self._msg_send(email_body, recv=False)

            response = self._msg_send('\r\n.\r\n')
            self._fetch_response_ok(Responses.SEND, response)

            response = self._msg_send(Commands.QUIT)
            self._fetch_response_ok(Responses.QUIT, response)
        except Exception as error:
            print(repr(error))

    def _connect(self):
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.socket = ssl.wrap_socket(self.socket, ssl_version=ssl.PROTOCOL_SSLv23)
        self.socket.connect((self._server, self._port))
        recv = self.socket.recv(4024).decode()
        if self.debug:
            print('Server: {}'.format(recv))

        self._msg_send(Commands.HELO, isbase64=False)

    def _fetch_response_ok(self, ok_response, response):
        pattern = re.compile(r'{0}'.format(ok_response))
        result = re.findall(pattern, response)
        if not result:
            raise Exception('Invalid response: {} in {}'.format(pattern, response));

    def _msg_send(self, msg_type, msg_body='', isbase64=True, recv=True):
        msg = '{0} {1}\r\n'.format(msg_type, msg_body)
        msg = msg.encode()
        self.socket.send(msg)
        msg = msg.decode()
        if self.debug:
            print('\n\nClient: {}'.format(msg))

        if recv:
            recv = self.socket.recv(2000).decode()
            print('Server: {}'.format(recv))
            return recv
