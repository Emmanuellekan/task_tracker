from datetime import datetime
import os
import json

class Task:

    id : str
    task : str
    description : str
    status : str
    created_on : datetime
    mark_done : datetime
    updated_on: datetime
    DATE_FORMAT = '%y/%m/%d - %H:%M:%S'


    def __init__(self, id, task, description, status, created_on, mark_done):
        self.id = id
        self.task = task
        self.description = description
        self.status = status
        self.created_on = created_on
        self.mark_done = datetime.strptime(mark_done, self.DATE_FORMAT)
        

    def to_json(self):
        return {
            'id' : self.id,
            'task' : self.task,
            'description' : self.description,
            'status' : self.status,
            'created_on' : self.created_on,
            'mark_done' : self.mark_done.strftime(self.DATE_FORMAT),
            'updated_on': None
        }
    

class TaskManager:
    FILENAME = 'task_tracker.json'
    # DATE_FORMAT = '%y/%m/%d - %H:%M:%S'

    def __init__(self):
        self.tasks = self.load_task()
        self.status = 'To-do'
        # self.updated = 'Not updated'

        for i, task in enumerate(self.tasks):
            created_on = datetime.strptime(task['created_on'], '%d/%m/%y %H:%M:%S')
            mark_done = datetime.strptime(task['mark_done'], '%y/%m/%d - %H:%M:%S')
            now = datetime.now()


            # print(f'the date is {created_on.date()}')
            if created_on == now:
                task['status'] = 'To-do'
                

            elif now < mark_done and now > created_on:
                task['status'] = 'In-process'

                # print(f'task expired {now}/ {mark_done} {self.status} ~ { i + 1}')
            else:
                task['status'] = 'Done'
                # print(f'not expired {now}/ {mark_done} {self.status} ~ { i + 1}')

        
            

            



    def load_task(self):
        if not os.path.exists(self.FILENAME):
            return []
        
        else:
            with open(self.FILENAME, 'r') as f:
                return json.load(f)


    def save_task(self, tasks):
        with open(self.FILENAME, 'w') as f:
            return json.dump(tasks, f, indent=4)
        
        
    def add_task(self):

        try:
            task_id = len(self.tasks) + 1
            task = input('Enter task: ')
            description = input('Enter description: ')
            status = self.status
            create_on = datetime.now().strftime('%d/%m/%y %H:%M:%S')
            mark_done = input('Enter date to expire in this format(DD/MM/YY - H/M/S): ')

 
            tasks = Task(task_id, task, description, status, create_on, mark_done)

            self.tasks.append(tasks.to_json())
            
        except (Exception, KeyboardInterrupt) as e:
            print('Error adding task or interrupted by user: ', e)

        self.save_task(self.tasks)

    def update_task(self):

        task_id = int(input('Enter task number to update: '))
        
        try:
            if task_id < 1 or task_id > len(self.tasks):
                print('task not found, try again')
                return
        except ValueError:
            return 'enter a number, try again'

        new_task = input('Enter new task: ')
        new_description = input('Enter new description: ')
        new_expired_date = input('Enter date to expire in this format(YY/MM/DD - H/M/S): ')
        new_status = self.status

        if new_task:
            self.tasks[task_id - 1]['task'] = new_task

        if new_description:
            self.tasks[task_id - 1]['description'] = new_description

        if new_expired_date:
            self.tasks[task_id - 1]['mark_done'] = new_expired_date
        
        if new_status:
            self.tasks[task_id - 1]['status'] = new_status

        self.tasks[task_id - 1]['updated_on'] = datetime.now().strftime('%d/%m/%y %H:%M:%S')

        self.save_task(self.tasks)

    def delete_task(self):
        try:
            task_id = int(input("Enter task to delete: "))
            if task_id < 1 or task_id > len(self.tasks) + 1:
                print('No task found, try again')

            self.tasks.pop(task_id - 1)

            for i, task in enumerate(self.tasks):
                task['id'] = i + 1
        except (ValueError, UnboundLocalError):
            print('Enter number alone')
        

        self.save_task(self.tasks)

taskmanager = TaskManager()

while True:
    print('\n')
    print('1. Add task')
    print('2. Update task')
    print('3. Delete task')
    print('4. View task')
    print('5. Exit')

    try:
        choice = input('Enter -t(task) command follow by action to take: ')

        if choice == '-t add':
            taskmanager.add_task()
        elif choice == '-t update':
            taskmanager.update_task()
        elif choice == '-t delete':
            taskmanager.delete_task()
        elif choice == '-t view':
            tasks = taskmanager.tasks
            for task in tasks:
                print(f'id: {task['id']} - task: {task['task']} - description: {task['description']} - status: {task['status']} - created_on: {task['created_on']}')
        elif choice == '-t exit':
            print('Good bye')
            break


    except ValueError:
        print('Enter a number, try again')
            