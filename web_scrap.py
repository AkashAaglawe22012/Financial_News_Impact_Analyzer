import os
from tavily import TavilyClient
from typing import Annotated

os.environ["LANGCHAIN_IMPORT_WARNING_DISABLED"] = "1"
# from langchain_openai import ChatOpenAI
from langchain_cohere import ChatCohere

# from apiclient.errors import HttpError
from googleapiclient.errors import HttpError
import warnings

from langchain_community.adapters.openai import convert_openai_messages


import requests
from bs4 import BeautifulSoup
import time
import random
from fake_useragent import UserAgent
from dotenv import load_dotenv

load_dotenv()


def extract_article(url):
    headers = {
        "User-Agent": UserAgent().random,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Referer": "https://www.google.com/",
        "DNT": "1",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
    }

    session = requests.Session()

    for _ in range(3):  # Try up to 3 times
        try:
            response = session.get(url, headers=headers, timeout=10)
            response.raise_for_status()  # Raise an exception for bad status codes

            # Parse the HTML content with BeautifulSoup
            soup = BeautifulSoup(response.content, "html.parser")

            # Extract the article content
            article_content = soup.find("article")
            if article_content:
                content = article_content.get_text()
            else:
                content = soup.get_text()

            return content.strip()  # Remove unnecessary whitespace
        except requests.RequestException as e:
            print(f"Request failed: {e}")
            time.sleep(random.uniform(1, 3))  # Wait before retrying

    raise Exception("Failed to extract article after multiple attempts")


warnings.simplefilter("ignore")


TAVILY_API_KEY = os.environ.get("tav_API_Key")

client = TavilyClient(api_key=TAVILY_API_KEY)

import openai


def search_tool(
    query: Annotated[str, "The search query"],
) -> Annotated[str, "The search results"]:

    try:
        # print("query = ",query)
        content = client.search(
            query=query,
            search_depth="advanced",
            use_cache=True,
            max_results=2,
        )
        # print("content = ",content)
        content = content["results"]
        content = get_content(content)
        prompt = [
            {
                "role": "system",
                "content": f"You are an AI critical thinker research assistant. "
                f"Your sole purpose is to write well written, critically acclaimed,"
                f"It must include the thoughts of the industry leaders.It is a mandatory in the report"
                f"objective and structured reports on given text."
                f"The report should contain the economic and market growth impact."
                f"The report should be detailed and it should mention the source of the information."
                f"The report should be extremely informative."
                f"Always mention the examples related to the facts.",
            },
            {
                "role": "user",
                "content": f'Information: """{content}"""\n\n'
                f"Using the above information, answer the following"
                f'query: "{query}" in a detailed report do not include conclusion and references and summary --',
            },
        ]
        lc_messages = convert_openai_messages(prompt)
        result = str(
            ChatCohere(
                model="command-r",
                cohere_api_key=os.environ.get("cohere_api_key"),
            )
            .invoke(lc_messages)
            .content
        )
        return result.encode("utf-8")

    except HttpError as e:
        print(f"An HTTP error {e.resp.status} occurred:\n{e.content}")


def get_content(results):
    data = []
    for result in results:
        title = result.get("title")
        url = result.get("url")
        if title and url:
            content = extract_article(url)
            data.append({"title": title, "content": content})
    return data


# # # Example function call with real-time scenario

# # Define the search query
# query = "TechCorp announces record Q3 earnings"

# # Call the search_tool function
# article_report = search_tool(query)

# # Print the generated report
# print("article_report = ", article_report)


# #C:\Users\INDIA\Desktop\open_cv\computer_Vision\mcp_ciny\tav.py
