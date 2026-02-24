import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';
import LanguageDetector from 'i18next-browser-languagedetector';

// Import locale files
import en from '@/locales/en/common.json';
import sk from '@/locales/sk/common.json';
import cs from '@/locales/cs/common.json';
import de from '@/locales/de/common.json';
import es from '@/locales/es/common.json';
import fr from '@/locales/fr/common.json';
import it from '@/locales/it/common.json';
import pl from '@/locales/pl/common.json';
import pt from '@/locales/pt/common.json';
import ru from '@/locales/ru/common.json';
import uk from '@/locales/uk/common.json';

if (!i18n.isInitialized) {
    i18n
        .use(LanguageDetector)
        .use(initReactI18next)
        .init({
            resources: {
                en: { translation: en },
                sk: { translation: sk },
                cs: { translation: cs },
                de: { translation: de },
                es: { translation: es },
                fr: { translation: fr },
                it: { translation: it },
                pl: { translation: pl },
                pt: { translation: pt },
                ru: { translation: ru },
                uk: { translation: uk },
            },
            fallbackLng: 'en',
            interpolation: {
                escapeValue: false,
            },
            detection: {
                order: ['localStorage', 'navigator'],
                caches: ['localStorage'],
            },
        });
}

export default i18n;
