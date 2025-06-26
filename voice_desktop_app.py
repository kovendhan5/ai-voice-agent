"""
Desktop Voice Interface for Orpheus TTS API
A GUI application that allows voice input and audio output
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import requests
import json
import tempfile
import os
import pygame
import time
from datetime import datetime

try:
    import speech_recognition as sr
    SPEECH_RECOGNITION_AVAILABLE = True
except ImportError:
    SPEECH_RECOGNITION_AVAILABLE = False

class VoiceInterface:
    def __init__(self, root):
        self.root = root
        self.root.title("🎤 Orpheus TTS Voice Interface")
        self.root.geometry("800x600")
        self.root.configure(bg='#2c3e50')
        
        # Initialize variables
        self.is_listening = False
        self.current_text = ""
        self.api_url = "http://localhost:8080"
        self.conversation_history = []
        
        # Initialize speech recognition
        if SPEECH_RECOGNITION_AVAILABLE:
            self.recognizer = sr.Recognizer()
            self.microphone = sr.Microphone()
        else:
            self.recognizer = None
            self.microphone = None
        
        # Initialize pygame for audio playback
        try:
            pygame.mixer.init()
            self.audio_available = True
        except:
            self.audio_available = False
        
        self.setup_ui()
        self.check_dependencies()
    
    def setup_ui(self):
        """Setup the user interface"""
        # Configure style
        style = ttk.Style()
        style.theme_use('clam')
        
        # Main frame
        main_frame = tk.Frame(self.root, bg='#2c3e50')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        title_label = tk.Label(
            main_frame, 
            text="🎤 Orpheus Voice Chat", 
            font=('Arial', 24, 'bold'),
            fg='white', 
            bg='#2c3e50'
        )
        title_label.pack(pady=(0, 20))
        
        # Status frame
        status_frame = tk.Frame(main_frame, bg='#2c3e50')
        status_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.status_label = tk.Label(
            status_frame,
            text="Ready - Click 'Start Listening' to begin",
            font=('Arial', 12),
            fg='#ecf0f1',
            bg='#2c3e50'
        )
        self.status_label.pack()
        
        # Control buttons frame
        controls_frame = tk.Frame(main_frame, bg='#2c3e50')
        controls_frame.pack(pady=10)
        
        self.listen_button = tk.Button(
            controls_frame,
            text="🎤 Start Listening",
            font=('Arial', 14, 'bold'),
            bg='#e74c3c',
            fg='white',
            padx=20,
            pady=10,
            command=self.toggle_listening
        )
        self.listen_button.pack(side=tk.LEFT, padx=5)
        
        self.speak_button = tk.Button(
            controls_frame,
            text="🔊 Speak Text",
            font=('Arial', 14, 'bold'),
            bg='#3498db',
            fg='white',
            padx=20,
            pady=10,
            command=self.speak_text
        )
        self.speak_button.pack(side=tk.LEFT, padx=5)
        
        self.clear_button = tk.Button(
            controls_frame,
            text="🗑️ Clear",
            font=('Arial', 14),
            bg='#95a5a6',
            fg='white',
            padx=20,
            pady=10,
            command=self.clear_text
        )
        self.clear_button.pack(side=tk.LEFT, padx=5)
        
        # Voice selection frame
        voice_frame = tk.Frame(main_frame, bg='#2c3e50')
        voice_frame.pack(pady=10)
        
        tk.Label(
            voice_frame, 
            text="Voice:", 
            font=('Arial', 12),
            fg='white', 
            bg='#2c3e50'
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        self.voice_var = tk.StringVar(value="tara")
        self.voice_combo = ttk.Combobox(
            voice_frame,
            textvariable=self.voice_var,
            values=["tara", "alex", "sarah"],
            state="readonly",
            font=('Arial', 12)
        )
        self.voice_combo.pack(side=tk.LEFT)
        
        # Text display frame
        text_frame = tk.Frame(main_frame, bg='#2c3e50')
        text_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        tk.Label(
            text_frame, 
            text="Recognized Speech:", 
            font=('Arial', 12, 'bold'),
            fg='white', 
            bg='#2c3e50'
        ).pack(anchor=tk.W)
        
        self.text_display = scrolledtext.ScrolledText(
            text_frame,
            height=8,
            font=('Arial', 12),
            bg='#34495e',
            fg='white',
            insertbackground='white'
        )
        self.text_display.pack(fill=tk.BOTH, expand=True, pady=(5, 0))
        
        # Conversation history frame
        history_frame = tk.Frame(main_frame, bg='#2c3e50')
        history_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        tk.Label(
            history_frame, 
            text="Conversation History:", 
            font=('Arial', 12, 'bold'),
            fg='white', 
            bg='#2c3e50'
        ).pack(anchor=tk.W)
        
        self.history_display = scrolledtext.ScrolledText(
            history_frame,
            height=6,
            font=('Arial', 10),
            bg='#34495e',
            fg='#ecf0f1',
            state=tk.DISABLED
        )
        self.history_display.pack(fill=tk.BOTH, expand=True, pady=(5, 0))
        
        # Settings frame
        settings_frame = tk.Frame(main_frame, bg='#2c3e50')
        settings_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(
            settings_frame, 
            text="API URL:", 
            font=('Arial', 10),
            fg='white', 
            bg='#2c3e50'
        ).pack(side=tk.LEFT)
        
        self.api_entry = tk.Entry(
            settings_frame,
            font=('Arial', 10),
            width=30,
            bg='#34495e',
            fg='white',
            insertbackground='white'
        )
        self.api_entry.insert(0, self.api_url)
        self.api_entry.pack(side=tk.LEFT, padx=(5, 10))
        
        test_api_button = tk.Button(
            settings_frame,
            text="Test API",
            font=('Arial', 10),
            bg='#27ae60',
            fg='white',
            padx=10,
            command=self.test_api_connection
        )
        test_api_button.pack(side=tk.LEFT)
        
        # Auto-speak checkbox
        self.auto_speak_var = tk.BooleanVar(value=True)
        auto_speak_check = tk.Checkbutton(
            settings_frame,
            text="Auto Speak",
            variable=self.auto_speak_var,
            font=('Arial', 10),
            fg='white',
            bg='#2c3e50',
            selectcolor='#34495e'
        )
        auto_speak_check.pack(side=tk.RIGHT)
    
    def check_dependencies(self):
        """Check if required dependencies are available"""
        messages = []
        
        if not SPEECH_RECOGNITION_AVAILABLE:
            messages.append("⚠️ Speech recognition not available. Install: pip install SpeechRecognition pyaudio")
        
        if not self.audio_available:
            messages.append("⚠️ Audio playback not available. Install: pip install pygame")
        
        if messages:
            messagebox.showwarning("Dependencies Missing", "\n".join(messages))
    
    def toggle_listening(self):
        """Toggle speech recognition on/off"""
        if not SPEECH_RECOGNITION_AVAILABLE:
            messagebox.showerror("Error", "Speech recognition not available")
            return
        
        if self.is_listening:
            self.stop_listening()
        else:
            self.start_listening()
    
    def start_listening(self):
        """Start listening for speech"""
        self.is_listening = True
        self.listen_button.config(text="🛑 Stop Listening", bg='#27ae60')
        self.status_label.config(text="🎤 Listening... Speak now!")
        
        # Start listening in a separate thread
        threading.Thread(target=self.listen_worker, daemon=True).start()
    
    def stop_listening(self):
        """Stop listening for speech"""
        self.is_listening = False
        self.listen_button.config(text="🎤 Start Listening", bg='#e74c3c')
        self.status_label.config(text="Ready - Click 'Start Listening' to begin")
    
    def listen_worker(self):
        """Worker thread for speech recognition"""
        try:
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
            
            while self.is_listening:
                try:
                    with self.microphone as source:
                        # Listen for audio with timeout
                        audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=5)
                    
                    # Recognize speech
                    text = self.recognizer.recognize_google(audio)
                    
                    # Update UI in main thread
                    self.root.after(0, self.update_text, text)
                    
                except sr.WaitTimeoutError:
                    # Timeout is normal, continue listening
                    continue
                except sr.UnknownValueError:
                    # Could not understand audio
                    self.root.after(0, self.update_status, "Could not understand audio")
                except sr.RequestError as e:
                    # API error
                    self.root.after(0, self.update_status, f"Speech recognition error: {e}")
                    break
        
        except Exception as e:
            self.root.after(0, self.update_status, f"Microphone error: {e}")
        
        finally:
            self.root.after(0, self.stop_listening)
    
    def update_text(self, text):
        """Update the text display with recognized speech"""
        self.current_text = text
        self.text_display.delete(1.0, tk.END)
        self.text_display.insert(tk.END, text)
        
        self.add_to_history("👤 You", text)
        self.status_label.config(text=f"✅ Recognized: {text[:50]}...")
        
        # Auto-speak if enabled
        if self.auto_speak_var.get():
            threading.Thread(target=self.speak_text, daemon=True).start()
    
    def update_status(self, message):
        """Update the status label"""
        self.status_label.config(text=message)
    
    def speak_text(self):
        """Generate and play speech from current text"""
        text = self.current_text.strip()
        if not text:
            text = self.text_display.get(1.0, tk.END).strip()
        
        if not text:
            self.update_status("❌ No text to speak")
            return
        
        voice = self.voice_var.get()
        api_url = self.api_entry.get()
        
        self.root.after(0, self.update_status, "🔊 Generating speech...")
        
        try:
            # Make API request
            response = requests.post(
                f"{api_url}/speak",
                json={"text": f"{voice}: {text}", "voice": voice},
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            
            if response.status_code == 200:
                # Save audio to temporary file
                with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
                    temp_file.write(response.content)
                    temp_filename = temp_file.name
                
                # Play audio
                if self.audio_available:
                    pygame.mixer.music.load(temp_filename)
                    pygame.mixer.music.play()
                    
                    # Wait for playback to finish
                    while pygame.mixer.music.get_busy():
                        time.sleep(0.1)
                
                # Clean up
                os.unlink(temp_filename)
                
                self.root.after(0, self.add_to_history, f"🤖 {voice.upper()}", text)
                self.root.after(0, self.update_status, "✅ Speech completed")
            
            else:
                self.root.after(0, self.update_status, f"❌ API error: {response.status_code}")
        
        except Exception as e:
            self.root.after(0, self.update_status, f"❌ Speech error: {str(e)}")
    
    def clear_text(self):
        """Clear the text display"""
        self.text_display.delete(1.0, tk.END)
        self.current_text = ""
        self.update_status("Text cleared")
    
    def add_to_history(self, speaker, text):
        """Add message to conversation history"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        message = f"[{timestamp}] {speaker}: {text}\n"
        
        self.history_display.config(state=tk.NORMAL)
        self.history_display.insert(tk.END, message)
        self.history_display.see(tk.END)
        self.history_display.config(state=tk.DISABLED)
    
    def test_api_connection(self):
        """Test connection to the API"""
        api_url = self.api_entry.get()
        try:
            response = requests.get(f"{api_url}/", timeout=5)
            if response.status_code == 200:
                self.update_status("✅ API connection successful")
                messagebox.showinfo("Success", "Connected to API successfully!")
            else:
                self.update_status(f"❌ API error: {response.status_code}")
        except Exception as e:
            self.update_status(f"❌ Connection failed: {str(e)}")
            messagebox.showerror("Connection Error", f"Could not connect to API:\n{str(e)}")

def main():
    """Main function to run the application"""
    root = tk.Tk()
    app = VoiceInterface(root)
    
    # Center the window
    root.update_idletasks()
    x = (root.winfo_screenwidth() - root.winfo_width()) // 2
    y = (root.winfo_screenheight() - root.winfo_height()) // 2
    root.geometry(f"+{x}+{y}")
    
    root.mainloop()

if __name__ == "__main__":
    main()
