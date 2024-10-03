import tkinter as tk
from tkinter import messagebox


class CalculadoraApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculadora")
        self.root.geometry("400x500")

        # StringVar para mostrar la entrada
        self.entrada = tk.StringVar()

        # Configuración de la pantalla de la calculadora
        pantalla = tk.Entry(root, textvariable=self.entrada, font=("Arial", 24), bd=10, insertwidth=4, width=14, borderwidth=4)
        pantalla.grid(row=0, column=0, columnspan=4)

        # Creación de los botones
        self.crear_botones()

    def crear_botones(self):
        # Botones numéricos
        botones = [
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
            ('0', 4, 0), ('.', 4, 1), ('+', 4, 2), ('=', 4, 3),
            ('C', 5, 0)
        ]

        # Creación de los botones en la interfaz
        for (texto, fila, columna) in botones:
            if texto == '=':
                boton = tk.Button(self.root, text=texto, padx=20, pady=20, font=("Arial", 18), command=self.calcular)
            elif texto == 'C':
                boton = tk.Button(self.root, text=texto, padx=20, pady=20, font=("Arial", 18), command=self.limpiar)
            else:
                boton = tk.Button(self.root, text=texto, padx=20, pady=20, font=("Arial", 18), 
                                  command=lambda t=texto: self.agregar_a_entrada(t))
            boton.grid(row=fila, column=columna, sticky="nsew")

    def agregar_a_entrada(self, valor):
        self.entrada.set(self.entrada.get() + valor)

    def limpiar(self):
        self.entrada.set("")

    def calcular(self):
        try:
            resultado = eval(self.entrada.get())  # Evalúa la expresión
            self.entrada.set(resultado)
        except Exception as e:
            messagebox.showerror("Error", "Entrada inválida")


class InfoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Acerca de")
        self.root.geometry("300x200")
        
        label = tk.Label(self.root, text="Aplicación de Calculadora v1.0\nCreada por: [Tu Nombre]", font=("Arial", 14))
        label.pack(pady=40)

        boton_cerrar = tk.Button(self.root, text="Cerrar", command=self.root.destroy)
        boton_cerrar.pack(pady=10)


class AppPrincipal:
    def __init__(self, root):
        self.root = root
        self.root.title("Aplicación Principal")
        self.root.geometry("300x200")
        
        # Botón para abrir la calculadora
        boton_calculadora = tk.Button(self.root, text="Abrir Calculadora", command=self.abrir_calculadora, font=("Arial", 14), width=20)
        boton_calculadora.pack(pady=20)
        
        # Botón para abrir la ventana de información
        boton_info = tk.Button(self.root, text="Acerca de", command=self.abrir_info, font=("Arial", 14), width=20)
        boton_info.pack(pady=20)

    def abrir_calculadora(self):
        nueva_ventana = tk.Toplevel(self.root)
        app_calculadora = CalculadoraApp(nueva_ventana)

    def abrir_info(self):
        nueva_ventana = tk.Toplevel(self.root)
        app_info = InfoApp(nueva_ventana)


if __name__ == "__main__":
    root = tk.Tk()
    app_principal = AppPrincipal(root)
    root.mainloop()
