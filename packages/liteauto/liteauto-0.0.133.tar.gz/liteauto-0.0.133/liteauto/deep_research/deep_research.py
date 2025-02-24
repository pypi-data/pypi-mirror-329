from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from litegen import LLM
from liteauto import google, parse, wlanswer
from pydantic import BaseModel
from typing import List, Optional, Tuple
from dataclasses import dataclass
from time import sleep
from collections import defaultdict
import hashlib
from datetime import datetime, timedelta

from liteauto.deep_research.intent import QStepper
# Initialize the LLM model


class ResearchSummary(BaseModel):
    title: str
    url: str
    summary: str
    relevance_score: float
    key_findings: Optional[str] = None
    citation_count: Optional[int] = None
    paper_hash: Optional[str] = None
    publication_date: Optional[str] = None


class SearchQueries(BaseModel):
    queries: List[str]


@dataclass
class ResearchConfig:
    desired_papers: int = 10
    min_relevance_score: float = 0.85
    max_iterations: int = 5
    max_urls_per_query: int = 3
    months_lookback: int = 12  # How many months back to consider papers


def get_date_range():
    """Get current date and lookback date for paper filtering."""
    current_date = datetime.now()
    lookback_date = current_date - timedelta(days=365)  # 1 year lookback
    return current_date, lookback_date


def format_date_for_query(date: datetime) -> str:
    """Format date for search queries."""
    return date.strftime("%Y-%m")


def compute_paper_hash(title: str, summary: str) -> str:
    """Compute a hash for paper deduplication based on title and summary."""
    content = (title + summary).lower()
    return hashlib.md5(content.encode()).hexdigest()


def is_duplicate_paper(paper: ResearchSummary, existing_papers: List[ResearchSummary]) -> bool:
    """Check if a paper is a duplicate using fuzzy matching on title and content."""
    paper_title_lower = paper.title.lower()
    for existing in existing_papers:
        existing_title_lower = existing.title.lower()
        if (paper_title_lower in existing_title_lower or
            existing_title_lower in paper_title_lower or
            paper.paper_hash == existing.paper_hash):
            return True
    return False


def fetch_urls(queries: List[str], config: ResearchConfig) -> List[str]:
    """Fetch URLs from Google, refining for academic sources."""
    urls = set()
    for query in queries:
        urls.update(google(query + " arxiv papers only", config.max_urls_per_query))
    return list(urls)


def generate_search_queries(user_query: str,llm) -> List[str]:
    """Generate initial search queries with date restrictions."""
    current_date, lookback_date = get_date_range()
    date_range = f"after:{format_date_for_query(lookback_date)}"

    system_prompt = f"""
        You are a research assistant helping to find relevant academic papers.
        Generate 5 precise search queries for finding recent academic papers based on the user's query.
        Focus on papers published after {format_date_for_query(lookback_date)}.
        Current date is {format_date_for_query(current_date)}.

        Guidelines for query generation:
        1. Create diverse queries covering different aspects of the topic
        2. Focus on technical and academic content
        3. Target recent research papers and developments
        4. Include relevant academic keywords and terms
        5. Avoid overly broad or generic searches
        """

    prompt = f"""
        User query: {user_query}
        Generate 5 diverse academic search queries that will find recent papers about this topic.
        Each query should focus on different aspects or approaches to the research question.
        Ensure queries are specific enough to return academic papers rather than general articles.
        Return as a  list.
        """

    queries: SearchQueries = llm(
        system_prompt=system_prompt,
        prompt=prompt,
        response_format=SearchQueries
    )

    # Append date restriction to each query
    return [f"{query} {date_range}" for query in queries.queries]


def generate_focused_queries(
    user_query: str,
    filtered_papers: List[ResearchSummary],
    discarded_papers: List[ResearchSummary],
    llm
) -> List[str]:
    """Generate refined search queries with date restrictions."""
    current_date, lookback_date = get_date_range()
    date_range = f"after:{format_date_for_query(lookback_date)}"

    system_prompt = f"""
        You are a research assistant helping to find academic papers.
        Current date: {format_date_for_query(current_date)}
        Consider papers published after {format_date_for_query(lookback_date)}.

        Rules for academic query generation:
        1. Focus on specific methodologies and implementations
        2. Target technical papers and primary research
        3. Avoid general surveys unless specifically requested
        4. Emphasize recent developments and findings
        5. Use precise academic terminology
        """
    prompt = f"""
    Original research query: {user_query}

    Successfully found papers:
    {[f"{p.title} (score: {p.relevance_score})" for p in filtered_papers]}

    Less relevant papers (too general or off-topic):
    {[f"{p.title} (score: {p.relevance_score})" for p in discarded_papers]}

    Generate 5 refined search queries that:
    1. Build upon the themes of successful papers
    2. Target similar technical depth and specificity
    3. Avoid topics that led to less relevant results
    4. Focus on concrete research findings and methodologies
    Return as a Python list.
    """

    queries: SearchQueries = llm(
        system_prompt=system_prompt,
        prompt=prompt,
        response_format=SearchQueries
    )

    # Append date restriction to each query
    return [f"{query} {date_range}" for query in queries.queries]




