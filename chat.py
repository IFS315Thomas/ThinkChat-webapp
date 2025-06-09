import azure.functions as func
import openai
import os
import json

def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        user_msg = req.get_json().get("message", "")

        # Azure OpenAI configuration
        openai.api_type = "azure"
        openai.api_base = "https://cogman.openai.azure.com"  # ✅ base URL only
        openai.api_version = "2025-01-01"  # ✅ version only
        openai.api_key = os.environ["AZURE_OPENAI_API_KEY"]  # ✅ stored in Application Settings

        # Chat Completion
        response = openai.ChatCompletion.create(
            engine="ThinkChat",  # ✅ deployment name
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_msg}
            ]
        )

        reply = response["choices"][0]["message"]["content"]
        return func.HttpResponse(json.dumps({"reply": reply}), mimetype="application/json")

    except Exception as e:
        return func.HttpResponse(str(e), status_code=500)
