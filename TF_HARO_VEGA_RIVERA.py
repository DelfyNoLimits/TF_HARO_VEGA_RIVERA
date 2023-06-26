import tkinter as tk
from tkinter import messagebox, Checkbutton, BooleanVar
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

# Función para encontrar el camino más corto
def encontrar_camino():
    persona_origen = textbox_origen.get("1.0", "end-1c").lower()
    persona_destino = textbox_destino.get("1.0", "end-1c").lower()
    shortest_path = nx.shortest_path(G, persona_origen, persona_destino) # camino más corto
    path_edges = list(zip(shortest_path, shortest_path[1:])) # obtener los bordes del camino más corto
    ax.clear() # limpiar el eje para el nuevo dibujo
    pos = nx.spring_layout(G) # obtener las posiciones de los nodos

    # crear un subgrafo con solo los nodos y aristas en el camino más corto
    H = G.subgraph(shortest_path)

    # dibujar los nodos, las etiquetas y los bordes
    nx.draw_networkx_nodes(H, pos, ax=ax)
    nx.draw_networkx_labels(H, pos, ax=ax)
    nx.draw_networkx_edges(H, pos, edgelist=path_edges, edge_color='r', ax=ax)

    # obtener los pesos de las aristas en el camino más corto
    edge_labels = nx.get_edge_attributes(H, 'weight')
    # dibujar las etiquetas de las aristas (pesos)
    nx.draw_networkx_edge_labels(H, pos, edge_labels=edge_labels, ax=ax)

    datos_persona = data.loc[data['Name'].str.lower() == shortest_path[-1]] # obtener los datos de la última persona en el camino
    datos_texto = f"Nombre: {datos_persona['Name'].values[0]}\nDeporte: {datos_persona['Deporte'].values[0]}\nHobbie: {datos_persona['Hobbie'].values[0]}\nProfesión: {datos_persona['Profesión'].values[0]}"
    textbox_datos.delete("1.0", tk.END) # limpiar la caja de texto
    textbox_datos.insert(tk.END, datos_texto) # insertar los nuevos datos
    canvas.draw() # dibujar el grafo

# Función para dibujar el grafo
def dibujar_grafo():
    G.clear() # limpiar el grafo para el nuevo dibujo
    personas = data['Name'].tolist() # obtener la lista de nombres
    for persona in personas: # añadir cada persona como un nodo
        G.add_node(persona.lower())
    atributos = [] # lista para los atributos seleccionados
    # si las casillas de verificación están marcadas, añadir los atributos a la lista
    if var_hobbie.get():
        atributos.append('Hobbie')
    if var_profesion.get():
        atributos.append('Profesión')
    if var_deporte.get():
        atributos.append('Deporte')
    # para cada par de personas, comprobar si tienen atributos en común
    for i in range(len(personas)):
        for j in range(i+1, len(personas)):
            persona1 = personas[i].lower()
            persona2 = personas[j].lower()
            atributos_comunes = sum(data.loc[i, atributos] == data.loc[j, atributos]) # contar los atributos en común
            if atributos_comunes > 0: # si tienen atributos en común, añadir un borde entre ellos
                G.add_edge(persona1, persona2, weight=atributos_comunes)
    ax.clear() # limpiar el eje para el nuevo dibujo
    pos = nx.spring_layout(G) # obtener las posiciones de los nodos
    # dibujar el grafo con los nodos, las etiquetas y los bordes
    nx.draw_networkx(G, pos, ax=ax, with_labels=True, node_color="lightblue", edge_color="gray", font_color="black")
    textbox_datos.delete("1.0", tk.END) # limpiar la caja de texto
    canvas.draw() # dibujar el grafo

# Leer los datos
archivo_evaluado = 'EncuestaAlumnos.xlsx'
data = pd.read_excel(archivo_evaluado)
data = data.head(50) # usar solo los primeros 10 datos

# Inicializar el grafo y la ventana
G = nx.Graph()
ventana = tk.Tk()
ventana.attributes("-fullscreen", True)
ventana.configure(bg="#40E0D0")
ventana.title("Conectando Personas!")

# Crear y empacar los widgets de la interfaz

# Label "Archivo evaluado"
label_archivo = tk.Label(ventana, text=f"Archivo evaluado: {archivo_evaluado}", font=("Arial", 12), bg="#40E0D0")
label_archivo.pack(pady=10)

# Frame para los elementos
frame = tk.Frame(ventana, bg="#40E0D0")
frame.pack(expand=True)

# Label "Persona Origen"
label_origen = tk.Label(frame, text="Persona Origen:")
label_origen.grid(row=0, column=0, padx=10, pady=0, sticky="e")

# Textbox "Persona Origen"
textbox_origen = tk.Text(frame, height=1, width=20)
textbox_origen.grid(row=0, column=1, padx=10, pady=0, sticky="w")

# Label "Persona Destino"
label_destino = tk.Label(frame, text="Persona Destino:")
label_destino.grid(row=1, column=0, padx=10, pady=10, sticky="e")

# Textbox "Persona Destino"
textbox_destino = tk.Text(frame, height=1, width=20)
textbox_destino.grid(row=1, column=1, padx=10, pady=10, sticky="w")

# Casillas de verificación para las restricciones
var_hobbie = BooleanVar()
check_hobbie = Checkbutton(frame, text="Hobbie", variable=var_hobbie)
check_hobbie.grid(row=2, column=0, padx=10, pady=5, sticky="w")

var_profesion = BooleanVar()
check_profesion = Checkbutton(frame, text="Profesión", variable=var_profesion)
check_profesion.grid(row=2, column=1, padx=10, pady=5, sticky="w")

var_deporte = BooleanVar()
check_deporte = Checkbutton(frame, text="Deporte", variable=var_deporte)
check_deporte.grid(row=3, column=0, padx=10, pady=5, sticky="w")

# Botón "Graficar"
boton_graficar = tk.Button(frame, text="Graficar", command=dibujar_grafo)
boton_graficar.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

# Botón "Encontrar Camino"
boton_encontrar_camino = tk.Button(frame, text="Encontrar Camino", command=encontrar_camino)
boton_encontrar_camino.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

# Configurar el gráfico inicial
fig = plt.figure(figsize=(5, 4), dpi=100)
ax = fig.add_subplot(111)
canvas = FigureCanvasTkAgg(fig, master=ventana)
canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
toolbar = NavigationToolbar2Tk(canvas, ventana)
toolbar.update()
canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

# Caja de texto para mostrar los datos de la última persona
textbox_datos = tk.Text(ventana, height=4, width=30)
textbox_datos.pack(pady=5)

# Comenzar el ciclo principal de eventos
ventana.mainloop()
