from flask import Flask, request, jsonify
from google.cloud import dialogflowcx_v3 as dialogflow
from google.oauth2 import service_account

app = Flask(__name__)

# Provide the path to your Google Cloud JSON key file
credentials = service_account.Credentials.from_service_account_file("path\\to\\gcp-key.json")

PROJECT_ID = 'PROJECT_ID'
LOCATION = 'LOCATION'
AGENT_ID = 'AGENT_ID'
LANGUAGE_CODE = 'LANGUAGE_CODE'

@app.route('/chat', methods=['POST', 'OPTIONS'])
def chatbot():
    if request.method == 'OPTIONS':
        response = jsonify({'message': 'Preflight request'})
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type")
        response.headers.add("Access-Control-Allow-Methods", "POST, OPTIONS")
        return response
    
    try:
        # Extract message from the request
        req_data = request.get_json()
        user_message = req_data.get('message', '')

        # Dialogflow session setup
        session_client = dialogflow.SessionsClient(
            credentials=credentials,
            client_options={"api_endpoint": "us-central1-dialogflow.googleapis.com"}
        )
        session_id = '123456'
        session_path = f"projects/{PROJECT_ID}/locations/{LOCATION}/agents/{AGENT_ID}/sessions/{session_id}"

        # Create TextInput and QueryInput
        text_input = dialogflow.TextInput(text=user_message)
        query_input = dialogflow.QueryInput(text=text_input, language_code=LANGUAGE_CODE)

        # Detect user intent
        response = session_client.detect_intent(
            request={
                "session": session_path,
                "query_input": query_input
            }
        )

        # Extract response message from Dialogflow
        if response.query_result.response_messages:
            fulfillment_message = response.query_result.response_messages[0].text.text[0]
        else:
            fulfillment_message = "I'm sorry, I didn't understand that."

        # Return response to the React frontend
        return jsonify({"response": fulfillment_message})

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"response": "There was an error. Please try again later."}), 500

if __name__ == '__main__':
    app.run(port=5000, debug=True)
