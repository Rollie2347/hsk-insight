# ⛓️ HSK Insight — AI-Powered Wallet Analytics on HashKey Chain

> Submitted to the HashKey Chain Horizon Hackathon 2026 | AI Track

## What It Does

HSK Insight is an AI-powered analytics tool for HashKey Chain wallets. Users enter any wallet address and instantly receive:

- **Real-time on-chain data** — HSK balance, transaction count, recent activity
- **AI analysis** — Claude-powered insights on spending patterns, portfolio health, anomalies
- **Natural language Q&A** — Chat interface to ask anything about the wallet ("What's my biggest transaction?", "Am I a DeFi power user?")

## Why HashKey Chain?

HashKey Chain is an EVM-compatible L2 built for regulated finance. HSK Insight bridges the gap between raw on-chain data and human-readable intelligence — making the chain accessible to mainstream users and institutional participants alike.

## Tech Stack

- **Backend:** Python + FastAPI
- **Chain:** HashKey Chain (web3.py, Chain ID 177 / Testnet 133)
- **AI:** Anthropic Claude (claude-3-5-haiku)
- **Frontend:** Vanilla HTML/CSS/JS (no dependencies, runs anywhere)

## Quick Start

```bash
# 1. Clone the repo
git clone https://github.com/YOUR_GITHUB/hsk-insight
cd hsk-insight

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set up environment
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY

# 4. Run the server
cd backend
python app.py

# 5. Open http://localhost:8000
```

## Demo

Enter any HashKey Chain wallet address. Toggle testnet for development wallets.

The AI will:
1. Fetch live on-chain data
2. Analyze patterns and provide insights
3. Answer follow-up questions in natural language

## Tracks

- ✅ **AI Track** — Claude-powered wallet intelligence
- ✅ **PayFi Track** — On-chain payment flow analysis

## Team

Built for the HashKey Chain Horizon Hackathon 2026.
