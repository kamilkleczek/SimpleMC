import re


class Email:
    def __init__(self):
        self.send_from = ""
        self.send_to = ""
        self.send_cc = ""
        self.send_bcc = ""
        self.subject = ""
        self.date = ""
        self.body = ""

    def create(self, send_from, send_to, send_cc, send_bcc, subject, body):
        self.send_from = send_from
        self.send_to = send_to
        self.send_cc = send_cc
        self.send_bcc = send_bcc
        self.subject = subject
        self.body = body
        return self

    def receive(self, response_header, response_body):
        pattern = re.compile(r'From: <(.*?)>')
        match = re.search(pattern, response_header)
        if match and match.group(1):
            self.send_from = match.group(1)

        pattern = re.compile(r'Cc: <(.*?)>')
        match = re.search(pattern, response_header)
        if match and match.group(1):
            self.cc = match.group(1)

        pattern = re.compile(r'Subject: (.*)')
        match = re.search(pattern, response_header)
        if match and match.group(1):
            self.subject = match.group(1)

        pattern = re.compile(r'Date: (.*)')
        match = re.search(pattern, response_header)
        if match and match.group(1):
            self.date = match.group(1)

        pattern = re.compile(r'BODY\[1\] \{\d+\}(.*)\)', re.DOTALL)
        match = re.search(pattern, response_body)
        if match and match.group(1):
            self.body = match.group(1)
