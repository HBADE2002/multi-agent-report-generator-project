from agents import build_search_agent, build_research_agent, writer_chain, critic_chain
from rich import print

def run_research_pipeline(topic:str) -> dict:


    state ={}
    #search agent working
    print("\n"+ "="*50)
    print("step 1: Search Agent - Gathering initial research")
    print("\n"+ "="*50)

    search_agent = build_search_agent()
    search_result = search_agent.invoke({
        "messages": [("user", f"Search for recent and reliable information on the topic: {topic}")]
    })

    for m in search_result["messages"]:
        print(type(m).__name__, getattr(m, "tool_calls", None), repr(getattr(m, "content", ""))[:200])

    state['search_results'] = search_result["messages"][-1].content

    

    print("\n search results: \n", state['search_results'])

    #step 2 - reader agent working

    print("\n"+ "="*50)
    print("step 2: Research Agent - Scraping and analyzing the search results")
    print("\n"+ "="*50)

    reader_agent = build_research_agent()
    reader_result = reader_agent.invoke({
        "messages":[("user", f"Based on the following search results about '{topic}', "
                          f"pick the most relevant URL and scrape it for deeper content.\n\n"
                          f"Search Results: \n{state['search_results']}"
                          )]
    })

    state['scraped_content'] = reader_result["messages"][-1].content
    print("\n scraped content: \n", state['scraped_content'])

    #step 3 - writer agent working

    print("\n"+ "="*50)
    print("step 3: Writer Agent - Writing a detailed research report")
    print("\n"+ "="*50)

    research_combined = (
        f"Search Results:\n{state['search_results']}\n\n"
        f"Scraped Content:\n{state['scraped_content']}"
    )

    state['report'] = writer_chain.invoke(
        {
            "topic": topic,
            "research": research_combined
            }
    )

    print("\n final research report: \n", state['report'])

    #step 4 - critic agent working

    print("\n"+ "="*50)
    print("step 4: Critic Agent - Reviewing and providing feedback on the research report")
    print("\n"+ "="*50)

    state['feedback'] = critic_chain.invoke(
        {
            "report": state['report']
        }
    )

    print("\n critic feedback: \n", state['feedback'])

    return state



if __name__ == "__main__":
    topic = input("Enter a topic for research: ")
    run_research_pipeline(topic)