from tkinter import Tk, Label, Entry, Button, Listbox, END, messagebox

class CourseManager:
    def __init__(self):
        self.courses = {}

    def add_course_professor(self, course, professor):
        if course in self.courses:
            self.courses[course].append(professor)
        else:
            self.courses[course] = [professor]

    def update_course_professor(self, course, professor):
        if course in self.courses:
            self.courses[course] = [professor]

    def delete_course_professor(self, course):
        if course in self.courses:
            del self.courses[course]

    def load_data(self):
        self.courses = {}
        try:
            with open("datos.txt", "r") as file:
                for line in file:
                    if line.strip():
                        course, professors = line.strip().split("=>")
                        self.courses[course] = professors.split(",")
        except FileNotFoundError:
            messagebox.showwarning("Error", "El archivo 'datos.txt' no existe. Asegúrate de guardar los datos antes de cargarlos.")

    def save_data(self):
        with open("datos.txt", "w") as file:
            for course, professors in self.courses.items():
                file.write(f"{course}=>{','.join(professors)}\n")

class GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestor de Cursos y Profesores")

        self.course_manager = CourseManager()
        self.course_manager.load_data()

        self.course_label = Label(root, text="Curso:")
        self.course_label.grid(row=0, column=0, padx=5, pady=5)
        self.course_entry = Entry(root, width=30)
        self.course_entry.grid(row=0, column=1, padx=5, pady=5)

        self.professor_label = Label(root, text="Profesor(es):")
        self.professor_label.grid(row=1, column=0, padx=5, pady=5)
        self.professor_entry = Entry(root, width=30)
        self.professor_entry.grid(row=1, column=1, padx=5, pady=5)

        self.add_button = Button(root, text="Agregar Curso/Profesor", command=self.add_course_professor)
        self.add_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

        self.course_monitor_label = Label(root, text="Monitor de Cursos")
        self.course_monitor_label.grid(row=3, column=0, padx=5, pady=5)
        self.course_monitor = Listbox(root, width=30)
        self.course_monitor.grid(row=4, column=0, padx=5, pady=5)

        self.professor_monitor_label = Label(root, text="Monitor de Profesores")
        self.professor_monitor_label.grid(row=3, column=1, padx=5, pady=5)
        self.professor_monitor = Listbox(root, width=30)
        self.professor_monitor.grid(row=4, column=1, padx=5, pady=5)

        self.update_button = Button(root, text="Actualizar Curso/Profesores", command=self.update_course_professors)
        self.update_button.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

        self.delete_button = Button(root, text="Eliminar Curso/Profesor", command=self.delete_course_professor)
        self.delete_button.grid(row=6, column=0, columnspan=2, padx=5, pady=5)

        self.course_monitor.bind("<<ListboxSelect>>", self.select_course)

        self.load_data_button = Button(root, text="Cargar Datos", command=self.load_data)
        self.load_data_button.grid(row=7, column=0, columnspan=2, padx=5, pady=5)

        self.update_course_monitor()
        self.update_professor_monitor()

    def add_course_professor(self):
        course = self.course_entry.get()
        professor = self.professor_entry.get()

        if course and professor:
            self.course_manager.add_course_professor(course, professor)
            self.course_entry.delete(0, END)
            self.professor_entry.delete(0, END)
            self.update_course_monitor()
            self.update_professor_monitor()
            self.course_manager.save_data()
        else:
            messagebox.showwarning("Error", "Por favor, ingresa un curso y al menos un profesor.")

    def select_course(self, event):
        selected_index = self.course_monitor.curselection()

        if selected_index:
            self.selected_index = selected_index[0]
            selected_course = self.course_monitor.get(self.selected_index)
            selected_professors = ", ".join(self.course_manager.courses[selected_course])

            self.course_entry.delete(0, END)
            self.course_entry.insert(END, selected_course)

            self.professor_entry.delete(0, END)
            self.professor_entry.insert(END, selected_professors)

            self.update_button.config(state="normal")
            self.delete_button.config(state="normal")
        else:
            self.selected_index = None
            self.course_entry.delete(0, END)
            self.professor_entry.delete(0, END)
            self.update_button.config(state="disabled")
            self.delete_button.config(state="disabled")

    def update_course_professors(self):
        course = self.course_entry.get()
        professor = self.professor_entry.get()

        if self.selected_index is not None and course and professor:
            self.course_manager.update_course_professor(course, professor)
            self.update_course_monitor()
            self.update_professor_monitor()
            self.course_manager.save_data()
            messagebox.showinfo("Éxito", "La línea seleccionada se ha actualizado correctamente.")
        else:
            messagebox.showwarning("Error", "Por favor, selecciona una línea y asegúrate de ingresar un curso y al menos un profesor.")

    def delete_course_professor(self):
        if self.selected_index is not None:
            course = self.course_monitor.get(self.selected_index)
            self.course_manager.delete_course_professor(course)
            self.update_course_monitor()
            self.update_professor_monitor()
            self.course_manager.save_data()
            messagebox.showinfo("Éxito", "La línea seleccionada se ha eliminado correctamente.")
            self.selected_index = None
            self.course_entry.delete(0, END)
            self.professor_entry.delete(0, END)
            self.update_button.config(state="disabled")
            self.delete_button.config(state="disabled")
        else:
            messagebox.showwarning("Error", "Por favor, selecciona una línea para eliminar.")

    def update_course_monitor(self):
        self.course_monitor.delete(0, END)
        for course in self.course_manager.courses.keys():
            self.course_monitor.insert(END, course)

    def update_professor_monitor(self):
        self.professor_monitor.delete(0, END)
        for professors in self.course_manager.courses.values():
            professors_str = ", ".join(professors)
            self.professor_monitor.insert(END, professors_str)

    def load_data(self):
        self.course_manager.load_data()
        self.update_course_monitor()
        self.update_professor_monitor()
        messagebox.showinfo("Carga exitosa", "Los datos se han cargado correctamente.")

    def save_data(self):
        self.course_manager.save_data()
        messagebox.showinfo("Guardado exitoso", "Los datos se han guardado correctamente.")

root = Tk()
gui = GUI(root)
root.mainloop()
