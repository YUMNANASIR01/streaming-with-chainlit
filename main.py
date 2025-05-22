
import os 
from dotenv import load_dotenv
from agents import Agent,OpenAIChatCompletionsModel, Runner,set_tracing_disabled
from openai import AsyncOpenAI
from openai.types.responses import ResponseTextDeltaEvent
import chainlit as cl
import rich


load_dotenv()

set_tracing_disabled(disabled=True)

OPEN_ROUTER_API_KEY = os.getenv("OPEN_ROUTER_API_KEY")
#----------------------------------------
history = []
# -------------------------

client = AsyncOpenAI(
    api_key=OPEN_ROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1",
)

agent = Agent(
     model = OpenAIChatCompletionsModel(model="deepseek/deepseek-r1:free", openai_client=client),
     name = "my_agent",
     instructions = "you are a helpful assistant",
                        #  --------- system prompt-------
)

# ----------------------------------------------
# ------------------- streaming ----------------------
#                                             ---- user prompt-------
@cl.on_message
async def chat(message: cl.Message):
    user_prompt = message.content

    history.append({"role": "user", "content": user_prompt})

    msg = cl.Message(content="")
    res = Runner.run_streamed(agent,history)
    async for event in res.stream_events():
        if event.type == "raw_response_event" and isinstance(event.data , ResponseTextDeltaEvent):
            await msg.stream_token(event.data.delta)
 