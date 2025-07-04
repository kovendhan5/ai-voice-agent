# 🔐 SECURITY SETUP GUIDE

## 🔑 Environment Variables Setup

### Required Tokens

1. **Hugging Face Token** (Required for Orpheus TTS)
   - Go to: https://huggingface.co/settings/tokens
   - Create a token with "Read" permissions
   - Set environment variable: `HUGGINGFACE_TOKEN=your_token_here`

2. **Google API Key** (Required for AI responses)
   - Go to: https://console.cloud.google.com/apis/credentials
   - Create API key and enable Gemini API
   - Set environment variable: `GOOGLE_API_KEY=your_api_key_here`

### Setup Methods

#### Option 1: .env File (Recommended)
```bash
# Copy the example file
cp .env.example .env

# Edit .env file with your tokens
HUGGINGFACE_TOKEN=hf_your_actual_token_here
GOOGLE_API_KEY=your_google_api_key_here
```

#### Option 2: System Environment Variables
```bash
# Windows
set HUGGINGFACE_TOKEN=hf_your_actual_token_here
set GOOGLE_API_KEY=your_google_api_key_here

# Linux/Mac
export HUGGINGFACE_TOKEN=hf_your_actual_token_here
export GOOGLE_API_KEY=your_google_api_key_here
```

#### Option 3: Python Script
```python
import os
os.environ['HUGGINGFACE_TOKEN'] = 'hf_your_actual_token_here'
os.environ['GOOGLE_API_KEY'] = 'your_google_api_key_here'
```

## 🛡️ Security Best Practices

### ✅ DO:
- Use environment variables for all secrets
- Keep your .env file in .gitignore
- Use tokens with minimal required permissions
- Regularly rotate your tokens

### ❌ DON'T:
- Hardcode tokens in source code
- Commit .env files to git
- Share tokens in plain text
- Use tokens with excessive permissions

## 🔒 Model Access

### Orpheus TTS Model Access
1. **Login to Hugging Face**: https://huggingface.co/canopylabs/orpheus-3b-0.1-ft
2. **Accept Terms**: Click to share contact information
3. **Wait for Approval**: Usually instant
4. **Use Your Token**: Set in environment variables

### Verification
```python
# Test if your setup works
from huggingface_hub import whoami
print(whoami())  # Should show your username
```

## 🚨 If Tokens Are Exposed

1. **Immediate Action**: Revoke the exposed token
2. **Generate New Token**: Create a replacement
3. **Update Environment**: Use the new token
4. **Check Git History**: Remove from commits if needed

## 📞 Support

- **Hugging Face Issues**: https://huggingface.co/support
- **Google API Issues**: https://cloud.google.com/support
- **This Project**: Check README.md for troubleshooting
