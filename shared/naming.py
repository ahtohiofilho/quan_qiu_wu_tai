import random

# ==========================   NOMES DAS PROVÍNCIAS EM INGLÊS   ==========================#

adj_ing = ["Good", "White", "Sacred", "Broken", "Hidden",
           "Long", "Little", "Old", "Heavenly", "Big",
           "High", "Small", "Large", "Pristine", "Bad",
           "Red", "Blue", "Green", "Yellow", "Black",
           "Golden", "Calm", "Dry", "Lost", "Brave",
           "Deep", "Bright", "Heavy", "Joyful", "Mysterious",
           "Petrified", "Split", "Pleasant", "Cooling", "Falling",
           "Sharp", "Distant", "Ancient", "Sad", "Beautiful",
           "Eternal", "Enchanted", "Sunny", "Cold", "Steep",
           "Gentle", "Peaceful", "Turbulent", "Dead", "Wide",
           "Open", "Closed", "Flat", "Dark", "Warm",
           "Serene", "Giant", "Pure"]

nouns_ing = ["Rock", "Mountain", "River", "Land", "House",
             "Field", "Cavern", "Sky", "Star", "Swamp",
             "Spring", "Forest", "Lake", "Sand", "Soil",
             "Winds", "Rain", "Cliff", "Fountain", "Water",
             "Man", "Grove", "Air", "Fire", "Leaf",
             "Trail", "Night", "Fruit", "Bird", "Snake",
             "Ville", "Hill", "Creek", "Hut", "Meadow",
             "Wolf", "Spirit", "Light", "Slope", "Soldier",
             "Valley", "Mound", "Town",
             "Woods", "Ridge", "Day", "Peak",
             "Refuge", "Sign", "Bush",
             "Pond", "Road", "Chapel", "City",
             "Bridge", "Priest", "Grave", "Curse",
             "Ground", "View", "Grass"]

# ==========================   NOMES DAS PROVÍNCIAS EM CHINÊS   ==========================#

adj_chi = [
    "Hǎo", "Bái", "Shénshèng", "Pòsuì", "Yǐncáng",
    "Xiǎo", "Lǎo", "Tiāntáng de", "Dà", "Gāo",
    "Yuánshǐ de", "Huài", "Hóngsè de", "Lánsè de", "Lǜsè de",
    "Huángsè de", "Hēisè de", "Jīn sè de", "Ānjìng", "Gānzào",
    "Míshī", "Yǒnggǎn", "Shēn", "Míngliàng", "Zhòng",
    "Kuàilè", "Shénmì", "Shíhuà", "Fēnliè", "Yúkuài",
    "Fēnlí", "Yáoyuǎn", "Gǔlǎo", "Bēishāng", "Měilì",
    "Yǒnghéng", "Qīnglǎng", "Wēnróu", "Píngjìng", "Dòngdàng",
    "Kuān", "Hēi'àn", "Níngjìng", "Jùdà", "Chúnjìng",
    "Sǐwáng", "Lěng", "Wēnnuǎn", "Zhāomì"
]

nouns_chi = [
    "Yánshí", "Shān", "Hé", "Tǔdì", "Fángzi",
    "Tián", "Dòngxué", "Tiānkōng", "Xīngxīng", "Zhǎozé",
    "Quán", "Sēnlín", "Hú", "Shā", "Tǔrǎng",
    "Fēng", "Yǔ", "Xuányá", "Pēnquán", "Shuǐ",
    "Nánrén", "Xiǎoshùlín", "Kōngqì", "Huǒ", "Yè",
    "Xiǎolù", "Yè", "Shuǐguǒ", "Niǎo", "Shé",
    "Xiǎozhèn", "Qiū", "Xī", "Xiǎowū", "Cǎodì",
    "Láng", "Líng", "Guāng", "Pō", "Shìbīng",
    "Shāngǔ", "Tǔqiū", "Chéngzhèn",
    "Shùlín", "Shānjǐ", "Tiān", "Fēng",
    "Bìnàn Suǒ", "Biāozhì", "Guànmù",
    "Chítáng", "Lù", "Xiǎo jiàotáng", "Chéngshì",
    "Qiáo", "Mùshī", "Fénmù", "Zǔzhòu",
    "Dìmiàn", "Jǐngsè", "Cǎo"
]

# ==========================   NOMES DAS PROVÍNCIAS EM WU   ==========================#

adj_wu = [
    "Hao", "Baek", "Shensheng", "Posui", "Yincang",
    "Long", "Xiao", "Lao", "Tiantang De", "Da",
    "Gao", "Xiao", "Da", "Yuanshi", "Huai",
    "Hong", "Lan", "Lǜ", "Huang", "Hei",
    "Jin", "Anjing", "Ganzao", "Mishi", "Yonggan",
    "Shen", "Liang", "Zhong", "Kuaile", "Shenmi",
    "Shihua", "Fenlie", "Yukuai", "Shuangshuang", "Falling",
    "Ji", "Yuan", "Gulao", "Beishang", "Meili",
    "Yongheng", "Jingya", "Wenxin", "Pingjing", "Dongdang",
    "Guang", "Hei'an", "Ningjing", "Juda", "Chunjing",
    "Si", "Leng", "Wennuan", "Zhaomi"
]

nouns_wu = [
    "Yan", "Shan", "He", "Di", "Fangzi",
    "Tian", "Dong", "Tian", "Xing", "Zhaoze",
    "Quan", "Senlin", "Hu", "Sha", "Turang",
    "Feng", "Yu", "Xuanya", "Penquan", "Shui",
    "Nan", "Xiaoshulin", "Kongqi", "Huo", "Ye",
    "Xiaolu", "Ye", "Shuiguo", "Niao", "She",
    "Zhen", "Qiu", "Xi", "Wu", "Caodi",
    "Lang", "Ling", "Guang", "Po", "Shibing",
    "Gu", "Qiu", "Zhen",
    "Ling", "Tian", "Feng",
    "Binan", "Biaozhi", "Guanmu",
    "Chitang", "Lù", "Jiaotang", "Cheng",
    "Qiao", "Mushi", "Fen", "Zuzhou",
    "Dimian", "Jingse", "Cao"
]

# ==========================   NOMES DAS PROVÍNCIAS EM YUE   ==========================#

adj_yue = [
    "Hóu", "Baahk", "Sān", "Kāp", "Chòih",
    "Cheung", "Sai", "Louh", "Tin", "Daih",
    "Hòhng", "Sai", "Daaih", "Chīng", "Wāi",
    "Hùhng", "Làahm", "Luhk", "Wòhng", "Hāak",
    "Gām", "Ngaan", "Gaan", "Sāt", "Yùhng",
    "Sām", "Mihng", "Jung", "Fùhng", "Sām",
    "Sāam", "Fāan", "Fāan", "Sīk", "Lohk",
    "Kēui", "Yúhn", "Gú", "Sāam", "Meih",
    "Yúhn", "Meih", "Tìng", "Làahng", "Ging",
    "Wān", "Fèihng", "Sūng", "Sīk", "Fú",
    "Dāk", "Gwán", "Bihn", "Aàm", "Wān",
    "Nìhng", "Gin", "Kéuhng"
]

nouns_yue = [
    "Sék", "Sāan", "Hòh", "Dih", "Uk",
    "Tìhn", "Duhng", "Tin", "Sīng", "Jóu",
    "Chēun", "Sāan", "Wuht", "Sā", "Tó",
    "Fūng", "Yúh", "Nga", "Bāan", "Sēui",
    "Nàahm", "Làahm", "Hēung", "Fó", "Yihp",
    "Jīng", "Yeh", "Gwó", "Jīu", "Séh",
    "Chéng", "Kā", "Hēung", "Wū", "Tīn",
    "Lòhng", "Lìhng", "Gōng", "Bōu", "Sih",
    "Gūk", "Fūng", "Māhng",
    "Líng", "Yaht", "Fūng",
    "Bāk", "Bīu", "Chāan",
    "Chìh", "Lóuh", "Sīu", "Sihng",
    "Kiu", "Sīn", "Fan", "Joek",
    "Deih", "Jíng", "Chou"
]

# ==========================   NOMES DAS PROVÍNCIAS EM MIN   ==========================#

adj_min = [
    "Hó", "Pe̍h", "Siān-tè", "Pō", "Bih",
    "Tiô", "Sió", "Lō", "Thian-tâng ê", "Tōa",
    "Kò͘", "Sió", "Tōa", "Chheng-chhiūⁿ", "Phāi",
    "Âng-sek ê", "Lán-sek ê", "Lū-sek ê", "N̂g-sek ê", "Hēi-sek ê",
    "Kim-sek ê", "Bêng-an", "Kan", "Lò͘", "Yúng",
    "Khâm", "Bêng", "Chòng", "Khoai-lo̍h", "Sīm-ji̍t",
    "Pê", "Pun-liāu", "Khoân-hòaⁿ", "Chhia̍t-liāu", "Tò-lo̍h",
    "Siam", "Tū", "Kó͘", "Phainn", "Biú",
    "Íⁿ-chióng", "Tīn-hiong", "Thinn-siaⁿ", "Kang", "Sú",
    "Lêng", "Khìaⁿ", "Lóng", "Sǹg", "Oân",
    "Chhiūⁿ", "Khí-á", "Chêng"
]

nouns_min = [
    "Chioh", "Suann", "Hô", "Tō", "Tiám",
    "Chhân", "Tōng", "Thinn", "Chhiⁿ", "Chháu",
    "Chhûn", "Sng-lîm", "Oh", "Sòaⁿ", "Thô",
    "Hûiⁿ", "Hō͘", "Kiám", "Pun", "Chúi",
    "Lâng", "Siâu", "Khong-khì", "Hóe", "Hâ",
    "Lō͘-chhù", "I̍aⁿ", "Kúi", "Chhui", "Chôa",
    "Chiâⁿ", "Kio", "Kè", "Koe", "Chháu-lí",
    "Lâng-kī", "Seng", "Chhìng", "Pò", "Chû",
    "Kheh", "Kiôⁿ", "Chhng",
    "Lêng", "Jat", "Hiong"
    "Pi-bāng", "Pió", "Chhe-bò",
    "Chhê", "Lō͘", "Chha", "Chhīⁿ",
    "Kiô", "Sūn", "Būn", "Chòe",
    "Toē", "Chhīng", "Chháu"
]

