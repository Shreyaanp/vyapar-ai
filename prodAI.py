import os
import requests
import json
from bs4 import BeautifulSoup, Comment
from dotenv import load_dotenv
import time

from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain

# Load environment variables
load_dotenv()
openai_api_key = os.getenv("OPENAI_APIKEY")
serper_api_key = os.getenv("SERPERAPI_APIKEY")

if not openai_api_key or not serper_api_key:
    raise ValueError("API keys for OpenAI or Serper are missing. Check your .env file.")

os.environ["OPENAI_API_KEY"] = openai_api_key
os.environ["SERPER_API_KEY"] = serper_api_key

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 10; Pixel 4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Mobile Safari/537.36'
}

serper_url = "https://google.serper.dev/search"
serper_headers = {
    'X-API-KEY': serper_api_key,
    'Content-Type': 'application/json'
}

def perform_search(query: str):
    payload = json.dumps({
        "q": query,
        "gl": "in",
        "autocorrect": False
    })

    start_time = time.time()
    try:
        response = requests.post(serper_url, headers=serper_headers, data=payload)
        results = response.json()
        end_time = time.time()
        
        return results
    except Exception as e:
        return {}

def clean_html(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    
    for script_or_style in soup(['script', 'style']):
        script_or_style.decompose()

    for comment in soup.find_all(string=lambda text: isinstance(text, Comment)):
        comment.extract()
    
    for tag in soup.find_all():
        if not tag.get_text(strip=True):
            tag.decompose()

    cleaned_text = soup.get_text(separator=' ', strip=True)
    
    return cleaned_text

def parse_html(content) -> str:
    cleaned_content = clean_html(content)
    text = ' '.join(cleaned_content.split())
    return text

web_content_buffer = []

def fetch_web_page(url: str) -> str:
    start_time = time.time()
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        content = parse_html(response.content)
        web_content_buffer.append(content)
        end_time = time.time()
        
        return content
    except requests.exceptions.RequestException as e:
        return ""

prompt_template = "Summarize the following content to generate SEO friendly data: {content}"
llm = ChatOpenAI(model="gpt-4o")
llm_chain = LLMChain(llm=llm, prompt=PromptTemplate.from_template(prompt_template))

def process_prompt(prompt: str) -> str:
    retries = 0
    max_retries = 2
    
    while retries < max_retries:
        search_start_time = time.time()
        search_results = perform_search(prompt)
        search_end_time = time.time()
        
        
        urls = [result['link'] for result in search_results.get('organic', [])[:3]]
        organic_data = search_results.get('organic', [])
        people_also_ask = search_results.get('peopleAlsoAsk', [])
        related_searches = search_results.get('relatedSearches', [])

        fetch_start_time = time.time()
        for url in urls:
            fetch_web_page(url)
        fetch_end_time = time.time()
        
        
        combined_content = ' '.join(web_content_buffer)
        organic_info = '\n'.join([f"{item['title']}: {item['snippet']}" for item in organic_data])
        people_ask_info = '\n'.join([f"Q: {item['question']}\nA: {item.get('answer', 'No answer provided')}" for item in people_also_ask])
        related_searches_info = '\n'.join([f"Related Search: {item['query']}" for item in related_searches])

        post_prompt = f'''
        Here is some initial data from the search results:
        Organic Data: {organic_info}
        People Also Ask: {people_ask_info}
        Related Searches: {related_searches_info}
        
        Use your tools to search and create a proper product name, product description, about product in points, and a product tagline.
        Follow this process to complete your task:
        Step 1: Summarize all the generated content obtained from the website.
        Step 2: Provide the output in this format, with no extra data or explanation.

        Product Regional Names: [product regional names in India]
        Product Name: [product name]
        Product Description: [product description]
        Product Variation: [product variation]
        About Product: [about product in 10 points]
        Product Tagline: [product tagline]
        Product Prompt: [generate a prompt for converting input photos to professional photos based on the product use parameters for ecommerce.]
        Market PainPoints : [market painpoints]
        Customer Acquisition: [customer acquisition in points]
        Market Entry Strategy: [market entry strategy in points]
        Seo Friendly Tags: [seo friendly tags]
        The generated data should be more or less around 900 words.
        Do not break the above format and provide the output in json format.

        You can stop once the data has been generated
        '''
        complete_prompt = f'''
        Understand the context of the data provided below. 
        The data is extracted from the top search results. 
        You need to understand why they are ranked to the top search result and generate SEO friendly data to complete the task mentioned. 
        Also keep in mind that we need to have all the Names the product is called in different regions of India. 
        You can provide the data with respect to its usuage and why this product is best suited for the user.
        {prompt}

        Top Ranked data: {combined_content}. 
        Task to Perform : {post_prompt}'''

        with open('complete_prompt.txt', 'w') as f:
            f.write(complete_prompt)

        try:
            llm_start_time = time.time()
            result = llm_chain.run(complete_prompt)
            llm_end_time = time.time()
            
            break
        except Exception as e:
            print(f"Error occurred: {e}")
        retries += 1
    
    web_content_buffer.clear()
    return result

if __name__ == "__main__":
    test_prompt = "Product name : banarasi saree"
    print("Processing Prompt:", test_prompt)
    
    processed_prompt = process_prompt(test_prompt)
    print("Processed Prompt Result:", processed_prompt)
    
    with open('output.txt', 'w') as f:
        f.write(processed_prompt)
