# AgentAuth

AgentAuth is a Python package that helps automate web authentication by simulating human-like login behavior. It supports various authentication methods including:
- Standard username/password login
- Time-based One-Time Passwords (TOTP)
- Email magic links
- Email verification codes

## Features

- 🤖 **Automated Authentication**: Handles complex login flows automatically
- 📧 **Email Integration**: Supports email-based verification (magic links and codes)
- 🔐 **Password Manager Integration**: Works with 1Password and local credential storage
- 🌐 **Browser Integration**: Compatible with remote CDP-based browsers

## Installation

```bash
pip install agentauth
```

## Quick Start

```python
from agentauth import AgentAuth, CredentialManager

# Load credentials from a file and/or password manager
credential_manager = CredentialManager()
credential_manager.load_file("credentials.json")
credential_manager.load_1password("1password_service_account_token")

# Creat an instance of AgentAuth with access to credentials and an email inbox
aa = AgentAuth(
    credential_manager=credential_manager,

    # (Optional) Connect an email inbox for authentication requiring email links or codes
    imap_server="imap.example.com",
    imap_username="agent@example.com",
    imap_password="agent_email_password"
)

# Authenticate to a website for a given username
cookies = await aa.auth(
    "https://example.com",
    "agent@example.com",
    cdp_url="wss://..."  # Optional: for using remote browser services
)

# Use cookies for authenticated agent actions
```

**ℹ️ You can pass a custom LLM to the AgentAuth constructor. OpenAI's `gpt-4o` is the default and requires an `OPENAI_API_KEY` environment variable.**

# To Do

- [ ] Add Bitwarden integration
- [ ] Support local S/LLM for email scanning
- [ ] Add automatic publishing

# Contributing

Contributions are welcome! Please feel free to submit a pull request.

# License

This project is licensed under the MIT License.
