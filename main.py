from tkinter import *
from tkinter import messagebox
from tkinter import scrolledtext as st
import sqlite3
import os 		

root=Tk()
root.title("Controlador de BD")

miFrame=Frame(root)			#Crea frame
miFrame.config(width="400", height="700")
miFrame.pack()

#__________VARIABLES______________________________
#each for id, name, password, surname, address, comment, and for cursor and connection
id_dato=StringVar()
nombre_dato=StringVar()
password_dato=StringVar()
apellido_dato=StringVar()
direccion_dato=StringVar()
comentario_dato=StringVar()
miCursor=StringVar()
miConexion=StringVar()

#__________FUNCIONS_______________________________
def createDB():
	global miCursor
	global miConexion
	miConexion=sqlite3.connect("GestionDB")
	miCursor=miConexion.cursor()

	try:
		miCursor.execute(''' 
			CREATE TABLE USERSDATA (
			ID INTEGER PRIMARY KEY AUTOINCREMENT,
			Nombre VARCHAR(50),
			Password VARCHAR(50),
			Apellido VARCHAR(50),
			Direccion VARCHAR(50),
			Comentario VARCHAR(200))
		''')
		messagebox.showwarning("Advice","The Database was created")

	except: 
		messagebox.showwarning("Advice","The Database currently exists") 

def connectDB():				# Create/conect with DataBase.
	global miCursor
	global miConexion	

	if os.path.exists("GestionDB"):
		miConexion=sqlite3.connect("GestionDB")
		miCursor=miConexion.cursor()
		messagebox.showwarning("Advice","It was connected to the Database") 

	else:
		valor=messagebox.askokcancel("Warning",
		 "not detected any Database. \n ¿Do you want to create it?")
		if valor==True:
			createDB()

def exitApp(): 					# Get out from the app.
	global miConexion
	valor=messagebox.askokcancel("Exit", "¿Do you want to exit?")

	if valor==True:
		if not miConexion:		# If not empty, close connection.
			miConexion.close()
		root.destroy()

def deleteAll():				# To clean all inputs.
	id_dato.set("")
	nombre_dato.set("")
	password_dato.set("")
	apellido_dato.set("")
	direccion_dato.set("")
	cuadroComment.delete('1.0', END)

def createOption():
	miCursor=miConexion.cursor()
	nameData=nombre_dato.get()
	passData=password_dato.get()
	surnameData=apellido_dato.get()
	addressData=direccion_dato.get()
	commentData=cuadroComment.get("1.0",END)
# PREPARE DATA TO SEND
	datosInsert=nombre_dato.get(),password_dato.get(),apellido_dato.get(),\
		direccion_dato.get(),cuadroComment.get("1.0",END)
# SEND
	miCursor.execute("INSERT INTO USERSDATA VALUES (NULL,?,?,?,?,?)", (datosInsert))
# Alternative:
	#datosInsert=[(nameData,passData,surnameData,addressData,commentData)]
	#miCursor.executemany("INSERT INTO USERSDATA VALUES (NULL,?,?,?,?,?)", datosInsert)

	miConexion.commit()
	messagebox.showwarning("Advice","User created success") 

def readOption():	
	miCursor=miConexion.cursor()
	cuadroComment.delete('1.0', END)	# Clean to avoid acumulative data
	miCursor.execute("SELECT * FROM USERSDATA WHERE ID=" + id_dato.get())
	theUser=miCursor.fetchall() 		# Return an array with all results.

	for user in theUser:
		id_dato.set(user[0])
		nombre_dato.set(user[1])
		password_dato.set(user[2])
		apellido_dato.set(user[3])
		direccion_dato.set(user[4])
		cuadroComment.insert(1.0,user[5])

	miConexion.commit()

def updateOption():
	miCursor=miConexion.cursor()
	nameData=nombre_dato.get()
	passData=password_dato.get()
	surnameData=apellido_dato.get()
	addressData=direccion_dato.get()
	commentData=cuadroComment.get("1.0",END)
# PREPARE DATA TO SEND
	datosInsert=[(nameData,passData,surnameData,addressData,commentData)]	
# SEND
	miCursor.executemany("UPDATE USERSDATA SET Nombre = ?, Password = ?,Apellido = ?,\
		Direccion = ?,Comentario = ? WHERE ID=" + id_dato.get(), datosInsert)
	miConexion.commit()

