import os
import requests
import time

# ==========================================
# TELEGRAM BOT TOKEN
# ==========================================

TOKEN = "8281681546:AAERQQ3h8md7kZPClfJsPTIp4ku0IJ3_Lao"

API = f"https://api.telegram.org/bot{TOKEN}/"


# ==========================================
# TELEGRAM API
# ==========================================

def telegram(method, data=None):
    try:
        response = requests.post(
            API + method,
            data=data or {},
            timeout=60
        )

        return response.json()

    except Exception as e:
        print("API Error:", e)
        return {}


# ==========================================
# SEND MESSAGE
# ==========================================

def send_message(chat_id, text, keyboard=None):

    data = {
        "chat_id": chat_id,
        "text": text
    }

    if keyboard:
        data["reply_markup"] = keyboard

    return telegram(
        "sendMessage",
        data
    )


# ==========================================
# MAIN MENU
# ==========================================

def main_menu():

    return {
        "inline_keyboard": [

            [
                {
                    "text": "📧 Create Temp Email",
                    "callback_data": "create"
                }
            ],

            [
                {
                    "text": "📥 Inbox",
                    "callback_data": "inbox"
                },
                {
                    "text": "🔄 Refresh",
                    "callback_data": "refresh"
                }
            ],

            [
                {
                    "text": "🗑️ Delete Email",
                    "callback_data": "delete"
                }
            ],

            [
                {
                    "text": "ℹ️ Help",
                    "callback_data": "help"
                }
            ]

        ]
    }


# ==========================================
# START
# ==========================================

def start_bot(chat_id):

    text = (
        "👋 Welcome!\n\n"
        "📧 TEMP MAIL BOT\n\n"
        "Create a temporary email address "
        "and check incoming messages.\n\n"
        "👇 Select an option:"
    )

    send_message(
        chat_id,
        text,
        main_menu()
    )


# ==========================================
# HELP
# ==========================================

def help_menu(chat_id):

    text = (
        "ℹ️ HELP\n\n"
        "📧 Create Temp Email\n"
        "Create a temporary email address.\n\n"
        "📥 Inbox\n"
        "View received emails.\n\n"
        "🔄 Refresh\n"
        "Check for new messages.\n\n"
        "🗑️ Delete Email\n"
        "Delete your current temporary email."
    )

    send_message(
        chat_id,
        text,
        main_menu()
    )


# ==========================================
# MESSAGE HANDLER
# ==========================================

def handle_message(message):

    chat_id = message["chat"]["id"]

    text = message.get(
        "text",
        ""
    )

    if text == "/start":

        start_bot(
            chat_id
        )

    elif text == "/help":

        help_menu(
            chat_id
        )

    else:

        send_message(
            chat_id,
            "👇 Please select an option:",
            main_menu()
        )


# ==========================================
# BUTTON HANDLER
# ==========================================

def handle_callback(callback):

    callback_id = callback["id"]

    chat_id = callback[
        "message"
    ]["chat"]["id"]

    action = callback["data"]

    # Remove Telegram loading state
    telegram(
        "answerCallbackQuery",
        {
            "callback_query_id":
                callback_id
        }
    )

    # -----------------------------
    # CREATE EMAIL
    # -----------------------------

    if action == "create":

        send_message(
            chat_id,
            "📧 CREATE TEMP EMAIL\n\n"
            "⏳ Email provider is not connected yet.\n\n"
            "Next step will connect the "
            "temporary-email API."
        )

    # -----------------------------
    # INBOX
    # -----------------------------

    elif action == "inbox":

        send_message(
            chat_id,
            "📥 INBOX\n\n"
            "📭 No temporary email has "
            "been created yet.",
            main_menu()
        )

    # -----------------------------
    # REFRESH
    # -----------------------------

    elif action == "refresh":

        send_message(
            chat_id,
            "🔄 Checking inbox...\n\n"
            "No email account is connected yet.",
            main_menu()
        )

    # -----------------------------
    # DELETE
    # -----------------------------

    elif action == "delete":

        send_message(
            chat_id,
            "🗑️ DELETE EMAIL\n\n"
            "You don't have an active "
            "temporary email.",
            main_menu()
        )

    # -----------------------------
    # HELP
    # -----------------------------

    elif action == "help":

        help_menu(
            chat_id
        )


# ==========================================
# BOT LOOP
# ==========================================

def run_bot():

    print(
        "================================"
    )

    print(
        "      TEMP MAIL TELEGRAM BOT"
    )

    print(
        "================================"
    )

    print(
        "Connecting to Telegram..."
    )

    # Test connection

    result = telegram(
        "getMe"
    )

    if not result.get("ok"):

        print("")
        print(
            "❌ Telegram connection failed."
        )

        print(
            "Check your bot token."
        )

        return

    bot_info = result[
        "result"
    ]

    username = bot_info.get(
        "username",
        "Unknown"
    )

    print("")
    print(
        "✅ Bot connected!"
    )

    print(
        "Bot:",
        "@" + username
    )

    print("")
    print(
        "Waiting for messages..."
    )

    print("")

    offset = None

    # ======================================
    # LONG POLLING
    # ======================================

    while True:

        try:

            data = {
                "timeout": 50
            }

            if offset is not None:

                data[
                    "offset"
                ] = offset

            result = telegram(
                "getUpdates",
                data
            )

            if not result.get("ok"):

                time.sleep(3)

                continue

            updates = result.get(
                "result",
                []
            )

            for update in updates:

                offset = (
                    update["update_id"]
                    + 1
                )

                # Normal message

                if "message" in update:

                    handle_message(
                        update["message"]
                    )

                # Button callback

                elif "callback_query" in update:

                    handle_callback(
                        update["callback_query"]
                    )

        except KeyboardInterrupt:

            print("")
            print(
                "Bot stopped."
            )

            break

        except Exception as e:

            print(
                "Loop Error:",
                e
            )

            time.sleep(3)


# ==========================================
# START PROGRAM
# ==========================================

if __name__ == "__main__":

    if TOKEN == "12345":

        print("")
        print(
            "⚠️ TEST TOKEN DETECTED"
        )

        print(
            "Replace 12345 with your "
            "real BotFather token."
        )

        print("")

    else:

        run_bot()
