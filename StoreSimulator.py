
import random

class producto:
    
    def __init__(self,nombre,precio_unidad,cantidad):
        self.nombre= nombre
        self.precio_unidad= precio_unidad
        self.cantidad= cantidad

    #precio_total = int(self.cantidad)*precio_unidad 

    def save_database(self):
        print(f'Producto :{self.nombre} Cantidad: {self.cantidad} Total: {int(self.cantidad)*self.precio_unidad }')
    
if __name__ =="__main__":    
    productos ={"producto":(("manzana",1000),("pera",700),("banano",1500))}



    producto_random = (random.choice(productos["producto"]))
    cantidad = random.randint(1, 10)


    item_factura =(producto_random[0],producto_random[1],cantidad,producto_random[1]*cantidad)
    producto_1 = producto(producto_random[0],producto_random[1],cantidad)
    print(producto_random)
    print (item_factura)
    producto_1.save_database()



def lista_compra(productos):
    n_elementos = random.randint(1,5)
    factura=[]
    total = 0
    for i in range(n_elementos):
        producto_random = (random.choice(productos["producto"]))
        cantidad = random.randint(1, 10)
        item_factura =(producto_random[0],producto_random[1],cantidad,producto_random[1]*cantidad) 
        factura.append(item_factura)
        total+=producto_random[1]*cantidad
    print(lista_compra(productos))
    return(factura,total)

    

#HOLAAAA