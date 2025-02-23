import asyncio
from DiceAgent import DiceAgent

async def main():
    agent = DiceAgent(
        llm="llama-3.3-70b-versatile",
        api_key="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"
    )

    while True:
        user_message = input("You: ")
        response = await agent.process_user_input(user_message)

        if response == "Exiting...":
            break

        print(response)

if __name__ == "__main__":
    asyncio.run(main())
