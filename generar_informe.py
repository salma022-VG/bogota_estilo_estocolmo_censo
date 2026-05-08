"""
Generador de informe completo del proyecto Bogotá Estilo Estocolmo
Extrae información de todos los archivos y genera un reporte detallado.
"""

import os
import json
import re
import subprocess
from pathlib import Path
from datetime import datetime
from collections import defaultdict

ROOT = Path(__file__).parent
REPORT_PATH = ROOT / f"informe_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"


# ─── Utilidades ────────────────────────────────────────────────────────────────

def run(cmd):
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=ROOT, shell=True)
        return result.stdout.strip()
    except Exception:
        return ""

def human_size(bytes_):
    for unit in ("B", "KB", "MB", "GB"):
        if bytes_ < 1024:
            return f"{bytes_:.1f} {unit}"
        bytes_ /= 1024
    return f"{bytes_:.1f} GB"

def file_size(path):
    try:
        return os.path.getsize(path)
    except Exception:
        return 0


# ─── Sección: Metadatos del proyecto ──────────────────────────────────────────

def seccion_metadatos():
    lines = ["# Informe del Proyecto: Bogotá Estilo Estocolmo\n"]
    lines.append(f"**Generado:** {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
    lines.append(f"**Ruta:** `{ROOT}`\n")
    lines.append(f"**Sistema:** {os.name.upper()} / {os.sys.platform}\n")
    return "\n".join(lines)


# ─── Sección: Estructura de archivos ──────────────────────────────────────────

def seccion_estructura():
    lines = ["---", "## 1. Estructura de Archivos\n"]
    total_size = 0
    file_count = 0
    ext_counts = defaultdict(int)
    ext_sizes = defaultdict(int)

    for root, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d != ".git"]
        level = Path(root).relative_to(ROOT).parts
        indent = "  " * len(level)
        folder = Path(root).name if level else str(ROOT)
        if level:
            lines.append(f"{indent[:-2]}📁 **{folder}/**")
        for f in sorted(files):
            path = Path(root) / f
            size = file_size(path)
            total_size += size
            file_count += 1
            ext = path.suffix.lower() or "(sin ext)"
            ext_counts[ext] += 1
            ext_sizes[ext] += size
            lines.append(f"{indent}  - `{f}` ({human_size(size)})")

    lines.append(f"\n**Total:** {file_count} archivos · {human_size(total_size)}\n")
    lines.append("\n### Distribución por extensión\n")
    lines.append("| Extensión | Archivos | Tamaño total |")
    lines.append("|-----------|----------|--------------|")
    for ext, count in sorted(ext_counts.items(), key=lambda x: -x[1]):
        lines.append(f"| `{ext}` | {count} | {human_size(ext_sizes[ext])} |")

    return "\n".join(lines)


# ─── Sección: HTML ─────────────────────────────────────────────────────────────

def seccion_html():
    lines = ["---", "## 2. Análisis del HTML (index.html)\n"]
    html_path = ROOT / "index.html"
    if not html_path.exists():
        return "\n".join(lines + ["_Archivo no encontrado._"])

    content = html_path.read_text(encoding="utf-8", errors="ignore")
    all_lines = content.splitlines()
    lines.append(f"- **Líneas totales:** {len(all_lines):,}")
    lines.append(f"- **Tamaño:** {human_size(file_size(html_path))}\n")

    # Meta tags
    metas = re.findall(r'<meta\s+([^>]+)>', content, re.IGNORECASE)
    lines.append("### Meta tags\n")
    for m in metas[:15]:
        lines.append(f"- `<meta {m.strip()}>`")

    # Librerías externas
    scripts = re.findall(r'<script[^>]+src=["\']([^"\']+)["\']', content, re.IGNORECASE)
    links = re.findall(r'<link[^>]+href=["\']([^"\']+)["\']', content, re.IGNORECASE)
    lines.append("\n### Librerías / recursos externos\n")
    for s in scripts:
        lines.append(f"- (JS) `{s}`")
    for l in links:
        lines.append(f"- (CSS/Font) `{l}`")

    # Secciones HTML por id/class destacados
    ids = re.findall(r'\bid=["\']([^"\']+)["\']', content)
    lines.append(f"\n### IDs HTML ({len(ids)} encontrados)\n")
    for i in sorted(set(ids)):
        lines.append(f"- `#{i}`")

    # Conteo de etiquetas
    tags = re.findall(r'<([a-zA-Z][a-zA-Z0-9]*)', content)
    tag_counts = defaultdict(int)
    for t in tags:
        tag_counts[t.lower()] += 1
    lines.append("\n### Etiquetas más usadas\n")
    lines.append("| Etiqueta | Veces |")
    lines.append("|----------|-------|")
    for tag, count in sorted(tag_counts.items(), key=lambda x: -x[1])[:20]:
        lines.append(f"| `<{tag}>` | {count} |")

    return "\n".join(lines)


