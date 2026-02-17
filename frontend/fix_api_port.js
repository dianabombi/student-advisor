const fs = require('fs');
const path = require('path');

// Recursively find all .tsx and .ts files
function findFiles(dir, fileList = []) {
    const files = fs.readdirSync(dir);

    files.forEach(file => {
        const filePath = path.join(dir, file);
        const stat = fs.statSync(filePath);

        if (stat.isDirectory()) {
            // Skip node_modules and .next directories
            if (file !== 'node_modules' && file !== '.next' && file !== '.git') {
                findFiles(filePath, fileList);
            }
        } else if (file.endsWith('.tsx') || file.endsWith('.ts') || file.endsWith('.js')) {
            fileList.push(filePath);
        }
    });

    return fileList;
}

// Replace localhost:8002 with localhost:8002
function replaceInFile(filePath) {
    try {
        let content = fs.readFileSync(filePath, 'utf8');
        const originalContent = content;

        // Replace all occurrences of localhost:8002 with localhost:8002
        content = content.replace(/localhost:8002/g, 'localhost:8002');

        // Only write if content changed
        if (content !== originalContent) {
            fs.writeFileSync(filePath, content, 'utf8');
            console.log(`✅ Updated: ${path.relative(process.cwd(), filePath)}`);
            return true;
        }
        return false;
    } catch (error) {
        console.error(`❌ Error processing ${filePath}:`, error.message);
        return false;
    }
}

// Main execution
const frontendDir = path.join(__dirname);
console.log(`🔍 Searching for files in: ${frontendDir}\n`);

const files = findFiles(frontendDir);
console.log(`📁 Found ${files.length} TypeScript/JavaScript files\n`);

let updatedCount = 0;
files.forEach(file => {
    if (replaceInFile(file)) {
        updatedCount++;
    }
});

console.log(`\n✨ Done! Updated ${updatedCount} files`);
console.log(`🎯 Changed all localhost:8002 → localhost:8002`);