# ==========================   NOMES DAS PROVÍNCIAS EM ESPANHOL   ==========================#

nouns_esp_mas = ["Río", "Hombre", "Viento", "Fuego", "Sendero",
                 "Campo", "Pueblo", "Lobo", "Soldado", "Arroyo",
                 "Montículo", "Día", "Bosque", "Rancho", "Pantano",
                 "Parque", "Señal", "Estanque", "Camino", "Puente",
                 "Cielo", "Manantial", "Bosque", "Lago", "Suelo",
                 "Acantilado", "Pájaro", "Sitio", "Valle", "Pozo",
                 "Refugio", "Arbusto", "Nacimiento", "Terreno", "Espíritu"]

nouns_esp_fem = ["Roca", "Montaña", "Tierra", "Casa", "Fruta",
                 "Caverna", "Estrella", "Arena", "Cima",
                 "Lluvia", "Fuente", "Agua", "Arboleda", "Hoja",
                 "Noche", "Serpiente", "Colina", "Cabaña", "Pradera",
                 "Luz", "Ladera", "Margem", "Ciudad", "Cresta",
                 "Hada", "Capilla", "Tumba", "Maldición", "Vista",
                 "Hierba", "Cruz"]

adj_esp_mas = ["Bueno", "Blanco", "Sagrado", "Roto", "Oculto",
               "Pequeño", "Pequeño", "Viejo", "Celestial", "Grande",
               "Alto", "Pequeño", "Grande", "Prístino", "Malo",
               "Rojo", "Azul", "Verde", "Amarillo", "Negro",
               "Dorado", "Calmado", "Ruidoso", "Seco", "Perdido",
               "Profundo", "Brillante", "Pesado", "Alegre", "Misterioso",
               "Móvil", "Dividido", "Agradable", "Refrigerante", "Cayente",
               "Afilado", "Distante", "Antiguo", "Triste", "Hermoso",
               "Rasgado", "Majestuoso", "Soleado", "Sombrío", "Empinado",
               "Suave", "Pacífico", "Turbulento", "Áspero", "Ancho",
               "Abierto", "Cerrado", "Plano", "Oscuro", "Infinito",
               "Sereno", "Gigante", "Fino", "Largo", "Ruidoso",
               "Frío", "Cálido", "Peligroso", "Encantado", "Carvado",
               "Puro", "Valiente", "Eterno", "Petrificado", "Muerto"]

adj_esp_fem = ["Buena", "Blanca", "Sacra", "Rota", "Oculta",
               "Pequeña", "Pequeña", "Vieja", "Celestial", "Grande",
               "Alta", "Pequeña", "Grande", "Prístina", "Mala",
               "Roja", "Azul", "Verde", "Amarilla", "Negra",
               "Dorada", "Calmada", "Ruidosa", "Seca", "Perdida",
               "Profunda", "Brillante", "Pesada", "Alegre", "Misteriosa",
               "Móvil", "Dividida", "Agradable", "Refrigerante", "Cayente",
               "Afilada", "Distante", "Antigua", "Triste", "Hermosa",
               "Rasgada", "Majestuosa", "Soleada", "Sombría", "Empinada",
               "Suave", "Pacífica", "Turbulenta", "Áspera", "Ancha",
               "Abierta", "Cerrada", "Plana", "Oscura", "Infinita",
               "Serena", "Gigante", "Fina", "Larga", "Ruidosa",
               "Fría", "Cálida", "Peligrosa", "Encantada", "Carvada",
               "Pura", "Valiente", "Eterna", "Petrificada", "Muerta"]

# ==========================   NOMES DAS PROVÍNCIAS EM FRANCÊS   ==========================#

adj_fra_mas = ["Bon", "Blanc", "Sacré", "Cassé", "Caché",
               "Petit", "Mort", "Vieux", "Céleste", "Grand",
               "Haut", "Pétrifié", "Éternel", "Pristin", "Mauvais",
               "Rouge", "Bleu", "Vert", "Jaune", "Noir",
               "Doré", "Calme", "Bruyant", "Sec", "Perdu",
               "Profond", "Brillant", "Lourd", "Joyeux", "Mystérieux",
               "Mouvant", "Divisé", "Agréable", "Rafraîchissant", "Tombant",
               "Tranchant", "Lointain", "Ancien", "Triste", "Beau",
               "Déchiré", "Majestueux", "Ensoleillé", "Sombre", "Escarpé",
               "Douc", "Paisible", "Turbulent", "Dur", "Large",
               "Ouvert", "Fermé", "Pur", "Sombre", "Infini",
               "Serein", "Géant", "Fin", "Long", "Courageux",
               "Froid", "Chaud", "Périlleux", "Enchanté", "Taillé"]

adj_fra_fem = ["Bonne", "Blanche", "Sacrée", "Cassée", "Cachée",
               "Petite", "Morte", "Vieille", "Céleste", "Grande",
               "Haute", "Pétrifiée", "Éternelle", "Pristine", "Mauvaise",
               "Rouge", "Bleue", "Verte", "Jaune", "Noire",
               "Dorée", "Calme", "Bruyante", "Sèche", "Perdue",
               "Profonde", "Brillante", "Lourde", "Joyeuse", "Mystérieuse",
               "Mouvante", "Divisée", "Agréable", "Rafraîchissante", "Tombante",
               "Tranchante", "Lointaine", "Ancienne", "Triste", "Belle",
               "Déchirée", "Majestueuse", "Ensoleillée", "Sombre", "Escarpée",
               "Douce", "Paisible", "Turbulente", "Dure", "Large",
               "Ouverte", "Fermée", "Pure", "Sombre", "Infinie",
               "Sereine", "Géante", "Fine", "Longue", "Courageuse",
               "Froide", "Chaude", "Périlleuse", "Enchantée", "Taillée"]

bags = ["Bon", "Petit", "Vieux", "Grand", "Haut",
        "Ancien", "Beau", "Large", "Long", "Bonne",
        "Petite", "Vieille", "Grande", "Haute", "Ancienne",
        "Belle", "Large", "Longue"]

nouns_fra_mas = ["Champ", "Ciel", "Marais", "Site", "Lac",
                 "Sable", "Sol", "Vent", "Homme", "Bosquet",
                 "Air", "Feu", "Sentier", "Oiseau", "Ruisseau",
                 "Pré", "Loup", "Esprit", "Soldat", "Puits",
                 "Tertre", "Bois", "Jour", "Pic", "Parc",
                 "Refuge", "Signe", "Buisson", "Étang", "Pont",
                 "Prêtre", "Sol"]

nouns_fra_fem = ["Roche", "Montagne", "Rivière", "Terre", "Maison",
                 "Caverne", "Étoile", "Forêt", "Pluie",
                 "Falaise", "Fontaine", "Eau", "Feuille",
                 "Nuit", "Fruit", "Serpent", "Ville", "Colline",
                 "Cabane", "Lumière", "Pente", "Vallée", "Rive",
                 "Ville", "Crête", "Croix", "Ligne", "Fée",
                 "Route", "Chapelle", "Ville", "Tombe", "Malédiction",
                 "Naissance", "Vue", "Herbe"]

# ==========================   NOMES DAS PROVÍNCIAS EM HINDI   ==========================#

adj_hin_mas = ["Achchha", "Safed", "Pavitr", "Toota Hua", "Chhipa Hua",
               "Chhota", "Thoda", "Puraana", "Swargiy", "Bada",
               "Ucch", "Chhota", "Bada", "Nirmal", "Bura",
               "Laal", "Neela", "Hara", "Peela", "Kaala",
               "Svarnim", "Shaant", "Sookha", "Kho Gaya", "Bahadur",
               "Gahra", "Chamkeela", "Bhaari", "Aanandmay", "Rahasyamay",
               "Shilajit", "Vibhaajit", "Sukhad", "Sheetal", "Girta",
               "Tez", "Door", "Praacheen", "Dukhii", "Sundar",
               "Shaashvat", "Mantramugdh", "Sooryamay", "Thanda", "Dhalwaan",
               "Naram", "Shaantipoorn", "Ashaant", "Mara Hua",
               "Chaudaa", "Khula", "Band", "Lamba", "Andhera",
               "Garam", "Shaant", "Vishaalkaay", "Shuddh"]

adj_hin_fem = ["Achchhi", "Safed", "Pavitr", "Tooti Hui", "Chhupi Hui",
               "Chhoti", "Thodi", "Puraani", "Swargiy", "Badi",
               "Ucchi", "Chhoti", "Badi", "Nirmal", "Buri",
               "Laal", "Neeli", "Hari", "Peeli", "Kaali",
               "Svarn", "Shaant", "Sookhi", "Kho Gayi", "Bahadur",
               "Gahri", "Chamkeeli", "Bhaari", "Aanandmay", "Rahasyamay",
               "Shilajit", "Vibhaajit", "Sukhad", "Sheetal", "Girti",
               "Tez", "Door", "Praacheen", "Dukhii", "Sundar",
               "Shaashvat", "Mantramugdh", "Sooryamay", "Thandi", "Dhalwaan",
               "Naram", "Shaantipoorn", "Ashaant", "Mari", "Chaudii",
               "Khulii", "Band", "Andherii", "Garam",
               "Shaant", "Vishaal", "Shuddh", "Lambii"]

nouns_hin_mas = ["Pahaad", "Parvat", "Ghar", "Khet", "Guha",
                 "Aakash", "Tara", "Aadmi", "Vriksh", "Vayu",
                 "Aag", "Gaon", "Pahaadi", "Jhupri", "Maidaan",
                 "Prakash", "Dhalan", "Sainik", "Teela", "Din",
                 "Shikhar", "Aashray", "Sanket", "Talab", "Sadak",
                 "Pul", "Pujari", "Shaap"]

nouns_hin_fem = ["Nadi", "Bhoomi", "Daldal", "Junglai", "Jheel",
                 "Ret", "Mitti", "Hawa", "Baarish", "Khaai",
                 "Fawara", "Paani", "Patta", "Raat",
                 "Pakshi", "Saanp", "Nadiya", "Bheriya", "Aatma",
                 "Ghaati", "Nagari", "Chotee", "Jangal", "Jhaadi",
                 "Ghaas", "Nagar", "Kabar", "Zameen", "Drishya"]

