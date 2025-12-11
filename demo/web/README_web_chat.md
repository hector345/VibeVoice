# 🎤 VibeVoice Web Chat - Conversación por Voz Fluida

Una aplicación web moderna que permite conversaciones fluidas por voz con IA, sin necesidad de escribir texto.

## 🌟 Características Principales

### 🎙️ **Chat de Voz Completo**
- **Reconocimiento de voz** automático (Web Speech API)
- **Respuestas inteligentes** usando tu modelo de LM Studio  
- **Síntesis de voz** natural para las respuestas
- **Conversación fluida** sin escribir ni un texto

### 🎨 **Interfaz Moderna**
- Diseño responsivo y elegante
- Indicadores visuales de estado
- Controles táctiles para móviles
- Animaciones fluidas

### ⚡ **Tecnología Avanzada**
- Flask backend con API REST
- JavaScript frontend con Web APIs
- Docker para fácil deployment
- Integración perfecta con LM Studio

## 🚀 Inicio Rápido

### **Opción 1 - Script Automático (Más Fácil)**
```cmd
# Ejecutar con un solo comando:
run_web_chat.bat

# O con docker-compose:
run_web_compose.bat
```

### **Opción 2 - Manual con Docker**
```cmd
# Construir imagen
docker build -f Dockerfile.web -t vibevoice-web .

# Ejecutar
docker run -it --rm --add-host host.docker.internal:host-gateway -p 5000:5000 vibevoice-web
```

### **Opción 3 - Docker Compose**
```cmd
docker-compose up --build vibevoice-web
```

## 🌐 Acceso a la Aplicación

Una vez iniciada, visita:
- **URL**: http://localhost:5000
- **Puerto**: 5000 (configurable)

## 🎯 Cómo Usar

### 1. **Configuración Inicial**
- Asegúrate de que **LM Studio** esté ejecutándose en puerto 1234
- Permite acceso al **micrófono** cuando el navegador lo solicite
- Verifica que el **indicador de estado** esté verde (conectado)

### 2. **Conversación por Voz**
1. **Mantén presionado** el botón del micrófono 🎤
2. **Habla claramente** (verás el texto reconocido)
3. **Suelta el botón** para enviar tu mensaje
4. **Espera la respuesta** de la IA por voz 🔊

### 3. **Controles Disponibles**
- **🎤 Micrófono**: Mantén presionado para hablar
- **🔇 Detener**: Para el audio en reproducción  
- **🗑️ Limpiar**: Borra el historial de chat

## 🔧 Configuración Avanzada

### Variables de Entorno
```env
LM_STUDIO_URL=http://host.docker.internal:1234  # URL de LM Studio
FLASK_DEBUG=false                               # Modo debug
```

### Puertos Personalizados
```cmd
# Cambiar puerto de la aplicación
docker run -p 8080:5000 vibevoice-web python voice_chat_app.py --port 5000

# La app estará en http://localhost:8080
```

### Configuración de LM Studio
```cmd
# Si LM Studio usa otro puerto:
docker run -e LM_STUDIO_URL=http://host.docker.internal:8080 vibevoice-web
```

## 🌍 Compatibilidad de Navegadores

### ✅ **Totalmente Compatible**
- **Chrome/Chromium** (Recomendado)
- **Microsoft Edge**
- **Opera**

### ⚠️ **Parcialmente Compatible**
- **Firefox** (reconocimiento de voz limitado)
- **Safari** (algunas funciones pueden no funcionar)

### 📱 **Móviles**
- **Android Chrome** ✅
- **iOS Safari** ⚠️ (limitaciones de iOS)

## 🔧 Solución de Problemas

### Error: "Tu navegador no soporta reconocimiento de voz"
```
Solución: Usar Chrome, Edge o Chromium
```

### Error: "No se puede acceder al micrófono" 
```
Solución: 
1. Permitir acceso al micrófono en el navegador
2. Verificar permisos del sitio web
3. Comprobar que no hay otras apps usando el micrófono
```

### Error: "No se pudo conectar con LM Studio"
```
Solución:
1. Verificar que LM Studio esté ejecutándose
2. Confirmar que hay un modelo cargado
3. Verificar puerto 1234
4. Revisar firewall/antivirus
```

### La voz no se reproduce
```
Solución:
1. Verificar volumen del sistema
2. Comprobar que no hay otros audios reproduciéndose
3. Probar en modo incógnito
4. Reiniciar navegador
```

### Problemas de Docker
```
# Ver logs del contenedor:
docker logs vibevoice-web-chat

# Verificar conectividad:
docker exec -it vibevoice-web-chat curl http://host.docker.internal:1234/v1/models
```

## 🎨 Personalización

### Cambiar Idioma de Reconocimiento
Editar en `voice_chat.html`:
```javascript
this.recognition.lang = 'en-US';  // Para inglés
this.recognition.lang = 'fr-FR';  // Para francés
```

### Personalizar Voz de Síntesis
```javascript
// Buscar voces específicas
const voice = voices.find(v => v.name.includes('Microsoft Zira'));
if (voice) utterance.voice = voice;
```

### Modificar Estilos
Los estilos están en `voice_chat.html`. Puedes cambiar:
- Colores del gradiente
- Tamaños de botones  
- Animaciones
- Diseño responsive

## 📊 Monitoreo y Logs

### Endpoint de Salud
```
GET /api/health
```
Retorna el estado del servidor y conexión con LM Studio.

### Logs del Servidor
```bash
# Ver logs en tiempo real:
docker logs -f vibevoice-web-chat
```

## 🔄 Comparación de Modos

| Aspecto | Chat Texto | Chat Web Voz |
|---------|------------|-------------|
| **Entrada** | Teclado | Voz (micrófono) |
| **Salida** | Texto + archivo .wav | Voz directa |
| **Interfaz** | Terminal | Navegador web |
| **Portabilidad** | Solo local | Acceso remoto |
| **Facilidad** | Escribir | Solo hablar |
| **Multitarea** | ❌ | ✅ |

## 🚧 Funciones Futuras

- [ ] Soporte para múltiples idiomas simultáneos
- [ ] Integración con VibeVoice TTS del servidor  
- [ ] Grabación y descarga de conversaciones
- [ ] Temas visuales personalizables
- [ ] Soporte para comandos por voz
- [ ] Integración con otros modelos de IA

## 🤝 Contribuir

¿Ideas para mejorar la aplicación web?
1. Fork del repositorio
2. Crear rama feature
3. Implementar mejoras  
4. Pull request

## 📄 Licencia

Misma licencia que VibeVoice.

---

## 🎉 ¡Disfruta tu Chat de Voz!

Ahora puedes conversar naturalmente con IA usando solo tu voz. ¡Es como tener un asistente personal inteligente! 🤖🎤