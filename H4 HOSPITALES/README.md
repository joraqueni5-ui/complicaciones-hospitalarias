# H4 HOSPITALES

K-Means para perfilar pacientes hospitalarios (proyecto de minería de datos, complicaciones hospitalarias).

## Contenido

| Archivo | Descripción |
|---|---|
| `h4_1_kmeans_complicaciones_comentado.ipynb` | Notebook completo; **cada línea de código lleva un comentario** que explica qué hace. Incluye al final el marco teórico y la bibliografía. |
| `BIBLIOGRAFIA.md` | Marco teórico y bibliografía en español (triglicéridos, colesterol, glucemia, IMC, creatinina, hemoglobina, presión arterial, K-Means, silueta), con enlaces verificables. |

## Cómo ejecutarlo

1. Instalar dependencias: `pip install pandas numpy matplotlib seaborn scikit-learn openpyxl jupyter`
2. Abrir el notebook desde esta carpeta. El Excel se busca junto al notebook o en `../proyectoKRISKAO/`.
3. Ejecutar todas las celdas (Kernel > Restart & Run All).

## Resultados de referencia (semilla 42)

- K = 4 clusters, WCSS = 34,052.60, Silhouette = 0.1471 (débil).
- Prevalencia global de complicaciones: 87.82 %; ningún grupo se aparta de ese valor (87.6 % a 88.2 %).
- El dataset presenta inconsistencias médicas graves, lo que indica que es simulado.