# ==========================   NOMES DAS PROVÍNCIAS EM RUSSO   ==========================#

adj_rus_mas = ["Khoroshiy", "Belyy", "Svyatoy", "Slomannyy", "Skrytyy",
               "Malen'kiy", "Staryy", "Nebesnyy", "Bol'shoy", "Vysokiy",
               "Gigantskiy", "Dlinnyy", "Chistyy", "Netronutyy", "Plokhoy",
               "Krasnyy", "Siniy", "Zelenyy", "Zheltyy", "Chernyy",
               "Zolotoy", "Spokoinyy", "Sukhoy", "Poteryannyy", "Smelyy",
               "Glubokiy", "Yarkiy", "Tyazhelyy", "Radostnyy", "Zagadochnyy",
               "Okamenelyy", "Raskolotyy", "Priyatnyy", "Okhlazhdayushchiy", "Padayushchiy",
               "Ostryy", "Dalekiy", "Drevniy", "Grustnyy", "Prekrasnyy",
               "Vechnyy", "Ocharovannyy", "Solnechnyy", "Kholodnyy", "Krutoy",
               "Nezhnyy", "Spokoinyy", "Burnyy", "Mertvyy", "Shirokiy",
               "Otkrytyy", "Zakrytyy", "Ploskiy", "Temnyy", "Teplyy",
               "Bezmyatezhnyy"]

adj_rus_fem = ["Khoroshaya", "Belaya", "Svyataya", "Slomannaya", "Skrytaya",
               "Malen'kaya", "Chistaya", "Staraya", "Nebesnaya", "Bol'shaya",
               "Vysokaya", "Malen'kaya", "Dlinnaya", "Netronutaya", "Plohaya",
               "Krasnaya", "Sinyaya", "Zelenaya", "Zhel'taya", "Chernaya",
               "Zolotaya", "Spokojnaya", "Sukhaya", "Poteryannaya", "Smelaya",
               "Glubokaya", "Yarkaya", "Tyazhelaya", "Radostnaya", "Zagadochnaya",
               "Okamenelaya", "Raskolotaya", "Priyatnaya", "Okhlazhdayushchaya", "Padayushchaya",
               "Ostraya", "Dalekaya", "Drevnyaya", "Grustnaya", "Prekrasnaya",
               "Vechnaya", "Ocharovannaya", "Solnechnaya", "Kholodnaya", "Krutaya",
               "Nezhnaya", "Spokojnaya", "Burnaya", "Mertvaya", "Shirokaya",
               "Otkrytaya", "Zakrytaya", "Ploskaya", "Temnaya", "Teplaya",
               "Bezmyatezhnaya", "Gigantskaya"]

adj_rus_neu = ["Khoroshee", "Beloe", "Svyatoe", "Slomannoe", "Skrytoe",
               "Malen'koe", "Chistoe", "Staroe", "Nebesnoe", "Bol'shoe",
               "Vysokoe", "Gigantskoe", "Dlinnoe", "Netronutoe", "Plokhoе",
               "Krasnoe", "Sinee", "Zelenoe", "Zheltоe", "Chernoe",
               "Zolotoe", "Spokoynoe", "Sukhoe", "Poteryannoe", "Smeloe",
               "Glubokoe", "Yarkoe", "Tyazheloe", "Radostnoe", "Zagadochnoe",
               "Okameneloe", "Raskolotoe", "Priyatnoe", "Okhlazhdayushchee", "Padayushchee",
               "Ostroе", "Dalekoe", "Drevnee", "Grustnoe", "Prekrasnoe",
               "Vechnoe", "Ocharovannoe", "Solnechnoe", "Kholodnoe", "Krutoe",
               "Nezhnoe", "Spokoynoe", "Burnoe", "Mertvoe", "Shirokoe",
               "Otkrytoe", "Zakrytoe", "Ploskoe", "Temnoe", "Teploe",
               "Bezmyatezhnoe"]

nouns_rus_mas = ["Dom", "Rodnik", "Les", "Pesok", "Vetry",
                 "Dozhd'", "Utes", "Fontan", "Chelovek", "Vozdukh",
                 "Ogon'", "List", "Frukt", "Kholm", "Ruchey",
                 "Lug", "Volk", "Dukh", "Svet", "Sklon",
                 "Soldat", "Valun", "Gorod", "Lesa", "Greben'",
                 "Den'", "Pik", "Znak", "Kust", "Prud",
                 "Most", "Svyashchennik", "Vid"]

nouns_rus_fem = ["Skala", "Gora", "Reka", "Zemlya", "Peshchera",
                 "Zvezda", "Pochva", "Voda", "Rosha", "Tropa",
                 "Noch'", "Ptitsa", "Zmeya", "Derevnya", "Khizhina",
                 "Dolina", "Doroga", "Chasovnya", "Mogila", "Zemlya",
                 "Trava"]

nouns_rus_neu = ["Pole", "Nebo", "Boloto", "Ozero", "Ubezhishche",
                 "Proklyatie"]

# ==========================   NOMES DAS PROVÍNCIAS EM VIETNAMITA   ==========================#

nouns_viet = ["Đá", "Núi", "Sông", "Đất", "Nhà",
              "Ruộng", "Hang Động", "Bầu Trời", "Sao", "Đầm Lầy",
              "Suối", "Rừng", "Hồ", "Cát", "Đất",
              "Gió", "Mưa", "Vách Đá", "Suối", "Nước",
              "Người", "Rừng", "Không Khí", "Lửa", "Lá",
              "Đường Mòn", "Đêm", "Trái Cây", "Chim", "Rắn",
              "Làng", "Đồi", "Rãnh", "Nhà Gỗ", "Đồng Cỏ",
              "Sói", "Hồn", "Ánh Sáng", "Dốc", "Người Lính",
              "Thung Lũng", "Gò Đất", "Thị Trấn",
              "Rừng", "Dãy Núi", "Ngày", "Đỉnh",
              "Nơi Trú Ẩn", "Dấu Hiệu", "Cây Bụi",
              "Ao", "Đường", "Nhà Thờ Nhỏ", "Thành Phố",
              "Cây Cầu", "Thầy Tu", "Nghĩa Trang", "Lời Nguyền",
              "Mặt Đất", "Quang Cảnh", "Cỏ"]

adj_viet = ["Tốt", "Trắng", "Thánh Thiêng", "Vỡ", "Ẩn",
            "Nhỏ", "Nhỏ", "Cũ", "Thiên Thần", "Lớn",
            "Cao", "Nhỏ", "Lớn", "Nguyên Sơ", "Xấu",
            "Đỏ", "Xanh Dương", "Xanh Lá", "Vàng", "Đen",
            "Vàng", "Bình Tĩnh", "Khô", "Lạc", "Dũng Cảm",
            "Sâu", "Sáng", "Nặng", "Vui Vẻ", "Bí Ẩn",
            "Hóa Thạch", "Chia", "Dễ Chịu", "Làm Mát", "Rơi",
            "Sắc", "Xa Xôi", "Cổ Xưa", "Buồn", "Xinh Đẹp",
            "Vĩnh Cửu", "Phù Thủy", "Nắng", "Lạnh", "Dốc",
            "Nhẹ Nhàng", "Thanh Bình", "Hỗn Loạn", "Chết", "Rộng",
            "Mở", "Đóng", "Bằng Phẳng", "Tối", "Ấm Áp",
            "Yên Bình", "Khổng Lồ", "Trong Trắng", "Dài"]

# ==========================   NOMES DAS PROVÍNCIAS EM TURCO   ==========================#

adj_tur = ["İyi", "Beyaz", "Kutsal", "Kırık", "Gizli",
           "Minik", "Küçük", "Eski", "Cennetsel", "Büyük",
           "Yüksek", "Küçük", "Büyük", "El değmemiş", "Kötü",
           "Kırmızı", "Mavi", "Yeşil", "Sarı", "Siyah",
           "Altın", "Sakin", "Kuru", "Kayıp", "Cesur",
           "Derin", "Parlak", "Ağır", "Sevinçli", "Gizemli",
           "Taşlaşmış", "Bölünmüş", "Hoş", "Serinletici", "Düşen",
           "Keskin", "Uzak", "Antik", "Üzgün", "Güzel",
           "Ebedi", "Büyülenmiş", "Güneşli", "Soğuk", "Dik",
           "Nazik", "Huzurlu", "Turbulanslı", "Ölü", "Geniş",
           "Açık", "Kapalı", "Düz", "Karanlık", "Sıcak",
           "Sakin", "Dev", "Saf", "Uzun"]

nouns_tur = ["Kaya", "Dağ", "Nehir", "Toprak", "Ev",
             "Tarla", "Mağara", "Gökyüzü", "Yıldız", "Bataklık",
             "Pınar", "Orman", "Göl", "Kum", "Toprak",
             "Rüzgarlar", "Yağmur", "Uçurum", "Fıskiye", "Su",
             "Adam", "Ağaçlık", "Hava", "Ateş", "Yaprak",
             "Yol", "Gece", "Meyve", "Kuş", "Yılan",
             "Köy", "Tepelik", "Köy", "Kümes", "Çayır",
             "Kurt", "Ruh", "Işık", "Yamaç", "Asker",
             "Vadi", "Tepenin", "Şehir",
             "Orman", "Sırt", "Gün", "Zirve",
             "Sığınak", "İşaret", "Çalı",
             "Gölet", "Yol", "Kapalı Mekan", "Şehir",
             "Köprü", "Rahip", "Mezar", "Lanet",
             "Toprak", "Manzara", "Çim"]

# ==========================   NOMES DAS PROVÍNCIAS EM ÁRABE   ==========================#

nouns_ara_mas = ["Jabal", "Nahr", "Ard", "Bayt", "Haql",
                 "Kahf", "Najm", "Naba", "Ramal", "Turab",
                 "Riyah", "Matar", "Jurf", "Maa", "Rajul",
                 "Bustan", "Hawa", "Nar", "Mamar", "Layl",
                 "Tair", "Tal", "Jadwal", "Koukh", "Dhi'b",
                 "Ruh", "Daw'", "Munhadar", "Jundi", "Wadi",
                 "Tal", "Balda", "Yawm", "Qimma", "Malja'",
                 "Alama", "Shujaira", "Birka", "Tariq", "Jisr",
                 "Kahin", "Qabr", "Manzar"]

