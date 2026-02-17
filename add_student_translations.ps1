$langs = @(
    @{code='cs'; title='Vaše brána k vzdělávacím příležitostem'; subtitle='Objevte univerzity, získejte AI poradenství a naplánujte svou akademickou budoucnost'; getStarted='Začít'; findHousing='Najít Ubytování'; explore='Prozkoumat Univerzity'},
    @{code='pl'; title='Twoja Brama do Możliwości Edukacyjnych'; subtitle='Odkryj uniwersytety, uzyskaj wsparcie AI i zaplanuj swoją akademicką przyszłość'; getStarted='Rozpocznij'; findHousing='Znajdź Zakwaterowanie'; explore='Przeglądaj Uniwersytety'},
    @{code='de'; title='Ihr Tor zu Bildungsmöglichkeiten'; subtitle='Entdecken Sie Universitäten, erhalten Sie KI-gestützte Beratung und planen Sie Ihre akademische Zukunft'; getStarted='Loslegen'; findHousing='Unterkunft Finden'; explore='Universitäten Erkunden'},
    @{code='fr'; title='Votre Porte vers les Opportunités Éducatives'; subtitle='Découvrez des universités, obtenez des conseils IA et planifiez votre avenir académique'; getStarted='Commencer'; findHousing='Trouver un Logement'; explore='Explorer les Universités'},
    @{code='es'; title='Su Puerta a las Oportunidades Educativas'; subtitle='Descubra universidades, obtenga orientación con IA y planifique su futuro académico'; getStarted='Comenzar'; findHousing='Encontrar Alojamiento'; explore='Explorar Universidades'},
    @{code='uk'; title='Ваші Ворота до Освітніх Можливостей'; subtitle='Відкрийте університети, отримайте AI-консультації та сплануйте своє академічне майбутнє'; getStarted='Почати'; findHousing='Знайти Житло'; explore='Досліджувати Університети'},
    @{code='it'; title='Il tuo accesso alle opportunità educative'; subtitle='Scopri le università, ottieni una guida AI e pianifica il tuo futuro accademico'; getStarted='Inizia'; findHousing='Trova Alloggio'; explore='Esplora le Università'},
    @{code='ru'; title='Ваши Ворота к Образовательным Возможностям'; subtitle='Откройте университеты, получите AI-консультации и спланируйте свое академическое будущее'; getStarted='Начать'; findHousing='Найти Жилье'; explore='Исследовать Университеты'}
)

foreach ($lang in $langs) {
    $file = "c:\Users\info\OneDrive\Dokumenty\STUDENT\frontend\locales\$($lang.code)\common.json"
    $content = Get-Content $file -Raw -Encoding UTF8
    
    # Find the position before "housing"
    $housingPos = $content.IndexOf('  "housing": {')
    if ($housingPos -gt 0) {
        $studentSection = @"
  "student": {
    "hero": {
      "title": "$($lang.title)",
      "subtitle": "$($lang.subtitle)",
      "getStarted": "$($lang.getStarted)",
      "findHousing": "$($lang.findHousing)",
      "exploreUniversities": "$($lang.explore)"
    }
  },

"@
        $newContent = $content.Insert($housingPos, $studentSection)
        $newContent | Out-File $file -Encoding UTF8 -NoNewline
        Write-Host "Updated $($lang.code)"
    }
}
