import json
import logging
from tqdm import tqdm
from utils import load_config, save_animation
import cv2
import numpy as np

class DocumentConversionError(Exception):
    """Custom exception for document conversion errors."""
    pass

class DocumentToAnimation:
    def __init__(self, config_path):
        try:
            self.config = load_config(config_path)
            if 'output_path' not in self.config:
                raise DocumentConversionError("Configuration missing 'output_path'")
        except Exception as e:
            logging.error(f"Failed to load configuration: {e}")
            raise DocumentConversionError(f"Failed to load configuration: {e}")

    def apply_fade_in_effect(self, frame):
        """Apply fade-in effect to the frame and return list of transition frames."""
        logging.info("Applying fade-in effect")
        transition_frames = []
        height, width, _ = frame.shape
        fade_in_frame = np.zeros_like(frame)
        
        for alpha in np.linspace(0, 1, num=30):
            blended_frame = cv2.addWeighted(frame, alpha, fade_in_frame, 1 - alpha, 0)
            transition_frames.append(blended_frame)
            logging.debug(f"Alpha: {alpha}, Frame shape: {blended_frame.shape}")
            
        logging.info("Fade-in effect applied successfully")
        return transition_frames

    def convert(self, document_path):
        try:
            frames = self.extract_frames(document_path)
            for frame in tqdm(frames, desc="Converting frames"):
                self.apply_fade_in_effect(frame)
            save_animation(frames, self.config['output_path'])
        except Exception as e:
            logging.error(f"Conversion failed: {e}")
            raise DocumentConversionError(f"Conversion failed: {e}")

    def extract_frames(self, document_path):
        # Extract frames from the document
        # ...implementation...
        frames = []
        try:
            with open(document_path, 'r') as file:
                document_data = json.load(file)
                for page in document_data.get('pages', []):
                    frames.append(self.process_page(page))
        except Exception as e:
            logging.error(f"Failed to extract frames: {e}")
            raise DocumentConversionError(f"Failed to extract frames: {e}")
        return frames

    def process_page(self, page):
        # Process a single page and return a frame
        frames = []
        doc = self.load_document(page)
        for paragraph in doc.paragraphs:
            if paragraph.text.strip():
                frames.extend(self.process_page(paragraph.text))
            else:
                raise DocumentConversionError("Unsupported document format")
        return frames

    def process_page(self, text):
        """Process a single page/paragraph and return frames."""
        from utils import split_into_segments, clean_text
        import numpy as np
        import cv2
        
        frames = []
        cleaned_text = clean_text(text)
        segments = split_into_segments(cleaned_text)
        
        # Создаем базовое изображение
        height, width = 720, 1280  # HD resolution
        background_color = (255, 255, 255)  # Белый фон
        
        for segment in segments:
            # Создаем чистый кадр
            frame = np.ones((height, width, 3), dtype=np.uint8) * background_color
            
            # Настраиваем параметры текста
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 1.0
            font_color = (0, 0, 0)  # Черный текст
            thickness = 2
            line_spacing = 40
            
            # Разбиваем текст на строки
            words = segment.split()
            lines = []
            current_line = []
            
            for word in words:
                current_line.append(word)
                text_size = cv2.getTextSize(' '.join(current_line), font, font_scale, thickness)[0]
                
                if text_size[0] > width - 100:  # Отступ от краев
                    lines.append(' '.join(current_line[:-1]))
                    current_line = [word]
            
            if current_line:
                lines.append(' '.join(current_line))
            
            # Отрисовываем текст
            y_position = height // 3  # Начинаем с трети высоты
            for line in lines:
                text_size = cv2.getTextSize(line, font, font_scale, thickness)[0]
                x_position = (width - text_size[0]) // 2  # Центрируем текст
                
                cv2.putText(frame, line, (x_position, y_position),
                           font, font_scale, font_color, thickness)
                y_position += line_spacing
            
            frames.append(frame)
            
        return frames