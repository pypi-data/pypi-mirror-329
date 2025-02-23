import aiohttp
import json
import asyncio
from typing import Optional, Dict, AsyncGenerator, Union, List, BinaryIO
from dataclasses import dataclass
import os
import mimetypes
from pathlib import Path

@dataclass
class SandboxResponse:
    """Response from sandbox operations.
    
    Attributes:
        success: Whether the operation was successful
        data: Optional response data
        error: Optional error message if operation failed
    """
    success: bool
    data: Optional[Dict] = None
    error: Optional[str] = None

@dataclass
class StreamEvent:
    """Event from streaming code execution.
    
    Attributes:
        type: Type of event ('stdout', 'stderr', 'info', 'error', 'completed', 'keepalive')
        data: Event data
    """
    type: str
    data: str

@dataclass
class FileOperationResponse:
    """Response from file operations.
    
    Attributes:
        success: Whether the operation was successful
        filename: Name of the file
        size: Size of the file in bytes
        path: Path where the file was saved
        message: Optional status message
        error: Optional error message if operation failed
    """
    success: bool
    filename: Optional[str] = None
    size: Optional[int] = None
    path: Optional[str] = None
    message: Optional[str] = None
    error: Optional[str] = None

class SandboxClient:
    """Client for interacting with the AI Sandbox service.
    
    This client provides methods to execute Python code in an isolated sandbox environment.
    It handles authentication, sandbox creation/deletion, and code execution.
    
    Args:
        base_url: The base URL of the sandbox service
        token: Optional pre-existing authentication token
    """
    
    def __init__(
        self,
        base_url: str = "http://aicomputer.dev",
        token: Optional[str] = None
    ):
        self.base_url = base_url.rstrip('/')
        self.token = token
        self.sandbox_id = None
        
    async def setup(self) -> SandboxResponse:
        """Initialize the client and create a sandbox.
        
        This method:
        1. Gets a development token (if not provided)
        2. Creates a new sandbox
        3. Waits for the sandbox to be ready
        
        Returns:
            SandboxResponse indicating success/failure
        """
        async with aiohttp.ClientSession() as session:
            # Get development token if not provided
            if not self.token:
                async with session.post(f"{self.base_url}/dev/token") as response:
                    if response.status == 200:
                        data = await response.json()
                        self.token = data["access_token"]
                    else:
                        text = await response.text()
                        return SandboxResponse(success=False, error=text)
                
            # Create sandbox
            headers = {"Authorization": f"Bearer {self.token}"}
            async with session.post(f"{self.base_url}/api/v1/sandbox/create", headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    self.sandbox_id = data["sandbox_id"]
                    # Wait for sandbox to be ready
                    ready = await self.wait_for_ready()
                    if not ready.success:
                        return ready
                    return SandboxResponse(success=True, data=data)
                else:
                    text = await response.text()
                    return SandboxResponse(success=False, error=text)
    
    async def wait_for_ready(self, max_retries: int = 30, delay: int = 1) -> SandboxResponse:
        """Wait for the sandbox to be in Running state.
        
        Args:
            max_retries: Maximum number of status check attempts
            delay: Delay between retries in seconds
            
        Returns:
            SandboxResponse indicating if sandbox is ready
        """
        if not self.token or not self.sandbox_id:
            return SandboxResponse(success=False, error="Client not properly initialized")
            
        headers = {"Authorization": f"Bearer {self.token}"}
        
        for _ in range(max_retries):
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.base_url}/api/v1/sandbox/{self.sandbox_id}/status",
                    headers=headers
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        if data["status"] == "Running":
                            return SandboxResponse(success=True, data=data)
                    await asyncio.sleep(delay)
        
        return SandboxResponse(success=False, error="Sandbox failed to become ready")
    
    async def execute_code(
        self,
        code: Union[str, bytes],
        timeout: int = 30
    ) -> SandboxResponse:
        """Execute Python code in the sandbox and return the combined output.
        
        This method collects all output from the streaming response and returns it as a single result.
        It captures both stdout and stderr, and handles any errors during execution.
        
        Args:
            code: Python code to execute
            timeout: Maximum execution time in seconds
            
        Returns:
            SandboxResponse containing execution results
        """
        if not self.token or not self.sandbox_id:
            return SandboxResponse(success=False, error="Client not properly initialized. Call setup() first")
            
        # Ensure sandbox is ready
        ready = await self.wait_for_ready()
        if not ready.success:
            return ready
            
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
        
        data = {
            "code": code,
            "timeout": timeout
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/api/v1/sandbox/{self.sandbox_id}/execute",
                    headers=headers,
                    json=data
                ) as response:
                    if response.status != 200:
                        error_text = await response.text()
                        return SandboxResponse(success=False, error=error_text)
                    
                    # Parse the response
                    result = await response.json()
                    return SandboxResponse(success=True, data=result)
                    
        except Exception as e:
            return SandboxResponse(success=False, error=f"Connection error: {str(e)}")
    
    async def execute_code_stream(
        self,
        code: Union[str, bytes],
        timeout: int = 30
    ) -> AsyncGenerator[StreamEvent, None]:
        """Execute Python code in the sandbox and stream the output.
        
        This method returns an async generator that yields StreamEvent objects containing
        the type of event and the associated data.
        
        Args:
            code: Python code to execute
            timeout: Maximum execution time in seconds
            
        Yields:
            StreamEvent objects with execution output/events
        """
        if not self.token or not self.sandbox_id:
            yield StreamEvent(type="error", data="Client not properly initialized. Call setup() first")
            return
            
        # Ensure sandbox is ready
        ready = await self.wait_for_ready()
        if not ready.success:
            yield StreamEvent(type="error", data=ready.error or "Sandbox not ready")
            return
            
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
        
        data = {
            "code": code,
            "timeout": timeout
        }
        
        try:
            # Create a ClientTimeout object with all timeout settings
            timeout_settings = aiohttp.ClientTimeout(
                total=timeout + 30,  # Add buffer for connection overhead
                connect=30,
                sock_connect=30,
                sock_read=timeout + 30
            )
            
            async with aiohttp.ClientSession(timeout=timeout_settings) as session:
                async with session.post(
                    f"{self.base_url}/api/v1/sandbox/{self.sandbox_id}/execute/stream",
                    headers=headers,
                    json=data
                ) as response:
                    if response.status != 200:
                        error_text = await response.text()
                        yield StreamEvent(type="error", data=error_text)
                        return
                        
                    # Process the streaming response
                    async for line in response.content:
                        if line:
                            try:
                                event = json.loads(line.decode())
                                yield StreamEvent(type=event['type'], data=event['data'])
                                
                                # Stop if we receive an error or completed event
                                if event['type'] in ['error', 'completed']:
                                    break
                            except json.JSONDecodeError as e:
                                yield StreamEvent(type="error", data=f"Failed to parse event: {str(e)}")
                                break
                                
        except Exception as e:
            yield StreamEvent(type="error", data=f"Connection error: {str(e)}")
    
    async def execute_shell(
        self,
        command: str,
        args: Optional[List[str]] = None,
        timeout: int = 30
    ) -> SandboxResponse:
        """Execute a shell command in the sandbox.
        
        Args:
            command: The shell command to execute
            args: Optional list of arguments for the command
            timeout: Maximum execution time in seconds
            
        Returns:
            SandboxResponse containing execution results
        """
        if not self.token or not self.sandbox_id:
            return SandboxResponse(success=False, error="Client not properly initialized. Call setup() first")
            
        # Ensure sandbox is ready
        ready = await self.wait_for_ready()
        if not ready.success:
            return ready
            
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
        
        data = {
            "command": command,
            "args": args or [],
            "timeout": timeout
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/api/v1/sandbox/{self.sandbox_id}/execute/shell",
                    headers=headers,
                    json=data
                ) as response:
                    if response.status != 200:
                        error_text = await response.text()
                        return SandboxResponse(success=False, error=error_text)
                    
                    # Parse the response
                    result = await response.json()
                    return SandboxResponse(success=True, data=result)
                    
        except Exception as e:
            return SandboxResponse(success=False, error=f"Connection error: {str(e)}")
    
    async def cleanup(self) -> SandboxResponse:
        """Delete the sandbox.
        
        Returns:
            SandboxResponse indicating success/failure of cleanup
        """
        if not self.token or not self.sandbox_id:
            return SandboxResponse(success=True)
            
        headers = {"Authorization": f"Bearer {self.token}"}
        async with aiohttp.ClientSession() as session:
            async with session.delete(
                f"{self.base_url}/api/v1/sandbox/{self.sandbox_id}",
                headers=headers
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    self.sandbox_id = None
                    return SandboxResponse(success=True, data=data)
                else:
                    text = await response.text()
                    return SandboxResponse(success=False, error=text)

    async def upload_file(
        self,
        file_path: Union[str, Path],
        destination: str = "/workspace",
        chunk_size: int = 1024 * 1024,  # 1MB chunks
        timeout: int = 300  # 5 minutes
    ) -> FileOperationResponse:
        """Upload a file to the sandbox environment.
        
        Args:
            file_path: Path to the file to upload
            destination: Destination path in the sandbox (absolute path starting with /)
            chunk_size: Size of chunks for reading large files
            timeout: Maximum upload time in seconds
            
        Returns:
            FileOperationResponse containing upload results
        """
        if not self.token or not self.sandbox_id:
            return FileOperationResponse(
                success=False,
                error="Client not properly initialized. Call setup() first"
            )

        # Ensure sandbox is ready
        ready = await self.wait_for_ready()
        if not ready.success:
            return FileOperationResponse(
                success=False,
                error=ready.error or "Sandbox not ready"
            )

        # Convert to Path object and validate file
        file_path = Path(file_path)
        if not file_path.exists():
            return FileOperationResponse(
                success=False,
                error=f"File not found: {file_path}"
            )
        
        if not file_path.is_file():
            return FileOperationResponse(
                success=False,
                error=f"Not a file: {file_path}"
            )

        # Get file size and validate
        file_size = file_path.stat().st_size
        if file_size > 100 * 1024 * 1024:  # 100MB limit
            return FileOperationResponse(
                success=False,
                error="File too large. Maximum size is 100MB"
            )

        try:
            # Prepare the upload
            headers = {
                "Authorization": f"Bearer {self.token}"
            }

            # Guess content type
            content_type = mimetypes.guess_type(file_path)[0] or 'application/octet-stream'
            
            # Prepare multipart form data
            data = aiohttp.FormData()
            data.add_field('file',
                         open(file_path, 'rb').read(),
                         filename=file_path.name,
                         content_type=content_type)
            data.add_field('path', destination)

            timeout_settings = aiohttp.ClientTimeout(
                total=timeout,
                connect=30,
                sock_connect=30,
                sock_read=timeout
            )

            async with aiohttp.ClientSession(timeout=timeout_settings) as session:
                async with session.post(
                    f"{self.base_url}/api/v1/sandbox/{self.sandbox_id}/files/upload",
                    headers=headers,
                    data=data
                ) as response:
                    if response.status != 200:
                        error_text = await response.text()
                        return FileOperationResponse(
                            success=False,
                            error=f"Upload failed: {error_text}"
                        )

                    result = await response.json()
                    return FileOperationResponse(
                        success=True,
                        filename=result.get("filename"),
                        size=result.get("size"),
                        path=result.get("path"),
                        message=result.get("message")
                    )

        except asyncio.TimeoutError:
            return FileOperationResponse(
                success=False,
                error=f"Upload timed out after {timeout} seconds"
            )
        except Exception as e:
            return FileOperationResponse(
                success=False,
                error=f"Upload failed: {str(e)}"
            )

    async def download_file(
        self,
        sandbox_path: str,
        local_path: Optional[Union[str, Path]] = None,
        chunk_size: int = 8192,  # 8KB chunks for download
        timeout: int = 300  # 5 minutes
    ) -> FileOperationResponse:
        """Download a file from the sandbox environment.
        
        Args:
            sandbox_path: Path to the file in the sandbox (must be an absolute path starting with /).
                        Any double slashes in the path will be normalized.
            local_path: Local path to save the file (default: current directory with original filename)
            chunk_size: Size of chunks for downloading large files
            timeout: Maximum download time in seconds
            
        Returns:
            FileOperationResponse containing download results
        """
        if not self.token or not self.sandbox_id:
            return FileOperationResponse(
                success=False,
                error="Client not properly initialized. Call setup() first"
            )

        # Ensure sandbox is ready
        ready = await self.wait_for_ready()
        if not ready.success:
            return FileOperationResponse(
                success=False,
                error=ready.error or "Sandbox not ready"
            )

        # Ensure path is absolute and normalize any double slashes
        if not sandbox_path.startswith('/'):
            sandbox_path = f"/{sandbox_path}"
        clean_path = '/'.join(part for part in sandbox_path.split('/') if part)
        clean_path = f"/{clean_path}"
        
        # Determine local path
        if local_path is None:
            local_path = Path(os.path.basename(sandbox_path))
        else:
            local_path = Path(local_path)

        # Create parent directories if they don't exist
        local_path.parent.mkdir(parents=True, exist_ok=True)

        try:
            timeout_settings = aiohttp.ClientTimeout(
                total=timeout,
                connect=30,
                sock_connect=30,
                sock_read=timeout
            )

            headers = {
                "Authorization": f"Bearer {self.token}"
            }

            async with aiohttp.ClientSession(timeout=timeout_settings) as session:
                async with session.get(
                    f"{self.base_url}/api/v1/sandbox/{self.sandbox_id}/files/download{clean_path}",
                    headers=headers
                ) as response:
                    if response.status != 200:
                        error_text = await response.text()
                        return FileOperationResponse(
                            success=False,
                            error=f"Download failed: {error_text}"
                        )

                    # Get content length if available
                    total_size = int(response.headers.get('content-length', 0))

                    # Download the file in chunks
                    downloaded_size = 0
                    try:
                        with open(local_path, 'wb') as f:
                            async for chunk in response.content.iter_chunked(chunk_size):
                                f.write(chunk)
                                downloaded_size += len(chunk)

                        return FileOperationResponse(
                            success=True,
                            filename=local_path.name,
                            size=downloaded_size or total_size,
                            path=str(local_path.absolute()),
                            message="File downloaded successfully"
                        )
                    except Exception as e:
                        # Clean up partial download
                        if local_path.exists():
                            local_path.unlink()
                        raise e

        except asyncio.TimeoutError:
            # Clean up partial download
            if local_path.exists():
                local_path.unlink()
            return FileOperationResponse(
                success=False,
                error=f"Download timed out after {timeout} seconds"
            )
        except Exception as e:
            # Clean up partial download
            if local_path.exists():
                local_path.unlink()
            return FileOperationResponse(
                success=False,
                error=f"Download failed: {str(e)}"
            )

    async def upload_bytes(
        self,
        content: Union[bytes, BinaryIO],
        filename: str,
        destination: str = "/workspace",
        content_type: Optional[str] = None,
        timeout: int = 300  # 5 minutes
    ) -> FileOperationResponse:
        """Upload bytes or a file-like object to the sandbox environment.
        
        Args:
            content: Bytes or file-like object to upload
            filename: Name to give the file in the sandbox
            destination: Destination path in the sandbox (absolute path starting with /)
            content_type: Optional MIME type (will be guessed from filename if not provided)
            timeout: Maximum upload time in seconds
            
        Returns:
            FileOperationResponse containing upload results
        """
        if not self.token or not self.sandbox_id:
            return FileOperationResponse(
                success=False,
                error="Client not properly initialized. Call setup() first"
            )

        # Ensure sandbox is ready
        ready = await self.wait_for_ready()
        if not ready.success:
            return FileOperationResponse(
                success=False,
                error=ready.error or "Sandbox not ready"
            )

        try:
            # Handle both bytes and file-like objects
            if isinstance(content, bytes):
                file_obj = content
                content_length = len(content)
            else:
                # Ensure we're at the start of the file
                if hasattr(content, 'seek'):
                    content.seek(0)
                file_obj = content
                # Try to get content length if possible
                content_length = None
                if hasattr(content, 'seek') and hasattr(content, 'tell'):
                    try:
                        current_pos = content.tell()
                        content.seek(0, os.SEEK_END)
                        content_length = content.tell()
                        content.seek(current_pos)
                    except (OSError, IOError):
                        pass

            # Validate size if we can determine it
            if content_length and content_length > 100 * 1024 * 1024:  # 100MB limit
                return FileOperationResponse(
                    success=False,
                    error="Content too large. Maximum size is 100MB"
                )

            # Prepare the upload
            headers = {
                "Authorization": f"Bearer {self.token}"
            }

            # Guess content type if not provided
            if not content_type:
                content_type = mimetypes.guess_type(filename)[0] or 'application/octet-stream'
            
            # Prepare multipart form data
            data = aiohttp.FormData()
            data.add_field('file',
                         file_obj,
                         filename=filename,
                         content_type=content_type)
            data.add_field('path', destination)

            timeout_settings = aiohttp.ClientTimeout(
                total=timeout,
                connect=30,
                sock_connect=30,
                sock_read=timeout
            )

            async with aiohttp.ClientSession(timeout=timeout_settings) as session:
                async with session.post(
                    f"{self.base_url}/api/v1/sandbox/{self.sandbox_id}/files/upload",
                    headers=headers,
                    data=data
                ) as response:
                    if response.status != 200:
                        error_text = await response.text()
                        return FileOperationResponse(
                            success=False,
                            error=f"Upload failed: {error_text}"
                        )

                    result = await response.json()
                    return FileOperationResponse(
                        success=True,
                        filename=result.get("filename"),
                        size=result.get("size"),
                        path=result.get("path"),
                        message=result.get("message")
                    )

        except asyncio.TimeoutError:
            return FileOperationResponse(
                success=False,
                error=f"Upload timed out after {timeout} seconds"
            )
        except Exception as e:
            return FileOperationResponse(
                success=False,
                error=f"Upload failed: {str(e)}"
            )

    async def download_bytes(
        self,
        sandbox_path: str,
        chunk_size: int = 8192,  # 8KB chunks for download
        timeout: int = 300  # 5 minutes
    ) -> Union[bytes, FileOperationResponse]:
        """Download a file from the sandbox environment into memory.
        
        Args:
            sandbox_path: Path to the file in the sandbox (must be an absolute path starting with /).
                        Any double slashes in the path will be normalized.
            chunk_size: Size of chunks for downloading large files
            timeout: Maximum download time in seconds
            
        Returns:
            On success: The file contents as bytes
            On failure: FileOperationResponse with error details
        """
        if not self.token or not self.sandbox_id:
            return FileOperationResponse(
                success=False,
                error="Client not properly initialized. Call setup() first"
            )

        # Ensure sandbox is ready
        ready = await self.wait_for_ready()
        if not ready.success:
            return FileOperationResponse(
                success=False,
                error=ready.error or "Sandbox not ready"
            )

        # Ensure path is absolute and normalize any double slashes
        if not sandbox_path.startswith('/'):
            sandbox_path = f"/{sandbox_path}"
        clean_path = '/'.join(part for part in sandbox_path.split('/') if part)
        clean_path = f"/{clean_path}"

        try:
            timeout_settings = aiohttp.ClientTimeout(
                total=timeout,
                connect=30,
                sock_connect=30,
                sock_read=timeout
            )

            headers = {
                "Authorization": f"Bearer {self.token}"
            }

            async with aiohttp.ClientSession(timeout=timeout_settings) as session:
                async with session.get(
                    f"{self.base_url}/api/v1/sandbox/{self.sandbox_id}/files/download{clean_path}",
                    headers=headers
                ) as response:
                    if response.status != 200:
                        error_text = await response.text()
                        return FileOperationResponse(
                            success=False,
                            error=f"Download failed: {error_text}"
                        )

                    # Read the entire response into memory
                    content = await response.read()
                    
                    return content

        except asyncio.TimeoutError:
            return FileOperationResponse(
                success=False,
                error=f"Download timed out after {timeout} seconds"
            )
        except Exception as e:
            return FileOperationResponse(
                success=False,
                error=f"Download failed: {str(e)}"
            ) 