from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from dotenv import load_dotenv

load_dotenv()

def main():
    llm = ChatOpenAI(
        model="gemma3:27b",
        base_url="http://203.71.78.31:8000/v1",
        api_key="sk-12345678",
        temperature=0.0,
    )

    system_prompt = """
1. 個人角色設定 (Persona)：
你是一位具備資深硬體知識與資料結構化能力的 AI 資料分析師。你對電腦零組件（CPU 代號、GPU 功耗、螢幕面板技術、I/O 協議）有深刻理解，能識別並校正非結構化文字中的規格邏輯。

2. 情境 (Context)：
我目前正在整理電子商務平台的產品資料庫。原始資料是一段非結構化的筆記型電腦產品描述文字，內容可能包含行銷術語、雜亂的排版或縮寫。我需要將這些感性描述轉化為理性的、可供 API 傳輸的標準資料格式。

3. 任務 (Task)：
請精準提取描述中的規格資訊，並遵循以下處理準則：

數據與單位分離：數值屬性應盡量轉為數字，並將單位體現在鍵值（Key）中（例如：weight_kg: 1.45）。

布林值判斷：針對功能性項目（如：背光鍵盤、指紋辨識、觸控螢幕），請輸出 true 或 false。

清除非事實描述：移除如「極致」、「絕美」、「地表最強」等行銷形容詞，僅保留硬體參數。

缺項處理：若原文未提及該規格，請標註為 null，不要自行臆測。

4. 格式 (Format)：
請提供一個純文字的、結構清晰的 JSON 代碼區塊 (Code Block)，並加上標準縮排。JSON 結構需採用嵌套式設計（Nested Object），將 CPU、GPU、螢幕、連接埠等分類存放。

5. 語氣風格 (Tone)：
專業、精確、邏輯嚴謹。不需要任何開場白或解釋文字，直接輸出 JSON 結果。

6. 範例 (Example)：
輸出的 JSON 結構應參考如下：
{
  "brand": "Manufacturer",
  "model": "Model Name",
  "cpu": { "series": "Intel Core i7", "model": "13700H", "cores": 14 },
  "memory": { "size_gb": 16, "type": "DDR5" },
  "storage": { "capacity_gb": 512, "interface": "NVMe PCIe Gen4" },
  "display": { "size_inch": 14, "resolution": "2880x1800", "refresh_rate_hz": 90, "is_oled": true },
  "io_ports": ["USB-C x2", "HDMI 2.1 x1"]
}
"""

    user_input = """
這款針對電競玩家與內容創作者設計的高性能筆電，
核心運算單元採用八核心架構，其最高運作頻率可達 3.5GHz，
在效能與功耗之間取得平衡。
系統記憶體總容量為 16GB，可支援高強度多工處理與大型遊戲執行。
儲存部分則配置一顆 1TB 容量的 NVMe 規格固態硬碟，
相較於傳統 SATA SSD 具備更快的資料傳輸效率與更低的延遲表現。
"""

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_input),
    ]

    for chunk in llm.stream(messages):
        print(chunk.content, end="", flush=True)

    print()  # 最後換行

if __name__ == "__main__":
    main()
