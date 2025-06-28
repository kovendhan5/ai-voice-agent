# 🛠️ Manual Troubleshooting Guide

## 🎯 Let's Get This Working Step by Step!

### **Step 1: Test Basic Setup**
Open a command prompt in your project folder and run:

```cmd
cd "k:\full stack\AI\voice model\voice-ai-orpheus"
python simple_server.py
```

**Expected output:**
```
Loading TTS model...
Mock: Loading Orpheus model...
Model loaded!
🚀 Starting Orpheus TTS Server...
🌐 Server will be available at: http://localhost:8080
🔄 Starting server...
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:8080
 * Running on http://[your-ip]:8080
```

---

### **Step 2: Test the API (New Terminal Window)**
While the server is running, open a NEW command prompt and run:

```cmd
cd "k:\full stack\AI\voice model\voice-ai-orpheus"
python simple_test.py
```

**Expected output:**
```
🧪 Testing Orpheus TTS API
========================================
1. Testing health endpoint...
   Status: 200
   Response: {'status': 'healthy', 'message': 'Server is running!'}

2. Testing speech generation...
   ✅ Success! Audio saved to: api_test_output.wav
   📊 File size: 88244 bytes
```

---

### **Step 3: Test Voice Interface**
If Step 2 works, then:

1. **Keep the server running** from Step 1
2. **Double-click** `voice_interface.html` in your file explorer
3. **Allow microphone access** when prompted
4. **Click the big red microphone button**
5. **Speak into your microphone**
6. **You should see text appear and hear audio back**

---

## 🔍 **If Something Fails, Tell Me:**

### **A. Server Won't Start?**
Error messages like:
- `ModuleNotFoundError`
- `Port already in use`
- `Permission denied`

### **B. API Test Fails?**
Error messages like:
- `Connection refused`
- `HTTP 500 error`
- `Module not found`

### **C. Voice Interface Issues?**
Problems like:
- `Microphone not working`
- `No audio playback`
- `Speech recognition not working`
- `API connection failed`

---

## 🎯 **Quick Fixes for Common Issues:**

### **❌ "Module not found" errors:**
```cmd
pip install flask numpy scipy requests
```

### **❌ "Port 8080 in use" error:**
- Stop any running servers with Ctrl+C
- Or change port in the code to 8081

### **❌ "Permission denied" errors:**
- Run command prompt as Administrator
- Or use a different folder

### **❌ Voice interface not working:**
- Use Chrome or Edge browser
- Allow microphone permissions
- Check if server is running on localhost:8080

---

## 📋 **What Should Work:**

1. ✅ **Server starts** and shows "Running on http://127.0.0.1:8080"
2. ✅ **API test** creates a WAV file
3. ✅ **Voice interface** opens in browser
4. ✅ **Microphone** converts speech to text
5. ✅ **TTS generates** audio and plays it back

---

## 📞 **Let Me Know:**

**Copy and paste the exact error message you see, and tell me:**
- Which step fails?
- What error message appears?
- What you tried to do?

Then I can give you a specific solution! 🚀
