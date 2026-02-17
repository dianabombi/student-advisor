#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Clean legal content and adapt for educational platform
All 10 languages
"""

import json
import os

languages = ['sk', 'en', 'uk', 'cs', 'pl', 'de', 'fr', 'es', 'it', 'ru']

# New educational content for all languages
educational_content = {
    'sk': {
        'landing_description': 'Objavte univerzity, porovnajte študijné programy a získajte personalizované poradenstvo pre vaše vzdelávanie. Student Advisor vám pomôže nájsť ideálnu školu.',
        'upload_title': 'Nahrať Dokumenty',
        'upload_description': 'Nahrajte svoje akademické dokumenty, vysvedčenia alebo prihlášky',
        'ai_title': 'Študentský Poradca',
        'ai_welcome': 'Ahoj! Som váš študentský poradca. Môžem vám pomôcť s výberom univerzity, požiadavkami na prijatie a študijnými programami.',
        'chat_welcome': 'Vitajte v Student Advisor',
        'chat_welcomeDesc': 'Opýtajte sa ma na čokoľvek o univerzitách, študijných programoch alebo procese prijímania.',
        'dashboard_upload_title': 'Hľadať Univerzity',
        'dashboard_upload_desc': 'Preskúmajte a porovnajte univerzity z celého sveta',
        'dashboard_declaration_title': 'Sledovať Prihlášky',
        'dashboard_declaration_desc': 'Spravujte svoje univerzitné prihlášky a termíny',
        'dashboard_chat_title': 'Študentský Poradca',
        'dashboard_chat_desc': 'Získajte rady o vzdelávaní a odpovede na vaše otázky'
    },
    'en': {
        'landing_description': 'Discover universities, compare study programs, and get personalized guidance for your education. Student Advisor helps you find your ideal school.',
        'upload_title': 'Upload Documents',
        'upload_description': 'Upload your academic documents, transcripts, or applications',
        'ai_title': 'Student Advisor',
        'ai_welcome': 'Hello! I\'m your student advisor. I can help you with university selection, admission requirements, and study programs.',
        'chat_welcome': 'Welcome to Student Advisor',
        'chat_welcomeDesc': 'Ask me anything about universities, study programs, or the admission process.',
        'dashboard_upload_title': 'Search Universities',
        'dashboard_upload_desc': 'Explore and compare universities from around the world',
        'dashboard_declaration_title': 'Track Applications',
        'dashboard_declaration_desc': 'Manage your university applications and deadlines',
        'dashboard_chat_title': 'Student Advisor',
        'dashboard_chat_desc': 'Get educational guidance and answers to your questions'
    },
    'uk': {
        'landing_description': 'Відкрийте університети, порівняйте навчальні програми та отримайте персоналізовані поради для вашої освіти. Student Advisor допоможе вам знайти ідеальну школу.',
        'upload_title': 'Завантажити Документи',
        'upload_description': 'Завантажте свої академічні документи, атестати або заявки',
        'ai_title': 'Студентський Консультант',
        'ai_welcome': 'Привіт! Я ваш студентський консультант. Можу допомогти з вибором університету, вимогами до вступу та навчальними програмами.',
        'chat_welcome': 'Ласкаво просимо до Student Advisor',
        'chat_welcomeDesc': 'Запитайте мене про університети, навчальні програми або процес вступу.',
        'dashboard_upload_title': 'Шукати Університети',
        'dashboard_upload_desc': 'Досліджуйте та порівнюйте університети з усього світу',
        'dashboard_declaration_title': 'Відстежувати Заявки',
        'dashboard_declaration_desc': 'Керуйте своїми університетськими заявками та термінами',
        'dashboard_chat_title': 'Студентський Консультант',
        'dashboard_chat_desc': 'Отримайте освітні поради та відповіді на ваші питання'
    },
    'cs': {
        'landing_description': 'Objevte univerzity, porovnejte studijní programy a získejte personalizované poradenství pro vaše vzdělání. Student Advisor vám pomůže najít ideální školu.',
        'upload_title': 'Nahrát Dokumenty',
        'upload_description': 'Nahrajte své akademické dokumenty, vysvědčení nebo přihlášky',
        'ai_title': 'Studentský Poradce',
        'ai_welcome': 'Ahoj! Jsem váš studentský poradce. Mohu vám pomoci s výběrem univerzity, požadavky na přijetí a studijními programy.',
        'chat_welcome': 'Vítejte v Student Advisor',
        'chat_welcomeDesc': 'Zeptejte se mě na cokoliv o univerzitách, studijních programech nebo procesu přijímání.',
        'dashboard_upload_title': 'Hledat Univerzity',
        'dashboard_upload_desc': 'Prozkoumejte a porovnejte univerzity z celého světa',
        'dashboard_declaration_title': 'Sledovat Přihlášky',
        'dashboard_declaration_desc': 'Spravujte své univerzitní přihlášky a termíny',
        'dashboard_chat_title': 'Studentský Poradce',
        'dashboard_chat_desc': 'Získejte vzdělávací rady a odpovědi na vaše otázky'
    },
    'pl': {
        'landing_description': 'Odkryj uniwersytety, porównaj programy studiów i uzyskaj spersonalizowane porady dotyczące edukacji. Student Advisor pomoże Ci znaleźć idealną szkołę.',
        'upload_title': 'Prześlij Dokumenty',
        'upload_description': 'Prześlij swoje dokumenty akademickie, świadectwa lub aplikacje',
        'ai_title': 'Doradca Studencki',
        'ai_welcome': 'Cześć! Jestem twoim doradcą studenckim. Mogę pomóc w wyborze uniwersytetu, wymaganiach przyjęcia i programach studiów.',
        'chat_welcome': 'Witamy w Student Advisor',
        'chat_welcomeDesc': 'Zapytaj mnie o wszystko dotyczące uniwersytetów, programów studiów lub procesu przyjęcia.',
        'dashboard_upload_title': 'Szukaj Uniwersytetów',
        'dashboard_upload_desc': 'Odkrywaj i porównuj uniwersytety z całego świata',
        'dashboard_declaration_title': 'Śledź Aplikacje',
        'dashboard_declaration_desc': 'Zarządzaj swoimi aplikacjami uniwersyteckimi i terminami',
        'dashboard_chat_title': 'Doradca Studencki',
        'dashboard_chat_desc': 'Uzyskaj porady edukacyjne i odpowiedzi na pytania'
    },
    'de': {
        'landing_description': 'Entdecken Sie Universitäten, vergleichen Sie Studienprogramme und erhalten Sie personalisierte Beratung für Ihre Ausbildung. Student Advisor hilft Ihnen, Ihre ideale Schule zu finden.',
        'upload_title': 'Dokumente Hochladen',
        'upload_description': 'Laden Sie Ihre akademischen Dokumente, Zeugnisse oder Bewerbungen hoch',
        'ai_title': 'Studentenberater',
        'ai_welcome': 'Hallo! Ich bin Ihr Studentenberater. Ich kann Ihnen bei der Universitätswahl, Zulassungsvoraussetzungen und Studienprogrammen helfen.',
        'chat_welcome': 'Willkommen bei Student Advisor',
        'chat_welcomeDesc': 'Fragen Sie mich alles über Universitäten, Studienprogramme oder den Zulassungsprozess.',
        'dashboard_upload_title': 'Universitäten Suchen',
        'dashboard_upload_desc': 'Erkunden und vergleichen Sie Universitäten aus der ganzen Welt',
        'dashboard_declaration_title': 'Bewerbungen Verfolgen',
        'dashboard_declaration_desc': 'Verwalten Sie Ihre Universitätsbewerbungen und Fristen',
        'dashboard_chat_title': 'Studentenberater',
        'dashboard_chat_desc': 'Erhalten Sie Bildungsberatung und Antworten auf Ihre Fragen'
    },
    'fr': {
        'landing_description': 'Découvrez des universités, comparez des programmes d\'études et obtenez des conseils personnalisés pour votre éducation. Student Advisor vous aide à trouver votre école idéale.',
        'upload_title': 'Télécharger des Documents',
        'upload_description': 'Téléchargez vos documents académiques, relevés de notes ou candidatures',
        'ai_title': 'Conseiller Étudiant',
        'ai_welcome': 'Bonjour! Je suis votre conseiller étudiant. Je peux vous aider avec le choix d\'université, les exigences d\'admission et les programmes d\'études.',
        'chat_welcome': 'Bienvenue sur Student Advisor',
        'chat_welcomeDesc': 'Posez-moi des questions sur les universités, les programmes d\'études ou le processus d\'admission.',
        'dashboard_upload_title': 'Rechercher des Universités',
        'dashboard_upload_desc': 'Explorez et comparez des universités du monde entier',
        'dashboard_declaration_title': 'Suivre les Candidatures',
        'dashboard_declaration_desc': 'Gérez vos candidatures universitaires et délais',
        'dashboard_chat_title': 'Conseiller Étudiant',
        'dashboard_chat_desc': 'Obtenez des conseils éducatifs et des réponses à vos questions'
    },
    'es': {
        'landing_description': 'Descubre universidades, compara programas de estudio y obtén orientación personalizada para tu educación. Student Advisor te ayuda a encontrar tu escuela ideal.',
        'upload_title': 'Subir Documentos',
        'upload_description': 'Sube tus documentos académicos, transcripciones o solicitudes',
        'ai_title': 'Asesor Estudiantil',
        'ai_welcome': '¡Hola! Soy tu asesor estudiantil. Puedo ayudarte con la selección de universidad, requisitos de admisión y programas de estudio.',
        'chat_welcome': 'Bienvenido a Student Advisor',
        'chat_welcomeDesc': 'Pregúntame sobre universidades, programas de estudio o el proceso de admisión.',
        'dashboard_upload_title': 'Buscar Universidades',
        'dashboard_upload_desc': 'Explora y compara universidades de todo el mundo',
        'dashboard_declaration_title': 'Seguir Solicitudes',
        'dashboard_declaration_desc': 'Gestiona tus solicitudes universitarias y plazos',
        'dashboard_chat_title': 'Asesor Estudiantil',
        'dashboard_chat_desc': 'Obtén orientación educativa y respuestas a tus preguntas'
    },
    'it': {
        'landing_description': 'Scopri università, confronta programmi di studio e ottieni consulenza personalizzata per la tua istruzione. Student Advisor ti aiuta a trovare la scuola ideale.',
        'upload_title': 'Carica Documenti',
        'upload_description': 'Carica i tuoi documenti accademici, certificati o domande',
        'ai_title': 'Consulente Studentesco',
        'ai_welcome': 'Ciao! Sono il tuo consulente studentesco. Posso aiutarti con la selezione dell\'università, i requisiti di ammissione e i programmi di studio.',
        'chat_welcome': 'Benvenuto su Student Advisor',
        'chat_welcomeDesc': 'Chiedimi qualsiasi cosa su università, programmi di studio o processo di ammissione.',
        'dashboard_upload_title': 'Cerca Università',
        'dashboard_upload_desc': 'Esplora e confronta università da tutto il mondo',
        'dashboard_declaration_title': 'Traccia Domande',
        'dashboard_declaration_desc': 'Gestisci le tue domande universitarie e scadenze',
        'dashboard_chat_title': 'Consulente Studentesco',
        'dashboard_chat_desc': 'Ottieni consulenza educativa e risposte alle tue domande'
    },
    'ru': {
        'landing_description': 'Откройте для себя университеты, сравните учебные программы и получите персонализированные советы для вашего образования. Student Advisor поможет вам найти идеальную школу.',
        'upload_title': 'Загрузить Документы',
        'upload_description': 'Загрузите свои академические документы, аттестаты или заявки',
        'ai_title': 'Студенческий Консультант',
        'ai_welcome': 'Привет! Я ваш студенческий консультант. Могу помочь с выбором университета, требованиями к поступлению и учебными программами.',
        'chat_welcome': 'Добро пожаловать в Student Advisor',
        'chat_welcomeDesc': 'Спросите меня о университетах, учебных программах или процессе поступления.',
        'dashboard_upload_title': 'Искать Университеты',
        'dashboard_upload_desc': 'Исследуйте и сравнивайте университеты со всего мира',
        'dashboard_declaration_title': 'Отслеживать Заявки',
        'dashboard_declaration_desc': 'Управляйте своими университетскими заявками и сроками',
        'dashboard_chat_title': 'Студенческий Консультант',
        'dashboard_chat_desc': 'Получите образовательные советы и ответы на вопросы'
    }
}

base_path = 'C:/Users/info/OneDrive/Dokumenty/Student/frontend/locales'

for lang in languages:
    file_path = f'{base_path}/{lang}/common.json'
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        content = educational_content[lang]
        
        # Update landing description
        if 'landing' in data:
            data['landing']['description'] = content['landing_description']
        
        # Update upload section
        if 'upload' in data:
            data['upload']['title'] = content['upload_title']
            data['upload']['description'] = content['upload_description']
        
        # Update AI section
        if 'ai' in data:
            data['ai']['title'] = content['ai_title']
            data['ai']['welcome'] = content['ai_welcome']
        
        # Update chat section
        if 'chat' in data:
            data['chat']['welcome'] = content['chat_welcome']
            data['chat']['welcomeDesc'] = content['chat_welcomeDesc']
        
        # Update dashboard cards
        if 'dashboard' in data:
            if 'upload_card' in data['dashboard']:
                data['dashboard']['upload_card']['title'] = content['dashboard_upload_title']
                data['dashboard']['upload_card']['description'] = content['dashboard_upload_desc']
            if 'declaration_card' in data['dashboard']:
                data['dashboard']['declaration_card']['title'] = content['dashboard_declaration_title']
                data['dashboard']['declaration_card']['description'] = content['dashboard_declaration_desc']
            if 'chat_card' in data['dashboard']:
                data['dashboard']['chat_card']['title'] = content['dashboard_chat_title']
                data['dashboard']['chat_card']['description'] = content['dashboard_chat_desc']
        
        # Write back
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f'[OK] Updated {lang}/common.json - Educational content')
        
    except Exception as e:
        print(f'[ERROR] {lang}: {e}')

print('\n[SUCCESS] All legal content replaced with educational content!')
