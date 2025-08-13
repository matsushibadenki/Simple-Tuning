# src/simple_tuning/chat/server.py
# llama.cppサーバーを起動するラッパー
import subprocess
from ..config import PathConfig

def start_server():
    """llama.cppのサーバーを起動"""
    llama_bin = PathConfig.ROOT / "llama.cpp" / "bin" / "server"
    model_path = PathConfig.GGUF_MODEL
    
    command = [
        str(llama_bin),
        "-m", str(model_path),
        "--host", "127.0.0.1",
        "--port", "8080",
        "-c", "8192",
        "--repeat-penalty", "1.1",
        "--temp", "0.7",
        "--verbose"
    ]
    
    print(f"Starting server with command:\n{' '.join(command)}")
    
    try:
        subprocess.run(command, check=True)
    except FileNotFoundError:
        print(f"Error: '{llama_bin}' not found. Did you build llama.cpp?")
    except subprocess.CalledProcessError as e:
        print(f"Server exited with error: {e}")