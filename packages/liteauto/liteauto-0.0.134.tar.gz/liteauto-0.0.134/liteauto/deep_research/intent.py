import itertools


from liteauto import google, parse, wlanswer, wlsplit, wltopk
from litegen import LLM
from pydantic import BaseModel


class DoubtNodeOutput(BaseModel):
    is_valid: bool
    feeback_single_line: str


class DoubtNode(BaseModel):
    doubt: str
    understanding: str
    questions: list[str]


class SearchQueryNodeResult(BaseModel):
    query: str
    doubt_nodes: list[DoubtNode] = []
    doubt_nodes_output: list[DoubtNodeOutput] = []


class UnderstandAndDoubts(BaseModel):
    understandings: str
    doubts: list[str]


class LLMAnswerList(BaseModel):
    answers: list[DoubtNode]


class QStepper:
    def __init__(self, llm=None):
        self._llm = LLM() if llm is None else llm

    def _get_understanding_and_doubts(self, query, num_of_doubts=None) -> UnderstandAndDoubts:
        if num_of_doubts is None:
            raise ValueError("num of doubts is None")
        system_prompt = f"""
        Understand the user's query and provide a clear understanding of it in English.
        Then, list {num_of_doubts} meaningful questions that will help clarify any doubts or uncertainties in the user's query.
        """
        return self._llm(prompt=query, system_prompt=system_prompt, response_format=UnderstandAndDoubts)

    def _get_node_with_search_questions(self, understandings, current_doubt, num_questions) -> DoubtNode:
        system_prompt = f"""
        Given the following understandings and current doubt:
        
        the understandings are from user raw query previously.
        
        Understandings:
        
        {understandings}
        

        Generate {num_questions} simple unique meaningful google search questions that will help clarify the user request doubt.
        
        such that after search in google we endup with enough context to clarify the userdoubt.
        
        """

        response: DoubtNode = self._llm(prompt=current_doubt, system_prompt=system_prompt,
                                        response_format=DoubtNode)
        return response

    def _generate_search_queries(self, understandings, doubts, query, each_node_search_questions=None):
        if each_node_search_questions is None:
            raise ValueError('error each node question count')
        results = SearchQueryNodeResult(query=query)
        for doubt in doubts:
            response: DoubtNode = self._get_node_with_search_questions(understandings, doubt,
                                                                       each_node_search_questions)
            print(f'{doubt=}')
            print(f'{response.questions}')
            results.doubt_nodes.append(response)
        return results

    def _get_doubt_node_output(self, doubt_node: DoubtNode, query: str, max_urls=3):
        urls_list = google(doubt_node.questions, max_urls=max_urls)
        urls = itertools.chain.from_iterable(urls_list)
        contents = "\n".join([c.content for c in parse(urls) if c.content])

        chunks = wlsplit(contents)

        relevant_content = set()

        for q in doubt_node.questions:
            relevant_content.update(wltopk(chunks,q,k=5))


        web_result = "\n".join(list(relevant_content))

        system_prompt = f"""
           Based on the understanding and query, determine if the following doubt is valid:
           If the doubt is valid and can be worth exploring further based on the understanding and web result, respond with 'True'. Otherwise, respond with 'False' and feeback line as "".
           If the doubt is invalid and cannot be explore , respond with single feedback line it will help user to not explore in this direction for the user.
           """
        prompt = f"""
        OriginalQuery: {query}
        Understanding: {doubt_node.understanding}
        Doubt: {doubt_node.doubt}
        Web Result: {web_result}
    """
        doubt_output = self._llm(system_prompt=system_prompt, prompt=prompt, response_format=DoubtNodeOutput)
        return doubt_output

    def _get_updated_query(self, search_query_list: SearchQueryNodeResult):
        res = ""
        for d, o in zip(search_query_list.doubt_nodes, search_query_list.doubt_nodes_output):
            res += f"[VALID_EXPLORE] [DIRECTION]{d.doubt}" if o.is_valid else f"[INVALID_EXPLORE] [REASON_TO_LEARN]{o.feeback_single_line}"

        combine_system_prompt = f"""
            Understand the user's query "{search_query_list.query}" and provide a clear rewritten query of it in English.
        """
        prompt = f"""
                The understandings with validations are:
            {res}.
            Rewrite the user's query clearly based on the provided context including all valid explorations make feature rich query.
        """
        updated_query: str = self._llm(system_prompt=combine_system_prompt, prompt=prompt)
        return updated_query

    def __call__(
        self,
        query: str,
        num_of_doubts=2,
        each_node_search_questions=2,
        each_node_search_question_max_urls=1
    ):
        result = self._get_understanding_and_doubts(query, num_of_doubts=num_of_doubts)

        search_query_list: SearchQueryNodeResult = self._generate_search_queries(result.understandings, result.doubts,
                                                                                 query,
                                                                                 each_node_search_questions=each_node_search_questions)

        for node in search_query_list.doubt_nodes:
            search_query_list.doubt_nodes_output.append(self._get_doubt_node_output(node, search_query_list.query,
                                                                                    max_urls=each_node_search_question_max_urls))

        updated_query = self._get_updated_query(search_query_list)

        return updated_query


if __name__ == '__main__':
    query = "when i ran two agents i got issue,i want to leanr about autogen framework exactly aobu this in ther doucmentaitons"
    intent = QStepper(LLM("dsollama"))(query)
    print(intent)
