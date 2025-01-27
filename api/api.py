import json
import os

def load_student_data():
    try:
        file_path = os.path.join(os.path.dirname(__file__), '..', 'q-vercel-python.json')
        print(f"Loading student data from: {file_path}")  # Log the file path
        
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print("File not found.")
        return None
    except json.JSONDecodeError:
        print("Error decoding JSON.")
        return None
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return None

def handler(request):
    try:
        students_data = load_student_data()

        if students_data is None:
            print("Student data could not be loaded.")
            return json.dumps({"error": "Failed to load student data"}), 500, {"Content-Type": "application/json"}

        query_params = request.query_params
        names = query_params.get('name', [])

        if isinstance(names, str):
            names = [names]  # Ensure names are in a list format

        result = []
        for name in names:
            student = next((s for s in students_data if s['name'] == name), None)
            if student:
                result.append({"name": name, "marks": student["marks"]})
            else:
                result.append({"name": name, "marks": "Not Found"})

        print(f"Returning result: {result}")
        return json.dumps(result), 200, {"Content-Type": "application/json"}
    
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return json.dumps({"error": f"An error occurred: {str(e)}"}), 500, {"Content-Type": "application/json"}