nouns_ara_fem = ["Sakhra", "Samaa", "Mustanqaa", "Ghaabah", "Buhayrah",
                 "Nafura", "Waraqa", "Fakihah", "Thu'ban", "Madina",
                 "Marj", "La'na", "Ard", "Ushb"]

adj_ara_mas = ["Jayyid", "Abyad", "Muqaddas", "Maksur", "Makhfi",
               "Saghir", "Qadeem", "Samaawi", "Kabir",
               "Aali", "Naqi", "Sayyi'", "Hadi'",
               "Ahmar", "Azraq", "Akhdar", "Asfar", "Aswad",
               "Dhahabi", "Haade", "Jaa'if", "Mafqood",
               "Ameek", "Mashriq", "Thaqeel", "Mufrih", "Ghaamid",
               "Mutaharrik", "Mashquq", "Latif'", "Mubarrid", "Suqut",
               "Had", "Ba'id", "Qadeem", "Hazeen", "Jameel",
               "Mumazziq", "Muhib", "Mashmis", "Ka'ib", "Shadid",
               "Salem", "Mutadarrib", "Qaas", "Wasi'",
               "Muftuh", "Maghluq", "Mustah", "Dakn", "Lanha'i",
               "Amlaq", "Twil", "Sakhb",
               "Baarid", "Daa'if", "Khaatir",
               "Naqi", "Shaji'", "Abedi", "Mutahjar", "Mayyit"]

adj_ara_fem = ["Jayyidah", "Abyadah", "Muqaddasah", "Maksurah", "Makhfiyah",
               "Saghirah", "Qadeemah", "Samaawiyah", "Kabirah", "Aaliyah",
               "Naqiyah", "Sayyi'ah", "Hadi'ah", "Ahmarah", "Azraqah",
               "Akhdarah", "Asfarah", "Aswadah", "Dhahabiyah", "Haadeh",
               "Jaa'ifah", "Mafqoodah", "Ameekah", "Mashriqah", "Thaqeelah",
               "Mufrihah", "Ghaamidah", "Mutaharrikah", "Mashquqah", "Latif'ah",
               "Mubarridah", "Suqutah", "Hadh", "Baidah", "Qadeemah",
               "Hazeenah", "Jameelah", "Mumazziqah", "Muhibah", "Mashmisah",
               "Salemah", "Mutadarribah", "Qaasah", "Wasi'ah", "Muftuhah",
               "Maghluqah", "Mustahah", "Daknah", "Lanha'iah", "Amlaqah",
               "Twilah", "Sakhbah", "Baaridah", "Daa'ifah", "Khaatirah",
               "Naqiyah", "Shaji'ah", "Abediyah", "Mutahjarah", "Mayyitah"]

# ==========================   NOMES DAS PROVÍNCIAS EM INDONÉSIO   ==========================#

nouns_ind = ["Batu", "Gunung", "Sungai", "Tanah", "Rumah",
             "Lapangan", "Gua", "Langit", "Bintang", "Lembah",
             "Mata Air", "Hutan", "Danau", "Pasir", "Angin",
             "Hujan", "Tebing", "Air", "Pria", "Udara",
             "Api", "Daun", "Jejak", "Malam", "Buah",
             "Burung", "Ular", "Desa", "Bukit",
             "Gubuk", "Padang", "Serigala", "Roh", "Cahaya",
             "Kemiringan", "Prajurit", "Bank", "Sumur", "Gundukan",
             "Kota", "Punggung", "Ranch", "Hari", "Puncak",
             "Garis", "Taman", "Tempat Perlindungan", "Tanda", "Semak",
             "Kolam", "Peri", "Jalan", "Gereja", "Jembatan",
             "Imam", "Kuburan", "Kutukan", "Kelahiran", "Pemandangan",
             "Rumput", "Tempat"]

adj_ind = ["Baik", "Putih", "Suci", "Patah", "Tersembunyi",
           "Kecil", "Tua", "Ilahi", "Besar",
           "Tinggi", "Besar", "Buruk",
           "Merah", "Biru", "Hijau", "Kuning", "Hitam",
           "Emas", "Tenang", "Bising", "Kering", "Hilang",
           "Dalam", "Terang", "Berat", "Gembira", "Misterius",
           "Bergerak", "Terbelah", "Menyenangkan", "Pendinginan", "Jatuh",
           "Tajam", "Jauh", "Kuno", "Sedih", "Indah",
           "Robek", "Mewah", "Cerah", "Suram", "Curam",
           "Lembut", "Damai", "Berombak", "Kasar", "Lebar",
           "Terbuka", "Tertutup", "Dat", "Gelap", "Tak Terbatas",
           "Tenang", "Raksasa", "Bagus", "Panjang", "Loud",
           "Dingin", "Hangat", "Berbahaya", "Bertih", "Diukir",
           "Murni", "Berani", "Abadi", "Membeku", "Mati"]

# ==========================   NOMES DAS PROVÍNCIAS EM FARSI   ==========================#

nouns_far = [
    "Sang", "Kūh", "Rudkhāneh", "Zamīn", "Khāneh",
    "Keshāvarzī", "Ghar", "Āsemān", "Setāreh", "Batlāgh",
    "Cheshmeh", "Jangal", "Daryācheh", "Shen", "Khat",
    "Bād", "Bārān", "Sakhreh", "Cheshmeh", "Āb",
    "Mard", "Bāgh", "Havā", "Ātash", "Barg",
    "Rāh", "Shab", "Miveh", "Parandeh", "Mār",
    "Shahrak", "Tappeh", "Juybār", "Kolbeh", "Marghzār",
    "Gorg", "Rūh", "Nūr", "Sarak", "Sarbaaz",
    "Dara", "Tappey", "Shahr",
    "Kamar", "Ruz", "Qolleh",
    "Panāh", "Neshān", "Booteh",
    "Hawz", "Jādeh", "Kelīsā", "Shahr",
    "Pol", "Keshīsh", "Ghabr", "Lanat",
    "Zamīn", "Manzareh", "Alaf"
]

adj_far = [
    "Khoob", "Sefid", "Moghaddas", "Shekasteh", "Penhan",
    "Toolani", "Koochak", "Pir", "Asemani", "Bozorg",
    "Boland", "Koochak", "Bozorg", "Pāk", "Bad",
    "Ghermez", "Ābi", "Sabz", "Zard", "Siah",
    "Talāyi", "Ārām", "Khoshk", "Gomshodeh", "Shoja",
    "Amigh", "Roshan", "Sangin", "Shad", "Asrārāmiz",
    "Sang Shodeh", "Taghseem Shodeh", "Khoshāyand", "Sard Konandeh", "Soghut Konandeh",
    "Tez", "Door", "Bāstān", "Ghamgin", "Ziba",
    "Abadi", "Gonjunje", "Aftābi", "Sard", "Sakht",
    "Lotf", "Āram", "Ashofteh", "Morde", "Pahn",
    "Bāz", "Basteh", "Hamvār", "Tārik", "Garm",
    "Arām", "Azim", "Pak"
]


# ==========================   NOMES DAS PROVÍNCIAS EM HAUSA   ==========================#

nouns_hau = ["Dutse", "Kogi", "Kasa", "Gida", "Fili",
             "Sama", "Tauraro", "Fadama", "Bazara", "Daji",
             "Tafkin", "Yashi", "Iska", "Ruwan Sama", "Hayi",
             "Ruwa", "Mutum", "Wuta", "Ganye", "Hanya",
             "Dare", "Ya'yan Itace", "Tsuntsu", "Maciji", "Kauye",
             "Tudu", "Daki", "Ruhu", "Fitila", "Soja",
             "Kwari", "Gari", "Katako", "Rana", "Hanya",
             "Birni", "Gada", "Firist", "Kabari", "Tsinewa",
             "Haihuwa", "Ciyawa"]

adj_hau = ["Mai Kyau", "Fari", "Mai Tsarki", "Boye", "Karami",
           "Tsoho", "Babba", "Mugu", "Ja", "Shudi"
            "Kore", "Rawaya", "Baki", "Jarumi", "Mai Zurfi"
            "Mai Haske", "Mai Nauyi", "Mai Kaifi",
            "Mai Nisa", "Mai Fadi",
            "Mai Duhu", "Dogo", "Mai Sanyi", "Mai Dumi"]

# ==========================   NOMES DAS PROVÍNCIAS EM SWAHILI   ==========================#

nouns_sua_c1 = ["Mwanajeshi", "Mchungaji"]

nouns_sua_c3 = ["Mlima", "Mto", "Msitu", "Mchanga", "Mwamba",
                "Moto", "Mwanga", "Mteremko", "Mji", "Mwitu",
                "Mgongo", "Mwatuko", "Mzizi", "Msalaba"]

nouns_sua_c5 = ["Jiwe", "Pango", "Anga", "Bwawa", "Ziwa",
                "Hori", "Bwana", "Jani", "Tunda", "Shamba",
                "Bonde", "Kimbilio", "Daraja", "Jini", "Kanisa",
                "Jiji"]

nouns_sua_c7 = ["Kisima", "Kichaka", "Kijiji", "Kilima", "Kibanda",
                "Kilele"]

nouns_sua_c9 = ["Nchi", "Nyumba", "Nyota", "Mvua", "Chemchem",
                "Hewa", "Njia", "Ndege", "Nyoka", "Mbwa Mwito",
                "Roho", "Kando", "Siku", "Ishara", "Barabara",
                "Kaburi", "Ardhi"]

nouns_sua_c11 = ["Uwanja", "Udongo", "Upepo", "Unyasi"]

