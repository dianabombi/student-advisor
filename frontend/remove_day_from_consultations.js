const fs = require('fs');
const path = require('path');

const localesDir = path.join(__dirname, 'locales');
const languages = ['sk', 'cs', 'pl', 'uk', 'en', 'de', 'fr', 'es', 'it', 'pt', 'ru'];

console.log('🔄 Removing "/day" from AI consultation translations...\n');

const replacements = {
    sk: { from: '/deň', to: '' },
    cs: { from: '/den', to: '' },
    pl: { from: '/dzień', to: '' },
    uk: { from: '/день', to: '' },
    en: { from: '/day', to: '' },
    de: { from: '/Tag', to: '' },
    fr: { from: '/jour', to: '' },
    es: { from: '/día', to: '' },
    it: { from: '/giorno', to: '' },
    pt: { from: '/dia', to: '' },
    ru: { from: '/день', to: '' }
};

languages.forEach(lang => {
    const filePath = path.join(localesDir, lang, 'common.json');

    if (fs.existsSync(filePath)) {
        let content = fs.readFileSync(filePath, 'utf8');
        const original = content;

        // Replace AI consultations text
        const replacement = replacements[lang];
        content = content.replace(new RegExp(`25 AI [^"]+${replacement.from}`, 'g'), match => match.replace(replacement.from, replacement.to));
        content = content.replace(new RegExp(`50 AI [^"]+${replacement.from}`, 'g'), match => match.replace(replacement.from, replacement.to));
        content = content.replace(new RegExp(`100 AI [^"]+${replacement.from}`, 'g'), match => match.replace(replacement.from, replacement.to));

        if (content !== original) {
            fs.writeFileSync(filePath, content, 'utf8');
            console.log(`✅ Updated ${lang}/common.json`);
        } else {
            console.log(`⚠️  No changes needed for ${lang}/common.json`);
        }
    } else {
        console.log(`❌ File not found: ${lang}/common.json`);
    }
});

// Also update student_*.json files
console.log('\n🔄 Updating student_*.json files...\n');

languages.forEach(lang => {
    const filePath = path.join(localesDir, `student_${lang}.json`);

    if (fs.existsSync(filePath)) {
        let content = fs.readFileSync(filePath, 'utf8');
        const original = content;

        const replacement = replacements[lang];
        content = content.replace(new RegExp(`25 AI [^"]+${replacement.from}`, 'g'), match => match.replace(replacement.from, replacement.to));
        content = content.replace(new RegExp(`50 AI [^"]+${replacement.from}`, 'g'), match => match.replace(replacement.from, replacement.to));
        content = content.replace(new RegExp(`100 AI [^"]+${replacement.from}`, 'g'), match => match.replace(replacement.from, replacement.to));

        if (content !== original) {
            fs.writeFileSync(filePath, content, 'utf8');
            console.log(`✅ Updated student_${lang}.json`);
        } else {
            console.log(`⚠️  No changes needed for student_${lang}.json`);
        }
    }
});

console.log('\n🎉 All translations updated successfully!');
