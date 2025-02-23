import os 
import jinja2
from bs4 import BeautifulSoup

from . import html_boilerplates

TEMPLATE_STYLES_AVAILABLE= [1,2]

def strip_html_tags(html:str)-> str:
	'''
	Removes the tags from html content and return the plain text in between the tags .
	'''
	soup = BeautifulSoup(html , "html.parser")
	text  = soup.get_text()
	return text



class EmailTemplate:
	"""
	This class represents the HTML email you wish to send 
	"""

	name = "Template"
	def __init__(self , html, context = {} , name = "Template"):
		'''
		Parameters
		----------
		html:str
			The html code to send in the email 
		context:dict 
			Context information to be inserted into the html code eg. { 'name' : 'John' }
		name:str
			The name you wish to give to the template

		Methods
		-------
		Edit(key:str , value:str)
			Edit a variable in the context and update the html_content

			Parameters
			----------
			key:str
				The name of the value to be updated in the html code
			value:str
				The value you wish to insert into the html code
		UpdateContent()
			Update the data in the content attribute 
			Use this when editing/updating the context 
		'''
		self.name = name 
		self.context = context		 
		self.html = html # will not change ever
		self.content = ""
		self.plain_text_content = ""
		self.jinja_environment = jinja2.Environment()
		self.UpdateContent()

	def UpdateContent(self) -> None:
		'''
		Update the data in the content attribute 
		Use this when editing/updating the context 
		'''
		template = self.jinja_environment.from_string(self.html)
		content =  template.render(**self.context)
		self.content =content
		self.plain_text_content = strip_html_tags(content)

	def Edit(self, key:str , value:str):
		'''
		Edit a variable in the context and update the html_content

		Parameters
		----------
		key:str
			The name of the value to be updated in the html code
		value:str
			The value you wish to insert into the html code
	
		'''
		if not key in self.context:
			raise KeyError("The key provided is not in the context : {}".format(self.context))
		self.context[key] = value
		self.UpdateContent()

 

class FileEmailTemplate(EmailTemplate) :
	'''
	An EmailTemplate class where html content is loaded from a file 

	Parameters
	----------
	file:str
		The path to the file with the html code  
	context:dict 
		Context information to be inserted into the html code eg. { 'name' : 'John' }
	name:str
		The name you wish to give to the template
	'''
	def __init__(self ,file:str , context:str , name = "file-email-template" ):
		self.context = context
		self.file  =file
		if not os.path.isfile(file):
			raise FileNotFoundError("Please provide the file path ")
		with open(file , "r", encoding  ="utf-8") as f:
			html = f.read()

		EmailTemplate.__init__(self , html , context , name = name)

 


class BasicCodeVerificationEmailTemplate(FileEmailTemplate):
	'''
	A pre-set template for sending authentication codes to a users email 
	'''

	def __init__(self ,
		code ,
		recipient_name,
		company_name = "", 
		company_address = "",
		customer_support_link = "" ,
		company_phone_number = "",
		company_website_link = "",
		template_style = 1,
		name = 'code-verification',

					 ):
		# get the html template
		html_file = html_boilerplates.VERIFICATION_CODE_TEMPLATES[template_style]
		context = locals()
		context.pop("self")
		super().__init__(html_file , context , name = name)

class BasicEmailVerificationEmailTemplate(FileEmailTemplate):
	'''
	A pre-set template for sending authentication links to a users email 
	'''

	def __init__(self ,
					recipient_name , 
					company_name, 
					email_verification_link , 
					company_address = "",
					customer_support_link = "" ,
					company_phone_number = "",
					company_website_link = "",
					template_style = 1,
					name = "Simple-email-verification-template",
					 ):
		# get the html template
		html_file = html_boilerplates.EMAIL_VERIFICATION_TEMPLATES[template_style]
		context = locals()
		context.pop("self")
		super().__init__(html_file ,context , name = name )
