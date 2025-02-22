import os, json, re
import http.client
import pandas as pd

class tools():
    def __init__(self, engine="serper"):
        self.tools_list = [
            {
                "type": "function",
                "function": {
                    "name": "web_search",
                    "description": "Retrieve up-to-date and relevant information from the web. It is used when a query requires real-time updates, external sources, or specific details not available in the agent's pre-existing knowledge.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "words, phrases, or questions that describe what to look for."
                            }
                        },
                        "required": [
                            "query"
                        ],
                        "additionalProperties": False
                    },
                    "strict": True
                }
            }
        ]
        self._functions_dict = {'web_search':web_search}

    def get_tools_tbl(self):
        tools_df = pd.DataFrame([[x['function']["name"],x['function']["description"]]  for x in self.tools_list], columns=['Name', 'Description'])
        return tools_df

    def get_tool(self, tool_name):
        if isinstance(tool_name, list):
            tool_data = [x for x in self.tools_list if x['function']['name'] in tool_name]
        else:
            tool_data = [x for x in self.tools_list if x['function']['name']==tool_name]
        return tool_data

    def get_functions_dict(self, tool_name):
        if isinstance(tool_name, list):
            functions_dict = {k: self._functions_dict[k] for k in tool_name}
        else:
            functions_dict = {tool_name:self._functions_dict[tool_name]}
        return functions_dict



def web_search(query, num=10, engine="serper"):
    if engine=="serper":
        api_key = os.environ["SERPER_API_KEY"]
    else:
        raise ValueError("Engine not supported!")
    conn = http.client.HTTPSConnection("google.serper.dev")
    payload = json.dumps({
    "q": query,
    "num": num
    })
    headers = {
    'X-API-KEY': api_key,
    'Content-Type': 'application/json'
    }
    conn.request("POST", "/search", payload, headers)
    res = conn.getresponse()
    data = json.loads(res.read().decode("utf-8"))

    # Formatted
    results = data.get("organic", [])
    formatted_text = ""

    for result in results:
        formatted_text += f"Title: {result.get('title', 'No Title')}\n"
        formatted_text += f"Link: {result.get('link', 'No Link')}\n"
        formatted_text += f"Snippet: {result.get('snippet', 'No Snippet')}\n"
        formatted_text += f"Date: {result.get('date', 'No Date')}\n"
        formatted_text += f"Position: {result.get('position', 'No Position')}\n\n"    
    return formatted_text


def extract_reply(text, tag='reply'):
    pattern = f'<{tag}>(.*?)</{tag}>'
    match = re.search(pattern, text, re.DOTALL)
    if match:
        return match.group(1)
    else:
        return None    
