import json
import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

# Load the data from the q-vercel-python.json file
def load_data():
    file_path = "q-vercel-python.json"
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            return json.load(file)
    return []

# Helper function to get marks by name
def get_marks(names, data):
    result = []
    name_to_marks = {entry["name"]: entry["marks"] for entry in data}
    for name in names:
        result.append(name_to_marks.get(name, None))
    return result

# Main request handler for the API
class RequestHandler(BaseHTTPRequestHandler):
    def _send_json_response(self, data, status_code=200):
        self.send_response(status_code)
        self.send_header("Content-type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def do_GET(self):
        # Load the data from the JSON file
        data = load_data()

        # Parse the query parameters
        query_params = parse_qs(urlparse(self.path).query)
        names = query_params.get("name", [])
        
        if not names:
            self._send_json_response({"error": "No names provided"}, status_code=400)
            return
        
        # Get the marks for the provided names
        marks = get_marks(names, data)
        self._send_json_response({"marks": marks})

# Run the server (for local development testing)
def run(server_class=HTTPServer, handler_class=RequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Server running on port {port}...")
    httpd.serve_forever()

if __name__ == "__main__":
    run()
