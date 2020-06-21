import sqlite3
from tkinter import *
from tkinter import messagebox
from tkinter import ttk

#Juan Pablo Meza Gazabón
# -----------------------------------------VALIDACIONES------------------------------------------


def validate_number(text):
    return text.isdecimal()


# -----------------------------------------FUNCIONES------------------------------------------


def conexionBBDD():
    miConexion = sqlite3.connect("CONTACTOS")
    miCursor = miConexion.cursor()

    try:
        miCursor.execute(
            "CREATE TABLE DATOS_CONTACTOS (ID INT (10) PRIMARY KEY ,NOMBRE_CONTACTO VARCHAR (50),APELLIDO VARCHAR (50),TELEFONO VARCHAR(50), EMAIL VARCHAR (20))")

        messagebox.showinfo("BBDD", "BBDD creada con éxtio")

    except:

        messagebox.showwarning("¡ATENCIÓN!", "la BBDD ya existe")

    miConexion.close()


def salirAplicacion():
    valor = messagebox.askquestion("Salir", "¿Desea salir de la aplicación?")

    if (valor == "yes"):
        root.destroy()


def limpiarCampos():
    miId.set("")
    miNombre.set("")
    miApellido.set("")
    miEmail.set("")
    miTelefono.set("")


def guardar():

    try:
        miConexion = sqlite3.connect("CONTACTOS")
        miCursor = miConexion.cursor()

        miID2 = miId.get()
        miNombre2 = miNombre.get()
        miApellido2 = miApellido.get()
        miTelefono2 = miTelefono.get()
        miEmail2 = miEmail.get()

        if ((miID2 != "") and (miNombre2 != "") and (miApellido2 != "") and (miTelefono2 != "") and (miEmail2 != "")):

            datos = miId.get(), miNombre.get(), miApellido.get(), miTelefono.get(), miEmail.get()

            miCursor.execute(
                "INSERT INTO DATOS_CONTACTOS VALUES(?,?,?,?,?)", (datos))

            miConexion.commit()

            messagebox.showinfo("BBDD", "Contacto guardado con éxito")

            limpiarCampos()
            mostrarContactos()
        else:
            messagebox.showerror("ERROR", "Debe llenar todos los campos")

    except sqlite3.OperationalError:
        messagebox.showwarning("¡ATENCIÓN!", "Debe conectar la base de datos. \n Para conectarla diríjase a BBDD Y presione conectar")
    except sqlite3.IntegrityError:
        messagebox.showerror("ERROR","No pueden haber dos ID iguales")

    


def leer():

    try:

        if (miBuscaId.get() != ""):
            miConexion = sqlite3.connect("CONTACTOS")
            miCursor = miConexion.cursor()

            miCursor.execute(
                "SELECT * FROM DATOS_CONTACTOS WHERE ID="+miBuscaId.get())

            elContacto = miCursor.fetchall()

            if (not elContacto):
                messagebox.showwarning(
                    "ERROR", "contacto no encontrado verifique el código del contacto")

            else:
                for contacto in elContacto:
                    miId.set(contacto[0])
                    miNombre.set(contacto[1])
                    miApellido.set(contacto[2])
                    miTelefono.set(contacto[3])
                    miEmail.set(contacto[4])

                
            miConexion.commit()

        else:
            messagebox.showerror(
                "ERROR", "Debe llenar el campo ID para buscar el contacto")

    except:
        messagebox.showwarning(
            "¡ATENCIÓN!", "Debe conectar la base de datos. \n Para conectarla diríjase a BBDD Y presione conectar")


def mostrarContactos():
    try:
        r = Text(root, width=80, height=15)
        miConexion = sqlite3.connect("CONTACTOS")
        miCursor = miConexion.cursor()

        miCursor.execute("SELECT * FROM DATOS_CONTACTOS")

        losContactos = miCursor.fetchall()
        r.insert(INSERT, "ID\tNOMBRE \t\tAPELLIDO \t\tTELEFONO\t\tEMAIL\n")

        for contactos in losContactos:
            print("ID: ", contactos[0])
            print("NOMBRE: ", contactos[1])
            print("APELLIDO: ", contactos[2])
            print("TELEFONO: ", contactos[3])
            print("EMAIL: ", contactos[4])

            varId = str(contactos[0])
            varNombre = str(contactos[1])
            varApellido = str(contactos[2])
            varTelefono = str(contactos[3])
            varEmail = str(contactos[4])

            r.insert(INSERT, varId+"\t"+varNombre+"\t\t" +
                     varApellido+"\t\t"+varTelefono+"\t\t"+varEmail+"\t\n")

        r.place(x=20, y=240)
        r.config(state=DISABLED)

        miConexion.commit()

    except:
        messagebox.showwarning(
            "¡ATENCIÓN!", "Debe conectar la base de datos. \n Para conectarla diríjase a BBDD Y presione conectar")


def actualizar():
    try:
        if (miBuscaId.get() != ""):

            miConexion = sqlite3.connect("CONTACTOS")
            miCursor = miConexion.cursor()

            datos = miId.get(), miNombre.get(), miApellido.get(), miTelefono.get(), miEmail.get()

            miCursor.execute(
                "UPDATE DATOS_CONTACTOS SET ID = ?, NOMBRE_CONTACTO = ?,APELLIDO =?,TELEFONO=?,EMAIL=?" + "WHERE ID="+miId.get(), (datos))

            miConexion.commit()
        

            messagebox.showinfo("BBDD", "Usuario actualizado con éxito")

            limpiarCampos()
            mostrarContactos()

        else:
            messagebox.showerror(
                "ERROR", "Debe llenar el campo ID para actualizar el contacto")
    except FileNotFoundError:
        messagebox.showwarning(
            "¡ATENCIÓN!", "Debe conectar la base de datos. \n Para conectarla diríjase a BBDD Y presione conectar")
    except sqlite3.OperationalError:
        messagebox.showwarning(
            "¡ATENCIÓN!", "Para Actualizar. \n Primero debe clickear el botón buscar, para posteiormente actualizar los datos")


