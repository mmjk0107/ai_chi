import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

# 載入環境變數
load_dotenv()

def read_workspace_file(filename):
    """讀取 workspace 資料夾下的檔案，若失敗則報錯並結束。"""
    file_path = Path("workspace") / filename
    if not file_path.exists():
        print(f"❌ 錯誤：找不到必要的檔案 '{file_path}'，請確認該檔案存在於正確位置。", file=sys.stderr)
        sys.exit(1)
    
    try:
        return file_path.read_text(encoding="utf-8")
    except Exception as e:
        print(f"❌ 錯誤：無法讀取檔案 '{file_path}'。細節：{e}", file=sys.stderr)
        sys.exit(1)

def main():
    # 讀取並合併靈魂核心 (System Prompt)
    soul_content = read_workspace_file("SOUL.md")
    agents_content = read_workspace_file("AGENTS.md")
    user_content = read_workspace_file("USER.md")

    # 組合結構化 System Prompt
    system_prompt = f"""
=== SYSTEM SOUL ===
{soul_content}

=== SYSTEM AGENTS ===
{agents_content}

=== SYSTEM USER PREFERENCES ===
{user_content}
"""

    # 初始化 LLM (根據 .env 或預設設定)
    llm = ChatOpenAI(
        model="gemma3:27b",
        base_url="http://203.71.78.31:8000/v1",
        api_key="sk-12345678",
        temperature=0.0,
    )

    # 預設範例任務：分析當前戰局 (這只是一個範例輸入)
    user_input = "我是誰?介紹一下!"

    # 使用串列 (List) 組合傳遞給 LLM 的訊息
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_input),
    ]

    # 持續傳串流輸出
    print("--- 今晚打老虎正在推算中 ---")
    try:
        for chunk in llm.stream(messages):
            print(chunk.content, end="", flush=True)
    except Exception as e:
        print(f"\n❌ LLM 呼叫失敗：{e}", file=sys.stderr)
        sys.exit(1)

    print()  # 結束換行

if __name__ == "__main__":
    main()
