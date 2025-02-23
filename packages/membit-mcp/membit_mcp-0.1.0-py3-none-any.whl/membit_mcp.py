"""
Membit MCP Server
--------------------------------
This FastMCP server exposes three tools that enable access to Membit's API endpoints:
1. membit-clusters-search: Search for trending discussion clusters.
2. membit-clusters-info: Retrieve detailed information (and posts) for a specific cluster.
3. membit-posts-search: Search for raw social posts by keyword.

Before running, create a `.env` file in the same directory with:
    MEMBIT_API_KEY=your_membit_api_key

Visit https://membit.ai/ for more information about Membit's API.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
import httpx
from mcp.server.fastmcp import FastMCP

# Define settings to load from .env with prefix MEMBIT_


class MembitSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="MEMBIT_", env_file=".env")
    api_key: str


# Load settings
membit_settings = MembitSettings()

# Create FastMCP server instance
mcp = FastMCP("membit-mcp")


@mcp.tool(
    name="membit-clusters-search",
    description="Search for trending discussion clusters using Membit's API."
)
def clusters_search(q: str, limit: int = 10) -> str:
    """
    Tool: Search for clusters.

    Parameters:
      - q: Search query.
      - limit: Maximum number of clusters to return (default 10).

    Returns:
      - A JSON-formatted string with the search results.
    """
    with httpx.Client() as client:
        response = client.get(
            "https://api-app.membit.ai/clusters/search",
            headers={
                "accept": "application/json",
                "content-type": "application/json",
                "Authorization": f"Bearer {membit_settings.api_key}",
            },
            params={"q": q, "limit": limit},
        )
        response.raise_for_status()
        return response.json()


@mcp.tool(
    name="membit-clusters-info",
    description="Retrieve detailed information and posts for a specific cluster by label using Membit's API."
)
def clusters_info(label: str, limit: int = 10) -> str:
    """
    Tool: Get cluster information.

    Parameters:
      - label: The cluster label.
      - limit: Maximum number of posts to return (default 10).

    Returns:
      - A JSON-formatted string with the cluster details.
    """
    with httpx.Client() as client:
        response = client.get(
            "https://api-app.membit.ai/clusters/info",
            headers={
                "accept": "application/json",
                "content-type": "application/json",
                "Authorization": f"Bearer {membit_settings.api_key}",
            },
            params={"label": label, "limit": limit},
        )
        response.raise_for_status()
        return response.json()


@mcp.tool(
    name="membit-posts-search",
    description="Search for raw social posts by keyword using Membit's API."
)
def posts_search(q: str, limit: int = 10) -> str:
    """
    Tool: Search for posts.

    Parameters:
      - q: Search keyword.
      - limit: Maximum number of posts to return (default 10).

    Returns:
      - A JSON-formatted string with the search results.
    """
    with httpx.Client() as client:
        response = client.get(
            "https://api-app.membit.ai/posts/search",
            headers={
                "accept": "application/json",
                "content-type": "application/json",
                "Authorization": f"Bearer {membit_settings.api_key}",
            },
            params={"q": q, "limit": limit},
        )
        response.raise_for_status()
        return response.json()


def main():
    # Run the MCP server. This will use FastMCP's default STDIO transport.
    mcp.run()


if __name__ == "__main__":
    main()
