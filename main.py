from imap import IMAP
from smtp import SMTP
from Email import Email

# Reading emails

imap = IMAP(debug=True)
imap.login('***', '***')
imap.select('INBOX')
imap.search('ALL')
email = imap.fetch_email('4')

print(email.send_from)
print(email.subject)
print(email.body)

# Sending emails

smtp = SMTP(debug=True)
smtp.login('***', '***')
send_from = 'imaptestask@gmail.com'
send_to = 'kkleczek@gmail.com'
subject = 'This is test email'
body = 'The body is here' \
       '\nand also new line'
email = Email()
email.create(send_from, send_to, subject, body)
smtp.send_email(email)