# ─── Sección: CSS ──────────────────────────────────────────────────────────────

def seccion_css():
    lines = ["---", "## 3. Análisis del CSS\n"]
    html_path = ROOT / "index.html"
    if not html_path.exists():
        return "\n".join(lines + ["_No se encontró index.html._"])

    content = html_path.read_text(encoding="utf-8", errors="ignore")
    style_blocks = re.findall(r'<style[^>]*>(.*?)</style>', content, re.DOTALL | re.IGNORECASE)
    css = "\n".join(style_blocks)

    lines.append(f"- **CSS embebido:** {len(css):,} caracteres · {len(css.splitlines()):,} líneas\n")

    # Variables CSS
    variables = re.findall(r'(--.+?)\s*:', css)
    lines.append("### Variables CSS (custom properties)\n")
    var_values = {}
    for var in sorted(set(variables)):
        match = re.search(rf'{re.escape(var)}\s*:\s*([^;]+);', css)
        var_values[var] = match.group(1).strip() if match else "?"
    for var, val in var_values.items():
        lines.append(f"- `{var}`: `{val}`")

    # Clases
    classes = re.findall(r'\.([\w-]+)\s*[{,]', css)
    class_counts = defaultdict(int)
    for c in classes:
        class_counts[c] += 1
    lines.append(f"\n### Clases CSS ({len(set(classes))} únicas)\n")
    for cls in sorted(set(classes)):
        lines.append(f"- `.{cls}`")

    # Keyframes
    keyframes = re.findall(r'@keyframes\s+([\w-]+)', css)
    lines.append(f"\n### Animaciones @keyframes ({len(keyframes)})\n")
    for kf in keyframes:
        lines.append(f"- `@keyframes {kf}`")

    # Media queries
    mq = re.findall(r'@media\s+([^{]+)', css)
    lines.append(f"\n### Media queries ({len(mq)})\n")
    for q in mq:
        lines.append(f"- `@media {q.strip()}`")

    return "\n".join(lines)


# ─── Sección: JavaScript ──────────────────────────────────────────────────────

