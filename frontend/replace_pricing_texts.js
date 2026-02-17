const fs = require('fs');
const path = require('path');

const filePath = path.join(__dirname, 'app', 'page.tsx');
let content = fs.readFileSync(filePath, 'utf8');

// Pricing section title and subtitle
content = content.replace(
    /Vyberte si svoj plán/g,
    "{t('student.pricing.title')}"
);

content = content.replace(
    /Začnite s bezplatným plánom alebo si vyberte prémiové funkcie/g,
    "{t('student.pricing.subtitle')}"
);

// FREE plan
content = content.replace(
    /<h3 className="text-2xl font-bold text-gray-900 mb-2">FREE<\/h3>/g,
    '<h3 className="text-2xl font-bold text-gray-900 mb-2">{t(\'student.pricing.free.name\')}</h3>'
);

content = content.replace(
    /<span className="text-gray-500 ml-2">\/mesiac<\/span>/g,
    '<span className="text-gray-500 ml-2">{t(\'student.pricing.free.period\')}</span>'
);

content = content.replace(
    /<p className="text-sm text-gray-600">Základný prístup<\/p>/g,
    '<p className="text-sm text-gray-600">{t(\'student.pricing.free.description\')}</p>'
);

content = content.replace(
    /<span className="text-sm text-gray-600">Prehliadanie univerzít<\/span>/g,
    '<span className="text-sm text-gray-600">{t(\'student.pricing.free.features.browse\')}</span>'
);

content = content.replace(
    /<span className="text-sm text-gray-600">Odkazy na oficiálne stránky<\/span>/g,
    '<span className="text-sm text-gray-600">{t(\'student.pricing.free.features.links\')}</span>'
);

content = content.replace(
    /<span className="text-sm text-gray-600">Základné informácie<\/span>/g,
    '<span className="text-sm text-gray-600">{t(\'student.pricing.free.features.info\')}</span>'
);

content = content.replace(
    /<span className="text-sm text-gray-400">Bez AI konzultanta<\/span>/g,
    '<span className="text-sm text-gray-400">{t(\'student.pricing.free.features.noAI\')}</span>'
);

content = content.replace(
    />Aktuálny plán</g,
    '>{t(\'student.pricing.free.currentPlan\')}<'
);

content = content.replace(
    />Začať zadarmo</g,
    '>{t(\'student.pricing.free.button\')}<'
);

// BASIC plan
content = content.replace(
    /<h3 className="text-2xl font-bold text-gray-900 mb-2">BASIC<\/h3>/g,
    '<h3 className="text-2xl font-bold text-gray-900 mb-2">{t(\'student.pricing.basic.name\')}</h3>'
);

content = content.replace(
    /<div className="absolute top-0 right-0 bg-blue-500 text-white px-4 py-1 rounded-bl-lg rounded-tr-lg text-sm font-semibold">\s*Populárne\s*<\/div>/g,
    '<div className="absolute top-0 right-0 bg-blue-500 text-white px-4 py-1 rounded-bl-lg rounded-tr-lg text-sm font-semibold">\n                                    {t(\'student.pricing.basic.badge\')}\n                                </div>'
);

content = content.replace(
    /<p className="text-sm text-gray-600">Pre aktívnych študentov<\/p>/g,
    '<p className="text-sm text-gray-600">{t(\'student.pricing.basic.description\')}</p>'
);

content = content.replace(
    /<span className="text-sm text-gray-600">Všetko z FREE \+<\/span>/g,
    '<span className="text-sm text-gray-600">{t(\'student.pricing.basic.features.allFree\')}</span>'
);

content = content.replace(
    /<span className="text-sm text-gray-600"><strong>25 AI konzultácií\/deň<\/strong><\/span>/g,
    '<span className="text-sm text-gray-600"><strong>{t(\'student.pricing.basic.features.aiConsultations\')}</strong></span>'
);

content = content.replace(
    /<span className="text-sm text-gray-600">Detailné odpovede<\/span>/g,
    '<span className="text-sm text-gray-600">{t(\'student.pricing.basic.features.detailed\')}</span>'
);

content = content.replace(
    /<span className="text-sm text-gray-600">Hľadanie ubytovania<\/span>/g,
    '<span className="text-sm text-gray-600">{t(\'student.pricing.basic.features.housing\')}</span>'
);

content = content.replace(
    /<span className="text-sm text-gray-600">Brigády pre študentov<\/span>/g,
    '<span className="text-sm text-gray-600">{t(\'student.pricing.basic.features.jobs\')}</span>'
);

content = content.replace(
    />Vybrať BASIC</g,
    '>{t(\'student.pricing.basic.button\')}<'
);

