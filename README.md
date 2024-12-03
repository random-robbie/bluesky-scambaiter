# Bluesky Scambaiter 🎭

A defensive cybersecurity tool for automated scam response using the Bluesky social network. This tool helps security professionals waste scammers' time by automatically responding to their DMs using an AI-powered Lord Flashheart (from Blackadder) personality.

## 🛡️ Security Professional Use Only

This tool is intended for legitimate cybersecurity professionals conducting authorized testing and scam prevention. Always ensure compliance with:
- Applicable laws and regulations
- Bluesky's Terms of Service
- OpenRouter's Terms of Service
- Your organization's security policies

## 🚀 Features

- Automated monitoring of Bluesky DMs from specified accounts
- Integration with OpenRouter's Mythomax LLM for response generation
- Lord Flashheart personality simulation for engaging responses
- Rate limiting and API error handling
- Message deduplication
- Comprehensive error logging

## 📋 Prerequisites

- Node.js 16.x or higher
- npm or yarn
- Bluesky account
- OpenRouter API key
- Proper authorization for security testing

## 🔧 Installation

1. Clone the repository:
```bash
git clone https://github.com/random-robbie/bluesky-scambaiter.git
cd bluesky-scambaiter
```

2. Install dependencies:
```bash
npm install @atproto/api dotenv node-fetch winston
```

3. Create a `.env` file in the project root:
```env
BLUESKY_IDENTIFIER=your.handle.com
BLUESKY_PASSWORD=your_password
TARGET_USER=scammer.handle.com
OPENROUTER_API_KEY=your_openrouter_api_key
```

## 🚀 Usage

1. Start the script:
```bash
node scambaiter.js
```

2. Monitor the console output for:
- Connection status
- Message processing
- API responses
- Error logs

## 🔍 Error Handling

The script includes comprehensive error handling for:
- Bluesky API authentication failures
- Network connectivity issues
- API rate limiting
- Message processing errors
- LLM API failures
- Invalid responses

All errors are logged with:
- Timestamp
- Error type
- Detailed error message
- Stack trace when applicable

## 📝 Logging

Logs are written to:
- Console (standard output)
- error.log (for error tracking)
- activity.log (for message processing)

## ⚙️ Configuration

Modify `config.js` to adjust:
- Check interval (default: 60 seconds)
- Response temperature (default: 0.85)
- Max tokens per response (default: 200)
- Personality prompt settings

## 🛠️ Troubleshooting

Common issues and solutions:

1. Authentication Failures
```
Error: Failed to login to Bluesky
Solution: Check your credentials in .env
```

2. Rate Limiting
```
Error: Too many requests
Solution: Adjust CHECK_INTERVAL in config
```

3. API Connection Issues
```
Error: Network error
Solution: Check your internet connection and API endpoints
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

- AtProto team for the Bluesky API
- OpenRouter for AI API access
- BBC's Blackadder for Lord Flashheart inspiration
