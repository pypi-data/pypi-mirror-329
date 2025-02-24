# -*- coding: utf-8 -*-
"""
@Time: 2024/12/25 14:00
@Author: ZJun
@File: tools.py
@Description: This file contains the tools for the agent to use.
"""


from duckduckgo_search import DDGS
import requests
from bs4 import BeautifulSoup
from tenacity import retry, wait_exponential, stop_after_attempt
from tavily import TavilyClient
from dotenv import load_dotenv
import os

load_dotenv()


@retry(stop=stop_after_attempt(5), wait=wait_exponential(multiplier=1, min=4, max=10))
def web_search(query:str,timelimit:str,max_results:int):
    """
    Search the web for the given query with the specified time limit and maximum number of results.

    Args:
        query (str): The query to search.
        timelimit (Literal['d', 'w', 'm', 'y']): The time limit for the search.
        max_results (int): The maximum number of results to return usually set to 10.

    """
    try:
        results = DDGS().text(keywords=query, safesearch='moderate', timelimit=timelimit, max_results=max_results)
    except Exception as e:
        # print(f"Error during search: {e}")
        return []

    DETAIL_N = 1

    for result in results[:DETAIL_N]:
        try:
            result['content'] = web_content_extract(result['href'], timeout=10)
        except Exception as e:
            # print(f"Error extracting content from {result['href']}: {e}")
            result['content'] = None

    return results

@retry(stop=stop_after_attempt(5), wait=wait_exponential(multiplier=1, min=4, max=10))
def web_content_extract(link: str) -> str:
    """
    Process the content of the given link by using beautifulsoup.

    Args:
        link (str): The link to process.

    Returns:
        str: The main content of the link.
    """
    response = requests.get(link, timeout=10)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Attempt to find the main content using common tags
    main_content = ''
    if soup.main:
        main_content = soup.main.get_text(strip=True)
    elif soup.article:
        main_content = soup.article.get_text(strip=True)
    elif soup.section:
        main_content = soup.section.get_text(strip=True)
    elif soup.body:
        main_content = soup.body.get_text(strip=True)
    else:
        main_content = soup.get_text(strip=True)

    return main_content

def save_to_markdown(workspace:str,filename:str,text:str):
    """
    Save the given text to a markdown file.

    Args:
        workspace (str): The workspace to save the file.
        filename (str): The filename to save.
        text (str): The text to save.
    """

    with open(f"{workspace}/{filename}.md", "w") as f:
        f.write(text)

def tavily_search(query:str,days:int,max_results:int):
    tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
    # context = tavily_client.get_search_context(query=query,max_results=max_results,days=days)
    context = tavily_client.search(query=query,max_results=max_results,days=days,include_raw_content=False)
    return context
