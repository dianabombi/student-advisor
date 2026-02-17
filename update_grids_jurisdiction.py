#!/usr/bin/env python3
"""
Add jurisdiction filtering to all grid components
"""

import os
import re

components = [
    'LanguageSchoolsGrid.tsx',
    'VocationalSchoolsGrid.tsx',
    'ConservatoriesGrid.tsx',
    'FoundationProgramsGrid.tsx'
]

base_path = 'C:/Users/info/OneDrive/Dokumenty/Student/frontend/components'

for component in components:
    file_path = f'{base_path}/{component}'
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Add jurisdiction import if not present
        if 'useJurisdiction' not in content:
            content = content.replace(
                "import { useLanguage } from '@/lib/LanguageContext';",
                "import { useLanguage } from '@/lib/LanguageContext';\nimport { useJurisdiction } from '@/contexts/JurisdictionContext';"
            )
        
        # Add jurisdiction hook
        if 'const { jurisdiction }' not in content:
            content = content.replace(
                "const { language, t } = useLanguage();",
                "const { language, t } = useLanguage();\n    const { jurisdiction } = useJurisdiction();"
            )
        
        # Update fetch URL to include jurisdiction
        content = re.sub(
            r"fetch\('http://localhost:8002/api/universities\?type=([^']+)'\)",
            r"fetch(`http://localhost:8002/api/universities?jurisdiction_code=${jurisdiction}&type=\1`)",
            content
        )
        
        # Update useEffect dependency
        content = content.replace('}, []);', '}, [jurisdiction]);')
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f'[OK] Updated {component}')
        
    except Exception as e:
        print(f'[ERROR] {component}: {e}')

print('\n[SUCCESS] All grid components updated with jurisdiction filtering!')
