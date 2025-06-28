
import re
import os

INCLUDE_PATTERN = re.compile(r"\(!(.+?)(?:\s+(.+?))?!\)")

INPUT_DIR = "docs/pages"
OUTPUT_DIR = "docs/pages_fixed"

def parse_attributes(attr_str: str) -> dict:
    """Parse key="value" attributes from the include directive."""
    if not attr_str:
        return {}
    return dict(re.findall(r'(\w+)\s*=\s*"([^"]+)"', attr_str))

def resolve_includes_in_text(text: str, base_dir: str, visited: set) -> str:
    """Resolve all include directives in a text block recursively."""
    def replacer(match):
        rel_path, attr_str = match.groups()
        rel_path = rel_path.strip()
        rel_path = rel_path.lstrip("/")
        rel_path = os.path.normpath(rel_path)
        if rel_path.startswith("examples/"):
            rel_path = os.path.join("docs", rel_path)

        full_path = os.path.join(base_dir, rel_path)

        if full_path in visited:
            return f"<!-- skipping recursive loop: {rel_path} -->"

        if not os.path.isfile(full_path):
            print(f"warning: include not found: {full_path}")
            return f"<!-- include not found: {rel_path} -->"

        attrs = parse_attributes(attr_str)
        visited.add(full_path)

        with open(full_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Recursively resolve nested includes
        content = resolve_includes_in_text(content, base_dir, visited)

        # Apply simple {{key}} replacement
        for key, val in attrs.items():
            content = content.replace(f"{{{{{key}}}}}", val)

        return f"<!-- start include: {rel_path} -->\n{content}\n<!-- end include -->"

    return INCLUDE_PATTERN.sub(replacer, text)

def preprocess_all_mdx(input_dir: str, output_dir: str, base_dir: str):
    os.makedirs(output_dir, exist_ok=True)

    for root, _, files in os.walk(input_dir):
        for file in files:
            if not file.endswith(".mdx"):
                continue

            in_path = os.path.join(root, file)

            # Skip any file inside an 'includes' folder
            if "/includes/" in in_path.replace("\\", "/"):
                continue

            # Preserve relative structure
            rel_path = os.path.relpath(in_path, input_dir)
            out_path = os.path.join(output_dir, rel_path)
            os.makedirs(os.path.dirname(out_path), exist_ok=True)

            with open(in_path, "r", encoding="utf-8") as f:
                raw = f.read()

            print(f"📄 Processing: {rel_path}")
            resolved = resolve_includes_in_text(raw, base_dir, visited=set())

            with open(out_path, "w", encoding="utf-8") as f:
                f.write(resolved)

BASE_DIR = "./"
INPUT_DIR = "docs/pages"
OUTPUT_DIR = "docs/pages_fixed"
preprocess_all_mdx(input_dir=INPUT_DIR, output_dir=OUTPUT_DIR, base_dir=BASE_DIR)
