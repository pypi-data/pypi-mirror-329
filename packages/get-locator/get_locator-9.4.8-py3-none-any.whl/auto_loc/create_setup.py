import argparse
import os

def get_project_root(auto_loc_path):
    project_root = auto_loc_path
    while not auto_loc_path.endswith("venv"):
        project_root = os.path.dirname(project_root)
        if project_root.endswith("venv"):
            project_root = os.path.dirname(project_root)
            break
    return project_root

def create_setup(project_root, lib_root):
    # Read text from the source .txt file
    with open(os.path.join(lib_root, "run_text.txt"), "r") as txt_file:
        content = txt_file.read()

    # Path to the check.py file
    check_py_path = os.path.join(project_root, "web_inspector.py")

    # Check if the check.py file exists and is not empty
    if not os.path.exists(check_py_path) or os.path.getsize(check_py_path) == 0:
        # Create the .py file in the project root
        with open(check_py_path, "w") as py_file:
            py_file.write(content)

        # Add check.py to .gitignore
        gitignore_path = os.path.join(project_root, ".gitignore")
        with open(gitignore_path, "a") as gitignore_file:
            gitignore_file.write("\nweb_inspector.py\n")


def main():
    # Define the root directory of the project
    lib_root = os.path.dirname(os.path.abspath(__file__))
    project_root = get_project_root(lib_root)
    parser = argparse.ArgumentParser(description="Run Web Inspector locally")
    parser.add_argument('--run', action='store_true', help="run inspector")
    args = parser.parse_args()
    if args.run:
        create_setup(project_root, lib_root)


if __name__ == '__main__':
    # e.g.: create-setup --run
    main()
