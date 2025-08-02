import os
from journal_entry.log_structure_read import log_structure_event

def map_self(root_dir="../../"):  # from introspection to src
    for folder, subfolders, files in os.walk(root_dir):
        depth = folder.replace(root_dir, '').count(os.sep)
        indent = '    ' * depth
        print(f"{indent}{os.path.basename(folder)}/")
        for f in files:
            print(f"{indent}    {f}")
    
    log_structure_event()  # Log only after successful reflection

if __name__ == "__main__":
    map_self()