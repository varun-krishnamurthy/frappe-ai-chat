app_name = "frappe_ai_chat"
app_title = "Frappe AI Chat"
app_publisher = "Hermes Agent"
app_description = "A Frappe app providing a ChatGPT-like interface for AI interactions"
app_email = "dev@hermes.ai"
app_license = "MIT"

# Apps
# ------------------

# required_apps = []

# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
# 	{
# 		"name": "frappe_ai_chat",
# 		"logo": "/assets/frappe_ai_chat/logo.png",
# 		"title": "Frappe AI Chat",
# 		"route": "/ai-chat",
# 		"color": "#7C3AED",
# 	}
# ]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/frappe_ai_chat/css/frappe_ai_chat.css"
# app_include_js = "/assets/frappe_ai_chat/js/frappe_ai_chat.js"

# include js, css files in header of web template
# web_include_css = "/assets/frappe_ai_chat/css/frappe_ai_chat.css"
# web_include_js = "/assets/frappe_ai_chat/js/frappe_ai_chat.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "frappe_ai_chat/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

include js in page
page_js = {"ai-chat" : "/assets/frappe_ai_chat/js/ai-chat-bundle.js"}

# include js in doctype views
# doctype_js = {"doctype" : "Chat Session"}
# doctype_list_js = {"doctype" : "Chat Session"}
# doctype_tree_js = {"doctype" : "Chat Session"}
# doctype_calendar_js = {"doctype" : "Chat Session"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "ai-chat"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "frappe_ai_chat.install.before_install"
# after_install = "frappe_ai_chat.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "frappe_ai_chat.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in desk
# permissions = [{"doctype": "Chat Session", "read": "frappe_ai_chat.utils.has_permission"}]

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"Chat Session": "frappe_ai_chat.overrides.ChatSession"
# }

# Document Events
# ---------------
# DocType events

doc_events = {
	# "Chat Session": {
	# 	"after_insert": "frappe_ai_chat.chat_session.after_insert",
	# 	"on_update": "frappe_ai_chat.chat_session.on_update",
	# 	"on_trash": "frappe_ai_chat.chat_session.on_trash",
	# }
}

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"frappe_ai_chat.tasks.all"
# 	],
# 	"daily": [
# 		"frappe_ai_chat.tasks.daily"
# 	],
# 	"hourly": [
# 		"frappe_ai_chat.tasks.hourly"
# 	],
# 	"weekly": [
# 		"frappe_ai_chat.tasks.weekly"
# 	]
# 	"monthly": [
# 		"frappe_ai_chat.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "frappe_ai_chat.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "frappe_ai_chat.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype,
# along with any modifications made in other Frappe frameworks
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "frappe_ai_chat.event.get_events"
# }

# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype,
# along with any modifications made in other Frappe frameworks
# override_doctype_dashboards = {
# 	"Chat Session": "frappe_ai_chat.chat_session.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]


# Request Events
# ---------------
# before_request = ["frappe_ai_chat.utils.before_request"]
# after_request = ["frappe_ai_chat.utils.after_request"]

# Job Events
# ----------
# before_job = ["frappe_ai_chat.utils.before_job"]
# after_job = ["frappe_ai_chat.utils.after_job"]

# User Data Protection
# --------------------

# update_user_data = [
# 	{
# 		"doctype": "Chat Session",
# 		"filter_by": "user",
# 		"redact_fields": ["start_time", "end_time"],
# 		"partial": 1,
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"frappe_ai_chat.auth.validate"
# ]

fixtures = [
	{"dt": "Custom Field", "filters": [["dt", "in", ["Chat Session", "Chat Message"]]]},
	{"dt": "Property Setter", "filters": [["doc_type", "in", ["Chat Session", "Chat Message"]]]},
]
