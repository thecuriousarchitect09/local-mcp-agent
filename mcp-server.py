from fastmcp import FastMCP
import psutil

# Create MCP server
mcp = FastMCP("System Monitor")


@mcp.tool()
def get_cpu_usage() -> str:
    """
    Get the current CPU usage of the local machine.
    Returns CPU usage as a percentage.
    """
    cpu = psutil.cpu_percent(interval=1)

    return f"Current CPU usage: {cpu}%"


@mcp.tool()
def get_memory_available() -> str:
    """
    Get the amount of memory currently available
    on the local machine.
    """
    memory = psutil.virtual_memory()

    available_gb = memory.available / (1024 ** 3)
    total_gb = memory.total / (1024 ** 3)
    used_percent = memory.percent

    return (
        f"Available memory: {available_gb:.2f} GB\n"
        f"Total memory: {total_gb:.2f} GB\n"
        f"Memory usage: {used_percent}%"
    )


if __name__ == "__main__":
    mcp.run(
        transport="http",
        host="127.0.0.1",
        port=8000
    )