adj_sua_c1 = ["Mwema", "Mweupe", "Mtakatifu", "Mvunjika", "Mfichwa",
              "Mdogo", "Mdogo", "Mzee", "Mbinguni", "Mkubwa",
              "Mrefu", "Mdogo", "Mkubwa", "Msafi", "Mbaya",
              "Mwekundu", "Mbuluu", "Mkijani", "Mnjano", "Mweusi",
              "Mdhahabu", "Mtulivu", "Mkelele", "Mkavu", "Mpotea",
              "Mkina", "Mangavu", "Mzito", "Mfuraha", "Msiri",
              "Msonga", "Mgawanyika", "Mpendeza", "Mburudisha", "Manguka",
              "Mkali", "Mbali", "Mkale", "Mhuzuni", "Mzuri",
              "Mraruka", "Madhimu", "Mjua", "Mgiza", "Mwima",
              "Mpole", "Mamani", "Mvurugu", "Mkali", "Mpana",
              "Mwazi", "Mfungwa", "Mbapa", "Mgiza", "Milele",
              "Mtulivu", "Mkubwa", "Mzuri", "Mrefu", "Mkelele",
              "Mbaridi", "Mjoto", "Mhatari", "Mpumbaza", "Mchonga",
              "Msafi", "Mjasiri", "Milele", "Mganda", "Mkufa"]

adj_sua_c3 = ["Mwema", "Mweupe", "Mtakatifu", "Mvunjika", "Mfichwa",
              "Mdogo", "Mdogo", "Mzee", "Mbinguni", "Mkubwa",
              "Mrefu", "Mdogo", "Mkubwa", "Msafi", "Mbaya",
              "Mwekundu", "Mbuluu", "Mkjani", "Mnjano", "Mweusi",
              "Mdhahabu", "Mtulivu", "Mkelele", "Mkavu", "Mpotea",
              "Mkina", "Mangavu", "Mzito", "Mfuraha", "Msiri",
              "Msonga", "Mgawanyika", "Mpendeza", "Mburudisha", "Manguka",
              "Mkali", "Mbali", "Mkale", "Mhuzuni", "Mzuri",
              "Mraruka", "Madhimu", "Mjua", "Mgiza", "Mwima",
              "Mpole", "Mmani", "Mvurugu", "Mkali", "Mpana",
              "Mwazi", "Mfungwa", "Mbapa", "Mgiza", "Milele",
              "Mtulivu", "Mkubwa", "Mzuri", "Mrefu", "Mkelele",
              "Mbaridi", "Mjoto", "Mhatari", "Mpumbaza", "Mchonga",
              "Msafi", "Mjasiri", "Milele", "Mganda", "Mkufa"]

adj_sua_c5 = ["Jema", "Jeupe", "Takatifu", "Vunjika", "Fichwa",
              "Dogo", "Dogo", "Zee", "Mbinguni", "Kubwa",
              "Refu", "Dogo", "Kubwa", "Safi", "Baya",
              "Jekundu", "Buluu", "Kijani", "Njano", "Jeusi",
              "Dhahabu", "Tulivu", "Kelele", "Kavu", "Potea",
              "Refu", "Angavu", "Zito", "Furaha", "Siri",
              "Songa", "Gawanyika", "Pendeza", "Burudisha", "Anguka",
              "Kali", "Mbali", "Kale", "Huzuni", "Zuri",
              "Raruka", "Adhimu", "Jua", "Giza", "Wima",
              "Mpole", "Amani", "Vurugu", "Kali", "Pana",
              "Wazi", "Fungwa", "Bapa", "Giza", "Milele",
              "Tulivu", "Kubwa", "Zuri", "Refu", "Kelele",
              "Baridi", "Joto", "Hatari", "Pumbaza", "Chonga",
              "Safi", "Jasiri", "Milele", "Ganda", "Kufa"]

adj_sua_c7 = ["Kizuri", "Kyeupe", "Kitakatifu", "Kivunjika", "Kifichika",
              "Kidogo", "Kidogo", "Kikongwe", "Kimbingu", "Kikubwa",
              "Kirefu", "Kidogo", "Kikubwa", "Kisafi", "Kibaya",
              "Kikundu", "Kibuluu", "Kijani", "Kinanjano", "Kyeusi",
              "Kidhahabu", "Kitulivu", "Kelele", "Kavu", "Kipotea",
              "Kina", "Kangavu", "Kizito", "Kifuraha", "Kiujabu",
              "Kisonga", "Kigawanyika", "Kipendeza", "Kipooza", "Kianguka",
              "Kikali", "Kimbali", "Kikale", "Kihuzuni", "Kizuri",
              "Kiraruka", "Kifalme", "Kijua", "Kigiza", "Kishuka",
              "Kipole", "Kiamani", "Kiturbulent", "Kikali", "Kipan",
              "Ki wazi", "Kifungwa", "Kibapa", "Kigiza", "Kisicho Na Mwisho",
              "Kitulivu", "Kijitu", "Kizuri", "Kirefu", "Kenye Sauti Kubwa",
              "Kibaridi", "Kijoto", "Kihatari", "Kivutia", "Kichongwa",
              "Kisafi", "Kijasiri", "Kidaima", "Kikamilifu", "Kimfu"]

adj_sua_c9 = ["Nzuri", "Nyeupe", "Takatifu", "Vunjika", "Fichwa",
              "Ndogo", "Ndogo", "Nzee", "Nbinguni", "Nkubwa",
              "Nrefu", "Ndogo", "Nkubwa", "Nsafi", "Nbaya",
              "Nyekundu", "Nbuluu", "Nkijani", "Nnjano", "Njeusi",
              "Ndahabu", "Ntulivu", "Nkelele", "Nkavu", "Npotea",
              "Nrefu", "Nangavu", "Nzito", "Nfuraha", "Nsiri",
              "Nsonga", "Ngawanyika", "Npendeza", "Nburudisha", "Nanguka",
              "Nkali", "Nmbali", "Nkale", "Nhuzuni", "Nzuri",
              "Nraruka", "Nadhimu", "Njua", "Ngiza", "Nwima",
              "Nmpole", "Namani", "Nvurugu", "Nkali", "Npana",
              "Nwazi", "Nfungwa", "Nbapa", "Ngiza", "Nmilele",
              "Ntulivu", "Nkubwa", "Nzuri", "Nrefu", "Nkelele",
              "Nbaridi", "Njoto", "Nhatari", "Npumbaza", "Nchonga",
              "Nsafi", "Njasiri", "Nmilele", "Nganda", "Nkufa"]

adj_sua_c11 = ["Uzuri", "Ueupe", "Utakatifu", "Unywele", "Uficho",
               "Udogo", "Udogo", "Uzee", "Ubinguni", "Ukubwa",
               "Urefu", "Udogo", "Ukubwa", "Usafi", "Ubayo",
               "Uekundu", "Ubuluu", "Ukijani", "Unjano", "Ueusi",
               "Udhahabu", "Utulivu", "Ukelele", "Ukavu", "Upotea",
               "Urefu", "Uangavu", "Uzito", "Ufuraha", "Usiri",
               "Usonga", "Ugawanyika", "Upendeza", "Uburudisha", "Uanguka",
               "Ukali", "Umbali", "Ukale", "Uhuzuni", "Uzuri",
               "Uraruka", "Uadhimu", "Ujua", "Ugiza", "Uwima",
               "Upole", "Uamani", "Uvurugu", "Ukali", "Upana",
               "Uwazi", "Ufungwa", "Ubapa", "Ugiza", "Umilele",
               "Utulivu", "Ukubwa", "Uzuri", "Urefu", "Ukelele",
               "Ubaridi", "Ujoto", "Uhatari", "Upumbaza", "Uchonga",
               "Usafi", "Ujasiri", "Umilele", "Uganda", "Ukufa"]

# ==========================   NOMES DAS PROVÍNCIAS EM PORTUGUÊS   ==========================#

nouns_por_mas = ["Rio", "Campo", "Céu", "Pântano", "lago", "Solo",
                 "Vento", "Penhasco", "Homem", "Ar", "Fogo", "Pássaro",
                 "Morro", "Riacho", "Lobo", "Espírito", "Soldado",
                 "Vale", "Monte", "Dia", "Pico", "Refúgio",
                 "Sinal", "Arbusto", "Sacerdote", "Terreno", "Gramado",
                 "Feitiço", "Jardim"]

nouns_por_fem = ["Pedra", "Montanha", "Terra", "Casa", "Caverna",
                 "Estrela", "Nascente", "Floresta", "Areia",
                 "Chuva", "Escarpa", "Fonte", "Água", "Gruta",
                 "Folha", "Trilha", "Noite", "Fruta", "Serpente",
                 "Vila", "Cabana", "Campina", "Luz", "Barra",
                 "Serra", "Cidade", "Mata", "Lagoa", "Estrada",
                 "Capela", "Ponte", "Cova", "Vista"]

adj_por_mas = ["Bom", "Branco", "Sagrado", "Quebrado", "Escondido",
               "Longo", "Pequeno", "Velho", "Paradisíaco", "Grande",
               "Alto", "Pristino", "Mau",
               "Vermelho", "Azul", "Verde", "Amarelo", "Preto",
               "Dourado", "Calmo", "Seco", "Perdido", "Bravio",
               "Profundo", "Brilhante", "Pesado", "Alegre", "Misterioso",
               "Petrificado", "Dividido", "Agradável", "Cadente",
               "Afiado", "Distante", "Antigo", "Triste", "Bonito",
               "Eterno", "Encantado", "Ensolarado", "Frio", "Íngrime",
               "Gentil", "Pacífico", "Turbulento", "Morto", "Amplo",
               "Aberto", "Fechado", "Plano", "Escuro", "Quente",
               "Sereno", "Gigante", "Puro"]

adj_por_fem = ["Boa", "Branca", "Sagrada", "Quebrada", "Escondida",
               "Longa", "Pequena", "Velha", "Paradisíaca", "Grande",
               "Alta", "Pristina", "Má",
               "Vermelha", "Azul", "Verde", "Amarela", "Preta",
               "Dourada", "Calma", "Seca", "Perdida", "Bravia",
               "Profunda", "Brilhante", "Pesada", "Alegre", "Misteriosa",
               "Petrificada", "Dividida", "Agradável", "Cadente",
               "Afiada", "Distante", "Antiga", "Triste", "Bonita",
               "Eterna", "Encantada", "Ensolarada", "Fria", "Íngrime",
               "Gentil", "Pacífica", "Turbulenta", "Morta", "Ampla",
               "Aberta", "Fechada", "Plana", "Escura", "Quente",
               "Serena", "Gigante", "Pura"]

