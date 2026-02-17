const fs = require('fs');
const path = require('path');

const localesDir = path.join(__dirname, 'locales');
const languages = ['sk', 'cs', 'pl', 'uk', 'en', 'de', 'fr', 'es', 'it', 'pt', 'ru'];

console.log('📁 Creating translation folder structure...\n');

languages.forEach(lang => {
    const langDir = path.join(localesDir, lang);
    const sourceFile = path.join(localesDir, `student_${lang}.json`);
    const targetFile = path.join(langDir, 'common.json');

    // Create language directory if it doesn't exist
    if (!fs.existsSync(langDir)) {
        fs.mkdirSync(langDir, { recursive: true });
        console.log(`✅ Created directory: ${lang}/`);
    }

    // Copy student_{lang}.json to {lang}/common.json
    if (fs.existsSync(sourceFile)) {
        fs.copyFileSync(sourceFile, targetFile);
        console.log(`📄 Copied student_${lang}.json → ${lang}/common.json`);
    } else {
        console.log(`❌ Source file not found: student_${lang}.json`);
    }
});

console.log('\n🎉 Translation folder structure created successfully!');
console.log('\nStructure:');
console.log('locales/');
languages.forEach(lang => {
    console.log(`  ${lang}/`);
    console.log(`    common.json`);
});
