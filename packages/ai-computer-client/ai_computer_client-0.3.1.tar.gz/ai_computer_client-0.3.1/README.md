# AI Computer Python Client

Python client library for interacting with the AI Computer Sandbox service.

## Installation

```bash
pip install ai-computer-client
```

## Usage

### Basic Usage

```python
from ai_computer import SandboxClient

async def main():
    # Initialize client
    client = SandboxClient()
    
    # Setup sandbox environment
    await client.setup()
    
    try:
        # Execute code
        result = await client.execute_code("print('Hello, World!')")
        print(result.data["output"])
        
        # Upload a file
        response = await client.upload_file("local/path/to/file.txt")
        if response.success:
            print(f"File uploaded to {response.path}")
        
        # Download a file
        response = await client.download_file(
            "/workspace/file.txt",
            "local/download/path.txt"
        )
        if response.success:
            print(f"File downloaded to {response.path}")
            
        # Work with bytes directly
        content = b"Hello, World!"
        response = await client.upload_bytes(
            content=content,
            filename="hello.txt"
        )
        
        # Download as bytes
        content = await client.download_bytes("/workspace/hello.txt")
        if isinstance(content, bytes):
            print(content.decode())
            
    finally:
        # Cleanup
        await client.cleanup()

# Run with asyncio
import asyncio
asyncio.run(main())
```

### Advanced Usage

```python
# Stream code execution
async for event in client.execute_code_stream("print('Hello')\nprint('World')"):
    if event.type == "stdout":
        print(f"Output: {event.data}")
    elif event.type == "stderr":
        print(f"Error: {event.data}")
    elif event.type == "completed":
        print("Execution completed")

# Upload with custom settings
response = await client.upload_file(
    "file.txt",
    destination="/workspace/custom/path",
    chunk_size=2*1024*1024,  # 2MB chunks
    timeout=600  # 10 minutes
)

# Work with file-like objects
from io import BytesIO

buffer = BytesIO(b"Hello from buffer!")
response = await client.upload_bytes(
    content=buffer,
    filename="buffer.txt",
    content_type="text/plain"
)
```

## Development

### Setup

```bash
# Clone the repository
git clone https://github.com/ai-computer/ai-computer-client-python
cd ai-computer-client-python

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows

# Install development dependencies
pip install -e ".[dev]"
```

### Running Tests

```bash
pytest tests/
```

## License

MIT License 