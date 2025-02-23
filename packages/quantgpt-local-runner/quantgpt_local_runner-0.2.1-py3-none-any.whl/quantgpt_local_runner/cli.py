# cli.py
import typer
import uvicorn
import socket
from typing import Optional

app = typer.Typer()

def find_free_port(start_port: int = 8000, max_attempts: int = 10) -> int:
    """Find a free port starting from start_port."""
    for port in range(start_port, start_port + max_attempts):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('', port))
                return port
        except OSError:
            continue
    raise RuntimeError(f"Could not find a free port after {max_attempts} attempts")

@app.command()
def main(
    port: Optional[int] = typer.Option(8000, help="Port to run the server on"),
    host: Optional[str] = typer.Option("0.0.0.0", help="Host to run the server on"),
    log_level: str = typer.Option("info", help="Logging level")
):
    """Launch the local FastAPI server with WebSocket support"""
    # Get the raw values from Typer's OptionInfo objects
    port_value = port if isinstance(port, int) else port.default
    host_value = host if isinstance(host, str) else host.default
    log_level_value = log_level if isinstance(log_level, str) else log_level.default
    
    try:
        # Try to find a free port if the specified one is taken
        actual_port = find_free_port(port_value)
        if actual_port != port_value:
            typer.echo(f"Port {port_value} is in use, using port {actual_port} instead")
        
        uvicorn.run(
            "quantgpt_local_runner.server:app",
            host=host_value,
            port=actual_port,
            reload=True,
            log_level=log_level_value,
            ws_ping_interval=None,
            ws_ping_timeout=None
        )
    except RuntimeError as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(1)

if __name__ == "__main__":
    app()