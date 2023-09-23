import logging
import socket
import json

from routes import app
from flask import Flask, request, jsonify

logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route('/', methods=['GET'])
def default_route():
    return 'Python Template'

@app.route('/lazy-developer', methods=['POST'])
def lazy_developer():
    try:
        # Get the JSON data from the request
        data = request.get_json()

        if 'classes' in data and 'statements' in data:
            classes = data['classes']
            statements = data['statements']

            results = getNextProbableWords(classes, statements)

            response = {"status": "success", "message": message}
            return jsonify(response), 200
        else:
            return jsonify({"error": "Invalid JSON payload"}), 400

    except Exception as e:
        logger.error(f"Error processing JSON payload: {str(e)}")
        return jsonify({"error": "Error processing JSON payload"}), 500
    
def getNextProbableWords(classes: List[Dict], statements: List[str]) -> Dict[str, List[str]]:
    results = {}

    def find_variable_names(directory, remaining_statements):
        statementLen = len(remaining_statements)
        # print("lenght = ", statementLen)
        variable_names = []
        if(statementLen == 0):
            return []

        current_statement = remaining_statements[0]
        if(statementLen == 1):
            # print("hi last round")
            # print("the type is: ", type(directory))
            for item in directory:
                # print("the item type is: ", type(item))
                if isinstance(item, str) and item.startswith(current_statement):
                    variable_names.append(item)
                    
        else:
            rest_of_statement = remaining_statements[1:]

            for item in directory:
                if isinstance(item, dict) and current_statement in item:
                    variable_names.extend(find_variable_names(item[current_statement], rest_of_statement))

        return variable_names

                    
    for statement in statements:
        # print(statement)
        variable_names = find_variable_names(classes, statement.split("."))
        variable_names = list(set(variable_names))  # Remove duplicates
        variable_names.sort()
        if len(variable_names) == 0:
           results[statement] = ['']
        else:
            results[statement] = variable_names[:5]

    return results
    
logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter(
    '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

if __name__ == "__main__":
    logging.info("Starting application ...")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('localhost', 8080))
    port = sock.getsockname()[1]
    sock.close()
    app.run(port=port)
