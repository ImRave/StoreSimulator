import tkinter as tk #Asignamos el modulo Tkinter al alias 'tk' para usar sus clases y funciones de manera mas consisa.

def saludar():
    etiqueta.config(text="¡Hola, mundo!") #Modifica las propiedades del widget (label).

ventana = tk.Tk() #Se crea la ventana llamando el contructor (Tk()) de Tkinter.
ventana.geometry("400x280") #Asignamos un size para la ventana.
ventana.title("Mi Primera Interfaz") #Asignar el titulo de la ventana.

etiqueta = tk.Label(ventana, text="¡Hola!", bg="yellow") #Crea el widget tipo label (primer argumento es donde aparecera el label, segundo establece su contenido)
etiqueta.pack() # El método pack() se usa para colocar el widget en la ventana. pack() es un gestor de geometría que organiza los widgets en la ventana.

boton = tk.Button(ventana, text="Haz clic aquí", command=saludar) #Crea el widget tipo button (primer argumento es donde aparecera el label, segundo establece su contenido y el tercero funcion que se llamara cuando se precione.)
boton.pack() #Colocar el widget en la ventana
boton.place(x=60, y=40, width=100, height=30) #Ubicar elementos.
boton.config(fg="red", bg="blue") #Configurar widgets
#Si se cambia el nombre del archivo de .py a .pyw la aplicacion se ejecutara automaticamente al hacer doble click en ella.

def sumar():
    n1 = texto.get()
    n2 = texto2.get()
    res = float(n1) + float(n2)
    resu.delete(0, 'end ')
    resu.insert(0, res)

texto = tk.Entry(ventana, bg="pink") 
texto.place(relx=0.08, rely=0.3, relwidth=0.1, relheight=0.2) #Ubicar elementos.

texto2 = tk.Entry(ventana, bg="pink") 
texto2.place(x=120, y=120, width=100, height=30) #Ubicar elementos.

resu = tk.Entry(ventana, bg="violet") 
resu.place(x=120, y=160, width=100, height=30) #Ubicar elementos.

suma = tk.Button(ventana, text="Sumar", command=sumar) #Crea el widget tipo button (primer argumento es donde aparecera el label, segundo establece su contenido y el tercero funcion que se llamara cuando se precione.)
suma.place(x=230, y=100, width=100, height=30) #Ubicar elementos.

ventana.mainloop() #Inicia el bucle de la interfaz   