from web_scrap import search_tool
import json
import agents
import asyncio
from datetime import datetime


async def main():
    # query = {
    #     "article_id": "FIN-005",
    #     "headline": "China tech giant ByteDance reports stellar growth, regulatory clouds remain",
    #     "content": "ByteDance, TikTok's parent company, leaked financials show revenue grew 70% to $12",
    #     "published_at": "2024-11-21T18:45:00Z",
    # }

    # query_string = input("Enter your query in JSON format Or Python Dictionaries : ")
    # query = json.loads(query_string)

    print(
        "Enter your query in JSON format or Python dict format (press ENTER twice to finish):"
    )

    # Read multiline input
    lines = []
    while True:
        line = input()
        if line.strip() == "":
            break
        lines.append(line)

    # Combine lines into one string
    query_string = "\n".join(lines)

    try:
        # Try to parse as JSON
        query = json.loads(query_string)
    except json.JSONDecodeError:
        # If it's not valid JSON, try using ast.literal_eval for Python dicts
        import ast

        try:
            query = ast.literal_eval(query_string)
        except Exception as e:
            print("❌ Error parsing input:", e)
            return

    final_query = query["headline"] + query["content"]
    article_report = search_tool(final_query)

    Impact_Prediction_Agent_result = await agents.Impact_Prediction_Agent.run(
        article_report.decode("utf-8")
    )

    Market_Context_Agent_result = await agents.Market_Context_Agent.run(
        Impact_Prediction_Agent_result.output
    )

    financial_research_expert_result = await agents.financial_research_expert.run(
        Market_Context_Agent_result.output
    )

    print("Final Report = ", financial_research_expert_result.output)

    with open("ai_chat_history.txt", "a", encoding="utf-8") as f:
        f.write("\n==================== NEW RUN ====================\n")
        f.write(f"Timestamp: {datetime.now()}\n")
        f.write("Input:\n")
        f.write(json.dumps(query_string, indent=2))
        f.write("\n\nOutput:\n")
        f.write(
            financial_research_expert_result.output
        )  # output is written directly, no conversion
        f.write("\n=================================================\n")


if __name__ == "__main__":
    asyncio.run(main())
# print(await ak(a))
