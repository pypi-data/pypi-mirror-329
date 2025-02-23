"""Tests for the IncludeProcessor class."""

import os
import re
import pytest
from pathlib import Path
from yoix_pi.processor import IncludeProcessor

@pytest.fixture
def temp_dirs(tmp_path):
    """Create temporary directories for testing."""
    partials_dir = tmp_path / "includes" / "partials"
    public_dir = tmp_path / "public"
    partials_dir.mkdir(parents=True)
    public_dir.mkdir(parents=True)
    return {'partials_dir': partials_dir, 'public_dir': public_dir}

@pytest.fixture
def processor(temp_dirs):
    """Create an IncludeProcessor instance for testing."""
    return IncludeProcessor(temp_dirs)

def create_test_files(temp_dirs, partial_content, html_content):
    """Helper function to create test files."""
    partial_file = temp_dirs['partials_dir'] / "header.html"
    html_file = temp_dirs['public_dir'] / "index.html"
    
    partial_file.write_text(partial_content)
    html_file.write_text(html_content)
    
    return partial_file, html_file

def normalize_whitespace(text):
    """Helper function to normalize whitespace in text."""
    return re.sub(r'\s+', ' ', text.strip())

def test_init_with_default_paths():
    """Test initialization with default paths."""
    processor = IncludeProcessor({})
    assert processor.partials_dir == Path('includes/partials')
    assert processor.public_dir == Path('public')

def test_init_with_custom_paths(temp_dirs):
    """Test initialization with custom paths."""
    processor = IncludeProcessor(temp_dirs)
    assert processor.partials_dir == temp_dirs['partials_dir']
    assert processor.public_dir == temp_dirs['public_dir']

def test_read_partial_existing_file(processor, temp_dirs):
    """Test reading an existing partial file."""
    content = "<header>Test Header</header>"
    partial_file = temp_dirs['partials_dir'] / "header.html"
    partial_file.write_text(content)
    
    assert processor.read_partial("header.html") == content

def test_read_partial_missing_file(processor):
    """Test reading a non-existent partial file."""
    assert processor.read_partial("nonexistent.html") == ''

def test_parse_variables_empty():
    """Test parsing empty variables section."""
    processor = IncludeProcessor({})
    assert processor.parse_variables("") == {}

def test_parse_variables_single():
    """Test parsing a single variable."""
    processor = IncludeProcessor({})
    directive = '#TITLE# = "My Page"'
    expected = {'#TITLE#': 'My Page'}
    assert processor.parse_variables(directive) == expected

def test_parse_variables_multiple():
    """Test parsing multiple variables."""
    processor = IncludeProcessor({})
    directive = '#TITLE# = "My Page" #AUTHOR# = "John Doe"'
    expected = {'#TITLE#': 'My Page', '#AUTHOR#': 'John Doe'}
    assert processor.parse_variables(directive) == expected

def test_process_includes_no_includes(processor, temp_dirs):
    """Test processing content with no includes."""
    content = "<html><body>Test</body></html>"
    assert processor.process_includes(content) == content

def test_process_includes_simple(processor, temp_dirs):
    """Test processing a simple include without variables."""
    partial_content = "<header>Test Header</header>"
    html_content = '''
    <html>
    <!-- #bbinclude "header.html" -->
    <!-- end bbinclude -->
    </html>
    '''
    partial_file, html_file = create_test_files(temp_dirs, partial_content, html_content)
    
    processed = processor.process_includes(html_content)
    assert "<header>Test Header</header>" in processed
    assert normalize_whitespace('<!-- #bbinclude "header.html"') in normalize_whitespace(processed)
    assert normalize_whitespace("<!-- end bbinclude -->") in normalize_whitespace(processed)

def test_process_includes_with_variables(processor, temp_dirs):
    """Test processing an include with variables."""
    partial_content = "<title>#TITLE#</title>"
    html_content = '''
    <html>
    <!-- #bbinclude "header.html" #TITLE# = "My Page" -->
    <!-- end bbinclude -->
    </html>
    '''
    partial_file, html_file = create_test_files(temp_dirs, partial_content, html_content)
    
    processed = processor.process_includes(html_content)
    assert "<title>My Page</title>" in processed
    assert normalize_whitespace('<!-- #bbinclude "header.html" #TITLE# = "My Page"') in normalize_whitespace(processed)
    assert normalize_whitespace("<!-- end bbinclude -->") in normalize_whitespace(processed)

def test_process_file(processor, temp_dirs):
    """Test processing a complete file."""
    partial_content = "<header>#TITLE#</header>"
    html_content = '''
    <html>
    <!-- #bbinclude "header.html" #TITLE# = "My Page" -->
    <!-- end bbinclude -->
    <body>Test</body>
    </html>
    '''
    partial_file, html_file = create_test_files(temp_dirs, partial_content, html_content)
    
    processor.process_file(html_file)
    
    processed_content = html_file.read_text()
    assert "<header>My Page</header>" in processed_content
    assert "Test</body>" in processed_content

def test_process_all_files(processor, temp_dirs):
    """Test processing multiple files in the public directory."""
    # Create test files
    partial_content = "<header>#TITLE#</header>"
    html_content1 = '''<!-- #bbinclude "header.html" #TITLE# = "Page 1" --><!-- end bbinclude -->'''
    html_content2 = '''<!-- #bbinclude "header.html" #TITLE# = "Page 2" --><!-- end bbinclude -->'''
    
    partial_file = temp_dirs['partials_dir'] / "header.html"
    html_file1 = temp_dirs['public_dir'] / "page1.html"
    html_file2 = temp_dirs['public_dir'] / "page2.html"
    
    partial_file.write_text(partial_content)
    html_file1.write_text(html_content1)
    html_file2.write_text(html_content2)
    
    # Process all files
    processor.process_all_files()
    
    # Check results
    processed1 = html_file1.read_text()
    processed2 = html_file2.read_text()
    
    assert "<header>Page 1</header>" in processed1
    assert "<header>Page 2</header>" in processed2

def test_error_handling_invalid_file(processor, temp_dirs):
    """Test error handling for invalid file operations."""
    # Create a file without read permissions
    html_file = temp_dirs['public_dir'] / "no_access.html"
    html_file.write_text("test")
    os.chmod(html_file, 0o000)  # Remove all permissions
    
    # This should not raise an exception
    processor.process_file(html_file)
    
    # Restore permissions for cleanup
    os.chmod(html_file, 0o666)
