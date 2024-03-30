from functionalities.autogen_code import autogen_command
from functionalities.math_autogen import autogen_math
from functionalities.web_search import scrape_google_search

import google.generativeai as genai
import os
from dotenv import load_dotenv
import asyncio

load_dotenv()

if "GOOGLE_API_KEY" not in os.environ:
    raise ValueError("GOOGLE_API_KEY not found in environment or .env file")

genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

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

def llm_model(input_string):
    # input_string = input("Hello User!: ")

    classification_prompt = [
        f"""
        
        Given user input: {input_string}

        Given the raw text input above, select the task best suited for the input, depending on what the user seems to need: 
        
        if the user asks for any mathematical calculations or puts forth any mathemtical problem, output in strictly this format: 'calculator'
          
        if the user asks to execute a command prompt or a code:
        output format: 'command', input_string
          
        if the user asks to send an email:
        identify task_type: 'send', 'delete', 'check_inbox'
        in case of task_type 'send', identify the message and receiver
        output format:'email', task_type, message (if any), receiver (if any)
          
        if the user asks to send a text message:
        identify the message and the receiver
        output format: 'text', message, receiver
          
        if user asks for current news, sports events or the weather:
        identify api_type: 'news', 'weather'
        output format: 'api', api_type
          
        if user asks to edit their schedule (example: add or delete tasks for a day or hour, etc):
        identify task_type based on context: "new event", "delete event", "check events", "edit event", "check date" 
        output format: 'calendar' 
          
        if user specifically asks to search the web for something:
        identify prompt to search
        output format: 'web', prompt
          
        if none of the above tasks apply:
        output format: 'chat', input_string
                  
        GIVE OUTPUT IN STRING ONLY IN THE GIVEN OUTPUT FORMAT FOR EACH CASE MENTIONED ABOVE
        
        """
    ]

    response = model.generate_content(classification_prompt)
    task = response.text.split(",")[0].strip()
    print(task)
    if task == "calculator":
        print(response.text)
        
        async def math():
            global output 
            output = await autogen_math(input_string)
        
        asyncio.run(math())
        
        return output

    elif task == "command":
        print(response.text)
        
        input_string = response.text.split(",")[1].strip()
                
        async def command():
            global output 
            output = await autogen_command(input_string)
        
        asyncio.run(command())
        
        return output
        
    elif task == "email":
        print(response.text)
        return response.text
        
    elif task == "text":
        print(response.text)
        return response.text
        
    elif task == "api":
        print(response.text)
        return response.text
        
    elif task == "calendar":
        print(response.text)
        return response.text
    
    elif task == "web":
        print(response.text)
        
        links = scrape_google_search(input_string, 5) # 5 is the number of search results to return (i.e. top 5 results)
        
        prompt = [
            f"""
            Given input string: {input_string}
            
        
            Output whatever you know about the above mentioned input string in one short paragraph and if you don't have any knowledge about it, output 'I don't know anything about this topic but I can search the web for you'
            """
        ]
        
        llm_response = model.generate_content(prompt)
        
        final_response = llm_response.text + "\n\n" + "Here are the top 5 results from the web:\n-" + "\n- ".join(links)
                
        return final_response
        
    elif task == "chat":
        print(response.text)
        return response.text

    else:
        return "Invalid response"

