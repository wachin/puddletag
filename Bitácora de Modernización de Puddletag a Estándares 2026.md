

puddletag-dev/puddletag/MODERNIZACION_2026.md


# 📋 Bitácora de Modernización de Puddletag a Estándares 2026

**Fecha de inicio:** 29 de agosto de 2026  
**Estado actual:** Fase 1 en progreso (Higiene de Código)  
**Estrategia:** Modernización incremental archivo por archivo para evitar romper funcionalidad

---

## 🔧 Reparaciones Realizadas

### ✅ Archivo: `puddlestuff/util.py`

**Fecha:** 29 de agosto de 2026  
**Herramienta utilizada:** `ruff check --fix` + edición manual

#### Cambios automáticos (ruff --fix):
- ✅ Reemplazo de `EnvironmentError` por `OSError` (líneas 350, 368)
- ✅ Conversión de `dict([(k, v) for ...])` a dict comprehensions `{k: v for ...}` (líneas 311, 396, 406)
- ✅ Eliminación de herencia innecesaria de `object` en clases (línea 409)
- ✅ Corrección de imports y sintaxis obsoleta

#### Cambios manuales:
- ✅ Reemplazo de `logging.error()` + `logging.exception(ex)` por `logger.exception("mensaje")` (líneas 358, 370)
- ✅ Uso de logger propio en lugar del logger raíz (LOG015)
- ✅ Eliminación de parámetro redundante en `logging.exception()` (TRY401)

**Resultado:** 0 errores de ruff en este archivo  
**Estado funcional:** ✅ Verificado - El código compila y funciona correctamente

---

## 🛠️ Entorno de Desarrollo

### Herramientas Instaladas (según guía "Entorno Linux Para Agentes IA")

#### ✅ Control de Versiones
- `git` - Control de versiones
- `git-lfs` - Git Large File Storage
- `gh` - GitHub CLI
- `git-flow` - Flujo de trabajo Git
- `gitk` - Visualizador gráfico
- `tig` - Visualizador en terminal

#### ✅ Python y Desarrollo
- `python3` - Intérprete Python 3.11
- `python3-pip` - Gestor de paquetes
- `python3-venv` - Entornos virtuales
- `python3-dev` - Archivos de desarrollo
- `build-essential` - Compiladores (gcc, make, etc.)
- `python3-mypy` - Verificador de tipos estáticos

#### ✅ Análisis de Código
- `ruff` - Linter y formateador ultra-rápido (instalado vía pip)
- `ripgrep` (rg) - Búsqueda recursiva ultra-rápida
- `fd-find` (fdfind) - Búsqueda de archivos por nombre
- `jq` - Procesador de JSON
- `tree` - Visualización de estructura de directorios
- `bat` - Cat mejorado con resaltado de sintaxis
- `silversearcher-ag` (ag) - Búsqueda rápida de código
- `universal-ctags` - Generación de índices de código

#### ✅ Herramientas GNU Esenciales
- `findutils` - find, xargs
- `coreutils` - ls, cp, mv, cat, sort, uniq, wc, etc.
- `grep` - Búsqueda de patrones
- `sed` - Edición de texto
- `gawk` - Procesamiento de texto
- `diffutils` - diff, comm
- `parallel` - Ejecución paralela de comandos

#### ✅ Compresión y Archivos
- `unzip` / `zip` - Formato ZIP
- `tar` - Archivos tar/gz/bz2/xz
- `xz-utils` - Compresión XZ
- `zstd` - Compresión Zstandard
- `p7zip-full` - Soporte 7z
- `rsync` - Sincronización eficiente
- `file` - Identificación de tipo de archivo

#### ✅ Análisis de Binarios
- `binutils` - readelf, objdump, strings, nm, strip, ar
- `elfutils` - eu-readelf, eu-objdump
- `strace` - Seguimiento de llamadas al sistema
- `ltrace` - Seguimiento de llamadas a bibliotecas
- `patchelf` - Modificación de ELF