def seccion_js():
    lines = ["---", "## 4. Análisis del JavaScript\n"]
    html_path = ROOT / "index.html"
    if not html_path.exists():
        return "\n".join(lines + ["_No se encontró index.html._"])

    content = html_path.read_text(encoding="utf-8", errors="ignore")
    script_blocks = re.findall(r'<script(?![^>]*src)[^>]*>(.*?)</script>', content, re.DOTALL | re.IGNORECASE)
    js = "\n".join(script_blocks)

    lines.append(f"- **JS embebido:** {len(js):,} caracteres · {len(js.splitlines()):,} líneas\n")

    # Funciones
    funcs = re.findall(r'(?:function\s+([\w$]+)|(?:const|let|var)\s+([\w$]+)\s*=\s*(?:async\s+)?(?:function|\())', js)
    func_names = sorted(set(f[0] or f[1] for f in funcs if (f[0] or f[1])))
    lines.append(f"### Funciones declaradas ({len(func_names)})\n")
    for f in func_names:
        lines.append(f"- `{f}()`")

    # Variables globales (const/let/var en nivel raíz)
    globals_ = re.findall(r'^(?:const|let|var)\s+([\w$]+)', js, re.MULTILINE)
    lines.append(f"\n### Variables globales ({len(set(globals_))})\n")
    for g in sorted(set(globals_)):
        lines.append(f"- `{g}`")

    # Eventos
    events = re.findall(r'addEventListener\s*\(\s*["\'](\w+)["\']', js)
    lines.append(f"\n### Event listeners ({len(events)})\n")
    for e in sorted(set(events)):
        count = events.count(e)
        lines.append(f"- `{e}` × {count}")

    # Fetch / URLs de datos
    fetches = re.findall(r'fetch\s*\(\s*[`"\']([^`"\']+)[`"\']', js)
    lines.append(f"\n### fetch() detectados ({len(fetches)})\n")
    for f in fetches:
        lines.append(f"- `{f}`")

    # Librerías usadas (referencias)
    libs = []
    if "maplibregl" in js.lower() or "maplibre" in js.lower():
        libs.append("MapLibre GL")
    if "chart" in js.lower():
        libs.append("Chart.js")
    if "geojson" in js.lower():
        libs.append("GeoJSON")
    lines.append(f"\n### Librerías referenciadas\n")
    for l in libs:
        lines.append(f"- {l}")

    return "\n".join(lines)


# ─── Sección: Datos JSON ──────────────────────────────────────────────────────

def seccion_json():
    lines = ["---", "## 5. Análisis de Datos JSON (2012–2026)\n"]
    json_files = sorted(ROOT.glob("datos_*.json"))

    if not json_files:
        return "\n".join(lines + ["_No se encontraron archivos JSON._"])

    lines.append(f"**Archivos encontrados:** {len(json_files)}\n")

    all_stats = []
    localidades_set = set()
    grupos_set = set()
    campos_set = set()
    total_predios_por_año = {}
    avaluo_total_por_año = {}

    for jf in json_files:
        year = re.search(r'(\d{4})', jf.name)
        year = int(year.group(1)) if year else 0
        try:
            data = json.loads(jf.read_text(encoding="utf-8"))
        except Exception:
            continue

        if not isinstance(data, list) or not data:
            continue

        campos_set.update(data[0].keys())

        # Detectar columnas dinámicas del año
        yy = str(year)[2:]
        predios_col = f"PREDIOS_{yy}"
        avaluo_col = f"VALOR_AVALUO_{yy}"

        total_predios = 0
        total_avaluo = 0
        locs_año = set()
        grupos_año = set()

        for rec in data:
            loc = rec.get("NOMBRE_LOCALIDAD", "?")
            grupo = rec.get("GRUPO_ECONOMICO", "?")
            locs_año.add(loc)
            grupos_año.add(grupo)
            localidades_set.add(loc)
            grupos_set.add(grupo)
            try:
                total_predios += float(rec.get(predios_col, 0) or 0)
                total_avaluo += float(rec.get(avaluo_col, 0) or 0)
            except Exception:
                pass

        total_predios_por_año[year] = int(total_predios)
        avaluo_total_por_año[year] = total_avaluo
        all_stats.append({
            "año": year,
            "registros": len(data),
            "localidades": len(locs_año),
            "grupos": len(grupos_año),
            "predios": int(total_predios),
            "avaluo_B": total_avaluo / 1e9,
            "size": human_size(file_size(jf)),
        })

    # Tabla resumen
    lines.append("### Resumen por año\n")
    lines.append("| Año | Registros | Localidades | Grupos | Predios | Avalúo (miles MM COP) | Tamaño |")
    lines.append("|-----|-----------|-------------|--------|---------|----------------------|--------|")
    for s in all_stats:
        avaluo_str = f"{s['avaluo_B']:,.1f}" if s['avaluo_B'] > 0 else "N/D"
        predios_str = f"{s['predios']:,}" if s['predios'] > 0 else "N/D"
        lines.append(f"| {s['año']} | {s['registros']:,} | {s['localidades']} | {s['grupos']} | {predios_str} | {avaluo_str} | {s['size']} |")

    # Localidades
    lines.append(f"\n### Localidades detectadas ({len(localidades_set)})\n")
    for loc in sorted(localidades_set):
        lines.append(f"- {loc.title()}")

    # Grupos económicos
    lines.append(f"\n### Grupos económicos / usos del suelo ({len(grupos_set)})\n")
    for g in sorted(grupos_set):
        lines.append(f"- {g.title()}")

    # Campos JSON
    lines.append(f"\n### Campos en los registros ({len(campos_set)})\n")
    for c in sorted(campos_set):
        lines.append(f"- `{c}`")

    return "\n".join(lines)


