const fs = require('fs');
const path = require('path');

// Read the privacy policy file
const filePath = path.join(__dirname, '..', 'app', 'privacy', 'page.tsx');
let content = fs.readFileSync(filePath, 'utf8');

console.log('🔄 Updating Privacy Policy from CODEX to Student Advisor...\n');

// Replace all occurrences
const replacements = [
    { from: /CODEX Platform/g, to: 'Student Advisor Platform' },
    { from: /CODEX/g, to: 'Student Advisor' },
    { from: /codex-platform\.com/g, to: 'student-advisor.com' },
    { from: /nahrané dokumenty, správy v chate/g, to: 'informácie o vzdelávacích inštitúciách, vyhľadávanie ubytovania' },
    { from: /nahrané dokumenty, zprávy v chatu/g, to: 'informace o vzdělávacích institucích, vyhledávání ubytování' },
    { from: /przesłane dokumenty, wiadomości na czacie/g, to: 'informacje o instytucjach edukacyjnych, wyszukiwanie zakwaterowania' },
    { from: /uploaded documents, chat messages/g, to: 'educational institution information, housing search' },
    { from: /hochgeladene Dokumente, Chat-Nachrichten/g, to: 'Informationen über Bildungseinrichtungen, Wohnungssuche' },
    { from: /завантажені документи, повідомлення в чаті/g, to: 'інформація про освітні заклади, пошук житла' },
    { from: /documenti caricati, messaggi in chat/g, to: 'informazioni sulle istituzioni educative, ricerca alloggio' },
    { from: /documents téléchargés, messages de chat/g, to: 'informations sur les établissements d\'enseignement, recherche de logement' },
    { from: /documentos cargados, mensajes de chat/g, to: 'información sobre instituciones educativas, búsqueda de alojamiento' },
    { from: /загруженные документы, сообщения в чате/g, to: 'информация об образовательных учреждениях, поиск жилья' },
    { from: /21\. december 2024/g, to: '11. január 2026' },
    { from: /21\. prosinec 2024/g, to: '11. leden 2026' },
    { from: /21 grudnia 2024/g, to: '11 stycznia 2026' },
    { from: /December 21, 2024/g, to: 'January 11, 2026' },
    { from: /21\. Dezember 2024/g, to: '11. Januar 2026' },
    { from: /21 грудня 2024/g, to: '11 січня 2026' },
    { from: /21 dicembre 2024/g, to: '11 gennaio 2026' },
    { from: /21 décembre 2024/g, to: '11 janvier 2026' },
    { from: /21 de diciembre de 2024/g, to: '11 de enero de 2026' },
    { from: /21 декабря 2024/g, to: '11 января 2026' },
    { from: /Verzia: 1\.0/g, to: 'Verzia: 2.0 (Student Platform)' },
    { from: /Verze: 1\.0/g, to: 'Verze: 2.0 (Student Platform)' },
    { from: /Wersja: 1\.0/g, to: 'Wersja: 2.0 (Student Platform)' },
    { from: /Version: 1\.0/g, to: 'Version: 2.0 (Student Platform)' },
    { from: /Версія: 1\.0/g, to: 'Версія: 2.0 (Student Platform)' },
    { from: /Versione: 1\.0/g, to: 'Versione: 2.0 (Student Platform)' },
    { from: /Версия: 1\.0/g, to: 'Версия: 2.0 (Student Platform)' }
];

let changeCount = 0;
replacements.forEach(({ from, to }) => {
    const matches = content.match(from);
    if (matches) {
        changeCount += matches.length;
        content = content.replace(from, to);
    }
});

// Write back
fs.writeFileSync(filePath, content, 'utf8');

console.log(`✅ Updated Privacy Policy!`);
console.log(`📝 Made ${changeCount} replacements`);
console.log(`📄 File: ${filePath}\n`);
console.log('🎉 Privacy Policy now reflects Student Advisor educational platform!');
