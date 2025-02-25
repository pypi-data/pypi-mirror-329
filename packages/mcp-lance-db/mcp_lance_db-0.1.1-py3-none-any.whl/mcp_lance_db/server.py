from mcp.server.fastmcp import FastMCP

# Store notes as a simple key-value dict to demonstrate state management
notes: dict[str, str] = {}

# Create FastMCP server
mcp = FastMCP("mcp-lance-db")

@mcp.resource("note://{name}")
def get_note(name: str) -> str:
    """Get a note's content by name"""
    if name not in notes:
        raise ValueError(f"Note not found: {name}")
    return notes[name]


@mcp.prompt()
def summarize_notes(style: str = "brief") -> str:
    """
    Creates a summary of all notes
    Args:
        style: Style of the summary (brief/detailed)
    """
    detail_prompt = " Give extensive details." if style == "detailed" else ""
    return (
        f"Here are the current notes to summarize:{detail_prompt}\n\n"
        + "\n".join(f"- {name}: {content}" for name, content in notes.items())
    )

@mcp.tool()
async def add_note(name: str, content: str) -> str:
    """
    Add a new note
    Args:
        name: Name of the note
        content: Content of the note
    """
    notes[name] = content
    return f"Added note '{name}' with content: {content}"
