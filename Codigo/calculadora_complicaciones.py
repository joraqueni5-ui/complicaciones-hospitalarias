import tkinter as tk
from tkinter import ttk, filedialog, messagebox

import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import pandas as pd
import numpy as np

# ------------------------------------------------------------------
# Metas del proyecto (Informe Fase 1)
# ------------------------------------------------------------------
BASELINE_PREVALENCIA = 87.82   # % historico
META_PREVALENCIA = 75.0        # % meta propuesta

# Valores que se interpretan como "sin complicacion" dentro de la columna
# de complicaciones a nivel paciente (columna tipo COMPLICACIONES).
VALORES_SIN_COMPLICACION = {
    "ninguna", "ninguno", "no", "sin complicacion", "sin complicaciones",
    "nan", "none", "n/a", ""
}

# Palabras que, dentro de una columna tipo "flag" (formato ya resumido),
# se interpretan como "SI tuvo complicacion".
VALORES_CON_FLAG = {"si", "sí", "1", "true", "con complicacion", "yes", "y"}

dataframe_actual = None  # guarda el ultimo dataframe cargado, para el EDA


# ====================================================================
# Utilidades para detectar columnas automaticamente
# ====================================================================
def encontrar_columna(df, candidatos):
    """Busca una columna cuyo nombre (en minusculas) coincida exactamente
    o contenga alguno de los textos candidatos."""
    cols_lower = {c.lower().strip(): c for c in df.columns}

    # 1) coincidencia exacta
    for cand in candidatos:
        if cand in cols_lower:
            return cols_lower[cand]

    # 2) coincidencia parcial (contains)
    for col in df.columns:
        col_l = str(col).lower()
        for cand in candidatos:
            if cand in col_l:
                return col
    return None


def calcular_iqr_outliers(serie):
    """Cuenta valores atipicos con el metodo del rango intercuartilico (IQR)."""
    serie_num = pd.to_numeric(serie, errors="coerce").dropna()
    if serie_num.empty:
        return 0, None, None
    q1 = serie_num.quantile(0.25)
    q3 = serie_num.quantile(0.75)
    iqr = q3 - q1
    lim_inf = q1 - 1.5 * iqr
    lim_sup = q3 + 1.5 * iqr
    n_outliers = int(((serie_num < lim_inf) | (serie_num > lim_sup)).sum())
    return n_outliers, lim_inf, lim_sup


# ====================================================================
# Carga y procesamiento del Excel
# ====================================================================
def cargar_excel():
    ruta = filedialog.askopenfilename(
        title="Selecciona la base de datos de pacientes",
        filetypes=[("Archivos Excel", "*.xlsx *.xls"), ("Todos los archivos", "*.*")],
    )
    if not ruta:
        return

    try:
        df = pd.read_excel(ruta)
    except Exception as e:
        messagebox.showerror("Error al leer el archivo", f"No se pudo abrir el Excel:\n{e}")
        return

    if df.empty:
        messagebox.showwarning("Archivo vacio", "El archivo cargado no contiene filas.")
        return

    procesar_dataframe(df, ruta)