def deleteOption():	
	miCursor=miConexion.cursor()
	miCursor.execute("DELETE FROM USERSDATA WHERE ID=" + id_dato.get())
	miConexion.commit()

	id_dato.set("")
	nombre_dato.set("")
	password_dato.set("")
	apellido_dato.set("")
	direccion_dato.set("")
	cuadroComment.delete('1.0', END)

	messagebox.showwarning("Advice","User deleted success") 

def deleteDB():
	global miConexion

	if os.path.exists("GestionDB"):
  		os.remove("GestionDB")
  		messagebox.showwarning("Advice","The file was delete")

	else:
  		messagebox.showwarning("Advice", "Sorry, the file doesn't exist.\
  			\n You can try to create a new one.")

#__________MENUS__________________________________
barraMenu=Menu(root)
root.config(menu=barraMenu)

menuDB=Menu(barraMenu,tearoff=0)
menuDB.add_command(label="Create",command=createDB)
menuDB.add_command(label="Connect",command=connectDB)
menuDB.add_command(label="Exit",command=exitApp)
barraMenu.add_cascade(label="DB", menu=menuDB)

menuDelete=Menu(barraMenu,tearoff=0)
menuDelete.add_command(label="Delete fields",command=deleteAll)
menuDelete.add_command(label="Delete DB",command=deleteDB)
barraMenu.add_cascade(label="Delete", menu=menuDelete)

menuCRUD=Menu(barraMenu,tearoff=0)
menuCRUD.add_command(label="Create",command=createOption)
menuCRUD.add_command(label="Read",command=readOption)
menuCRUD.add_command(label="Update",command=updateOption)
menuCRUD.add_command(label="Delete",command=deleteOption)
barraMenu.add_cascade(label="CRUD", menu=menuCRUD)

menuDelete=Menu(barraMenu,tearoff=0)
menuDelete.add_command(label="How to use",command=deleteAll)
menuDelete.add_command(label="License",command=deleteAll)
menuDelete.add_command(label="About…",command=deleteAll)
barraMenu.add_cascade(label="Help", menu=menuDelete)

#__________INPUTS_________________________________
id_input=Entry(miFrame,textvariable=id_dato)
id_input.grid(row=1,column=2, padx=10, pady=10, columnspan=4)
id_input.config(background="white", justify="left")
id_label=Label(miFrame, text="Id:").grid(row=1,column=1,padx=10, pady=10)

nombre_input=Entry(miFrame,textvariable=nombre_dato).grid(row=2,column=2,padx=10, pady=10, columnspan=4)
nombre_label=Label(miFrame, text="Nombre:").grid(row=2,column=1,padx=10, pady=10)

password_input=Entry(miFrame,show="*",textvariable=password_dato).grid(row=3,column=2,padx=10, pady=10, columnspan=4)
password_label=Label(miFrame, text="Password:").grid(row=3,column=1,padx=10, pady=10)

apellido_input=Entry(miFrame,textvariable=apellido_dato).grid(row=4,column=2,padx=10, pady=10, columnspan=4)
apellido_label=Label(miFrame, text="Apellido:").grid(row=4,column=1,padx=10, pady=10)

direccion_input=Entry(miFrame,textvariable=direccion_dato).grid(row=5,column=2,padx=10, pady=10, columnspan=4)
direccion_label=Label(miFrame, text="Direccion:").grid(row=5,column=1,padx=10, pady=10)

#comentario_input=Text(miFrame, height=4, width=20).grid(row=6,column=2,padx=10, pady=10, columnspan=4)
comentario_label=Label(miFrame, text="Comentario:").grid(row=6,column=1,padx=10, pady=10)
#scrollVert=Scrollbar(miFrame, command=comentario_input.yview).grid(row=6, column=2, sticky="nsew")
#comentario_input.config(yscrollcommand=scrollVert.set)

#from tkinter import scrolledtext as st  → Requiere
cuadroComment=st.ScrolledText(miFrame,height=4, width=20)
cuadroComment.grid(row=6,column=2,padx=10, pady=10, columnspan=4)

#__________BUTTONS_________________________________
botonCreate=Button(miFrame, text="Create", width=6, command=createOption)
botonCreate.grid(row=7, column=1,padx=10, pady=10,)
botonRead=Button(miFrame, text="Read", width=6, command=readOption)
botonRead.grid(row=7, column=2,padx=10, pady=10,)
botonUpdate=Button(miFrame, text="Update", width=6, command=updateOption)
botonUpdate.grid(row=7, column=3,padx=10, pady=10,)
botonDelete=Button(miFrame, text="Detele", width=6, command=deleteOption)
botonDelete.grid(row=7, column=4,padx=10, pady=10,)

mainloop()