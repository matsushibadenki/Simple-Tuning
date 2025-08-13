# src/simple_tuning/chat/client.py
# チャットクライアント

import json
import urllib.request
from typing import List, Dict, Any

from ..config import ChatConfig

def chat(messages: List[Dict[str, str]], url: str = ChatConfig.SERVER_URL) -> str:
    """チャットAPIにリクエストを送信"""
    body = json.dumps({
        "model": ChatConfig.MODEL_NAME,
        "messages": messages,
        "temperature": 0.7,
        "stream": False
    }).encode("utf-8")

    req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req) as r:
        resp: Dict[str, Any] = json.loads(r.read())

    # --- 型安全性のためのアサーションを追加 ---
    assert "choices" in resp, "API response missing 'choices' key"
    assert isinstance(resp["choices"], list), "'choices' should be a list"
    assert len(resp["choices"]) > 0, "'choices' list is empty"
    
    first_choice = resp["choices"][0]
    assert isinstance(first_choice, dict), "A choice item should be a dict"
    assert "message" in first_choice, "Choice item missing 'message' key"
    
    message = first_choice["message"]
    assert isinstance(message, dict), "'message' should be a dict"
    assert "content" in message, "Message object missing 'content' key"
    
    content = message["content"]
    assert isinstance(content, str), "'content' should be a string"

    return content

def main() -> None:
    """クライアントの実行例"""
    msgs = [
        {"role": "system", "content": ChatConfig.DEFAULT_SYSTEM_PROMPT},
        {"role": "user", "content": ChatConfig.DEFAULT_USER_PROMPT}
    ]
    response = chat(msgs)
    print(response)

if __name__ == "__main__":
    main()