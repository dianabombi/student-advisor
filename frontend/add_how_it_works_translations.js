const fs = require('fs');
const path = require('path');

const howItWorksTranslations = {
    sk: {
        title: "Ako to funguje",
        subtitle: "Jednoduchý sprievodca používaním platformy CODEX",
        step1: {
            title: "Registrácia a prihlásenie",
            description: "Vytvorte si účet zadaním mena, emailu a hesla. Získate 7-dňový bezplatný prístup k všetkým funkciám platformy."
        },
        step2: {
            title: "Nahratie dokumentov",
            description: "Nahrajte svoje právne dokumenty (zmluvy, žaloby, rozhodnutia súdov) vo formáte PDF, DOCX alebo obrázky. Systém ich automaticky spracuje pomocou OCR."
        },
        step3: {
            title: "Automatická klasifikácia",
            description: "AI automaticky rozpozná typ dokumentu a kategorizuje ho (zmluva, žaloba, rozhodnutie súdu atď.) pre lepšiu organizáciu."
        },
        step4: {
            title: "AI právny konzultant",
            description: "Položte otázku o vašom dokumente alebo právnom probléme. AI analyzuje kontext a poskytne odborné právne poradenstvo podľa slovenského práva."
        },
        step5: {
            title: "Okamžité odpovede",
            description: "Získajte odpovede na právne otázky za sekundy namiesto hodín čakania na advokáta. AI pracuje 24/7."
        },
        step6: {
            title: "Bezpečné uloženie",
            description: "Všetky vaše dokumenty sú šifrované a bezpečne uložené v cloude. Máte k nim prístup kedykoľvek a odkiaľkoľvek."
        },
        step7: {
            title: "História konzultácií",
            description: "Všetky rozhovory s AI sú uložené. Môžete sa kedykoľvek vrátiť k predchádzajúcim konzultáciám a odpovediam."
        },
        step8: {
            title: "Viacjazyčná podpora",
            description: "Platforma podporuje slovenčinu, češtinu, poľštinu, angličtinu, ukrajinčinu, ruštinu, nemčinu, francúzštinu, španielčinu a taliančinu."
        },
        step9: {
            title: "Hromadné spracovanie",
            description: "Nahrajte viacero dokumentov naraz. Systém ich všetky spracuje paralelne a pripraví na analýzu."
        },
        step10: {
            title: "Technická podpora AI",
            description: "Ak máte technický problém, kliknite na modrú ikonu 🔧 v pravom dolnom rohu. AI analyzuje vaše logy a pomôže vyriešiť problém."
        },
        step11: {
            title: "Výber predplatného",
            description: "Po skončení 7-dňovej skúšobnej doby si vyberte mesačné (30€), polročné (80€) alebo ročné (120€) predplatné podľa vašich potrieb."
        },
        step12: {
            title: "Ochrana súkromia",
            description: "Vaše dáta sú chránené podľa GDPR. Nikdy nezdieľame vaše dokumenty s tretími stranami. Máte plnú kontrolu nad svojimi údajmi."
        },
        cta: {
            title: "Pripravení začať?",
            description: "Zaregistrujte sa teraz a získajte 7 dní bezplatného prístupu k všetkým funkciám!",
            button: "Začať zadarmo"
        }
    },
    cs: {
        title: "Jak to funguje",
        subtitle: "Jednoduchý průvodce používáním platformy CODEX",
        step1: {
            title: "Registrace a přihlášení",
            description: "Vytvořte si účet zadáním jména, emailu a hesla. Získáte 7denní bezplatný přístup ke všem funkcím platformy."
        },
        step2: {
            title: "Nahrání dokumentů",
            description: "Nahrajte své právní dokumenty (smlouvy, žaloby, soudní rozhodnutí) ve formátu PDF, DOCX nebo obrázky. Systém je automaticky zpracuje pomocí OCR."
        },
        step3: {
            title: "Automatická klasifikace",
            description: "AI automaticky rozpozná typ dokumentu a kategorizuje ho (smlouva, žaloba, soudní rozhodnutí atd.) pro lepší organizaci."
        },
        step4: {
            title: "AI právní konzultant",
            description: "Položte otázku o vašem dokumentu nebo právním problému. AI analyzuje kontext a poskytne odborné právní poradenství podle českého práva."
        },
        step5: {
            title: "Okamžité odpovědi",
            description: "Získejte odpovědi na právní otázky za sekundy místo hodin čekání na advokáta. AI pracuje 24/7."
        },
        step6: {
            title: "Bezpečné uložení",
            description: "Všechny vaše dokumenty jsou šifrovány a bezpečně uloženy v cloudu. Máte k nim přístup kdykoliv a odkudkoliv."
        },
        step7: {
            title: "Historie konzultací",
            description: "Všechny rozhovory s AI jsou uloženy. Můžete se kdykoliv vrátit k předchozím konzultacím a odpovědím."
        },
        step8: {
            title: "Vícejazyčná podpora",
            description: "Platforma podporuje slovenštinu, češtinu, polštinu, angličtinu, ukrajinštinu, ruštinu, němčinu, francouzštinu, španělštinu a italštinu."
        },
        step9: {
            title: "Hromadné zpracování",
            description: "Nahrajte více dokumentů najednou. Systém je všechny zpracuje paralelně a připraví k analýze."
        },
        step10: {
            title: "Technická podpora AI",
            description: "Pokud máte technický problém, klikněte na modrou ikonu 🔧 v pravém dolním rohu. AI analyzuje vaše logy a pomůže problém vyřešit."
        },
        step11: {
            title: "Výběr předplatného",
            description: "Po skončení 7denní zkušební doby si vyberte měsíční (30€), pololetní (80€) nebo roční (120€) předplatné podle vašich potřeb."
        },
        step12: {
            title: "Ochrana soukromí",
            description: "Vaše data jsou chráněna podle GDPR. Nikdy nesdílíme vaše dokumenty s třetími stranami. Máte plnou kontrolu nad svými údaji."
        },
        cta: {
            title: "Připraveni začít?",
            description: "Zaregistrujte se nyní a získejte 7 dní bezplatného přístupu ke všem funkcím!",
            button: "Začít zdarma"
        }
    },
    pl: {
        title: "Jak to działa",
        subtitle: "Prosty przewodnik korzystania z platformy CODEX",
        step1: {
            title: "Rejestracja i logowanie",
            description: "Utwórz konto podając imię, email i hasło. Otrzymasz 7-dniowy bezpłatny dostęp do wszystkich funkcji platformy."
        },
        step2: {
            title: "Przesyłanie dokumentów",
            description: "Prześlij swoje dokumenty prawne (umowy, pozwy, orzeczenia sądowe) w formacie PDF, DOCX lub obrazy. System automatycznie je przetworzy za pomocą OCR."
        },
        step3: {
            title: "Automatyczna klasyfikacja",
            description: "AI automatycznie rozpozna typ dokumentu i skategoryzuje go (umowa, pozew, orzeczenie sądowe itp.) dla lepszej organizacji."
        },
        step4: {
            title: "AI konsultant prawny",
            description: "Zadaj pytanie o swoim dokumencie lub problemie prawnym. AI przeanalizuje kontekst i udzieli fachowej porady prawnej zgodnie z polskim prawem."
        },
        step5: {
            title: "Natychmiastowe odpowiedzi",
            description: "Otrzymaj odpowiedzi na pytania prawne w ciągu sekund zamiast godzin oczekiwania na adwokata. AI działa 24/7."
        },
        step6: {
            title: "Bezpieczne przechowywanie",
            description: "Wszystkie twoje dokumenty są zaszyfrowane i bezpiecznie przechowywane w chmurze. Masz do nich dostęp zawsze i wszędzie."
        },
        step7: {
            title: "Historia konsultacji",
            description: "Wszystkie rozmowy z AI są zapisywane. Możesz w każdej chwili wrócić do poprzednich konsultacji i odpowiedzi."
        },
        step8: {
            title: "Wsparcie wielojęzyczne",
            description: "Platforma obsługuje słowacki, czeski, polski, angielski, ukraiński, rosyjski, niemiecki, francuski, hiszpański i włoski."
        },
        step9: {
            title: "Przetwarzanie zbiorcze",
            description: "Prześlij wiele dokumentów jednocześnie. System przetworzy je wszystkie równolegle i przygotuje do analizy."
        },
        step10: {
            title: "Wsparcie techniczne AI",
            description: "Jeśli masz problem techniczny, kliknij niebieską ikonę 🔧 w prawym dolnym rogu. AI przeanalizuje twoje logi i pomoże rozwiązać problem."
        },
        step11: {
            title: "Wybór subskrypcji",
            description: "Po zakończeniu 7-dniowego okresu próbnego wybierz miesięczną (30€), półroczną (80€) lub roczną (120€) subskrypcję według swoich potrzeb."
        },
        step12: {
            title: "Ochrona prywatności",
            description: "Twoje dane są chronione zgodnie z RODO. Nigdy nie udostępniamy twoich dokumentów stronom trzecim. Masz pełną kontrolę nad swoimi danymi."
        },
        cta: {
            title: "Gotowy zacząć?",
            description: "Zarejestruj się teraz i otrzymaj 7 dni bezpłatnego dostępu do wszystkich funkcji!",
            button: "Rozpocznij za darmo"
        }
    },
    en: {
        title: "How It Works",
        subtitle: "Simple guide to using the CODEX platform",
        step1: {
            title: "Registration and Login",
            description: "Create an account by entering your name, email, and password. Get 7 days of free access to all platform features."
        },
        step2: {
            title: "Upload Documents",
            description: "Upload your legal documents (contracts, lawsuits, court decisions) in PDF, DOCX format or images. The system will automatically process them using OCR."
        },
        step3: {
            title: "Automatic Classification",
            description: "AI automatically recognizes the document type and categorizes it (contract, lawsuit, court decision, etc.) for better organization."
        },
        step4: {
            title: "AI Legal Consultant",
            description: "Ask a question about your document or legal problem. AI analyzes the context and provides expert legal advice according to the law."
        },
        step5: {
            title: "Instant Answers",
            description: "Get answers to legal questions in seconds instead of hours waiting for a lawyer. AI works 24/7."
        },
        step6: {
            title: "Secure Storage",
            description: "All your documents are encrypted and securely stored in the cloud. You have access to them anytime, anywhere."
        },
        step7: {
            title: "Consultation History",
            description: "All conversations with AI are saved. You can return to previous consultations and answers at any time."
        },
        step8: {
            title: "Multilingual Support",
            description: "The platform supports Slovak, Czech, Polish, English, Ukrainian, Russian, German, French, Spanish, and Italian."
        },
        step9: {
            title: "Batch Processing",
            description: "Upload multiple documents at once. The system will process them all in parallel and prepare for analysis."
        },
        step10: {
            title: "AI Technical Support",
            description: "If you have a technical problem, click the blue 🔧 icon in the bottom right corner. AI will analyze your logs and help solve the problem."
        },
        step11: {
            title: "Choose Subscription",
            description: "After the 7-day trial period, choose monthly (€30), semi-annual (€80), or annual (€120) subscription according to your needs."
        },
        step12: {
            title: "Privacy Protection",
            description: "Your data is protected under GDPR. We never share your documents with third parties. You have full control over your data."
        },
        cta: {
            title: "Ready to Start?",
            description: "Register now and get 7 days of free access to all features!",
            button: "Start Free"
        }
    },
    uk: {
        title: "Як це працює",
        subtitle: "Простий посібник з використання платформи CODEX",
        step1: {
            title: "Реєстрація та вхід",
            description: "Створіть обліковий запис, вказавши ім'я, email та пароль. Отримайте 7 днів безкоштовного доступу до всіх функцій платформи."
        },
        step2: {
            title: "Завантаження документів",
            description: "Завантажте свої юридичні документи (договори, позови, судові рішення) у форматі PDF, DOCX або зображення. Система автоматично обробить їх за допомогою OCR."
        },
        step3: {
            title: "Автоматична класифікація",
            description: "AI автоматично розпізнає тип документа та категоризує його (договір, позов, судове рішення тощо) для кращої організації."
        },
        step4: {
            title: "AI юридичний консультант",
            description: "Поставте питання про ваш документ або юридичну проблему. AI проаналізує контекст та надасть експертну юридичну консультацію відповідно до законодавства."
        },
        step5: {
            title: "Миттєві відповіді",
            description: "Отримуйте відповіді на юридичні питання за секунди замість годин очікування на адвоката. AI працює 24/7."
        },
        step6: {
            title: "Безпечне зберігання",
            description: "Всі ваші документи зашифровані та безпечно зберігаються в хмарі. Ви маєте доступ до них завжди і всюди."
        },
        step7: {
            title: "Історія консультацій",
            description: "Всі розмови з AI зберігаються. Ви можете в будь-який час повернутися до попередніх консультацій та відповідей."
        },
        step8: {
            title: "Багатомовна підтримка",
            description: "Платформа підтримує словацьку, чеську, польську, англійську, українську, російську, німецьку, французьку, іспанську та італійську мови."
        },
        step9: {
            title: "Пакетна обробка",
            description: "Завантажте кілька документів одночасно. Система обробить їх усі паралельно та підготує до аналізу."
        },
        step10: {
            title: "Технічна підтримка AI",
            description: "Якщо у вас технічна проблема, натисніть синю іконку 🔧 у правому нижньому куті. AI проаналізує ваші логи та допоможе вирішити проблему."
        },
        step11: {
            title: "Вибір підписки",
            description: "Після закінчення 7-денного пробного періоду оберіть місячну (30€), піврічну (80€) або річну (120€) підписку відповідно до ваших потреб."
        },
        step12: {
            title: "Захист конфіденційності",
            description: "Ваші дані захищені відповідно до GDPR. Ми ніколи не передаємо ваші документи третім особам. Ви маєте повний контроль над своїми даними."
        },
        cta: {
            title: "Готові почати?",
            description: "Зареєструйтесь зараз і отримайте 7 днів безкоштовного доступу до всіх функцій!",
            button: "Почати безкоштовно"
        }
    },
    ru: {
        title: "Как это работает",
        subtitle: "Простое руководство по использованию платформы CODEX",
        step1: {
            title: "Регистрация и вход",
            description: "Создайте учетную запись, указав имя, email и пароль. Получите 7 дней бесплатного доступа ко всем функциям платформы."
        },
        step2: {
            title: "Загрузка документов",
            description: "Загрузите свои юридические документы (договоры, иски, судебные решения) в формате PDF, DOCX или изображения. Система автоматически обработает их с помощью OCR."
        },
        step3: {
            title: "Автоматическая классификация",
            description: "AI автоматически распознает тип документа и категоризирует его (договор, иск, судебное решение и т.д.) для лучшей организации."
        },
        step4: {
            title: "AI юридический консультант",
            description: "Задайте вопрос о вашем документе или юридической проблеме. AI проанализирует контекст и предоставит экспертную юридическую консультацию в соответствии с законодательством."
        },
        step5: {
            title: "Мгновенные ответы",
            description: "Получайте ответы на юридические вопросы за секунды вместо часов ожидания адвоката. AI работает 24/7."
        },
        step6: {
            title: "Безопасное хранение",
            description: "Все ваши документы зашифрованы и безопасно хранятся в облаке. У вас есть доступ к ним всегда и везде."
        },
        step7: {
            title: "История консультаций",
            description: "Все разговоры с AI сохраняются. Вы можете в любое время вернуться к предыдущим консультациям и ответам."
        },
        step8: {
            title: "Многоязычная поддержка",
            description: "Платформа поддерживает словацкий, чешский, польский, английский, украинский, русский, немецкий, французский, испанский и итальянский языки."
        },
        step9: {
            title: "Пакетная обработка",
            description: "Загрузите несколько документов одновременно. Система обработает их все параллельно и подготовит к анализу."
        },
        step10: {
            title: "Техническая поддержка AI",
            description: "Если у вас техническая проблема, нажмите синюю иконку 🔧 в правом нижнем углу. AI проанализирует ваши логи и поможет решить проблему."
        },
        step11: {
            title: "Выбор подписки",
            description: "После окончания 7-дневного пробного периода выберите месячную (30€), полугодовую (80€) или годовую (120€) подписку в соответствии с вашими потребностями."
        },
        step12: {
            title: "Защита конфиденциальности",
            description: "Ваши данные защищены в соответствии с GDPR. Мы никогда не передаем ваши документы третьим лицам. Вы имеете полный контроль над своими данными."
        },
        cta: {
            title: "Готовы начать?",
            description: "Зарегистрируйтесь сейчас и получите 7 дней бесплатного доступа ко всем функциям!",
            button: "Начать бесплатно"
        }
    },
    de: {
        title: "Wie es funktioniert",
        subtitle: "Einfache Anleitung zur Nutzung der CODEX-Plattform",
        step1: {
            title: "Registrierung und Anmeldung",
            description: "Erstellen Sie ein Konto, indem Sie Ihren Namen, E-Mail und Passwort eingeben. Erhalten Sie 7 Tage kostenlosen Zugang zu allen Plattformfunktionen."
        },
        step2: {
            title: "Dokumente hochladen",
            description: "Laden Sie Ihre Rechtsdokumente (Verträge, Klagen, Gerichtsentscheidungen) im PDF-, DOCX-Format oder als Bilder hoch. Das System verarbeitet sie automatisch mit OCR."
        },
        step3: {
            title: "Automatische Klassifizierung",
            description: "KI erkennt automatisch den Dokumenttyp und kategorisiert ihn (Vertrag, Klage, Gerichtsentscheidung usw.) für bessere Organisation."
        },
        step4: {
            title: "KI-Rechtsberater",
            description: "Stellen Sie eine Frage zu Ihrem Dokument oder rechtlichen Problem. KI analysiert den Kontext und bietet fachkundige Rechtsberatung gemäß dem Gesetz."
        },
        step5: {
            title: "Sofortige Antworten",
            description: "Erhalten Sie Antworten auf rechtliche Fragen in Sekunden statt Stunden Wartezeit auf einen Anwalt. KI arbeitet 24/7."
        },
        step6: {
            title: "Sichere Speicherung",
            description: "Alle Ihre Dokumente sind verschlüsselt und sicher in der Cloud gespeichert. Sie haben jederzeit und überall Zugriff darauf."
        },
        step7: {
            title: "Beratungshistorie",
            description: "Alle Gespräche mit KI werden gespeichert. Sie können jederzeit zu früheren Beratungen und Antworten zurückkehren."
        },
        step8: {
            title: "Mehrsprachige Unterstützung",
            description: "Die Plattform unterstützt Slowakisch, Tschechisch, Polnisch, Englisch, Ukrainisch, Russisch, Deutsch, Französisch, Spanisch und Italienisch."
        },
        step9: {
            title: "Stapelverarbeitung",
            description: "Laden Sie mehrere Dokumente gleichzeitig hoch. Das System verarbeitet sie alle parallel und bereitet sie zur Analyse vor."
        },
        step10: {
            title: "KI-Technischer Support",
            description: "Wenn Sie ein technisches Problem haben, klicken Sie auf das blaue 🔧-Symbol in der unteren rechten Ecke. KI analysiert Ihre Protokolle und hilft bei der Problemlösung."
        },
        step11: {
            title: "Abonnement wählen",
            description: "Nach der 7-tägigen Testphase wählen Sie ein monatliches (30€), halbjährliches (80€) oder jährliches (120€) Abonnement nach Ihren Bedürfnissen."
        },
        step12: {
            title: "Datenschutz",
            description: "Ihre Daten sind gemäß DSGVO geschützt. Wir geben Ihre Dokumente niemals an Dritte weiter. Sie haben die volle Kontrolle über Ihre Daten."
        },
        cta: {
            title: "Bereit anzufangen?",
            description: "Registrieren Sie sich jetzt und erhalten Sie 7 Tage kostenlosen Zugang zu allen Funktionen!",
            button: "Kostenlos starten"
        }
    },
    fr: {
        title: "Comment ça marche",
        subtitle: "Guide simple d'utilisation de la plateforme CODEX",
        step1: {
            title: "Inscription et connexion",
            description: "Créez un compte en saisissant votre nom, email et mot de passe. Obtenez 7 jours d'accès gratuit à toutes les fonctionnalités de la plateforme."
        },
        step2: {
            title: "Télécharger des documents",
            description: "Téléchargez vos documents juridiques (contrats, poursuites, décisions de justice) au format PDF, DOCX ou images. Le système les traitera automatiquement avec OCR."
        },
        step3: {
            title: "Classification automatique",
            description: "L'IA reconnaît automatiquement le type de document et le catégorise (contrat, poursuite, décision de justice, etc.) pour une meilleure organisation."
        },
        step4: {
            title: "Consultant juridique IA",
            description: "Posez une question sur votre document ou problème juridique. L'IA analyse le contexte et fournit des conseils juridiques experts selon la loi."
        },
        step5: {
            title: "Réponses instantanées",
            description: "Obtenez des réponses aux questions juridiques en secondes au lieu d'heures d'attente pour un avocat. L'IA fonctionne 24/7."
        },
        step6: {
            title: "Stockage sécurisé",
            description: "Tous vos documents sont cryptés et stockés en toute sécurité dans le cloud. Vous y avez accès à tout moment, n'importe où."
        },
        step7: {
            title: "Historique des consultations",
            description: "Toutes les conversations avec l'IA sont enregistrées. Vous pouvez revenir aux consultations et réponses précédentes à tout moment."
        },
        step8: {
            title: "Support multilingue",
            description: "La plateforme prend en charge le slovaque, le tchèque, le polonais, l'anglais, l'ukrainien, le russe, l'allemand, le français, l'espagnol et l'italien."
        },
        step9: {
            title: "Traitement par lots",
            description: "Téléchargez plusieurs documents à la fois. Le système les traitera tous en parallèle et les préparera pour l'analyse."
        },
        step10: {
            title: "Support technique IA",
            description: "Si vous avez un problème technique, cliquez sur l'icône bleue 🔧 dans le coin inférieur droit. L'IA analysera vos journaux et aidera à résoudre le problème."
        },
        step11: {
            title: "Choisir un abonnement",
            description: "Après la période d'essai de 7 jours, choisissez un abonnement mensuel (30€), semestriel (80€) ou annuel (120€) selon vos besoins."
        },
        step12: {
            title: "Protection de la vie privée",
            description: "Vos données sont protégées selon le RGPD. Nous ne partageons jamais vos documents avec des tiers. Vous avez un contrôle total sur vos données."
        },
        cta: {
            title: "Prêt à commencer?",
            description: "Inscrivez-vous maintenant et obtenez 7 jours d'accès gratuit à toutes les fonctionnalités!",
            button: "Commencer gratuitement"
        }
    },
    es: {
        title: "Cómo funciona",
        subtitle: "Guía simple para usar la plataforma CODEX",
        step1: {
            title: "Registro e inicio de sesión",
            description: "Cree una cuenta ingresando su nombre, correo electrónico y contraseña. Obtenga 7 días de acceso gratuito a todas las funciones de la plataforma."
        },
        step2: {
            title: "Subir documentos",
            description: "Suba sus documentos legales (contratos, demandas, decisiones judiciales) en formato PDF, DOCX o imágenes. El sistema los procesará automáticamente usando OCR."
        },
        step3: {
            title: "Clasificación automática",
            description: "La IA reconoce automáticamente el tipo de documento y lo categoriza (contrato, demanda, decisión judicial, etc.) para una mejor organización."
        },
        step4: {
            title: "Consultor legal IA",
            description: "Haga una pregunta sobre su documento o problema legal. La IA analiza el contexto y proporciona asesoramiento legal experto según la ley."
        },
        step5: {
            title: "Respuestas instantáneas",
            description: "Obtenga respuestas a preguntas legales en segundos en lugar de horas esperando a un abogado. La IA funciona 24/7."
        },
        step6: {
            title: "Almacenamiento seguro",
            description: "Todos sus documentos están encriptados y almacenados de forma segura en la nube. Tiene acceso a ellos en cualquier momento y lugar."
        },
        step7: {
            title: "Historial de consultas",
            description: "Todas las conversaciones con IA se guardan. Puede volver a consultas y respuestas anteriores en cualquier momento."
        },
        step8: {
            title: "Soporte multilingüe",
            description: "La plataforma admite eslovaco, checo, polaco, inglés, ucraniano, ruso, alemán, francés, español e italiano."
        },
        step9: {
            title: "Procesamiento por lotes",
            description: "Suba varios documentos a la vez. El sistema los procesará todos en paralelo y los preparará para el análisis."
        },
        step10: {
            title: "Soporte técnico IA",
            description: "Si tiene un problema técnico, haga clic en el icono azul 🔧 en la esquina inferior derecha. La IA analizará sus registros y ayudará a resolver el problema."
        },
        step11: {
            title: "Elegir suscripción",
            description: "Después del período de prueba de 7 días, elija una suscripción mensual (30€), semestral (80€) o anual (120€) según sus necesidades."
        },
        step12: {
            title: "Protección de privacidad",
            description: "Sus datos están protegidos según GDPR. Nunca compartimos sus documentos con terceros. Tiene control total sobre sus datos."
        },
        cta: {
            title: "¿Listo para comenzar?",
            description: "¡Regístrese ahora y obtenga 7 días de acceso gratuito a todas las funciones!",
            button: "Comenzar gratis"
        }
    },
    it: {
        title: "Come funziona",
        subtitle: "Guida semplice all'uso della piattaforma CODEX",
        step1: {
            title: "Registrazione e accesso",
            description: "Crea un account inserendo nome, email e password. Ottieni 7 giorni di accesso gratuito a tutte le funzionalità della piattaforma."
        },
        step2: {
            title: "Carica documenti",
            description: "Carica i tuoi documenti legali (contratti, cause, decisioni giudiziarie) in formato PDF, DOCX o immagini. Il sistema li elaborerà automaticamente usando OCR."
        },
        step3: {
            title: "Classificazione automatica",
            description: "L'IA riconosce automaticamente il tipo di documento e lo categorizza (contratto, causa, decisione giudiziaria, ecc.) per una migliore organizzazione."
        },
        step4: {
            title: "Consulente legale IA",
            description: "Fai una domanda sul tuo documento o problema legale. L'IA analizza il contesto e fornisce consulenza legale esperta secondo la legge."
        },
        step5: {
            title: "Risposte istantanee",
            description: "Ottieni risposte a domande legali in secondi invece di ore di attesa per un avvocato. L'IA funziona 24/7."
        },
        step6: {
            title: "Archiviazione sicura",
            description: "Tutti i tuoi documenti sono crittografati e archiviati in modo sicuro nel cloud. Hai accesso ad essi sempre e ovunque."
        },
        step7: {
            title: "Cronologia consultazioni",
            description: "Tutte le conversazioni con l'IA vengono salvate. Puoi tornare a consultazioni e risposte precedenti in qualsiasi momento."
        },
        step8: {
            title: "Supporto multilingue",
            description: "La piattaforma supporta slovacco, ceco, polacco, inglese, ucraino, russo, tedesco, francese, spagnolo e italiano."
        },
        step9: {
            title: "Elaborazione batch",
            description: "Carica più documenti contemporaneamente. Il sistema li elaborerà tutti in parallelo e li preparerà per l'analisi."
        },
        step10: {
            title: "Supporto tecnico IA",
            description: "Se hai un problema tecnico, fai clic sull'icona blu 🔧 nell'angolo in basso a destra. L'IA analizzerà i tuoi log e aiuterà a risolvere il problema."
        },
        step11: {
            title: "Scegli abbonamento",
            description: "Dopo il periodo di prova di 7 giorni, scegli un abbonamento mensile (30€), semestrale (80€) o annuale (120€) secondo le tue esigenze."
        },
        step12: {
            title: "Protezione privacy",
            description: "I tuoi dati sono protetti secondo GDPR. Non condividiamo mai i tuoi documenti con terze parti. Hai il pieno controllo sui tuoi dati."
        },
        cta: {
            title: "Pronto per iniziare?",
            description: "Registrati ora e ottieni 7 giorni di accesso gratuito a tutte le funzionalità!",
            button: "Inizia gratis"
        }
    }
};

Object.keys(howItWorksTranslations).forEach(lang => {
    const filePath = path.join(__dirname, 'locales', lang, 'common.json');
    try {
        const content = JSON.parse(fs.readFileSync(filePath, 'utf8'));
        content.howItWorks = howItWorksTranslations[lang];
        fs.writeFileSync(filePath, JSON.stringify(content, null, 4), 'utf8');
        console.log(`✅ Added howItWorks to ${lang}/common.json`);
    } catch (error) {
        console.error(`❌ Error: ${lang} - ${error.message}`);
    }
});

console.log('\n✅ All translations added!');
