import os
import argparse

# CLI Logic
def main():
    parser = argparse.ArgumentParser(description='Structify - Generate project structures easily.')
    parser.add_argument('command', choices=['init', 'generate', 'preview'], help='Command to execute')
    
    args = parser.parse_args()
    if args.command == 'init':
        interactive_setup()
    elif args.command == 'generate':
        generate_structure()
    elif args.command == 'preview':
        preview_structure()

# Interactive Setup
def interactive_setup():
    project_name = input('Enter project name: ')
    structure = get_user_defined_structure()
    generate_structure(project_name, structure)
    print(f'Project "{project_name}" created successfully.')

# Get user-defined structure
def get_user_defined_structure():
    structure = {}
    print("Enter files and folders (use '/' for folders, ';' for root files, and '?' to nest inside last folder):")
    print("Example: app.py; templates?index.html; static/style.css")
    user_input = input('Structure: ')
    elements = user_input.split(';')
    
    for element in elements:
        element = element.strip()
        if '/' in element:
            folders = element.split('/')
            folder = folders[0]
            file = '/'.join(folders[1:])
            structure.setdefault(folder, []).append(file)
        elif '?' in element:
            folder, file = element.split('?')
            structure.setdefault(folder, []).append(file)
        else:
            structure.setdefault('', []).append(element)
    
    return structure

# Structure Generator
def generate_structure(project_name=None, structure=None):
    if not project_name:
        project_name = os.getcwd()
    if not structure:
        structure = parse_structure_file()
    
    for folder, files in structure.items():
        folder_path = os.path.join(project_name, folder) if folder else project_name
        os.makedirs(folder_path, exist_ok=True)
        for file in files:
            file_path = os.path.join(folder_path, file)
            open(file_path, 'w').close()

# Preview Structure
def preview_structure():
    structure = parse_structure_file()
    print('Project Structure Preview:')
    for folder, files in structure.items():
        print(f'{folder}/' if folder else '.')
        for file in files:
            print(f'  ├── {file}')

# Parse structure.bash/.txt
def parse_structure_file():
    structure = {}
    for filename in ['structure.bash', 'structure.sh', 'structure.txt']:
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                lines = f.readlines()
            current_folder = ''
            for line in lines:
                line = line.strip()
                if line.endswith('/'):
                    current_folder = line.rstrip('/')
                    structure[current_folder] = []
                else:
                    structure.setdefault(current_folder, []).append(line)
            return structure
    return {'': ['app.py']}  # Default structure

if __name__ == '__main__':
    main()
