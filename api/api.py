import json
import os

# Load student data from the JSON file
def load_student_data():
    try:
        # Ensure the file is correctly referenced relative to the location of the Python script
        file_path = os.path.join(os.path.dirname(__file__), '..', 'q-vercel-python.json')  # Path to parent directory
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return None  # Handle case where file is not found
    except json.JSONDecodeError:
        return None  # Handle invalid JSON error

def handler(request):
    try:
        # Load the student data
        students_data = load_student_data()

        # Check if the JSON file was loaded successfully
        if students_data is None:
            return json.dumps({"error": "Failed to load student data"}), 500, {"Content-Type": "application/json"}

        # Get query parameters from the request
        query_params = request.query_params
        names = query_params.get('name', [])  # Get names from query (default to empty list)

        # If the names are passed as a single string, convert to a list
        if isinstance(names, str):
            names = [names]

        # Find the marks for the requested names
        result = []
        for name in names:
            student = next((s for s in students_data if s['name'] == name), None)
            if student:
                result.append({"name": name, "marks": student["marks"]})
            else:
                result.append({"name": name, "marks": "Not Found"})
        
        # Return the result as a JSON response with status code 200
        return json.dumps(result), 200, {"Content-Type": "application/json"}
    
    except Exception as e:
        # Catch any exceptions and return a 500 error with a message
        return json.dumps({"error": f"An error occurred: {str(e)}"}), 500, {"Content-Type": "application/json"}
