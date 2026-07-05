from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
import json

# Gemini
from .gemini import ask_gemini
from django.views.decorators.http import require_POST
# Models
from .models import Chat, Message, Bookmark


@login_required(login_url="login")
def home(request):
    """
    Display chatbot homepage with chat history.
    """

    # Get all chats of logged-in user
    chats = Chat.objects.filter(
        user=request.user
    ).order_by("-created_at")

    # Get active chat from session
    active_chat_id = request.session.get("chat_id")

    messages = []

    if active_chat_id:

        try:

            active_chat = Chat.objects.get(
                id=active_chat_id,
                user=request.user
            )

            messages = Message.objects.filter(
                chat=active_chat
            ).order_by("created_at")

        except Chat.DoesNotExist:

            request.session.pop("chat_id", None)

    context = {
        "chats": chats,
        "messages": messages,
        "active_chat_id": active_chat_id,
    }

    return render(
        request,
        "chatbot/index.html",
        context
    )


@login_required(login_url="login")
def open_chat(request, chat_id):
    """
    Open an existing conversation.
    """

    # Selected chat
    chat = Chat.objects.get(
        id=chat_id,
        user=request.user
    )

    # Save active chat in session
    request.session["chat_id"] = chat.id

    # Sidebar chats
    chats = Chat.objects.filter(
        user=request.user
    ).order_by("-created_at")

    # Conversation messages
    messages = Message.objects.filter(
        chat=chat
    ).order_by("created_at")

    context = {
        "chats": chats,
        "messages": messages,
        "active_chat_id": chat.id,
    }

    return render(
        request,
        "chatbot/index.html",
        context
    )


@login_required(login_url="login")
def chat(request):
    """
    Receive user message,
    send to Gemini,
    save conversation,
    return AI response.
    """

    if request.method == "POST":

        data = json.loads(request.body)

        user_message = data.get("message")

        # Current chat
        chat_id = request.session.get("chat_id")

        # Create chat if needed
        if chat_id is None:

            chat = Chat.objects.create(
                user=request.user,
                title=user_message[:50]
            )

            request.session["chat_id"] = chat.id

        else:

            chat = Chat.objects.get(
                id=chat_id
            )

        # Save user message
        # Save user message
        user_message_obj = Message.objects.create(
        chat=chat,
        sender="user",
        content=user_message
        )

# Ask Gemini
        ai_reply = ask_gemini(user_message)

# Save AI reply
    ai_message_obj = Message.objects.create(
    chat=chat,
    sender="assistant",
    content=ai_reply
)

    return JsonResponse({
    "response": ai_reply,
    "user_message_id": user_message_obj.id,
    "assistant_message_id": ai_message_obj.id,
})

    return JsonResponse({
        "error": "Invalid request"
    }, status=400)


@login_required(login_url="login")
def new_chat(request):
    """
    Start a new conversation.
    """

    request.session.pop("chat_id", None)

    return redirect("home")

@require_POST
@login_required(login_url="login")
def toggle_bookmark(request):
    """
    Add or remove a bookmark for a message.
    """

    data = json.loads(request.body)
    message_id = data.get("message_id")

    try:
        message = Message.objects.get(id=message_id)

        bookmark = Bookmark.objects.filter(
            user=request.user,
            message=message
        )

        if bookmark.exists():

            bookmark.delete()

            return JsonResponse({
                "status": "removed"
            })

        Bookmark.objects.create(
            user=request.user,
            message=message
        )

        return JsonResponse({
            "status": "saved"
        })

    except Message.DoesNotExist:

        return JsonResponse({
            "status": "error"
        }, status=404)
    
@login_required(login_url="login")
def bookmarks(request):
    """
    Display all bookmarked messages.
    """

    bookmarks = Bookmark.objects.filter(
        user=request.user
    ).select_related(
        "message",
        "message__chat"
    ).order_by("-created_at")

    return render(
        request,
        "chatbot/bookmarks.html",
        {
            "bookmarks": bookmarks
        }
    )
def logout_view(request):
    logout(request)
    return redirect("login")