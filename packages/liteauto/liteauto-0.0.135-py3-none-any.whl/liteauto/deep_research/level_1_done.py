from typing import Optional, List, Dict
from pydantic import BaseModel, Field
from litegen import DSLLM
from liteauto import google, parse

from typing import Optional

from litegen import DSLLM
from pydantic import BaseModel
from liteauto import parse
from weblair import google


def get_google_result(query, max_urls=10):
    query = query.replace('"', "")
    res = google(query, max_urls=max_urls, advanced=True)
    return [
        {"url": r.url, "title": r.title, "description": r.description}
        for r in res
    ]


def get_wikipedia_result(query, max_urls=1):  # Reduced max_urls for focused Wikipedia search
    try:
        query = query.replace('"', "")
        res = google(query, max_urls=max_urls, advanced=True)[0]
        content = parse([res.url])[0].content
        res.description = content
        return [
            {"url": res.url, "title": res.title, "description": res.description}
        ]
    except:
        return None


class SubTasks(BaseModel):
    sub_tasks: list[str]


class WikipediaSearchQueries(BaseModel):
    queries: list[str]


class KnowledgeItem(BaseModel):
    url: str
    title: str
    description: str


class SubTaskKnowledge(BaseModel):
    sub_task: str
    knowledge: list[KnowledgeItem]


class DeepResearchKnowledgeBase(BaseModel):
    knowledge_base: list[SubTaskKnowledge]


# *** ADD THIS CLASS DEFINITION ***
class IntentGenSchema(BaseModel):
    system_prompt: str
    user_prompt: str
    response_model: BaseModel = SubTasks


llm = DSLLM()


def generate_sub_tasks(user_query: str) -> list[str]:
    system_prompt = """You are an expert AI research assistant tasked with creating a detailed research plan for a given user query.  This plan should outline the major steps involved in conducting a deep investigation into the topic, going beyond simple search results.

    Here's how you should approach the task:

    1. **Understand the User's Query:** Carefully analyze the user's query to identify the core topic and any specific aspects or nuances mentioned.

    2. **Generate Sub-Tasks:** Break down the main query into a set of focused, manageable sub-tasks. These sub-tasks should represent different facets or perspectives of the main topic. Aim for 5-7 well-defined sub-tasks.  These sub-tasks should be specific questions or areas of inquiry.

    3. **Wikipedia Focus:**  For each sub-task, the plan should include identifying relevant information from Wikipedia.  This will involve crafting specific search queries to target Wikipedia articles.

    4. **Knowledge Base Construction:** The plan should mention the creation of a knowledge base to organize the findings from each sub-task. This will store URLs, titles, descriptions, and potentially extracted content from the Wikipedia articles.

    5. **(Optional, Mention Briefly) Future Steps:**  Briefly mention potential future enhancements, such as:
        *   Extracting the full content of the Wikipedia articles.
        *   Summarizing the extracted content.
        *   Synthesizing information from multiple sources.
        *    Checking sources and cross-referencing the final result with the user query.

    **Output:**
    The output should be ONLY THE LIST OF SUBTASKS, as concise strings in a Python list format. Do *not* output the full plan description. Focus solely on the sub-tasks that will guide the research.

    **Example:**

    If the user query is: "What are the ethical implications of using AI in healthcare?"

    Your output should be something like:

    ```
    [
        "Data privacy and security in AI-driven healthcare",
        "Algorithmic bias and fairness in AI medical diagnoses",
        "Impact of AI on the doctor-patient relationship",
        "Responsibility and accountability for AI-driven medical errors",
        "Access and equity in the distribution of AI healthcare technologies",
        "Informed consent and patient autonomy in AI-assisted treatments"
    ]
    ```
    """

    schema = IntentGenSchema(system_prompt=system_prompt, user_prompt=user_query)
    result: SubTasks = llm(schema)
    return result.sub_tasks


def generate_wikipedia_search_queries(sub_task: str) -> list[str]:
    system_prompt = """You are an expert in crafting Google search queries to find relevant Wikipedia articles.
    Given a sub-task, generate one or more search queries that are highly likely to return Wikipedia pages directly related to that sub-task.
    Be specific and use precise keywords.
    add Wikipedia at the end of query.
    Output should be a list of search queries."""

    schema = IntentGenSchema(system_prompt=system_prompt, user_prompt=sub_task)
    schema.response_model = WikipediaSearchQueries
    result: WikipediaSearchQueries = llm(schema)
    return result.queries


# New models for step-based research
class StepResult(BaseModel):
    search_query: str
    results: List[KnowledgeItem]
    summary: str
    score: float


