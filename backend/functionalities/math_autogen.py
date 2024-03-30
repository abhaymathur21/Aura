import os
import re
import asyncio

import autogen
from autogen.agentchat.contrib.math_user_proxy_agent import MathUserProxyAgent


# 1. create an AssistantAgent instance named "assistant"


# 2. create the MathUserProxyAgent instance named "mathproxyagent"
# By default, the human_input_mode is "NEVER", which means the agent will not ask for human input.

# given a math problem, we use the mathproxyagent to generate a prompt to be sent to the assistant as the initial message.
# the assistant receives the message and generates a response. The response will be sent back to the mathproxyagent for processing.
# The conversation continues until the termination condition is met, in MathChat, the termination condition is the detect of "\boxed{}" in the response.


# math_problem = (
#     "Find all $x$ that satisfy the inequality $(2x+10)(x+3)<(3x+9)(x+8)$. Express your answer in interval notation."
# )

# We call `initiate_chat` to start the conversation.
# When setting `message=mathproxyagent.message_generator`, you need to pass in the problem through the `problem` parameter.


async def autogen_math(problem):
    config_list = autogen.config_list_from_json(
        "backend/OAI_CONFIG_LIST",
    )
    assistant_agent = autogen.AssistantAgent(
        name="assistant",
        system_message="You are a helpful assistant.",
        llm_config={
            "timeout": 600,
            "seed": 42,
            "config_list": config_list,
        },
    )
    
    math_proxy_agent = MathUserProxyAgent(
        name="mathproxyagent",
        human_input_mode="NEVER",
        code_execution_config={"use_docker": False},
    )

    math_proxy_agent.initiate_chat(assistant_agent, message=math_proxy_agent.message_generator, problem=problem)
    
    await math_proxy_agent.a_send(
        f"""Based on the results in above conversation, please provide the final answer to the math problem between ``` and ```.
        Only give the output verbatim as it is and not any sample data or any other information.

        There is no need to use the word TERMINATE in this response.

        """,
        assistant_agent,
        request_reply=False,
        silent=True,
    )
    response = await assistant_agent.a_generate_reply(
        assistant_agent.chat_messages[math_proxy_agent], math_proxy_agent
    )
    await assistant_agent.a_send(
        response, math_proxy_agent, request_reply=False, silent=True
    )

    last_message = assistant_agent.chat_messages[math_proxy_agent][-1]["content"]
    # print("last_Message: ", last_message)

    autogen_output = re.search(
        r"('''|```)?(.*?)('''|```)", last_message, re.DOTALL
    ).group(2)
    
    return autogen_output

math_problem = (
    "Find the value of $x$ that satisfies the equation $2x + 5 = 11$. "
)


# async def main():
#     response = await autogen_math(math_problem)
#     print(response)

# asyncio.run(main())