# Amazon Customer Support Chatbot

![image](https://github.com/user-attachments/assets/b964e804-b0f5-404b-8f4a-b9fe0164fced)

This project implements a chatbot designed to assist users with common issues related to Amazon products, such as returns, delivery updates, warranties, and manuals. The chatbot is built with a **React frontend** and a **Python Flask backend** to ensure a seamless user experience.

---

## Features

- **Real-Time Chat Interface:** Built using React, the frontend enables users to interact with the chatbot dynamically.
- **Keyword Matching for User Queries:** The backend intelligently matches user questions to provide relevant responses and useful links to Amazon help pages.
- **Fallback Support:** If the chatbot cannot match a query, it provides a general help URL for further assistance.

---

## Project Architecture

### Frontend

The React frontend is implemented with the following features:
- A simple and clean chat interface.
- Toggleable chat window.
- Dynamic updates for user and bot messages.

Setup Instructions:

To begin let's create a front-end client in **React** using Vite. The project will use TypeScript for type safety and general good practices. Run `npm create vite@latest chatbot -- --template react-ts
` in the terminal followed by `cd chatbot` and `npm install`. 
1. Add relevant logo files in the **public** folder
	* **amazon-icon.svg**
	* **logo.png**
2. Edit the content of the **index.html** file
3. Edit the content of the **App.tsx** file
4. Edit the content of the **App.css** file

Then we will create **GCP Project** and **Dialogflow CX Agent** for basic chatbot instance using GCP resources. Finally, we will create **Python** server API that will take user input, send it to Dialogflow CX, and return the response.

1. Create new project and name it **amazon-chatbot**
2. Activate required APIs by navigating to **APIs & Services > Library** in the left-hand menu and the enabling the following services:
	* **Dialogflow API**
	* **Cloud Functions API**
	* **Cloud Firestore API (Optional)**
3. Setup Dialogflow CX Agent 
	* Go to https://dialogflow.cloud.google.com/cx/projects
	* Select the previously created project **amazon-chatbot**
	* Create new **agent**
	* Click the **Create your own** template and give it name **AmazonSupportBot**
4. Create Intents that will be used to determine what the user wants
	* In the left-hand menu, under **Manage** section click on **Intents**
	* Click **Create** and enter information for the intent
		* **Name**: *Return Policy*
		* **Labels**: *head intent*
		* **Description**: Add brief description
		* **Training phrases**: Add relevant training phrases such as *Where is my package* and *Track my order*
		* Click on **Create**
	* Repeat this process for the other intent you want to add
5. Link Intents to the main flow of the chat, so that when a user asks for refunds the relevant response is given
	* Go to the **Build** tab 
	* Click on the **Start Page** under the **Pages** tab
	* Click the **+** icon on the **Routes** tab and fill the required information
		* **Description**: Describe the function of the transition route
		* **Intent**: Select the intent previously created
		* Under **Fulfillment** add content for the **Agent responses** which is essentially what the chatbot will reply when the intent is matched
		* Click **Save**
6. Create **chatbot_server.py** Python server that will take user input, send it to Dialogflow CX, and return the response
	* Generate Google Cloud JSON key file
	* Create the python file in the same directory as the JSON key file and paste the below:
	* Replace the **path\to\gcp-key.json**, **PROJECT_ID**, **LOCATION**, **AGENT_ID**, and **LANGUAGE_CODE** constants.
7. Test the chatbot and make sure that it works