class ResearchStep(BaseModel):
    step_description: str
    results: Optional[StepResult] = None
    failed_paths: List[str] = []  # Store paths that failed from this step


class StepDecision(BaseModel):
    decision_type: str = Field(description='new_step/backtrack')
    step_index: Optional[int] = Field(description="If backtrack, which step to go back to")
    reasoning: str
    next_step_description: Optional[str] = None


class SubTaskResearch(BaseModel):
    sub_task: str
    wiki_knowledge: List[KnowledgeItem]
    research_steps: List[ResearchStep]


class EvaluateSchema(BaseModel):
    relevance_score: float
    reasoning: str


def generate_first_step(sub_task: str, wiki_knowledge: List[KnowledgeItem]) -> str:
    system_prompt = """Given a research sub-task and Wikipedia knowledge, generate the first logical step to begin investigating this topic.
    The step should be specific and actionable, focusing on gathering concrete information or analyzing specific aspects.
    Output should be a single step description."""

    wiki_summaries = "\n".join([f"- {item.title}: {item.description[:200]}..." for item in wiki_knowledge])
    user_prompt = f"Sub-task: {sub_task}\n\nWikipedia Knowledge:\n{wiki_summaries}"

    schema = IntentGenSchema(
        system_prompt=system_prompt,
        user_prompt=user_prompt
    )
    schema.response_model = None
    return llm(schema)


class PathNode(BaseModel):
    step_description: str
    children: List['PathNode'] = []
    failed_attempts: List[str] = []
    results: Optional[StepResult] = None
    is_complete: bool = False
    parent: Optional['PathNode'] = None  # Add parent reference

    def add_failed_path(self, path: str):
        """Add failed path and propagate to parent nodes"""
        if path not in self.failed_attempts:
            self.failed_attempts.append(path)
            if self.parent:
                self.parent.add_failed_path(path)


def generate_next_step(current_node: PathNode, previous_steps: List[ResearchStep],
                       failed_paths: List[str]) -> StepDecision:
    system_prompt = """Analyze the current research step, its results, and previous steps to determine the next course of action.
    You can either:
    1. Generate a new step to continue the research
    2. Suggest backtracking to a previous step if the current direction seems unproductive

    Consider any failed research paths to avoid repeating unproductive directions.

    Output should be a decision with reasoning and either a next step description or a previous step index.

    for decision types pick one of [new_step,backtrack,done]"""

    steps_history = "\n".join([f"{i}. {step.step_description}" for i, step in enumerate(previous_steps)])
    failed_paths_str = "\n".join(failed_paths)

    current_results_summary = (
        current_node.results.summary
        if current_node.results
        else 'No results yet'
    )
    user_prompt = f"""Current Step: {current_node.step_description}
        Current Results Summary: {current_results_summary}
    Previous Steps:
    {steps_history}

    Failed Research Paths:
    {failed_paths_str}"""

    print('Next step System prompt\n\n')
    print(system_prompt)
    print('\n\n')
    print(user_prompt)
    print('\n\n\n')
    schema = IntentGenSchema(
        system_prompt=system_prompt,
        user_prompt=user_prompt,
    )
    schema.response_model = StepDecision
    return llm(schema)


# Update the function signature to accept named parameters
def generate_search_query(*, current_step: ResearchStep, previous_steps: List[ResearchStep]) -> str:
    """
    Generate a search query based on current step and research history.

    Args:
        current_step: The current research step
        previous_steps: List of previous research steps

    Returns:
        str: A focused search query
    """
    system_prompt = """Generate a specific web search query based on the current research step and its context.
    The query should be focused and use relevant technical terms to find high-quality sources.
    Output should be a single search query string."""

    steps_path = "\n".join([f"{i}. {step.step_description}" for i, step in enumerate(previous_steps)])

    user_prompt = f"""Current Step: {current_step.step_description}

    Research Path:
    {steps_path}"""

    schema = IntentGenSchema(system_prompt=system_prompt, user_prompt=user_prompt)
    schema.response_model = None
    return llm(schema)


def evaluate_search_result(result: KnowledgeItem, step: ResearchStep) -> EvaluateSchema:
    system_prompt = """Evaluate the relevance and quality of a search result for the current research step.
    Consider factors like:
    - Relevance to the specific step
    - Technical depth and accuracy
    - Source credibility

    Output a score between 0 and 1, with reasoning."""

    user_prompt = f"""Research Step: {step.step_description}

    Search Result:
    Title: {result.title}
    Description: {result.description}
    URL: {result.url}"""

    schema = IntentGenSchema(
        system_prompt=system_prompt,
        user_prompt=user_prompt,
    )
    schema.response_model = EvaluateSchema
    return llm(schema)


