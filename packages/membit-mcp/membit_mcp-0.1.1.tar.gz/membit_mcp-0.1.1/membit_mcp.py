"""
Membit MCP Server
--------------------------------
This FastMCP server exposes three tools that enable access to Membit's API endpoints:
1. clusters_search: Search for trending discussion clusters.
2. clusters_info: Retrieve detailed information (and posts) for a specific cluster.
3. posts_search: Search for raw social posts by keyword.

Before running, create a `.env` file in the same directory with:
    MEMBIT_API_KEY=your_membit_api_key

Visit https://membit.ai/ for more information about Membit's API.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
import httpx
from mcp.server.fastmcp import FastMCP


class MembitSettings(BaseSettings):
    # Define settings to load from .env with prefix MEMBIT_
    model_config = SettingsConfigDict(env_prefix="MEMBIT_", env_file=".env")
    api_key: str


# Load settings
membit_settings = MembitSettings()

# Create FastMCP server instance
mcp = FastMCP("membit-mcp")


@mcp.tool(
    name="clusters_search",
    description="Get trending discussions across social platforms: useful for finding topics of interest and understanding live conversations."
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
        data = response.json()

        result_string = f"Here are clusters of trending discussions related to your query \"{q}\":\n\n"
        for cluster in data.get("clusters", []):
            result_string += f"Label: \"{cluster.get('label', 'N/A')}\"\n"
            result_string += f"Summary: {cluster.get('summary', 'N/A')}\n"
            result_string += f"Engagement Score: {cluster.get('engagement_score', 'N/A')}\n"
            result_string += "---\n"
        result_string += (
            "Next, you may call `cluster_info` tool with the label you're interested in "
            "to dive deeper into each conversation. Make sure to use the exact label."
        )

        return result_string


@mcp.tool(
    name="clusters_info",
    description="Dive deeper into a specific trending discussion cluster: useful for understanding the context and participants of a particular conversation (requires a cluster label from `clusters_search`)."
)
def clusters_info(label: str, limit: int = 10) -> str:
    """
    Tool: Get cluster information and posts.

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
        data = response.json()

        result_string = f"Here's social dicussions around the topic of {label} ({data.get('category', 'Unknown Category')}):\n\n"

        result_string += f"# Summary:\n"
        result_string += f"{data.get('summary', 'N/A')}\n"

        result_string += "\n# Posts:\n---\n"
        for post in data.get("posts", []):
            author = post.get("author", {})
            engagement = post.get("engagement", {})
            mentioned = post.get("mentioned", None)

            result_string += f"URL: {post.get('url', 'N/A')}\n"
            result_string += f"Post Time: {post.get('timestamp', 'N/A')}\n"
            result_string += f"Author: {author.get('name', 'N/A')} ({author.get('handle', 'N/A')})\n"
            result_string += (
                f"Engagement: Likes={engagement.get('likes', 'N/A')}, "
                f"Replies={engagement.get('replies', 'N/A')}, "
                f"Retweets={engagement.get('retweets', 'N/A')}\n"
            )
            result_string += f"Engagement Score: {post.get('engagement_score', 'N/A')}\n"
            result_string += f"\nContent:\n{post.get('content', 'N/A')}\n"

            if mentioned:
                mentioned_author = mentioned.get("author", {})
                result_string += f"\n| Mentioned a Post by {mentioned_author.get('name', 'N/A')} ({mentioned_author.get('handle', 'N/A')}):\n"
                result_string += "\n".join("| " + line for line in mentioned.get(
                    'content', 'N/A').strip().split("\n"))
                result_string += "\n"

            result_string += "---\n"

        result_string += (
            "Review the above posts to gain deeper insights into the conversation cluster. "
            "This information can help you understand the context and key participants involved."
        )

        return result_string


@mcp.tool(
    name="posts_search",
    description="Search for raw social posts: useful when you need to find specific posts (not recommended for finding trending discussions)."
)
def posts_search(q: str, limit: int = 10) -> str:
    """
    Tool: Search for posts.

    Parameters:
      - q: Search keyword.
      - limit: Maximum number of posts to return (default 10).

    Returns:
      - A formatted string with the raw social posts matching the query.
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
        data = response.json()

        result_string = f"Here are raw social posts for your query \"{q}\":\n---\n"

        for post in data.get("posts", []):
            author = post.get("author", {})
            engagement = post.get("engagement", {})
            cluster = post.get("cluster", {})
            mentioned = post.get("mentioned", None)

            result_string += f"URL: {post.get('url', 'N/A')}\n"
            result_string += f"Post Time: {post.get('timestamp', 'N/A')}\n"
            result_string += f"Author: {author.get('name', 'N/A')} ({author.get('handle', 'N/A')})\n"
            result_string += (
                f"Engagement: Likes={engagement.get('likes', 'N/A')}, "
                f"Replies={engagement.get('replies', 'N/A')}, "
                f"Retweets={engagement.get('retweets', 'N/A')}\n"
            )
            result_string += f"Engagement Score: {post.get('engagement_score', 'N/A')}\n"

            if cluster:
                result_string += f"Cluster: label=\"{cluster.get('label', 'N/A')}\" ({cluster.get('summary', 'N/A')})\n"

            result_string += "\nContent:\n"
            result_string += f"{post.get('content', 'N/A')}\n"

            if mentioned:
                mentioned_author = mentioned.get("author", {})
                result_string += f"\n| Mentioned a Post by {mentioned_author.get('name', 'N/A')} ({mentioned_author.get('handle', 'N/A')}):\n"
                result_string += "\n".join("| " + line for line in mentioned.get(
                    'content', 'N/A').strip().split("\n"))
                result_string += "\n"

            result_string += "---\n"

        result_string += (
            "You may call `cluster_info` to dive deeper into the discussions around a similar topic of a post. Make sure to use the exact label."
        )

        return result_string


def main():
    # Run the MCP server. This will use FastMCP's default STDIO transport.
    mcp.run()


if __name__ == "__main__":
    main()
