




import os
from os.path import join 

current_file = __file__
base_dir ,file_name = os.path.split(current_file)
boilerplates_dir = join(base_dir , "html_boilerplates")

email_verification_templates_base_dir = join(boilerplates_dir , "email_verification")
verification_code_templates_base_dir = join(boilerplates_dir , "verification_code")


EMAIL_VERIFICATION_TEMPLATES = {
		1:join( email_verification_templates_base_dir , "1.html" ),
		2:join( email_verification_templates_base_dir , "2.html" ),
		3:join( email_verification_templates_base_dir , "3.html" ),

}

VERIFICATION_CODE_TEMPLATES = {
		1:join( verification_code_templates_base_dir, "1.html" ),
		2:join( verification_code_templates_base_dir, "2.html" ),
		3:join( verification_code_templates_base_dir, "3.html" ),

	
}






