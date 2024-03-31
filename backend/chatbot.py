from functionalities.autogen_code import autogen_command
from functionalities.math_autogen import autogen_math
from functionalities.web_search import scrape_google_search

import google.generativeai as genai
import os
import json
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

def llm_model(input_string, chat_history):
    # input_string = input("Hello User!: ")

    classification_prompt = [
        f"""
        You are a helpful chatbot. You talk to the user and help them with their queries.
        This is the user's input: {input_string}
        
        Here is the user's chat history with you: {chat_history}

        Figure out whether the above user input is a task that the user wants you to do or if it is a question that can be answered given the chat history above. If it is a task, output "task". If it is a question answerable by chat history, output "chat".

        Output of this prompt should be in string format only with the output being either "task" or "chat".
        
        """
    ]
    
    response = model.generate_content(classification_prompt)
    # print(response)
    classification_response = str(response.text.strip())
    # print("classification response:"+classification_response)
    
    if classification_response == "task":
        task_prompt = [
            f"""
            Given user input: {input_string}

            Given the raw text input above, select the task best suited for the input, depending on what the user seems to need: 
            
            if the user asks for any mathematical calculations or puts forth any mathemtical problem, output in strictly this format: 'calculation'
            
            if the user asks to execute a command prompt or a code:
            output format: 'command execution', input_string
            
            if the user asks to send an email:
            identify task_type: 'send', 'delete', 'check_inbox'
            in case of task_type 'send', identify the message and receiver
            output format:'email', task_type, message (if any), receiver (if any)
            
            if the user asks to send a text message:
            identify the message and the receiver
            output format: 'text message', message, receiver
            
            if user asks for current news or weather:
            identify api_type: 'news', 'weather'
            output format: 'api call', api_type
            
            if user asks to edit their schedule (example: add or delete tasks for a day or hour, etc):
            identify task_type based on context: "new event", "delete event", "check events", "edit event", "check date" 
            output format: 'calendar function', task_type
            
            if user specifically asks to search the web for something:
            identify prompt to search
            output format: 'web search', prompt
            
            if none of the above tasks apply, but you think the user is still asking for a task to completed:
            output the 3 most relevant tasks from the above list of tasks you are able to identify based on the user input task. 
            Output format: 'multi', task1, task2, task3
                    
            GIVE OUTPUT IN STRING ONLY IN THE GIVEN OUTPUT FORMAT FOR EACH CASE MENTIONED ABOVE
            
            """
        ]

        response = model.generate_content(task_prompt)
        # print(task_response.text)
        task = response.text.split(",")[0].strip()
        # print(task)
        if task == "calculation":
            print(response.text)
            
            async def math():
                output = await autogen_math(input_string)
                return output
            
            output = asyncio.run(math())
            
            return output

        elif task == "command execution":
            print(response.text)
            
            input_string = response.text.split(",")[1].strip()
                    
            async def command():
                output = await autogen_command(input_string)
                return output
            
            output = asyncio.run(command())
            
            return output
            
        elif task == "email":
            print(response.text)
            return response.text
            
        elif task == "text message":
            print(response.text)
            return response.text
            
        elif task == "api call":
            print(response.text)
            return response.text
            
        elif task == "calendar function":
            print(response.text)
            return response.text
        
        elif task == "web search":
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
        
        elif task == "multi":
            print(response.text)
            
            tasks = []            
            
            for i in range(1, 4):
                task = response.text.split(",")[i].strip()
                tasks.append(task)
            
            print(tasks)
            
            output = "Sorry, I cannot perform that task. But here are the 3 most relevant tasks I can perform based on your input: \n\n1. "+tasks[0]+"\n2. "+tasks[1]+"\n3. "+tasks[2]
            
            # tasks_json = json.loads("{"+"task1:"+tasks[0]+", task2:"+tasks[1]+", task3:"+tasks[2]+"}")
            
            # json_output = json.loads("{"+"message:"+output+"buttons:"+tasks_json+"}")
            
            return output
            

        else:
            return "Invalid response"

    elif classification_response == "chat":
                
        chat_prompt = [
            f"""
            You are a helpful chatbot. Talk to the user and help them with their queries.
            Here is the user's chat history with you: {chat_history}
            
            Use the chat history as context to generate a response to the user's input.
            Here is the user's input: {input_string}
            """
        ]
        
        chat_response = model.generate_content(chat_prompt)
        
        return chat_response.text
    
    else:
        return "Invalid Response"
    
    
def rag_llm(user_input, file_text):
    
    prompt = [
        f"""
        This is the provided file text: {file_text}
        
        This is the user's input: {user_input}
        
        Given the user input and the file text, generate a response to the user's input ONLY BASED ON THE FILE TEXT.
        """
    ]
    
    response = model.generate_content(prompt)
    
    return response.text
    