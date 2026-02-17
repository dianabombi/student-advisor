const fs = require('fs');
const path = require('path');

// AI Support translations for all languages
const translations = {
    sk: {
        title: "AI Podpora",
        description: "Popíšte svoj problém a AI analyzuje vaše záznamy a pomôže vám ho vyriešiť.",
        placeholder: "Napríklad: 'Nemôžem nahrať dokument' alebo 'AI pomaly odpovedá'",
        analyzing: "Analyzujem záznamy...",
        analyze: "Analyzovať problém",
        analyzed: "Analyzovaných {count} záznamov",
        errorsFound: "Nájdených {count} chýb",
        needsHuman: "Potrebná pomoc operátora",
        needsHumanDesc: "AI zistil zložitý problém. Pošleme váš dopyt technickej podpore.",
        anotherIssue: "Iný problém",
        helped: "Pomohlo!"
    },
    cs: {
        title: "AI Podpora",
        description: "Popište svůj problém a AI analyzuje vaše záznamy a pomůže vám ho vyřešit.",
        placeholder: "Například: 'Nemohu nahrát dokument' nebo 'AI pomalu odpovídá'",
        analyzing: "Analyzuji záznamy...",
        analyze: "Analyzovat problém",
        analyzed: "Analyzováno {count} záznamů",
        errorsFound: "Nalezeno {count} chyb",
        needsHuman: "Potřebná pomoc operátora",
        needsHumanDesc: "AI zjistil složitý problém. Pošleme váš dotaz technické podpoře.",
        anotherIssue: "Jiný problém",
        helped: "Pomohlo!"
    },
    pl: {
        title: "Pomoc AI",
        description: "Opisz swój problem, a AI przeanalizuje twoje logi i pomoże go rozwiązać.",
        placeholder: "Na przykład: 'Nie mogę przesłać dokumentu' lub 'AI wolno odpowiada'",
        analyzing: "Analizuję logi...",
        analyze: "Przeanalizuj problem",
        analyzed: "Przeanalizowano {count} wpisów logów",
        errorsFound: "Znaleziono {count} błędów",
        needsHuman: "Potrzebna pomoc operatora",
        needsHumanDesc: "AI wykrył złożony problem. Prześlemy twoje zapytanie do wsparcia technicznego.",
        anotherIssue: "Inny problem",
        helped: "Pomogło!"
    },
    en: {
        title: "AI Support",
        description: "Describe your problem and AI will analyze your logs and help solve it.",
        placeholder: "For example: 'Cannot upload document' or 'AI responds slowly'",
        analyzing: "Analyzing logs...",
        analyze: "Analyze problem",
        analyzed: "Analyzed {count} log entries",
        errorsFound: "Found {count} errors",
        needsHuman: "Operator assistance needed",
        needsHumanDesc: "AI detected a complex problem. We will send your request to technical support.",
        anotherIssue: "Another issue",
        helped: "Helped!"
    },
    uk: {
        title: "AI Допомога",
        description: "Опиши свою проблему, і AI проаналізує твої логи та допоможе вирішити її.",
        placeholder: "Наприклад: 'Не можу завантажити документ' або 'AI повільно відповідає'",
        analyzing: "Аналізую логи...",
        analyze: "Проаналізувати проблему",
        analyzed: "Проаналізовано {count} записів логів",
        errorsFound: "Знайдено {count} помилок",
        needsHuman: "Потрібна допомога оператора",
        needsHumanDesc: "AI виявив складну проблему. Ми надішлемо твій запит технічній підтримці.",
        anotherIssue: "Інша проблема",
        helped: "Допомогло!"
    },
    ru: {
        title: "AI Помощь",
        description: "Опишите свою проблему, и AI проанализирует ваши логи и поможет решить её.",
        placeholder: "Например: 'Не могу загрузить документ' или 'AI медленно отвечает'",
        analyzing: "Анализирую логи...",
        analyze: "Проанализировать проблему",
        analyzed: "Проанализировано {count} записей логов",
        errorsFound: "Найдено {count} ошибок",
        needsHuman: "Нужна помощь оператора",
        needsHumanDesc: "AI выявил сложную проблему. Мы отправим ваш запрос технической поддержке.",
        anotherIssue: "Другая проблема",
        helped: "Помогло!"
    },
    de: {
        title: "AI-Unterstützung",
        description: "Beschreiben Sie Ihr Problem und die KI analysiert Ihre Protokolle und hilft bei der Lösung.",
        placeholder: "Zum Beispiel: 'Kann Dokument nicht hochladen' oder 'KI antwortet langsam'",
        analyzing: "Analysiere Protokolle...",
        analyze: "Problem analysieren",
        analyzed: "{count} Protokolleinträge analysiert",
        errorsFound: "{count} Fehler gefunden",
        needsHuman: "Operator-Unterstützung erforderlich",
        needsHumanDesc: "Die KI hat ein komplexes Problem erkannt. Wir senden Ihre Anfrage an den technischen Support.",
        anotherIssue: "Anderes Problem",
        helped: "Geholfen!"
    },
    fr: {
        title: "Support IA",
        description: "Décrivez votre problème et l'IA analysera vos journaux et aidera à le résoudre.",
        placeholder: "Par exemple : 'Impossible de télécharger le document' ou 'L'IA répond lentement'",
        analyzing: "Analyse des journaux...",
        analyze: "Analyser le problème",
        analyzed: "{count} entrées de journal analysées",
        errorsFound: "{count} erreurs trouvées",
        needsHuman: "Assistance opérateur nécessaire",
        needsHumanDesc: "L'IA a détecté un problème complexe. Nous enverrons votre demande au support technique.",
        anotherIssue: "Autre problème",
        helped: "Aidé!"
    },
    es: {
        title: "Soporte IA",
        description: "Describe tu problema y la IA analizará tus registros y ayudará a resolverlo.",
        placeholder: "Por ejemplo: 'No puedo subir documento' o 'IA responde lentamente'",
        analyzing: "Analizando registros...",
        analyze: "Analizar problema",
        analyzed: "{count} entradas de registro analizadas",
        errorsFound: "{count} errores encontrados",
        needsHuman: "Se necesita asistencia del operador",
        needsHumanDesc: "La IA detectó un problema complejo. Enviaremos su solicitud al soporte técnico.",
        anotherIssue: "Otro problema",
        helped: "¡Ayudó!"
    },
    it: {
        title: "Supporto IA",
        description: "Descrivi il tuo problema e l'IA analizzerà i tuoi log e aiuterà a risolverlo.",
        placeholder: "Ad esempio: 'Non riesco a caricare il documento' o 'L'IA risponde lentamente'",
        analyzing: "Analizzando i log...",
        analyze: "Analizza problema",
        analyzed: "{count} voci di log analizzate",
        errorsFound: "{count} errori trovati",
        needsHuman: "Necessaria assistenza operatore",
        needsHumanDesc: "L'IA ha rilevato un problema complesso. Invieremo la tua richiesta al supporto tecnico.",
        anotherIssue: "Altro problema",
        helped: "Aiutato!"
    }
};

// Add aiSupport to each language file
Object.keys(translations).forEach(lang => {
    const filePath = path.join(__dirname, 'locales', lang, 'common.json');

    try {
        const content = JSON.parse(fs.readFileSync(filePath, 'utf8'));
        content.aiSupport = translations[lang];
        fs.writeFileSync(filePath, JSON.stringify(content, null, 4), 'utf8');
        console.log(`✅ Added aiSupport to ${lang}/common.json`);
    } catch (error) {
        console.error(`❌ Error updating ${lang}/common.json:`, error.message);
    }
});

console.log('\n✅ All translations added!');