# ─── Sección: Imágenes y media ────────────────────────────────────────────────

def seccion_media():
    lines = ["---", "## 6. Archivos de Imagen y Media\n"]

    # Frames de animación
    frames = sorted(ROOT.glob("animacion-campin_*.jpeg"))
    if frames:
        total_frames_size = sum(file_size(f) for f in frames)
        sizes = [file_size(f) for f in frames]
        lines.append(f"### Animación de introducción\n")
        lines.append(f"- **Frames:** {len(frames)} archivos JPEG")
        lines.append(f"- **Patrón:** `animacion-campin_000.jpeg` → `animacion-campin_{len(frames)-1:03d}.jpeg`")
        lines.append(f"- **Tamaño total:** {human_size(total_frames_size)}")
        lines.append(f"- **Tamaño promedio por frame:** {human_size(sum(sizes) / len(sizes))}")
        lines.append(f"- **Frame más pequeño:** {human_size(min(sizes))} (`{frames[sizes.index(min(sizes))].name}`)")
        lines.append(f"- **Frame más grande:** {human_size(max(sizes))} (`{frames[sizes.index(max(sizes))].name}`)")
        lines.append(f"- **Velocidad de reproducción:** ~34ms/frame → {1000/34:.0f} fps")
        lines.append(f"- **Duración estimada:** ~{len(frames)*34/1000:.1f} segundos\n")

    # Imágenes de localidades
    loc_imgs = list((ROOT / "Localidades").glob("*")) if (ROOT / "Localidades").exists() else []
    img_exts = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg"}
    imgs = [f for f in loc_imgs if f.suffix.lower() in img_exts]

    if imgs:
        lines.append("### Imágenes de localidades\n")
        lines.append("| Archivo | Tamaño | Formato |")
        lines.append("|---------|--------|---------|")
        for img in sorted(imgs, key=lambda x: x.name.lower()):
            lines.append(f"| `{img.name}` | {human_size(file_size(img))} | `{img.suffix.upper()}` |")
        total_img = sum(file_size(f) for f in imgs)
        lines.append(f"\n**Total imágenes localidades:** {len(imgs)} archivos · {human_size(total_img)}")

    # Otros archivos en Localidades
    otros = [f for f in loc_imgs if f.suffix.lower() not in img_exts and f.is_file()]
    if otros:
        lines.append("\n### Otros archivos en /Localidades/\n")
        for o in otros:
            lines.append(f"- `{o.name}` ({human_size(file_size(o))})")

    return "\n".join(lines)


# ─── Sección: Git ─────────────────────────────────────────────────────────────

def seccion_git():
    lines = ["---", "## 7. Historial Git\n"]

    branch = run("git rev-parse --abbrev-ref HEAD")
    lines.append(f"- **Rama activa:** `{branch}`")

    remote = run("git remote get-url origin")
    if remote:
        lines.append(f"- **Remoto:** `{remote}`")

    first_commit_date = run("git log --reverse --format=%ci | head -1")
    last_commit_date = run("git log -1 --format=%ci")
    total_commits = run("git rev-list --count HEAD")
    authors = run("git log --format='%an' | sort | uniq -c | sort -rn")

    lines.append(f"- **Total commits:** {total_commits}")
    lines.append(f"- **Primer commit:** {first_commit_date[:10] if first_commit_date else 'N/D'}")
    lines.append(f"- **Último commit:** {last_commit_date[:10] if last_commit_date else 'N/D'}\n")

    if authors:
        lines.append("### Autores\n")
        for line in authors.splitlines()[:10]:
            lines.append(f"- {line.strip()}")

    log = run("git log --oneline -20")
    if log:
        lines.append("\n### Últimos 20 commits\n")
        lines.append("```")
        lines.append(log)
        lines.append("```")

    diff_stat = run("git diff --stat HEAD~1 HEAD")
    if diff_stat:
        lines.append("\n### Cambios en el último commit\n")
        lines.append("```")
        lines.append(diff_stat)
        lines.append("```")

    return "\n".join(lines)


