import azure.functions as func
import openai
import os
import json
import requests

# Function to query Azure Cognitive Search
def query_azure_search(query_text):
    search_endpoint = os.environ["https://cogman.search.windows.net"]  # e.g., https://<your-search-service>.search.windows.net
    index_name = os.environ["vector-1749398608728"]
    search_key = os.environ["LNUBkeLdCqmygIwqrcEoHbhyypewIblwNGP1r1j9npAzSeChsmoh"]

    url = f"{search_endpoint}/indexes/{index_name}/docs/search?api-version=2023-07-01-Preview"
    headers = {
        "Content-Type": "application/json",
        "api-key": search_key
    }
    body = {
        "search": query_text,
        "top": 3  # Number of top documents to retrieve
    }

    response = requests.post(url, headers=headers, json=body)
    results = response.json().get("value", [])

    # Combine the contents of the top documents
    context = "\n".join([doc.get("content", "") for doc in results])
    return context

# Main Azure Function

def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        user_msg = req.get_json().get("message", "")

        # Set OpenAI config
        openai.api_type = "azure"
        openai.api_base = os.environ["https://cogman.openai.azure.com/"]  # e.g., https://<your-resource>.openai.azure.com
        openai.api_version = os.environ["2025-01-01-preview"]  # e.g., 2023-12-01-preview
        openai.api_key = os.environ["4qef0cJNSSBOq0vl4cpzBM7zrUvKtJXGteRVQqZi1uzjNiKv1X7PJQQJ99BFACYeBjFXJ3w3AAABACOGQjq4"]

        # Query indexed data
        context = query_azure_search(user_msg)

        # Call OpenAI with context
        response = openai.ChatCompletion.create(
            engine=os.environ["gpt-4.1"],
            messages=[
                {"role": "system", "content": "You are a helpful assistant. Use the provided context to answer questions."},
                {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {user_msg}"}
            ]
        )

        reply = response["choices"][0]["message"]["content"]
        return func.HttpResponse(json.dumps({"reply": reply}), mimetype="application/json")

    except Exception as e:
        return func.HttpResponse(f"Error: {str(e)}", status_code=500)
