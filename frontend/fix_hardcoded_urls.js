const fs = require('fs');
const path = require('path');

const frontendDir = path.join(__dirname);

// Files to update
const filesToUpdate = [
    'components/VocationalSchoolsGrid.tsx',
    'components/UsageIndicator.tsx',
    'hooks/useDocumentProgress.ts',
    'components/UniversitiesGrid.tsx',
    'components/TemplateManagement.tsx',
    'components/LanguageSchoolsGrid.tsx',
    'components/FoundationProgramsGrid.tsx',
    'components/DocumentUpload.tsx',
    'components/ConservatoriesGrid.tsx',
    'components/ChatWidget.tsx',
    'components/ChatInterface.tsx',
    'components/AIChatWidget.tsx',
    'components/AISupportButton.tsx',
    'lib/api.ts',
    'app/register/page.tsx',
    'components/admin/UserDetailsModal.tsx',
    'app/login/page.tsx',
    'app/lawyer/cases/page.tsx',
    'app/dashboard/upload/page.tsx',
    'app/dashboard/chat/page.tsx',
    'app/chat/page.tsx',
    'app/cases/[id]/page.tsx',
    'app/cases/page.tsx',
    'app/cases/new/page.tsx',
    'app/auth/login/page_old.tsx',
    'app/auth/register/page.tsx',
    'components/admin/ActivityFeed.tsx',
    'app/admin/users/page.tsx',
    'app/admin/universities/page.tsx',
    'app/admin/templates/page.tsx',
    'app/admin/settings/page.tsx'
];

console.log('🔄 Replacing hardcoded http://localhost:8002 with /api...\n');

let totalReplacements = 0;

filesToUpdate.forEach(file => {
    const filePath = path.join(frontendDir, file);

    if (fs.existsSync(filePath)) {
        let content = fs.readFileSync(filePath, 'utf8');
        const original = content;

        // Replace http://localhost:8002/api with /api
        content = content.replace(/http:\/\/localhost:8002\/api/g, '/api');

        // Also replace process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8002' with just process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
        content = content.replace(/process\.env\.NEXT_PUBLIC_API_URL \|\| 'http:\/\/localhost:8002'/g, "process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'");

        if (content !== original) {
            fs.writeFileSync(filePath, content, 'utf8');
            const count = (original.match(/http:\/\/localhost:8002/g) || []).length;
            totalReplacements += count;
            console.log(`✅ Updated ${file} (${count} replacements)`);
        }
    } else {
        console.log(`⚠️  File not found: ${file}`);
    }
});

// Also update lib/api.ts default
const apiFile = path.join(frontendDir, 'lib/api.ts');
if (fs.existsSync(apiFile)) {
    let content = fs.readFileSync(apiFile, 'utf8');
    content = content.replace(/'http:\/\/localhost:8002'/g, "'http://localhost:8000'");
    fs.writeFileSync(apiFile, content, 'utf8');
    console.log(`✅ Updated lib/api.ts default URL`);
}

console.log(`\n🎉 Done! Made ${totalReplacements} replacements across ${filesToUpdate.length} files`);
console.log('\n⚠️  Note: Some files may still need manual review for complex URL patterns');
