from autogen import config_list_from_json, AssistantAgent, UserProxyAgent
import re
import asyncio


async def autogen_command(command):

    config_list = config_list_from_json(
        env_or_file="backend/OAI_CONFIG_LIST",
    )

    llm_config = {"config_list": config_list}

    # User Proxy Agent
    user_proxy_agent = UserProxyAgent(
        name="User_Proxy_Agent",
        code_execution_config={"work_dir": "coding", "use_docker": False},
        human_input_mode="NEVER",
        max_consecutive_auto_reply=5,
        is_termination_msg=lambda msg: "TERMINATE" in msg.get("content", ""),
    )
    # system_message="""

    #     If the code is correct and runs successfully, respond with the final corrected code inside 3 single quotes for example, and after that leave a line and write the word 'SUCCESS'."""

    # Assistant Agent
    assistant_agent = AssistantAgent(
        name="Assistant_Agent",
        llm_config=llm_config,
    )
    # is_termination_msg=lambda msg: "SUCCESS" in msg.get("content", ""),

    prompt = f"""
    You are a command line command executor agent.
    Execute the command in the terminal and provide the output. 
    
    IF THE COMMAND IS RELATED TO GIT, MAKE SURE YOU ONLY EXECUTE THE ONE COMMAND NECESSARY, DO NOT GIT COMMIT OR GIT PUSH UNLESS ASKED TO EXPLICITLY BY THE USER
    
    Given command: {command}
    """

    user_proxy_agent.initiate_chat(assistant_agent, message=prompt)
    await user_proxy_agent.a_send(
        f"""Based on the results in above conversation, please provide the output generateed by the command execution between ``` and ```.
        Only give the output verbatim as it is and not any sample data or any other information.

        There is no need to use the word TERMINATE in this response.

        """,
        assistant_agent,
        request_reply=False,
        silent=True,
    )
    response = await assistant_agent.a_generate_reply(
        assistant_agent.chat_messages[user_proxy_agent], user_proxy_agent
    )
    await assistant_agent.a_send(
        response, user_proxy_agent, request_reply=False, silent=True
    )

    last_message = assistant_agent.chat_messages[user_proxy_agent][-1]["content"]
    # print("last_Message: ", last_message)

    autogen_output = re.search(
        r"('''|```)?(.*?)('''|```)", last_message, re.DOTALL
    ).group(2)
    # start_index = last_message.find("```") + 3 # Adding 3 to exclude the triple quotes themselves
    # end_index = last_message.rfind("```")
    # autogen_code = last_message[start_index:end_index]
    # print("final autogen_output: ", autogen_output)
    return autogen_output


# async def main():
#     input_command = input("Enter the command to be executed: ")
#     response = await autogen_command(input_command)
#     print(response)

# asyncio.run(main())