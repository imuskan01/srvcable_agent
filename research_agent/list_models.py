"""Lists Gemini models your key can use. Run: python list_models.py"""
import json, os, urllib.request
key = os.getenv("GEMINI_API_KEY")
req = urllib.request.Request("https://generativelanguage.googleapis.com/v1beta/models?pageSize=200",
                             headers={"x-goog-api-key": key})
for m in json.load(urllib.request.urlopen(req))["models"]:
    if "generateContent" in m.get("supportedGenerationMethods", []):
        print(m["name"].replace("models/", ""))
