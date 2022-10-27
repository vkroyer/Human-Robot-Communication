modes = {
    "Tired": "0",
    "Rubber finish": "0",
    "Rubber duck": "2",
    "Sad": "3",
    "Happy": "4",
    "End": "5"
}

def detect_intent_text(text, project_id="human-robot-com", session_id="123456789", language_code="en-US"):
    """Returns the result of detect intent with text as input.

    Using the same `session_id` between requests allows continuation
    of the conversation."""
    
    if text == "":
        return ""
    
    from google.cloud import dialogflow

    session_client = dialogflow.SessionsClient()

    session = session_client.session_path(project_id, session_id)
    # print(f"Session path: {session}\n")

    text_input = dialogflow.TextInput(text=text, language_code=language_code)

    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )

    print("=" * 20)
    print(f"Query text: {response.query_result.query_text}")
    print(
        f"Detected intent: {response.query_result.intent.display_name} \
            (confidence: {response.query_result.intent_detection_confidence})"
    )
    print(f"Fulfillment text: {response.query_result.fulfillment_text}")
    try:
        mode = modes[response.query_result.intent.display_name]
        return mode
    except KeyError:
        return ""

# print(detect_intent_text("Fuck this shit"))


