import { AlertTriangle } from 'lucide-react';
import { useLanguage } from '@/lib/LanguageContext';

export function UPLDisclaimer() {
    const { language } = useLanguage();

    // Get disclaimer text based on current language
    const getDisclaimerText = () => {
        const disclaimers: Record<string, string> = {
            'sk': "CODEX nie je právnická firma a neposkytuje právne poradenstvo. Táto informácia je určená len na všeobecné vzdelávacie účely. Pre konkrétnu právnu situáciu sa obráťte na licencovaného advokáta.",
            'en': "CODEX is not a law firm and does not provide legal advice. This information is intended for general educational purposes only. For specific legal situations, please consult a licensed attorney.",
            'uk': "CODEX не є юридичною фірмою і не надає юридичних консультацій. Ця інформація призначена лише для загальних освітніх цілей. Для конкретної юридичної ситуації зверніться до ліцензованого адвоката.",
            'ru': "CODEX не является юридической фирмой и не предоставляет юридических консультаций. Эта информация предназначена только для общих образовательных целей. Для конкретной юридической ситуации обратитесь к лицензированному адвокату.",
            'de': "CODEX ist keine Anwaltskanzlei und bietet keine Rechtsberatung an. Diese Informationen dienen nur allgemeinen Bildungszwecken. Für spezifische rechtliche Situationen wenden Sie sich bitte an einen zugelassenen Rechtsanwalt.",
            'it': "CODEX non è uno studio legale e non fornisce consulenza legale. Queste informazioni sono destinate solo a scopi educativi generali. Per situazioni legali specifiche, si prega di consultare un avvocato autorizzato.",
            'fr': "CODEX n'est pas un cabinet d'avocats et ne fournit pas de conseils juridiques. Ces informations sont destinées uniquement à des fins éducatives générales. Pour des situations juridiques spécifiques, veuillez consulter un avocat agréé.",
            'es': "CODEX no es un bufete de abogados y no proporciona asesoramiento legal. Esta información está destinada solo para fines educativos generales. Para situaciones legales específicas, consulte a un abogado licenciado.",
            'pl': "CODEX nie jest kancelarią prawną i nie świadczy usług doradztwa prawnego. Te informacje są przeznaczone wyłącznie do ogólnych celów edukacyjnych. W konkretnych sytuacjach prawnych należy skonsultować się z licencjonowanym adwokatem.",
            'cs': "CODEX není právnická firma a neposkytuje právní poradenství. Tyto informace jsou určeny pouze pro všeobecné vzdělávacie účely. Pro konkrétní právnu situáciu se obraťte na licencovaného advokáta."
        };

        return disclaimers[language] || disclaimers['sk'];
    };

    return (
        <div className="bg-amber-500/10 border border-amber-500/30 rounded-xl p-4 mb-6 backdrop-blur-sm">
            <div className="flex items-start space-x-3">
                <AlertTriangle className="w-5 h-5 text-amber-400 flex-shrink-0 mt-0.5" />
                <div className="flex-1">
                    <p className="text-sm text-amber-100 leading-relaxed">
                        <span className="font-semibold">⚠️ DÔLEŽITÉ:</span>{' '}
                        {getDisclaimerText()}
                    </p>
                </div>
            </div>
        </div>
    );
}
