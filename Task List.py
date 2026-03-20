import csv
import tkinter as tk
####################################################
"""
data = [
    ["Status", "Task", "Priority"]
]
with open("Tasks.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(data)
with open("Tasks.csv", "r") as f:
    reader = csv.reader(f)
    for row in reader:
        print(row)
"""
####################################################

WINDOW_WIDTH = 320
WINDOW_HEIGHT = 200
class TasksApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Tasks List")

        #self.canvas = tk.Canvas(root, width=WINDOW_WIDTH, height=WINDOW_HEIGHT, bg="white")
        #self.canvas.pack()

        button_frame = tk.Frame(root)
        button_frame.pack(pady=5)
        tk.Button(button_frame, text="Add Task", command=self.add_task).pack(side="left", padx=2)
        tk.Button(button_frame, text="View All Tasks", command=self.view_tasks).pack(side="left", padx=2)
        tk.Button(button_frame, text="Delete Task", command=self.delete_task).pack(side="left", padx=2)
        tk.Button(button_frame, text="Exit", command=self.exit).pack(side="left", padx=2)

    def add_task(self):
        pass

    def view_tasks(self):
        pass

    def delete_task(self):
        pass

    def exit(self):
        quit()

####################################################
if __name__ == "__main__":
    root = tk.Tk()
    app = TasksApp(root)
    root.mainloop()