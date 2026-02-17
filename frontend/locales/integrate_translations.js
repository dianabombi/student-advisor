const fs = require('fs');
const path = require('path');

// Chat translations
const chatTranslations = {
    sk: {
        title: "Právny Chat",
        welcome: "Vitajte v CODEX Legal AI",
        welcomeDesc: "Opýtajte sa ma na čokoľvek o slovenskom práve alebo vašich právnych dokumentoch.",
        placeholder: "Položte právnu otázku...",
        send: "Odoslať",
        thinking: "Premýšľam...",
        error: "Prepáčte, vyskytla sa chyba. Skúste to prosím znova.",
        sources: "Zdroje",
        similarity: "Relevancia",
        newSession: "Nová konverzácia",
        noSessions: "Zatiaľ žiadne konverzácie",
        messages: "správ",
        confirmDelete: "Naozaj chcete vymazať túto konverzáciu?",
        justNow: "Práve teraz",
        minsAgo: "m",
        hoursAgo: "h",
        daysAgo: "d"
    },
    en: {
        title: "Legal Chat",
        welcome: "Welcome to CODEX Legal AI",
        welcomeDesc: "Ask me anything about Slovak law or your legal documents.",
        placeholder: "Ask a legal question...",
        send: "Send",
        thinking: "Thinking...",
        error: "Sorry, something went wrong. Please try again.",
        sources: "Sources",
        similarity: "Relevance",
        newSession: "New Conversation",
        noSessions: "No conversations yet",
        messages: "messages",
        confirmDelete: "Are you sure you want to delete this conversation?",
        justNow: "Just now",
        minsAgo: "m ago",
        hoursAgo: "h ago",
        daysAgo: "d ago"
    },
    uk: {
        title: "Юридичний Чат",
        welcome: "Ласкаво просимо до CODEX Legal AI",
        welcomeDesc: "Запитайте мене про що завгодно щодо словацького права або ваших юридичних документів.",
        placeholder: "Поставте юридичне питання...",
        send: "Надіслати",
        thinking: "Думаю...",
        error: "Вибачте, сталася помилка. Спробуйте ще раз.",
        sources: "Джерела",
        similarity: "Релевантність",
        newSession: "Нова розмова",
        noSessions: "Поки немає розмов",
        messages: "повідомлень",
        confirmDelete: "Ви впевнені, що хочете видалити цю розмову?",
        justNow: "Щойно",
        minsAgo: "хв тому",
        hoursAgo: "год тому",
        daysAgo: "дн тому"
    },
    ru: {
        title: "Юридический Чат",
        welcome: "Добро пожаловать в CODEX Legal AI",
        welcomeDesc: "Спросите меня о чем угодно касательно словацкого права или ваших юридических документов.",
        placeholder: "Задайте юридический вопрос...",
        send: "Отправить",
        thinking: "Думаю...",
        error: "Извините, произошла ошибка. Попробуйте еще раз.",
        sources: "Источники",
        similarity: "Релевантность",
        newSession: "Новый разговор",
        noSessions: "Пока нет разговоров",
        messages: "сообщений",
        confirmDelete: "Вы уверены, что хотите удалить этот разговор?",
        justNow: "Только что",
        minsAgo: "мин назад",
        hoursAgo: "ч назад",
        daysAgo: "дн назад"
    }
};

// Extended common translations
const commonExtensions = {
    sk: {
        back: "Späť",
        loading: "Načítavam...",
        error: "Chyba",
        success: "Úspech",
        cancel: "Zrušiť",
        save: "Uložiť",
        delete: "Vymazať",
        edit: "Upraviť",
        close: "Zavrieť",
        backToDashboard: "Späť na prehľad"
    },
    en: {
        back: "Back",
        loading: "Loading...",
        error: "Error",
        success: "Success",
        cancel: "Cancel",
        save: "Save",
        delete: "Delete",
        edit: "Edit",
        close: "Close",
        backToDashboard: "Back to dashboard"
    },
    uk: {
        back: "Назад",
        loading: "Завантаження...",
        error: "Помилка",
        success: "Успіх",
        cancel: "Скасувати",
        save: "Зберегти",
        delete: "Видалити",
        edit: "Редагувати",
        close: "Закрити",
        backToDashboard: "Назад до панелі"
    },
    ru: {
        back: "Назад",
        loading: "Загрузка...",
        error: "Ошибка",
        success: "Успех",
        cancel: "Отменить",
        save: "Сохранить",
        delete: "Удалить",
        edit: "Редактировать",
        close: "Закрыть",
        backToDashboard: "Назад к панели"
    }
};

const languages = ['sk', 'en', 'uk', 'ru'];

console.log('🚀 Starting chat translations integration...\n');

languages.forEach(lang => {
    const filePath = path.join(__dirname, lang, 'common.json');

    try {
        // Read existing file
        const content = JSON.parse(fs.readFileSync(filePath, 'utf8'));

        // Add chat translations
        content.chat = chatTranslations[lang];

        // Extend common translations
        content.common = { ...content.common, ...commonExtensions[lang] };

        // Write back with proper formatting
        fs.writeFileSync(filePath, JSON.stringify(content, null, 4) + '\n');

        console.log(`✅ Updated ${lang}/common.json`);
    } catch (error) {
        console.error(`❌ Error updating ${lang}/common.json:`, error.message);
    }
});

console.log('\n✨ Translation integration complete!');
