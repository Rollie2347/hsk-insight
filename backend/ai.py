from google import genai
from google.genai import types
import os
import json
from typing import Optional, List

SYSTEM_PROMPT = """You are HSK Insight — an AI analyst specialized in HashKey Chain (HSK) on-chain data.
You analyze wallet activity and provide clear, actionable insights for DeFi users.
Be concise, specific, and highlight anything notable (large transfers, unusual patterns, DeFi activity).
Always mention the HSK balance prominently. Use bullet points for clarity.
End with 1-2 actionable recommendations."""

def get_client():
    return genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def analyze_wallet(wallet_data: dict, user_question: Optional[str] = None) -> str:
    client = get_client()
    data_summary = f"""
Wallet Address: {wallet_data['address']}
Network: HashKey Chain ({wallet_data['network']})
HSK Balance: {wallet_data['balance_hsk']:.4f} HSK
Total Transactions (lifetime): {wallet_data['total_tx_count']}
Current Block: {wallet_data['block_number']}

Recent Transactions (up to 10):
{json.dumps(wallet_data['recent_transactions'], indent=2)}
"""
    if user_question:
        prompt = f"Wallet data:\n{data_summary}\n\nUser question: {user_question}\n\nPlease analyze and answer."
    else:
        prompt = f"Please provide a comprehensive analysis of this HashKey Chain wallet:\n{data_summary}"

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        config=types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT),
        contents=prompt
    )
    return response.text

def chat_about_wallet(wallet_data: dict, conversation_history: List[dict], new_message: str) -> str:
    client = get_client()
    context = f"""You have access to this wallet's on-chain data:
Address: {wallet_data['address']}
HSK Balance: {wallet_data['balance_hsk']:.4f} HSK
Total TXs: {wallet_data['total_tx_count']}
Recent TXs: {json.dumps(wallet_data['recent_transactions'], indent=2)}
"""
    history = [
        types.Content(role="user", parts=[types.Part(text=context)]),
        types.Content(role="model", parts=[types.Part(text="Got it, I have the wallet data loaded. What would you like to know?")])
    ]
    for msg in conversation_history:
        role = "user" if msg["role"] == "user" else "model"
        history.append(types.Content(role=role, parts=[types.Part(text=msg["content"])]))
    history.append(types.Content(role="user", parts=[types.Part(text=new_message)]))

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        config=types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT),
        contents=history
    )
    return response.text
