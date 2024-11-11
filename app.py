from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Mind Map Generator",
    description="Generate mind maps from Markdown text using Markmap.",
    version="1.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Modify according to your frontend settings
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


class MindMapRequest(BaseModel):
    markdown_text: str


@app.post("/generate_mindmap", response_class=HTMLResponse, tags=["Mind Maps"])
async def generate_mindmap(request: MindMapRequest):
    """
    Generates a mind map HTML using Markmap from Markdown text.

    Args:
        request (MindMapRequest): The request body containing the Markdown text.

    Returns:
        HTMLResponse: The generated mind map in HTML format.
    """

    markdown_text = request.markdown_text
    if not markdown_text:
        raise HTTPException(
            status_code=400, detail="Markdown text is required.")

    # HTML content with embedded Markmap script
    html_content = f"""
        <!DOCTYPE html>
        <html>

        <head>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <meta http-equiv="X-UA-Compatible" content="ie=edge" />
        <title>Markmap Example</title>

        <script src="https://cdn.jsdelivr.net/npm/d3@7.9.0/dist/d3.min.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/markmap-view@0.17.3-alpha.1/dist/browser/index.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/markmap-lib"></script>
        </head>

        <body>
        <svg id="mindmap" style="position: fixed; top: 0; left: 0; width: 100%; height: 100%; background-color: white;"></svg>
        <script>
            const markdownContent = `{markdown_text}`;
    """
    html_content += """const { Transformer } = window.markmap;
            const transformer = new Transformer();
            const { root, features } = transformer.transform(markdownContent);
            const { styles, scripts } = transformer.getUsedAssets(features);
            if (styles) markmap.loadCSS(styles);
            if (scripts) markmap.loadJS(scripts, { getMarkmap: () => markmap });

            const mindmap = markmap.Markmap.create("svg#mindmap", {}, root);
            // mindmap.setData({ content: root });
            mindmap.fit();
        </script>
        </body>

        </html>
    """

    return HTMLResponse(content=html_content)
