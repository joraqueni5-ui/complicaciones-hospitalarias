# Marco teórico y bibliografía

Esta sección amplía los conceptos que aparecen en las tablas del notebook y los respalda con fuentes **en español**, consultadas y verificadas el 14 de noviembre de 2026. Las cifras clínicas son de **referencia general para adultos**; el diagnóstico individual siempre lo hace un profesional de la salud.

## A. Variables clínicas del modelo

### A.1 Triglicéridos
Los triglicéridos **no son un tipo de colesterol**: son otro tipo de grasa en la sangre que también se mide en el perfil lipídico y que puede aumentar el riesgo de enfermedad cardíaca [5].

| Categoría | Valor (mg/dL) | Fuente |
|---|---|---|
| Normal / deseable | menos de 150 | [5], [6] |
| Límite alto | 150 – 199 | [5], [6] |
| Alto | 200 – 499 | [6] |
| Muy alto | 500 o más | [6] |

**Uso en el notebook:** línea de referencia en 150 y regla "triglicéridos ≥ 200 (alto)". Variable del modelo K-Means.

### A.2 Colesterol total
El colesterol total reúne el colesterol LDL ("malo"), el HDL ("bueno") y otros componentes; es uno de los números del perfil lipídico [5].

| Categoría | Valor (mg/dL) | Fuente |
|---|---|---|
| Deseable | menos de 200 | [5], [6] |
| Límite superior | 200 – 239 | [6] |
| Alto | 240 o más | [6] |

**Uso en el notebook:** línea de referencia en 200 y regla "colesterol ≥ 240 (alto)". Es la variable que separa a los dos grupos de adultos.

### A.3 Glucemia (glucosa en sangre)
La glucemia es la concentración de azúcar en sangre. El criterio de diagnóstico de diabetes por glucemia en ayunas es **126 mg/dL o más**; ese umbral se propuso a partir de estudios epidemiológicos que lo relacionan con la aparición de complicaciones [3]. Más adelante la ADA bajó el límite superior de lo normal en ayunas de 110 a **100 mg/dL**, lo que redefinió la "glucosa alterada en ayuno" como 100–125 mg/dL [4].

| Categoría (en ayunas) | Valor (mg/dL) | Fuente |
|---|---|---|
| Normal | menos de 100 | [4] |
| Glucosa alterada en ayuno (prediabetes) | 100 – 125 | [4] |
| Rango de diabetes | 126 o más | [3] |

**Uso en el notebook:** línea de referencia en 100 y regla "glucemia ≥ 126". La OMS ofrece además una nota descriptiva general sobre la diabetes y su diagnóstico [2].

> Nota de verificación: el límite inferior de 70 mg/dL que se usa en el texto del Paso 8 es de uso clínico habitual, pero **no apareció textualmente** en las fuentes consultadas para esta bibliografía; el umbral que sí se respalda es el superior (100 y 126).

### A.4 Índice de masa corporal (IMC)
Se calcula como peso (kg) dividido por la estatura al cuadrado (m²) y es la medida que la OMS usa para diagnosticar sobrepeso y obesidad [1].

| Categoría (adultos) | IMC | Fuente |
|---|---|---|
| Sobrepeso | 25 o más | [1] |
| Obesidad | 30 o más | [1] |

**Uso en el notebook:** línea de referencia en 25 y regla "IMC ≥ 30 (obesidad)". El límite 18.5 para "peso normal" es la clasificación OMS habitual, pero **no figura** en la nota descriptiva consultada [1]; por eso solo se respaldan formalmente los cortes de 25 y 30. En niños y adolescentes el IMC se interpreta según la edad, por lo que los cortes de adultos no aplican al grupo "Jóvenes" [1].

### A.5 Creatinina
La creatinina es un residuo de la actividad muscular que los riñones filtran y eliminan por la orina [7], [8]; si los riñones fallan, se acumula en la sangre, y un nivel anormal puede ser signo de enfermedad renal. Lo "normal" depende de la masa muscular, la dieta, la edad y la actividad [7].

| Grupo | Valor orientativo (mg/dL) | Fuente |
|---|---|---|
| Varones adultos sanos | 0.7 – 1.3 | [8] |
| Mujeres adultas sanas | 0.5 – 0.95 | [8] |

**Uso en el notebook:** la regla "creatinina > 1.3 (posible daño renal)" usa el tope masculino; en mujeres el tope es menor, por lo que el porcentaje real de valores elevados sería aún mayor. Un solo valor alto no basta para diagnosticar una enfermedad [7].

### A.6 Hemoglobina
Es la proteína de los glóbulos rojos que transporta oxígeno; su concentración es el criterio principal para definir anemia. La directriz de la OMS 2024 fija como anemia valores **menores de 120 g/L (12 g/dL) en mujeres no embarazadas** y **menores de 130 g/L (13 g/dL) en hombres**, de 15 a 65 años [9].

**Uso en el notebook:** se compara la hemoglobina de pacientes con y sin diagnóstico de anemia (Paso 4).

### A.7 Presión arterial
Se expresa como sistólica/diastólica en mmHg. La OMS define hipertensión como **140/90 mmHg o más**, confirmada con mediciones en dos días distintos [10]. En una medición válida, la presión diastólica (la "baja") es menor que la sistólica (la "alta").

**Uso en el notebook:** se separa "120/80" en dos columnas y se cuentan los registros con diastólica ≥ sistólica (956), físicamente imposibles.

## B. Conceptos de ciencia de datos

