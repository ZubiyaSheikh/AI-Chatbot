from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
import json

# Import Gemini function
from .gemini import ask_gemini

# Import database models
from .models import Chat, Message


@login_required(login_url="login")
def home(request):
    """
    Display chatbot homepage.
    """
    return render(request, "chatbot/index.html")


@login_required(login_url="login")
def chat(request):
    """
    Receive user's message,
    save conversation,
    send it to Gemini,
    and return AI response.
    """

    if request.method == "POST":

        # Read JSON sent by JavaScript
        data = json.loads(request.body)

        user_message = data.get("message")

        # Get current chat from session
        chat_id = request.session.get("chat_id")

        # Create a new chat if one doesn't exist
        if chat_id is None:

            chat = Chat.objects.create(
                user=request.user,
                title=user_message[:50]
            )

            # Save chat id in session
            request.session["chat_id"] = chat.id

        else:
            # Load existing chat
            chat = Chat.objects.get(id=chat_id)

        # Save user's message
        Message.objects.create(
            chat=chat,
            sender="user",
            content=user_message
        )

        # Ask Gemini
        ai_reply = ask_gemini(user_message)

        # Save AI response
        Message.objects.create(
            chat=chat,
            sender="assistant",
            content=ai_reply
        )

        print("\n========== AI RESPONSE ==========")
        print(ai_reply)
        print("=================================\n")

        # Return AI response
        return JsonResponse({
            "response": ai_reply
        })

    return JsonResponse({
        "error": "Invalid Request"
    }, status=400)


@login_required(login_url="login")
def new_chat(request):
    """
    Start a new conversation.
    """

    # Remove current chat from session
    request.session.pop("chat_id", None)

    return redirect("home")