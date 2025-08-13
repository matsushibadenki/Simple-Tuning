# /serve/chat_client.py
# 配置先: gemma3-llamacpp/serve/chat_client.py
#!/usr/bin/env python3
"""
/serve/chat_client.py
"""
import json, sys, urllib.request

def chat(messages, url="http://127.0.0.1:8080/v1/chat/completions"):
    body = json.dumps({
        "model": "gemma3-local",
        "messages": messages,
        "temperature": 0.7,
        "stream": False
    }).encode("utf-8")
    req = urllib.request.Request(url, data=body, headers={"Content-Type":"application/json"})
    with urllib.request.urlopen(req) as r:
        resp = json.loads(r.read())
    return resp["choices"][0]["message"]["content"]

if __name__ == "__main__":
    sys_prompt = "You are a helpful assistant. Answer briefly."
    user = "こんにちは、要約をお願いします。"
    msgs = [{"role":"system","content":sys_prompt},
            {"role":"user","content":user}]
    print(chat(msgs))
