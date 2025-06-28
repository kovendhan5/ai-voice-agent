# 🎤 Voice Interface Guide for Orpheus TTS

## 🌟 **You Now Have TWO Voice Interfaces!**

### 🌐 **Web Interface** (`voice_interface.html`)
- **Modern, responsive web UI**
- **Works in any modern browser**
- **Speech recognition + TTS in one page**
- **Real-time conversation history**
- **Easy to share and use**

### 🖥️ **Desktop App** (`voice_desktop_app.py`)
- **Native desktop application**
- **Tkinter-based GUI**
- **Offline capability**
- **Direct audio playback**
- **System integration**

---

## 🚀 **Quick Start Guide**

### **Option 1: Web Interface (Recommended)**
```cmd
# Start everything at once
start_voice_interface.bat
```
**What it does:**
1. ✅ Starts the TTS API server
2. ✅ Opens the web interface in your browser
3. ✅ Ready for voice interaction!

### **Option 2: Desktop App**
```cmd
# Start desktop application
start_desktop_voice.bat
```

### **Option 3: Manual Setup**
```cmd
# Terminal 1: Start API server
python app.py

# Terminal 2: Open web interface
start voice_interface.html

# OR start desktop app
python voice_desktop_app.py
```

---

## 🎤 **How to Use Voice Interface**

### **1. Web Interface Steps:**
1. 📱 **Allow microphone access** when prompted
2. 🎯 **Click the big microphone button** 
3. 🗣️ **Speak clearly** into your microphone
4. ✅ **See your speech as text** in real-time
5. 🔊 **Hear the AI speak back** automatically
6. 💬 **View conversation history** below

### **2. Desktop App Steps:**
1. 🔴 **Click "Start Listening"**
2. 🗣️ **Speak into microphone**
3. 📝 **See text appear** in the text box
4. 🔊 **Click "Speak Text"** or enable auto-speak
5. 🎵 **Audio plays automatically**

---

## ⚙️ **Voice Interface Features**

### **🎯 Core Features:**
- ✅ **Real-time speech recognition**
- ✅ **Multiple AI voices** (Tara, Alex, Sarah)
- ✅ **Automatic text-to-speech**
- ✅ **Conversation history**
- ✅ **API status monitoring**
- ✅ **Audio playback controls**

### **🛠️ Advanced Features:**
- ✅ **Auto-speak toggle**
- ✅ **Voice selection**
- ✅ **API URL configuration**
- ✅ **Connection testing**
- ✅ **Error handling**
- ✅ **Responsive design**

---

## 🎛️ **Voice Commands & Tips**

### **📢 Voice Input Format:**
```
"Hello, how are you today?"
"Tell me about artificial intelligence"
"What's the weather like?"
"Goodbye!"
```

### **🎤 Best Practices:**
- 🗣️ **Speak clearly** and at normal speed
- 🔇 **Avoid background noise**
- ⏸️ **Pause briefly** between sentences
- 🎯 **Stay within 3 feet** of microphone
- 💬 **Use natural language**

### **🔧 Troubleshooting:**
- ❌ **No speech detected**: Check microphone permissions
- ❌ **API connection failed**: Ensure server is running
- ❌ **Audio not playing**: Check browser audio settings
- ❌ **Poor recognition**: Reduce background noise

---

## 🌐 **Browser Compatibility**

### **✅ Recommended Browsers:**
- **Chrome** - Full support, best performance
- **Edge** - Full support, good performance  
- **Firefox** - Good support
- **Safari** - Limited speech recognition

### **📱 Mobile Support:**
- ✅ **Android Chrome** - Full support
- ✅ **iOS Safari** - Limited support
- ⚠️ **Mobile audio** may require user interaction

---

## 🎮 **Interface Controls**

### **🌐 Web Interface:**
| Control | Function |
|---------|----------|
| 🎤 **Big Red Button** | Start/Stop listening |
| 🔊 **Speak Text** | Generate speech from text |
| 🗑️ **Clear** | Clear current text |
| 🎵 **Voice Selector** | Choose AI voice |
| ⚙️ **API URL** | Configure server address |
| 🔄 **Auto Speak** | Automatic text-to-speech |

### **🖥️ Desktop App:**
| Control | Function |
|---------|----------|
| 🎤 **Start Listening** | Begin speech recognition |
| 🔊 **Speak Text** | Generate and play speech |
| 🗑️ **Clear** | Clear text display |
| 🎵 **Voice Dropdown** | Select voice |
| 🔗 **Test API** | Check server connection |
| ☑️ **Auto Speak** | Enable automatic speech |

---

## 💡 **Use Cases**

### **🎯 Perfect For:**
- 🗣️ **Voice testing** of TTS quality
- 💬 **Interactive conversations** with AI
- 🎵 **Voice comparison** between different speakers
- 🧪 **API functionality testing**
- 🎤 **Accessibility applications**
- 🎨 **Creative voice projects**

### **🚀 Example Interactions:**
```
You: "Hello, I'm testing the voice interface"
AI (Tara): "Hello, I'm testing the voice interface"

You: "Switch to Alex's voice and say something funny"
AI (Alex): "Switch to Alex's voice and say something funny"

You: "Can you tell me about the weather?"
AI (Sarah): "Can you tell me about the weather?"
```

---

## 🔧 **Configuration Options**

### **API Settings:**
- 🌐 **Server URL**: Default `http://localhost:8080`
- ⏱️ **Timeout**: 30 seconds for speech generation
- 🔄 **Retry**: Automatic reconnection attempts

### **Audio Settings:**
- 🎵 **Format**: WAV audio output
- 📊 **Quality**: 22kHz, 16-bit, mono
- 🔊 **Playback**: Automatic browser/system audio

### **Speech Recognition:**
- 🗣️ **Language**: English (US)
- ⏱️ **Timeout**: 5 seconds per phrase
- 🎯 **Accuracy**: Google Speech Recognition API

---

## 🎉 **You're All Set!**

Your voice interface is ready for testing! The system provides:

- ✅ **Full voice-to-voice interaction**
- ✅ **Multiple interface options**
- ✅ **Real-time processing**
- ✅ **Easy deployment**
- ✅ **Professional quality**

**🎤 Ready to start talking with your AI?** Run `start_voice_interface.bat` and begin your voice conversation! 🗣️
