import cv2
import easyocr
from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from .forms import ImageUploadForm
from .models import UploadedImage
from PIL import Image
import numpy as np
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from django.conf import settings
import os

reader = easyocr.Reader(['es'])

def ocr_image(image_path):
    try:
        pil_image = Image.open(image_path)
        open_cv_image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
        gray_image = cv2.cvtColor(open_cv_image, cv2.COLOR_BGR2GRAY)
        gray_image = cv2.resize(gray_image, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
        gray_image = cv2.GaussianBlur(gray_image, (5, 5), 0)
        threshold_image = cv2.adaptiveThreshold(gray_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                                cv2.THRESH_BINARY, 31, 2)
        result = reader.readtext(threshold_image)
        text = ' '.join([res[1] for res in result])
        return text
    except Exception as e:
        print(f"Error en OCR: {e}")

def generate_wordcloud(text, image_name):
    stopwords = set([
        "el", "la", "un", "una", "pero", "como", "para", "sin", "las", "los",
        "y", "o", "a", "de", "que", "en", "se", "con", "por", "su", "es", "al",
        "lo", "del", "más", "si", "no", "me", "mi", "te", "tu", "sus", "ser", 
        "son", "ha", "ya", "esta", "este", "estos", "estas", "eso", "esa", 
        "esas", "esos", "esa"
    ])

    wordcloud = WordCloud(width=800, height=400, background_color='white', stopwords=stopwords).generate(text)
    wordcloud_path = f'wordclouds/{os.path.splitext(image_name)[0]}_wordcloud.png'
    wordcloud_full_path = os.path.join(settings.MEDIA_ROOT, wordcloud_path)
    
    # Crear el directorio si no existe
    os.makedirs(os.path.dirname(wordcloud_full_path), exist_ok=True)
    
    wordcloud.to_file(wordcloud_full_path)
    return wordcloud_path

def upload_image(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['image']
            if UploadedImage.objects.filter(image__icontains=uploaded_file.name).exists():
                return render(request, 'ocr_app/upload.html', {'form': form, 'error': 'Esta imagen ya ha sido subida.'})
            
            uploaded_image = form.save(commit=False)
            fs = FileSystemStorage()
            filename = fs.save(uploaded_file.name, uploaded_file)
            image_path = fs.path(filename)
            extracted_text = ocr_image(image_path)
            uploaded_image.extracted_text = extracted_text

            wordcloud_path = generate_wordcloud(extracted_text, uploaded_file.name)
            uploaded_image.wordcloud = wordcloud_path
            uploaded_image.save()

            wordcloud_url = os.path.join(settings.MEDIA_URL, wordcloud_path)
            return render(request, 'ocr_app/result.html', {'text': extracted_text, 'wordcloud_url': wordcloud_url})
    else:
        form = ImageUploadForm()
    images = UploadedImage.objects.all()
    return render(request, 'ocr_app/upload.html', {'form': form, 'images': images})


def delete_image(request, image_id):
    image = UploadedImage.objects.get(id=image_id)
    image.delete()
    return redirect('upload_image')
