# AI_LOG — Registro de uso de IA en el desarrollo

Este documento describe cómo usé IA (Claude, de Anthropic) durante el desarrollo de la Polla Mundialista, qué generó, qué decidí y verifiqué yo, y qué problemas reales tuve que resolver en el camino.

## 1. Planeación

Antes de escribir una sola línea de código, le pedí a la IA que desglosara la prueba técnica en un plan de trabajo concreto para el día. No dejé que asumiera nada: me hizo preguntas puntuales sobre el stack que prefería (Python + React + SQL), el tiempo disponible ese día, y dónde pensaba hostear la app. Con esas respuestas, la IA propuso un stack específico (FastAPI + PostgreSQL + React/Vite + Render/Vercel) y un plan por fases con tiempos estimados: setup, diseño de esquema, auth, predicciones, panel admin, leaderboard, testing, deploy y documentación.

Ese plan fue la guía que seguimos todo el día. Lo usé como checklist real, no como un documento decorativo.

## 2. Generación del proyecto base

Con el plan aprobado, le pedí a la IA que generara la primera versión funcional del proyecto completo: backend en FastAPI (modelos, auth con JWT, endpoints de predicciones/admin/leaderboard, seeder de datos) y frontend en React con Vite y Tailwind (login, registro, vista de partidos, panel admin, ranking).

La IA generó el código completo del esqueleto funcional. Mi trabajo en esta parte fue:
- Revisar la estructura de carpetas y el modelo de datos (usuarios, grupos, partidos, predicciones) antes de aceptarlo.
- Leer el código generado (modelos, endpoints, lógica de autenticación y de cálculo de puntos) para entender qué hacía cada parte antes de correrlo, no solo confiar en que "compilara".
- Correrlo yo mismo en mi máquina (no me quedé con que "compilara" en el entorno de la IA — lo probé de verdad con mi propio Python y Node).
- Verificar el flujo completo end-to-end (registro, login, predicción, carga de resultado como admin, cálculo de puntos, ranking) antes de dar por bueno cualquier módulo.

## 3. Depuración de errores reales durante la ejecución local

Al correr el proyecto en mi máquina aparecieron varios errores que la IA no había anticipado y que tuve que reportar con el traceback completo para que los diagnosticara:

- **Incompatibilidad `passlib` + `bcrypt`**: la librería `passlib` (usada originalmente para el hashing de contraseñas) es un paquete sin mantenimiento que rompe con versiones nuevas de `bcrypt`. Solución: reemplazar `passlib` por el uso directo de la librería `bcrypt`.
- **`email-validator` faltante**: Pydantic necesita este paquete para validar el tipo `EmailStr`, y no estaba en `requirements.txt`. Tuve que instalarlo y luego asegurarme de que quedara declarado en el archivo de dependencias (si no, funcionaba local pero fallaba en el deploy).

En ambos casos, mi aporte fue ejecutar el código, capturar el error exacto y decidir si la solución propuesta tenía sentido antes de aplicarla.

## 4. Deploy: la parte donde más aprendí

Nunca había desplegado un proyecto en Render ni en Vercel, así que esta fue la parte con más curva de aprendizaje real. La IA me guió paso a paso por la configuración de ambas plataformas (Root Directory, Build/Start Command, variables de entorno, bases de datos gestionadas), pero **los errores de producción los tuve que reportar yo con capturas de pantalla y logs reales**, y en varios casos la causa no era obvia:

- **`psycopg2` fallando en el build de Render**: Render estaba usando Python 3.14 (recién salido) y el driver de Postgres todavía no tenía soporte para esa versión. Se resolvió fijando Python 3.11 con un archivo `runtime.txt`.
- **404 en rutas de React Router en Vercel**: al entrar directo a `/login` o recargar la página, Vercel devolvía 404 porque no sabía redirigir rutas de una SPA. Se resolvió agregando un `vercel.json` con reglas de `rewrites`.
- **Base de datos de producción vacía**: el archivo `backend/.env` nunca llegó a crearse en mi máquina. Sin ese archivo, la aplicación usaba los valores por defecto del código (SQLite local), así que el seeder corría "sin errores" pero nunca tocaba la base de Postgres de producción. Tuve que crear el `.env` real con la URL de conexión correcta para que el seeder poblara la base de datos verdadera.

En cada uno de estos casos, el patrón de trabajo fue el mismo: yo ejecutaba, pegaba el error real (log de Render, consola del navegador, captura de pantalla), y la IA proponía un diagnóstico y una solución concreta que yo aplicaba y volvía a probar. No hubo ningún cambio que se diera por bueno sin que yo lo verificara corriendo la app de verdad.

## 5. Qué generó la IA vs. qué hice yo

| Generado por la IA | Hecho por mí |
|---|---|
| Código base del backend y frontend | Instalación de dependencias, entornos virtuales, Node |
| Explicación de la estructura y decisiones de diseño propuestas | Lectura y revisión del código generado antes de correrlo, para entender qué hacía cada parte |
| Diagnóstico de cada error a partir de logs/capturas | Ejecutar el proyecto y capturar los errores reales |
| Configuración sugerida para Render y Vercel | Crear las cuentas, los servicios y pegar la configuración |
| Reglas de puntuación y estructura de la base de datos | Verificar manualmente que los puntos calcularan bien |
| Este mismo documento (AI_LOG.md) | Revisión y aprobación del contenido |

## 6. Conclusión

La IA fue clave para no perder tiempo escribiendo boilerplate y para no quedarme trabado en herramientas de deploy que no conocía (Render y Vercel), pero el desarrollo no fue "copiar y pegar": revisé el código generado antes de aceptarlo, cada módulo se probó de verdad en mi máquina y en producción, y cada error de despliegue se resolvió con mi propio diagnóstico inicial (leyendo el log, tomando la captura, identificando qué pantalla estaba viendo) antes de pedir ayuda puntual para la causa raíz.