def procesar_dataframe(df, ruta):
    global dataframe_actual
    dataframe_actual = df

    nombre_archivo = ruta.split("/")[-1].split("\\")[-1]
    total = len(df)
    con = None
    modo_detectado = ""

    # --- Caso 1: base de datos a nivel de paciente, con columna tipo
    #     COMPLICACIONES (valores: "Ninguna", "Sepsis", "Hemorragia", etc.)
    col_comp = encontrar_columna(df, ["complicaciones", "complicacion"])
    if col_comp is not None:
        serie = df[col_comp].astype(str).str.strip().str.lower()
        con = int((~serie.isin(VALORES_SIN_COMPLICACION)).sum())
        modo_detectado = f"Columna por paciente detectada: '{col_comp}'"

    # --- Caso 2: archivo ya resumido en dos columnas, p.ej.
    #     'complicacion' (Si/No) y 'numero_pacientes' (conteo)
    if con is None:
        col_flag = encontrar_columna(df, ["complicacion", "complicaciones", "tiene_complicacion"])
        col_num = encontrar_columna(
            df, ["numero_pacientes", "numero de pacientes", "n_pacientes",
                 "numero_de_pacientes", "cantidad_pacientes", "cantidad", "total_pacientes"]
        )
        if col_flag is not None and col_num is not None:
            total = int(pd.to_numeric(df[col_num], errors="coerce").fillna(0).sum())
            flags = df[col_flag].astype(str).str.strip().str.lower()
            mask_con = flags.isin(VALORES_CON_FLAG)
            con = int(pd.to_numeric(df.loc[mask_con, col_num], errors="coerce").fillna(0).sum())
            modo_detectado = f"Formato resumido detectado: '{col_flag}' + '{col_num}'"

    if con is None:
        # No se pudo detectar automaticamente: se deja el total y se pide
        # completar manualmente el numero de pacientes con complicacion.
        entry_total.delete(0, tk.END)
        entry_total.insert(0, str(total))
        label_archivo.config(
            text=f"Archivo: {nombre_archivo} ({total} filas). "
                 f"No se detecto una columna de complicaciones: completa 'Con complicacion' manualmente."
        )
        messagebox.showwarning(
            "Columnas no reconocidas",
            "Se cargaron los datos, pero no se encontro una columna de complicaciones "
            "reconocible automaticamente.\nSe cargo el total de pacientes; completa el "
            "campo 'Total de pacientes con complicaciones' manualmente y presiona Calcular."
        )
        actualizar_eda(df)
        return

    entry_con.delete(0, tk.END)
    entry_con.insert(0, str(con))
    entry_total.delete(0, tk.END)
    entry_total.insert(0, str(total))
    label_archivo.config(text=f"Archivo cargado: {nombre_archivo}  |  {modo_detectado}")

    calcular()
    actualizar_eda(df)
    notebook.select(tab_calculadora)


# ====================================================================
# Calculo de la metrica (misma logica del codigo original)
# ====================================================================
def calcular():
    texto_con = entry_con.get().strip()
    texto_total = entry_total.get().strip()

    if not texto_con or not texto_total:
        messagebox.showerror("Error", "Debes llenar los dos campos.")
        return
    try:
        con_complicacion = int(float(texto_con))
        total_pacientes = int(float(texto_total))
    except ValueError:
        messagebox.showerror("Error", "Los campos deben ser numeros enteros.")
        return
    if total_pacientes <= 0:
        messagebox.showerror("Error", "El total de pacientes debe ser mayor a 0.")
        return
    if con_complicacion > total_pacientes:
        messagebox.showerror("Error", "Los pacientes con complicacion no pueden ser mas que el total.")
        return

    sin_complicacion = total_pacientes - con_complicacion
    prevalencia = (con_complicacion / total_pacientes) * 100
    brecha_meta = prevalencia - META_PREVALENCIA
    pacientes_a_reducir = max(0, round((prevalencia - META_PREVALENCIA) / 100 * total_pacientes))

    resultado_label.config(
        text=(
            f"Total de pacientes: {total_pacientes}\n"
            f"Con complicacion: {con_complicacion}\n"
            f"Sin complicacion: {sin_complicacion}\n"
            f"Prevalencia: {prevalencia:.2f}%\n"
            f"Meta del proyecto: {META_PREVALENCIA:.2f}%  "
            f"({'por encima' if brecha_meta > 0 else 'por debajo'} de la meta por "
            f"{abs(brecha_meta):.2f} puntos, ~{pacientes_a_reducir} pacientes a reducir)"
        )
    )

    dibujar_graficas(con_complicacion, sin_complicacion, total_pacientes, prevalencia)