#### ✅ Paquetes Debian
- `dpkg-dev` - dpkg-deb, dpkg-buildpackage
- `debhelper` - dh
- `devscripts` - debuild, dch, debchange
- `fakeroot` - Simular usuario root
- `lintian` - Verificador de calidad .deb
- `desktop-file-utils` - desktop-file-validate
- `dpkg-repack` - Reconstruir .deb

#### ✅ AppImage
- `squashfs-tools` - unsquashfs, mksquashfs
- `squashfuse` - Montar squashfs sin root
- `fuse3` / `fuse` - Filesystem in Userspace

#### ✅ Red y Debugging
- `net-tools` - netstat, ifconfig
- `iproute2` - ip, ss
- `socat` - Multiplexor de sockets
- `ncat` - Cliente/servidor TCP/UDP
- `httpie` - Cliente HTTP amigable
- `curl` - Cliente HTTP
- `wget` - Descarga de archivos
- `tmux` - Multiplexor de terminal
- `screen` - Sesiones de terminal

#### ✅ Texto y Documentación
- `pandoc` - Conversor universal de documentos
- `texlive-base` - pdflatex
- `groff` - Formateado de texto
- `vim` / `nano` - Editores de texto
- `htop` / `btop` - Monitoreo de procesos
- `less` - Visualizador de archivos

#### ✅ Configuración Post-Instalación
- ✅ `fd` configurado como alias de `fdfind`
- ✅ PATH actualizado con `~/.local/bin`
- ✅ Git configurado con usuario y email

---

## 📊 Estado Actual del Proyecto

### Estadísticas de Ruff (29 de agosto de 2026)

```bash
# Antes de las reparaciones:
Found 974 errors
[*] 331 fixable with the `--fix` option

# Después de ruff --fix:
Found 644 errors
[*] 369 fixable with the `--fix` option

# Después de ruff format:
92 files reformatted, 3 files left unchanged
```

### Archivos con Errores Pendientes

**Total de archivos con errores:** ~90 archivos  
**Archios completados:** 1 archivo (`puddlestuff/util.py`)  
**Progreso:** ~1%

---

## 🎯 Plan de Modernización Paso a Paso

### Reglas Críticas para No Romper el Código

1. **UN archivo a la vez** - Nunca modificar múltiples archivos simultáneamente
2. **Probar después de cada cambio** - Ejecutar `python3 puddletag` para verificar que inicia
3. **Commits frecuentes** - Hacer commit después de cada archivo completado
4. **Backup antes de cambios grandes** - `cp archivo.py archivo.py.backup`
5. **Verificar con ruff** - `ruff check archivo.py` debe mostrar 0 errores
6. **No cambiar lógica de negocio** - Solo sintaxis y estilo, no funcionalidad

### Flujo de Trabajo para Cada Archivo

```bash
# 1. Ver errores del archivo
ruff check puddlestuff/nombre_archivo.py

# 2. Aplicar correcciones automáticas
ruff check puddlestuff/nombre_archivo.py --fix

# 3. Formatear el código
ruff format puddlestuff/nombre_archivo.py

# 4. Verificar que quedan 0 errores
ruff check puddlestuff/nombre_archivo.py

# 5. Probar que puddletag aún funciona
python3 puddletag

# 6. Si todo funciona, hacer commit
git add puddlestuff/nombre_archivo.py
git commit -m "Modernizar nombre_archivo.py: f-strings, type hints, sintaxis 2026"

# 7. Actualizar este documento (MODERNIZACION_2026.md)
```

---

## 📝 Lista de Archivos Pendientes (Orden de Prioridad)

### Prioridad 1: Archivos Críticos del Sistema
Estos archivos son usados por todo el sistema, modernizarlos primero.

