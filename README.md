# 🔎 Multi-Agent Research System

An AI-powered research pipeline that automatically searches the web, scrapes relevant content, writes a structured report, and critiques its own output — all through a chain of cooperating LLM agents. Includes a Streamlit UI for easy interaction.

## How It Works

The pipeline runs four agents in sequence, each handing its output to the next:

1. **Search Agent** — Uses the [Tavily](https://tavily.com) search API to gather recent, relevant sources on the given topic.
2. **Research Agent** — Picks the most relevant URL(s) from the search results and scrapes the page content for deeper context.
3. **Writer Agent** — Synthesizes the search results and scraped content into a structured research report (Introduction, Key Findings, Conclusion, Sources).
4. **Critic Agent** — Reviews the generated report and provides a score (out of 10), strengths, areas to improve, and a one-line verdict.

All agents are powered by an LLM served through [OpenRouter](https://openrouter.ai), orchestrated with [LangChain](https://www.langchain.com/).

## Project Structure

```
.
├── agents.py            # Defines the LLM, agents, and writer/critic chains
├── app.py                # Streamlit UI for running the pipeline interactively
├── pipeline.py            # Core pipeline logic (CLI entry point)
├── tools.py                # Custom tools: web_search (Tavily) and scrape_url (BeautifulSoup)
├── requirements.txt        # Python dependencies
├── .env                     # API keys (not committed — see Setup)
└── .gitignore
```

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/<your-repo-name>.git
cd <your-repo-name>
```

### 2. Create and activate a virtual environment

Using `uv`:
```bash
uv venv
source .venv/bin/activate
```

Or using standard `venv`:
```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
uv pip install -r requirements.txt
```
or
```bash
pip install -r requirements.txt
```

### 4. Configure API keys

Create a `.env` file in the project root with:

```
OPENROUTER_API_KEY=your_openrouter_api_key
TAVILY_API_KEY=your_tavily_api_key
```

- Get an OpenRouter key at [openrouter.ai](https://openrouter.ai)
- Get a Tavily key at [tavily.com](https://tavily.com)

## Usage

### Run via the Streamlit UI (recommended)

```bash
streamlit run app.py
```

This opens a browser interface where you can enter a topic and view the final report, critic feedback, and intermediate search/scrape output.

### Run via the command line

```bash
python pipeline.py
```

You'll be prompted to enter a topic, and the pipeline will print each step's output directly to the terminal.

## Example

**Input topic:** `impact of water pollution in Mumbai`

**Output:** A structured Markdown report covering key findings, sources, and health/economic impacts, followed by a critic review scoring the report's rigor and flagging any unverified claims or weak sourcing.

## Notes & Limitations

- Report quality depends on the underlying LLM's ability to reliably call tools (`web_search`, `scrape_url`) rather than answering from memory — some free-tier models are inconsistent about this.
- Scraping can fail on JavaScript-heavy or access-restricted pages; the pipeline falls back to search snippets in that case.
- The writer agent is instructed to only use facts present in the gathered research, but LLM outputs should still be fact-checked before use in any formal or published context.

## Tech Stack

- [LangChain](https://www.langchain.com/) — agent orchestration
- [OpenRouter](https://openrouter.ai) — LLM access
- [Tavily](https://tavily.com) — web search API
- [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/) — web scraping
- [Streamlit](https://streamlit.io) — UI

## License

MIT (or update as appropriate)
