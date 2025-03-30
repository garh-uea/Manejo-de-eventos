import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry  # Importamos DateEntry para seleccionar la fecha

class GestorTareas:
    def __init__(self, root):
        # Configuración de la ventana principal
        self.root = root
        self.root.title("Gestor de Tareas")
        self.root.geometry("620x480")
        self.root.resizable(True, True)

        # Variables para almacenar datos
        self.var_nueva_tarea = tk.StringVar()  # Variable para el campo de entrada
        self.var_categoria = tk.StringVar()  # Variable para la categoría

        # Crear y configurar widgets
        self._crear_widgets()

        # Configurar estilos
        self._configurar_estilos()

    def _configurar_estilos(self):
        # Configura los estilos de los widgets
        estilo = ttk.Style()
        estilo.configure("TButton", padding=5, relief="flat", font=("Arial", 10))
        estilo.configure("TLabel", font=("Arial", 10))
        estilo.configure("TFrame", background="#f0f0f0")
        estilo.configure("TCombobox", padding=5)

    def _crear_widgets(self):
        # Crea todos los widgets de la interfaz
        # Frame principal
        frame_principal = ttk.Frame(self.root, padding="10")
        frame_principal.pack(fill=tk.BOTH, expand=True)

        # Título
        lbl_titulo = ttk.Label(frame_principal, text="Gestor de Tareas", font=("Arial", 16, "bold"))
        lbl_titulo.pack(pady=10)

        # Frame para entrada
        frame_entrada = ttk.Frame(frame_principal)
        frame_entrada.pack(fill=tk.X, pady=5)

        # Etiqueta y campo de entrada
        lbl_nueva_tarea = ttk.Label(frame_entrada, text="Nueva tarea:")
        lbl_nueva_tarea.pack(side=tk.LEFT, padx=5)

        entrada_tarea = ttk.Entry(frame_entrada, textvariable=self.var_nueva_tarea, width=30)
        entrada_tarea.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        entrada_tarea.bind("<Return>", self.añadir_tarea)  # Vincular tecla Enter
        entrada_tarea.focus()  # Se stablecee el foco en el widget del campo de entrada

        # Frame para opciones adicionales
        frame_opciones = ttk.Frame(frame_principal)
        frame_opciones.pack(fill=tk.X, pady=5)

        # Menú desplegable de categorías
        categorias = ["Educativa", "Familiar", "Salud", "Financiera", "Deportiva", "Viajes"]
        self.var_categoria.set("Seleccione categoria")  # Valor por defecto
        menu_categorias = ttk.Combobox(frame_opciones, textvariable=self.var_categoria, values=categorias,
                                       state="readonly")
        menu_categorias.pack(side=tk.LEFT, padx=5)

        # Selección de fecha
        self.fecha_tarea = DateEntry(frame_opciones, width=12, background='darkblue', foreground='white', borderwidth=2)
        self.fecha_tarea.pack(side=tk.LEFT, padx=5)

        # Botón para añadir tarea
        btn_añadir = ttk.Button(frame_opciones, text="Añadir Tarea", command=self.añadir_tarea)
        btn_añadir.pack(side=tk.LEFT, padx=5)

        # Frame para la lista de tareas
        frame_lista = ttk.LabelFrame(frame_principal, text="Tareas Pendientes", padding="5")
        frame_lista.pack(fill=tk.BOTH, expand=True, pady=10)

        # Lista de tareas (Treeview)
        columnas = ("estado", "tarea", "categoria", "fecha")
        self.tree_tareas = ttk.Treeview(frame_lista, columns=columnas, show="headings", selectmode="browse")
        self.tree_tareas.heading("estado", text="Estado")
        self.tree_tareas.heading("tarea", text="Tarea")
        self.tree_tareas.heading("categoria", text="Categoría")
        self.tree_tareas.heading("fecha", text="Fecha")

        self.tree_tareas.column("estado", width=100, anchor=tk.CENTER)
        self.tree_tareas.column("tarea", width=200)
        self.tree_tareas.column("categoria", width=100, anchor=tk.CENTER)
        self.tree_tareas.column("fecha", width=100, anchor=tk.CENTER)

        self.tree_tareas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Scrollbar para la lista
        scrollbar = ttk.Scrollbar(frame_lista, orient=tk.VERTICAL, command=self.tree_tareas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree_tareas.configure(yscrollcommand=scrollbar.set)

        # Frame para botones de acción
        frame_botones = ttk.Frame(frame_principal)
        frame_botones.pack(fill=tk.X, pady=5)

        # Botones de acción
        btn_completar = ttk.Button(frame_botones, text="Marcar como Completada", command=self.marcar_completada)
        btn_completar.pack(side=tk.LEFT, padx=5)

        btn_editar = ttk.Button(frame_botones, text="Editar Tarea", command=self.editar_tarea)
        btn_editar.pack(side=tk.LEFT, padx=5)

        btn_eliminar = ttk.Button(frame_botones, text="Eliminar Tarea", command=self.eliminar_tarea)
        btn_eliminar.pack(side=tk.LEFT, padx=5)

    def añadir_tarea(self, event=None):
        # Añade una nueva tarea a la lista
        texto_tarea = self.var_nueva_tarea.get().strip()
        categoria = self.var_categoria.get()
        fecha = self.fecha_tarea.get()

        if not texto_tarea:
            messagebox.showwarning("Advertencia", "Por favor, ingrese una tarea.")
            return

        self.tree_tareas.insert("", tk.END, values=("Pendiente", texto_tarea, categoria, fecha))
        self.var_nueva_tarea.set("")

    def marcar_completada(self):
        # Marca la tarea seleccionada como completada
        seleccion = self.tree_tareas.selection()
        if not seleccion:
            messagebox.showinfo("Información", "Por favor, seleccione una tarea.")
            return

        item = seleccion[0]
        valores = self.tree_tareas.item(item, "values")
        self.tree_tareas.item(item, values=("Completada", valores[1], valores[2], valores[3]))

    def editar_tarea(self):
        # Permite editar la tarea seleccionada
        seleccion = self.tree_tareas.selection()
        if not seleccion:
            messagebox.showinfo("Información", "Por favor, seleccione una tarea.")
            return

        item = seleccion[0]
        valores = self.tree_tareas.item(item, "values")
        self.var_nueva_tarea.set(valores[1])
        self.var_categoria.set(valores[2])
        self.fecha_tarea.set_date(valores[3])

        self.tree_tareas.delete(item)

    def eliminar_tarea(self):
        # Elimina la tarea seleccionada
        seleccion = self.tree_tareas.selection()
        if seleccion:
            if messagebox.askyesno("Confirmación", "¿Está seguro de que desea eliminar esta tarea?"):
                self.tree_tareas.delete(seleccion[0])

ventana = tk.Tk()
app = GestorTareas(ventana)
ventana.mainloop()