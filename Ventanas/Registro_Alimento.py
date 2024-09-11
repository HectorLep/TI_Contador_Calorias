import customtkinter as ctk
import tkinter as tk
import sqlite3
from tkinter import messagebox
from util.colores import *
from Ventanas.Ventana_interfaz import New_ventana
from datetime import datetime

class Registro_Alimento(New_ventana):
    def __init__(self, panel_principal, color):
        super().__init__(panel_principal, color)
        self.add_widget_registro()
        self.cargar_alimentos()
        self.update_coincidencias()

    def add_widget_registro(self):
        self.label_agregar = ctk.CTkLabel(self.sub, text="Agregar alimento", text_color="white", bg_color=COLOR_BOTON2,font=("Arial", 20))
        self.label_agregar.place(relx=0.1, rely=0.10, relwidth=0.3, relheight=0.05)

        # ComboBox dinámico, será llenado desde la base de datos
        self.combo_box = ctk.CTkComboBox(self.sub, corner_radius=0, fg_color="#183549",
                                         values=self.cargar_alimentos(),
                                         border_width=0, button_color="#26656D",
                                         button_hover_color="white", text_color="white")
        self.combo_box.place(relx=0.1, rely=0.15, relwidth=0.3, relheight=0.05)

        # Mensaje "predeterminado" para el combobox
        self.combo_box.set("Seleccionar alimento")  

        # Label "Buscador de alimentos"
        self.label_buscar = ctk.CTkLabel(self.sub, text="Buscador de alimentos", text_color="white", bg_color=COLOR_BOTON2,font=("Arial", 20))
        self.label_buscar.place(relx=0.1, rely=0.30, relwidth=0.3, relheight=0.055)
                
        # Entry "Buscar alimento" que también estará vinculado a la búsqueda
        self.entry_buscar = ctk.CTkEntry(self.sub, corner_radius=0, placeholder_text="Buscar alimento", 
                                         placeholder_text_color="black", border_width=0, fg_color="white", 
                                         text_color="black") 
        self.entry_buscar.place(relx=0.1, rely=0.35, relwidth=0.3) 
        self.entry_buscar.bind('<KeyRelease>', self.obtener_busqueda)
        # ListBox
        self.coincidencias = tk.Listbox(self.sub)
        self.coincidencias.place(relx=0.1, rely=0.4, relwidth=0.3, relheight=0.055)
        self.coincidencias.bind('<<ListboxSelect>>', self.rellenar)

        self.alimentos_buscar = self.cargar_alimentos()
        self.match = []

        # Registro        
        self.label_registro = ctk.CTkLabel(self.sub, text="Último alimento registrado: ", text_color="white", 
                                           bg_color="#183549",font=("Arial", 20))
        self.label_registro.place(relx=0.5, rely=0.3, relwidth=0.4, relheight=0.055)
        
        self.label_segundo_registro = ctk.CTkLabel(self.sub, text="", text_color="white", bg_color="#1f2329")
        self.label_segundo_registro.place(relx=0.5, relwidth=0.4, relheight=0.055, rely=0.35)
        
        # Corrección para mostrar el Label y Entry al cambiar la opción del ComboBox
        self.combo_box_b = ctk.CTkComboBox(self.sub, corner_radius=0, fg_color="#183549",
                                   values=["Por 100gr", "Por porcion"],
                                   border_width=0, button_color="#26656D",
                                   button_hover_color="white", text_color="white",
                                   command=self.on_combobox_change)  # Se debe agregar el 'command'
        self.combo_box_b.place(relx=0.1, rely=0.4, relwidth=0.3, relheight=0.05)

       
        self.label = ctk.CTkLabel(self.sub, text="", text_color="white", bg_color=COLOR_BOTON2,font=("Arial", 20))
        self.entry = ctk.CTkEntry(self.sub,corner_radius=0, placeholder_text="Ingrese kcal consumidas", 
                                         placeholder_text_color="black", border_width=0, fg_color="white", 
                                         text_color="black") 
        
    def on_combobox_change(self, selection):
        if selection == "Por 100gr":
            self.label.configure(text="100gr")
        elif selection == "Por porcion":
            self.label.configure(text="Porción")

        # Corregir las posiciones de los elementos
        self.label.place(relx=0.1, rely=0.5,relwidth=0.3, relheight=0.05)
        self.entry.place(relx=0.1, rely=0.55, relwidth=0.3, relheight=0.05)
        # Botón "Registrar"
        self.boton_buscar = ctk.CTkButton(self.sub, text="Registrar", text_color="white", fg_color= COLOR_BOTON2, 
                                          hover_color= COLOR_DESPLEGABLE, command=self.insert_alimento, font=("Arial", 20))
        self.boton_buscar.place(relx=0.1, rely=0.73, relwidth=0.3, relheight=0.085)



    def cargar_alimentos(self):
        conn = sqlite3.connect(f"./users/{self.usuario}/alimentos.db")
        cursor = conn.cursor()

        cursor.execute("SELECT nombre FROM alimento")
        alimentos = cursor.fetchall()

        # Cargar los alimentos en el ComboBox
        lista_alimentos = [alimento[0] for alimento in alimentos]
        
        conn.close()
        return lista_alimentos
    
    def update_coincidencias(self):
        self.coincidencias.delete(0, tk.END)
        
        num_coincidencias = len(self.match)
    
        if num_coincidencias > 0:
            height = min(num_coincidencias, 5)
            self.coincidencias.place(relx=0.1, rely=0.4, relwidth=0.3, relheight=0.05 * height)
        else:
            self.coincidencias.place_forget()

        for alimento in self.match:
            self.coincidencias.insert(tk.END, alimento)

    def rellenar(self, e):
        self.entry_buscar.delete(0, ctk.END)
        self.entry_buscar.insert(0, self.coincidencias.get(tk.ACTIVE))

    def obtener_busqueda(self, e):
        typeado = self.entry_buscar.get()
        if not typeado or typeado == '':
            self.alimentos_buscar = ''
            self.match = []

        else: 
            self.alimentos_buscar = self.cargar_alimentos()
            self.match = []
            for i in self.alimentos_buscar:
                if typeado.lower() in i.lower():
                    self.match.append(i)
        self.update_coincidencias()
        print('typed')

    def boton_registrar_click(self):
        # Obtener el alimento desde el ComboBox o desde el Entry
        alimento_seleccionado = self.combo_box.get()
        alimento_entry = self.entry_buscar.get().strip()

        if alimento_seleccionado != "Seleccionar alimento":  # Si se seleccionó un alimento en el ComboBox
            alimento = alimento_seleccionado
        elif alimento_entry:  # Si no hay selección en el ComboBox pero hay texto en el Entry
            alimento = alimento_entry
        else:
            messagebox.showwarning("Advertencia", "Por favor, selecciona un alimento o ingresa uno válido.")
            return
        
        # Consultar el alimento en la base de datos
        alimento_info = self.buscar_alimento_en_db(alimento)
        
        if alimento_info:  # Si el alimento fue encontrado
            nombre, calorias_100g, calorias_porcion = alimento_info
            
            # Mostrar el nombre del alimento
            self.label_registro.configure(text=f"Último alimento registrado: {nombre}",font=("Arial", 14))
            
            # Mostrar las calorías en porción o por 100g
            if calorias_porcion:
                self.label_segundo_registro.configure(text=f"Calorías totales: {calorias_porcion} por porción")
            else:
                self.label_segundo_registro.configure(text=f"Calorías totales: {calorias_100g} por 100g")
            
            messagebox.showinfo("Búsqueda exitosa", f"Se encontró el alimento: {nombre}")

            # Reiniciar el ComboBox y limpiar el Entry
            self.combo_box.set("Seleccionar alimento")
            self.entry_buscar.delete(0, "end")
        else:
            messagebox.showwarning("Alimento no encontrado", "No se encontró el alimento en la base de datos.")
            print("Alimento no encontrado en la base de datos.")

    def buscar_alimento_en_db(self, nombre_alimento):
        conn = sqlite3.connect(f"./users/{self.usuario}/alimentos.db")
        cursor = conn.cursor()
        
        query = "SELECT nombre, calorias_100gr, calorias_porcion FROM alimento WHERE nombre = ?"
        cursor.execute(query, (nombre_alimento,))
        
        resultado = cursor.fetchone()
        
        conn.close()
        
        return resultado

    def insert_alimento(self):
        conn = sqlite3.connect(f"./users/{self.usuario}/alimentos.db")
        cursor = conn.cursor()
        query = '''
        INSERT INTO consumo_diario (fecha, nombre) VALUES (?, ?);
        '''
        cursor.execute(query, (datetime.now().strftime('%d-%m-%Y'), self.combo_box.get()))
        conn.commit()
        conn.close()
        
