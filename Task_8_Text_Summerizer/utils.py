import PyPDF2
import requests
from bs4 import BeautifulSoup
import re
import trafilatura
from readability import Document
import os
import tempfile
import time
import gc

def extract_text_from_pdf(pdf_file):
    try:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + " "
        return text.strip() if text else "No text found in PDF"
    except Exception as e:
        return f"Error: Failed to read PDF"

def scrape_url_content(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
    except Exception as e:
        return f"Error: Failed to fetch URL"
    
    try:
        extracted = trafilatura.extract(response.text)
        if extracted and len(extracted) > 100:
            return extracted
    except:
        pass
    
    try:
        doc = Document(response.text)
        content = doc.summary()
        if content and len(content) > 100:
            return content
    except:
        pass
    
    try:
        soup = BeautifulSoup(response.text, 'html.parser')
        for script in soup(["script", "style"]):
            script.decompose()
        text = soup.get_text()
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)
        return text if text else "No content extracted"
    except:
        return "Error: Failed to extract content"

def extract_audio_transcript(audio_file):
    """Extract transcript from audio - FIXED file handling"""
    try:
        import speech_recognition as sr
        from pydub import AudioSegment
        
        # Create unique temp file name
        timestamp = int(time.time() * 1000000)
        temp_dir = tempfile.gettempdir()
        
        mp3_path = os.path.join(temp_dir, f"audio_{timestamp}.mp3")
        wav_path = os.path.join(temp_dir, f"audio_{timestamp}.wav")
        
        # Save uploaded file
        with open(mp3_path, 'wb') as f:
            f.write(audio_file.read())
        
        # Load audio
        try:
            audio = AudioSegment.from_mp3(mp3_path)
        except Exception as e:
            # Try as WAV if MP3 fails
            try:
                audio = AudioSegment.from_wav(mp3_path)
            except:
                # Try auto-detect
                audio = AudioSegment.from_file(mp3_path)
        
        # Export to WAV
        audio.export(wav_path, format="wav")
        
        # Force garbage collection to release MP3
        del audio
        gc.collect()
        
        recognizer = sr.Recognizer()
        recognizer.energy_threshold = 4000
        
        # Split into 30-second chunks
        chunk_duration = 30000
        full_text = ""
        
        try:
            with sr.AudioFile(wav_path) as source:
                audio_data = recognizer.record(source)
            
            # Try languages in order
            text = ""
            for lang in ["en-US", "te-IN", "hi-IN"]:
                try:
                    text = recognizer.recognize_google(audio_data, language=lang)
                    if text:
                        break
                except sr.UnknownValueError:
                    continue
                except sr.RequestError:
                    return "Could not reach speech service - try again later"
            
            full_text = text if text else "No speech detected"
            
        except Exception as e:
            full_text = "Could not process audio - ensure it contains clear speech"
        
        finally:
            # Cleanup - force delete files
            time.sleep(0.2)
            for fpath in [mp3_path, wav_path]:
                if os.path.exists(fpath):
                    try:
                        os.chmod(fpath, 0o777)
                        os.remove(fpath)
                    except:
                        pass
        
        return full_text
        
    except ImportError:
        return "Error: Required libraries missing - run pip install -r requirements.txt"
    except Exception as e:
        return "Audio processing failed - try MP3 or WAV files"

def validate_url(url):
    pattern = r'^https?://[a-zA-Z0-9-._~:/?#\[\]@!$&\'()*+,;=]+$'
    return bool(re.match(pattern, url))

def is_youtube_url(url):
    return 'youtube' in url.lower() or 'youtu.be' in url.lower()
