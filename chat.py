import azure.functions as func
import openai
import os
import json

def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        user_msg = req.get_json().get("message", "")

        openai.api_type = "azure"
        openai.api_base = os.environ["https://cogman.openai.azure.com/openai/deployments/gpt-4.1/chat/completions?api-version=2025-01-01-preview"]
        openai.api_version = "2025-01-01"
        AZURE_SEARCH_ADMIN_KEY = "REDACTED"

        response = openai.ChatCompletion.create(
            engine=os.environ["ThinkChat"],
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_msg}
            ]
        )

        reply = response["choices"][0]["message"]["content"]
        return func.HttpResponse(json.dumps({"reply": reply}), mimetype="application/json")

    except Exception as e:
        return func.HttpResponse(str(e), status_code=500)