| Concepto | Qué es | Uso en el notebook | Fuente |
|---|---|---|---|
| **K-Means** | Algoritmo no supervisado que agrupa observaciones en K grupos cercanos a un centro (centroide) | Paso 6: agrupar pacientes en 4 perfiles | [13], [15] |
| **Normalización / estandarización** | Llevar las variables a una escala común; necesaria en algoritmos basados en distancia | `StandardScaler` (Paso 5) | [13], [15] |
| **WCSS (inercia)** | Suma de distancias al cuadrado de cada punto a su centroide; mide la compacidad | Método del codo (Paso 6) | [14] |
| **Método del codo** | Probar varios K y buscar donde la mejora del WCSS se aplana | Elegir K (Paso 6) | [14] |
| **Coeficiente de silueta** | Mide, de -1 a 1, qué tan bien asignado está cada dato a su grupo; cerca de 1 = bien asignado, cerca de 0 = entre dos grupos, cerca de -1 = mal asignado | Calidad de los clusters (Pasos 6 y 10) | [11], [12] |
| **Limitación de forma** | K-Means supone grupos esféricos y de tamaño parecido | Sección de limitaciones | [13] |

## C. Lista de referencias

**Organismos de salud y fuentes clínicas**

[1] Organización Mundial de la Salud (OMS). *Obesidad y sobrepeso* (nota descriptiva). Define sobrepeso (IMC ≥ 25) y obesidad (IMC ≥ 30) en adultos y el cálculo del IMC. https://www.who.int/es/news-room/fact-sheets/detail/obesity-and-overweight

[2] Organización Mundial de la Salud (OMS). *Diabetes* (nota descriptiva, 14 de noviembre de 2024). https://www.who.int/es/news-room/fact-sheets/detail/diabetes

[3] Birulés Pons M, Fernández Fernández I. *Criterios de cribado y diagnóstico de diabetes mellitus*. Atención Primaria. 2003;31(5):334-336. Documentos semFYC (Sociedad Española de Medicina de Familia y Comunitaria). https://www.elsevier.es/es-revista-atencion-primaria-27-pdf-download-13045696

[4] Revista Médica del Instituto Mexicano del Seguro Social. Artículo sobre la prevalencia de glucosa alterada en ayuno con los criterios ADA-1997 y ADA-2003 (descenso del límite normal de 110 a 100 mg/dL). https://revistamedica.imss.gob.mx/index.php/revista_medica/article/download/4052/3863/23510

[5] MedlinePlus en español, Biblioteca Nacional de Medicina de EE. UU. *Niveles de colesterol: lo que necesita saber*. https://www.medlineplus.gov/spanish/cholesterollevelswhatyouneedtoknow.html

[6] Mayo Clinic (versión en español). *Colesterol alto: diagnóstico y tratamiento*. https://mayoclinic.org/es-es/diseases-conditions/high-blood-cholesterol/diagnosis-treatment/drc-20350806

[7] MedlinePlus en español, Biblioteca Nacional de Medicina de EE. UU. *¿Qué es una prueba de creatinina?* https://www.medlineplus.gov/spanish/pruebas-de-laboratorio/prueba-de-creatinina/

[8] Clínica Universidad de Navarra. *Diccionario médico: creatinina* (valores orientativos en adultos sanos). https://www.cun.es/diccionario-medico/terminos/creatinina

[9] Fundación Bengoa. *Directriz sobre los valores de corte de hemoglobina para definir la anemia en individuos y poblaciones de la Organización Mundial de la Salud, 2024*. Anales Venezolanos de Nutrición. 2024;37(1):61-67. https://doi.org/10.54624/2024.37.1.006 · PDF: https://ve.scielo.org/pdf/avn/v37n1/0798-0752-avn-37-01-61.pdf

[10] Organización Mundial de la Salud (OMS). *Hipertensión* (nota descriptiva, 25 de septiembre de 2025). https://www.who.int/es/news-room/fact-sheets/detail/hypertension

**Estadística y aprendizaje automático**

[11] Rousseeuw PJ. *Silhouettes: a graphical aid to the interpretation and validation of cluster analysis*. Journal of Computational and Applied Mathematics. 1987;20:53-65. https://doi.org/10.1016/0377-0427(87)90125-7 *(artículo original, en inglés; es la referencia fundacional del coeficiente de silueta)*

[12] Nuevo método para el seguimiento de la evolución de los estudiantes basado en técnicas de agrupamiento (explica el coeficiente de silueta en español y su interpretación entre -1 y 1). Acofipapers. https://acofipapers.org/index.php/eiei/article/download/37/32/63

[13] DataCamp (en español). *Introducción a k-Means Clustering con scikit-learn en Python*. 3 de mayo de 2024. https://www.datacamp.com/es/tutorial/k-means-clustering-python

[14] Zilliz. *Comprender el algoritmo de agrupamiento K-means en el aprendizaje automático* (WCSS y selección de K). https://zilliz.com/es/blog/k-means-clustering

[15] OCW Universidad de Cádiz. *Ejercicio 108_01: clustering con K-medias con normalización, visualización y métricas en Python*. https://ocw.uca.es/mod/resource/view.php?id=4665

---
### Notas de verificación

- Todas las fuentes se consultaron en línea el **14/11/2026**. Las cifras de las secciones A.1 a A.7 se contrastaron con el texto de cada fuente; las dos excepciones (límite inferior de glucemia 70 mg/dL e IMC 18.5) están señaladas arriba como **no respaldadas textualmente**.
- La fuente [4] se cita por su contenido y enlace; el enlace permite comprobar título y autores exactos.
- La fuente [11] y el trabajo original de silueta están en inglés porque no existe versión original en español; [12] la explica en español.
- La regla de "fiebre ≥ 38 °C" usada en el Paso 3 no se incluyó en esta bibliografía por no haberse contrastado con una fuente en español.
- Los valores de referencia son generales para adultos y **no sustituyen** el criterio clínico.
