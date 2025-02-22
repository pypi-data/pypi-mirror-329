from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import os
from .utils import extract_text, parse_text_to_dict


@csrf_exempt
def ocr_view(request):
    if request.method == "POST" and request.FILES.get("image"):
        image = request.FILES["image"]
        image_path = f"/tmp/{image.name}"

        with open(image_path, "wb") as f:
            f.write(image.read())

        raw_text = extract_text(image_path)
        os.remove(image_path)

        mappings_json = request.POST.get("mappings")
        if mappings_json:
            try:
                request_data = json.loads(mappings_json)
                structured_data = parse_text_to_dict(raw_text, request_data)
                return JsonResponse({"raw_text": raw_text, "structured_data": structured_data})
            except json.JSONDecodeError:
                return JsonResponse({"error": "Invalid mappings format"}, status=400)

        return JsonResponse({"raw_text": raw_text})

    return JsonResponse({"error": "Invalid request"}, status=400)
