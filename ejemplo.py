import tkinter as tk
from tkinter import messagebox

# Clase para manejar empleados
class EmpleadosApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Administrar Empleados")
        self.root.geometry("400x300")
        
        # Lista para almacenar los empleados
        self.empleados = []

        # Componentes de la interfaz
        self.lbl_nombre = tk.Label(self.root, text="Nombre del Empleado:")
        self.lbl_nombre.pack(pady=5)
        self.entrada_nombre = tk.Entry(self.root)
        self.entrada_nombre.pack(pady=5)

        self.boton_agregar = tk.Button(self.root, text="Agregar Empleado", command=self.agregar_empleado)
        self.boton_agregar.pack(pady=5)

        self.boton_ver = tk.Button(self.root, text="Ver Empleados", command=self.ver_empleados)
        self.boton_ver.pack(pady=5)

    def agregar_empleado(self):
        nombre = self.entrada_nombre.get()
        if nombre:
            self.empleados.append(nombre)
            messagebox.showinfo("Éxito", f"Empleado '{nombre}' agregado")
            self.entrada_nombre.delete(0, tk.END)
        else:
            messagebox.showerror("Error", "Debe ingresar un nombre")

    def ver_empleados(self):
        empleados_str = "\n".join(self.empleados) if self.empleados else "No hay empleados registrados"
        messagebox.showinfo("Lista de Empleados", empleados_str)


# Clase para manejar proveedores
class ProveedoresApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Administrar Proveedores")
        self.root.geometry("400x300")
        
        self.proveedores = []

        self.lbl_nombre = tk.Label(self.root, text="Nombre del Proveedor:")
        self.lbl_nombre.pack(pady=5)
        self.entrada_nombre = tk.Entry(self.root)
        self.entrada_nombre.pack(pady=5)

        self.boton_agregar = tk.Button(self.root, text="Agregar Proveedor", command=self.agregar_proveedor)
        self.boton_agregar.pack(pady=5)

        self.boton_ver = tk.Button(self.root, text="Ver Proveedores", command=self.ver_proveedores)
        self.boton_ver.pack(pady=5)

    def agregar_proveedor(self):
        nombre = self.entrada_nombre.get()
        if nombre:
            self.proveedores.append(nombre)
            messagebox.showinfo("Éxito", f"Proveedor '{nombre}' agregado")
            self.entrada_nombre.delete(0, tk.END)
        else:
            messagebox.showerror("Error", "Debe ingresar un nombre")

    def ver_proveedores(self):
        proveedores_str = "\n".join(self.proveedores) if self.proveedores else "No hay proveedores registrados"
        messagebox.showinfo("Lista de Proveedores", proveedores_str)


# Clase para manejar productos
class ProductosApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Administrar Productos")
        self.root.geometry("400x300")
        
        self.productos = []

        self.lbl_nombre = tk.Label(self.root, text="Nombre del Producto:")
        self.lbl_nombre.pack(pady=5)
        self.entrada_nombre = tk.Entry(self.root)
        self.entrada_nombre.pack(pady=5)

        self.lbl_precio = tk.Label(self.root, text="Precio del Producto:")
        self.lbl_precio.pack(pady=5)
        self.entrada_precio = tk.Entry(self.root)
        self.entrada_precio.pack(pady=5)

        self.boton_agregar = tk.Button(self.root, text="Agregar Producto", command=self.agregar_producto)
        self.boton_agregar.pack(pady=5)

        self.boton_ver = tk.Button(self.root, text="Ver Productos", command=self.ver_productos)
        self.boton_ver.pack(pady=5)

    def agregar_producto(self):
        nombre = self.entrada_nombre.get()
        try:
            precio = float(self.entrada_precio.get())
            self.productos.append({'nombre': nombre, 'precio': precio})
            messagebox.showinfo("Éxito", f"Producto '{nombre}' agregado con precio {precio}")
            self.entrada_nombre.delete(0, tk.END)
            self.entrada_precio.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Error", "Debe ingresar un precio válido")

    def ver_productos(self):
        if self.productos:
            productos_str = "\n".join([f"{p['nombre']}: ${p['precio']}" for p in self.productos])
        else:
            productos_str = "No hay productos registrados"
        messagebox.showinfo("Lista de Productos", productos_str)


# Clase para manejar facturación
class FacturacionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Generar Factura")
        self.root.geometry("400x300")
        
        self.factura = []

        self.lbl_producto = tk.Label(self.root, text="Nombre del Producto:")
        self.lbl_producto.pack(pady=5)
        self.entrada_producto = tk.Entry(self.root)
        self.entrada_producto.pack(pady=5)

        self.lbl_cantidad = tk.Label(self.root, text="Cantidad:")
        self.lbl_cantidad.pack(pady=5)
        self.entrada_cantidad = tk.Entry(self.root)
        self.entrada_cantidad.pack(pady=5)

        self.boton_agregar = tk.Button(self.root, text="Agregar a Factura", command=self.agregar_a_factura)
        self.boton_agregar.pack(pady=5)

        self.boton_ver = tk.Button(self.root, text="Ver Factura", command=self.ver_factura)
        self.boton_ver.pack(pady=5)

    def agregar_a_factura(self):
        producto = self.entrada_producto.get()
        try:
            cantidad = int(self.entrada_cantidad.get())
            self.factura.append({'producto': producto, 'cantidad': cantidad})
            messagebox.showinfo("Éxito", f"{cantidad} unidades de '{producto}' agregadas a la factura")
            self.entrada_producto.delete(0, tk.END)
            self.entrada_cantidad.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Error", "Debe ingresar una cantidad válida")

    def ver_factura(self):
        if self.factura:
            factura_str = "\n".join([f"{item['cantidad']} x {item['producto']}" for item in self.factura])
        else:
            factura_str = "La factura está vacía"
        messagebox.showinfo("Factura Actual", factura_str)


# Clase para la ventana principal que administra el menú
class AppPrincipal:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Administración")
        self.root.geometry("300x250")
        
        # Botón para abrir la gestión de empleados
        boton_empleados = tk.Button(self.root, text="Administrar Empleados", command=self.abrir_empleados, font=("Arial", 12), width=25)
        boton_empleados.pack(pady=10)
        
        # Botón para abrir la gestión de proveedores
        boton_proveedores = tk.Button(self.root, text="Administrar Proveedores", command=self.abrir_proveedores, font=("Arial", 12), width=25)
        boton_proveedores.pack(pady=10)
        
        # Botón para abrir la gestión de productos
        boton_productos = tk.Button(self.root, text="Administrar Productos", command=self.abrir_productos, font=("Arial", 12), width=25)
        boton_productos.pack(pady=10)
        
        # Botón para abrir la gestión de facturación
        boton_facturacion = tk.Button(self.root, text="Generar Factura", command=self.abrir_facturacion, font=("Arial", 12), width=25)
        boton_facturacion.pack(pady=10)

    def abrir_empleados(self):
        nueva_ventana = tk.Toplevel(self.root)
        empleados_app = EmpleadosApp(nueva_ventana)

    def abrir_proveedores(self):
        nueva_ventana = tk.Toplevel(self.root)
        proveedores_app = ProveedoresApp(nueva_ventana)

    def abrir_productos(self):
        nueva_ventana = tk.Toplevel(self.root)
        productos_app = ProductosApp(nueva_ventana)

    def abrir_facturacion(self):
        nueva_ventana = tk.Toplevel(self.root)
        facturacion_app = FacturacionApp(nueva_ventana)


if __name__ == "__main__":
    root = tk.Tk()
    app_principal = AppPrincipal(root)
    root.mainloop()
