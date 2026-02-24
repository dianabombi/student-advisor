'use client';

import { ArrowLeft } from 'lucide-react';
import Link from 'next/link';
import { useLanguage } from '@/lib/LanguageContext';

export default function PrivacyPolicyPage() {
    const { t, language } = useLanguage();

    // Translations for all 10 languages
    const translations: Record<string, any> = {
        sk: {
            title: 'Ochrana osobných údajov',
            back: 'Späť',
            lastUpdated: 'Posledná aktualizácia',
            version: 'Verzia',
            contact: 'Kontakt',
            sections: {
                intro: {
                    title: '1. Úvod',
                    content: 'Táto Politika ochrany osobných údajov vysvetľuje, ako Student Advisor zhromažďuje, používa, uchováva a chráni vaše osobné údaje v súlade s Nariadením GDPR (EU) 2016/679.'
                },
                controller: {
                    title: '2. Prevádzkovateľ',
                    content: 'Prevádzkovateľom vašich osobných údajov je Student Advisor Platform.',
                    email: 'E-mail: info@student-advisor.com'
                },
                dataCollected: {
                    title: '3. Aké údaje zhromažďujeme',
                    intro: 'Zhromažďujeme nasledujúce kategórie osobných údajov:',
                    items: [
                        'Identifikačné údaje: meno, priezvisko, e-mail',
                        'Prihlasovacie údaje: heslo (šifrované)',
                        'Údaje o používaní: IP adresa, User Agent, dátum a čas návštevy',
                        'Obsah: informácie o vzdelávacích inštitúciách, vyhľadávanie ubytovania',
                        'Platobné údaje: informácie o predplatnom a platbách'
                    ]
                },
                legalBasis: {
                    title: '4. Právny základ spracovania',
                    intro: 'Vaše údaje spracovávame na základe:',
                    items: [
                        'Súhlas (čl. 6 ods. 1 písm. a GDPR) - pri registrácii',
                        'Plnenie zmluvy (čl. 6 ods. 1 písm. b GDPR) - poskytovanie služieb',
                        'Oprávnený záujem (čl. 6 ods. 1 písm. f GDPR) - zlepšovanie služieb'
                    ]
                },
                purpose: {
                    title: '5. Účel spracovania',
                    intro: 'Vaše údaje používame na:',
                    items: [
                        'Poskytovanie služieb Student Advisor',
                        'Správu vášho účtu',
                        'Spracovanie platieb',
                        'Komunikáciu s vami',
                        'Zlepšovanie našich služieb',
                        'Dodržiavanie právnych povinností'
                    ]
                },
                retention: {
                    title: '6. Doba uchovávania',
                    content: 'Vaše údaje uchovávame:',
                    items: [
                        'Počas trvania vášho účtu',
                        '5 rokov po ukončení účtu (účtovné doklady)',
                        'Do odvolania súhlasu (marketingové účely)'
                    ]
                },
                rights: {
                    title: '7. Vaše práva',
                    intro: 'Máte právo na:',
                    items: [
                        'Prístup k svojim údajom',
                        'Opravu nesprávnych údajov',
                        'Vymazanie údajov ("právo byť zabudnutý")',
                        'Obmedzenie spracovania',
                        'Prenosnosť údajov',
                        'Námietku proti spracovaniu',
                        'Odvolanie súhlasu',
                        'Podanie sťažnosti na Úrad na ochranu osobných údajov SR'
                    ]
                },
                security: {
                    title: '8. Bezpečnosť údajov',
                    content: 'Vaše údaje chránime pomocou:',
                    items: [
                        'Šifrovania hesiel (bcrypt)',
                        'HTTPS protokolu',
                        'Zabezpečených serverov',
                        'Pravidelných bezpečnostných auditov',
                        'Obmedzenia prístupu len pre oprávnené osoby'
                    ]
                },
                cookies: {
                    title: '9. Cookies',
                    content: 'Používame cookies na:',
                    items: [
                        'Udržanie prihlásenia',
                        'Uloženie jazykových preferencií',
                        'Analytiku návštevnosti (anonymne)'
                    ]
                },
                thirdParty: {
                    title: '10. Zdieľanie údajov',
                    content: 'Vaše údaje môžeme zdieľať s:',
                    items: [
                        'Platobné brány (spracovanie platieb)',
                        'Hosting poskytovatelia (uloženie dát)',
                        'Analytické nástroje (anonymizované údaje)'
                    ],
                    note: 'Nikdy nepredávame vaše údaje tretím stranám na marketingové účely.'
                },
                changes: {
                    title: '11. Zmeny politiky',
                    content: 'Túto politiku môžeme kedykoľvek aktualizovať. O zmenách vás budeme informovať e-mailom alebo oznámením na platforme.'
                },
                contact: {
                    title: '12. Kontakt',
                    content: 'Pre otázky ohľadom ochrany osobných údajov nás kontaktujte:',
                    email: 'E-mail: privacy@student-advisor.com'
                }
            }
        },
        cs: {
            title: 'Ochrana osobních údajů',
            back: 'Zpět',
            lastUpdated: 'Poslední aktualizace',
            version: 'Verze',
            contact: 'Kontakt',
            sections: {
                intro: {
                    title: '1. Úvod',
                    content: 'Tato Politika ochrany osobních údajů vysvětluje, jak Student Advisor shromažďuje, používá, uchovává a chrání vaše osobní údaje v souladu s Nařízením GDPR (EU) 2016/679.'
                },
                controller: {
                    title: '2. Správce',
                    content: 'Správcem vašich osobních údajů je Student Advisor Platform.',
                    email: 'E-mail: info@student-advisor.com'
                },
                dataCollected: {
                    title: '3. Jaké údaje shromažďujeme',
                    intro: 'Shromažďujeme následující kategorie osobních údajů:',
                    items: [
                        'Identifikační údaje: jméno, příjmení, e-mail',
                        'Přihlašovací údaje: heslo (šifrované)',
                        'Údaje o používání: IP adresa, User Agent, datum a čas návštěvy',
                        'Obsah: informace o vzdělávacích institucích, vyhledávání ubytování',
                        'Platební údaje: informace o předplatném a platbách'
                    ]
                },
                legalBasis: {
                    title: '4. Právní základ zpracování',
                    intro: 'Vaše údaje zpracováváme na základě:',
                    items: [
                        'Souhlas (čl. 6 odst. 1 písm. a GDPR) - při registraci',
                        'Plnění smlouvy (čl. 6 odst. 1 písm. b GDPR) - poskytování služeb',
                        'Oprávněný zájem (čl. 6 odst. 1 písm. f GDPR) - zlepšování služeb'
                    ]
                },
                purpose: {
                    title: '5. Účel zpracování',
                    intro: 'Vaše údaje používáme k:',
                    items: [
                        'Poskytování služeb Student Advisor',
                        'Správě vašeho účtu',
                        'Zpracování plateb',
                        'Komunikaci s vámi',
                        'Zlepšování našich služeb',
                        'Dodržování právních povinností'
                    ]
                },
                retention: {
                    title: '6. Doba uchovávání',
                    content: 'Vaše údaje uchováváme:',
                    items: [
                        'Po dobu trvání vašeho účtu',
                        '5 let po ukončení účtu (účetní doklady)',
                        'Do odvolání souhlasu (marketingové účely)'
                    ]
                },
                rights: {
                    title: '7. Vaše práva',
                    intro: 'Máte právo na:',
                    items: [
                        'Přístup ke svým údajům',
                        'Opravu nesprávných údajů',
                        'Výmaz údajů ("právo být zapomenut")',
                        'Omezení zpracování',
                        'Přenositelnost údajů',
                        'Námitku proti zpracování',
                        'Odvolání souhlasu',
                        'Podání stížnosti na Úřad pro ochranu osobních údajů ČR'
                    ]
                },
                security: {
                    title: '8. Bezpečnost údajů',
                    content: 'Vaše údaje chráníme pomocí:',
                    items: [
                        'Šifrování hesel (bcrypt)',
                        'HTTPS protokolu',
                        'Zabezpečených serverů',
                        'Pravidelných bezpečnostních auditů',
                        'Omezení přístupu pouze pro oprávněné osoby'
                    ]
                },
                cookies: {
                    title: '9. Cookies',
                    content: 'Používáme cookies k:',
                    items: [
                        'Udržení přihlášení',
                        'Uložení jazykových preferencí',
                        'Analytice návštěvnosti (anonymně)'
                    ]
                },
                thirdParty: {
                    title: '10. Sdílení údajů',
                    content: 'Vaše údaje můžeme sdílet s:',
                    items: [
                        'Platební brány (zpracování plateb)',
                        'Hosting poskytovatelé (uložení dat)',
                        'Analytické nástroje (anonymizované údaje)'
                    ],
                    note: 'Nikdy neprodáváme vaše údaje třetím stranám pro marketingové účely.'
                },
                changes: {
                    title: '11. Změny politiky',
                    content: 'Tuto politiku můžeme kdykoli aktualizovat. O změnách vás budeme informovat e-mailem nebo oznámením na platformě.'
                },
                contact: {
                    title: '12. Kontakt',
                    content: 'Pro otázky ohledně ochrany osobních údajů nás kontaktujte:',
                    email: 'E-mail: privacy@student-advisor.com'
                }
            }
        },
        pl: {
            title: 'Ochrona danych osobowych',
            back: 'Wstecz',
            lastUpdated: 'Ostatnia aktualizacja',
            version: 'Wersja',
            contact: 'Kontakt',
            sections: {
                intro: {
                    title: '1. Wstęp',
                    content: 'Niniejsza Polityka ochrony danych osobowych wyjaśnia, w jaki sposób Student Advisor zbiera, wykorzystuje, przechowuje i chroni Państwa dane osobowe zgodnie z Rozporządzeniem RODO (UE) 2016/679.'
                },
                controller: {
                    title: '2. Administrator',
                    content: 'Administratorem Państwa danych osobowych jest Student Advisor Platform.',
                    email: 'E-mail: info@student-advisor.com'
                },
                dataCollected: {
                    title: '3. Jakie dane zbieramy',
                    intro: 'Zbieramy następujące kategorie danych osobowych:',
                    items: [
                        'Dane identyfikacyjne: imię, nazwisko, e-mail',
                        'Dane logowania: hasło (zaszyfrowane)',
                        'Dane o użytkowaniu: adres IP, User Agent, data i czas wizyty',
                        'Treść: informacje o instytucjach edukacyjnych, wyszukiwanie zakwaterowania',
                        'Dane płatności: informacje o subskrypcji i płatnościach'
                    ]
                },
                legalBasis: {
                    title: '4. Podstawa prawna przetwarzania',
                    intro: 'Przetwarzamy Państwa dane na podstawie:',
                    items: [
                        'Zgoda (art. 6 ust. 1 lit. a RODO) - przy rejestracji',
                        'Wykonanie umowy (art. 6 ust. 1 lit. b RODO) - świadczenie usług',
                        'Prawnie uzasadniony interes (art. 6 ust. 1 lit. f RODO) - ulepszanie usług'
                    ]
                },
                purpose: {
                    title: '5. Cel przetwarzania',
                    intro: 'Wykorzystujemy Państwa dane do:',
                    items: [
                        'Świadczenia usług Student Advisor',
                        'Zarządzania Państwa kontem',
                        'Przetwarzania płatności',
                        'Komunikacji z Państwem',
                        'Ulepszania naszych usług',
                        'Przestrzegania obowiązków prawnych'
                    ]
                },
                retention: {
                    title: '6. Okres przechowywania',
                    content: 'Przechowujemy Państwa dane:',
                    items: [
                        'Przez okres trwania Państwa konta',
                        '5 lat po zakończeniu konta (dokumenty księgowe)',
                        'Do momentu wycofania zgody (cele marketingowe)'
                    ]
                },
                rights: {
                    title: '7. Państwa prawa',
                    intro: 'Mają Państwo prawo do:',
                    items: [
                        'Dostępu do swoich danych',
                        'Sprostowania nieprawidłowych danych',
                        'Usunięcia danych ("prawo do bycia zapomnianym")',
                        'Ograniczenia przetwarzania',
                        'Przenoszenia danych',
                        'Sprzeciwu wobec przetwarzania',
                        'Cofnięcia zgody',
                        'Wniesienia skargi do Urzędu Ochrony Danych Osobowych'
                    ]
                },
                security: {
                    title: '8. Bezpieczeństwo danych',
                    content: 'Chronimy Państwa dane za pomocą:',
                    items: [
                        'Szyfrowania haseł (bcrypt)',
                        'Protokołu HTTPS',
                        'Zabezpieczonych serwerów',
                        'Regularnych audytów bezpieczeństwa',
                        'Ograniczenia dostępu tylko dla upoważnionych osób'
                    ]
                },
                cookies: {
                    title: '9. Pliki cookies',
                    content: 'Używamy plików cookies do:',
                    items: [
                        'Utrzymania zalogowania',
                        'Zapisania preferencji językowych',
                        'Analityki odwiedzin (anonimowo)'
                    ]
                },
                thirdParty: {
                    title: '10. Udostępnianie danych',
                    content: 'Możemy udostępniać Państwa dane:',
                    items: [
                        'Bramki płatności (przetwarzanie płatności)',
                        'Dostawcy hostingu (przechowywanie danych)',
                        'Narzędzia analityczne (dane zanonimizowane)'
                    ],
                    note: 'Nigdy nie sprzedajemy Państwa danych stronom trzecim w celach marketingowych.'
                },
                changes: {
                    title: '11. Zmiany polityki',
                    content: 'Możemy w dowolnym momencie zaktualizować niniejszą politykę. O zmianach poinformujemy Państwa e-mailem lub powiadomieniem na platformie.'
                },
                contact: {
                    title: '12. Kontakt',
                    content: 'W sprawach dotyczących ochrony danych osobowych prosimy o kontakt:',
                    email: 'E-mail: privacy@student-advisor.com'
                }
            }
        },
        en: {
            title: 'Privacy Policy',
            back: 'Back',
            lastUpdated: 'Last updated',
            version: 'Version',
            contact: 'Contact',
            sections: {
                intro: {
                    title: '1. Introduction',
                    content: 'This Privacy Policy explains how Student Advisor collects, uses, stores, and protects your personal data in accordance with GDPR Regulation (EU) 2016/679.'
                },
                controller: {
                    title: '2. Data Controller',
                    content: 'The controller of your personal data is Student Advisor Platform.',
                    email: 'Email: info@student-advisor.com'
                },
                dataCollected: {
                    title: '3. What Data We Collect',
                    intro: 'We collect the following categories of personal data:',
                    items: [
                        'Identification data: name, surname, email',
                        'Login credentials: password (encrypted)',
                        'Usage data: IP address, User Agent, date and time of visit',
                        'Content: educational institution information, housing search',
                        'Payment data: subscription and payment information'
                    ]
                },
                legalBasis: {
                    title: '4. Legal Basis for Processing',
                    intro: 'We process your data based on:',
                    items: [
                        'Consent (Art. 6(1)(a) GDPR) - upon registration',
                        'Contract performance (Art. 6(1)(b) GDPR) - service provision',
                        'Legitimate interest (Art. 6(1)(f) GDPR) - service improvement'
                    ]
                },
                purpose: {
                    title: '5. Purpose of Processing',
                    intro: 'We use your data to:',
                    items: [
                        'Provide Student Advisor services',
                        'Manage your account',
                        'Process payments',
                        'Communicate with you',
                        'Improve our services',
                        'Comply with legal obligations'
                    ]
                },
                retention: {
                    title: '6. Retention Period',
                    content: 'We retain your data:',
                    items: [
                        'For the duration of your account',
                        '5 years after account termination (accounting documents)',
                        'Until consent withdrawal (marketing purposes)'
                    ]
                },
                rights: {
                    title: '7. Your Rights',
                    intro: 'You have the right to:',
                    items: [
                        'Access your data',
                        'Rectify incorrect data',
                        'Erasure of data ("right to be forgotten")',
                        'Restriction of processing',
                        'Data portability',
                        'Object to processing',
                        'Withdraw consent',
                        'Lodge a complaint with the Data Protection Authority'
                    ]
                },
                security: {
                    title: '8. Data Security',
                    content: 'We protect your data using:',
                    items: [
                        'Password encryption (bcrypt)',
                        'HTTPS protocol',
                        'Secured servers',
                        'Regular security audits',
                        'Access restriction to authorized personnel only'
                    ]
                },
                cookies: {
                    title: '9. Cookies',
                    content: 'We use cookies for:',
                    items: [
                        'Maintaining login session',
                        'Storing language preferences',
                        'Analytics (anonymously)'
                    ]
                },
                thirdParty: {
                    title: '10. Data Sharing',
                    content: 'We may share your data with:',
                    items: [
                        'Payment gateways (payment processing)',
                        'Hosting providers (data storage)',
                        'Analytics tools (anonymized data)'
                    ],
                    note: 'We never sell your data to third parties for marketing purposes.'
                },
                changes: {
                    title: '11. Policy Changes',
                    content: 'We may update this policy at any time. We will inform you of changes via email or platform notification.'
                },
                contact: {
                    title: '12. Contact',
                    content: 'For questions regarding data protection, please contact us:',
                    email: 'Email: privacy@student-advisor.com'
                }
            }
        },
        // Add more languages (de, it, fr, es, hu, ro) - shortened for space
        de: {
            title: 'Datenschutzrichtlinie',
            back: 'Zurück',
            lastUpdated: 'Letzte Aktualisierung',
            version: 'Version',
            contact: 'Kontakt',
            sections: {
                intro: {
                    title: '1. Einleitung',
                    content: 'Diese Datenschutzrichtlinie erklärt, wie Student Advisor Ihre personenbezogenen Daten gemäß der DSGVO-Verordnung (EU) 2016/679 sammelt, verwendet, speichert und schützt.'
                },
                controller: {
                    title: '2. Verantwortlicher',
                    content: 'Der Verantwortliche für Ihre personenbezogenen Daten ist Student Advisor Platform.',
                    email: 'E-Mail: info@student-advisor.com'
                },
                dataCollected: {
                    title: '3. Welche Daten wir sammeln',
                    intro: 'Wir sammeln folgende Kategorien personenbezogener Daten:',
                    items: [
                        'Identifikationsdaten: Name, Nachname, E-Mail',
                        'Anmeldedaten: Passwort (verschlüsselt)',
                        'Nutzungsdaten: IP-Adresse, User Agent, Datum und Uhrzeit des Besuchs',
                        'Inhalt: Informationen über Bildungseinrichtungen, Wohnungssuche',
                        'Zahlungsdaten: Abonnement- und Zahlungsinformationen'
                    ]
                },
                legalBasis: {
                    title: '4. Rechtsgrundlage der Verarbeitung',
                    intro: 'Wir verarbeiten Ihre Daten auf Grundlage von:',
                    items: [
                        'Einwilligung (Art. 6 Abs. 1 lit. a DSGVO) - bei Registrierung',
                        'Vertragserfüllung (Art. 6 Abs. 1 lit. b DSGVO) - Dienstleistungserbringung',
                        'Berechtigtes Interesse (Art. 6 Abs. 1 lit. f DSGVO) - Verbesserung der Dienste'
                    ]
                },
                purpose: {
                    title: '5. Zweck der Verarbeitung',
                    intro: 'Wir verwenden Ihre Daten für:',
                    items: [
                        'Bereitstellung der Student Advisor-Dienste',
                        'Verwaltung Ihres Kontos',
                        'Zahlungsabwicklung',
                        'Kommunikation mit Ihnen',
                        'Verbesserung unserer Dienste',
                        'Einhaltung gesetzlicher Verpflichtungen'
                    ]
                },
                retention: {
                    title: '6. Aufbewahrungsdauer',
                    content: 'Wir speichern Ihre Daten:',
                    items: [
                        'Für die Dauer Ihres Kontos',
                        '5 Jahre nach Kontoauflösung (Buchhaltungsunterlagen)',
                        'Bis zum Widerruf der Einwilligung (Marketingzwecke)'
                    ]
                },
                rights: {
                    title: '7. Ihre Rechte',
                    intro: 'Sie haben das Recht auf:',
                    items: [
                        'Zugang zu Ihren Daten',
                        'Berichtigung falscher Daten',
                        'Löschung von Daten ("Recht auf Vergessenwerden")',
                        'Einschränkung der Verarbeitung',
                        'Datenübertragbarkeit',
                        'Widerspruch gegen die Verarbeitung',
                        'Widerruf der Einwilligung',
                        'Beschwerde bei der Datenschutzbehörde'
                    ]
                },
                security: {
                    title: '8. Datensicherheit',
                    content: 'Wir schützen Ihre Daten durch:',
                    items: [
                        'Passwortverschlüsselung (bcrypt)',
                        'HTTPS-Protokoll',
                        'Gesicherte Server',
                        'Regelmäßige Sicherheitsaudits',
                        'Zugriffsbeschränkung nur für autorisiertes Personal'
                    ]
                },
                cookies: {
                    title: '9. Cookies',
                    content: 'Wir verwenden Cookies für:',
                    items: [
                        'Aufrechterhaltung der Anmeldung',
                        'Speicherung von Spracheinstellungen',
                        'Analytik (anonym)'
                    ]
                },
                thirdParty: {
                    title: '10. Datenweitergabe',
                    content: 'Wir können Ihre Daten weitergeben an:',
                    items: [
                        'Zahlungsgateways (Zahlungsabwicklung)',
                        'Hosting-Anbieter (Datenspeicherung)',
                        'Analysetools (anonymisierte Daten)'
                    ],
                    note: 'Wir verkaufen Ihre Daten niemals an Dritte für Marketingzwecke.'
                },
                changes: {
                    title: '11. Richtlinienänderungen',
                    content: 'Wir können diese Richtlinie jederzeit aktualisieren. Wir werden Sie über Änderungen per E-Mail oder Plattformbenachrichtigung informieren.'
                },
                contact: {
                    title: '12. Kontakt',
                    content: 'Bei Fragen zum Datenschutz kontaktieren Sie uns bitte:',
                    email: 'E-Mail: privacy@student-advisor.com'
                }
            }
        },
        uk: {
            title: 'Захист персональних даних',
            back: 'Назад',
            lastUpdated: 'Остання актуалізація',
            version: 'Версія',
            contact: 'Контакт',
            sections: {
                intro: {
                    title: '1. Вступ',
                    content: 'Ця Політика захисту персональних даних пояснює, як Student Advisor збирає, використовує, зберігає та захищає ваші персональні дані відповідно до Регламенту GDPR (ЄС) 2016/679.'
                },
                controller: {
                    title: '2. Контролер даних',
                    content: 'Контролером ваших персональних даних є Student Advisor Platform.',
                    email: 'Email: info@student-advisor.com'
                },
                dataCollected: {
                    title: '3. Які дані ми збираємо',
                    intro: 'Ми збираємо наступні категорії персональних даних:',
                    items: [
                        'Ідентифікаційні дані: ім\'я, прізвище, email',
                        'Дані для входу: пароль (зашифрований)',
                        'Дані використання: IP-адреса, User Agent, дата та час відвідування',
                        'Контент: інформація про освітні заклади, пошук житла',
                        'Платіжні дані: інформація про підписку та платежі'
                    ]
                },
                legalBasis: {
                    title: '4. Правова основа обробки',
                    intro: 'Ми обробляємо ваші дані на основі:',
                    items: [
                        'Згода (ст. 6(1)(a) GDPR) - при реєстрації',
                        'Виконання договору (ст. 6(1)(b) GDPR) - надання послуг',
                        'Законний інтерес (ст. 6(1)(f) GDPR) - покращення послуг'
                    ]
                },
                purpose: {
                    title: '5. Мета обробки',
                    intro: 'Ми використовуємо ваші дані для:',
                    items: [
                        'Надання послуг Student Advisor',
                        'Управління вашим обліковим записом',
                        'Обробки платежів',
                        'Спілкування з вами',
                        'Покращення наших послуг',
                        'Дотримання юридичних зобов\'язань'
                    ]
                },
                retention: {
                    title: '6. Термін зберігання',
                    content: 'Ми зберігаємо ваші дані:',
                    items: [
                        'Протягом терміну дії вашого облікового запису',
                        '5 років після закриття облікового запису (бухгалтерські документи)',
                        'До відкликання згоди (маркетингові цілі)'
                    ]
                },
                rights: {
                    title: '7. Ваші права',
                    intro: 'Ви маєте право на:',
                    items: [
                        'Доступ до ваших даних',
                        'Виправлення неправильних даних',
                        'Видалення даних ("право бути забутим")',
                        'Обмеження обробки',
                        'Переносимість даних',
                        'Заперечення проти обробки',
                        'Відкликання згоди',
                        'Подання скарги до Уповноваженого з захисту персональних даних'
                    ]
                },
                security: {
                    title: '8. Безпека даних',
                    content: 'Ми захищаємо ваші дані за допомогою:',
                    items: [
                        'Шифрування паролів (bcrypt)',
                        'Протоколу HTTPS',
                        'Захищених серверів',
                        'Регулярних аудитів безпеки',
                        'Обмеження доступу тільки для уповноважених осіб'
                    ]
                },
                cookies: {
                    title: '9. Cookies',
                    content: 'Ми використовуємо cookies для:',
                    items: [
                        'Підтримки сесії входу',
                        'Збереження мовних налаштувань',
                        'Аналітики (анонімно)'
                    ]
                },
                thirdParty: {
                    title: '10. Передача даних',
                    content: 'Ми можемо передавати ваші дані:',
                    items: [
                        'Платіжні шлюзи (обробка платежів)',
                        'Хостинг-провайдери (зберігання даних)',
                        'Аналітичні інструменти (анонімізовані дані)'
                    ],
                    note: 'Ми ніколи не продаємо ваші дані третім особам для маркетингових цілей.'
                },
                changes: {
                    title: '11. Зміни політики',
                    content: 'Ми можемо оновити цю політику в будь-який час. Ми повідомимо вас про зміни електронною поштою або сповіщенням на платформі.'
                },
                contact: {
                    title: '12. Контакт',
                    content: 'З питань захисту персональних даних зв\'яжіться з нами:',
                    email: 'Email: privacy@student-advisor.com'
                }
            }
        },
        it: {
            title: 'Informativa sulla privacy',
            back: 'Indietro',
            lastUpdated: 'Ultimo aggiornamento',
            version: 'Versione',
            contact: 'Contatto',
            sections: {
                intro: {
                    title: '1. Introduzione',
                    content: 'Questa Informativa sulla privacy spiega come Student Advisor raccoglie, utilizza, conserva e protegge i vostri dati personali in conformità con il Regolamento GDPR (UE) 2016/679.'
                },
                controller: {
                    title: '2. Titolare del trattamento',
                    content: 'Il titolare del trattamento dei vostri dati personali è Student Advisor Platform.',
                    email: 'Email: info@student-advisor.com'
                },
                dataCollected: {
                    title: '3. Quali dati raccogliamo',
                    intro: 'Raccogliamo le seguenti categorie di dati personali:',
                    items: [
                        'Dati identificativi: nome, cognome, email',
                        'Credenziali di accesso: password (criptata)',
                        'Dati di utilizzo: indirizzo IP, User Agent, data e ora della visita',
                        'Contenuto: informazioni sulle istituzioni educative, ricerca alloggio',
                        'Dati di pagamento: informazioni su abbonamento e pagamenti'
                    ]
                },
                legalBasis: {
                    title: '4. Base giuridica del trattamento',
                    intro: 'Trattiamo i vostri dati sulla base di:',
                    items: [
                        'Consenso (Art. 6(1)(a) GDPR) - al momento della registrazione',
                        'Esecuzione del contratto (Art. 6(1)(b) GDPR) - fornitura di servizi',
                        'Interesse legittimo (Art. 6(1)(f) GDPR) - miglioramento dei servizi'
                    ]
                },
                purpose: {
                    title: '5. Finalità del trattamento',
                    intro: 'Utilizziamo i vostri dati per:',
                    items: [
                        'Fornire i servizi Student Advisor',
                        'Gestire il vostro account',
                        'Elaborare i pagamenti',
                        'Comunicare con voi',
                        'Migliorare i nostri servizi',
                        'Rispettare gli obblighi legali'
                    ]
                },
                retention: {
                    title: '6. Periodo di conservazione',
                    content: 'Conserviamo i vostri dati:',
                    items: [
                        'Per la durata del vostro account',
                        '5 anni dopo la chiusura dell\'account (documenti contabili)',
                        'Fino alla revoca del consenso (finalità di marketing)'
                    ]
                },
                rights: {
                    title: '7. I vostri diritti',
                    intro: 'Avete il diritto di:',
                    items: [
                        'Accedere ai vostri dati',
                        'Rettificare dati inesatti',
                        'Cancellare i dati ("diritto all\'oblio")',
                        'Limitare il trattamento',
                        'Portabilità dei dati',
                        'Opporsi al trattamento',
                        'Revocare il consenso',
                        'Presentare un reclamo all\'Autorità Garante per la protezione dei dati personali'
                    ]
                },
                security: {
                    title: '8. Sicurezza dei dati',
                    content: 'Proteggiamo i vostri dati utilizzando:',
                    items: [
                        'Crittografia delle password (bcrypt)',
                        'Protocollo HTTPS',
                        'Server protetti',
                        'Audit di sicurezza regolari',
                        'Restrizione dell\'accesso solo al personale autorizzato'
                    ]
                },
                cookies: {
                    title: '9. Cookie',
                    content: 'Utilizziamo i cookie per:',
                    items: [
                        'Mantenere la sessione di accesso',
                        'Memorizzare le preferenze linguistiche',
                        'Analisi (in forma anonima)'
                    ]
                },
                thirdParty: {
                    title: '10. Condivisione dei dati',
                    content: 'Possiamo condividere i vostri dati con:',
                    items: [
                        'Gateway di pagamento (elaborazione pagamenti)',
                        'Provider di hosting (archiviazione dati)',
                        'Strumenti di analisi (dati anonimizzati)'
                    ],
                    note: 'Non vendiamo mai i vostri dati a terze parti per scopi di marketing.'
                },
                changes: {
                    title: '11. Modifiche alla politica',
                    content: 'Possiamo aggiornare questa politica in qualsiasi momento. Vi informeremo delle modifiche via email o tramite notifica sulla piattaforma.'
                },
                contact: {
                    title: '12. Contatto',
                    content: 'Per domande sulla protezione dei dati, contattateci:',
                    email: 'Email: privacy@student-advisor.com'
                }
            }
        },
        fr: {
            title: 'Politique de confidentialité',
            back: 'Retour',
            lastUpdated: 'Dernière mise à jour',
            version: 'Version',
            contact: 'Contact',
            sections: {
                intro: {
                    title: '1. Introduction',
                    content: 'Cette Politique de confidentialité explique comment Student Advisor collecte, utilise, stocke et protège vos données personnelles conformément au Règlement RGPD (UE) 2016/679.'
                },
                controller: {
                    title: '2. Responsable du traitement',
                    content: 'Le responsable du traitement de vos données personnelles est Student Advisor Platform.',
                    email: 'Email: info@student-advisor.com'
                },
                dataCollected: {
                    title: '3. Quelles données nous collectons',
                    intro: 'Nous collectons les catégories suivantes de données personnelles:',
                    items: [
                        'Données d\'identification: nom, prénom, email',
                        'Identifiants de connexion: mot de passe (crypté)',
                        'Données d\'utilisation: adresse IP, User Agent, date et heure de visite',
                        'Contenu: informations sur les établissements d\'enseignement, recherche de logement',
                        'Données de paiement: informations sur l\'abonnement et les paiements'
                    ]
                },
                legalBasis: {
                    title: '4. Base juridique du traitement',
                    intro: 'Nous traitons vos données sur la base de:',
                    items: [
                        'Consentement (Art. 6(1)(a) RGPD) - lors de l\'inscription',
                        'Exécution du contrat (Art. 6(1)(b) RGPD) - fourniture de services',
                        'Intérêt légitime (Art. 6(1)(f) RGPD) - amélioration des services'
                    ]
                },
                purpose: {
                    title: '5. Finalité du traitement',
                    intro: 'Nous utilisons vos données pour:',
                    items: [
                        'Fournir les services Student Advisor',
                        'Gérer votre compte',
                        'Traiter les paiements',
                        'Communiquer avec vous',
                        'Améliorer nos services',
                        'Respecter les obligations légales'
                    ]
                },
                retention: {
                    title: '6. Durée de conservation',
                    content: 'Nous conservons vos données:',
                    items: [
                        'Pendant la durée de votre compte',
                        '5 ans après la fermeture du compte (documents comptables)',
                        'Jusqu\'au retrait du consentement (finalités marketing)'
                    ]
                },
                rights: {
                    title: '7. Vos droits',
                    intro: 'Vous avez le droit de:',
                    items: [
                        'Accéder à vos données',
                        'Rectifier les données inexactes',
                        'Effacer les données ("droit à l\'oubli")',
                        'Limiter le traitement',
                        'Portabilité des données',
                        'Vous opposer au traitement',
                        'Retirer votre consentement',
                        'Déposer une plainte auprès de la CNIL'
                    ]
                },
                security: {
                    title: '8. Sécurité des données',
                    content: 'Nous protégeons vos données en utilisant:',
                    items: [
                        'Cryptage des mots de passe (bcrypt)',
                        'Protocole HTTPS',
                        'Serveurs sécurisés',
                        'Audits de sécurité réguliers',
                        'Restriction d\'accès au personnel autorisé uniquement'
                    ]
                },
                cookies: {
                    title: '9. Cookies',
                    content: 'Nous utilisons des cookies pour:',
                    items: [
                        'Maintenir la session de connexion',
                        'Stocker les préférences linguistiques',
                        'Analyses (de manière anonyme)'
                    ]
                },
                thirdParty: {
                    title: '10. Partage des données',
                    content: 'Nous pouvons partager vos données avec:',
                    items: [
                        'Passerelles de paiement (traitement des paiements)',
                        'Fournisseurs d\'hébergement (stockage des données)',
                        'Outils d\'analyse (données anonymisées)'
                    ],
                    note: 'Nous ne vendons jamais vos données à des tiers à des fins marketing.'
                },
                changes: {
                    title: '11. Modifications de la politique',
                    content: 'Nous pouvons mettre à jour cette politique à tout moment. Nous vous informerons des modifications par email ou par notification sur la plateforme.'
                },
                contact: {
                    title: '12. Contact',
                    content: 'Pour toute question concernant la protection des données, contactez-nous:',
                    email: 'Email: privacy@student-advisor.com'
                }
            }
        },
        es: {
            title: 'Política de privacidad',
            back: 'Atrás',
            lastUpdated: 'Última actualización',
            version: 'Versión',
            contact: 'Contacto',
            sections: {
                intro: {
                    title: '1. Introducción',
                    content: 'Esta Política de privacidad explica cómo Student Advisor recopila, utiliza, almacena y protege sus datos personales de conformidad con el Reglamento RGPD (UE) 2016/679.'
                },
                controller: {
                    title: '2. Responsable del tratamiento',
                    content: 'El responsable del tratamiento de sus datos personales es Student Advisor Platform.',
                    email: 'Email: info@student-advisor.com'
                },
                dataCollected: {
                    title: '3. Qué datos recopilamos',
                    intro: 'Recopilamos las siguientes categorías de datos personales:',
                    items: [
                        'Datos de identificación: nombre, apellido, email',
                        'Credenciales de acceso: contraseña (encriptada)',
                        'Datos de uso: dirección IP, User Agent, fecha y hora de visita',
                        'Contenido: información sobre instituciones educativas, búsqueda de alojamiento',
                        'Datos de pago: información sobre suscripción y pagos'
                    ]
                },
                legalBasis: {
                    title: '4. Base legal del tratamiento',
                    intro: 'Tratamos sus datos en base a:',
                    items: [
                        'Consentimiento (Art. 6(1)(a) RGPD) - al registrarse',
                        'Ejecución del contrato (Art. 6(1)(b) RGPD) - prestación de servicios',
                        'Interés legítimo (Art. 6(1)(f) RGPD) - mejora de servicios'
                    ]
                },
                purpose: {
                    title: '5. Finalidad del tratamiento',
                    intro: 'Utilizamos sus datos para:',
                    items: [
                        'Proporcionar los servicios de Student Advisor',
                        'Gestionar su cuenta',
                        'Procesar pagos',
                        'Comunicarnos con usted',
                        'Mejorar nuestros servicios',
                        'Cumplir con obligaciones legales'
                    ]
                },
                retention: {
                    title: '6. Período de conservación',
                    content: 'Conservamos sus datos:',
                    items: [
                        'Durante la vigencia de su cuenta',
                        '5 años después del cierre de la cuenta (documentos contables)',
                        'Hasta la retirada del consentimiento (fines de marketing)'
                    ]
                },
                rights: {
                    title: '7. Sus derechos',
                    intro: 'Tiene derecho a:',
                    items: [
                        'Acceder a sus datos',
                        'Rectificar datos incorrectos',
                        'Suprimir datos ("derecho al olvido")',
                        'Limitar el tratamiento',
                        'Portabilidad de datos',
                        'Oponerse al tratamiento',
                        'Retirar el consentimiento',
                        'Presentar una reclamación ante la Agencia Española de Protección de Datos'
                    ]
                },
                security: {
                    title: '8. Seguridad de los datos',
                    content: 'Protegemos sus datos mediante:',
                    items: [
                        'Encriptación de contraseñas (bcrypt)',
                        'Protocolo HTTPS',
                        'Servidores seguros',
                        'Auditorías de seguridad regulares',
                        'Restricción de acceso solo a personal autorizado'
                    ]
                },
                cookies: {
                    title: '9. Cookies',
                    content: 'Utilizamos cookies para:',
                    items: [
                        'Mantener la sesión de inicio',
                        'Almacenar preferencias de idioma',
                        'Analíticas (de forma anónima)'
                    ]
                },
                thirdParty: {
                    title: '10. Compartir datos',
                    content: 'Podemos compartir sus datos con:',
                    items: [
                        'Pasarelas de pago (procesamiento de pagos)',
                        'Proveedores de hosting (almacenamiento de datos)',
                        'Herramientas de análisis (datos anonimizados)'
                    ],
                    note: 'Nunca vendemos sus datos a terceros con fines de marketing.'
                },
                changes: {
                    title: '11. Cambios en la política',
                    content: 'Podemos actualizar esta política en cualquier momento. Le informaremos de los cambios por email o mediante notificación en la plataforma.'
                },
                contact: {
                    title: '12. Contacto',
                    content: 'Para preguntas sobre protección de datos, contáctenos:',
                    email: 'Email: privacy@student-advisor.com'
                }
            }
        },
        ru: {
            title: 'Политика конфиденциальности',
            back: 'Назад',
            lastUpdated: 'Последнее обновление',
            version: 'Версия',
            contact: 'Контакт',
            sections: {
                intro: {
                    title: '1. Введение',
                    content: 'Эта Политика конфиденциальности объясняет, как Student Advisor собирает, использует, хранит и защищает ваши персональные данные в соответствии с Регламентом GDPR (ЕС) 2016/679.'
                },
                controller: {
                    title: '2. Контроллер данных',
                    content: 'Контроллером ваших персональных данных является Student Advisor Platform.',
                    email: 'Email: info@student-advisor.com'
                },
                dataCollected: {
                    title: '3. Какие данные мы собираем',
                    intro: 'Мы собираем следующие категории персональных данных:',
                    items: [
                        'Идентификационные данные: имя, фамилия, email',
                        'Данные для входа: пароль (зашифрованный)',
                        'Данные использования: IP-адрес, User Agent, дата и время посещения',
                        'Контент: информация об образовательных учреждениях, поиск жилья',
                        'Платежные данные: информация о подписке и платежах'
                    ]
                },
                legalBasis: {
                    title: '4. Правовая основа обработки',
                    intro: 'Мы обрабатываем ваши данные на основании:',
                    items: [
                        'Согласие (Ст. 6(1)(a) GDPR) - при регистрации',
                        'Исполнение договора (Ст. 6(1)(b) GDPR) - предоставление услуг',
                        'Законный интерес (Ст. 6(1)(f) GDPR) - улучшение услуг'
                    ]
                },
                purpose: {
                    title: '5. Цель обработки',
                    intro: 'Мы используем ваши данные для:',
                    items: [
                        'Предоставления услуг Student Advisor',
                        'Управления вашим аккаунтом',
                        'Обработки платежей',
                        'Общения с вами',
                        'Улучшения наших услуг',
                        'Соблюдения юридических обязательств'
                    ]
                },
                retention: {
                    title: '6. Срок хранения',
                    content: 'Мы храним ваши данные:',
                    items: [
                        'В течение срока действия вашего аккаунта',
                        '5 лет после закрытия аккаунта (бухгалтерские документы)',
                        'До отзыва согласия (маркетинговые цели)'
                    ]
                },
                rights: {
                    title: '7. Ваши права',
                    intro: 'Вы имеете право на:',
                    items: [
                        'Доступ к вашим данным',
                        'Исправление неверных данных',
                        'Удаление данных ("право быть забытым")',
                        'Ограничение обработки',
                        'Переносимость данных',
                        'Возражение против обработки',
                        'Отзыв согласия',
                        'Подачу жалобы в орган по защите данных'
                    ]
                },
                security: {
                    title: '8. Безопасность данных',
                    content: 'Мы защищаем ваши данные с помощью:',
                    items: [
                        'Шифрования паролей (bcrypt)',
                        'Протокола HTTPS',
                        'Защищенных серверов',
                        'Регулярных аудитов безопасности',
                        'Ограничения доступа только для уполномоченного персонала'
                    ]
                },
                cookies: {
                    title: '9. Cookies',
                    content: 'Мы используем cookies для:',
                    items: [
                        'Поддержания сеанса входа',
                        'Сохранения языковых настроек',
                        'Аналитики (анонимно)'
                    ]
                },
                thirdParty: {
                    title: '10. Передача данных',
                    content: 'Мы можем передавать ваши данные:',
                    items: [
                        'Платежные шлюзы (обработка платежей)',
                        'Хостинг-провайдеры (хранение данных)',
                        'Аналитические инструменты (анонимизированные данные)'
                    ],
                    note: 'Мы никогда не продаем ваши данные третьим лицам в маркетинговых целях.'
                },
                changes: {
                    title: '11. Изменения политики',
                    content: 'Мы можем обновить эту политику в любое время. Мы уведомим вас об изменениях по электронной почте или уведомлением на платформе.'
                },
                contact: {
                    title: '12. Контакт',
                    content: 'По вопросам защиты данных свяжитесь с нами:',
                    email: 'Email: privacy@student-advisor.com'
                }
            }
        }
    };


    // Get current language translations or fallback to English
    const content = translations[language] || translations['en'];

    return (
        <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
            <div className="container mx-auto px-6 py-12">
                <Link href="/" className="inline-flex items-center space-x-2 text-gray-300 hover:text-white mb-8 transition-colors">
                    <ArrowLeft className="w-5 h-5" />
                    <span>{content.back}</span>
                </Link>

                <div className="max-w-4xl mx-auto bg-white/5 backdrop-blur-lg rounded-2xl border border-white/10 p-8">
                    <h1 className="text-4xl font-bold text-white mb-8">
                        {content.title}
                    </h1>

                    <div className="prose prose-invert max-w-none">
                        {/* Section 1: Introduction */}
                        <section className="mb-8">
                            <h2 className="text-2xl font-bold text-white mb-4">{content.sections.intro.title}</h2>
                            <p className="text-gray-300 leading-relaxed mb-4">
                                {content.sections.intro.content}
                            </p>
                        </section>

                        {/* Section 2: Controller */}
                        <section className="mb-8">
                            <h2 className="text-2xl font-bold text-white mb-4">{content.sections.controller.title}</h2>
                            <p className="text-gray-300 leading-relaxed mb-2">
                                {content.sections.controller.content}
                            </p>
                            <p className="text-gray-400 text-sm">{content.sections.controller.email}</p>
                        </section>

                        {/* Section 3: Data Collected */}
                        <section className="mb-8">
                            <h2 className="text-2xl font-bold text-white mb-4">{content.sections.dataCollected.title}</h2>
                            <p className="text-gray-300 leading-relaxed mb-4">
                                {content.sections.dataCollected.intro}
                            </p>
                            <ul className="text-gray-300 space-y-2 list-disc list-inside">
                                {content.sections.dataCollected.items.map((item: string, index: number) => (
                                    <li key={index}>{item}</li>
                                ))}
                            </ul>
                        </section>

                        {/* Section 4: Legal Basis */}
                        <section className="mb-8">
                            <h2 className="text-2xl font-bold text-white mb-4">{content.sections.legalBasis.title}</h2>
                            <p className="text-gray-300 leading-relaxed mb-4">
                                {content.sections.legalBasis.intro}
                            </p>
                            <ul className="text-gray-300 space-y-2 list-disc list-inside">
                                {content.sections.legalBasis.items.map((item: string, index: number) => (
                                    <li key={index}>{item}</li>
                                ))}
                            </ul>
                        </section>

                        {/* Section 5: Purpose */}
                        <section className="mb-8">
                            <h2 className="text-2xl font-bold text-white mb-4">{content.sections.purpose.title}</h2>
                            <p className="text-gray-300 leading-relaxed mb-4">
                                {content.sections.purpose.intro}
                            </p>
                            <ul className="text-gray-300 space-y-2 list-disc list-inside">
                                {content.sections.purpose.items.map((item: string, index: number) => (
                                    <li key={index}>{item}</li>
                                ))}
                            </ul>
                        </section>

                        {/* Section 6: Retention */}
                        <section className="mb-8">
                            <h2 className="text-2xl font-bold text-white mb-4">{content.sections.retention.title}</h2>
                            <p className="text-gray-300 leading-relaxed mb-4">
                                {content.sections.retention.content}
                            </p>
                            <ul className="text-gray-300 space-y-2 list-disc list-inside">
                                {content.sections.retention.items.map((item: string, index: number) => (
                                    <li key={index}>{item}</li>
                                ))}
                            </ul>
                        </section>

                        {/* Section 7: Rights */}
                        <section className="mb-8 bg-blue-500/10 border-2 border-blue-500/50 rounded-xl p-6">
                            <h2 className="text-2xl font-bold text-blue-300 mb-4">{content.sections.rights.title}</h2>
                            <p className="text-gray-300 leading-relaxed mb-4">
                                {content.sections.rights.intro}
                            </p>
                            <ul className="text-gray-300 space-y-2 list-disc list-inside">
                                {content.sections.rights.items.map((item: string, index: number) => (
                                    <li key={index}>{item}</li>
                                ))}
                            </ul>
                        </section>

                        {/* Section 8: Security */}
                        <section className="mb-8">
                            <h2 className="text-2xl font-bold text-white mb-4">{content.sections.security.title}</h2>
                            <p className="text-gray-300 leading-relaxed mb-4">
                                {content.sections.security.content}
                            </p>
                            <ul className="text-gray-300 space-y-2 list-disc list-inside">
                                {content.sections.security.items.map((item: string, index: number) => (
                                    <li key={index}>{item}</li>
                                ))}
                            </ul>
                        </section>

                        {/* Section 9: Cookies */}
                        <section className="mb-8">
                            <h2 className="text-2xl font-bold text-white mb-4">{content.sections.cookies.title}</h2>
                            <p className="text-gray-300 leading-relaxed mb-4">
                                {content.sections.cookies.content}
                            </p>
                            <ul className="text-gray-300 space-y-2 list-disc list-inside">
                                {content.sections.cookies.items.map((item: string, index: number) => (
                                    <li key={index}>{item}</li>
                                ))}
                            </ul>
                        </section>

                        {/* Section 10: Third Party */}
                        <section className="mb-8">
                            <h2 className="text-2xl font-bold text-white mb-4">{content.sections.thirdParty.title}</h2>
                            <p className="text-gray-300 leading-relaxed mb-4">
                                {content.sections.thirdParty.content}
                            </p>
                            <ul className="text-gray-300 space-y-2 list-disc list-inside mb-4">
                                {content.sections.thirdParty.items.map((item: string, index: number) => (
                                    <li key={index}>{item}</li>
                                ))}
                            </ul>
                            <p className="text-green-300 font-semibold">{content.sections.thirdParty.note}</p>
                        </section>

                        {/* Section 11: Changes */}
                        <section className="mb-8">
                            <h2 className="text-2xl font-bold text-white mb-4">{content.sections.changes.title}</h2>
                            <p className="text-gray-300 leading-relaxed mb-4">
                                {content.sections.changes.content}
                            </p>
                        </section>

                        {/* Section 12: Contact */}
                        <section className="mb-8">
                            <h2 className="text-2xl font-bold text-white mb-4">{content.sections.contact.title}</h2>
                            <p className="text-gray-300 leading-relaxed mb-2">
                                {content.sections.contact.content}
                            </p>
                            <p className="text-gray-400 text-sm">{content.sections.contact.email}</p>
                        </section>

                        {/* Footer */}
                        <div className="mt-12 pt-8 border-t border-white/20">
                            <p className="text-gray-400 text-sm">
                                {content.lastUpdated}: 21. {language === 'sk' ? 'december' : language === 'cs' ? 'prosinec' : language === 'pl' ? 'grudzień' : 'December'} 2024<br />
                                {content.version}: 1.0<br />
                                {content.contact}: info@student-advisor.com
                            </p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}