# ─── Sección: Resumen ejecutivo ───────────────────────────────────────────────

def seccion_resumen():
    lines = ["---", "## 8. Resumen Ejecutivo\n"]
    lines.append("""
**Bogotá Estilo Estocolmo** es una visualización de datos inmobiliarios interactiva
del catastro de Bogotá D.C. (2012–2026), desarrollada como una aplicación web
de una sola página (SPA) sin frameworks externos más allá de librerías de visualización.

### Stack tecnológico

| Componente | Tecnología |
|------------|------------|
| Mapas interactivos | MapLibre GL v3.6.2 |
| Gráficos estadísticos | Chart.js v4.4.0 |
| Tipografías | Google Fonts (Ramaraja, Roboto) |
| Basemaps | CartoDB Positron (claro / oscuro) |
| Datos | JSON local (15 archivos, 2012–2026) |
| Lenguaje | HTML5 + CSS3 + Vanilla JavaScript |

### Características principales

- **Storytelling interactivo:** 10 estados narrativos con navegación paso a paso
- **Animación cinematográfica:** 148 frames JPEG (~5 seg) de introducción
- **Análisis por localidad:** 20 localidades de Bogotá con datos catastrales detallados
- **Multi-año:** Serie temporal de 15 años (2012–2026)
- **Temas:** Modo oscuro / claro con transición CSS
- **Métricas:** Predios, avalúo catastral, área construida, uso del suelo
- **Geolocalización:** Coordenadas y marcadores para cada localidad
- **Clustering:** Agrupación de predios por zoom y estrato socioeconómico

### Volumen de datos

- **Registros totales:** ~15 archivos JSON con datos catastrales anuales
- **Grupos económicos:** Usos del suelo clasificados (residencial, comercial, industrial, dotacional)
- **Cobertura:** 20 localidades urbanas de Bogotá D.C.

### Arquitectura de carga

```
DOMContentLoaded
├── initIntroAnimation()    → 148 frames JPEG precargados
├── initMap()               → MapLibre GL + CartoDB
│   └── setupClusterLayers() → GeoJSON clusters por estrato
├── renderChart('historico') → Chart.js inicial
├── Event listeners         → Interactividad
└── loadAllData()           → 15 × fetch(datos_YYYY.json) async
```
""")
    return "\n".join(lines)


# ─── Main ──────────────────────────────────────────────────────────────────────

def main():
    print("Generando informe...")
    secciones = [
        seccion_metadatos,
        seccion_estructura,
        seccion_html,
        seccion_css,
        seccion_js,
        seccion_json,
        seccion_media,
        seccion_git,
        seccion_resumen,
    ]

    partes = []
    for i, fn in enumerate(secciones, 1):
        print(f"  [{i}/{len(secciones)}] {fn.__name__}...")
        try:
            partes.append(fn())
        except Exception as e:
            partes.append(f"_Error en {fn.__name__}: {e}_")

    contenido = "\n\n".join(partes) + "\n\n---\n_Informe generado automáticamente por generar_informe.py_\n"
    REPORT_PATH.write_text(contenido, encoding="utf-8")
    print(f"\nInforme guardado en: {REPORT_PATH.name}")
    print(f"Tamaño: {human_size(file_size(REPORT_PATH))}")


if __name__ == "__main__":
    import sys
    os.sys = sys
    main()
