# Financial News Impact Analyzer

This project is an **AI-based agentic system** that analyzes financial news articles and predicts their market impact. It uses three agents in sequence and saves the final output to a `.txt` file.

---

## 🔧 What It Does

1. **Takes a news article** as input (in JSON format)
2. Uses **Tavly** to fetch related info from the internet
3. Passes the article through 3 agents:
   - `Impact_Prediction_Agent`: Predicts direction, volatility, sentiment
   - `Market_Context_Agent`: Adds market and industry context
   - `Financial_Research_Expert`: Writes a summary like a financial analyst
4. **Saves the summary** in a `.txt` file in the `output/` folder

---

## 📥 Sample Input

```json
{
  "article_id": "FIN-002",
  "headline": "Small biotech CureGen soars on FDA approval, analysts remain skeptical",
  "content": "CureGen (NASDAQ: CURE), a small-cap biotech, received FDA approval for its novel compound...",
  "published_at": "2024-11-01T14:30:00Z"
}
