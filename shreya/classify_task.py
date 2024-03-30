
import google.generativeai as genai


genai.configure(api_key="AIzaSyCUuqLqywywm3WC1RXcQlV7Iqx_53a1oHE")

# Set up the model
generation_config = {
    "temperature": 0.9,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
}

safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE",
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE",
    },
]

model = genai.GenerativeModel(
    model_name="gemini-pro",
    generation_config=generation_config,
    safety_settings=safety_settings,
)

def chat():
    input_string = input("Hello User!: ")

    classification_prompt = [
        f"""
          Given a raw text input to a language model select the task best suited for the input, depending on what the user seems to need: 
          'calculator' if the user asks for any mathematical calculations that require a calculator (example: addition, subtraction, multiplication, division, sin, cosine, standard deviation, etc)
          'command' if the user asks to execute a command prompt or a code
          'email' if the user asks to send an email
          'message' if the user asks to send a text message
          'api' if user asks for current news, sports events or the weather
          'calendar' if user asks to edit their schedule (example: add or delete tasks for a day or hour, etc)
          'web' if user specifically asks to search the web for something
          'chat' if none of the above tasks apply
          
          answer in the following format:
          task 
          given user input: {input_string}
          """
    ]

    response = model.generate_content(classification_prompt)

    if "calculator" in response.text:
        print("calculator")

    elif "command" in response.text:
        print("command")
        
    elif "email" in response.text:
        print("email")
        
    elif "message" in response.text:
        print("message")
        
    elif "api" in response.text:
        print("api")
        
    elif "calendar" in response.text:
        print("calendar")
    
    elif "web" in response.text:
        print("web")
        
    elif "chat" in response.text:
        print("chat")

    else:
        return "Invalid response"

chat()