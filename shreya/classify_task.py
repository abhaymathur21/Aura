
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
          if the user asks for any mathematical calculations that require a calculator (example: addition, subtraction, multiplication, division, sin, cosine, standard deviation, etc), 
            identify operators and operation
          answer format: 'calculator', operators, operation
          
          if the user asks to execute a command prompt or a code:
          answer format: 'command_execute', input_string
          
          if the user asks to send an email:
            identify task_type: 'send', 'delete', 'check_inbox'
            in case of task_type 'send', identify the message
          answer format:'email', task_type, message (if any)
          
          if the user asks to send a text message:
            identify the message and the receiver
          answer format: 'text', message, receiver
          
          if user asks for current news, sports events or the weather:
            identify api_type: 'news', 'sports', 'weather'
          answer format: 'api', api_type
          
          if user asks to edit their schedule (example: add or delete tasks for a day or hour, etc):
           identify task_type based on context: "new event", "delete event", "check events", "edit event", "check date" 
          answer format: 'calendar' 
          
          if user specifically asks to search the web for something:
            identify prompt to search
          answer format: 'web', prompt
          
          if none of the above tasks apply:
          answer format: 'chat', user input
          
          given user input: {input_string}
          """
    ]

    response = model.generate_content(classification_prompt)

    if "calculator" in response.text:
        print(response.text)

    elif "command" in response.text:
        print(response.text)
        
    elif "email" in response.text:
        print(response.text)
        
    elif "text" in response.text:
        print(response.text)
        
    elif "api" in response.text:
        print(response.text)
        
    elif "calendar" in response.text:
        print(response.text)
    
    elif "web" in response.text:
        print(response.text)
        
    elif "chat" in response.text:
        print(response.text)

    else:
        return "Invalid response"

chat()