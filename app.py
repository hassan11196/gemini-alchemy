from fastapi import FastAPI, Form, HTTPException
from fastapi.responses import FileResponse
import graphviz
import re
from pydantic import BaseModel
import mermaid as md
from mermaid.graph import Graph

# Setup CORS
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Mind Map Generator",
    description="Generate mind maps from Markdown text using Graphviz.",
    version="1.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*.github.dev", "localhost", "localhost:3000", "127.0.0.1"],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

class MindMapRequest(BaseModel):
    markdown_text: str

def generate_mind_map_image(markdown_text: str) -> str:
    """
    Generates a mind map image from Markdown text using Graphviz.

    Args:
        markdown_text (str): The Markdown text to convert to a mind map.

    Returns:
        str: The path to the generated mind map image file.
    """

    # Initialize the Graphviz digraph
    # 
    dot = graphviz.Digraph(comment="Mind Map", format="png", 
                            graph_attr={"size": "1920,1080"}) 

    # Parse the markdown to extract headings
    lines = markdown_text.splitlines()
    stack = []

    for line in lines:
        match = re.match(r"^(#+) (.+)", line)
        if match:
            level = len(match.group(1))
            text = match.group(2)

            # Adjust stack to maintain hierarchy
            while len(stack) >= level:
                stack.pop()
            if stack:
                dot.edge(stack[-1], text)  # Connect current node to its parent
            stack.append(text)
            dot.node(text)  # Create a node for the current heading

    # Render the mind map
    try:
        # render the size to at atleast be 400x400
        dot.render(filename="./mindmap", cleanup=True)
    except graphviz.backend.ExecutableNotFound as e:
        raise RuntimeError(
            "Graphviz 'dot' executable not found. Please install Graphviz and ensure 'dot' is in your system PATH."
        ) from e

    return "./mindmap.png"


@app.post(
    "/generate_mindmap",
    responses={200: {"content": {"image/png": {}}}},
    tags=["Mind Maps"],
)
async def generate_mindmap(request: MindMapRequest):
    """
    Generates a mind map image from Markdown text using Graphviz.

    Args:
        request (dict): The request body containing the Markdown text to convert to a mind map.

    Returns:
        The generated mind map image in PNG format.
    """

    markdown_text = request.markdown_text
    if not markdown_text:
        raise HTTPException(status_code=400, detail="Markdown text is required.")

    try:
        image_path = generate_mind_map_image(markdown_text)
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))

    # Return the generated image as a FileResponse
    return FileResponse(image_path, media_type="image/png")
