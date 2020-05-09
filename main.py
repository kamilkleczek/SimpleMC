from imap import IMAP
from smtp import SMTP
from Email import Email

# Reading emails

imap = IMAP(debug=True)
imap.login('imaptestask@gmail.com', '***')
imap.select('INBOX')
imap.search('ALL')
email = imap.fetch_email('7')


# Sending emails

smtp = SMTP(debug=True)
smtp.login('imaptestask@gmail.com', '***')

send_from = 'imaptestask@gmail.com'
send_to = 'i.maptestas.k@gmail.com'
send_cc = 'imaptesta.s.k@gmail.com'
send_bcc = 'imapt.e.s.t.a.s.k@gmail.com'
subject = 'This is test email'
body = 'The body is here' \
       '\nand also new line'
email = Email()
email.create(send_from=send_from, send_to=send_to, send_cc=send_cc, send_bcc=send_bcc, subject=subject, body=body)

smtp.send_email(email)