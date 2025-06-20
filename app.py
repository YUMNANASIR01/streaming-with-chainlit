#  Streaming with chainlit 
import os
from dotenv import load_dotenv
from agents import Agent, Runner,OpenAIChatCompletionsModel,AsyncOpenAI,set_tracing_disabled
import chainlit as cl
import rich

# ---------------------------------------
load_dotenv()
set_tracing_disabled(disabled=True)
OPEN_ROUTER_API_KEY=os.getenv("OPEN_ROUTER_API_KEY")
# ---------------------------------------
history = []
# --------------------- model change karty huay chaly gya -----------------------------

client = AsyncOpenAI(
        api_key=OPEN_ROUTER_API_KEY,
        base_url="https://openrouter.ai/api/v1"
         )

agent = Agent(
        name="my_agent",
        model=OpenAIChatCompletionsModel(model="deepseek/deepseek-chat-v3-0324:free",openai_client=client),
        instructions="You are a helpful assistant.",
       )
# -----------------------------------------
@cl.on_message
async def my_message(msg: cl.Message):
    user_input = msg.content
    history.append({"role" :"user","content": user_input})
    message = cl.Message(content="")
    
    res =  Runner.run_streamed(agent, history)
    
    async for event in res.stream_events():
        if event.type == "raw_response_event" and hasattr(event.data, "delta"):
           await message.stream_token(event.data.delta)