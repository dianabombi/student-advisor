'use client';

import { ArrowLeft } from 'lucide-react';
import Link from 'next/link';
import { useLanguage } from '@/lib/LanguageContext';

export default function TermsOfServicePage() {
    const { t, language } = useLanguage();

    // Translations for STUDENT educational platform
    const getContent = () => {
        const translations: Record<string, any> = {
            sk: {
                title: 'Podmienky používania',
                back: 'Späť',
                intro: 'Vitajte na vzdelávacej platforme Student Advisor. Tieto Podmienky používania upravujú váš prístup a používanie našich vzdelávacích služieb.',
                noAdvice: 'Student Advisor je vzdelávacia platforma a neposkytuje profesionálne poradenstvo.',
                sections: [
                    { title: '1. Úvod', content: 'Používaním našich služieb súhlasíte s týmito Podmienkami. Student Advisor je vzdelávacia platforma určená na pomoc študentom pri hľadaní vzdelávacích príležitostí.' },
                    { title: '2. Služby', content: 'Student Advisor poskytuje informácie o univerzitách, jazykových školách, odborných školách a iných vzdelávacích inštitúciách. Platforma zahŕňa AI asistenta pre všeobecné vzdelávacie informácie a vyhľadávanie ubytovania pre študentov.' },
                    { title: '3. Povinnosti používateľa', content: 'Používateľ sa zaväzuje používať služby v súlade so zákonom, poskytovať pravdivé informácie a chrániť svoje prihlasovacie údaje. Používateľ je zodpovedný za overenie informácií poskytnutých platformou priamo u vzdelávacích inštitúcií.' },
                    { title: '4. Obmedzenie zodpovednosti', content: 'Student Advisor poskytuje informácie na vzdelávacie účely. Neposkytujeme žiadne záruky ohľadom presnosti informácií o vzdelávacích inštitúciách. Používateľ je zodpovedný za overenie všetkých informácií priamo u príslušných inštitúcií.' },
                    { title: '5. Predplatné', content: '7-dňová bezplatná skúšobná verzia, potom mesačné predplatné. Predplatné možno kedykoľvek zrušiť.' },
                    { title: '6. Ochrana osobných údajov', content: 'Spracovanie osobných údajov sa riadi našimi Zásadami ochrany osobných údajov a platnou legislatívou GDPR.' },
                    { title: '7. Rozhodné právo', content: 'Tieto Podmienky sa riadia právom Slovenskej republiky.' }
                ]
            },
            cs: {
                title: 'Podmínky používání',
                back: 'Zpět',
                intro: 'Vítejte na vzdělávací platformě Student Advisor. Tyto Podmínky používání upravují váš přístup a používání našich vzdělávacích služeb.',
                noAdvice: 'Student Advisor je vzdělávací platforma a neposkytuje profesionální poradenství.',
                sections: [
                    { title: '1. Úvod', content: 'Používáním našich služeb souhlasíte s těmito Podmínkami. Student Advisor je vzdělávací platforma určená k pomoci studentům při hledání vzdělávacích příležitostí.' },
                    { title: '2. Služby', content: 'Student Advisor poskytuje informace o univerzitách, jazykových školách, odborných školách a dalších vzdělávacích institucích. Platforma zahrnuje AI asistenta pro všeobecné vzdělávací informace a vyhledávání ubytování pro studenty.' },
                    { title: '3. Povinnosti uživatele', content: 'Uživatel se zavazuje používat služby v souladu se zákonem, poskytovat pravdivé informace a chránit své přihlašovací údaje. Uživatel je zodpovědný za ověření informací poskytnutých platformou přímo u vzdělávacích institucí.' },
                    { title: '4. Omezení odpovědnosti', content: 'Student Advisor poskytuje informace pro vzdělávací účely. Neposkytujeme žádné záruky ohledně přesnosti informací o vzdělávacích institucích. Uživatel je zodpovědný za ověření všech informací přímo u příslušných institucí.' },
                    { title: '5. Předplatné', content: '7denní bezplatná zkušební verze, poté měsíční předplatné. Předplatné lze kdykoli zrušit.' },
                    { title: '6. Ochrana osobních údajů', content: 'Zpracování osobních údajů se řídí našimi Zásadami ochrany osobních údajů a platnou legislativou GDPR.' },
                    { title: '7. Rozhodné právo', content: 'Tyto Podmínky se řídí právem České republiky.' }
                ]
            },
            en: {
                title: 'Terms of Service',
                back: 'Back',
                intro: 'Welcome to Student Advisor educational platform. These Terms of Service govern your access and use of our educational services.',
                noAdvice: 'Student Advisor is an educational platform and does not provide professional advice.',
                sections: [
                    { title: '1. Introduction', content: 'By using our services, you agree to these Terms. Student Advisor is an educational platform designed to help students find educational opportunities.' },
                    { title: '2. Services', content: 'Student Advisor provides information about universities, language schools, vocational schools, and other educational institutions. The platform includes an AI assistant for general educational information and student housing search.' },
                    { title: '3. User Obligations', content: 'User agrees to use services in accordance with the law, provide truthful information, and protect their login credentials. User is responsible for verifying information provided by the platform directly with educational institutions.' },
                    { title: '4. Limitation of Liability', content: 'Student Advisor provides information for educational purposes. We provide no warranties regarding the accuracy of information about educational institutions. User is responsible for verifying all information directly with the relevant institutions.' },
                    { title: '5. Subscription', content: '7-day free trial, then monthly subscription. Subscription can be cancelled at any time.' },
                    { title: '6. Privacy', content: 'Processing of personal data is governed by our Privacy Policy and applicable GDPR legislation.' },
                    { title: '7. Governing Law', content: 'These Terms are governed by the law of the jurisdiction you selected.' }
                ]
            },
            uk: {
                title: 'Умови використання',
                back: 'Назад',
                intro: 'Ласкаво просимо на освітню платформу Student Advisor. Ці Умови використання регулюють ваш доступ та використання наших освітніх послуг.',
                noAdvice: 'Student Advisor є освітньою платформою і не надає професійних консультацій.',
                sections: [
                    { title: '1. Вступ', content: 'Використовуючи наші послуги, ви погоджуєтесь з цими Умовами. Student Advisor - це освітня платформа, призначена для допомоги студентам у пошуку освітніх можливостей.' },
                    { title: '2. Послуги', content: 'Student Advisor надає інформацію про університети, мовні школи, професійні школи та інші освітні заклади. Платформа включає AI-асистента для загальної освітньої інформації та пошуку житла для студентів.' },
                    { title: '3. Обов\'язки користувача', content: 'Користувач зобов\'язується використовувати послуги відповідно до закону, надавати правдиву інформацію та захищати свої облікові дані. Користувач несе відповідальність за перевірку інформації, наданої платформою, безпосередньо в освітніх закладах.' },
                    { title: '4. Обмеження відповідальності', content: 'Student Advisor надає інформацію для освітніх цілей. Ми не надаємо жодних гарантій щодо точності інформації про освітні заклади. Користувач несе відповідальність за перевірку всієї інформації безпосередньо у відповідних закладах.' },
                    { title: '5. Підписка', content: '7-денна безкоштовна пробна версія, потім місячна підписка. Підписку можна скасувати в будь-який час.' },
                    { title: '6. Конфіденційність', content: 'Обробка персональних даних регулюється нашою Політикою конфіденційності та чинним законодавством GDPR.' },
                    { title: '7. Застосовне право', content: 'Ці Умови регулюються законодавством обраної вами юрисдикції.' }
                ]
            },
            pl: {
                title: 'Warunki korzystania',
                back: 'Wstecz',
                intro: 'Witamy na platformie edukacyjnej Student Advisor. Niniejsze Warunki korzystania regulują Państwa dostęp i korzystanie z naszych usług edukacyjnych.',
                noAdvice: 'Student Advisor jest platformą edukacyjną i nie świadczy profesjonalnych porad.',
                sections: [
                    { title: '1. Wstęp', content: 'Korzystając z naszych usług, zgadzają się Państwo na niniejsze Warunki. Student Advisor to platforma edukacyjna zaprojektowana, aby pomóc studentom w znalezieniu możliwości edukacyjnych.' },
                    { title: '2. Usługi', content: 'Student Advisor dostarcza informacji o uniwersytetach, szkołach językowych, szkołach zawodowych i innych instytucjach edukacyjnych. Platforma zawiera asystenta AI do ogólnych informacji edukacyjnych i wyszukiwania zakwaterowania dla studentów.' },
                    { title: '3. Obowiązki użytkownika', content: 'Użytkownik zobowiązuje się korzystać z usług zgodnie z prawem, dostarczać prawdziwych informacji i chronić swoje dane logowania. Użytkownik jest odpowiedzialny za weryfikację informacji dostarczonych przez platformę bezpośrednio w instytucjach edukacyjnych.' },
                    { title: '4. Ograniczenie odpowiedzialności', content: 'Student Advisor dostarcza informacji w celach edukacyjnych. Nie udzielamy żadnych gwarancji dotyczących dokładności informacji o instytucjach edukacyjnych. Użytkownik jest odpowiedzialny za weryfikację wszystkich informacji bezpośrednio w odpowiednich instytucjach.' },
                    { title: '5. Subskrypcja', content: '7-dniowa bezpłatna wersja próbna, następnie miesięczna subskrypcja. Subskrypcję można anulować w dowolnym momencie.' },
                    { title: '6. Prywatność', content: 'Przetwarzanie danych osobowych regulowane jest naszą Polityką Prywatności i obowiązującym prawem GDPR.' },
                    { title: '7. Prawo właściwe', content: 'Niniejsze Warunki podlegają prawu wybranej jurysdykcji.' }
                ]
            },
            de: {
                title: 'Nutzungsbedingungen',
                back: 'Zurück',
                intro: 'Willkommen auf der Bildungsplattform Student Advisor. Diese Nutzungsbedingungen regeln Ihren Zugang und die Nutzung unserer Bildungsdienste.',
                noAdvice: 'Student Advisor ist eine Bildungsplattform und bietet keine professionelle Beratung an.',
                sections: [
                    { title: '1. Einleitung', content: 'Durch die Nutzung unserer Dienste stimmen Sie diesen Bedingungen zu. Student Advisor ist eine Bildungsplattform, die Studenten bei der Suche nach Bildungsmöglichkeiten unterstützt.' },
                    { title: '2. Dienste', content: 'Student Advisor bietet Informationen über Universitäten, Sprachschulen, Berufsschulen und andere Bildungseinrichtungen. Die Plattform umfasst einen KI-Assistenten für allgemeine Bildungsinformationen und Wohnungssuche für Studenten.' },
                    { title: '3. Nutzerpflichten', content: 'Der Nutzer verpflichtet sich, die Dienste rechtskonform zu nutzen, wahrheitsgemäße Informationen bereitzustellen und seine Anmeldedaten zu schützen. Der Nutzer ist verantwortlich für die Überprüfung der von der Plattform bereitgestellten Informationen direkt bei den Bildungseinrichtungen.' },
                    { title: '4. Haftungsbeschränkung', content: 'Student Advisor stellt Informationen für Bildungszwecke bereit. Wir übernehmen keine Gewährleistung für die Richtigkeit der Informationen über Bildungseinrichtungen. Der Nutzer ist verantwortlich für die Überprüfung aller Informationen direkt bei den entsprechenden Einrichtungen.' },
                    { title: '5. Abonnement', content: '7-tägige kostenlose Testversion, dann monatliches Abonnement. Das Abonnement kann jederzeit gekündigt werden.' },
                    { title: '6. Datenschutz', content: 'Die Verarbeitung personenbezogener Daten richtet sich nach unserer Datenschutzerklärung und der geltenden GDPR-Gesetzgebung.' },
                    { title: '7. Anwendbares Recht', content: 'Diese Bedingungen unterliegen dem Recht der von Ihnen gewählten Rechtsordnung.' }
                ]
            },
            fr: {
                title: 'Conditions d\'utilisation',
                back: 'Retour',
                intro: 'Bienvenue sur la plateforme éducative Student Advisor. Ces Conditions d\'utilisation régissent votre accès et votre utilisation de nos services éducatifs.',
                noAdvice: 'Student Advisor est une plateforme éducative et ne fournit pas de conseils professionnels.',
                sections: [
                    { title: '1. Introduction', content: 'En utilisant nos services, vous acceptez ces Conditions. Student Advisor est une plateforme éducative conçue pour aider les étudiants à trouver des opportunités éducatives.' },
                    { title: '2. Services', content: 'Student Advisor fournit des informations sur les universités, les écoles de langues, les écoles professionnelles et autres établissements d\'enseignement. La plateforme comprend un assistant IA pour les informations éducatives générales et la recherche de logement étudiant.' },
                    { title: '3. Obligations de l\'utilisateur', content: 'L\'utilisateur s\'engage à utiliser les services conformément à la loi, à fournir des informations véridiques et à protéger ses identifiants de connexion. L\'utilisateur est responsable de la vérification des informations fournies par la plateforme directement auprès des établissements d\'enseignement.' },
                    { title: '4. Limitation de responsabilité', content: 'Student Advisor fournit des informations à des fins éducatives. Nous ne fournissons aucune garantie concernant l\'exactitude des informations sur les établissements d\'enseignement. L\'utilisateur est responsable de la vérification de toutes les informations directement auprès des établissements concernés.' },
                    { title: '5. Abonnement', content: 'Essai gratuit de 7 jours, puis abonnement mensuel. L\'abonnement peut être annulé à tout moment.' },
                    { title: '6. Confidentialité', content: 'Le traitement des données personnelles est régi par notre Politique de confidentialité et la législation RGPD applicable.' },
                    { title: '7. Droit applicable', content: 'Ces Conditions sont régies par le droit de la juridiction que vous avez sélectionnée.' }
                ]
            },
            es: {
                title: 'Términos de servicio',
                back: 'Atrás',
                intro: 'Bienvenido a la plataforma educativa Student Advisor. Estos Términos de servicio rigen su acceso y uso de nuestros servicios educativos.',
                noAdvice: 'Student Advisor es una plataforma educativa y no proporciona asesoramiento profesional.',
                sections: [
                    { title: '1. Introducción', content: 'Al utilizar nuestros servicios, acepta estos Términos. Student Advisor es una plataforma educativa diseñada para ayudar a los estudiantes a encontrar oportunidades educativas.' },
                    { title: '2. Servicios', content: 'Student Advisor proporciona información sobre universidades, escuelas de idiomas, escuelas profesionales y otras instituciones educativas. La plataforma incluye un asistente de IA para información educativa general y búsqueda de alojamiento estudiantil.' },
                    { title: '3. Obligaciones del usuario', content: 'El usuario se compromete a utilizar los servicios de conformidad con la ley, proporcionar información veraz y proteger sus credenciales de acceso. El usuario es responsable de verificar la información proporcionada por la plataforma directamente con las instituciones educativas.' },
                    { title: '4. Limitación de responsabilidad', content: 'Student Advisor proporciona información con fines educativos. No proporcionamos ninguna garantía sobre la exactitud de la información sobre instituciones educativas. El usuario es responsable de verificar toda la información directamente con las instituciones correspondientes.' },
                    { title: '5. Suscripción', content: 'Prueba gratuita de 7 días, luego suscripción mensual. La suscripción puede cancelarse en cualquier momento.' },
                    { title: '6. Privacidad', content: 'El tratamiento de datos personales se rige por nuestra Política de Privacidad y la legislación RGPD aplicable.' },
                    { title: '7. Ley aplicable', content: 'Estos Términos se rigen por la ley de la jurisdicción que seleccionó.' }
                ]
            },
            it: {
                title: 'Termini di servizio',
                back: 'Indietro',
                intro: 'Benvenuti sulla piattaforma educativa Student Advisor. Questi Termini di servizio regolano il vostro accesso e utilizzo dei nostri servizi educativi.',
                noAdvice: 'Student Advisor è una piattaforma educativa e non fornisce consulenza professionale.',
                sections: [
                    { title: '1. Introduzione', content: 'Utilizzando i nostri servizi, accettate questi Termini. Student Advisor è una piattaforma educativa progettata per aiutare gli studenti a trovare opportunità educative.' },
                    { title: '2. Servizi', content: 'Student Advisor fornisce informazioni su università, scuole di lingue, scuole professionali e altre istituzioni educative. La piattaforma include un assistente AI per informazioni educative generali e ricerca di alloggi per studenti.' },
                    { title: '3. Obblighi dell\'utente', content: 'L\'utente si impegna a utilizzare i servizi in conformità con la legge, fornire informazioni veritiere e proteggere le proprie credenziali di accesso. L\'utente è responsabile della verifica delle informazioni fornite dalla piattaforma direttamente presso le istituzioni educative.' },
                    { title: '4. Limitazione di responsabilità', content: 'Student Advisor fornisce informazioni a scopi educativi. Non forniamo alcuna garanzia riguardo all\'accuratezza delle informazioni sulle istituzioni educative. L\'utente è responsabile della verifica di tutte le informazioni direttamente presso le istituzioni pertinenti.' },
                    { title: '5. Abbonamento', content: 'Prova gratuita di 7 giorni, poi abbonamento mensile. L\'abbonamento può essere cancellato in qualsiasi momento.' },
                    { title: '6. Privacy', content: 'Il trattamento dei dati personali è regolato dalla nostra Informativa sulla privacy e dalla legislazione GDPR applicabile.' },
                    { title: '7. Legge applicabile', content: 'Questi Termini sono regolati dalla legge della giurisdizione selezionata.' }
                ]
            },
            ru: {
                title: 'Условия использования',
                back: 'Назад',
                intro: 'Добро пожаловать на образовательную платформу Student Advisor. Эти Условия использования регулируют ваш доступ и использование наших образовательных услуг.',
                noAdvice: 'Student Advisor является образовательной платформой и не предоставляет профессиональных консультаций.',
                sections: [
                    { title: '1. Введение', content: 'Используя наши услуги, вы соглашаетесь с этими Условиями. Student Advisor - это образовательная платформа, предназначенная для помощи студентам в поиске образовательных возможностей.' },
                    { title: '2. Услуги', content: 'Student Advisor предоставляет информацию об университетах, языковых школах, профессиональных школах и других образовательных учреждениях. Платформа включает AI-ассистента для общей образовательной информации и поиска жилья для студентов.' },
                    { title: '3. Обязанности пользователя', content: 'Пользователь обязуется использовать услуги в соответствии с законом, предоставлять правдивую информацию и защищать свои учетные данные. Пользователь несет ответственность за проверку информации, предоставленной платформой, непосредственно в образовательных учреждениях.' },
                    { title: '4. Ограничение ответственности', content: 'Student Advisor предоставляет информацию в образовательных целях. Мы не предоставляем никаких гарантий относительно точности информации об образовательных учреждениях. Пользователь несет ответственность за проверку всей информации непосредственно в соответствующих учреждениях.' },
                    { title: '5. Подписка', content: '7-дневная бесплатная пробная версия, затем месячная подписка. Подписку можно отменить в любое время.' },
                    { title: '6. Конфиденциальность', content: 'Обработка персональных данных регулируется нашей Политикой конфиденциальности и действующим законодательством GDPR.' },
                    { title: '7. Применимое право', content: 'Эти Условия регулируются законодательством выбранной вами юрисдикции.' }
                ]
            }
        };

        return translations[language] || translations['en'];
    };

    const content = getContent();

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
                        {/* Introduction */}
                        <section className="mb-8">
                            <p className="text-gray-300 leading-relaxed mb-4 text-lg">
                                {content.intro}
                            </p>
                        </section>

                        {/* Critical Warning - Educational Platform */}
                        <section className="mb-8 bg-blue-500/10 border-2 border-blue-500/50 rounded-xl p-6">
                            <h2 className="text-2xl font-bold text-blue-300 mb-4">
                                ℹ️ {content.noAdvice}
                            </h2>
                            <p className="text-gray-200 leading-relaxed">
                                {language === 'sk' && 'Všetky informácie poskytované Student Advisor sú určené výlučne na všeobecné vzdelávacie účely. Pre konkrétne informácie o prijímacom konaní, štúdiu alebo ubytovaní sa obráťte priamo na príslušnú vzdelávaciu inštitúciu.'}
                                {language === 'cs' && 'Všechny informace poskytované Student Advisor jsou určeny výhradně pro všeobecné vzdělávací účely. Pro konkrétní informace o přijímacím řízení, studiu nebo ubytování se obraťte přímo na příslušnou vzdělávací instituci.'}
                                {language === 'pl' && 'Wszystkie informacje dostarczane przez Student Advisor są przeznaczone wyłącznie do ogólnych celów edukacyjnych. W sprawie konkretnych informacji o rekrutacji, studiach lub zakwaterowaniu należy skontaktować się bezpośrednio z odpowiednią instytucją edukacyjną.'}
                                {language === 'en' && 'All information provided by Student Advisor is intended solely for general educational purposes. For specific information about admissions, studies, or accommodation, contact the relevant educational institution directly.'}
                                {language === 'de' && 'Alle von Student Advisor bereitgestellten Informationen dienen ausschließlich allgemeinen Bildungszwecken. Für spezifische Informationen über Zulassungen, Studium oder Unterkunft wenden Sie sich bitte direkt an die entsprechende Bildungseinrichtung.'}
                                {language === 'uk' && 'Вся інформація, надана Student Advisor, призначена виключно для загальних освітніх цілей. Для конкретної інформації про вступ, навчання або проживання зверніться безпосередньо до відповідного навчального закладу.'}
                                {language === 'it' && 'Tutte le informazioni fornite da Student Advisor sono destinate esclusivamente a scopi educativi generali. Per informazioni specifiche su ammissioni, studi o alloggio, contattare direttamente l\'istituzione educativa pertinente.'}
                                {language === 'fr' && 'Toutes les informations fournies par Student Advisor sont destinées uniquement à des fins éducatives générales. Pour des informations spécifiques sur les admissions, les études ou le logement, contactez directement l\'établissement d\'enseignement concerné.'}
                                {language === 'es' && 'Toda la información proporcionada por Student Advisor está destinada únicamente a fines educativos generales. Para información específica sobre admisiones, estudios o alojamiento, contacte directamente con la institución educativa correspondiente.'}
                                {language === 'ru' && 'Вся информация, предоставляемая Student Advisor, предназначена исключительно для общих образовательных целей. Для конкретной информации о поступлении, обучении или проживании обращайтесь непосредственно в соответствующее образовательное учреждение.'}
                            </p>
                        </section>

                        {/* Sections */}
                        {content.sections.map((section: any, index: number) => (
                            <section key={index} className="mb-8">
                                <h2 className="text-2xl font-bold text-white mb-4">{section.title}</h2>
                                <p className="text-gray-300 leading-relaxed">
                                    {section.content}
                                </p>
                            </section>
                        ))}

                        {/* Footer */}
                        <div className="mt-12 pt-8 border-t border-white/20">
                            <p className="text-gray-400 text-sm">
                                {language === 'sk' && 'Posledná aktualizácia: 11. január 2026'}
                                {language === 'cs' && 'Poslední aktualizace: 11. leden 2026'}
                                {language === 'pl' && 'Ostatnia aktualizacja: 11 stycznia 2026'}
                                {language === 'en' && 'Last updated: January 11, 2026'}
                                {language === 'de' && 'Letzte Aktualisierung: 11. Januar 2026'}
                                {language === 'uk' && 'Остання актуалізація: 11 січня 2026'}
                                {language === 'it' && 'Ultimo aggiornamento: 11 gennaio 2026'}
                                {language === 'fr' && 'Dernière mise à jour: 11 janvier 2026'}
                                {language === 'es' && 'Última actualización: 11 de enero de 2026'}
                                {language === 'ru' && 'Последнее обновление: 11 января 2026'}
                                <br />
                                {language === 'sk' && 'Verzia: 2.0 (Student Platform)'}
                                {language === 'cs' && 'Verze: 2.0 (Student Platform)'}
                                {language === 'pl' && 'Wersja: 2.0 (Student Platform)'}
                                {language === 'en' && 'Version: 2.0 (Student Platform)'}
                                {language === 'de' && 'Version: 2.0 (Student Platform)'}
                                {language === 'uk' && 'Версія: 2.0 (Student Platform)'}
                                {language === 'it' && 'Versione: 2.0 (Student Platform)'}
                                {language === 'fr' && 'Version: 2.0 (Student Platform)'}
                                {language === 'es' && 'Versión: 2.0 (Student Platform)'}
                                {language === 'ru' && 'Версия: 2.0 (Student Platform)'}
                                <br />
                                {language === 'sk' && 'Kontakt: info@student-advisor.com'}
                                {language === 'cs' && 'Kontakt: info@student-advisor.com'}
                                {language === 'pl' && 'Kontakt: info@student-advisor.com'}
                                {language === 'en' && 'Contact: info@student-advisor.com'}
                                {language === 'de' && 'Kontakt: info@student-advisor.com'}
                                {language === 'uk' && 'Контакт: info@student-advisor.com'}
                                {language === 'it' && 'Contatto: info@student-advisor.com'}
                                {language === 'fr' && 'Contact: info@student-advisor.com'}
                                {language === 'es' && 'Contacto: info@student-advisor.com'}
                                {language === 'ru' && 'Контакт: info@student-advisor.com'}
                            </p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}