- [ ] `puddlestuff/__init__.py` - Inicialización del paquete
- [ ] `puddlestuff/constants.py` - Constantes globales
- [ ] `puddlestuff/translations.py` - Sistema de traducciones
- [ ] `puddlestuff/puddleobjects.py` - Objetos base (archivo grande, ~2500 líneas)
- [ ] `puddlestuff/puddletag.py` - Aplicación principal
- [ ] `puddlestuff/puddlesettings.py` - Configuración

### Prioridad 2: Módulos de Audio
Manejo de formatos de audio, crítico para la funcionalidad.

- [ ] `puddlestuff/audioinfo/__init__.py`
- [ ] `puddlestuff/audioinfo/util.py`
- [ ] `puddlestuff/audioinfo/id3.py`
- [ ] `puddlestuff/audioinfo/vorbis.py`
- [ ] `puddlestuff/audioinfo/mp4.py`
- [ ] `puddlestuff/audioinfo/apev2.py`
- [ ] `puddlestuff/audioinfo/wma.py`
- [ ] `puddlestuff/audioinfo/constants.py`
- [ ] `puddlestuff/audioinfo/tag_versions.py`
- [ ] `puddlestuff/audioinfo/formats.py`
- [ ] `puddlestuff/audioinfo/_compatid3.py`

### Prioridad 3: Funciones y Acciones
Lógica de negocio de las funciones de etiquetado.

- [ ] `puddlestuff/functions.py` - Funciones de etiquetado
- [ ] `puddlestuff/findfunc.py` - Búsqueda y procesamiento
- [ ] `puddlestuff/actiondlg.py` - Diálogos de acciones
- [ ] `puddlestuff/action_shortcuts.py` - Atajos de acciones
- [ ] `puddlestuff/functions_dialogs.py` - Diálogos de funciones

### Prioridad 4: Fuentes de Etiquetas
Integración con servicios externos.

- [ ] `puddlestuff/tagsources/__init__.py`
- [ ] `puddlestuff/tagsources/musicbrainz.py`
- [ ] `puddlestuff/tagsources/discogs.py`
- [ ] `puddlestuff/tagsources/amazon.py`
- [ ] `puddlestuff/tagsources/acoust_id.py`
- [ ] `puddlestuff/tagsources/freedb.py`
- [ ] `puddlestuff/tagsources/amg.py`
- [ ] `puddlestuff/tagsources/parse_html.py`
- [ ] `puddlestuff/tagsources/CDDB.py`
- [ ] `puddlestuff/tagsources/TagSource.py`
- [ ] `puddlestuff/tagsources/example.py`
- [ ] `puddlestuff/tagsources/exampletags.py`
- [ ] `puddlestuff/tagsources/mp3tag/__init__.py`
- [ ] `puddlestuff/tagsources/mp3tag/funcs.py`
- [ ] `puddlestuff/tagsources/mp3tag/parse_debug.py`

### Prioridad 5: Interfaz Principal (mainwin)
Componentes de la ventana principal.

- [ ] `puddlestuff/mainwin/__init__.py`
- [ ] `puddlestuff/mainwin/funcs.py`
- [ ] `puddlestuff/mainwin/tagpanel.py`
- [ ] `puddlestuff/mainwin/artwork.py`
- [ ] `puddlestuff/mainwin/dirview.py`
- [ ] `puddlestuff/mainwin/filterwin.py`
- [ ] `puddlestuff/mainwin/patterncombo.py`
- [ ] `puddlestuff/mainwin/previews.py`
- [ ] `puddlestuff/mainwin/storedtags.py`
- [ ] `puddlestuff/mainwin/tagtools.py`
- [ ] `puddlestuff/mainwin/action_dialogs.py`
- [ ] `puddlestuff/mainwin/logdialog.py`
- [ ] `puddlestuff/mainwin/logwin.py`
- [ ] `puddlestuff/mainwin/releasewidget.py`
- [ ] `puddlestuff/mainwin/statistics.py`
- [ ] `puddlestuff/mainwin/dupes.py`
- [ ] `puddlestuff/mainwin/teststuff.py`

### Prioridad 6: Modelo de Datos
Modelo de la tabla y manejo de etiquetas.

