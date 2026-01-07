import os
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from openai import OpenAI
from .models import ChatSession, ChatMessage
import json, uuid

client = OpenAI(api_key=settings.API_KEY)

KNOWLEDGE_PATH = os.path.join(settings.BASE_DIR, "assistant", "knowledge.json")

def load_knowledge():
    try:
        with open(KNOWLEDGE_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}
    

@csrf_exempt
def business_assistant(request):
    """
    Handles incoming messages from the chatbot frontend.
    Creates/loads a ChatSession and stores user/assistant messages.
    """
    if request.method == "POST":
        data = json.loads(request.body)
        user_message = data.get("message", "")
        language = data.get("language", "English")
        session_id = data.get("session_id")

        # Ensure message exists
        if not user_message:
            return JsonResponse({"reply": "Please type a message."})

        # Create or get existing chat session
        if not session_id:
            session_id = str(uuid.uuid4())
            chat_session = ChatSession.objects.create(session_id=session_id, language=language)
        else:
            chat_session, _ = ChatSession.objects.get_or_create(session_id=session_id)

        # Save user message
        ChatMessage.objects.create(
            session=chat_session,
            sender="user",
            message=user_message,
        )
        knowledge_data = load_knowledge()

        # System prompt
        system_prompt = f"""
        You are a professional assistant for Ignacio Furnitures.
        Use the following details to answer user inquiries accurately:
        {json.dumps(knowledge_data, indent=2)}.

        Be polite, professional, and concise.
        Do not include <html>, <head>, <meta>, or <title> tags.
        If the user asks for product details or pricing, refer to the above information.
        If you are unsure, politely suggest that they contact the sales team for confirmation.
        Respond in {language}.

        Respond in HTML format with structured and readable text (e.g., <b>Product:</b>, <ul><li>...</li></ul>).

        Example response style:
        <p><b>Product:</b> Panel Door<br>
        <b>Price Range:</b> ₱5,000 – ₱8,000<br>
        <b>Delivery:</b> Free within Tarlac City</p>
        <p>Would you like to know available designs or customization options?</p>
        """

        # Context from previous messages
        previous_messages = []
        for msg in chat_session.messages.all().order_by("timestamp"):
            previous_messages.append({
                "role": "user" if msg.sender == "user" else "assistant",
                "content": msg.message
            })

        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    *previous_messages,
                    {"role": "user", "content": user_message},
                ],
            )

            reply = response.choices[0].message.content

            # Save assistant response (replace 'bot' → 'assistant')
            ChatMessage.objects.create(
                session=chat_session,
                sender="assistant",
                message=reply,
            )

            return JsonResponse({"reply": reply, "session_id": session_id})

        except Exception as e:
            return JsonResponse({"reply": f"Error: {str(e)}", "session_id": session_id})

    return JsonResponse({"reply": "Invalid request."})


@csrf_exempt
def get_conversation(request):
    """
    Returns full conversation for the active session.
    If no session exists, creates a new one.
    """
    session_id = request.session.get("chat_session_id")

    if not session_id:
        # Generate new session if none exists
        session_id = str(uuid.uuid4())
        chat_session = ChatSession.objects.create(session_id=session_id)
        request.session["chat_session_id"] = session_id
    else:
        chat_session, _ = ChatSession.objects.get_or_create(session_id=session_id)

    # Load messages
    conversation = [
        {"sender": msg.sender, "message": msg.message, "timestamp": msg.timestamp.isoformat()}
        for msg in chat_session.messages.all().order_by("timestamp")
    ]

    return JsonResponse({
        "session_id": session_id,
        "conversation": conversation
    })


@csrf_exempt
def end_chat_session(request):
    """Ends current chat session (keeps data, creates a new session)."""
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            old_session_id = data.get("session_id")
            language = data.get("language", "English")

            # Confirm old session exists (optional)
            try:
                ChatSession.objects.get(session_id=old_session_id)
            except ChatSession.DoesNotExist:
                pass

            # Create new session
            new_session_id = str(uuid.uuid4())
            ChatSession.objects.create(session_id=new_session_id, language=language)

            return JsonResponse({
                "status": "success",
                "message": "Chat ended. A new session has been started.",
                "new_session_id": new_session_id
            })
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})

    return JsonResponse({"status": "error", "message": "Invalid request method."})
