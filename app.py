import logging
import socket
import json

from routes import app
from flask import Flask, request, jsonify
from typing import Dict, List

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

            return jsonify(results), 200
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

# end of first challenge
# ------------------------------------------------------------------------------------

@app.route('/greedymonkey', methods=['POST'])
def greedyMonkey():
    try:
        # Get the JSON data from the request
        data = request.get_json()

        if 'w' in data and 'v' in data and 'f' in data:
            maxW = data['w']
            maxV = data['v']
            f = data['f']

            result = greedyMonkey(maxW, maxV, f)
            responseText = str(result)

            return responseText, 200
        else:
            return "Invalid JSON payload", 400

    except Exception as e:
        logger.error(f"Error processing JSON payload: {str(e)}")
        return "Error processing JSON payload", 500
    
def greedyMonkey(maxW: int, maxV: int, f: List[List[int]]) -> int:
    possibilities = [[0, 0, 0]]
    
    for items in f:
        temp_result = []
        for possible in possibilities:
            newWeight = possible[0] + items[0]
            newVolume = possible[1] + items[1] 
            newValue = possible[2] + items[2] 
            if newWeight <= maxW and newVolume <= maxV:
                temp_result.append([newWeight, newVolume, newValue])

        possibilities.extend(temp_result)

    max_val = 0
    for items in possibilities:
        val = items[2]
        if val > max_val:  
            max_val = val  

    return max_val


#end of Greedy Monkey
# ------------------------------------------------------------------------------------
@app.route('/digital-colony', methods=['POST'])
def digitalColony():
    data = request.get_json()
    responses = []

    for entry in data:
        generations = entry['generations']
        colony = entry['colony']
        result = digitalColonyHelper(generations, colony)
        responses.append(result)

    return jsonify(responses)

def digitalColonyHelper(generations: int, colony: str) -> int:
    while generations > -1:
        colonySize = len(colony)
        weight = sum(map(int, colony))
        weight_last = weight % 10
        j = 1
        first = int(colony[0])
        second = int(colony[1])
        newColony = colony[0];

        while j < colonySize:
            second = int(colony[j])
            difference = first - second if first > second else 10 - (second - first)
            new = (weight_last + difference) % 10
            newColony += str(new);
            newColony += str(second);
            first = second
            j += 1

        generations -= 1
        colony = newColony

    return str(weight)
    
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