- [ ] `puddlestuff/tagmodel.py` - Modelo de la tabla principal

### Prioridad 7: Bibliotecas de Música
Integración con reproductores.

- [ ] `puddlestuff/libraries/__init__.py`
- [ ] `puddlestuff/libraries/quodlibetlib.py`
- [ ] `puddlestuff/libraries/rhythmbox.py`
- [ ] `puddlestuff/libraries/mpdlib.py`

### Prioridad 8: Etiquetado Masivo
Funcionalidad de masstagging.

- [ ] `puddlestuff/masstag/__init__.py`
- [ ] `puddlestuff/masstag/config.py`
- [ ] `puddlestuff/masstag/dialogs.py`

### Prioridad 9: Duplicados
Búsqueda de duplicados.

- [ ] `puddlestuff/duplicates/__init__.py`
- [ ] `puddlestuff/duplicates/algwin.py`
- [ ] `puddlestuff/duplicates/dupefuncs.py`
- [ ] `puddlestuff/duplicates/matchfuncs.py`

### Prioridad 10: Plugins
Plugins incluidos.

- [ ] `puddlestuff/plugins/__init__.py`
- [ ] `puddlestuff/plugins/modified_time/__init__.py`
- [ ] `puddlestuff/plugins/extended_tags/__init__.py`
- [ ] `puddlestuff/plugins/view_all_fields/__init__.py`
- [ ] `puddlestuff/plugins/dupe_fields/__init__.py`
- [ ] `puddlestuff/plugins/save_tags/__init__.py`
- [ ] `puddlestuff/plugins/id3_tools/__init__.py`
- [ ] `puddlestuff/plugins/export_tags/__init__.py`

### Prioridad 11: Archivos Auxiliares
Otros módulos del sistema.

- [ ] `puddlestuff/helperwin.py` - Ventanas auxiliares
- [ ] `puddlestuff/genres.py` - Gestión de géneros
- [ ] `puddlestuff/confirmations.py` - Confirmaciones
- [ ] `puddlestuff/loadshortcuts.py` - Carga de atajos
- [ ] `puddlestuff/shortcutsettings.py` - Configuración de atajos
- [ ] `puddlestuff/about.py` - Diálogo "Acerca de"
- [ ] `puddlestuff/theme.py` - Temas
- [ ] `puddlestuff/funcprint.py` - Impresión de funciones
- [ ] `puddlestuff/m3u.py` - Manejo de playlists
- [ ] `puddlestuff/export.py` - Exportación
- [ ] `puddlestuff/cli.py` - Interfaz de línea de comandos
- [ ] `puddlestuff/musiclib.py` - Biblioteca de música
- [ ] `puddlestuff/pluginloader.py` - Cargador de plugins
- [ ] `puddlestuff/audio_filter.py` - Filtro de audio
- [ ] `puddlestuff/resource.py` - Recursos
- [ ] `puddlestuff/plugindocs.py` - Documentación de plugins
- [ ] `puddlestuff/tagsourcedocs.py` - Documentación de fuentes
- [ ] `puddlestuff/functiondocs.py` - Documentación de funciones

### Prioridad 12: Archivos de Script
Scripts ejecutables.

- [ ] `puddletag` - Script principal de lanzamiento
- [ ] `console` - Consola de puddletag
- [ ] `get_tag.py` - Script para obtener etiquetas
- [ ] `restore_tag.py` - Script para restaurar etiquetas
- [ ] `tagbackup.py` - Backup de etiquetas

---

## 🔄 Historial de Cambios

### 29 de agosto de 2026

#### Sesión 1: Configuración Inicial
- ✅ Instalación de herramientas de análisis (ruff, pytest, mypy)
- ✅ Ejecución de `ruff check puddlestuff/` - 974 errores encontrados
- ✅ Ejecución de `ruff check --fix` - 369 errores corregidos automáticamente
- ✅ Ejecución de `ruff format` - 92 archivos formateados
- ✅ Resultado: 644 errores restantes (requieren intervención manual)

