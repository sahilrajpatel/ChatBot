"""
Run this to chat in the terminal:
    python main.py

Type 'exit' to quit.
"""
from langchain_core.messages import HumanMessage

from src.chatbot_graph import build_graph

graph = build_graph()


def main():
    print("Chatbot is ready! (connected to the internet for real-time stuff)")
    print("Type 'exit' to quit.\n")

    chat_history = []

    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Bye!")
            break

        chat_history.append(HumanMessage(content=user_input))

        result = graph.invoke({"messages": chat_history})
        chat_history = result["messages"]

        # last message is the final answer from the bot
        print("Bot:", chat_history[-1].content, "\n")


if __name__ == "__main__":
    main()
