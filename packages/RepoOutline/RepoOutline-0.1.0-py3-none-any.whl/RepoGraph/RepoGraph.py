import os
import re

class RepoGraph:
  def __init__(self, folder_path, file_patterns):
    """
    Initialize the RepoGraph object with the folder path and file patterns.

    Args:
        folder_path (str): The path to the folder to scan.
        file_patterns (list): A list of regex patterns to match file names.
    """
    self.folder_path = folder_path
    self.file_patterns = file_patterns

  def _find_files(self):
    """
    Recursively find all files whose name matches the defined regex pattern in the path.

    Returns:
        list: A list of strings that match the pattern.
    """
    file_paths = []
    for root, _, files in os.walk(self.folder_path):
      for file in files:
        if any([re.search(p, file) for p in self.file_patterns]):
          rel_path = os.path.relpath(os.path.join(root, file), self.folder_path)
          file_paths.append(rel_path)
    
    return sorted(file_paths)

  def _generate_folder_graph(self, file_paths):
    """
    Generate a hierarchical tree representation for all file paths.

    Args:
        file_paths (list): A list of file paths.

    Returns:
        dict: A nested dictionary representing the folder structure.
    """
    tree = {}
    for path in file_paths:
      parts = path.split(os.sep)
      node = tree
      for part in parts:
        if part not in node:
          node[part] = {}
        node = node[part]
    return tree

  def _format_text(self, txt):
    """
    Format the text to be used as a key in the tree.

    Args:
        txt (str): The text to format.

    Returns:
        str: The formatted text.
    """
    return re.sub(r"[^a-zA-Z0-9]", " ", txt).title()
  
  def _render_markdown(self, tree, parent_path=""): 
    """
    Render the tree into a markdown list with links.

    Args:
        tree (dict): The hierarchical tree representation of the folder structure.
        parent_path (str): The parent path for the current level of the tree.

    Returns:
        str: The markdown representation of the tree.
    """
    md = ""
    for key, sub_tree in tree.items():
      file_path = os.path.join(parent_path, key)
      key_name = self._format_text(key)
      indent = "  " * file_path.count(os.sep)
      if isinstance(sub_tree, dict) and any([re.search(p, t) for p in self.file_patterns for t in sub_tree]):
        file = f"[{key_name}]({file_path})"
      else:
        file = f"{key_name}"
      md += f"{indent}- {file}\n"
      md += self._render_markdown(sub_tree, file_path)
    return md

  def get_graph(self):
    """
    Main function to generate a markdown representation of the folder structure.

    Returns:
        str: The markdown representation of the folder structure.
    """
    readme_paths = self._find_files()
    tree = self._generate_folder_graph(readme_paths)
    return self._render_markdown(tree, self.folder_path)

def main():
  # Default values
  default_repo_path = os.path.abspath(os.getcwd())
  default_patterns = ['README.md']
  default_output_path = os.path.join(default_repo_path, "README.md")

  # Get user input
  repo_path = input(f"Enter the repository path (default: {default_repo_path}): ") or default_repo_path
  print(f"Enter the file patterns separated by new lines (default: {default_patterns}): ")
  patterns_input = []
  while True:
    line = input()
    if line:
      patterns_input.append(line.strip())
    else:
      break
  output_path = input(f"Enter the output markdown file path (default: {default_output_path}): ") or default_output_path

  # Process patterns input
  patterns = patterns_input if patterns_input else default_patterns
  
  # Generate the markdown representation
  mdGraph = RepoGraph(repo_path, patterns).get_graph()

  # Save the markdown to the specified file
  with open(output_path, 'w') as f:
    f.write(mdGraph)

  print(f"Markdown representation saved to {output_path}")

if __name__ == "__main__":
  main()
  