def dibujar_graficas(con_complicacion, sin_complicacion, total_pacientes, prevalencia):
    for widget in frame_graficas.winfo_children():
        widget.destroy()

    etiquetas = ["Con complicacion", "Sin complicacion"]
    valores = [con_complicacion, sin_complicacion]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9, 4.2))

    # grafica de pastel
    ax1.pie(
        valores,
        labels=etiquetas,
        autopct="%1.2f%%",
        colors=["#E74C3C", "#2ECC71"],
        startangle=90,
        explode=(0.05, 0),
        textprops={"fontsize": 9},
    )
    ax1.set_title("Prevalencia de complicaciones", fontsize=10, fontweight="bold")

    # grafica de barras
    barras = ax2.bar(
        etiquetas,
        valores,
        color=["#3498DB", "#95A5A6"],
        edgecolor="black",
        linewidth=1.2,
        width=0.5,
    )
    for barra in barras:
        alto = barra.get_height()
        x = barra.get_x()
        ancho = barra.get_width()
        if alto > 0:
            paso = alto / 6
            for nivel in range(1, 6):
                y = nivel * paso
                ax2.plot([x + 0.06, x + ancho - 0.06], [y, y], color="white", linewidth=1, alpha=0.6)
        ax2.text(barra.get_x() + ancho / 2, alto + total_pacientes * 0.01,
                  f"{int(alto)}", ha="center", va="bottom", fontsize=9, fontweight="bold")

    # lineas de referencia: baseline y meta del proyecto (en numero de pacientes)
    linea_baseline = BASELINE_PREVALENCIA / 100 * total_pacientes
    linea_meta = META_PREVALENCIA / 100 * total_pacientes
    ax2.axhline(linea_baseline, color="#8E44AD", linestyle="--", linewidth=1.2,
                label=f"Baseline hist. ({BASELINE_PREVALENCIA:.2f}%)")
    ax2.axhline(linea_meta, color="#F39C12", linestyle="--", linewidth=1.2,
                label=f"Meta ({META_PREVALENCIA:.0f}%)")
    ax2.legend(fontsize=7, loc="upper right")

    ax2.set_title("Con vs sin complicacion", fontsize=10, fontweight="bold")
    ax2.set_ylabel("Numero de pacientes")

    fig.tight_layout()

    canvas = FigureCanvasTkAgg(fig, master=frame_graficas)
    canvas.draw()
    canvas.get_tk_widget().pack()
    plt.close(fig)


# ====================================================================
# Pestaña de Analisis Exploratorio de Datos (EDA)
# ====================================================================
def actualizar_eda(df):
    for widget in frame_eda_texto.winfo_children():
        widget.destroy()
    for widget in frame_eda_grafico.winfo_children():
        widget.destroy()

    texto = tk.Text(frame_eda_texto, height=14, wrap="word", font=("Consolas", 9))
    texto.pack(fill="both", expand=True, padx=5, pady=5)

    filas, columnas = df.shape
    texto.insert("end", f"Filas x Columnas: {filas} x {columnas}\n\n")

    # --- Valores faltantes ---
    nulos = df.isnull().sum()
    nulos = nulos[nulos > 0]
    texto.insert("end", "Valores faltantes por columna:\n")
    if nulos.empty:
        texto.insert("end", "  (no se detectaron valores faltantes)\n")
    else:
        for col, n in nulos.items():
            pct = n / filas * 100
            texto.insert("end", f"  - {col}: {n} ({pct:.2f}%)\n")
    texto.insert("end", "\n")

    # --- Valores atipicos (IQR) en columnas numericas clave ---
    texto.insert("end", "Valores atipicos (metodo IQR) en columnas numericas:\n")
    columnas_numericas = df.select_dtypes(include=[np.number]).columns.tolist()
    if not columnas_numericas:
        texto.insert("end", "  (no se encontraron columnas numericas)\n")
    else:
        for col in columnas_numericas:
            n_out, lim_inf, lim_sup = calcular_iqr_outliers(df[col])
            if n_out > 0:
                texto.insert("end", f"  - {col}: {n_out} atipicos (limites ~[{lim_inf:.1f}, {lim_sup:.1f}])\n")
    texto.insert("end", "\n")

    # --- Distribucion por tipo de complicacion (si existe la columna) ---
    col_comp = encontrar_columna(df, ["complicaciones", "complicacion"])
    conteo_tipo = None
    if col_comp is not None:
        conteo_tipo = df[col_comp].astype(str).str.strip().value_counts()
        texto.insert("end", f"Distribucion por tipo ('{col_comp}'):\n")
        for tipo, n in conteo_tipo.items():
            texto.insert("end", f"  - {tipo}: {n} ({n / filas * 100:.2f}%)\n")

    texto.config(state="disabled")

    # --- Grafico: distribucion por tipo de complicacion ---
    if conteo_tipo is not None and len(conteo_tipo) > 0:
        fig, ax = plt.subplots(figsize=(8.5, 4.2))
        conteo_tipo_ordenado = conteo_tipo.sort_values(ascending=True)
        ax.barh(conteo_tipo_ordenado.index.astype(str), conteo_tipo_ordenado.values,
                color="#3498DB", edgecolor="black")
        ax.set_title("Casos por tipo de complicacion", fontsize=10, fontweight="bold")
        ax.set_xlabel("Numero de pacientes")
        fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=frame_eda_grafico)
        canvas.draw()
        canvas.get_tk_widget().pack()
        plt.close(fig)


