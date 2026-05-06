# Frappe AI Chat App

A Frappe app that provides a ChatGPT-like interface for interacting with AI models, using custom Vue components.

## Features

- Create chat sessions with different AI models (GPT-3.5, GPT-4, Claude, etc.)
- Send messages and receive AI responses
- View chat history
- Session management (open, closed, archived)
- Custom Vue.js components for a modern chat interface

## Installation

### Prerequisites

- A Frappe bench (version 13 or 14 recommended)
- Python 3.14+ (for Frappe v14) or Python 3.13 (for Frappe v13)
- Node.js and npm (for building Vue components, if needed)
- An OpenAI API key (or compatible service)

### Steps

1. Copy the `frappe_ai_chat` directory to your Frappe bench's `apps` folder:
   ```bash
   cp -r /path/to/frappe_ai_chat /path/to/your/frappe-bench/apps/
   ```

2. Install the app:
   ```bash
   cd /path/to/your/frappe-bench
   bench --site your-site install-app frappe_ai_chat
   ```

3. Migrate the site:
   ```bash
   bench --site your-site migrate
   ```

4. Configure the OpenAI API key:
   - Add to your site's `site_config.json`:
     ```json
     {
       "openai_api_key": "your-openai-api-key-here"
     }
     ```
   - Or set the environment variable `OPENAI_API_KEY`.

5. Start the bench:
   ```bash
   bench start
   ```

6. Visit `http://localhost:8000/ai-chat` to use the app.

## Usage

- Click "New Chat" to start a new session.
- Type your message in the input box and press Enter or click Send.
- View the conversation history in the main chat area.
- Use the sidebar to switch between sessions or create new ones.

## Customization

- To change the AI models available, edit the `model` field in `frappe_ai_chat/doctype/chat_session/chat_session.json`.
- To modify the Vue components, edit the files in `frappe_ai_chat/public/js/components/` and rebuild the bundle (if using a build system).
- The current bundle is a simplified representation; for production, consider using Frappe's webpack setup or a separate Vue CLI project.

## API Endpoints

All endpoints are whitelisted and accessible via `/api/method/frappe_ai_chat.api.*`:

- `create_session`: Create a new chat session.
- `send_message`: Send a message and get an AI response.
- `get_messages`: Retrieve messages for a session.
- `update_session`: Update session status (open, closed, archived).

## Notes

- This app uses the OpenAI API by default. To use other AI providers, modify the `api.py` file.
- The Vue.js bundle in `public/js/ai-chat-bundle.js` is a simplified example. For a real-world app, you would want to use a proper build system (like Webpack or Vite) and follow Frappe's guidelines for integrating Vue components.
- The app includes basic permission checks: users can only view and edit their own sessions unless they are System Managers.

## Troubleshooting

- If you encounter issues with missing dependencies during bench setup, ensure you have the required system packages (like `pkg-config`, `glib`, etc.) installed.
- For Python version incompatibilities, try using a Frappe version that matches your Python version (e.g., Frappe v13 for Python 3.13).
- If the Vue app doesn't load, check the browser console for errors and ensure the bundle file is correctly referenced.

## License

MIT