def summarize_results(results: List[KnowledgeItem], step: ResearchStep) -> str:
    system_prompt = """Create a concise summary of the search results for this research step.
    Focus on key findings, patterns, and insights that are most relevant to the research direction.
    Output should be a paragraph summarizing the key points."""

    results_text = "\n".join([f"- {r.title}: {r.description}" for r in results])
    user_prompt = f"""Research Step: {step.step_description}

    Results to Summarize:
    {results_text}"""

    schema = IntentGenSchema(system_prompt=system_prompt, user_prompt=user_prompt)
    schema.response_model = None
    return llm(schema)


class ResearchPath(BaseModel):
    current_node: PathNode
    path_history: List[PathNode] = []

    def backtrack(self, to_index: int) -> None:
        """Record failed path and reset to previous node"""
        # Record the failed path
        failed_nodes = self.path_history[to_index:]
        failed_path = " -> ".join([node.step_description for node in failed_nodes])

        # Add failed path to the node we're backtracking to and all its ancestors
        self.path_history[to_index].add_failed_path(failed_path)

        # Update path history
        self.path_history = self.path_history[:to_index + 1]
        self.current_node = self.path_history[to_index]

    def add_step(self, step: ResearchStep) -> None:
        """Add new step to research path"""
        new_node = PathNode(
            step_description=step.step_description,
            results=step.results,
            parent=self.current_node  # Set parent reference
        )
        self.current_node.children.append(new_node)
        self.path_history.append(new_node)
        self.current_node = new_node


def research_subtask(sub_task: str, wiki_knowledge: List[KnowledgeItem]) -> SubTaskResearch:
    """
    Conduct research on a specific sub-task using step-by-step exploration with backtracking.

    Args:
        sub_task: The specific research sub-task to investigate
        wiki_knowledge: List of relevant Wikipedia knowledge items

    Returns:
        SubTaskResearch object containing the complete research path and findings
    """
    print('Generating first step ...')
    initial_step = ResearchStep(
        step_description=generate_first_step(sub_task, wiki_knowledge)
    )
    print(f'Step: {initial_step.step_description}')

    # Initialize research path with root node
    root_node = PathNode(
        step_description=initial_step.step_description,
        failed_attempts=[],
        parent=None
    )
    research_path = ResearchPath(
        current_node=root_node,
        path_history=[root_node]
    )

    max_steps = 15  # Prevent infinite loops
    step_count = 0
    max_urls = 5  # Number of search results to retrieve

    while step_count < max_steps:
        print(f'\nStep {step_count + 1}/{max_steps}')

        # Create current research step with complete history
        current_research_step = ResearchStep(
            step_description=research_path.current_node.step_description,
            results=research_path.current_node.results,
            failed_paths=research_path.current_node.failed_attempts
        )

        # Get all previous steps with their failed paths
        previous_research_steps = [
            ResearchStep(
                step_description=node.step_description,
                results=node.results,
                failed_paths=node.failed_attempts
            )
            for node in research_path.path_history[:-1]
        ]

        # Generate and execute search
        search_query = generate_search_query(
            current_step=current_research_step,
            previous_steps=previous_research_steps
        )
        print(f'Search query: {search_query}')

        # Get and evaluate results
        search_results = get_google_result(search_query, max_urls=max_urls)
        print(f'Found {len(search_results)} results')

        verified_results = []
        for result_no, result in enumerate(search_results, 1):
            if result:
                result_item = KnowledgeItem(**result)
                evaluation = evaluate_search_result(result_item, current_research_step)
                print(f'Result {result_no} score: {evaluation.relevance_score:.2f}')

                if evaluation.relevance_score >= 0.7:  # Acceptance threshold
                    verified_results.append(result_item)

        # Update current node with results if any were verified
        if verified_results:
            print('Summarizing verified results...')
            summary = summarize_results(verified_results, current_research_step)
            print(f'Generated summary length: {len(summary)}')
            research_path.current_node.results = StepResult(
                search_query=search_query,
                results=verified_results,
                summary=summary,
                score=sum(
                    evaluate_search_result(r, current_research_step).relevance_score
                    for r in verified_results
                ) / len(verified_results)
            )
            print('Results saved to current node')
            print(f'Saved summary: {summary[:50]}...')

        # Get next decision based on current state
        print('Generating next step decision...')
        decision = generate_next_step(
            current_node=research_path.current_node,
            previous_steps=previous_research_steps,
            failed_paths=research_path.current_node.failed_attempts
        )
        print(f'Decision: {decision.decision_type}')

        if decision.decision_type == "done":
            print('Research complete')
            research_path.current_node.is_complete = True
            break

        elif decision.decision_type == "new_step":
            print('Proceeding to new step')
            new_step = ResearchStep(
                step_description=decision.next_step_description,
                failed_paths=[]
            )
            research_path.add_step(new_step)

        elif decision.decision_type == "backtrack":
            print(f'Backtracking to step {decision.step_index}')
            try:
                if 0 <= decision.step_index < len(research_path.path_history):
                    # Record failed path before backtracking
                    failed_nodes = research_path.path_history[decision.step_index:]
                    failed_path = " -> ".join([
                        node.step_description
                        for node in failed_nodes
                    ])

                    # Add failed path to backtrack node and propagate up
                    target_node = research_path.path_history[decision.step_index]
                    current_node = target_node
                    while current_node:
                        if failed_path not in current_node.failed_attempts:
                            current_node.failed_attempts.append(failed_path)
                        current_node = current_node.parent

                    # Update path history and current node
                    research_path.path_history = research_path.path_history[:decision.step_index + 1]
                    research_path.current_node = target_node

                    print(f'Backtracked successfully. Failed path recorded: {failed_path}')
                else:
                    print(f'Invalid backtrack index {decision.step_index}. Continuing from current step.')
            except Exception as e:
                print(f'Error during backtracking: {str(e)}. Continuing from current step.')

        step_count += 1

    if step_count >= max_steps:
        print('Reached maximum steps limit')

    # Convert final research path to SubTaskResearch
    return SubTaskResearch(
        sub_task=sub_task,
        wiki_knowledge=wiki_knowledge,
        research_steps=[
            ResearchStep(
                step_description=node.step_description,
                results=node.results,
                failed_paths=node.failed_attempts
            )
            for node in research_path.path_history
        ]
    )


