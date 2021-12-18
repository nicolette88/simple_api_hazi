from flask import Flask, render_template, request
from flask.json import jsonify

import pickle

app = Flask(__name__)


def readPickleData(inputFileName):
  with open(inputFileName, 'rb') as pickleFile:
    # projekts beolvasása a pickle fileból
    pickleData = pickle.load(pickleFile)
  # a dict többszörösen létrehozta a projects-et azért mélyebb szintől indítottam
  return pickleData[0]


projects = readPickleData('projects.pickle')

# projects = [{
#     'name': 'my project',
#     'tasks': [{
#         'name': 'my task',
#         'completed': False
#     }]
# }]


@app.route('/')
def home():
  name = "Niki"
  return render_template('index.html', user_name=name)


@app.route('/project')
def get_projects():
  return jsonify({'projects': projects})


# @app.route('/project/<string:name>')
# def get_project(name):
#   for project in projects:
#     if project['name'] == name:
#       return jsonify(project)
#   return jsonify({'message': 'project not found'})


@app.route('/project/<string:project_id>')
def get_project(project_id):
  for project in projects:
    if project['project_id'] == project_id:
      return jsonify(project)
  return jsonify({'message': 'project not found'})


@app.route('/project/<string:name>/task')
def get_all_tasks_in_project(name):
  for project in projects:
    if project['name'] == name:
      return jsonify({'tasks': project['tasks']})
  return jsonify({'message': 'project not found'})


@app.route('/project', methods=['POST'])
def create_project():
  # lekérdezzük a http request body-ból a JSON adatot:
  request_data = request.get_json()
  new_project = {'name': request_data['name'], 'tasks': request_data['tasks']}
  projects.append(new_project)
  return jsonify(new_project)


@app.route('/project/<string:name>/task', methods=['POST'])
def add_task_to_project(name):
  request_data = request.get_json()
  for project in projects:
    if project['name'] == name:
      new_task = {
          'name': request_data['name'],
          'completed': request_data['completed']
      }
      project['tasks'].append(new_task)
      return jsonify(new_task)
  return jsonify({'message': 'project not found'})


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000, debug=True)
