from litegen import DSLLM
from pydantic import BaseModel


class ClarificationQuestion(BaseModel):
    question: str
    reason: str  # Why this question is being asked


class ClarificationQuestionsList(BaseModel):
    questions: list[ClarificationQuestion]


class QueryRefiner:
    def __init__(self,llm=None):
        self.llm = llm or DSLLM()
        self.clarification_sp = """You are an AI assistant designed to help users formulate precise search queries.  Instead of rewriting their queries, you ask clarifying questions to understand their needs better.

1. **Analyze the User's Query:**
    - Identify any vague or ambiguous terms (e.g., "best," "agent," "impact").
    - Look for missing information (e.g., specific timeframes, domains, types).
    - Identify any unclear relationships between terms.

2. **Generate Clarifying Questions:**
    - For EACH identified ambiguity or missing piece of information, formulate a clear and concise question.
    - Phrase questions in a user-friendly way.
    - Offer potential options or examples when appropriate (e.g., "Did you mean 'agent' as in 'software agent' or 'real estate agent'?").
    - Focus on getting specific information to resolve the ambiguity.
    - Do not ask more than 5 questions at a time.
    - Ask question only related to query.
    - Do not ask any question to user which is not related to user query.

3. **Output:** Present the clarifying questions in a numbered list.

Example:
User Query: "find best papers about agents"
Clarifying Questions:
  - question: "What criteria define 'best' in this context? (e.g., most cited, most recent, highest rated)"
    reason: "The term 'best' is subjective and needs clarification."
  - question: "What kind of 'agents' are you interested in? (e.g., software agents, AI agents, biological agents)"
    reason: "The term 'agent' is ambiguous and needs context."
  - question:  "Are you looking for papers from a specific time period (e.g., the last year, the last 5 years)?"
    reason: 'It clarifies the timeframe of the question.'
"""

        self.final_query_sp = """You are a Query Refiner. You are given:

1.  The user's original query.
2.  A list of clarifying questions you asked the user.
3.  The user's answers to those questions.

Your task is to generate a SINGLE, refined search query that incorporates the user's answers and resolves any ambiguities.  The refined query should be clear, concise, and directly searchable.

Example:
Original Query: find best papers about agents
Clarifying Questions:
  1. What criteria define 'best' in this context? (e.g., most cited, most recent, highest rated): most cited
  2. What kind of 'agents' are you interested in? (e.g., software agents, AI agents, biological agents): AI agents
Refined Query: find most cited papers about AI agents
"""

    def generate_questions(self, query=None) -> ClarificationQuestionsList:
        questions: ClarificationQuestionsList = self.llm(
            prompt=query,
            system_prompt=self.clarification_sp,
            response_format=ClarificationQuestionsList,
        )
        return questions

    def __call__(self, query: str=None, questions=None, answer=None) -> str:
        if questions is None:
            questions = self.generate_questions(query)
        if questions and questions.questions:
            for i, q in enumerate(questions.questions):
                print(f"{i + 1}. {q.question}")
            answer = answer or input("Your answer: ")  # Get user input
            final_answer = (
                "\n".join([q.question for q in questions.questions])
                + f"\n user answer: {answer}"
            )
            # Construct the prompt for the final query generation
            final_query_prompt = f"""{self.final_query_sp}

Original Query: "{query}"
Clarifying Questions and Answers:
{final_answer}

Refined Query:
"""
            refined_query = self.llm(prompt=final_query_prompt)
            return refined_query
        else:
            return query


if __name__ == "__main__":
    prompts = [
        "go through all todays arxiv papers and find top5 best papers, i am an applied ai research engineer.",
        "how agents learn?",
        "can you find some papers like 3 paeprs i want to knwo about embeddings hwo it works in llm.",
        # Category 1: Basic Ambiguity and Missing Information
        "find best restaurants",  # Tests: Vague "best", missing location/cuisine.
        "impact of climate change",  # Tests: Ambiguous "impact" - type and target?
        "latest news about technology",  # Tests: Vague "technology" - specific area? "Latest" - timeframe?
        "good books to read",  # Tests: Subjective "good" - genre, level, purpose?
        "recipes for dinner",  # Tests: Missing dietary restrictions, cuisine, ingredients, time.

        # Category 2: More Specific, but Still Potentially Ambiguous
        "research papers on quantum computing published recently",  # Tests: "Recently" - timeframe?  Maybe subfields.
        "effects of exercise on mental health",  # Tests: "Exercise" type? Population? "Mental health" aspect?
        "tutorials for learning Python",  # Tests: Tutorial level? Learning goals (data science, web dev)?
        "find information about sustainable agriculture practices",
        # Tests: Clarify "sustainable". Geographic location?

        # Category 3: Domain-Specific Terms and Jargon
        "best practices for DevOps implementation",
        # Tests: DevOps context (cloud, company size, tools)?  Meaning of "best"?
        "analyze sentiment of tweets about TSLA",  # Tests: TSLA is known.  Might ask for timeframe.
        "find papers on GANs and diffusion models",
        # Tests: AI/ML terms are known.  Might ask about applications/aspects.

        # Category 4: Edge Cases and "No Clarification Needed"
        "what is the capital of France?",  # Tests: No clarification needed.
        "list the prime numbers between 1 and 100",  # Tests: No clarification needed.
        "find all papers by Geoffrey Hinton published after 2020",  # Tests: Specific, no clarification.

        # Category 5: Handling Multiple Answers
        "compare different cloud providers",
        # Tests: Ambiguous "compare".  Which providers?  What aspects to compare? (multiple answers)
    ]
    refiner = QueryRefiner(DSLLM())
    for p in prompts:
        print(p)
        refined_query = refiner(p)
        print(refined_query)

