import frappe
import json
import requests
from frappe import _
from frappe.utils import now_datetime

# OpenAI API configuration
def get_openai_api_key():
    # Try to get from site config
    api_key = frappe.conf.get("openai_api_key")
    if not api_key:
        # Try environment variable
        import os
        api_key = os.environ.get("OPENAI_API_KEY")
    return api_key

def get_openai_headers():
    api_key = get_openai_api_key()
    if not api_key:
        frappe.throw(_("OpenAI API key not configured. Please set it in site_config.json or as OPENAI_API_KEY environment variable."))
    return {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

@frappe.whitelist()
def create_session(model=None, temperature=None, max_tokens=None):
    """Create a new chat session."""
    # Set defaults
    if model is None:
        model = "gpt-3.5-turbo"
    if temperature is None:
        temperature = 0.7
    if max_tokens is None:
        max_tokens = 1000

    # Create a new Chat Session
    session = frappe.get_doc({
        "doctype": "Chat Session",
        "user": frappe.session.user,
        "model": model,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "status": "Open"
    })
    session.insert(ignore_permissions=True)  # Allow creation even if user doesn't have write permission? We'll check permissions via whitelist.
    frappe.db.commit()

    return session

@frappe.whitelist()
def send_message(session, content):
    """Send a message and get AI response."""
    # Validate session exists and user has permission
    session_doc = frappe.get_doc("Chat Session", session)
    # Check if the user is allowed to write to this session (optional: we can add a permission check)
    # For simplicity, we allow if the session user matches current user or if user is System Manager
    if session_doc.user != frappe.session.user and not frappe.has_role("System Manager"):
        frappe.throw(_("You are not allowed to send messages to this session."), frappe.PermissionError)

    # Save user message
    user_msg = frappe.get_doc({
        "doctype": "Chat Message",
        "session": session,
        "role": "User",
        "content": content
    })
    user_msg.insert(ignore_permissions=True)

    # Get chat history for context (limit to last 10 messages to avoid too long context)
    messages = frappe.get_all(
        "Chat Message",
        filters={"session": session},
        fields=["role", "content"],
        order_by="timestamp asc",
        limit=10
    )
    # Convert to format for OpenAI API
    openai_messages = []
    for msg in messages:
        openai_messages.append({"role": msg.role.lower(), "content": msg.content})

    # Call OpenAI API
    try:
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=get_openai_headers(),
            json={
                "model": session_doc.model,
                "messages": openai_messages,
                "temperature": session_doc.temperature,
                "max_tokens": session_doc.max_tokens
            },
            timeout=30
        )
        response.raise_for_status()
        result = response.json()
    except requests.exceptions.RequestException as e:
        frappe.throw(_("Failed to get response from AI service: {0}").format(str(e)))

    # Extract AI response
    if not result.get("choices") or len(result["choices"]) == 0:
        frappe.throw(_("No response from AI service."))

    ai_message_content = result["choices"][0]["message"]["content"].strip()
    tokens_used = result.get("usage", {}).get("total_tokens")

    # Save AI message
    ai_msg = frappe.get_doc({
        "doctype": "Chat Message",
        "session": session,
        "role": "Assistant",
        "content": ai_message_content,
        "tokens_used": tokens_used,
        "metadata": json.dumps(result.get("usage", {}))
    })
    ai_msg.insert(ignore_permissions=True)

    frappe.db.commit()

    return {
        "user_message": user_msg.as_dict(),
        "ai_message": ai_msg.as_dict()
    }

@frappe.whitelist()
def get_messages(session):
    """Get all messages for a session."""
    # Check permission (similar to send_message)
    session_doc = frappe.get_doc("Chat Session", session)
    if session_doc.user != frappe.session.user and not frappe.has_role("System Manager"):
        frappe.throw(_("You are not allowed to view messages for this session."), frappe.PermissionError)

    messages = frappe.get_all(
        "Chat Message",
        filters={"session": session},
        fields=["name", "role", "content", "timestamp", "tokens_used", "metadata"],
        order_by="timestamp asc"
    )
    return messages

@frappe.whitelist()
def update_session(session, status):
    """Update session status."""
    session_doc = frappe.get_doc("Chat Session", session)
    # Check permission
    if session_doc.user != frappe.session.user and not frappe.has_role("System Manager"):
        frappe.throw(_("You are not allowed to update this session."), frappe.PermissionError)

    session_doc.status = status
    if status in ["Closed", "Archived"]:
        session_doc.end_time = now_datetime()
    session_doc.save(ignore_permissions=True)
    frappe.db.commit()

    return session_doc