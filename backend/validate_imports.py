"""
Validate that all Python model files have proper imports.
Run this before committing to catch missing imports early.
"""
import ast
import sys
from pathlib import Path

def check_file(filepath):
    """Check if a Python file has proper imports for SQLAlchemy models"""
    with open(filepath, 'r', encoding='utf-8') as f:
        try:
            content = f.read()
            tree = ast.parse(content)
        except SyntaxError as e:
            return [f"⚠️  {filepath}: Syntax error - {e}"]
    
    has_base = False
    has_column = False
    uses_base = False
    uses_column = False
    
    for node in ast.walk(tree):
        # Check for imports
        if isinstance(node, ast.ImportFrom):
            if node.module == 'database':
                for alias in node.names:
                    if alias.name == 'Base':
                        has_base = True
            elif node.module == 'sqlalchemy':
                for alias in node.names:
                    if alias.name == 'Column':
                        has_column = True
        
        # Check for usage in class definition
        if isinstance(node, ast.ClassDef):
            for base in node.bases:
                if isinstance(base, ast.Name) and base.id == 'Base':
                    uses_base = True
            
            # Check for Column usage in class body
            for item in node.body:
                if isinstance(item, ast.Assign):
                    for target in item.targets:
                        if isinstance(item.value, ast.Call):
                            if isinstance(item.value.func, ast.Name) and item.value.func.id == 'Column':
                                uses_column = True
    
    errors = []
    if uses_base and not has_base:
        errors.append(f"❌ {filepath}: Uses Base but doesn't import it from database")
    if uses_column and not has_column:
        errors.append(f"❌ {filepath}: Uses Column but doesn't import it from sqlalchemy")
    
    return errors

def main():
    backend_dir = Path(__file__).parent
    errors = []
    checked_files = 0
    
    print('🔍 Validating Python imports in backend...\n')
    
    for py_file in backend_dir.rglob('*.py'):
        # Skip virtual environments and cache
        if any(skip in str(py_file) for skip in ['venv', '__pycache__', 'migrations', '.pytest_cache']):
            continue
        
        checked_files += 1
        file_errors = check_file(py_file)
        errors.extend(file_errors)
    
    print(f'Checked {checked_files} Python files\n')
    
    if errors:
        print('\n'.join(errors))
        print('\n❌ Found import issues! Please add missing imports.')
        sys.exit(1)
    else:
        print('✅ All model files have proper imports!')

if __name__ == '__main__':
    main()
