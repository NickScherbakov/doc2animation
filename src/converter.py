import os
from PyPDF2 import PdfReader
from docx import Document
import edge_tts
import asyncio
import moviepy.editor as mp
from moviepy.editor import *
import tempfile

class DocumentToAnimation:
    def __init__(self):
        self.VOICE = "en-GB-RyanNeural"
        self.RATE = "+0%"
        self.VOLUME = "+0%"

    async def text_to_speech(self, text, output_file):
        communicate = edge_tts.Communicate(text, self.VOICE, rate=self.RATE, volume=self.VOLUME)
        await communicate.save(output_file)

    def extract_text(self, file_path):
        text = ""
        if file_path.lower().endswith('.pdf'):
            with open(file_path, 'rb') as file:
                reader = PdfReader(file)
                for page in reader.pages:
                    text += page.extract_text()
        elif file_path.lower().endswith('.docx'):
            doc = Document(file_path)
            for para in doc.paragraphs:
                text += para.text + "\n"
        return text

    def create_slide(self, text, duration, size=(1920, 1080)):
        clip = ColorClip(size, col=(255, 255, 255))
        text_clip = TextClip(text, fontsize=30, color='black', size=size)
        return CompositeVideoClip([clip, text_clip.set_pos('center')]).set_duration(duration)

    async def create_presentation(self, input_file, output_file="output.mp4"):
        text = self.extract_text(input_file)
        segments = [s.strip() for s in text.split('\n') if s.strip()]
        temp_audio_files = []
        clips = []
        
        for i, segment in enumerate(segments):
            if not segment:
                continue
                
            temp_audio = tempfile.NamedTemporaryFile(suffix='.mp3', delete=False)
            temp_audio_files.append(temp_audio.name)
            
            await self.text_to_speech(segment, temp_audio.name)
            audio = mp.AudioFileClip(temp_audio.name)
            duration = audio.duration
            
            slide = self.create_slide(segment, duration)
            final_clip = slide.set_audio(audio)
            clips.append(final_clip)

        final_video = concatenate_videoclips(clips)
        final_video.write_videofile(output_file, fps=24)
        
        for temp_file in temp_audio_files:
            os.unlink(temp_file)

def main():
    converter = DocumentToAnimation()
    asyncio.run(converter.create_presentation("input.pdf", "output.mp4"))

if __name__ == "__main__":
    main()
