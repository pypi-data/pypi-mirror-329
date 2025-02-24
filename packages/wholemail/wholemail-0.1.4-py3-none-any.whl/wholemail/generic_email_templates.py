

import os

current_file = __file__
current_dir ,file_name = os.path.split(current_file)
html_boilerplate_dir = os.path.join(current_dir, "html_boilerplates")

# a hotfix function to create the html files
load_html_file = lambda file:os.path.join(html_boilerplate_dir , file)





