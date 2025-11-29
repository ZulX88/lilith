import json
import threading

import requests
import websocket


def create_conversation_id():
    response = requests.post("https://copilot.microsoft.com/c/api/conversations").json()
    return response["id"]


def send_copilot_request(text, model : str = "chat"):
    url = "wss://copilot.microsoft.com/c/api/chat?api-version=2&features=-,ncedge,edgepagecontext&setflight=-,ncedge,edgepagecontext&ncedge=1"

    conversationID = create_conversation_id()

    payload = {
        "event": "send",
        "content": [
            {"type": "text", "text": text}  # "Halo! Aku chika, bisa kenalan denganmu??"
        ],
        "conversationId": conversationID,
        "mode":model
    }

    # Global state
    full_response = {
        "conversationId": conversationID,
        "messageId": None,
        "text": "",
        "suggestions": [],
    }

    has_done = False
    has_suggestions = False
    done_event = threading.Event()

    def on_message(ws, message):
        nonlocal has_done, has_suggestions
        data = json.loads(message)

        if data.get("event") == "startMessage":
            full_response["messageId"] = data.get("messageId")

        elif (
            data.get("event") == "appendText"
            and data.get("messageId") == full_response["messageId"]
        ):
            full_response["text"] += data.get("text", "")

        elif data.get("event") == "done":
            has_done = True

        elif data.get("event") == "suggestedFollowups":
            full_response["suggestions"] = data.get("suggestions", [])
            has_suggestions = True
            ws.close()
            done_event.set()  # Signal that we're done

    def on_open(ws):
        ws.send(json.dumps(payload))

    def on_error(ws, error):
        print("❌ Error:", error)
        done_event.set()

    def on_close(ws, close_status_code, close_msg):
        pass

    ws = websocket.WebSocketApp(
        url,
        # header=headers,
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close,
    )

    def run_ws():
        ws.run_forever()

    thread = threading.Thread(target=run_ws)
    thread.start()

    done_event.wait()

    return json.dumps(full_response, indent=2, ensure_ascii=False)

print(send_copilot_request("Hai copilot"))