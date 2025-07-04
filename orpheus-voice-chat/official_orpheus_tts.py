#!/usr/bin/env python3
"""
🎯 OFFICIAL ORPHEUS-TTS IMPLEMENTATION
==================================================
✅ Based on official Canopy Labs Orpheus code
✅ Real SNAC tokenization and audio processing
✅ Actual Orpheus model inference
✅ CPU-optimized for Intel systems
✅ Real emotion tags support
==================================================
"""

import os
import sys
import warnings
import torch
import numpy as np
import soundfile as sf
import tempfile
import time
import asyncio
from typing import Optional, Dict, List
import pygame
import librosa
import torchaudio.transforms as T

# Force CPU-only mode for Intel systems
os.environ['CUDA_VISIBLE_DEVICES'] = ''
os.environ['FORCE_CPU'] = '1'
torch.set_num_threads(4)
warnings.filterwarnings("ignore")

class OfficialOrpheusTTS:
    """
    Official Orpheus-TTS implementation based on Canopy Labs code
    Uses real SNAC tokenization and proper model architecture
    """
    
    def __init__(self):
        self.device = 'cpu'  # CPU for Intel systems
        self.sample_rate = 24000
        
        # Official Orpheus voices
        self.voices = {
            'tara': 'tara',
            'leah': 'leah', 
            'jess': 'jess',
            'leo': 'leo',
            'dan': 'dan',
            'mia': 'mia',
            'zac': 'zac',
            'zoe': 'zoe'
        }
        
        # Official Orpheus emotion tags
        self.emotion_tags = ['<laugh>', '<chuckle>', '<sigh>', '<cough>', '<sniffle>', '<groan>', '<yawn>', '<gasp>']
        
        self.model = None
        self.tokenizer = None
        self.snac_model = None
        
        # Initialize pygame for audio playback
        pygame.mixer.pre_init(frequency=24000, size=-16, channels=1, buffer=512)
        pygame.mixer.init()
        
    def install_dependencies(self):
        """Install required Orpheus dependencies"""
        print("🔧 Installing Orpheus dependencies...")
        
        import subprocess
        
        # Install core dependencies
        packages = [
            "transformers",
            "datasets", 
            "torch",
            "torchaudio",
            "librosa",
            "soundfile"
        ]
        
        for package in packages:
            try:
                subprocess.run([sys.executable, "-m", "pip", "install", package], 
                             check=True, capture_output=True)
                print(f"✅ Installed {package}")
            except:
                print(f"⚠️ Failed to install {package}")
        
        # Try to install SNAC
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "snac"], 
                         check=True, capture_output=True)
            print("✅ Installed SNAC")
        except:
            print("⚠️ SNAC installation failed, will use fallback")
            
        # Try official orpheus-speech package
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "orpheus-speech"], 
                         check=True, capture_output=True)
            print("✅ Installed orpheus-speech")
        except:
            print("⚠️ orpheus-speech installation failed, using manual implementation")
    
    def load_orpheus_model(self):
        """Load ONLY the real Orpheus model - no alternatives"""
        print("🔄 Loading ONLY the real Orpheus-TTS model...")
        print("🚫 NO alternative models - Orpheus ONLY!")
        
        try:
            # Method 1: Try orpheus-speech package (real Orpheus)
            return self.load_orpheus_package()
            
        except Exception as e:
            print(f"⚠️ Orpheus package failed: {e}")
            
            try:
                # Method 2: Manual real Orpheus implementation ONLY
                return self.load_manual_orpheus()
                
            except Exception as e2:
                print(f"❌ Real Orpheus manual loading failed: {e2}")
                print("❌ FAILED: Could not load the REAL Orpheus model")
                print("💡 Please ensure you have access to canopylabs/orpheus-tts-0.1-finetune-prod")
                print("💡 Run: huggingface-cli login")
                return False
    
    def load_orpheus_package(self):
        """Load using orpheus-speech package"""
        try:
            from orpheus_tts import OrpheusModel
            
            self.model = OrpheusModel(
                model_name="canopylabs/orpheus-tts-0.1-finetune-prod",
                max_model_len=2048
            )
            
            print("✅ Orpheus package model loaded")
            self.model_type = 'package'
            return True
            
        except Exception as e:
            raise Exception(f"Package loading failed: {e}")
    
    def load_manual_orpheus(self):
        """Manual implementation using ONLY the real Orpheus model"""
        try:
            from transformers import AutoModelForCausalLM, AutoTokenizer
            from huggingface_hub import snapshot_download
            import subprocess
            
            # ONLY use the real Orpheus model  
            model_name = "canopylabs/orpheus-3b-0.1-ft"
            
            print(f"📥 Loading ONLY the real Orpheus model: {model_name}")
            
            # Login to Hugging Face if needed
            try:
                print("🔑 Setting up Hugging Face authentication...")
                subprocess.run([sys.executable, "-m", "pip", "install", "huggingface_hub"], 
                             check=True, capture_output=True)
                
                # Set token if available
                import os
                hf_token = os.getenv('HUGGINGFACE_HUB_TOKEN') or os.getenv('HUGGINGFACE_TOKEN')
                if hf_token:
                    print(f"🔑 Found HF token: {hf_token[:8]}...")
                    # Login using the token
                    from huggingface_hub import login
                    login(token=hf_token)
                    print("✅ Successfully logged into Hugging Face!")
                else:
                    print("⚠️ No HF token found. Please set HUGGINGFACE_TOKEN environment variable.")
                    print("💡 You may need to login with: huggingface-cli login")
                
            except Exception as e:
                print(f"⚠️ HF setup issue: {e}")
            
            try:
                # Load the REAL Orpheus tokenizer
                print("📥 Loading Orpheus tokenizer...")
                self.tokenizer = AutoTokenizer.from_pretrained(
                    model_name,
                    token=hf_token  # Use token parameter instead of use_auth_token
                )
                
                # Download ONLY the real Orpheus model
                print("📥 Downloading real Orpheus model files...")
                model_path = snapshot_download(
                    repo_id=model_name,
                    token=hf_token,  # Use token parameter
                    allow_patterns=[
                        "config.json",
                        "*.safetensors",
                        "model.safetensors.index.json",
                        "generation_config.json"
                    ],
                    ignore_patterns=[
                        "optimizer.pt",
                        "pytorch_model.bin", 
                        "training_args.bin",
                        "scheduler.pt"
                    ]
                )
                
                # Load the REAL Orpheus model for CPU
                print("🔄 Loading real Orpheus model on CPU...")
                self.model = AutoModelForCausalLM.from_pretrained(
                    model_name,
                    torch_dtype=torch.float32,  # CPU compatible
                    device_map='cpu',
                    token=hf_token,  # Use token parameter
                    low_cpu_mem_usage=True  # Optimize for CPU
                )
                
                print("✅ REAL Orpheus model loaded successfully!")
                
            except Exception as auth_error:
                print(f"❌ Authentication error: {auth_error}")
                print("💡 Please run: huggingface-cli login")
                print("� Or set HUGGINGFACE_TOKEN environment variable")
                raise Exception("Real Orpheus model requires authentication")
            
            # Load SNAC model for REAL Orpheus processing
            try:
                from snac import SNAC
                print("📥 Loading SNAC for real Orpheus processing...")
                self.snac_model = SNAC.from_pretrained("hubertsiuzdak/snac_24khz")
                print("✅ SNAC model loaded - ready for real Orpheus!")
            except Exception as snac_error:
                print(f"❌ SNAC loading failed: {snac_error}")
                print("❌ SNAC is REQUIRED for real Orpheus voice processing!")
                raise Exception("Real Orpheus requires SNAC model")
            
            print("🎭 REAL Orpheus-TTS model ready for CPU inference!")
            self.model_type = 'manual'
            return True
            
        except Exception as e:
            print(f"❌ REAL Orpheus loading failed: {e}")
            print("💡 Make sure you have access to canopylabs/orpheus-tts-0.1-finetune-prod")
            print("💡 Run: huggingface-cli login")
            raise Exception(f"Real Orpheus model loading failed: {e}")
    
    def load_tts_fallback(self):
        """Load TTS library as fallback for Orpheus-style synthesis"""
        try:
            import pyttsx3
            
            self.model = pyttsx3.init()
            
            # Configure for best quality
            voices = self.model.getProperty('voices')
            if voices:
                # Set a good voice
                self.model.setProperty('voice', voices[0].id)
            
            self.model.setProperty('rate', 180)
            self.model.setProperty('volume', 1.0)
            
            print("✅ TTS fallback loaded")
            self.model_type = 'fallback'
            return True
            
        except Exception as e:
            print(f"❌ TTS fallback failed: {e}")
            return False
    
    def tokenize_audio_snac(self, waveform):
        """Tokenize audio using SNAC (official Orpheus method)"""
        if self.snac_model is None:
            return None
            
        try:
            waveform = torch.from_numpy(waveform).unsqueeze(0)
            waveform = waveform.to(dtype=torch.float32)
            waveform = waveform.unsqueeze(0)
            
            with torch.inference_mode():
                codes = self.snac_model.encode(waveform)
            
            all_codes = []
            for i in range(codes[0].shape[1]):
                all_codes.append(codes[0][0][i].item() + 128266)
                all_codes.append(codes[1][0][2*i].item() + 128266 + 4096)
                all_codes.append(codes[2][0][4*i].item() + 128266 + (2*4096))
                all_codes.append(codes[2][0][(4*i)+1].item() + 128266 + (3*4096))
                all_codes.append(codes[1][0][(2*i)+1].item() + 128266 + (4*4096))
                all_codes.append(codes[2][0][(4*i)+2].item() + 128266 + (5*4096))
                all_codes.append(codes[2][0][(4*i)+3].item() + 128266 + (6*4096))
            
            return all_codes
            
        except Exception as e:
            print(f"❌ SNAC tokenization error: {e}")
            return None
    
    def redistribute_codes(self, code_list):
        """Redistribute codes back to audio (official Orpheus method)"""
        if self.snac_model is None:
            return None
            
        try:
            layer_1 = []
            layer_2 = []
            layer_3 = []
            
            for i in range((len(code_list)+1)//7):
                layer_1.append(code_list[7*i])
                layer_2.append(code_list[7*i+1] - 4096)
                layer_3.append(code_list[7*i+2] - (2*4096))
                layer_3.append(code_list[7*i+3] - (3*4096))
                layer_2.append(code_list[7*i+4] - (4*4096))
                layer_3.append(code_list[7*i+5] - (5*4096))
                layer_3.append(code_list[7*i+6] - (6*4096))
            
            codes = [
                torch.tensor(layer_1).unsqueeze(0),
                torch.tensor(layer_2).unsqueeze(0),
                torch.tensor(layer_3).unsqueeze(0)
            ]
            
            audio_hat = self.snac_model.decode(codes)
            return audio_hat
            
        except Exception as e:
            print(f"❌ Code redistribution error: {e}")
            return None
    
    def generate_with_package(self, text: str, voice: str) -> Optional[bytes]:
        """Generate using orpheus-speech package"""
        try:
            # Format text with voice
            prompt = f"{voice}: {text}"
            
            # Generate speech
            syn_tokens = self.model.generate_speech(
                prompt=prompt,
                voice=voice,
            )
            
            # Collect audio chunks
            audio_chunks = []
            for audio_chunk in syn_tokens:
                audio_chunks.append(audio_chunk)
            
            # Combine chunks
            if audio_chunks:
                full_audio = b''.join(audio_chunks)
                return full_audio
            else:
                return None
                
        except Exception as e:
            print(f"❌ Package generation error: {e}")
            return None
    
    def generate_with_fallback(self, text: str, voice: str) -> Optional[np.ndarray]:
        """Generate using TTS fallback with Orpheus-style processing"""
        try:
            # Remove emotion tags and process them
            clean_text = text
            emotion_detected = None
            
            for tag in self.emotion_tags:
                if tag in text:
                    emotion_detected = tag
                    clean_text = clean_text.replace(tag, '')
                    print(f"🎭 Processing emotion: {tag}")
                    break
            
            clean_text = clean_text.strip()
            
            # Apply emotion-specific modifications to voice
            if emotion_detected == '<laugh>':
                # Add laugh sound and modify speech
                clean_text = "Ha ha! " + clean_text
                self.model.setProperty('rate', 200)
                self.model.setProperty('volume', 1.0)
            elif emotion_detected == '<whisper>':
                # Whisper effect
                clean_text = clean_text.lower()
                self.model.setProperty('rate', 150)
                self.model.setProperty('volume', 0.6)
            elif emotion_detected == '<sigh>':
                # Add sigh and modify tone
                clean_text = "*sigh* " + clean_text
                self.model.setProperty('rate', 160)
            elif emotion_detected == '<gasp>':
                # Add gasp effect
                clean_text = "*gasp* " + clean_text
                self.model.setProperty('rate', 190)
            else:
                # Default settings
                self.model.setProperty('rate', 180)
                self.model.setProperty('volume', 0.9)
            
            # Set voice based on Orpheus voice selection
            voices = self.model.getProperty('voices')
            if voices:
                voice_idx = 0
                if voice in ['tara', 'leah', 'jess', 'mia', 'zoe']:
                    # Female voices
                    for i, v in enumerate(voices):
                        if 'female' in v.name.lower() or 'zira' in v.name.lower():
                            voice_idx = i
                            break
                elif voice in ['leo', 'dan', 'zac']:
                    # Male voices  
                    for i, v in enumerate(voices):
                        if 'male' in v.name.lower() or 'david' in v.name.lower():
                            voice_idx = i
                            break
                
                self.model.setProperty('voice', voices[voice_idx].id)
            
            # Generate audio file
            temp_file = tempfile.mktemp(suffix='.wav')
            self.model.save_to_file(clean_text, temp_file)
            self.model.runAndWait()
            
            # Read generated audio
            if os.path.exists(temp_file):
                audio_data, sr = sf.read(temp_file)
                os.unlink(temp_file)
                
                # Resample if needed
                if sr != self.sample_rate:
                    import librosa
                    audio_data = librosa.resample(audio_data, orig_sr=sr, target_sr=self.sample_rate)
                
                return audio_data
            else:
                return None
                
        except Exception as e:
            print(f"❌ Fallback generation error: {e}")
            return None
    def generate_with_manual(self, text: str, voice: str) -> Optional[np.ndarray]:
        """Generate using ONLY the real Orpheus model"""
        try:
            print(f"🎭 REAL Orpheus generation: {text[:30]}...")
            
            # Format prompt exactly like official Orpheus
            prompt = f"{voice}: {text}"
            
            # Tokenize prompt with real Orpheus tokenizer
            prompt_tokked = self.tokenizer(prompt, return_tensors="pt")
            input_ids = prompt_tokked["input_ids"]
            
            # Use REAL Orpheus special tokens (from official code)
            start_tokens = torch.tensor([[128259]], dtype=torch.int64)  # SOH
            end_tokens = torch.tensor([[128009, 128260, 128261, 128257]], dtype=torch.int64)  # SOT Text EOT EOH
            final_tokens = torch.tensor([[128258, 128262]], dtype=torch.int64)  # EOAI
            
            # Create REAL Orpheus input format
            full_input_ids = torch.cat([start_tokens, input_ids, end_tokens], dim=1)
            
            print("🔄 Generating with REAL Orpheus model...")
            
            # Generate using REAL Orpheus parameters
            with torch.no_grad():
                generated_ids = self.model.generate(
                    input_ids=full_input_ids,
                    max_new_tokens=990,
                    do_sample=True,
                    temperature=0.5,
                    top_p=0.9,
                    repetition_penalty=1.1,
                    num_return_sequences=1,
                    eos_token_id=128258,  # Real Orpheus EOS
                )
            
            print("✅ REAL Orpheus generation complete!")
            
            # Extract audio tokens using REAL Orpheus method
            token_to_find = 128257  # Start of speech token
            token_to_remove = 128258  # End token
            
            # Find last occurrence of start token
            token_indices = (generated_ids == token_to_find).nonzero(as_tuple=True)
            
            if len(token_indices[1]) > 0:
                last_occurrence_idx = token_indices[1][-1].item()
                cropped_tensor = generated_ids[:, last_occurrence_idx+1:]
            else:
                cropped_tensor = generated_ids
            
            # Remove end tokens
            mask = cropped_tensor != token_to_remove
            processed_rows = []
            for row in cropped_tensor:
                masked_row = row[row != token_to_remove]
                processed_rows.append(masked_row)
            
            # Convert to audio using REAL Orpheus SNAC processing
            audio_samples = []
            for row in processed_rows:
                row_length = row.size(0)
                new_length = (row_length // 7) * 7  # Real Orpheus 7-token grouping
                trimmed_row = row[:new_length]
                trimmed_row = [t.item() - 128266 for t in trimmed_row]  # Real Orpheus offset
                
                # Convert codes to audio using REAL SNAC
                if self.snac_model:
                    audio_hat = self.redistribute_codes(trimmed_row)
                    if audio_hat is not None:
                        audio_samples.append(audio_hat.detach().squeeze().cpu().numpy())
                        print("✅ REAL Orpheus audio generated with SNAC!")
                else:
                    print("❌ SNAC required for REAL Orpheus audio!")
                    return None
            
            if audio_samples:
                final_audio = np.concatenate(audio_samples)
                return final_audio
            else:
                print("❌ No REAL Orpheus audio generated")
                return None
                
        except Exception as e:
            print(f"❌ REAL Orpheus generation error: {e}")
            return None
    
    def play_orpheus_audio(self, audio_data) -> bool:
        """Play Orpheus audio on Intel system"""
        try:
            if isinstance(audio_data, bytes):
                # Handle bytes data from package
                temp_file = tempfile.mktemp(suffix='.wav')
                with open(temp_file, 'wb') as f:
                    f.write(audio_data)
                
                pygame.mixer.music.load(temp_file)
                pygame.mixer.music.play()
                
                while pygame.mixer.music.get_busy():
                    time.sleep(0.1)
                
                os.unlink(temp_file)
                
            elif isinstance(audio_data, np.ndarray):
                # Handle numpy array from manual method
                temp_file = tempfile.mktemp(suffix='.wav')
                sf.write(temp_file, audio_data, self.sample_rate)
                
                pygame.mixer.music.load(temp_file)
                pygame.mixer.music.play()
                
                while pygame.mixer.music.get_busy():
                    time.sleep(0.1)
                
                os.unlink(temp_file)
            
            print("✅ Orpheus audio played successfully")
            return True
            
        except Exception as e:
            print(f"❌ Audio playback error: {e}")
            return False
    
    async def speak_orpheus(self, text: str, voice: str = 'tara') -> bool:
        """Main Orpheus TTS function - ONLY real Orpheus"""
        if not text.strip():
            return False
        
        print(f"🎭 REAL Orpheus TTS: '{text[:50]}...' with voice '{voice}'")
        
        try:
            if self.model_type == 'package':
                print("🔄 Using real Orpheus package...")
                audio_data = self.generate_with_package(text, voice)
            elif self.model_type == 'manual':
                print("🔄 Using real Orpheus manual implementation...")
                audio_data = self.generate_with_manual(text, voice)
            else:
                print("❌ No REAL Orpheus model loaded!")
                return False
            
            if audio_data is not None:
                success = self.play_orpheus_audio(audio_data)
                if success:
                    print("✅ REAL Orpheus TTS complete")
                    return True
                else:
                    print("❌ Audio playback failed")
                    return False
            else:
                print("❌ REAL Orpheus audio generation failed")
                return False
                
        except Exception as e:
            print(f"❌ REAL Orpheus TTS error: {e}")
            return False

def test_official_orpheus():
    """Test the official Orpheus implementation"""
    print("🎯 OFFICIAL ORPHEUS-TTS TEST")
    print("=" * 50)
    print("🎭 Real Canopy Labs Orpheus model")
    print("🔧 SNAC tokenization and processing")
    print("🖥️ Intel CPU optimized")
    print("=" * 50)
    
    # Initialize Orpheus
    orpheus = OfficialOrpheusTTS()
    
    # Install dependencies
    orpheus.install_dependencies()
    
    # Load model
    if not orpheus.load_orpheus_model():
        print("❌ Failed to load Orpheus model")
        return False
    
    # Test cases with real Orpheus voices and emotions
    test_cases = [
        ("Hello! This is the official Orpheus voice model.", "tara"),
        ("I finally got into the university of my dreams! <laugh> I can't believe all this hard work actually paid off!", "jess"),
        ("Why is your frickin' Waymo blocking the frickin' road? GET OUT OF THE WAY!", "leo"),
        ("I'm so sorry to hear about your pet, but you know, he'll pull through. <sigh>", "leah"),
        ("Conversational, uhm, systems, tend to speak pretty robotically, because- because they don't, really understand how, uhm, humans talk.", "dan"),
        ("This is the real Orpheus voice with proper emotion processing! <laugh>", "mia")
    ]
    
    print("\n🧪 Testing Official Orpheus...")
    
    async def run_tests():
        success_count = 0
        for i, (text, voice) in enumerate(test_cases, 1):
            print(f"\n🎭 Orpheus Test {i}/6: {voice}")
            success = await orpheus.speak_orpheus(text, voice)
            if success:
                print(f"✅ Official Test {i} PASSED")
                success_count += 1
            else:
                print(f"❌ Official Test {i} FAILED")
            
            await asyncio.sleep(2)
        
        print(f"\n🎉 Official Orpheus testing complete!")
        print(f"✅ Success rate: {success_count}/6 tests")
        
        if success_count >= 5:
            print("🏆 EXCELLENT: Official Orpheus is working perfectly!")
        elif success_count >= 3:
            print("👍 GOOD: Official Orpheus is mostly working!")
        else:
            print("⚠️ NEEDS ATTENTION: Some issues with Orpheus")
    
    asyncio.run(run_tests())
    return True

if __name__ == "__main__":
    print("🎯 OFFICIAL ORPHEUS-TTS IMPLEMENTATION")
    print("=" * 50)
    print("🎭 Based on Canopy Labs official code")
    print("🔧 Real SNAC tokenization")
    print("💻 Intel CPU optimized")
    print("🎵 Authentic emotion processing")
    print("=" * 50)
    
    # System info
    print(f"🖥️ Device: {torch.device('cpu')}")
    print(f"🧵 Threads: {torch.get_num_threads()}")
    print(f"🐍 Python: {sys.version.split()[0]}")
    
    # Test official Orpheus
    test_official_orpheus()
