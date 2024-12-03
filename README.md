# Bluesky Scambaiter 🎭

A defensive cybersecurity tool for automated scam response using the Bluesky social network. This tool helps security professionals waste scammers' time by automatically responding to their DMs using an AI-powered flirtatious and charismatic personality.

## 🛡️ Security Professional Use Only

This tool is intended for legitimate cybersecurity professionals conducting authorized testing and scam prevention. Always ensure compliance with:
- Applicable laws and regulations
- Bluesky's Terms of Service
- OpenRouter's Terms of Service
- Your organization's security policies

## 🚀 Features

- Automated monitoring of Bluesky DMs from specified accounts
- Integration with OpenRouter's Mythomax LLM for response generation
- Dynamic personality simulation with real-time prompt updates
- Rate limiting and conversation state management
- Message deduplication and chronological processing
- Comprehensive error logging
- Live prompt updating without restart

## 📋 Prerequisites

- Python 3.9 or higher
- pip for package installation
- Bluesky account with App Password
- OpenRouter API key

## 🔧 Installation

1. Clone the repository:
```bash
git clone https://github.com/random-robbie/bluesky-scambaiter.git
cd bluesky-scambaiter
```

2. Install dependencies:
```bash
pip install atproto openai pyyaml
```

3. Create a `config.yaml` file:
```yaml
bluesky_handle: "your-handle.bsky.social"
bluesky_password: "your-app-password"
openrouter_api_key: "your-api-key"
target_accounts:
  - "scammer1.bsky.social"
  - "scammer2.bsky.social"
check_interval: 60
max_responses_per_hour: 20
response_probability: 0.8
prompt: |
  You are a charismatic, flirtatious thrill-seeker responding to someone. Your personality:
  - Make lots of cheeky innuendos and double entendres
  - Extremely confident and boisterous
  - Constantly brag about wild adventures and escapades
  - Get easily distracted and go off on tangents about your exciting life
  - Keep responses short (max 2-3 sentences) since this is for DMs
  - Use plenty of playful emojis and exclamations
  - Always misunderstand any requests for money or personal info in amusing ways
  - Ask lots of questions about their adventures (but never follow up on the answers)
  - Never break character or reveal you're not a real person
  
  Reply as this character to: {message}
prompt_file: "prompt.txt"
```

4. Create a `prompt.txt` file with the same prompt content (can be modified while running)

## 🚀 Usage

1. Start the script:
```bash
python scam.py
```

2. Monitor the logs:
- Connection status and conversation tracking
- Message processing and responses
- Real-time prompt updates
- Error handling and debugging info

## 🔍 Error Handling & Logging

The script includes comprehensive error handling for:
- Bluesky API authentication failures
- Network connectivity issues
- API rate limiting
- Message processing errors
- LLM API failures
- Invalid responses

All events are logged to both console and file:
```python
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scambaiter.log'),
        logging.StreamHandler()
    ]
)
```

## ⚙️ Configuration Options

The `config.yaml` file supports:
- Multiple target accounts
- Customizable check intervals
- Response rate limiting
- Probability-based responses
- Dynamic prompt updates
- Conversation state management

## 🛠️ Troubleshooting

Common issues and solutions:

1. Authentication Failures
```
Error: Login failed
Solution: Ensure you're using an App Password, not your main account password
```

2. Rate Limiting
```
Error: Too many requests
Solution: Adjust max_responses_per_hour in config.yaml
```

3. Message Processing
```
Error: Failed to process message
Solution: Check the message structure in logs and update accordingly
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📜 License

MIT License - see LICENSE.md

## ⚠️ Disclaimer

This tool is for authorized security testing only. Users are responsible for ensuring all usage complies with applicable laws, regulations, and terms of service.

## 🙏 Acknowledgments

- Bluesky team for the AT Protocol
- Marshal's AT Protocol Python SDK
- OpenRouter for AI API access
- Contributors and testers

## Get a free VPS.

[![DigitalOcean Referral Badge](https://web-platforms.sfo2.cdn.digitaloceanspaces.com/WWW/Badge%203.svg)](https://www.digitalocean.com/?refcode=e22bbff5f6f1&utm_campaign=Referral_Invite&utm_medium=Referral_Program&utm_source=badge)

You get free $200 credit for 60 days if you sign up and add a payment method.