# ====================================================================
# Interfaz grafica
# ====================================================================
ventana = tk.Tk()
ventana.title("Prevalencia de Complicaciones - Proyecto DM")
ventana.geometry("780x780")

titulo = tk.Label(ventana, text="Calculo de Prevalencia de Complicaciones",
                   font=("Arial", 14, "bold"))
titulo.pack(pady=10)

notebook = ttk.Notebook(ventana)
notebook.pack(fill="both", expand=True, padx=10, pady=5)

tab_calculadora = tk.Frame(notebook)
tab_eda = tk.Frame(notebook)
notebook.add(tab_calculadora, text="Calculadora")
notebook.add(tab_eda, text="Analisis Exploratorio (EDA)")

# ---------------- Pestaña 1: Calculadora ----------------
frame_carga = tk.Frame(tab_calculadora)
frame_carga.pack(pady=8)

boton_cargar = tk.Button(
    frame_carga, text="Cargar Excel de pacientes", command=cargar_excel,
    bg="#2ECC71", fg="white", font=("Arial", 11, "bold"), width=25,
)
boton_cargar.pack()

label_archivo = tk.Label(tab_calculadora, text="Ningun archivo cargado (puedes tambien llenar los campos a mano)",
                          font=("Arial", 9), fg="#555555", wraplength=700, justify="center")
label_archivo.pack(pady=(0, 8))

frame_con = tk.Frame(tab_calculadora)
frame_con.pack(pady=5)
tk.Label(frame_con, text="Total de pacientes con complicaciones:", width=32, anchor="w").pack(side="left")
entry_con = tk.Entry(frame_con, width=15)
entry_con.pack(side="left")

frame_total = tk.Frame(tab_calculadora)
frame_total.pack(pady=5)
tk.Label(frame_total, text="Total de pacientes:", width=32, anchor="w").pack(side="left")
entry_total = tk.Entry(frame_total, width=15)
entry_total.pack(side="left")

boton = tk.Button(tab_calculadora, text="Calcular", command=calcular,
                   bg="#3498DB", fg="white", font=("Arial", 11, "bold"), width=15)
boton.pack(pady=10)

resultado_label = tk.Label(tab_calculadora, text="", font=("Arial", 11), justify="left")
resultado_label.pack(pady=5)

frame_graficas = tk.Frame(tab_calculadora)
frame_graficas.pack(pady=10)

# ---------------- Pestaña 2: EDA ----------------
frame_eda_texto = tk.Frame(tab_eda)
frame_eda_texto.pack(fill="both", expand=False, padx=5, pady=5)

frame_eda_grafico = tk.Frame(tab_eda)
frame_eda_grafico.pack(fill="both", expand=True, padx=5, pady=5)

tk.Label(frame_eda_texto, text="Carga un Excel en la pestaña 'Calculadora' para ver aqui el resumen del dataset.",
          font=("Arial", 9), fg="#555555").pack()

ventana.mainloop()
