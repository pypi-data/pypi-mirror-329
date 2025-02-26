
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.message import EmailMessage




class EmailSender:
	'''
	a base class that facilitates sending of emails 

	Attributes
	-----------
	email:str
		Email address to use when sending emails
	password:str
		Password to the email
	'''

	def __init__(self , email , password):
		'''
		Parameters
		----------
		email:str
			Email address to use when sending emails
		password:str
			Password to the email
		'''

		self.email = email 
		self.password = password

 
	 

class GmailSender(EmailSender):
	'''
	This class is for sending gmail emails 

	Attributes
	-----------
	email:str
		Email address to use when sending emails
	password:str
		The Gmail app Password to the gmail account

	Methods
	-------
	SendHTMLEmail(email:str , password:str)
		Sends an html email to the provided recipient
		
		Parameters
		----------
		recipients:str
			email address to receive the email .
		subject:str
			The subject of the email to be sent .
		html:
			The html code to send 
		plain_message:str
			Alternative message in text form (To be shown if the HTML doesn't render)


		Returns
		-------
		bool
			True if the email is sent successfully ,else False

	'''

	def __init__(self , email:str , password:str):
		'''
		email:str
			Email address to use when sending emails
		password:str
			The Gmail app Password to the gmail account
		'''
		EmailSender.__init__(self , email , password)


	def SendHTMLEmail(self ,recipient:str, subject:str , html:str, plain_message:str = "" ) -> bool:
		'''
		Sends an html email to the provided recipient
		
		Parameters
		----------
		recipients:str
			email address to receive the email .
		subject:str
			The subject of the email to be sent .
		html:
			The html code to send 
		plain_message:str
			Alternative message in text form (To be shown if the HTML doesn't render)


		Returns
		-------
		bool
			True if the email is sent successfully ,else False

		'''
		print("Preparing to send HTML message to {} from sender {}. [PASSWORD = {} ]".format(recipient, self.email , self.password[:3] + ("*"*(len(self.password)-3))))
		port = 465  # For SSL
		# Create a secure SSL context
		# strip the tags from the html if the plain_message is not present
		message = MIMEMultipart("alternative")
		message["Subject"] = subject
		message["From"] = self.email
		message["To"] = recipient
		# load the html and plain messages as  MIMEText objects
		part1 = MIMEText(plain_message, "plain")
		part2 = MIMEText(html, "html")
		# Add HTML/plain-text parts to MIMEMultipart message
		# The email client will try to render the last part first
		message.attach(part1)
		message.attach(part2)
		context = ssl.create_default_context()
		with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
			try:
				server.login(self.email ,self.password)
				server.sendmail(self.email , recipient ,message.as_string())
				return True
			except Exception as e:
				raise
		return False


	def SendTextEmail(self , recipient:str, subject:str , message:str ) -> bool:
		'''
		Send an text based email to the provided recipients

		Parameters
		----------
		recipient:str
			The email address to receive the email .
		subject:str
			The subject of the email to be sent .
		message:
			The message to send 

		Returns
		-------
		bool
			Whether the email has been sent or not

		'''

		msg = EmailMessage()
		msg['Subject'] = subject
		msg['From'] =self.email
		msg['To'] = recipient
		msg.set_content(message)
		print("Preparing to send a text based message to {} from sender {}. [PASSWORD = {} ]".format(recipient, self.email , self.password[:3] + ("*"*(len(self.password)-3))))
		port = 465  # For SSL
		# Create a secure SSL context
		context = ssl.create_default_context()
		with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
			try:
				server.login(self.email ,self.password)
				server.send_message(msg)
				return True
			except Exception as e:
				raise
		return False
