import tkinter as tk #Asignamos el modulo Tkinter al alias 'tk' para usar sus clases y funciones de manera mas consisa.

def saludar():
    etiqueta.config(text="¡Hola, mundo!") #Modifica las propiedades del widget (label).

ventana = tk.Tk() #Se crea la ventana llamando el contructor (Tk()) de Tkinter.
ventana.geometry("400x280") #Asignamos un size para la ventana.
ventana.title("Mi Primera Interfaz") #Asignar el titulo de la ventana.

etiqueta = tk.Label(ventana, text="¡Hola!") #Crea el widget tipo label (primer argumento es donde aparecera el label, segundo establece su contenido)
etiqueta.pack() # El método pack() se usa para colocar el widget en la ventana. pack() es un gestor de geometría que organiza los widgets en la ventana.

boton = tk.Button(ventana, text="Haz clic aquí", command=saludar) #Crea el widget tipo button (primer argumento es donde aparecera el label, segundo establece su contenido y el tercero funcion que se llamara cuando se precione.)
boton.config(fg="red", bg="blue") #Configurar widgets
boton.pack() #Colocar el widget en la ventana




ventana.mainloop() #Inicia el bucle de la interfaz 