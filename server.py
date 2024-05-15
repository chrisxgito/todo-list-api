import uuid
from flask import Flask, request, jsonify, abort


# initialize Flask server
app = Flask(__name__)

# create unique id for lists, entries
todo_list_1_id = '1318d3d1-d979-47e1-a225-dab1751dbe75'
todo_list_2_id = '3062dc25-6b80-4315-bb1d-a7c86b014c65'
todo_list_3_id = '44b02e00-03bc-451d-8d01-0c67ea866fee'
todo_1_id = 'a2f74880-f12e-4969-a6b7-c86928c73507'
todo_2_id = str(uuid.uuid4())
todo_3_id = str(uuid.uuid4())
todo_4_id = str(uuid.uuid4())

# define internal data structures with example data
todo_lists = [
    {'id': todo_list_1_id, 'name': 'Einkaufsliste'},
    {'id': todo_list_2_id, 'name': 'Arbeit'},
    {'id': todo_list_3_id, 'name': 'Privat'},
]
todos = [
    {'id': todo_1_id, 'name': 'Milch', 'description': '', 'list_id': todo_list_1_id},
    {'id': todo_2_id, 'name': 'Arbeitsblätter ausdrucken', 'description': '', 'list_id': todo_list_2_id},
    {'id': todo_3_id, 'name': 'Kinokarten kaufen', 'description': '', 'list_id': todo_list_3_id},]

# add some headers to allow cross origin access to the API on this server, necessary for using preview in Swagger Editor!
@app.after_request
def apply_cors_header(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, DELETE, PATCH'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response

# define endpoint for getting and deleting existing todo lists
@app.route('/todo-list/<list_id>', methods=['GET', 'DELETE'])
def handle_list(list_id):
    # find todo list depending on given list id
    list_item = None
    for l in todo_lists:
        if l['id'] == list_id:
            list_item = l
            break
    # if the given list id is invalid, return status code 404
    if not list_item:
        abort(404)
    if request.method == 'GET':
        # find all todo entries for the todo list with the given id
        print('Returning todo list...')
        return jsonify([i for i in todos if i['list_id'] == list_id])
    elif request.method == 'DELETE':
        # delete list with given id
        print('Deleting todo list...')
        todo_lists.remove(list_item)
        return '', 200


# define endpoint for adding a new list
@app.route('/todo-list', methods=['POST'])
def add_new_list():
    # make JSON from POST data (even if content type is not set correctly)
    new_list = request.get_json(force=True)
    print('Got new list to be added: {}'.format(new_list))
    # create id for new list, save it and return the list with id
    new_list['id'] = uuid.uuid4()
    todo_lists.append(new_list)
    return jsonify(new_list), 200

@app.route('/todo-list/<list_id>/entry', methods=['POST'])
def add_new_entry(list_id):
    # Check if the list exists
    if not any(l['id'] == list_id for l in todo_lists):
        return jsonify({"error": "List not found"}), 404
    new_entry = request.get_json(force=True)
    if not new_entry:
        return jsonify({"error": "No data provided"}), 400
    new_entry['id'] = str(uuid.uuid4())
    new_entry['list_id'] = list_id  # Make sure the key matches other parts of the application

    # Append the new entry to the todos list
    todos.append(new_entry)
    return jsonify(new_entry), 200

@app.route('/todo-list/<list_id>/entry/<entry_id>', methods=['PATCH', 'DELETE'])
def update_or_delete_entry(list_id, entry_id):
    entry = None
    for e in todos:
        if e['id'] == entry_id and e['list_id'] == list_id:
            entry = e
            break
    if not entry:
        abort(404)
    if request.method == 'PATCH':
        updates = request.get_json()
        if 'name' in updates:
            entry['name'] = updates['name']
        if 'description' in updates:
            entry['description'] = updates['description']
        return jsonify(entry), 200
    elif request.method == 'DELETE':
        todos.remove(entry)
        return '', 200

@app.route('/lists', methods=['GET'])
def get_all_lists():
    return jsonify(todo_lists)

if __name__ == '__main__':
    # start Flask server
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
