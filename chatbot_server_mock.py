from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/chat', methods=['POST', 'OPTIONS'])
def chatbot():
    if request.method == 'OPTIONS':
        response = jsonify({'message': 'Preflight request'})
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type")
        response.headers.add("Access-Control-Allow-Methods", "POST, OPTIONS")
        return response

    try:
        # Extract user message
        req_data = request.get_json()
        user_message = req_data.get('message', '').lower()

        # Handcoded responses
        if "how do i return" in user_message or "return item" in user_message:
            response_text = (
                "To return an item, visit your orders page and select the item you want to return. "
                "You can find more details here: https://www.amazon.com/gp/help/customer/display.html?nodeId=201819200"
            )
        elif "track my order" in user_message or "delivery update" in user_message:
            response_text = (
                "For delivery updates, go to 'Your Orders' and track your package. More info here: "
                "https://www.amazon.com/gp/help/customer/display.html?nodeId=201117780"
            )
        elif "warranty information" in user_message or "product warranty" in user_message:
            response_text = (
                "Warranty information can be found on the product's detail page under 'Warranty and Support.' "
                "More details: https://www.amazon.com/gp/help/customer/display.html?nodeId=202194050"
            )
        elif "find manual" in user_message or "product manual" in user_message:
            response_text = (
                "You can find product manuals on the product page under 'Product Information.' General help: "
                "https://www.amazon.com/gp/help/customer/display.html?nodeId=200285450"
            )
        else:
            response_text = (
                "I'm sorry, I didn't understand that. You can check the Amazon help page here: "
                "https://www.amazon.com/gp/help/customer/display.html"
            )

        return jsonify({"response": response_text})

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"response": "There was an error. Please try again later."}), 500

if __name__ == '__main__':
    app.run(port=5000, debug=True)
