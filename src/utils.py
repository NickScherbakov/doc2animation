# src/utils.py

def split_into_segments(text, max_length=100):
    """Split text into reasonable segments for presentation."""
    segments = []
    current_segment = []
    current_length = 0
    
    for sentence in text.split('.'):
        sentence = sentence.strip()
        if not sentence:
            continue
            
        if current_length + len(sentence) > max_length:
            if current_segment:
                segments.append(' '.join(current_segment))
            current_segment = [sentence]
            current_length = len(sentence)
        else:
            current_segment.append(sentence)
            current_length += len(sentence)
            
    if current_segment:
        segments.append(' '.join(current_segment))
        
    return segments

def clean_text(text):
    """Clean and normalize text for presentation."""
    import re
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    # Remove special characters
    text = re.sub(r'[^\w\s.,!?-]', '', text)
    return text.strip()

def create_temp_file():
    """Create a temporary file and ensure it will be cleaned up."""
    import tempfile
    return tempfile.NamedTemporaryFile(suffix='.mp3', delete=False)

def load_config(config_path):
    """Load configuration from a file."""
    import json
    with open(config_path, 'r') as file:
        return json.load(file)

def save_animation(frames, output_path):
    """Save frames as an animation to the specified output path."""
    # ...implementation...
    pass

class DocumentConversionError(Exception):
    """Custom exception for document conversion errors."""
    pass