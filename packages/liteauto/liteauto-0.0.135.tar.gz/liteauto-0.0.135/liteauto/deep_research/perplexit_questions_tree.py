from litegen import DSLLM
from pydantic import BaseModel
from typing import List, Optional, Dict
from dataclasses import dataclass
from collections import deque


@dataclass
class QuestionNode:
    question: str
    children: List['QuestionNode']
    parent: Optional['QuestionNode'] = None
    depth: int = 0

    def get_path_to_root(self) -> List[str]:
        path = []
        current = self
        while current:
            path.append(current.question)
            current = current.parent
        return list(reversed(path))


class Questions(BaseModel):
    questions: List[str]


class QuestionGeneratorSchema(BaseModel):
    system_prompt: str = """You are an AI specialized in generating hierarchical questions.
    When given a topic and its context (previous questions in the path):
    1. Analyze the topic deeply
    2. Generate questions that logically follow from the context
    3. Ensure questions explore different aspects while maintaining relevance
    4. Consider the depth level to adjust specificity
    Your questions should help build a coherent knowledge tree."""

    user_prompt: str = """Given the topic and its context path: {context_path}
    Generate {num_children} follow-up questions that explore this topic further.
    These questions should naturally follow from the current context path."""

    response_model: BaseModel = Questions


class QuestionTree:
    def __init__(self, max_depth: int = 3, max_children: int = 3):
        self.max_depth = max_depth
        self.max_children = max_children
        self.llm = DSLLM()
        self.root = None

    def _generate_questions(self, context_path: List[str], depth: int) -> List[str]:
        schema = QuestionGeneratorSchema()
        path_str = " -> ".join(context_path)
        schema.user_prompt = schema.user_prompt.format(
            context_path=path_str,
            num_children=self.max_children
        )
        response = self.llm(schema)
        return response.questions[:self.max_children]

    def _build_tree(self, current_node: QuestionNode, depth: int):
        if depth >= self.max_depth:
            return

        # Get path from root to current node
        context_path = current_node.get_path_to_root()

        # Generate child questions based on the full context path
        child_questions = self._generate_questions(context_path, depth)

        # Create child nodes
        for question in child_questions:
            child_node = QuestionNode(
                question=question,
                children=[],
                parent=current_node,
                depth=depth + 1
            )
            current_node.children.append(child_node)

            # Recursively build tree for child node
            self._build_tree(child_node, depth + 1)

    def generate_tree(self, root_question: str):
        self.root = QuestionNode(
            question=root_question,
            children=[],
            depth=0
        )
        self._build_tree(self.root, 0)

    def print_tree(self, node: Optional[QuestionNode] = None, prefix: str = ""):
        if node is None:
            node = self.root

        # Print current node with its path to root
        path = node.get_path_to_root()
        print(f"{prefix}Question: {node.question}")
        print(f"{prefix}Path: {' -> '.join(path)}")
        print(f"{prefix}Depth: {node.depth}\n")

        # Print all children
        for child in node.children:
            self.print_tree(child, prefix + "  ")


# Example usage
if __name__ == "__main__":
    # Create tree with max depth 3 and max 3 children per node
    tree = QuestionTree(max_depth=3, max_children=3)

    # Generate tree from root question
    root_question = "How do neural networks learn from data?"
    tree.generate_tree(root_question)

    # Print the entire tree
    print("Question Tree Structure:")
    print("=" * 50)
    tree.print_tree()