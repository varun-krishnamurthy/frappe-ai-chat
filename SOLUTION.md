# Solution: Frappe AI Chat App

## Overview
Build a Frappe app that provides a ChatGPT-like interface for interacting with AI models, using custom Vue components for the frontend. The app will allow users to start chat sessions, send messages, and view AI responses in a conversational interface.

## Architecture Decision
We will extend Frappe's existing framework rather than building a completely separate SPA, leveraging:
- Frappe's backend for data storage (DocTypes) and API endpoints
- Frappe's frontend framework (Vue.js) for integrating custom components
- Custom page route for the chat interface

## Data Model

### 1. Chat Session DocType
Stores metadata for each chat conversation.
- **name**: Session ID (auto-generated)
- **user**: Link to User (who started the session)
- **start_time**: Datetime (auto-set on creation)
- **end_time**: Datetime (nullable, set when session is closed)
- **status**: Select (Open, Closed, Archived)
- **model**: Select (AI model used, e.g., gpt-3.5-turbo, gpt-4)
- **temperature**: Float (AI temperature setting)
- **max_tokens**: Int (maximum tokens for AI response)

### 2. Chat Message DocType
Stores individual messages within a session.
- **name**: Auto-generated ID
- **session**: Link to Chat Session (parent)
- **role**: Select (User, Assistant, System)
- **content**: Long Text (message content)
- **timestamp**: Datetime (auto-set)
- **tokens_used**: Int (optional, for tracking API usage)
- **metadata**: JSON (optional, for storing additional info like finish_reason)

## API Endpoints
All endpoints will be whitelisted and accessible via `/api/method/frappe_ai_chat.api.*`

### 1. Create New Chat Session
- **Method**: POST
- **Endpoint**: `/api/method/frappe_ai_chat.api.create_session`
- **Parameters**: 
  - model (optional, default: gpt-3.5-turbo)
  - temperature (optional, default: 0.7)
  - max_tokens (optional, default: 1000)
- **Returns**: Session document (name, status, etc.)

### 2. Send Message & Get AI Response
- **Method**: POST
- **Endpoint**: `/api/method/frappe_ai_chat.api.send_message`
- **Parameters**:
  - session: Session ID
  - content: User's message content
- **Process**:
  1. Save user message as Chat Message (role: User)
  2. Call AI API (OpenAI or compatible) with session history
  3. Save AI response as Chat Message (role: Assistant)
  4. Return both messages
- **Returns**: { user_message: {...}, ai_message: {...} }

### 3. Get Chat History
- **Method**: GET
- **Endpoint**: `/api/method/frappe_ai_chat.api.get_messages`
- **Parameters**: session (Session ID)
- **Returns**: List of Chat Messages ordered by timestamp

### 4. Update Session Status
- **Method**: POST
- **Endpoint**: `/api/method/frappe_ai_chat.api.update_session`
- **Parameters**:
  - session: Session ID
  - status: New status (Open/Closed/Archived)
- **Returns**: Updated session document

## Implementation Plan

### Backend (Python/Frappe)
1. Create DocTypes:
   - Chat Session
   - Chat Message
2. Create API methods in `frappe_ai_chat/api.py`:
   - create_session
   - send_message
   - get_messages
   - update_session
3. Add necessary permissions and roles
4. Implement AI service wrapper (pluggable for different providers)

### Frontend (Vue.js)
1. Create a custom Frappe page at `/ai-chat`
2. Develop Vue components:
   - ChatContainer: Main layout
   - MessageList: Displays messages with different styles for user/assistant
   - MessageInput: Text input with send button
   - SessionSidebar: Lists recent sessions (optional)
3. Use Frappe's `frappe.call` to interact with API endpoints
4. Implement real-time updates using Frappe's `frappe.realtime` (optional)
5. Style to resemble ChatGPT interface (dark theme, message bubbles, etc.)

### Integration Points
- Add chat icon to Frappe desk header (optional)
- Allow starting new chat from global search
- Add workspace for AI Chat (optional)

## Deployment Considerations
- API keys for AI services should be stored in site_config.json or environment variables
- Rate limiting and usage tracking can be implemented via hooks
- For production, consider webhook-based AI service integration to avoid long-running requests

## Open Questions
1. Should we store raw AI API responses or just the content?
2. How to handle streaming responses (for better UX)?
3. Should we add features like message regeneration, copying, etc.?
4. How to handle multiple AI providers (OpenAI, Anthropic, local models)?

## Next Steps
1. Create SOLUTION.md (done)
2. Scaffold Frappe app
3. Implement DocTypes and API
4. Build Vue components
5. Test and iterate