def eliminar():
    try:
        if (miBuscaId.get() != ""):
            miConexion = sqlite3.connect("CONTACTOS")
            miCursor = miConexion.cursor()

            miCursor.execute(
                "DELETE FROM DATOS_CONTACTOS WHERE ID="+miBuscaId.get())

            messagebox.showinfo("BBDD", "Contacto eliminado con éxito")

            limpiarCampos()

            miConexion.commit()

            mostrarContactos()

        else:
            messagebox.showerror(
                "ERROR", "Debe llenar el campo ID para eliminar el contacto")
    except:
        messagebox.showwarning(
            "¡ATENCIÓN!", "Contacto no encontrado, verifique el código o la conexión con la BBDD")


root = Tk()


# -----------------------------------------BARRA DE MENÚ------------------------------------------


barraMenu = Menu(root)
root.config(menu=barraMenu, width=300, height=300)
root.resizable(0, 0)
root.geometry("700x500")


bbddMenu = Menu(barraMenu, tearoff=0)
bbddMenu.add_command(label="Conectar", command=conexionBBDD)
bbddMenu.add_command(label="Salir", command=salirAplicacion)

borrarMenu = Menu(barraMenu, tearoff=0)
borrarMenu.add_command(label="Borrar campos", command=limpiarCampos)

crudMenu = Menu(barraMenu, tearoff=0)
crudMenu.add_command(label="Guardar", command=guardar)
crudMenu.add_command(label="leer", command=leer)
crudMenu.add_command(label="Actualizar", command=actualizar)
crudMenu.add_command(label="Eliminar", command=eliminar)

ayudaMenu = Menu(barraMenu, tearoff=0)
ayudaMenu.add_command(label="Ayuda")
ayudaMenu.add_command(label="Acerca de...")


barraMenu.add_cascade(label="BBDD", menu=bbddMenu)
barraMenu.add_cascade(label="Borrar", menu=borrarMenu)
barraMenu.add_cascade(label="CRUD", menu=crudMenu)
barraMenu.add_cascade(label="Ayuda", menu=ayudaMenu)


miframe = Frame(root)
miframe.pack()

colorFondo = "#006"
colorLetra = "#FFF"
root.config(background=colorFondo)
miId = StringVar()
miNombre = StringVar()
miApellido = StringVar()
miTelefono = StringVar()
miEmail = StringVar()
miBuscaId = StringVar()

# -----------------------------------------CAJAS DE TEXTO------------------------------------------


cuadroId = ttk.Entry(
    validate="key",
    textvariable=miId,

    validatecommand=(root.register(validate_number), "%S")
)

cuadroId.place(x=160, y=50)

cuadroNombre = Entry(root, textvariable=miNombre,
                     fg="BLACK").place(x=160, y=80)
cuadroApellido = Entry(root, textvariable=miApellido,
                       fg="BLACK").place(x=160, y=110)


cuadroTelefono = ttk.Entry(
    validate="key",
    textvariable=miTelefono,

    validatecommand=(root.register(validate_number), "%S")
)

cuadroTelefono.place(x=160, y=140)

cuadroEmail = Entry(root, textvariable=miEmail, fg="BLACK").place(x=160, y=170)


buscaId = ttk.Entry(
    validate="key",
    textvariable=miBuscaId,

    validatecommand=(root.register(validate_number), "%S")
)

buscaId.place(x=460, y=50)

# -----------------------------------------LABELS------------------------------------------

etiquetaTitulo = Label(root, text="AGENDA DE CONTACTOS",
                       bg="#006", fg=colorLetra).place(x=270, y=10)
etiquetaId = Label(root, text="ID:", bg=colorFondo,
                   fg=colorLetra).place(x=50, y=50)
etiquetaNombre = Label(root, text="NOMBRE:", bg=colorFondo,
                       fg=colorLetra).place(x=50, y=80)
etiquetaApellido = Label(root, text="APELLIDO:",
                         bg=colorFondo, fg=colorLetra).place(x=50, y=110)
etiquetaTelefono = Label(root, text="TELEFONO:",
                         bg=colorFondo, fg=colorLetra).place(x=50, y=140)
etiquetaEmail = Label(root, text="EMAIL:", bg=colorFondo,
                      fg=colorLetra).place(x=50, y=170)
etiquetaConsultaId = Label(
    root, text="ID: ", bg=colorFondo, fg=colorLetra).place(x=430, y=50)


# ---------------------------------------BOTONES...................................................

botonVerContactos = Button(root, text="Ver contactos", bg="#009",
                           fg="white", command=mostrarContactos).place(x=70, y=200)
botonGuardar = Button(root, text="Guardar", bg="#009",
                      fg="white", command=guardar).place(x=170, y=200)
botonLimpiarCampos = Button(root, text="Limpiar", bg="#009",
                            fg="white", command=limpiarCampos).place(x=240, y=200)
botonBuscar = Button(root, text="Buscar", bg="#009",
                     fg="white", command=leer).place(x=450, y=80)
botonActualizar = Button(root, text="Actualizar", bg="#009",
                         fg="white", command=actualizar).place(x=500, y=80)
botonEliminar = Button(root, text="Eliminar", bg="#009",
                       fg="white", command=eliminar).place(x=570, y=80)


root.mainloop()
