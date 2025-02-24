SyntaxMatrix UI Framework

SyntaxMatrix is a lightweight, Pythonic UI framework designed to help developers rapidly build interactive front-end interfaces for AI applications, especially Retrieval Augmented Generation (RAG) projects and more - without the need to learn or manage any web framework directly. SyntaxMatrix simplifies UI creation and also adds unique features such as dynamic theme toggling, multiple UI display modes, admin panel, and some coming up features like: a collapsible sidebar, and file upload capabilities in the admin panel.
Features
•	Rapid UI Creation: Easily create interactive widgets such as text inputs, buttons, and file uploaders with simple function calls.
•	Dynamic Theme Toggle: End users can switch between light and dark themes on the fly using a toggle link.
•	Multiple UI Modes: Choose among three distinct display modes:
o	Default Mode: Messages are rendered as full-width blocks.
o	Bubble Mode: Messages appear as rounded bubbles.
o	Card Mode: Messages are displayed in a card-style format with.
•	State Management: Chat history, file uploads (coming next), and widget states are automatically managed sessions, all via public APIs.
•	Admin Panel: An integrated admin panel lets developers manage and perform CRUD operations on the menu items just by clicking buttons.
Installation
•	In the terminal of your venv, run pip install syntaxmatrix
•	In your application: import syntaxmatrix as smx
Next Features (coming up)
•	Collapsible Sidebar:
A responsive sidebar that is collapsed by default and can be expanded via a hamburger toggle. The sidebar supports additional widgets (e.g., text inputs and buttons) that can be used for navigation or other interactive features.
•	File Upload in the Admin Panel:
This feature lets developers upload and manage files into their projects. File uploads are processed and stored - ready to be used as context for AI applications.



API Reference
Public API Functions
•	run()
Launches the UI server and opens the application in the default web browser.
•	text_input(key, label, placeholder="")
Registers a text input widget in the main UI.
•	button(key, label, callback=None)
Registers a button widget in the main UI. The callback is executed when the button is 
•	set_widget_position(position)
Sets the position of the widget area ("top" or "bottom").
•	set_ui_mode(mode)
Sets the chat UI mode. Options: "default", "bubble", "card".
•	set_theme(theme)
Sets the UI theme. Options: "light", "dark", or a custom dictionary.
•	enable_theme_toggle()
Enables a dynamic theme toggle link in the navigation bar.
•	get_text_input_value(key, default="")
Retrieves the current value of a text input widget.
•	clear_text_input_value(key)
Clears the value of a text input widget.
•	get_chat_history() / set_chat_history(history) / clear_chat_history()
Manage the chat history stored in the session.
•	sidebar_text_input(key, label, placeholder="")
Registers a text input widget in the sidebar.
•	sidebar_button(key, label, callback=None)
Registers a button widget in the sidebar.
•	write(content)
Appends content to a session buffer (useful for logging or dynamic actions).
•	pressed.
•	file_uploader(key, label, accept_multiple_files=False)
Registers a file upload widget in the main UI.
•	get_file_upload_value(key)
Retrieves the uploaded file's data.

