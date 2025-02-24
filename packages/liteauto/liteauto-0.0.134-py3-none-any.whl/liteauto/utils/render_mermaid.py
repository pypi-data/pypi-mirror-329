from pathlib import Path

import mermaid as md
from mermaid.graph import Graph
from typing import Dict, Tuple, Optional, Union
import re
from PIL import Image
import io


def analyze_diagram_complexity(mermaid_str: str) -> Dict[str, int]:
    """Analyze the complexity of the Mermaid diagram"""
    # Count number of nodes
    node_count = len(re.findall(r'\["[^"]+"\]', mermaid_str))

    # Count number of connections
    connection_count = len(re.findall(r'-->', mermaid_str))

    # Get max text length in nodes
    node_texts = re.findall(r'\["([^"]+)"\]', mermaid_str)
    max_text_length = max(len(text) for text in node_texts) if node_texts else 0

    # Count levels (approximate depth of the tree)
    lines = mermaid_str.split('\n')
    levels = set()
    for line in lines:
        if '-->' in line:
            parts = line.split('-->')
            levels.update(parts)
    tree_depth = len(levels)

    return {
        'node_count': node_count,
        'connection_count': connection_count,
        'max_text_length': max_text_length,
        'tree_depth': tree_depth
    }


def calculate_optimal_dimensions(complexity: Dict[str, int]) -> Tuple[int, int, float]:
    """Calculate optimal width, height, and scale based on diagram complexity"""
    # Base dimensions
    base_width_per_char = 10
    base_height_per_node = 50
    min_width = 600
    min_height = 400

    # Calculate width based on text length and node count
    width = max(
        min_width,
        complexity['max_text_length'] * base_width_per_char * 1.5,
        complexity['node_count'] * 150
    )

    # Calculate height based on tree depth and node count
    height = max(
        min_height,
        complexity['tree_depth'] * base_height_per_node * 2,
        (complexity['node_count'] / 2) * base_height_per_node
    )

    # Calculate scale based on content density
    content_density = (complexity['node_count'] * complexity['max_text_length']) / (width * height)
    scale = min(3, max(1, 1 + content_density * 1000))

    # Round dimensions to nearest 50 pixels
    width = round(width / 50) * 50
    height = round(height / 50) * 50

    return int(width), int(height), round(scale, 1)


def render_mermaid(
    mermaid_str: str,
    output_path: Optional[Union[str, Path]] = None,
    graph_title: Optional[str] = "Adaptive Solution Tree",
    width:Optional[int]=None,
    height:Optional[int]=None,
    scale:Optional[int]=None
) -> Image.Image:
    """
    Render Mermaid diagram with automatically calculated dimensions and return PIL Image

    Args:
        mermaid_str (str): The Mermaid diagram string
        output_path (Optional[Union[str, Path]]): Path to save PNG file (optional)

    Returns:
        PIL.Image.Image: The rendered diagram as a PIL Image object
    """
    # Create Graph object
    graph = Graph(graph_title, mermaid_str)

    # Analyze diagram complexity
    complexity = analyze_diagram_complexity(mermaid_str)

    # Calculate optimal dimensions
    if width is None or height is None or scale is None:
        width, height, scale = calculate_optimal_dimensions(complexity)

    # print(f"Diagram analysis:")
    # print(f"- Nodes: {complexity['node_count']}")
    # print(f"- Connections: {complexity['connection_count']}")
    # print(f"- Max text length: {complexity['max_text_length']} characters")
    # print(f"- Tree depth: {complexity['tree_depth']}")
    # print(f"\nCalculated dimensions:")
    # print(f"- Width: {width}px")
    # print(f"- Height: {height}px")
    # print(f"- Scale: {scale}")

    # Create Mermaid render
    render = md.Mermaid(
        graph,
        width=width,
        height=height,
        scale=scale,
        position=md.Position.CENTER
    )

    # Get image content
    img_content = render.img_response.content

    # Convert to PIL Image
    img = Image.open(io.BytesIO(img_content))

    # Save if output path is provided
    if output_path:
        img.save(output_path, 'PNG')

    return img

def extract_mermaid(text:str):
    try:
        return re.findall(r"```mermaid\s*(.*?)\s*```", text, flags=re.DOTALL)[0].strip()
    except:
        return None

if __name__ == '__main__':
    # Example usage
    mermaid_str = """
    graph TD
        n0["solve 2+3-5 step by step"]
        n1["First, add 2 and 3 to get 5"]
        n2["Next, subtract 5 from the result"]
        n3["Continue with the subtraction by performing 5-5"]
        n4["Calculate the expression from left to right: start with 2+3"]
        n5["Evaluate the sum of 2 and 3 to get 5"]
        n6["Add the result to -5: perform 2 + 3 + (-5)"]
        n0 --> n1
        n1 --> n2
        n1 --> n3
        n0 --> n4
        n4 --> n5
        n4 --> n6
    """

    # Get PIL Image and optionally save
    img = render_mermaid(mermaid_str, "adaptive_solution_tree.png")

    # Now you can use the PIL Image object directly
    # For example:
    print(f"Image size: {img.size}")
    print(f"Image mode: {img.mode}")

    # You can also manipulate the image using PIL functions
    # For example, resize:
    resized_img = img.resize((800, 600))

    # Or rotate:
    rotated_img = img.rotate(45)

    # Or apply filters, etc.
