import os

# Simple detector based on file extensions found in the project directory.
EXTENSION_LANGUAGE_MAP = {
    '.py': 'python',
    '.js': 'javascript',
    '.jsx': 'javascript',
    '.ts': 'typescript',
    '.tsx': 'typescript',
    '.java': 'java',
    '.c': 'cpp',
    '.cpp': 'cpp',
    '.cc': 'cpp',
    '.h': 'cpp',
    '.hpp': 'cpp',
}


def detect_language(project_dir):
    """Scan the project directory for common source file extensions and
    return a language string. If multiple languages are found this returns
    the language with the most matches. If none found, returns 'unknown'."""
    counts = {}
    for root, dirs, files in os.walk(project_dir):
        for f in files:
            _, ext = os.path.splitext(f.lower())
            lang = EXTENSION_LANGUAGE_MAP.get(ext)
            if lang:
                counts[lang] = counts.get(lang, 0) + 1

    if not counts:
        return 'unknown'
    # return the language with the highest count
    return max(counts.items(), key=lambda x: x[1])[0]


def detect_languages(project_dir):
    """Return a list of detected languages sorted by descending file count.
    If none found, returns an empty list."""
    counts = {}
    for root, dirs, files in os.walk(project_dir):
        for f in files:
            _, ext = os.path.splitext(f.lower())
            lang = EXTENSION_LANGUAGE_MAP.get(ext)
            if lang:
                counts[lang] = counts.get(lang, 0) + 1

    if not counts:
        return []

    # sort languages by count desc
    return [lang for lang, _ in sorted(counts.items(), key=lambda x: x[1], reverse=True)]
