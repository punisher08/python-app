from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from openai import OpenAI
from django.conf import settings
import json

client = OpenAI(api_key=settings.OPENAI_API_KEY)

@csrf_exempt
def business_assistant(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user_message = data.get("message", "")
        if not user_message:
            return JsonResponse({"reply": "Please type a message."})

        system_prompt = """
        You are a professional assistant for a company that makes custom wooden doors and furniture.
        Be polite, concise, and informative. You can explain services, collect lead details, and assist with product info.
        """

        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message},
                ]
            )
            reply = response.choices[0].message.content
            return JsonResponse({"reply": reply})
        except Exception as e:
            return JsonResponse({"reply": f"Error: {str(e)}"})

    return JsonResponse({"reply": "Invalid request."})
