#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Add proactive guidance to all AI consultant prompts - SIMPLIFIED VERSION
"""

import sys
sys.path.append('/app')

FILES = [
    '/app/services/housing_chat_service.py',
    '/app/services/jobs_chat_service.py',
]

# Proactive additions for each language
ADDITIONS = {
    'sk': '\n\n🎯 BUĎTE PROAKTÍVNY:\n- Ak nemáte presné informácie, VŽDY ponúknite alternatívu alebo Google vyhľadávanie\n- Navigujte používateľa: "Skúste vyhľadať na Google: [názov portálu] + [mesto]"\n- Buďte flexibilní - rozumejte rôznym formuláciám otázok\n- Ak niečo neviete, povedzte to úprimne a ponúknite ako to nájsť\n- Správajte sa ako skutočný konzultant, nie pasívny chatbot',
    
    'cs': '\n\n🎯 BUĎTE PROAKTIVNÍ:\n- Pokud nemáte přesné informace, VŽDY nabídněte alternativu nebo Google vyhledávání\n- Navigujte uživatele: "Zkuste vyhledat na Google: [název portálu] + [město]"\n- Buďte flexibilní - rozumějte různým formulacím otázek\n- Pokud něco nevíte, řekněte to upřímně a nabídněte jak to najít\n- Chovejte se jako skutečný konzultant, ne pasivní chatbot',
    
    'pl': '\n\n🎯 BĄDŹ PROAKTYWNY:\n- Jeśli nie masz dokładnych informacji, ZAWSZE zaproponuj alternatywę lub wyszukiwanie Google\n- Nawiguj użytkownika: "Spróbuj wyszukać w Google: [nazwa portalu] + [miasto]"\n- Bądź elastyczny - rozumiej różne sformułowania pytań\n- Jeśli czegoś nie wiesz, powiedz to szczerze i zaproponuj jak to znaleźć\n- Zachowuj się jak prawdziwy konsultant, nie pasywny chatbot',
    
    'en': '\n\n🎯 BE PROACTIVE:\n- If you don\'t have exact information, ALWAYS offer an alternative or Google search\n- Guide the user: "Try searching on Google: [portal name] + [city]"\n- Be flexible - understand different question formulations\n- If you don\'t know something, say it honestly and suggest how to find it\n- Act like a real consultant, not a passive chatbot',
    
    'de': '\n\n🎯 SEIEN SIE PROAKTIV:\n- Wenn Sie keine genauen Informationen haben, bieten Sie IMMER eine Alternative oder Google-Suche an\n- Führen Sie den Benutzer: "Versuchen Sie auf Google zu suchen: [Portalname] + [Stadt]"\n- Seien Sie flexibel - verstehen Sie verschiedene Frageformulierungen\n- Wenn Sie etwas nicht wissen, sagen Sie es ehrlich und schlagen Sie vor, wie man es findet\n- Verhalten Sie sich wie ein echter Berater, nicht wie ein passiver Chatbot',
    
    'fr': '\n\n🎯 SOYEZ PROACTIF:\n- Si vous n\'avez pas d\'informations exactes, proposez TOUJOURS une alternative ou recherche Google\n- Guidez l\'utilisateur: "Essayez de rechercher sur Google: [nom du portail] + [ville]"\n- Soyez flexible - comprenez différentes formulations de questions\n- Si vous ne savez pas quelque chose, dites-le honnêtement et suggérez comment le trouver\n- Comportez-vous comme un vrai consultant, pas comme un chatbot passif',
    
    'es': '\n\n🎯 SEA PROACTIVO:\n- Si no tiene información exacta, SIEMPRE ofrezca una alternativa o búsqueda Google\n- Guíe al usuario: "Intente buscar en Google: [nombre del portal] + [ciudad]"\n- Sea flexible - entienda diferentes formulaciones de preguntas\n- Si no sabe algo, dígalo honestamente y sugiera cómo encontrarlo\n- Actúe como un consultor real, no como un chatbot pasivo',
    
    'uk': '\n\n🎯 БУДЬТЕ ПРОАКТИВНИМИ:\n- Якщо не маєте точної інформації, ЗАВЖДИ пропонуйте альтернативу або пошук Google\n- Навігуйте користувача: "Спробуйте знайти в Google: [назва порталу] + [місто]"\n- Будьте гнучкими - розумійте різні формулювання питань\n- Якщо чогось не знаєте, скажіть це чесно і запропонуйте як це знайти\n- Поводьтеся як справжній консультант, а не пасивний чатбот',
    
    'it': '\n\n🎯 SII PROATTIVO:\n- Se non hai informazioni esatte, offri SEMPRE un\'alternativa o ricerca Google\n- Guida l\'utente: "Prova a cercare su Google: [nome del portale] + [città]"\n- Sii flessibile - comprendi diverse formulazioni di domande\n- Se non sai qualcosa, dillo onestamente e suggerisci come trovarlo\n- Comportati come un vero consulente, non come un chatbot passivo',
    
    'ru': '\n\n🎯 БУДЬТЕ ПРОАКТИВНЫМИ:\n- Если нет точной информации, ВСЕГДА предлагайте альтернативу или поиск Google\n- Направляйте пользователя: "Попробуйте найти в Google: [название портала] + [город]"\n- Будьте гибкими - понимайте разные формулировки вопросов\n- Если чего-то не знаете, скажите это честно и предложите как это найти\n- Ведите себя как настоящий консультант, а не пассивный чатбот',
    
    'pt': '\n\n🎯 SEJA PROATIVO:\n- Se não tiver informações exatas, SEMPRE ofereça uma alternativa ou pesquisa Google\n- Oriente o usuário: "Tente pesquisar no Google: [nome do portal] + [cidade]"\n- Seja flexível - entenda diferentes formulações de perguntas\n- Se não souber algo, diga honestamente e sugira como encontrar\n- Comporte-se como um consultor real, não como um chatbot passivo'
}

def enhance_file(filepath):
    """Add proactive sections to all prompts in file"""
    print(f"\n📝 Processing: {filepath}")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    modified_count = 0
    
    for lang, addition in ADDITIONS.items():
        # Find: "Be honest and use ONLY data from the list!"""
        # Replace with: "Be honest and use ONLY data from the list![ADDITION]"""
        
        # Pattern: find the end of each language prompt
        search_str = 'Be honest and use ONLY data from the list!'
        
        # Find all occurrences
        pos = 0
        while True:
            pos = content.find(search_str, pos)
            if pos == -1:
                break
            
            # Check if this is for our language by looking backwards
            # Find the language code definition (e.g., 'sk': f""")
            lang_start = content.rfind(f"'{lang}':", max(0, pos - 5000), pos)
            if lang_start != -1 and lang_start > pos - 5000:
                # Check if there's already a proactive section
                if '🎯' not in content[pos:pos+500]:
                    # Insert the addition after "Be honest..."
                    content = content[:pos + len(search_str)] + addition + content[pos + len(search_str):]
                    modified_count += 1
                    print(f"  ✅ Enhanced {lang} prompt")
                    pos += len(addition)
            
            pos += 1
    
    if modified_count > 0:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ Updated {modified_count} prompts in: {filepath}")
    else:
        print(f"⚠️  No changes needed: {filepath}")

if __name__ == "__main__":
    print("🚀 Enhancing AI consultant prompts for all 11 languages...")
    for filepath in FILES:
        try:
            enhance_file(filepath)
        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()
    
    print("\n✅ All prompts enhanced!")
