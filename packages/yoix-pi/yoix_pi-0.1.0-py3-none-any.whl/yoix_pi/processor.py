"""Core functionality for processing BBEdit-style includes."""

import os
import re
from pathlib import Path


class IncludeProcessor:
    """Process BBEdit-style includes in HTML files."""

    def __init__(self, config):
        """Initialize with configuration dictionary containing paths.
        
        Args:
            config (dict): Configuration with keys:
                - partials_dir: Path to partials directory
                - public_dir: Path to public directory
        """
        self.partials_dir = Path(config.get('partials_dir', 'includes/partials'))
        self.public_dir = Path(config.get('public_dir', 'public'))

    def read_partial(self, partial_name):
        """Read the content of a partial file from the configured partials directory.
        
        Args:
            partial_name (str): Name of the partial file to read
            
        Returns:
            str: Content of the partial file or empty string if not found
        """
        partial_path = self.partials_dir / partial_name
        try:
            with open(partial_path, 'r', encoding='utf-8') as f:
                return f.read().strip()
        except FileNotFoundError:
            print(f"Warning: Partial file '{partial_name}' not found at {partial_path}")
            return ''

    def parse_variables(self, include_directive):
        """Parse variables from the BBEdit include directive.
        
        Args:
            include_directive (str): The BBEdit include directive containing variables
            
        Returns:
            dict: Dictionary of variable names to values
        """
        variables = {}
        # Match variable assignments in the format #VAR# = "value"
        var_pattern = r'#([^#]+)#\s*=\s*"([^"]*)"'
        matches = re.finditer(var_pattern, include_directive)
        for match in matches:
            var_name, var_value = match.groups()
            variables[f'#{var_name}#'] = var_value
        return variables

    def process_includes(self, content):
        """Process BBEdit includes in the content.
        
        Args:
            content (str): Content containing BBEdit includes to process
            
        Returns:
            str: Processed content with includes resolved
        """
        # Updated pattern to match BBEdit includes with optional variables
        pattern = r'(<!--\s*#bbinclude\s*"([^"]+)"([^>]*?)-->)(.*?)(<!--\s*end bbinclude\s*-->)'
        
        def replace_include(match):
            try:
                full_match, partial_name, vars_section, between_content, end_directive = match.groups()
                # Read the partial content
                partial_content = self.read_partial(partial_name)
                
                # Parse and apply variables if present
                if vars_section.strip():
                    variables = self.parse_variables(vars_section)
                    # Replace each variable in the partial content
                    for var_name, var_value in variables.items():
                        partial_content = partial_content.replace(var_name, var_value)
                
                # Extract the indentation from the include directive
                indent = ''
                lines = full_match.split('\n')
                if len(lines) > 0:
                    indent = re.match(r'^\s*', lines[0]).group()
                
                # Apply indentation to the partial content
                indented_content = '\n'.join(indent + line if line else line 
                                           for line in partial_content.split('\n'))
                
                # Return the processed content with preserved comments
                return f'{indent}<!-- #bbinclude "{partial_name}"{vars_section} -->\n{indented_content}\n{indent}<!-- end bbinclude -->'
            except Exception as e:
                print(f"Error processing include: {e}")
                print(f"Match groups: {match.groups()}")
                return match.group(0)  # Return original content if there's an error
        
        # Replace all includes in the content
        return re.sub(pattern, replace_include, content, flags=re.DOTALL)

    def process_file(self, file_path):
        """Process a single file for BBEdit includes.
        
        Args:
            file_path (Path): Path to the file to process
        """
        print(f"Processing {file_path}")
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            processed_content = self.process_includes(content)
            
            if processed_content != content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(processed_content)
                print(f"Updated {file_path}")
        except Exception as e:
            print(f"Error processing {file_path}: {e}")

    def process_all_files(self):
        """Process all HTML files in the public directory."""
        # Walk through all files in public directory
        for root, _, files in os.walk(self.public_dir):
            for file in files:
                if file.endswith(('.html', '.htm')):  # Process only HTML files
                    file_path = Path(root) / file
                    self.process_file(file_path)


def process_persistent_includes(config=None):
    """Process BBEdit-style includes in HTML files.
    
    Args:
        config (dict, optional): Configuration with keys:
            - partials_dir: Path to partials directory (default: 'includes/partials')
            - public_dir: Path to public directory (default: 'public')
    """
    if config is None:
        config = {
            'partials_dir': 'includes/partials',
            'public_dir': 'public'
        }
    
    processor = IncludeProcessor(config)
    processor.process_all_files()
