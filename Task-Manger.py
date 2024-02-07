#Task-Manger

import json

def read_tasks_from_file(filename):
    try:
        with open(filename, 'r') as file:
            tasks = json.load(file)
            return tasks
    except FileNotFoundError:
        return [] 

def display_tasks(tasks):
  print("This is the list of tasks:")
  for task in tasks:
      required_tasks = ', '.join(task['requiredTasks']) if task['requiredTasks'] else 'None'
      print(f"Name: {task['name']}, Description: {task['description']}, Required Tasks: {required_tasks}")


def display_menu():
  print("\nDo you want to: ")
  print("1 - Add a task")
  print("2 - Delete a task")
  print("3 - Update a task")
  print("0 - Submit and exit")

def add_task(tasks):
  name = input("Task name: ")
  description = input("Task description: ")
  display_tasks_names(tasks)
  required_tasks = input("Choose required tasks (separate by comma): ").split(',')
  tasks.append({"name": name, "description": description, "requiredTasks": required_tasks})

def update_task(tasks):
  display_tasks_names(tasks)
  name_to_update = input("Choose the task name to update: ")

  new_name = input("New task name: ")
  new_description = input("New task description: ")
  display_tasks_names(tasks, exclude=name_to_update)
  new_required_tasks = input("Choose required tasks (separate by comma): ").split(',')

  # Update the task and its references in other tasks
  for task in tasks:
      if task['name'] == name_to_update:
          task['name'] = new_name
          task['description'] = new_description
          task['requiredTasks'] = new_required_tasks
      elif name_to_update in task['requiredTasks']:
          task['requiredTasks'].remove(name_to_update)
          task['requiredTasks'].append(new_name)


def delete_task(tasks):
  display_tasks_names(tasks)
  name_to_delete = input("Choose the task name to delete: ")

  # Find the index of the task to delete
  index_to_delete = None
  for i, task in enumerate(tasks):
      if task['name'] == name_to_delete:
          index_to_delete = i
          break

  
  if index_to_delete is not None:
      del tasks[index_to_delete]

  # Remove references to the deleted task in requiredTasks of other tasks
  for task in tasks:
      if name_to_delete in task['requiredTasks']:
          task['requiredTasks'].remove(name_to_delete)

def write_tasks_to_file(filename, tasks):
  with open(filename, 'w') as file:
      json.dump(tasks, file, indent=4)


def display_tasks_names(tasks, exclude=None):
  for i, task in enumerate(tasks):
      if task['name'] != exclude:
          print(f"{i + 1} - {task['name']}")


def topological_sort(tasks):
  def dfs(task):
      if visited.get(task, False):  # If we've already sorted this task, we skip it.
          return
      visited[task] = True  # Mark this task as sorted.
      for dependent_task in graph[task]:  # Look at all the tasks that should come after this task.
          dfs(dependent_task)  # Sort those tasks first.
      order.append(task)  # Once all the later tasks are sorted, add this task to the list.

  graph = build_graph(tasks)  # Build the map of tasks.
  visited = {}  # This keeps track of which tasks we've already sorted.
  order = []  # This will be our final sorted list of tasks.

  for task in tasks:
      if not visited.get(task['name'], False):  # For each task that we haven't sorted yet,
          dfs(task['name'])  # Start sorting from that task.

  order.reverse()  # Reverse the list because we added tasks to the end of the list.
  return order  # This is our final list of tasks, sorted in the order we should do them.

def build_graph(tasks):
  graph = {task['name']: [] for task in tasks}  # Initialize graph with task names
  '''{
    'Task1': ['Task4'],  # Task4 requires Task1
    'Task2': ['Task3', 'Task4'],  # Task3 and Task4 require Task2
    'Task3': ['Task1'],  # Task1 requires Task3
    'Task4': []  # No tasks depend on Task4
}'''
  for task in tasks:
    for required_task in task['requiredTasks']:
        graph[required_task].append(task['name'])  # Add an edge from required task to the task
  return graph



def main():
  tasks = read_tasks_from_file('tasks.txt')

  while True:
      display_tasks(tasks)
      display_menu()
      choice = input("Enter your choice: ")

      if choice == '1':
          add_task(tasks)
      elif choice == '2':
          delete_task(tasks)
      elif choice == '3':
          update_task(tasks)
      elif choice == '0':
          sorted_tasks = topological_sort(tasks)
          print("Here is the ordered list of tasks:")
          for task in sorted_tasks:
              print(task)

          write_tasks_to_file('tasks.txt', tasks)
          write_tasks_to_file('orderedTasks.txt', sorted_tasks)
          print("Tasks have been saved. Exiting program.")
          break


main()


