import sys

with open("iniciarVentaW.py", "r", encoding="utf-8") as f:
    content = f.read()

# The broken string pattern
broken = '"El período de uso de este sistema ha finalizado.\n"'
fixed = '"El período de uso de este sistema ha finalizado.\n"'

# Also check if it split across lines
broken_multiline = '"El período de uso de este sistema ha finalizado.\n'

if broken_multiline in content:
    # We found the newline inside the string
    # We need to replace the newline with literal \n and close quote if missing
    # But looking at tail output:
    # "El período ... finalizado.
    # "
    # The next line starts with "

    # We can search for the whole block
    search_block = '                "El período de uso de este sistema ha finalizado.\n"\n'
    replace_block = '                "El período de uso de este sistema ha finalizado.\n"\n'

    if search_block in content:
        content = content.replace(search_block, replace_block)
        print("Fixed by block replacement")
    else:
        # Fallback: strict replace
        # The tail output showed:
        # "El período de uso de este sistema ha finalizado.
        # "
        # It seems there is a " at the beginning of next line?
        # Let's just use regex or simple replace of the specific broken line.
        lines = content.splitlines(keepends=True)
        for i, line in enumerate(lines):
            if "El período de uso de este sistema ha finalizado." in line:
                # Check if it has a newline at the end instead of \n"
                if line.strip() == '"El período de uso de este sistema ha finalizado.':
                     lines[i] = '                "El período de uso de este sistema ha finalizado.\n"\n'
                     # Check if next line is just a quote or garbage
                     if i+1 < len(lines) and lines[i+1].strip() == '"':
                         lines[i+1] = '' # Remove standalone quote line if it exists
        content = "".join(lines)
        print("Fixed by line iteration")

with open("iniciarVentaW.py", "w", encoding="utf-8") as f:
    f.write(content)
