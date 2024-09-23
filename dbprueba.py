import sqlite3


def CrearDB():
    conn = sqlite3.connect("DataBases/InvetarioYFacturas.db")
    conn.commit()
    conn.close()

def CreateTabel():
    conn = sqlite3.connect("DataBases/InvetarioYFacturas.db")
    cursor =conn.cursor()
    cursor.execute("""Create Table producto (
                   nombre varchar(100),
                   precio int,
                   cantidad int)""")
    conn.commit()
    conn.close()

def Insert(nombre,precio):
    conn = sqlite3.connect("DataBases/InvetarioYFacturas.db")
    cursor =conn.cursor()
    #insert =f"INSERT into producto VALUES('mango',1500,500)"
    #cursor.execute(insert)
    insertAuto =f"INSERT into producto VALUES('{nombre}',{precio},500)"
    cursor.execute(insertAuto)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    productos =(("manzana",1000),("pera",700),("banano",1500))
    print(f'insert into producto values({", ".join(map(str, productos[2]))},500)')
    NomYPre = ", ".join(map(str, productos[2]))
    nombreYprecio = NomYPre.split(",")
    print(nombreYprecio[0],nombreYprecio[1])
    CrearDB()
    CreateTabel()
    Insert(nombreYprecio[0],nombreYprecio[1])
    for a in productos:
        Insert(a[0], a[1])
    #for a in productos:
    #    print(a)
    #    NomYPre = ", ".join(map(str, productos[a]))
    #    nombreYprecio = NomYPre.split(",")
    #    Insert(nombreYprecio[0],nombreYprecio[1])


#conexion=sqlite3.connect("DataBases/Pueba_1")
#cursor = conexion.cursor()
#cursor.execute("Create Table producto (id int primary key,nombre varchar(100),precio int,cantidad int)")
#cursor.execute('INSERT into producto VALUES(1,"mango",1500,500)')
#cursor.execute(f'insert into producto values({productos[2]},500)')