// STANDARD plan
content = content.replace(
    /<h3 className="text-2xl font-bold text-gray-900 mb-2">STANDARD<\/h3>/g,
    '<h3 className="text-2xl font-bold text-gray-900 mb-2">{t(\'student.pricing.standard.name\')}</h3>'
);

content = content.replace(
    /<p className="text-sm text-gray-600">Pre náročných<\/p>/g,
    '<p className="text-sm text-gray-600">{t(\'student.pricing.standard.description\')}</p>'
);

content = content.replace(
    /<span className="text-sm text-gray-600">Všetko z BASIC \+<\/span>/g,
    '<span className="text-sm text-gray-600">{t(\'student.pricing.standard.features.allBasic\')}</span>'
);

content = content.replace(
    /<span className="text-sm text-gray-600"><strong>50 AI konzultácií\/deň<\/strong><\/span>/g,
    '<span className="text-sm text-gray-600"><strong>{t(\'student.pricing.standard.features.aiConsultations\')}</strong></span>'
);

content = content.replace(
    /<span className="text-sm text-gray-600">Pokrokové plány vstupu<\/span>/g,
    '<span className="text-sm text-gray-600">{t(\'student.pricing.standard.features.plans\')}</span>'
);

content = content.replace(
    /<span className="text-sm text-gray-600">Personalizované rady<\/span>/g,
    '<span className="text-sm text-gray-600">{t(\'student.pricing.standard.features.advice\')}</span>'
);

content = content.replace(
    /<span className="text-sm text-gray-600">Šablóny dokumentov<\/span>/g,
    '<span className="text-sm text-gray-600">{t(\'student.pricing.standard.features.templates\')}</span>'
);

content = content.replace(
    />Vybrať STANDARD</g,
    '>{t(\'student.pricing.standard.button\')}<'
);

// PREMIUM plan
content = content.replace(
    /<h3 className="text-2xl font-bold text-gray-900 mb-2">PREMIUM<\/h3>/g,
    '<h3 className="text-2xl font-bold text-gray-900 mb-2">{t(\'student.pricing.premium.name\')}</h3>'
);

content = content.replace(
    /<div className="absolute top-0 right-0 bg-gradient-to-r from-yellow-400 to-orange-400 text-white px-4 py-1 rounded-bl-lg rounded-tr-lg text-sm font-semibold">\s*⭐ Najlepšie\s*<\/div>/g,
    '<div className="absolute top-0 right-0 bg-gradient-to-r from-yellow-400 to-orange-400 text-white px-4 py-1 rounded-bl-lg rounded-tr-lg text-sm font-semibold">\n                                    {t(\'student.pricing.premium.badge\')}\n                                </div>'
);

content = content.replace(
    /<p className="text-sm text-gray-600">Kompletná podpora<\/p>/g,
    '<p className="text-sm text-gray-600">{t(\'student.pricing.premium.description\')}</p>'
);

content = content.replace(
    /<span className="text-sm text-gray-600">Všetko zo STANDARD \+<\/span>/g,
    '<span className="text-sm text-gray-600">{t(\'student.pricing.premium.features.allStandard\')}</span>'
);

content = content.replace(
    /<span className="text-sm text-gray-600"><strong>100 AI konzultácií\/deň<\/strong><\/span>/g,
    '<span className="text-sm text-gray-600"><strong>{t(\'student.pricing.premium.features.aiConsultations\')}</strong></span>'
);

content = content.replace(
    /<span className="text-sm text-gray-600">Expertné konzultácie<\/span>/g,
    '<span className="text-sm text-gray-600">{t(\'student.pricing.premium.features.expert\')}</span>'
);

content = content.replace(
    /<span className="text-sm text-gray-600">Prioritná podpora 24\/7<\/span>/g,
    '<span className="text-sm text-gray-600">{t(\'student.pricing.premium.features.support\')}</span>'
);

content = content.replace(
    /<span className="text-sm text-gray-600">Osobný vstupný plán<\/span>/g,
    '<span className="text-sm text-gray-600">{t(\'student.pricing.premium.features.personalPlan\')}</span>'
);

content = content.replace(
    />Vybrať PREMIUM</g,
    '>{t(\'student.pricing.premium.button\')}<'
);

// Guarantee text
content = content.replace(
    /💳 Bezpečná platba • 🔒 Zrušiteľné kedykoľvek • ✅ Bez skrytých poplatkov/g,
    "{t('student.pricing.guarantee')}"
);

fs.writeFileSync(filePath, content, 'utf8');

console.log('✅ Successfully replaced all hardcoded pricing texts with translation keys!');
