import datetime
from pydantic_ai import Agent, RunContext
from pydantic_ai.models.groq import GroqModel
from pydantic import BaseModel, Field

from typing import Any
from dataclasses import dataclass
from tavily import AsyncTavilyClient
import nest_asyncio
import asyncio 

# Apply nest_asyncio to allow nested event loops (useful in Jupyter notebooks)
nest_asyncio.apply()

# Dataclass for search parameters
@dataclass
class SearchDataclass:
    max_results: int
    todays_date: str

# Dataclass for research dependencies
@dataclass
class ResearchDependencies:
    todays_date: str
    search_deps: SearchDataclass  # Add search_deps to ResearchDependencies

# Pydantic model for research results
class ResearchResult(BaseModel):
    research_title: str = Field(description='Markdown heading describing the article topic')
    research_main: str = Field(description='A main section that provides a detailed article')
    research_bullets: str = Field(description='A list of bullet points that summarize the article')

# Class to encapsulate the search agent and its functionality
class SearchAgentWrapper:
    def __init__(self, groq_api_key: str, tavily_api_key: str, model_name: str = "llama-3.3-70b-versatile"):
        # Initialize the Groq model
        self.model = GroqModel(
            model_name=model_name,
            api_key=groq_api_key,
        )

        # Initialize Tavily client
        self.tavily_client = AsyncTavilyClient(api_key=tavily_api_key)

        # Initialize the search agent
        self.search_agent = Agent(
            self.model,
            result_type=ResearchResult,
            deps_type=ResearchDependencies,
            system_prompt='You are a helpful research assistant, you are an expert in research. When given a query, write strong keywords to do 3-5 searches in total utilizing the provided search tool. Then combine the results into a detailed response.',
        )

        # System prompt with today's date
        @self.search_agent.system_prompt
        async def add_current_date(ctx: RunContext[ResearchDependencies]) -> str:
            todays_date = ctx.deps.todays_date
            system_prompt = (
                f"You're a helpful research assistant and an expert in research. "
                f"When given a question, write strong keywords to do 3-5 searches in total. "
                f"(each with query_number) and then combine the results. "
                f"If you need today's date, it is {todays_date}. "
                f"Focus on providing accurate and current information."
                f"Always provide the results from the search results"
            )
            return system_prompt

        # Search tool for Tavily
        @self.search_agent.tool
        async def get_search(search_data: RunContext[ResearchDependencies], query: str, query_number: int) -> dict[str, Any]:
            max_results = search_data.deps.search_deps.max_results  # Access max_results from search_deps
            results = await self.tavily_client.get_search_context(query=query, max_results=max_results)
            return results

    async def do_search(self, query: str, max_results: int):
        current_date = datetime.date.today()  # Corrected: Use datetime.date.today()
        data_string = current_date.strftime("%Y-%m-%d")
        search_deps = SearchDataclass(max_results=max_results, todays_date=data_string)  # Create SearchDataclass
        deps = ResearchDependencies(todays_date=data_string, search_deps=search_deps)  # Pass search_deps to ResearchDependencies
        result = await self.search_agent.run(query, deps=deps)  # Pass deps to run
        return result

# Example usage of the SearchAgentWrapper class
async def main():
    # Initialize the search agent wrapper
    groq_api_key = "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"
    tavily_api_key = "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"
    search_agent_wrapper = SearchAgentWrapper(groq_api_key, tavily_api_key)

    # Perform a search
    query = "what is the current price for the zephyrous g14 and tell me what the results are:"
    max_results = 5
    result_data = await search_agent_wrapper.do_search(query, max_results)

    # Extract and print the detailed text from the result
    if result_data and hasattr(result_data, 'data'):
        detailed_text = result_data.data.research_main
        print(detailed_text)
    else:
        print("No result data found.")

# Run the main function
if __name__ == "__main__":
    asyncio.run(main())