#### Sesión 2: Modernización de util.py
- ✅ Archivo: `puddlestuff/util.py`
- ✅ Correcciones automáticas con `ruff --fix`
- ✅ Correcciones manuales de logging
- ✅ Verificación: 0 errores restantes en el archivo
- ✅ Estado: Completado y funcional

---

## 📌 Notas Importantes

### Sobre la API Gratuita de TokenRouter
- **Modelo:** `qwen/qwen3.8-max-free`
- **Límite de contexto:** 262,144 tokens
- **Estrategia:** Trabajar archivo por archivo para no exceder el límite
- **Tip:** Si aparece error de tokens, iniciar nuevo chat y continuar desde el último archivo completado

### Sobre las Traducciones
- Los archivos `.ts` y `.qm` NO deben modificarse manualmente
- Se regeneran con `python3 update_translation.py es_ES`
- Las traducciones están en `puddlestuff/translations/`

### Sobre los Tests
- Tests ubicados en `tests/`
- Ejecutar con: `python3 -m pytest tests/ -v`
- No modificar tests hasta que toda la modernización esté completa

### Sobre la Documentación
- Documentación en `docs/`
- Se genera con Sphinx
- No modificar hasta finalizar modernización

---

## ✅ Checklist de Verificación Final

Cuando todos los archivos estén modernizados:

- [ ] `ruff check puddlestuff/` muestra 0 errores
- [ ] `ruff format --check puddlestuff/` muestra todos los archivos formateados
- [ ] `python3 -m pytest tests/ -v` todos los tests pasan
- [ ] `python3 puddletag` la aplicación inicia correctamente
- [ ] Cargar directorio con archivos de audio funciona
- [ ] Editar etiquetas funciona
- [ ] Guardar cambios funciona
- [ ] Búsqueda en fuentes de etiquetas funciona (MusicBrainz, Discogs, etc.)
- [ ] Exportación funciona
- [ ] Importación funciona
- [ ] Plugins se cargan correctamente

---

## 📞 Comandos Útiles

```bash
# Ver estado actual de errores
ruff check puddlestuff/ | wc -l

# Ver errores de un archivo específico
ruff check puddlestuff/nombre_archivo.py

# Corregir automáticamente un archivo
ruff check puddlestuff/nombre_archivo.py --fix

# Formatear un archivo
ruff format puddlestuff/nombre_archivo.py

# Ver qué archivos tienen más errores
ruff check puddlestuff/ --statistics

# Probar que puddletag funciona
python3 puddletag

# Ver logs de la aplicación
tail -f ~/.config/puddletag/puddletag.log

# Hacer backup de un archivo antes de modificarlo
cp archivo.py archivo.py.backup

# Ver diff de cambios
git diff puddlestuff/nombre_archivo.py

# Hacer commit de cambios
git add puddlestuff/nombre_archivo.py
git commit -m "Modernizar nombre_archivo.py"

# Ver progreso
git log --oneline | head -20
```

---

## 🎓 Lecciones Aprendidas

1. **No pedir a la IA que modernice todo el proyecto de una vez** - Excede el límite de contexto
2. **Trabajar archivo por archivo** - Más seguro y controlable
3. **Usar herramientas automáticas primero** - `ruff --fix` ahorra mucho tiempo
4. **Probar después de cada cambio** - Detectar problemas temprano
5. **Documentar todo** - Este archivo sirve como referencia futura
6. **Commits frecuentes** - Facilita rollback si algo sale mal

---

## 📅 Próximos Pasos

1. Continuar con **Prioridad 1: Archivos Críticos del Sistema**
2. Empezar con `puddlestuff/__init__.py`
3. Seguir el flujo de trabajo definido
4. Actualizar este documento después de cada archivo completado
5. Hacer commit después de cada archivo

---

**Última actualización:** 29 de agosto de 2026  
**Próximo archivo a modernizar:** `puddlestuff/__init__.py`