# ==========================   NOMES DAS PROVÍNCIAS EM TELUGU   ==========================#

adj_tel = ["Manchi", "Telupu", "PavitraMaina", "Virigina", "Dachina",
           "Podavaine", "Chinna", "Pata", "Devatal", "Pedda",
           "Ettaina", "Pristine", "Chedu",
           "Erupu", "Neelam", "Aakupacha", "Pasupu", "Nalupu",
           "Bangaru", "Uppika", "Poyina", "Dhairyanga",
           "Lothaina", "Prakasince", "Bharinga", "AnandakarMaina", "RahasyaMaina",
           "Oragina", "VibhajinchaBadina", "AahladaKaramaina", "Kooling", "Pade",
           "Padunaine", "Dooramaina", "Praachina", "Vipulu", "Andamaina",
           "ShashvataMaina", "MantramugdhaMaina", "EndaKaala", "Challani", "Nitaaaruga",
           "Susaadyam", "Shantamaina", "KuduPulaaga", "Chanipoina", "VistaraMaina",
           "Terichina", "Moochina", "SamataTa", "Cheekati", "VechaNani",
           "Telikapaatia", "Daitamt", "Parishuddha"]

nouns_tel = ["Parvatam", "Nakshatram", "Vasanta", "Sarassu",
             "Varsham", "Uuta", "Paadam", "Phalam",
             "Pakshi", "Grama", "Konda", "Vaagu", "Cheruvu",
             "Meda", "Metta", "EluguBanti",
             "Vampu", "Sainikudu", "Gutta", "Pattanam", "Agni",
             "Shikharam", "Chenulo", "Puli", "Poojari",
             "Raayi", "Nadi", "Guha", "Isuka", "Matti",
             "Raatri", "Paamu", "Loya", "Adavi",
             "Poda", "Thota", "Kaanti",
             "Bhumi", "Drushti", "Gali",
             "Illu", "Aakasham", "Neeru", "Dinam", "Kunta",
             "Pullu", "Aaka", "Ashrayam", "Suchakam", "Palakame",
             "Shaapam", "Podavu", "Nagaram", "Atma"]

# ==========================   NOMES DAS PROVÍNCIAS EM BENGALI   ==========================#

adj_ben = ["Bhalo", "Shada", "Pabitra", "Bhanga", "Lukiye",
               "Lomba", "Puraono", "Swargiya", "Boro",
               "Ucca", "Chhoto", "Nirmal", "Kharaap",
               "Lal", "Neel", "Shobuj", "Holud", "Kalo",
               "Swarna", "Shanto", "Shukna", "Hariye", "Sahasik",
               "Gahiro", "Ujjwal", "Bhari", "Anandomoy", "Rahasyojano",
               "Kothin", "Bhenge", "Sundor", "Shitala",
               "Tikto", "Duro", "Prachin", "Dukho",
               "Chironton", "Mohaishwarya", "Roudro", "Thanda", "Khar",
               "Komal", "Shanti", "Ashanto", "Mrito", "Chowra",
               "Khola", "Bondho", "Andhakar", "Garam",
               "Santo", "Bipul"]

nouns_ben = ["Pahar", "Nodi", "Bhumi", "Bari",
                 "Math", "Guhar", "Akash", "Tara", "Jheel",
                 "Jhorna", "Bon", "Hrida", "Balu", "Mati",
                 "Hawa", "Brishti", "Ku", "Fowara", "Jol",
                 "Manush", "Udyan", "Bayu", "Agun", "Pata",
                 "Potht", "Raat", "Fol", "Pakhi", "Saanp",
                 "Gram", "Tila", "Chhara", "Jhupi",
                 "Atma", "Aalo", "Shar",
                 "Upoth", "Tapaswi",
                 "Upottok", "Teerthashala", "Nagor",
                 "Raka", "Din", "Parbat",
                 "Chinho", "Jhop",
                 "Pukure", "Rasta", "Palakame", "Nagar",
                 "Setu", "Pujari", "Shoshan", "Shopath",
                 "Drishti", "Ghass"]

# ==========================   NOMES DAS PROVÍNCIAS EM JAPONÊS   ==========================#

adj_jap = [
    "Yoi", "Shiroi", "Shinseina", "Kowareta", "Kakushita",
    "Nagai", "Chiisana", "Furui", "Ten no", "Ookii",
    "Takai", "Chiisana", "Ookii", "Kiyoi", "Warui",
    "Akai", "Aoi", "Midori no", "Kiiroi", "Kuroi",
    "Kin'iro no", "Odayaka na", "Kawaita", "Ushinawareta", "Yuukan na",
    "Fukai", "Akarui", "Omoi", "Ureshii", "Nazo no",
    "Ishika shita", "Wakareta", "Tanoshii", "Reitou shita", "Ochiru",
    "Surudoi", "Tooi", "Kodai no", "Kanashii", "Utsukushii",
    "Eien no", "Maho ni kakerareta", "Hareta", "Samui", "Kyu",
    "Yasashii", "Heiwa na", "Arasoi no", "Shinda", "Hiroi",
    "Akeru", "Shimeru", "Taira na", "Kurai", "Atatakai",
    "Shizuka na", "Kyo na", "Junsei"
]

nouns_jap = [
    "Iwa", "Yama", "Kawa", "Chi", "Ie",
    "Hatake", "Horaana", "Sora", "Hoshi", "Numachi",
    "Izumi", "Mori", "Mizuumi", "Suna", "Tsuchi",
    "Kaze", "Ame", "Gake", "Izumi", "Mizu",
    "Otoko", "Hayashi", "Kuki", "Hi", "Ha",
    "Michi", "Yoru", "Kudamono", "Tori", "Hebi",
    "Machi", "Oka", "Kawa", "Koya", "No",
    "Ookami", "Seirei", "Hikari", "Saka", "Heishi",
    "Tani", "Tsuka", "Machi",
    "Hayashi", "Mine", "Hi", "Takane",
    "Hinansho", "Hyoushiki", "Shigeru",
    "Ike", "Michi", "Kyokai", "Toshi",
    "Hashi", "Shisai", "Haka", "Noroi",
    "Ji", "Keshiki", "Shiba"
]

# ==========================   NOMES DAS PROVÍNCIAS EM MARATHI   ==========================#

adj_mar_mas = [
    "Changla", "Pandhra", "Pavitra", "Tuta", "Laplele",
    "Lamb", "Chhota", "Juna", "Swargiya", "Motha",
    "Uccha", "Chhota", "Motha", "Nirmal", "Vait",
    "Lal", "Neela", "Hirva", "Pivla", "Kala",
    "Soneri", "Shanta", "Sukha", "Haravlela", "Shur",
    "Khola", "Tej", "Jadh", "Anandi", "Gudh",
    "Shila", "Vibhag", "Sukhada", "Shital", "Padnara",
    "Tikshna", "Durcha", "Prachin", "Dukhi", "Sundar",
    "Anadi", "Jadui", "Divasli", "Thanda", "Kadar",
    "Mild", "Shanta", "Gunj", "Mela", "Vishal",
    "Ughad", "Band", "Sad", "Andhara", "Garam",
    "Sthir", "Bhim", "Shuddha"
]

adj_mar_fem = [
    "Changli", "Pandhri", "Pavitra", "Tuti", "Lapleleli",
    "Lambi", "Chhoti", "Juni", "Swargiya", "Mothi",
    "Ucchi", "Chhoti", "Mothi", "Nirmal", "Vait",
    "Lali", "Neeli", "Hiravi", "Pivli", "Kali",
    "Soneri", "Shanti", "Sukhi", "Haravleli", "Shur",
    "Khola", "Tej", "Jadhi", "Anandi", "Gudh",
    "Shila", "Vibhag", "Sukhada", "Shital", "Padnari",
    "Tikshni", "Durchi", "Prachin", "Dukhi", "Sundar",
    "Anadi", "Jadui", "Divasli", "Thandi", "Kadak",
    "Mild", "Shanti", "Gunji", "Meli", "Vishal",
    "Ughadi", "Band", "Sad", "Andhari", "Garam",
    "Sthir", "Bhim", "Shuddha"
]

adj_mar_neu = [
    "Changle", "Pandhre", "Pavitra", "Tute", "Laplelele",
    "Lambe", "Chhote", "June", "Swargiya", "Mothe",
    "Ucche", "Chhote", "Mothe", "Nirmal", "Vait",
    "Lale", "Neel", "Hirve", "Pivle", "Kale",
    "Soneri", "Shant", "Sukhe", "Haravlele", "Shur",
    "Khol", "Tej", "Jadh", "Anand", "Gudh",
    "Shil", "Vibhag", "Sukhada", "Shital", "Padnar",
    "Tikshne", "Durcha", "Prachin", "Dukh", "Sundar",
    "Anad", "Jadui", "Divasle", "Thand", "Kadak",
    "Mild", "Shant", "Gunje", "Mel", "Vishal",
    "Ughad", "Band", "Sad", "Andhar", "Garam",
    "Sthir", "Bhim", "Shuddha"
]

nouns_mar_mas = [
    "Khadak", "Parvat", "Ghar", "Shet", "Aakash",
    "Jangal", "Vara", "Paus", "Kada", "Purush",
    "Van", "Pan", "Phal", "Pakshi", "Saap",
    "Gav", "Dongar", "Landga", "Atma", "Sainik",
    "Khor", "Shahar", "Pul", "Pujari", "Shap",
    "Drushya", "Gavat"
]

nouns_mar_fem = [
    "Nadi", "Zamin", "Guha", "Tara", "Chikhal",
    "Jhara", "Valu", "Mati", "Hawa", "Aag",
    "Paulwat", "Ratra", "Zhopdi", "Kuran",
    "Dhig", "Chinha", "Zhudup"
]

nouns_mar_neu = [
    "Karanje", "Pani", "Talav", "Shikhar", "Aashray"
]

# ==========================   NOMES DAS PROVÍNCIAS EM COREANO   ==========================#

