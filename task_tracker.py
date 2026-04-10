from datetime import datetime, timedelta
import os
import json

class Task:

    id : str
    task : str
    description : str
    status : str
    created_on : datetime
    end_date : datetime
    updated_on: datetime
    DATE_FORMAT = '%y/%m/%d - %H:%M:%S'


    def __init__(self, id, task, description, is_done, status, created_on, end_date, done_at):
        self.id = id
        self.task = task
        self.description = description
        self.is_done = is_done
        self.status = status
        self.created_on = created_on
        self.end_date = datetime.strptime(end_date, self.DATE_FORMAT)
        self.done_at = done_at

    def to_json(self):
        return {
            'id' : self.id,
            'task' : self.task,
            'description' : self.description,
            'is_done' : self.is_done,
            'status' : self.status,
            'created_on' : self.created_on,
            'end_date' : self.end_date.strftime(self.DATE_FORMAT),
            'done_at': self.done_at,
            'updated_on': None
        }
    

class TaskManager:
    FILENAME = 'task_tracker.json'
    DATE_FORMAT = '%y/%m/%d - %H:%M:%S'

    def __init__(self):
        self.tasks = self.load_task()
        self.status = 'To-do'

        for i, task in enumerate(self.tasks):
            created_on = datetime.strptime(task['created_on'], self.DATE_FORMAT)
            end_date = datetime.strptime(task['end_date'], self.DATE_FORMAT)
            now = datetime.now()


            print(f'The current status is {task['status']}')
            if task['is_done']:
                task['status'] = 'Done'
            
            elif now > end_date:
                task['status'] = 'Expired'
            
            else:
                task['status'] = 'In-process'
        

    def load_task(self):
        if not os.path.exists(self.FILENAME):
            return []
        
        if os.path.getsize(self.FILENAME) == 0:
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

            is_done = False

            status = self.status
            create_on = datetime.now().strftime(self.DATE_FORMAT)

            end_date = input('Enter date to expire in this format(YY/MM/DD - H/M/S): ')
            # days = int(input("Enter number of days to complete task: "))
            # end_date = (datetime.now() + timedelta(days=days)).strftime('%d/%m/%y %H:%M:%S')

            done_at = None


            tasks = Task(task_id, task, description, is_done, status, create_on, end_date, done_at)

            self.tasks.append(tasks.to_json())
            
        except (Exception, KeyboardInterrupt) as e:
            print('Error adding task or interrupted by user: ', e)

        self.save_task(self.tasks)


    def mark_done(self) :

        task_id = int(input('which number of task should be marked done: '))

        mark = input('done(true) or not(false): ')

        task = self.tasks[task_id - 1]
        if mark == 'true':
            task['is_done'] = True
        elif mark == 'false':
            task['is_done'] = False


        task['done_at'] = datetime.now().strftime(self.DATE_FORMAT)

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
        # new_status = 

        if new_task:
            self.tasks[task_id - 1]['task'] = new_task

        if new_description:
            self.tasks[task_id - 1]['description'] = new_description

        if new_expired_date:
            self.tasks[task_id - 1]['end_date'] = new_expired_date
        
        # if new_status:
        #     self.tasks[task_id - 1]['status'] = new_status

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
# taskmanager.mark_done()
while True:
    print('\n')
    print('1. Add task')
    print('2. Mark Task')
    print('3. Update task')
    print('4. Delete task')
    print('5. View task')
    print('6. Exit')

    try:
        choice = input('Enter -t(task) command follow by action to take: ')

        if choice == '-t add':
            taskmanager.add_task()
        elif choice == '-t mark':
            taskmanager.mark_done()
        elif choice == '-t update':
            taskmanager.update_task()
        elif choice == '-t delete':
            taskmanager.delete_task()
        elif choice == '-t view':
            tasks = taskmanager.tasks
            for task in tasks:
                print(f"""
                ID: {task['id']}
                Task: {task['task']}
                Description: {task['description']}
                Status: {task['status']}
                Created: {task['created_on']}
                Ends: {task['end_date']}
                -------------------------
                """)
                
        elif choice == '-t exit':
            print('Good bye')
            break


    except ValueError:
        print('Enter a number, try again')
            