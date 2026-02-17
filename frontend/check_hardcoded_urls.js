const fs = require('fs');
const path = require('path');

const searchDir = path.join(__dirname);
const hardcodedUrlPattern = /http:\/\/localhost:\d+/g;
const excludeDirs = ['.next', 'node_modules', '.git'];

function checkDirectory(dir, relativePath = '') {
    const files = fs.readdirSync(dir, { withFileTypes: true });
    let found = false;

    for (const file of files) {
        const fullPath = path.join(dir, file.name);
        const relPath = path.join(relativePath, file.name);

        if (file.isDirectory()) {
            if (!file.name.startsWith('.') && !excludeDirs.includes(file.name)) {
                if (checkDirectory(fullPath, relPath)) found = true;
            }
        } else if (file.name.endsWith('.tsx') || file.name.endsWith('.ts') || file.name.endsWith('.js')) {
            const content = fs.readFileSync(fullPath, 'utf8');
            const matches = content.match(hardcodedUrlPattern);

            if (matches) {
                console.error(`❌ Found hardcoded URL in ${relPath}:`);
                matches.forEach(m => console.error(`   ${m}`));
                found = true;
            }
        }
    }

    return found;
}

console.log('🔍 Checking for hardcoded URLs in frontend...\n');
const hasIssues = checkDirectory(searchDir);

if (hasIssues) {
    console.error('\n❌ Found hardcoded URLs! Please use relative paths like /api/...');
    console.error('   Example: fetch(\'/api/universities\') instead of fetch(\'http://localhost:8002/api/universities\')');
    process.exit(1);
} else {
    console.log('✅ No hardcoded URLs found!');
}