adj_cor = [
    "Joeun", "Hayan", "Shinseonghan", "Buseojin", "Sumgyeojin",
    "Gin", "Jageun", "Oraedoen", "Cheonsang-ui", "Keun",
    "Nop-eun", "Jageun", "Keun", "Wonsh-ui", "Nappeun",
    "Ppalgan", "Paran", "Chorok-ui", "Noran", "Geom-eun",
    "Geumsaeg-ui", "Pyeong-onhan", "Geonjohan", "Il-eobeolin", "Yong-gamhan",
    "Gip-eun", "Balgeun", "Mugeoun", "Jeulgeoun", "Shinbihan",
    "Seoghwadwin", "Bunyeol-dwin", "Jeulgeoun", "Siwonhan", "Tteoreojineun",
    "Nalkaroun", "Meolli Inneun", "Godae-ui", "Seulpeun", "Areumdaun",
    "Yeong-wonhan", "Mabeob-e Geollin", "Malgeun", "Chuun", "Gapareun",
    "Budeureoun", "Pyeonghwaro-un", "Gyeokdongjeogin", "Jukeun", "Neolbeun",
    "Yeollin", "Dat-eun", "Pyeongpyeonghan", "Eoduun", "Ttatteushan",
    "Goyohan", "Geodaehan", "Sunsuhan"
]

nouns_cor = [
    "Bawi", "San", "Gang", "Jigu", "Jip",
    "Bat", "Donggul", "Haneul", "Byeol", "Neup",
    "Saem", "Sup", "Ho", "Morae", "To",
    "Baram", "Bi", "Jeolbyeok", "Sup", "Mul",
    "Namja", "Sogeum", "Gonggi", "Bul", "Ip",
    "Gil", "Bam", "Gwail", "Sae", "Baem",
    "Ma-eul", "Eondeok", "Cheon", "Jjokbang", "Pyeongan",
    "Neukdae", "Yeonghon", "Bit", "Gyeon", "Gundae",
    "Gok", "Hwasal", "Doshi",
    "Sanrim", "Gogae", "Nal", "Jeomjeong",
    "Bigae", "Pyo", "Namuguri",
    "Mot", "Gildo", "Seongdang", "Dosi",
    "Dari", "Seongnyun", "Myoji", "Ju",
    "Bam", "Gyeong", "Pul"
]

# ==========================   NOMES DAS PROVÍNCIAS EM ITALIANO   ==========================#

adj_ita_mas = [
    "Buono", "Bianco", "Sacro", "Rotto", "Nascosto",
    "Lungo", "Vecchio", "Celeste", "Grande",
    "Alto", "Piccolo", "Puro", "Cattivo",
    "Rosso", "Blu", "Verde", "Giallo", "Nero",
    "Dorato", "Calmo", "Secco", "Perso", "Coraggioso",
    "Profondo", "Luminoso", "Pesante", "Gioioso", "Misterioso",
    "Pietrificato", "Diviso", "Piacevole", "Rinfrescante", "Cadente",
    "Affilato", "Distante", "Antico", "Triste", "Bello",
    "Eterno", "Incantato", "Soleggiato", "Freddo", "Ripido",
    "Gentile", "Pacifico", "Turbulento", "Morto", "Ampio",
    "Aperto", "Chiuso", "Piatto", "Scuro", "Caldo",
    "Sereno", "Gigantesco", "Puro"
]

adj_ita_fem = [
    "Buona", "Bianca", "Sacra", "Rotta", "Nascosta",
    "Lunga", "Piccola", "Vecchia", "Celeste",
    "Alta", "Grande", "Pura", "Cattiva",
    "Rossa", "Blu", "Verde", "Gialla", "Nera",
    "Dorata", "Calma", "Secca", "Persa", "Coraggiosa",
    "Profonda", "Luminosa", "Pesante", "Gioiosa", "Misteriosa",
    "Pietrificata", "Divisa", "Piacevole", "Rinfrescante", "Cadente",
    "Affilata", "Distante", "Antica", "Triste", "Bella",
    "Eterna", "Incantata", "Soleggiata", "Fredda", "Ripida",
    "Gentile", "Pacifica", "Turbulenta", "Morta", "Ampia",
    "Aperta", "Chiusa", "Piatta", "Scura", "Calda",
    "Serena", "Gigantesca", "Pura"
]

nouns_ita_mas = [
    "Fiume", "Campo", "Cielo", "Lago", "Vento",
    "Uomo", "Boschetto", "Fuoco", "Sentiero", "Uccello",
    "Ruscello", "Prato", "Lupo", "Spirito",
    "Pendio", "Soldato", "Tumulo", "Bosco", "Giorno",
    "Rifugio", "Segno", "Cespuglio", "Stagno",
    "Sacerdote", "Terreno"
]

nouns_ita_fem = [
    "Roccia", "Montagna", "Terra", "Casa",
    "Caverna", "Stella", "Palude", "Sorgente",
    "Foresta", "Sabbia", "Pioggia", "Scogliera",
    "Fontana", "Acqua", "Aria", "Foglia", "Ponte",
    "Notte", "Frutta", "Cittadina", "Collina",
    "Capanna", "Luce", "Valle", "Città", "Serpente",
    "Cresta", "Cima", "Strada", "Cappella",
    "Tomba", "Maledizione", "Vista", "Erba"
]

ita_bags = [
    "Buono", "Grande", "Piccolo", "Vecchio", "Bello",
    "Buona", "Piccola", "Vecchia", "Bella"
]

# ==========================   NOMES DAS PROVÍNCIAS EM ALEMÃO   ==========================#

adj_ale_mas = [
    "Guter", "Weißer", "Heiliger", "Gebrochener", "Versteckter",
    "Langer", "Kleiner", "Alter", "Himmlischer", "Großer",
    "Hoher", "Kleiner", "Großer", "Makelloser", "Schlechter",
    "Roter", "Blauer", "Grüner", "Gelber", "Schwarzer",
    "Goldener", "Ruhiger", "Trockener", "Verlorener", "Tapferer",
    "Tiefer", "Heller", "Schwerer", "Fröhlicher", "Geheimnisvoller",
    "Versteinerter", "Geteilter", "Angenehmer", "Erfrischender", "Fallender",
    "Scharfer", "Ferns", "Alter", "Trauriger", "Schöner",
    "Ewiger", "Verzauberter", "Sonniger", "Kalter", "Steiler",
    "Sanfter", "Friedlicher", "Stürmischer", "Toter", "Weiter",
    "Offener", "Geschlossener", "Flacher", "Dunkler", "Warmer",
    "Heiterer", "Gigantischer", "Reiner"
]

adj_ale_fem = [
    "Gute", "Weiße", "Heilige", "Gebrochene", "Versteckte",
    "Lange", "Kleine", "Alte", "Himmlische", "Große",
    "Hohe", "Kleine", "Große", "Makellose", "Schlechte",
    "Rote", "Blaue", "Grüne", "Gelbe", "Schwarze",
    "Goldene", "Ruhige", "Trockene", "Verlorene", "Tapfere",
    "Tiefe", "Helle", "Schwere", "Fröhliche", "Geheimnisvolle",
    "Versteinerte", "Geteilte", "Angenehme", "Erfrischende", "Fallende",
    "Scharfe", "Ferne", "Alte", "Traurige", "Schöne",
    "Ewige", "Verzauberte", "Sonnige", "Kalte", "Steile",
    "Sanfte", "Friedliche", "Stürmische", "Tote", "Weite",
    "Offene", "Geschlossene", "Flache", "Dunkle", "Warme",
    "Heitere", "Gigantische", "Reine"
]

adj_ale_neu = [
    "Gutes", "Weißes", "Heiliges", "Gebrochenes", "Verstecktes",
    "Langes", "Kleines", "Altes", "Himmlisches", "Großes",
    "Hohes", "Kleines", "Großes", "Makelloses", "Schlechtes",
    "Rotes", "Blaues", "Grünes", "Gelbes", "Schwarzes",
    "Goldenes", "Ruhiges", "Trockenes", "Verlorenes", "Tapferes",
    "Tiefes", "Helles", "Schweres", "Fröhliches", "Geheimnisvolles",
    "Versteinertes", "Geteiltes", "Angenehmes", "Erfrischendes", "Fallendes",
    "Scharfes", "Fernes", "Altes", "Trauriges", "Schönes",
    "Ewiges", "Verzaubertes", "Sonniges", "Kaltes", "Steiles",
    "Sanftes", "Friedliches", "Stürmisches", "Totes", "Weites",
    "Offenes", "Geschlossenes", "Flaches", "Dunkles", "Warmes",
    "Heiteres", "Gigantisches", "Reines"
]

nouns_ale_mas = [
    "Felsen", "Berg", "Fluss", "Wind", "Regen",
    "Brunnen", "Mann", "Hain", "Feuer", "Pfad",
    "Vogel", "Bach", "Wolf", "Geist",
    "Hang", "Soldat", "Grat", "Tag",
    "Gipfel", "Busch", "Teich", "Priester",
    "Fluch", "Boden"
]

nouns_ale_fem = [
    "Höhle", "Klippe", "Quelle", "Wiese", "Luft",
    "Nacht", "Frucht", "Schlange", "Stadt", "Straße",
    "Kapelle", "Brücke", "Zuflucht", "Aussicht",
    "Erde"
]

nouns_ale_neu = [
    "Land", "Haus", "Feld", "Himmel", "Stern",
    "Sumpf", "See", "Sand", "Wasser", "Blatt",
    "Licht", "Tal", "Zeichen",
    "Grab", "Gras"
]

# ==========================   CONSTRUIR FUNÇÕES DOS NOMES DAS CAPITAIS E PROVÍNCIAS   ==========================#

def formar_nome_chines(adj_chi, nouns_chi):
    adj = random.choice(adj_chi)
    noun = random.choice(nouns_chi)
    nome = adj + " " + noun
    return nome


def formar_nome_indonesio(nouns_ind, adj_ind):
    noun = random.choice(nouns_ind)
    adj = random.choice(adj_ind)
    nome = noun + " " + adj
    return nome


def formar_nome_vietnamita(nouns_viet, adj_viet):
    noun = random.choice(nouns_viet)
    adj = random.choice(adj_viet)
    nome = noun + " " + adj
    return nome


def formar_nome_hindi(adj_hin_mas, adj_hin_fem, nouns_hin_mas, nouns_hin_fem):
    lista_combinada = nouns_hin_mas + nouns_hin_fem
    noun = random.choice(lista_combinada)
    if noun in nouns_hin_mas:
        adj = random.choice(adj_hin_mas)
    else:
        adj = random.choice(adj_hin_fem)
    nome = adj + " " + noun
    return nome


