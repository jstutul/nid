from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import fitz
import io
import pytesseract
from PIL import Image,ImageEnhance
import os 

def cropImage(pdf_file, w, h, nid):
    doc = fitz.open(stream=pdf_file, filetype="pdf")
    page = doc.load_page(0)
    pix = page.get_pixmap()
    left = 611
    top = 265
    right = 726
    bottom = 296
    cropped_image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    cropped_image = cropped_image.crop((left, top, right, bottom))

    # Resize the cropped image to desired dimensions
    desired_width = 240  # Adjust as needed
    desired_height = 80  # Adjust as needed
    cropped_image = cropped_image.resize((desired_width, desired_height), resample=Image.LANCZOS)

    # Enhance the image (optional)
    enhancer = ImageEnhance.Contrast(cropped_image)
    cropped_image = enhancer.enhance(2.0)  # Increase contrast, adjust as needed
    image_name = f"images/photo_{nid}_1.png"
    cropped_image.save(image_name)

    doc.close()

    return image_name


def Home(request):
    data = {
        "status": True,
        "message": "Hello Api"
    }
    return JsonResponse(data)

def crop_image(image_path, position):
    image = Image.open(image_path)
    cropped_image = image.crop(position)
    return cropped_image

@csrf_exempt
def PdfToText(request):
    if request.method == 'POST' and request.FILES['pdf']:
        pdf_file = request.FILES['pdf']
        pdf_data = pdf_file.read()
        pdf_document = fitz.open(stream=pdf_data, filetype="pdf")

        # Create a directory to save the images
        output_directory = 'output_images'
        os.makedirs(output_directory, exist_ok=True)

        filename = 'tutul'
        image_paths = []

        # Iterate over each page in the PDF document
        for page_number in range(len(pdf_document)):
            page = pdf_document[page_number]
            pixmap = page.get_pixmap()
            img = Image.frombytes("RGB", [pixmap.width, pixmap.height], pixmap.samples)
            image_path = os.path.join(output_directory, f'{filename}_{page_number + 1}.png')
            img.save(image_path)
            image_paths.append(image_path)

        # Crop the first image
        print(image_paths[0])
        first_image_path = image_paths[0]
        cropped_image = crop_image(first_image_path, (198, 69, 350, 90))
        cropped_image.save(f'{output_directory}/nidno.jpg')

        cropped_image = crop_image(first_image_path, (198, 244, 400, 284))
        cropped_image.save(f'{output_directory}/names.jpg')

        cropped_image = crop_image(first_image_path, (198, 381, 400, 420))
        cropped_image.save(f'{output_directory}/parent.jpg')

        return JsonResponse({"status": True, "message": "Success"})
    else:
        return JsonResponse({"status": False, "message": "No PDF file found in request"}, status=400)