from pydantic_ai import Agent
from pydantic_ai.models.groq import GroqModel
from random import randint

def Dice_Agent(llm: str, deps_type: type, result_type: type, system_prompt: str, apikey: str) -> Agent:
    model = GroqModel(
        model_name=llm,
        api_key=apikey,
    )

    dice_agent = Agent(
        model=model,
        deps_type=deps_type,
        result_type=result_type,
        system_prompt=system_prompt,
    )

    ROLLS: int = 1
    @dice_agent.tool_plain(retries=ROLLS)
    async def roll_a_die() -> int:
        """Rolls a die and returns a random number between 1 and 6."""
        print("Rolling a die!")
        roll = randint(1,6)
        return roll

    return dice_agent