def formar_nome_farsi(nouns_far, adj_far):
    noun = random.choice(nouns_far)
    adj = random.choice(adj_far)
    nome = noun + " " + adj
    return nome


def formar_nome_arabe(nouns_ara_mas, nouns_ara_fem, adj_ara_mas, adj_ara_fem):
    lista_combinada = nouns_ara_mas + nouns_ara_fem
    noun = random.choice(lista_combinada)
    if noun in nouns_ara_mas:
        adj = random.choice(adj_ara_mas)
    else:
        adj = random.choice(adj_ara_fem)
    nome = noun + " " + adj
    return nome


def formar_nome_russo(adj_rus_mas, adj_rus_fem, adj_rus_neu, nouns_rus_mas, nouns_rus_fem, nouns_rus_neu):
    lista_combinada = nouns_rus_mas + nouns_rus_fem + nouns_rus_neu
    noun = random.choice(lista_combinada)
    if noun in nouns_rus_mas:
        adj = random.choice(adj_rus_mas)
    elif noun in nouns_rus_fem:
        adj = random.choice(adj_rus_fem)
    else:
        adj = random.choice(adj_rus_neu)
    nome = adj + " " + noun
    return nome


def formar_nome_suaili(nouns_sua_c1, nouns_sua_c3, nouns_sua_c5, nouns_sua_c7, nouns_sua_c9, nouns_sua_c11, adj_sua_c1,
                       adj_sua_c3, adj_sua_c5, adj_sua_c7, adj_sua_c9, adj_sua_c11):
    lista_combinada = nouns_sua_c1 + nouns_sua_c3 + nouns_sua_c5 + nouns_sua_c7 + nouns_sua_c9 + nouns_sua_c11
    noun = random.choice(lista_combinada)
    if noun in nouns_sua_c1:
        adj = random.choice(adj_sua_c1)
    elif noun in nouns_sua_c3:
        adj = random.choice(adj_sua_c3)
    elif noun in nouns_sua_c5:
        adj = random.choice(adj_sua_c5)
    elif noun in nouns_sua_c7:
        adj = random.choice(adj_sua_c7)
    elif noun in nouns_sua_c9:
        adj = random.choice(adj_sua_c9)
    else:
        adj = random.choice(adj_sua_c11)
    nome = noun + " " + adj
    return nome


def formar_nome_turco(adj_tur, nouns_tur):
    adj = random.choice(adj_tur)
    noun = random.choice(nouns_tur)
    nome = adj + " " + noun
    return nome


def formar_nome_frances(adj_fra_mas, adj_fra_fem, bags, nouns_fra_mas, nouns_fra_fem):
    lista_combinada = nouns_fra_mas + nouns_fra_fem
    noun = random.choice(lista_combinada)
    if noun in nouns_fra_mas:
        adj = random.choice(adj_fra_mas)
    else:
        adj = random.choice(adj_fra_fem)
    if adj in bags:
        nome = adj + " " + noun
    else:
        nome = noun + " " + adj
    return nome


def formar_nome_hausa(nouns_hau, adj_hau):
    noun = random.choice(nouns_hau)
    adj = random.choice(adj_hau)
    nome = noun + " " + adj
    return nome


def formar_nome_ingles(adj_ing, nouns_ing):
    adj = random.choice(adj_ing)
    noun = random.choice(nouns_ing)
    nome = adj + " " + noun
    return nome


def formar_nome_espanhol(nouns_esp_mas, nouns_esp_fem, adj_esp_mas, adj_esp_fem):
    lista_combinada = nouns_esp_mas + nouns_esp_fem
    noun = random.choice(lista_combinada)
    if noun in nouns_esp_mas:
        adj = random.choice(adj_esp_mas)
    else:
        adj = random.choice(adj_esp_fem)
    nome = noun + " " + adj
    return nome

def formar_nome_portugues(nouns_por_mas, nouns_por_fem, adj_por_mas, adj_por_fem):
    lista_combinada = nouns_por_mas + nouns_por_fem
    noun = random.choice(lista_combinada)
    if noun in nouns_por_mas:
        adj = random.choice(adj_por_mas)
    else:
        adj = random.choice(adj_por_fem)
    nome = noun + " " + adj
    return nome

def formar_nome_telugu(adj_tel, nouns_tel):
    adj = random.choice(adj_tel)
    noun = random.choice(nouns_tel)
    nome = adj + " " + noun
    return nome

def formar_nome_bengali(adj_ben, nouns_ben):
    adj = random.choice(adj_ben)
    noun = random.choice(nouns_ben)
    nome = adj + " " + noun
    return nome

def formar_nome_japones(adj_jap, nouns_jap):
    adj = random.choice(adj_jap)
    noun = random.choice(nouns_jap)
    nome = adj + " " + noun
    return nome

def formar_nome_marathi(adj_mar_mas, adj_mar_fem, adj_mar_neu, nouns_mar_mas, nouns_mar_fem, nouns_mar_neu):
    lista_combinada = nouns_mar_mas + nouns_mar_fem + nouns_mar_neu
    noun = random.choice(lista_combinada)
    if noun in nouns_mar_mas:
        adj = random.choice(adj_mar_mas)
    elif noun in nouns_mar_fem:
        adj = random.choice(adj_mar_fem)
    else:
        adj = random.choice(adj_mar_neu)
    nome = adj + " " + noun
    return nome

def formar_nome_coreano(adj_cor, nouns_cor):
    adj = random.choice(adj_cor)
    noun = random.choice(nouns_cor)
    nome = adj + " " + noun
    return nome

def formar_nome_italiano(nouns_ita_mas, nouns_ita_fem, adj_ita_mas, adj_ita_fem):
    lista_combinada = nouns_ita_mas + nouns_ita_fem
    noun = random.choice(lista_combinada)
    if noun in nouns_ita_mas:
        adj = random.choice(adj_ita_mas)
    else:
        adj = random.choice(adj_ita_fem)
    if adj in ita_bags:
        nome = adj + " " + noun
    else:
        nome = noun + " " + adj
    return nome

def formar_nome_alemao(adj_ale_mas, adj_ale_fem, adj_ale_neu, nouns_ale_mas, nouns_ale_fem, nouns_ale_neu):
    lista_combinada = nouns_ale_mas + nouns_ale_fem + nouns_ale_neu
    noun = random.choice(lista_combinada)
    if noun in nouns_ale_mas:
        adj = random.choice(adj_ale_mas)
    elif noun in nouns_ale_fem:
        adj = random.choice(adj_ale_fem)
    else:
        adj = random.choice(adj_ale_neu)
    nome = adj + " " + noun
    return nome

def formar_nome_wu(adj_wu, nouns_wu):
    adj = random.choice(adj_wu)
    noun = random.choice(nouns_wu)
    nome = adj + " " + noun
    return nome

######################################################################################################################

def formar_nome(cultura):
    if cultura == "Chinese":
        return formar_nome_chines(adj_chi, nouns_chi)
    elif cultura == "Indonesian":
        return formar_nome_indonesio(nouns_ind, adj_ind)
    elif cultura == "Vietnamese":
        return formar_nome_vietnamita(nouns_viet, adj_viet)
    elif cultura == "Indian":
        return formar_nome_hindi(adj_hin_mas, adj_hin_fem, nouns_hin_mas, nouns_hin_fem)
    elif cultura == "Persian":
        return formar_nome_farsi(nouns_far, adj_far)
    elif cultura == "Arabic":
        return formar_nome_arabe(nouns_ara_mas, nouns_ara_fem, adj_ara_mas, adj_ara_fem)
    elif cultura == "Russian":
        return formar_nome_russo(adj_rus_mas, adj_rus_fem, adj_rus_neu, nouns_rus_mas, nouns_rus_fem, nouns_rus_neu)
    elif cultura == "Swahili":
        return formar_nome_suaili(
            nouns_sua_c1, nouns_sua_c3, nouns_sua_c5,
            nouns_sua_c7, nouns_sua_c9, nouns_sua_c11,
            adj_sua_c1, adj_sua_c3, adj_sua_c5,
            adj_sua_c7, adj_sua_c9, adj_sua_c11
        )
    elif cultura == "Turkish":
        return formar_nome_turco(adj_tur, nouns_tur)
    elif cultura == "French":
        return formar_nome_frances(adj_fra_mas, adj_fra_fem, bags, nouns_fra_mas, nouns_fra_fem)
    elif cultura == "Hausa":
        return formar_nome_hausa(nouns_hau, adj_hau)
    elif cultura == "English":
        return formar_nome_ingles(adj_ing, nouns_ing)
    elif cultura == "Portuguese":
        return formar_nome_portugues(nouns_por_mas, nouns_por_fem, adj_por_mas, adj_por_fem)
    elif cultura == "Telugu":
        return formar_nome_telugu(adj_tel, nouns_tel)
    elif cultura == "Bengali":
        return formar_nome_bengali(adj_ben, nouns_ben)
    elif cultura == "Japanese":
        return formar_nome_japones(adj_jap, nouns_jap)
    elif cultura == "Marathi":
        return formar_nome_marathi(adj_mar_mas, adj_mar_fem, adj_mar_neu, nouns_mar_mas, nouns_mar_fem, nouns_mar_neu)
    elif cultura == "Korean":
        return formar_nome_coreano(adj_cor, nouns_cor)
    elif cultura == "Italian":
        return formar_nome_italiano(nouns_ita_mas, nouns_ita_fem, adj_ita_mas, adj_ita_fem)
    elif cultura == "German":
        return formar_nome_alemao(adj_ale_mas, adj_ale_fem, adj_ale_neu, nouns_ale_mas, nouns_ale_fem, nouns_ale_neu)
    elif cultura == "Wu":
        return formar_nome_wu(adj_wu, nouns_wu)
    elif cultura == "Yue":
        return formar_nome_wu(adj_yue, nouns_yue)
    elif cultura == "Min":
        return formar_nome_wu(adj_min, nouns_min)
    else:
        return formar_nome_espanhol(nouns_esp_mas, nouns_esp_fem, adj_esp_mas, adj_esp_fem)
