# # syntaxmatrix/__init__.py
from .synta_mui import SyntaxMUI

_app_instance = SyntaxMUI()

run = _app_instance.run
text_input = _app_instance.text_input
button = _app_instance.button
file_uploader = _app_instance.file_uploader
set_ui_mode = _app_instance.set_ui_mode
set_theme = _app_instance.set_theme
enable_theme_toggle = _app_instance.enable_theme_toggle
get_text_input_value = _app_instance.get_text_input_value
clear_text_input_value = _app_instance.clear_text_input_value
get_file_upload_value = _app_instance.get_file_upload_value
get_chat_history = _app_instance.get_chat_history
set_chat_history = _app_instance.set_chat_history
clear_chat_history = _app_instance.clear_chat_history
set_project_title = _app_instance.set_project_title
write = _app_instance.write
