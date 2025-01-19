# doc2animation# Document to Animation Converter

Конвертер документов PDF/DOCX в анимированные презентации с озвучиванием.

## Возможности

- Конвертация PDF и DOCX документов в анимированные презентации
- Автоматическое озвучивание текста с помощью edge-tts
- Создание слайдов с анимированным текстом
- Поддержка настройки параметров озвучки и анимации

## Установка

1. Клонируйте репозиторий:
    ```bash
    git clone https://github.com/NickScherbakov/doc2animation.git
    cd doc2animation
    ```

2. Установите зависимости:
    ```bash
    pip install -r requirements.txt
    ```

## Использование

Пример использования скрипта для конвертации документа в анимацию:

```python
from src.converter import DocumentToAnimation
import asyncio

converter = DocumentToAnimation()
asyncio.run(converter.create_presentation("input.pdf", "output.mp4"))