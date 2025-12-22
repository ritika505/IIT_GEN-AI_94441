from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langchain.agents.middleware import wrap_model_call
from langchain.tools import tool



@tool
def calculator(expression: str) -> str:
    """Evaluate a mathematical expression"""
    try:
        return str(eval(expression))
    except Exception as e:
        return f"Calculation error: {e}"


@tool
def current_weather(city: str) -> str:
    """Get current weather (mock data)"""
    data = {
        "pune": "Sunny, 32°C",
        "mumbai": "Cloudy, 30°C",
        "delhi": "Hot, 38°C"
    }
    return data.get(city.lower(), "Weather data not available")


@tool
def knowledge_lookup(topic: str) -> str:
    """Simple knowledge lookup"""
    kb = {
        "python": "Python is a high-level programming language.",
        "ai": "AI stands for Artificial Intelligence.",
        "langchain": "LangChain is used to build LLM-based agents."
    }
    return kb.get(topic.lower(), "Topic not found")



@wrap_model_call
def model_logging(request, handler):
    print("\n[LOG] Before model call")
    print("Messages:", len(request.messages))

    response = handler(request)

    print("[LOG] After model call")
    response.result[0].content = response.result[0].content.upper()
    return response


@wrap_model_call
def limit_model_context(request, handler):
    print("[CTX] Limiting context to last 5 messages")
    request = request.override(messages=request.messages[-5:])
    return handler(request)


# LOCAL MODEL (LM STUDIO)

llm = init_chat_model(
    model="google/gemma-3n-e4b",                   
    model_provider="openai",
    base_url="http://127.0.0.1:1234/v1",
    api_key="not-needed",
    temperature=0.2
)



agent = create_agent(
    model=llm,
    tools=[calculator, current_weather, knowledge_lookup],
    middleware=[model_logging, limit_model_context],
    system_prompt="You are a helpful assistant. Answer briefly."
)


conversation = []

print("\nType 'exit' to quit\n")

while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        break

    conversation.append({"role": "user", "content": user_input})

    result = agent.invoke({"messages": conversation})

    ai_msg = result["messages"][-1]
    print("AI:", ai_msg.content)

    conversation = result["messages"]
