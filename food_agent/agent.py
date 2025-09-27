from google.adk.agents import LlmAgent, SequentialAgent
from toolbox_core import ToolboxSyncClient
from .prompt import *
import asyncio

toolbox = ToolboxSyncClient("http://127.0.0.1:7000")

toolbox_tools = toolbox.load_toolset('my-bq-toolset')

food_dosage_tool = toolbox.load_tool('get_food_dosage')
daily_dosage_tool = toolbox.load_tool('get_daily_dosage')

food_dosage_agent = LlmAgent(
    name="food_dosage",
    model="gemini-2.5-flash",
    description=(
        "Agent to get the dosage each food item submitted by the user"
    ),
    instruction=(
        """You are an Agent who gets the vitamins and minerals available in a food item"
        "You will get the food item that the user ate from the user input."
        "Pass only the food item name to the tool which will be used as a parameter to get the vitamins and minerals of the food item"
        # "Pass the food item in the following JSON format"

        # {
        # food_item : food_item_name
        # }

        "Use the 'food_dosage_tool' tool from the toolset
        """
        # """
        # You are an Agent who gets the complete sql query from the State key `app:sql_query`. The State key will contain the query in the following format

        # {
        # "complete_sql_query": complete_sql_query
        # }
        # Pass this value `complete_sql_query` of the State key to the `food_dosage_tool`
        # """
    ),
    tools=[food_dosage_tool],
)

daily_dosage_agent = LlmAgent(
    name="daily_dosage_agent",
    model="gemini-2.5-flash",
    description=(
        "Agent to get the daily required dosage for pregnant women"
    ),
    instruction=(
        "You are a helpful agent who gets the daily required dosage of different vitamins and minerals."
        "Use the 'get_daily_dosage' tool from the toolset "
    ),
    tools=[daily_dosage_tool],
)

root_agent = LlmAgent(
    name="root_agent",
    model="gemini-2.5-flash",
    description=(
        "Agent to get required information about vitamins and mineral primarily for pregnant woman"
    ),
    instruction=agent_instruction,
    sub_agents=[
        daily_dosage_agent,
        food_dosage_agent
    ]
)