def build_knowledge_base(user_query: str) -> List[SubTaskResearch]:
    sub_tasks = generate_sub_tasks(user_query)
    research_results = []

    print('Generated Subtasks...')
    for _ in sub_tasks:
        print(_)

    print()

    for sub_task in sub_tasks:
        print()
        print('*' * 50)
        print(f"Researching sub-task: {sub_task}")
        # Get Wikipedia knowledge
        queries = generate_wikipedia_search_queries(sub_task)
        print('Wikipedia Search queries generated ...')
        print(queries)
        wiki_knowledge = []
        for query in queries:
            results = get_wikipedia_result(query)
            if results:
                wiki_knowledge.append(KnowledgeItem(**results[0]))

        # Conduct step-based research
        print('wiki knowledge added succesfully ...')
        print('Starting research subtask ...')
        sub_task_research = research_subtask(sub_task, wiki_knowledge)
        research_results.append(sub_task_research)

    return research_results


def print_research_results(results):
    """Pretty print the research results"""
    for i, research in enumerate(results, 1):
        print(f"\n{'=' * 80}")
        print(f"SUB-TASK {i}: {research.sub_task}")
        print(f"{'=' * 80}")

        print("\nWIKIPEDIA KNOWLEDGE:")
        for wiki in research.wiki_knowledge:
            print(f"\nTitle: {wiki.title}")
            print(f"URL: {wiki.url}")
            print(f"Description: {wiki.description[:200]}...")

        print("\nRESEARCH STEPS:")
        for j, step in enumerate(research.research_steps, 1):
            print(f"\nStep {j}: {step.step_description}")

            if step.results:
                print(f"\nSearch Query: {step.results.search_query}")
                print(f"Results Summary: {step.results.summary}")
                print(f"Average Score: {step.results.score:.2f}")
                print("\nVerified Sources:")
                for result in step.results.results:
                    print(f"- {result.title} ({result.url})")

            if step.failed_paths:
                print("\nFailed Research Paths:")
                for path in step.failed_paths:
                    print(f"- {path}")


def main():
    # Example research query
    query = """
    Help me find information about machine learning in healthcare, specifically focusing on:
    1. Diagnostic applications
    2. Treatment planning
    3. Patient monitoring
    """

    query = """
        Help me how llm based agents work together to complete a task.
        """

    print("Starting deep research...")
    print(f"Query: {query}\n")

    # Run the research
    results = build_knowledge_base(query)

    # Print results
    print_research_results(results)


if __name__ == "__main__":
    main()