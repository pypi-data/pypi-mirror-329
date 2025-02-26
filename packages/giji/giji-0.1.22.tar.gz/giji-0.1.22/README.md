# Giji

Herramientas Git potenciadas por IA para optimizar tu flujo de trabajo de desarrollo. Crea commits inteligentes y pull requests con descripciones generadas por IA, con integración completa con Jira.

## Características

- 🤖 **Commits Inteligentes**: Genera automáticamente mensajes de commit convencionales usando IA
- 📝 **Pull Requests con IA**: Crea PRs con descripciones generadas por IA
- 🎫 **Integración con Jira**: Gestión completa de tickets y comentarios automáticos
- 🚀 **Interfaz Simple**: Comandos CLI fáciles de usar


## Instalación

```bash
pip install giji
```

## Uso

### Pull Requests

Crea pull requests con descripciones generadas por IA:

```bash
# Crear un PR (auto-commit por defecto)
giji pr --base main

# Crear PR y agregar comentario en Jira
giji pr --base main --comment

# Crear un PR sin auto-commit
giji pr --base main --no-commit

# Crear un PR borrador con ticket JIRA
giji pr --base main --draft --ticket SIS-123

# Ver comandos adicionales
giji pr --help

```

### Commits Inteligentes

Crea commits con mensajes convencionales generados por IA:

```bash
# Hacer commit de todos los cambios con mensajes inteligentes
giji commit
```

### Integración con Jira

Gestiona tickets y mantén la documentación sincronizada:

```bash
# Ver descripción de un ticket
giji jira describe SIS-123

# Agregar comentario manual
giji jira comment SIS-123 "Actualizando estado..."

# Analizar PR y comentar automáticamente
giji jira analyze-pr --base main

# Buscar tickets
giji jira search "texto a buscar"
```

### Opciones

#### Comando PR

- `--base, -b`: Rama base (ej: main, develop) [default: master]
- `--ticket, -t`: Número de ticket JIRA (ej: SIS-290)
- `--draft, -d`: Crear PR como borrador
- `--no-commit, -n`: Omitir auto-commit de cambios
- `--comment, -c`: Agregar comentario en Jira automáticamente

#### Comando Jira

- `describe`: Ver descripción de un ticket
- `comment`: Agregar comentario manual
- `analyze-pr`: Analizar PR y comentar automáticamente
- `search`: Buscar tickets
- `config`: Configurar conexión con Jira

## Requisitos

- Python 3.7+
- Git
- GitHub CLI (`gh`)
- API key de Gemini
- Credenciales de Jira (para funcionalidades de Jira)

## Configuración del Entorno

1. Obtén una API key de Gemini en [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Configura las variables de entorno:

```bash
# Configuración de Gemini
export GEMINI_API_KEY='your-api-key'

# Configuración de Jira (opcional, solo para funcionalidades de Jira)
export JIRA_SERVER_URL='https://your-domain.atlassian.net'
export JIRA_EMAIL='your.email@company.com'
export JIRA_TOKEN='your-api-token'
```

Para obtener tu token de Jira:
1. Ve a [Atlassian API Tokens](https://id.atlassian.com/manage-profile/security/api-tokens)
2. Crea un nuevo token
3. Copia el token y configúralo como JIRA_TOKEN

## Licencia

MIT License - ver [LICENSE](LICENSE) para más detalles.


## Soporte

Si encuentras algún problema o tienes una sugerencia, por favor crea un issue en el [repositorio de GitHub](https://github.com/cometa/giji/issues).
