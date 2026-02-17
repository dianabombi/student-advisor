const fs = require('fs');
const path = require('path');

const sidebarTranslations = {
    sk: { about: "O nás", howItWorks: "Ako to funguje", feedback: "Spätná väzba" },
    cs: { about: "O nás", howItWorks: "Jak to funguje", feedback: "Zpětná vazba" },
    pl: { about: "O nas", howItWorks: "Jak to działa", feedback: "Opinia" },
    en: { about: "About Us", howItWorks: "How It Works", feedback: "Feedback" },
    uk: { about: "Про нас", howItWorks: "Як це працює", feedback: "Зворотній зв'язок" },
    ru: { about: "О нас", howItWorks: "Как это работает", feedback: "Обратная связь" },
    de: { about: "Über uns", howItWorks: "Wie es funktioniert", feedback: "Rückmeldung" },
    fr: { about: "À propos", howItWorks: "Comment ça marche", feedback: "Retour d'information" },
    es: { about: "Sobre nosotros", howItWorks: "Cómo funciona", feedback: "Comentarios" },
    it: { about: "Chi siamo", howItWorks: "Come funziona", feedback: "Feedback" }
};

Object.keys(sidebarTranslations).forEach(lang => {
    const filePath = path.join(__dirname, 'locales', lang, 'common.json');
    try {
        const content = JSON.parse(fs.readFileSync(filePath, 'utf8'));
        content.sidebar = sidebarTranslations[lang];
        fs.writeFileSync(filePath, JSON.stringify(content, null, 4), 'utf8');
        console.log(`✅ Added sidebar to ${lang}/common.json`);
    } catch (error) {
        console.error(`❌ Error: ${lang} - ${error.message}`);
    }
});

console.log('\n✅ Done!');
