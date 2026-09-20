# Proposal

## Why

La aplicación depende actualmente de la API comercial de OpenAI para generar respuestas y embeddings, lo que impide ejecutar el chatbot sin credenciales ni costes externos. Se necesita un modo local basado en Ollama y embeddings locales, manteniendo la reproducibilidad del índice FAISS cuando cambie la configuración del modelo.

## What Changes

- Añadir soporte de Ollama como proveedor configurable del modelo de chat.
- Añadir soporte de embeddings locales y mantenerlos seleccionables mediante configuración.
- Instalar y documentar las dependencias necesarias para el modo local.
- Comparar la identidad y configuración efectiva del embedding actual con el manifiesto del índice FAISS.
- Eliminar y reconstruir automáticamente el índice cuando el modelo o la configuración de embeddings hayan cambiado, evitando reutilizar vectores incompatibles.
- Mantener OpenAI como opción compatible cuando se configure explícitamente.
- Añadir pruebas para selección de proveedores, detección de incompatibilidad y reconstrucción del índice.

## Capabilities

### New Capabilities

### Modified Capabilities

- `technical-documentation-rag`: el runtime debe admitir proveedores locales de chat y embeddings, y reconstruir automáticamente el índice persistido cuando la configuración de embeddings no coincida con la registrada.

## Impact

- Afecta a la configuración, construcción de clientes en `src/rag_chatbot/providers.py`, ciclo de vida del índice FAISS y manifiesto de embeddings.
- Requiere nuevas dependencias de integración con Ollama y embeddings locales, además de instrucciones de instalación y configuración.
- Cambia el comportamiento de arranque o construcción del índice: una incompatibilidad de embeddings provoca reemplazo automático del índice, con sus efectos de tiempo y almacenamiento.
- No cambia el contrato de respuestas fundamentadas, citas, validación de documentos ni la interfaz Streamlit salvo los mensajes de estado y error necesarios.