def extract_and_summarize(
    user_query:str,
    urls: List[str],
    config: ResearchConfig,
    existing_papers: List[ResearchSummary],
    llm
) -> Tuple[List[ResearchSummary], List[ResearchSummary]]:
    """Parse URLs and summarize content with date-aware relevance criteria."""
    current_date, lookback_date = get_date_range()
    responses = [c for c in parse(urls) if c.content]

    def summarize(response):
        system_prompt = f"""
        You are a strict academic paper evaluator.
        Current date: {format_date_for_query(current_date)}

        Scoring criteria (0-1 scale):
        1.0: Ground-breaking paper with novel methods in the target field (after {format_date_for_query(lookback_date)})
        0.9: Strong research paper with clear methodology and significant findings
        0.85: Good paper with substantial relevance to the query topic
        0.7: Paper is related but not strongly focused on the query topic
        0.5 or lower: General overview or minimal relevance to the query

        Rules:
        - Be strict about relevance to the research query
        - General overview papers should score lower unless specifically requested
        - Papers before {format_date_for_query(lookback_date)} should score lower
        - Emphasize technical depth and research contribution
        """
        relevant_text = wlanswer(response.content,user_query,k=5)

        prompt = (f"URL: {response.url}\n\nContent:\n{relevant_text}\n...\n"
                  "Evaluate this results for the user request that is.\n\n"
                  f"{user_query}\n\n"
                  "Be strict - only high scores for recent papers focused on planning methods.")

        summary = llm(system_prompt=system_prompt, prompt=prompt, response_format=ResearchSummary)
        summary.paper_hash = compute_paper_hash(summary.title, summary.summary)
        return summary

    summaries = []
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(summarize, response) for response in responses]
        for future in futures:
            try:
                summary = future.result()
                if not is_duplicate_paper(summary, existing_papers + summaries):
                    summaries.append(summary)
            except Exception as e:
                print(f"Error processing paper: {e}")

    filtered = [s for s in summaries if s.relevance_score >= config.min_relevance_score]
    discarded = [s for s in summaries if s.relevance_score < config.min_relevance_score]

    filtered.sort(key=lambda x: (x.relevance_score, x.citation_count or 0), reverse=True)
    return filtered, discarded

class Papers(BaseModel):
    filtered_papers:list[ResearchSummary]
    discarded_papers:list[ResearchSummary]

def deepresearcher_processor(user_query: str, config: ResearchConfig = ResearchConfig()) -> Papers:
    """Main research function with date-aware paper filtering."""
    llm = LLM()
    # user_query = QStepper(llm=llm)(user_query)
    # print(f'updated user query: {user_query}')
    # exit()
    print(f"Starting search at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Looking for papers from the last {config.months_lookback} months")

    all_filtered_papers:list[ResearchSummary] = []
    all_discarded_papers:list[ResearchSummary] = []
    iteration = 0

    while (len(all_filtered_papers) < config.desired_papers and
           iteration < config.max_iterations):

        iteration += 1
        print(f"\n=== Iteration {iteration} ===")

        if iteration == 1:
            queries = generate_search_queries(user_query,llm)
        else:
            queries = generate_focused_queries(
                user_query,
                all_filtered_papers,
                all_discarded_papers,
                llm
            )

        print(f"\nGenerated queries for iteration {iteration}:")
        for q in queries:
            print(f"- {q}")

        print("\nFetching URLs...")
        urls = fetch_urls(queries, config)

        print("\nExtracting and summarizing content...")
        filtered_papers, discarded_papers = extract_and_summarize(
            user_query,
            urls,
            config,
            all_filtered_papers,
            llm
        )

        all_filtered_papers.extend(filtered_papers)
        all_discarded_papers.extend(discarded_papers)

        print(f"\nFound {len(filtered_papers)} relevant papers in this iteration")
        print(f"Total relevant papers so far: {len(all_filtered_papers)}")

    print("\n=== Final Research Results ===")
    print(f"Search completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Total iterations: {iteration}")
    print(f"Total relevant papers found: {len(all_filtered_papers)}")
    print(f"Total papers discarded: {len(all_discarded_papers)}")

    # for i, paper in enumerate(all_filtered_papers, 1):
    #     print(f"\n[{i}] {paper.title}")
    #     print(f"🔗 {paper.url}")
    #     print(f"📌 {paper.summary}")
    #     print(f"🔍 Key Findings: {paper.key_findings}")
    #     print(f"📖 Citations: {paper.citation_count}")
    #     print(f"⭐ Relevance Score: {paper.relevance_score}")

    return Papers(
        filtered_papers=all_filtered_papers,
        discarded_papers=all_discarded_papers
    )

def deep_research(
    user_query:str,
    desired_papers:int =30,
    min_relevance_score:float =0.9,
    max_iterations:int =10,
    max_urls_per_query:int =5,
    months_lookback:int =12
) -> Papers:
    config = ResearchConfig(
        desired_papers=desired_papers,
        min_relevance_score=min_relevance_score,
        max_iterations=max_iterations,
        max_urls_per_query=max_urls_per_query,
        months_lookback=months_lookback  # Look back 12 months
    )
    return deepresearcher_processor(
        user_query=user_query,
        config=config
    )


if __name__ == "__main__":
    import os
    os.environ['OPENAI_API_KEY'] = "dsollama"
    user_query = "how llm's can plan i want to know latest papers"
    config = ResearchConfig(
        desired_papers=4,
        min_relevance_score=0.9,
        max_iterations=10,
        max_urls_per_query=3,
        months_lookback=6  # Look back 12 months
    )
    papers = deepresearcher_processor(user_query, config)
    Path('filtered_papers.json').write_text(papers.model_dump_json(indent=2))