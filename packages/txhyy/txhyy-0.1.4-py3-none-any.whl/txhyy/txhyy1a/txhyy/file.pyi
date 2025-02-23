# file.pyi

def mkdir(path: str) -> int:
    """Create a directory"""

def rmdir(path: str) -> int:
    """Remove a directory"""

def remove(path: str) -> int:
    """Delete a file"""

def chdir(path: str) -> int:
    """Change working directory"""

def getvar(name: str) -> str | None:
    """Get environment variable"""

def getpath() -> str | None:
    """Get PATH environment variable"""

def command(cmd: str) -> int:
    """Execute system command"""

def pshell(script: str) -> int:
    """Execute shell command"""

def time() -> float:
    """Get current timestamp"""

def ctime(timestamp: int = 0) -> str:
    """Convert timestamp to string"""