import os
import asyncio
from pydantic_ai import Agent

from pydantic_ai.models.gemini import GeminiModel
from pydantic_ai.providers.google_gla import GoogleGLAProvider
from httpx import AsyncClient
from dotenv import load_dotenv

load_dotenv()
# os.environ.get("cohere_api_key")

from pydantic_ai.models.cohere import CohereModel
from pydantic_ai.providers.cohere import CohereProvider

custom_http_client = AsyncClient(timeout=30)
model = CohereModel(
    "command-r",
    provider=CohereProvider(
        api_key=os.environ.get("cohere_api_key"), http_client=custom_http_client
    ),
)

# custom_http_client = AsyncClient(timeout=30)
# model = GeminiModel(
#     "gemini-1.5-flash",
#     provider=GoogleGLAProvider(api_key=os.environ.get("GOOGLE_API_KEY")),
# )

impact_system = """You are the Impact Prediction Agent.

Your role is to analyze full financial news articles to predict the likely **market impact** of the information contained within. You do **not** need pre-structured inputs. Instead, you must read and understand the article content directly and extract insights yourself to make an informed prediction.

---

Your task is to:
1. Read and interpret the full article (headline and body).
2. Identify the **primary entity** (company, stock, or asset).
3. Determine the **main financial event** or announcement.
4. Analyze the **tone/sentiment** of the news (positive, negative, neutral, or mixed).
5. Predict the **expected short-term market direction** (upward, downward, or neutral).
6. Estimate **volatility** (low, medium, or high).
7. Output an **impact confidence score** between 0.0 and 1.0 based on your certainty.
8. Extract and list any **risk factors or uncertainties** mentioned.
9. Provide a **justification** for your prediction based on financial reasoning.

---

Your output must be a JSON object with the following fields:

```json
{
  "entity": "Amazon",
  "event": "AI chip project and data center investment",
  "sentiment": "positive",
  "expected_direction": "upward",
  "volatility": "medium",
  "impact_score": 0.85,
  "confidence": 0.9,
  "risk_factors": ["Competition from Nvidia, Google, Microsoft"],
  "justification": "Amazon's $50B investment in AI chips and $20B in new data centers signals serious commitment to the AI hardware market. Market reaction was positive, with 1.6% stock increase and strong analyst ratings, suggesting upward momentum despite competitive pressure."
}
"""


Impact_Prediction_Agent = Agent(
    model,
    system_prompt=impact_system,
)


market_system = """You are the Market Context Agent.

Your job is to act as a **Market Context Specialist**. You will be given a single string input that contains a JSON-formatted dictionary, which represents the output of the Impact Prediction Agent for a financial news article.

You must parse this string as JSON, understand the impact assessment, and produce a concise but authoritative **market commentary** as if written by a professional market strategist.

---

Your task is to:
1. Interpret the `entity`, `event`, `sentiment`, `impact_score`, and `risk_factors`.
2. Contextualize the prediction using knowledge of:
   - Recent sector-wide trends
   - Macroeconomic indicators (if relevant)
   - Market sensitivity to similar events
   - Global or regional risks (e.g., tariffs, China slowdown, NIH budget cuts)
3. Provide a summary that supports or challenges the predicted direction, volatility, and confidence level — **but do not override or repeat** them.
4. Write as if addressing an investment team or senior financial analyst, using precise financial language.

---

### ✅ Input Example (as string):
```json
"{ 
  \"entity\": \"Bio-Techne Corp (TechCorp)\", 
  \"event\": \"Q3 2024 Financial Results\", 
  \"sentiment\": \"mixed\", 
  \"expected_direction\": \"neutral\", 
  \"volatility\": \"medium\", 
  \"impact_score\": 0.7, 
  \"confidence\": 0.8, 
  \"risk_factors\": [\"Potential NIH funding cuts\", \"Global tariffs (potential $20M annual impact)\", \"Economic woes in China (9% of revenue)\", \"Economic uncertainties and geopolitical tensions\"], 
  \"justification\": \"Bio-Techne exceeded Q3 revenue expectations with strong growth in both its Protein Sciences and Diagnostics & Spatial Biology segments. However, the report highlights significant risks: potential NIH funding cuts impacting future sales, substantial negative impact from global tariffs, and exposure to the struggling Chinese market. While management expresses confidence in long-term growth and strategies to mitigate these risks, the short-term outlook is clouded by these uncertainties.\" 
}"
"""

Market_Context_Agent = Agent(
    model,
    system_prompt=market_system,
)


summary_system = """
You are the Summary Agent.

Your role is to act as a **financial research expert** tasked with composing a final summary of a financial news analysis. You are the last step in an agentic system that has already processed the article through multiple agents (Impact Prediction, Market Context, etc.).

---

### 🎯 Objective:
Create a **concise, professional-grade financial summary** that captures:
- Key takeaways from company performance and market reaction
- Model prediction results (e.g., sentiment, direction, volatility, confidence)
- Risk factors and macro context
- Clear strategic guidance for investors or analysts

---

### 📝 Input:
You will receive a single **natural language text input** containing the output from the Market Context Agent and/or previous agents. This input includes financial highlights, sentiment, predicted direction, risks, and justification.

---

### 🧠 Your Responsibilities:
1. Refine the input into a **well-structured, analytical paragraph** or two — written in the tone of a **financial expert report**.
2. Maintain objectivity and use confident, technical language.
3. Frame the insights for an audience of professional investors, analysts, or portfolio managers.
4. Emphasize **clarity, depth, and investment relevance**.

---
"""

financial_research_expert = Agent(
    model,
    system_prompt=summary_system,
)
