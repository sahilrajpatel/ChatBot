# Realtime Chatbot (LangChain + LangGraph)

A chatbot that can search the internet to answer questions about real-time stuff - like current news, weather, prices, scores, or anything happening right now that a normal LLM wouldn't know about (since LLMs only know things up to their training date).

It can also read a specific website if you give it a link.

## How it works

- Built using LangGraph's tool-calling pattern: the LLM decides on its own whether it needs to search the web or just answer directly
- Uses DuckDuckGo search (free, no API key needed) for real-time queries
- Uses `requests` + `BeautifulSoup` to read a website when you paste a URL
- Keeps chat history so it remembers the conversation

## Project structure

```
realtime-chatbot/
├── main.py            # chat in the terminal
├── app.py               # FastAPI version
├── src/
│   ├── config.py          # settings
│   ├── tools.py             # web_search and read_website tools
│   └── chatbot_graph.py      # the LangGraph agent (LLM + tools)
├── requirements.txt
└── .env.example
```

## How to run

1. Install dependencies
```bash
pip install -r requirements.txt
```

2. Add your OpenAI key
```bash
cp .env.example .env
# paste your key inside .env
```

3. Run it
```bash
python main.py
```

Then just chat normally, e.g.:
- "what's the weather in Delhi right now"
- "latest news about ISRO"
- "read this page and tell me what it says: https://example.com"

### API version

```bash
uvicorn app:app --reload
```
Go to `http://127.0.0.1:8000/docs` and try the `/chat` endpoint.

## Tech used

- LangChain - tool wrappers, messages
- LangGraph - agent loop (LLM decides: answer directly or call a tool)
- DuckDuckGo Search - free real-time web search
- BeautifulSoup - to read website content
- FastAPI - optional API

## Notes

- Search results depend on DuckDuckGo, so sometimes results can be a bit inconsistent for very specific queries
- Right now it only reads the first ~3000 characters of a website to keep things fast, can increase that in `tools.py` if needed
