
'''

Before running this test , make sure a file called [my_email_auth] exists in the root directory 
in the file incluse the following variables

		- GMAIL_EMAIL - An email address you own that will send the email
		- GMAIL_APP_PASSWORD - Gmail app password (NOT THE NORMAL PASSWORD)
		- TEST_RECEIVER_EMAIL - A different  email address you own that will receive the test emauk

  '''


import unittest
from unittest import TestCase

from tests.data_for_tests import *

from wholemail import BasicCodeVerificationEmailTemplate , GmailSender , BasicEmailVerificationEmailTemplate
from my_email_auth import GMAIL_EMAIL , GMAIL_APP_PASSWORD , TEST_RECIPIENT

test_sender = GmailSender(GMAIL_EMAIL , GMAIL_APP_PASSWORD )
template_style = 2
class Test_BasicEmailVerificationEmailTemplate(TestCase):

	def test_SimpleStyle(self):
		'''
		Just sending an email to see if everything works and looks as ot should
		'''

		sender = test_sender
		test_email_template = BasicEmailVerificationEmailTemplate(

					recipient_name = "JohnDoe" , 
					company_name = "WholemailApp",
					email_verification_link = "httpsverificationlink.com",
					company_address = "Mars",
					customer_support_link = "support",
					company_phone_number = "+123456",
					company_website_link = "wholemailwebsite",
					template_style = template_style,
					 )
		html  = test_email_template.content
		plain_message = test_email_template.plain_text_content
		subject = "Testing wholemail email verification email template"
		result = sender.SendHTMLEmail( TEST_RECIPIENT , subject , html , plain_message  )
		self.assertTrue(result)
		print("Email sent to {} for testing purposes".format(TEST_RECIPIENT))

class Test_BasicCodeVerificationEmailTemplate(TestCase):
	def test_SimpleStyle(self):
		'''
		Just sending an email to see if everything works and looks as ot should ,
		check your address to see the result
		'''

		sender = test_sender
		test_email_template = BasicCodeVerificationEmailTemplate(
					code = "12345",
					recipient_name = "JohnDoe" , 
					company_name = "WholemailApp",
					company_address = "Mars",
					customer_support_link = "support",
					company_phone_number = "+123456",
					company_website_link = "wholemailwebsite",
					template_style = template_style,
					)
		html  = test_email_template.content
		plain_message = test_email_template.plain_text_content
		subject = "Testing wholemail verification code email simple style"
		result = sender.SendHTMLEmail( TEST_RECIPIENT , subject , html , plain_message  )
		self.assertTrue(result)
		print("Email sent to {} for testing purposes".format(TEST_RECIPIENT))

