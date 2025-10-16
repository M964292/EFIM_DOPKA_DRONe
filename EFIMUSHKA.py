import random
import time


class FPVQuizGame:
    def __init__(self):
        self.score = 0
        self.questions_answered = 0
        self.components_learned = set()
        self.transfer_code = ""

        # База данных компонентов FPV дронов (расширенная)
        self.components = {
            "Фрейм (рама)": {
                "description": 'Основа дрона, к которой крепятся все компоненты. Бывают разных размеров (3", 5" и т.д.)',
                "image": """
          ┌─────┐
          │ │
          │ X │
          │ │
          └─────┘
        Карбоновая рама
                """,
                "function": "Служит основой для крепления всех компонентов дрона. Определяет его размер, прочность и аэродинамику.",
                "facts": [
                    "Материал: углеродное волокно (карбон)",
                    "Размер измеряется в дюймах по диагонали",
                    "Форма: X, H, крест, гибрид",
                    "Вес рамы влияет на маневренность дрона",
                ],
            },
            "Мотор": {
                "description": "Электродвигатель, который вращает пропеллеры. Измеряется в kV (обороты на вольт)",
                "image": """
          ┌──────────┐
          │ 🧲🧲🧲 │
          │ 🧲 🧲 │
                  🧲🧲🧲 │
          └──────────┘
          Бесколлекторный мотор
                """,
                "function": "Вращает пропеллеры, создавая подъемную силу. Чем выше kV - тем выше скорость вращения.",
                "facts": [
                    "Тип: бесколлекторный (BLDC)",
                    "Бывают разных размеров: 2207, 2306 и т.д.",
                    "Чем выше kV - тем выше скорость вращения",
                    "Количество полюсов влияет на плавность работы",
                ],
            },
            "Пропеллер (проп)": {
                "description": "Лопасти, создающие подъемную силу. Имеют разный шаг и диаметр",
                "image": """
           /\\
          / \\
         / \\
        /______\\
          Пропеллер
                """,
                "function": "Создает подъемную силу при вращении. Размер и форма влияют на тягу и эффективность полета.",
                "facts": [
                    "Материал: пластик, нейлон, карбон",
                    'Маркировка: 5x4.3 (5" диаметр, 4.3" шаг)',
                    "Бывают 2, 3, 4, 5 и более лопастей",
                    "Балансировка пропеллеров важна для вибраций",
                ],
            },
            "Регулятор хода (ESC)": {
                "description": "Управляет скоростью моторов. Преобразует сигнал с полетного контроллера",
                "image": """
          ┌──────────┐
          │ ESC │
          │ ┌────┐ │
          │ │ │ │
          └──┴────┴──┘
          4-in-1 регулятор
                """,
                "function": "Управляет скоростью вращения моторов на основе сигналов с полетного контроллера.",
                "facts": [
                    "Бывают отдельные и 4-in-1",
                    "Измеряются в амперах (A): 30A, 45A, 60A",
                    "Прошивка: BLHeli, Bluejay, KISS",
                    "Частота ШИМ влияет на плавность работы моторов",
                ],
            },
            "Полетный контроллер (FC)": {
                "description": "Мозг дрона. Обрабатывает данные с датчиков и управляет моторами",
                "image": """
          ┌──────────┐
          │ FC │
          │ 🎯 🎯 🎯 │
          │ 🎯 🎯 🎯 │
          └──────────┘
         Полетный контроллер
                """,
                "function": "Обрабатывает данные с датчиков и пульта управления, стабилизирует дрон в полете.",
                "facts": [
                    "Прошивка: Betaflight, Emuflight, KISS",
                    "Имеет гироскоп и акселерометр",
                    "Разъемы: UART, I2C, PWM",
                    "Частота процессора влияет на скорость реакции",
                ],
            },
            "Камера FPV": {
                "description": "Передает видео с дрона на шлем. Имеет широкий угол обзора",
                "image": """
          ┌──────────┐
          │ ___ │
          │ / \\ │
          │ \\___/ │
          └──────────┘
          FPV камера
                """,
                "function": "Передает видео в реальном времени на FPV шлем пилота, создавая эффект полета от первого лица.",
                "facts": [
                    "Разрешение: TVL (аналог) или цифровое",
                    "Угол обзора: 120-180 градусов",
                    "Форм-фактор: Micro, Nano, Full-size",
                    "Сенсор: CCD или CMOS",
                ],
            },
            "Видеопередатчик (VTX)": {
                "description": "Передает видео сигнал с камеры на шлем пилота",
                "image": """
          ┌──────────┐
          │ VTX │
          │ 📡 │
          │ ⚡⚡⚡⚡ │
          └──────────┘
         Видеопередатчик
                """,
                "function": "Передает видео сигнал с камеры на FPV шлем на частоте 5.8GHz.",
                "facts": [
                    "Мощность: 25mW, 200mW, 800mW, 1W+",
                    "Частоты: 5.8GHz каналы",
                    "Протоколы: Analog, HDZero, Walksnail, DJI",
                    "Антенны: линейная, круговая поляризация",
                ],
            },
            "Аккумулятор (LiPo)": {
                "description": "Литий-полимерный аккумулятор, питающий дрон",
                "image": """
          ┌──────────┐
          │ LiPo │
          │ ██████ │
          │ ██████ │
          └──────────┘
          4S 1500mAh
                """,
                "function": "Обеспечивает питание всех систем дрона. Определяет время полета и мощность.",
                "facts": [
                    "Напряжение: 1S, 2S, 3S, 4S, 6S (1S=3.7V)",
                    "Емкость: mAh (миллиампер-часы)",
                    "Разряд: C-рейтинг (50C, 100C, 150C)",
                    "Балансировка ячеек важна для долговечности",
                ],
            },
            "Приемник (RX)": {
                "description": "Получает сигнал с пульта управления и передает на полетный контроллер",
                "image": """
          ┌──────────┐
          │ RX │
          │ 📶 │
          │ ⚡ │
          └──────────┘
          Приемник 2.4GHz
                """,
                "function": "Принимает команды с пульта управления и передает их на полетный контроллер.",
                "facts": [
                    "Протоколы: FrSky, Crossfire, ELRS, TBS",
                    "Частоты: 2.4GHz, 900MHz, 5.8GHz",
                    "Антенны: внутренние, внешние, разнополяризованные",
                    "Задержка сигнала влияет на отзывчивость управления",
                ],
            },
            "Антенна": {
                "description": "Передает и принимает сигнал между дроном и пультом/шлемом",
                "image": """
            /\\
           / \\
          / \\
         /------\\
          Антенна
                """,
                "function": "Усиливает и направляет радиосигнал для лучшего приема и передачи.",
                "facts": [
                    "Типы: линейная, круговая поляризация",
                    "Коэффициент усиления измеряется в dBi",
                    "Диаграмма направленности влияет на зону покрытия",
                    "Поляризация влияет на качество сигнала при наклонах",
                ],
            },
            "Контроллер полета GPS": {
                "description": "Модуль GPS для навигации и автоматического удержания позиции",
                "image": """
          ┌──────────┐
          │ GPS │
          │ 🛰️ │
          │ ⚡⚡ │
          └──────────┘
          GPS модуль
                """,
                "function": "Обеспечивает точное позиционирование дрона в пространстве, позволяет использовать автономные режимы.",
                "facts": [
                    "Поддерживает GPS, GLONASS, Galileo",
                    "Точность позиционирования: 1-2 метра",
                    "Позволяет использовать Return-to-Home",
                    "Количество спутников влияет на точность",
                ],
            },
        }

        # Популярные модели дронов (расширенный список)
        self.drones = {
            "DJI FPV": {
                "type": "Готовый дрон",
                "description": "Готовый FPV дрон от DJI с цифровой системой",
                "features": [
                    "4K камера",
                    "Цифровая FPV система",
                    "GPS",
                    "Ассистенты полета",
                ],
                "image": """
              ┌──────────┐
              │ ___ │
              │ / \\ │
              │ \\___/ │
              │ / | | \\ │
              └──────────┘
                DJI FPV
                """,
                "function": "Готовый к полетам дрон с цифровой FPV системой, отлично подходит для начинающих.",
            },
            "iFlight Nazgul5": {
                "type": 'Квадрокоптер 5"',
                "description": "Популярный BNF (Bind-N-Fly) дрон для гонок",
                "features": [
                    "Карбоновая рама",
                    "Бесколлекторные моторы",
                    "Аналоговая FPV система",
                ],
                "image": """
              ┌──────────┐
              │ X │
              │ / \\ │
              │ \\___/ │
              │ / | | \\ │
              └──────────┘
              iFlight Nazgul5
                """,
                "function": "Дрон для гонок с отличным соотношением цены и качества, требует отдельной покупки пульта.",
            },
            "Tiny Whoop": {
                "type": "Мини дрон",
                "description": "Маленький дрон для полетов в помещении",
                "features": ["Защитный дуг", "Маленький размер", "Безопасен для дома"],
                "image": """
              ┌──────────┐
              │ ()() │
              │ / \\ │
              │ \\____/ │
              │ │
              └──────────┘
              Tiny Whoop
                """,
                "function": "Миниатюрный дрон для полетов в помещении, безопасен благодаря защитному дугу.",
            },
            "Cinewhoop": {
                "type": "Киносъемочный дрон",
                "description": "Дрон для аэросъемки с защищенными пропеллерами",
                "features": ["Защитные кольца", "Плавный полет", "Камера на подвесе"],
                "image": """
              ┌──────────┐
              │ [][] │
              │ / \\ │
              │ \\____/ │
              │ [][] │
              └──────────┘
                Cinewhoop
                """,
                "function": "Специализированный дрон для видеосъемки с защитой пропеллеров для безопасности.",
            },
            "Long Range Drone": {
                "type": "Дрон дальнего действия",
                "description": "Дрон для полетов на большие расстояния",
                "features": ["Большие пропеллеры", "Эффективные моторы", "Система GPS"],
                "image": """
              ┌──────────┐
              │ ___ │
              │ / \\ │
              │ \\___/ │
              │ / \\ │
              └──────────┘
              Long Range
                """,
                "function": "Дрон оптимизированный для полетов на большие расстояния с увеличенным временем полета.",
            },
        }

        # Модели пультов управления
        self.controllers = {
            "RadioMaster TX12": {
                "description": "Бюджетный пульт с цветным дисплеем",
                "price_range": "$$",
                "features": ["Color LCD", "4-in-1 module", "EdgeTX"],
                "views": {
                    "front": """
        ┌─────────────────────────┐
        │ RADIOMASTER TX12 │
        │ │
        │ ( ) ( ) │
        │ / \\ / \\ │
        │ │
        │ ┌─────────────────┐ │
        │ │ │ │
        │ │ LCD 2.4" │ │
        │ │ │ │
        │ └─────────────────┘ │
        │ │
        │ [SWA] [SWB] [SWC] [SWD]│
        │ [SWE] [SWF] [SWG] [SWH]│
        │ │
        │ [ ] [ ] [ ] [ ] [ ] │
        │ │
        │ [ ] [ ] │
        └─────────────────────────┘
                    """,
                    "side": """
              ┌───────┐
              │ │
              │ ( ) │
              │ / \\ │
              │ │
              │ LCD │
              │ │
              │[SWA] │
              │ │
              └───────┘
           Боковой вид TX12
                    """,
                },
            },
            "TBS Tango 2": {
                "description": "Компактный игровой пульт для FPV",
                "price_range": "$$$",
                "features": ["Compact", "Hall gimbals", "Crossfire"],
                "views": {
                    "front": """
          ┌─────────────────┐
          │ TBS TANGO 2 │
          │ │
          │ ( ) ( ) │
          │ / \\ / \\ │
          │ │
          │ ┌───────┐ │
          │ │ LCD │ │
          │ └───────┘ │
          │ │
          │ [ ] [ ] [ ] │
          │ │
          └─────────────────┘
                    """,
                    "side": """
              ┌───────┐
              │ │
              │ ( ) │
              │ / \\ │
              │ │
              │ LCD │
              │ │
              │ [ ] │
              │ │
              └───────┘
           Боковой вид Tango 2
                    """,
                },
            },
            "DJI FPV Remote Controller 2": {
                "description": "Пульт для DJI FPV системы",
                "price_range": "$$$$",
                "features": ["Low latency", "Ergonomic", "OcuSync"],
                "views": {
                    "front": """
          ┌─────────────────┐
          │ DJI FPV RC2 │
          │ │
          │ ┌───────┐ │
          │ │ │ │
          │ │ LCD │ │
          │ │ │ │
          │ └───────┘ │
          │ │
          │ ( ) ( ) │
          │ / \\ / \\ │
          │ │
          │ [ ] [ ] [ ] │
          └─────────────────┘
                    """,
                    "side": """
              ┌───────┐
              │ │
              │ ( ) │
              │ / \\ │
              │ │
              │ LCD │
              │ │
              │ [ ] │
              │ │
              └───────┘
           Боковой вид DJI RC2
                    """,
                },
            },
        }

        # Модели FPV шлемов
        self.goggles = {
            "DJI FPV Goggles 2": {
                "description": "Цифровой шлем от DJI",
                "price_range": "$$$$",
                "features": ["Digital HD", "Low latency", "OcuSync"],
                "views": {
                    "front": """
          ┌─────────────────┐
          │ DJI GOGGLES 2 │
          │ ####### ##### │
          │ # ## #│
          │ # # 🖥 #│
          │ # ## #│
          │ ####### ##### │
          │ │ │ │
          │ └────────┘ │
          │ [ANT] [PWR] [⚙] │
          │ [CH-] [CH+] │
          └─────────────────┘
                    """,
                    "side": """
          ┌─────────────┐
          │ _____ │
          │ / \\ │
          │ / 🖥 \\ │
          │ \\ / │
          │ \\_____/ │
          │ │
          │ [РЕГУЛИР] │
          └─────────────┘
          Боковой вид DJI Goggles 2
                    """,
                },
            },
            "FatShark Dominator": {
                "description": "Классический аналоговый шлем",
                "price_range": "$$$",
                "features": ["Analog", "Modular", "Lightweight"],
                "views": {
                    "front": """
          ┌─────────────────┐
          │ FATSHARK DOMIN. │
          │ #### #### │
          │ # # # # │
          │ # # # # │
          │ #### #### │
          │ │ │ │
          │ └────────┘ │
          │ [ ] [PWR] [⚙] │
          │ [CH-] [CH+] │
          └─────────────────┘
                    """,
                    "side": """
          ┌─────────────┐
          │ _____ │
          │ / \\ │
          │ / 👁 \\ │
          │ \\ / │
          │ \\_____/ │
          │ │
          │ [ФОКУС] │
          └─────────────┘
          Боковой вид FatShark
                    """,
                },
            },
            "Skyzone Sky04X": {
                "description": "Шлем с OLED дисплеями",
                "price_range": "$$$$",
                "features": ["OLED", "Diversity", "HDMI"],
                "views": {
                    "front": """
          ┌─────────────────┐
          │ SKYZONE SKY04X │
          │ ##### ##### │
          │ # ## # │
          │ # # 🖥 # │
          │ # ## # │
          │ ##### ##### │
          │ │ │ │
          │ └────────┘ │
          │ [ANT] [PWR] [⚙] │
          │ [CH-] [CH+] │
          └─────────────────┘
                    """,
                    "side": """
          ┌─────────────┐
          │ _____ │
          │ / \\ │
          │ / 🖥 \\ │
          │ \\ / │
          │ \\_____/ │
          │ │
          │ [ДИОПТР] │
          └─────────────┘
          Боковой вид Skyzone
                    """,
                },
            },
        }

    def show_menu(self):
        """Главное меню игры"""
        while True:
            print("\n" + "=" * 50)
            print("🎯 FPV ДРОНЫ: ВИКТОРИНА И ОБУЧЕНИЕ 🎯")
            print("=" * 50)
            print("1 - Викторина: Угадай компонент")
            print("2 - Викторина: Угадай дрон")
            print("3 - Обучалка: Компоненты FPV дрона")
            print("4 - Осмотреть FPV пульты")
            print("5 - Осмотреть FPV шлемы")
            print("6 - Передача данных на другой телефон")
            print("7 - Статистика")
            print("0 - Выйти")
            print("=" * 50)

            choice = input("Выберите пункт (0-7): ").strip()

            if choice == "1":
                self.quiz_components()
            elif choice == "2":
                self.quiz_drones()
            elif choice == "3":
                self.learning_components()
            elif choice == "4":
                self.show_controllers()
            elif choice == "5":
                self.show_goggles_collection()
            elif choice == "6":
                self.data_transfer()
            elif choice == "7":
                self.show_stats()
            elif choice == "0":
                print("Спасибо за изучение FPV дронов! 🚁")
                break
            else:
                print("Неверный выбор! Используйте цифры 0-7.")

    def quiz_components(self):
        """Викторина: угадай компонент по описанию с улучшенной рандомизацией"""
        print("\n" + "=" * 50)
        print("🧩 ВИКТОРИНА: УГАДАЙ КОМПОНЕНТ ДРОНА")
        print("=" * 50)

        components = list(self.components.keys())
        random.shuffle(components)

        # Случайное количество вопросов от 3 до 8
        num_questions = random.randint(3, min(8, len(components)))

        for i, component in enumerate(components[:num_questions], 1):
            print(f"\nВопрос {i}/{num_questions}")

            # Случайный выбор типа вопроса
            question_type = random.choice(["description", "function", "fact"])

            if question_type == "description":
                description = self.components[component]["description"]
                print(f"ОПИСАНИЕ: {description}")
            elif question_type == "function":
                function = self.components[component]["function"]
                print(f"ФУНКЦИЯ: {function}")
            else:
                fact = random.choice(self.components[component]["facts"])
                print(f"ФАКТ: {fact}")

            print("\nВарианты ответов:")

            # Выбираем случайные неправильные ответы + правильный
            options = [component]
            wrong_options = [c for c in components if c != component]
            random.shuffle(wrong_options)

            # Случайное количество вариантов от 3 до 5
            num_options = random.randint(3, 5)
            options.extend(wrong_options[: num_options - 1])
            random.shuffle(options)

            for i, option in enumerate(options, 1):
                print(f"{i}. {option}")

            while True:
                try:
                    answer = int(input(f"\nВаш ответ (1-{num_options}): ").strip())
                    if 1 <= answer <= num_options:
                        break
                    else:
                        print(f"Пожалуйста, введите число от 1 до {num_options}")
                except ValueError:
                    print("Пожалуйста, введите число")

            print("\n" + "=" * 40)
            if options[answer - 1] == component:
                print("✅ ПРАВИЛЬНО! +10 очков")
                self.score += 10
                self.components_learned.add(component)
            else:
                print(f"❌ НЕПРАВИЛЬНО! Это был: {component}")

            self.questions_answered += 1

            # Показываем изображение компонента и его функцию
            print(self.components[component]["image"])
            print(f"\nФУНКЦИЯ: {self.components[component]['function']}")

            # Показываем случайный интересный факт
            fact = random.choice(self.components[component]["facts"])
            print(f"💡 ИНТЕРЕСНЫЙ ФАКТ: {fact}")

            print("=" * 40)

    def quiz_drones(self):
        """Викторина: угадай дрон по описанию с рандомизацией"""
        print("\n" + "=" * 50)
        print("🚁 ВИКТОРИНА: УГАДАЙ ДРОН")
        print("=" * 50)

        drones = list(self.drones.keys())
        random.shuffle(drones)

        num_questions = random.randint(2, min(4, len(drones)))

        for i, drone in enumerate(drones[:num_questions], 1):
            drone_info = self.drones[drone]
            print(f"\nВопрос {i}/{num_questions}")

            # Случайный выбор типа вопроса
            question_type = random.choice(["type", "features", "description"])

            if question_type == "type":
                print(f"ТИП ДРОНА: {drone_info['type']}")
            elif question_type == "features":
                features = random.sample(
                    drone_info["features"], min(2, len(drone_info["features"]))
                )
                print(f"ОСОБЕННОСТИ: {', '.join(features)}")
            else:
                description = drone_info["description"]
                print(f"ОПИСАНИЕ: {description}")

            options = [drone]
            wrong_options = [d for d in drones if d != drone]
            random.shuffle(wrong_options)
            options.extend(wrong_options[:2])
            random.shuffle(options)

            print("\nВарианты ответов:")
            for i, option in enumerate(options, 1):
                print(f"{i}. {option}")

            while True:
                try:
                    answer = int(input("\nВаш ответ (1-3): ").strip())
                    if 1 <= answer <= 3:
                        break
                    else:
                        print("Пожалуйста, введите число от 1 до 3")
                except ValueError:
                    print("Пожалуйста, введите число")

            print("\n" + "=" * 30)
            if options[answer - 1] == drone:
                print("✅ ПРАВИЛЬНО! +15 очков")
                self.score += 15
            else:
                print(f"❌ НЕПРАВИЛЬНО! Это был: {drone}")

            self.questions_answered += 1

            print(drone_info["image"])
            print(f"\nНАЗНАЧЕНИЕ: {drone_info['function']}")

            print("=" * 30)

    def learning_components(self):
        """Обучалка по компонентам FPV дрона"""
        print("\n" + "=" * 50)
        print("📚 ОБУЧАЛКА: КОМПОНЕНТЫ FPV ДРОНА")
        print("=" * 50)

        components = list(self.components.keys())
        random.shuffle(components)  # Рандомный порядок изучения

        while True:
            print("\nВыберите компонент для изучения:")
            for i, component in enumerate(components, 1):
                learned = "✅" if component in self.components_learned else " "
                print(f"{learned} {i}. {component}")
            print("0. Назад в меню")

            try:
                choice = int(input("\nВаш выбор: ").strip())
                if choice == 0:
                    return
                elif 1 <= choice <= len(components):
                    component = components[choice - 1]
                    self.show_component_info(component)
                    self.components_learned.add(component)
                else:
                    print("Неверный выбор!")
            except ValueError:
                print("Пожалуйста, введите число")

    def show_component_info(self, component):
        """Показать подробную информацию о компоненте"""
        info = self.components[component]

        print("\n" + "=" * 50)
        print(f"🔧 {component.upper()}")
        print("=" * 50)
        print(info["image"])
        print(f"\n📝 ОПИСАНИЕ: {info['description']}")
        print(f"\n⚙️ ФУНКЦИЯ: {info['function']}")
        print("\n💡 ИНТЕРЕСНЫЕ ФАКТЫ:")
        for fact in info["facts"]:
            print(f"• {fact}")

        print("\n0 - Возврат в обучалку")
        while True:
            cmd = input().strip()
            if cmd == "0":
                return

    def show_controllers(self):
        """Показ коллекции FPV пультов"""
        print("\n" + "=" * 50)
        print("🎮 КОЛЛЕКЦИЯ FPV ПУЛЬТОВ")
        print("=" * 50)

        controllers = list(self.controllers.keys())

        while True:
            print("\nВыберите пульт для осмотра:")
            for i, controller in enumerate(controllers, 1):
                print(f"{i}. {controller}")
            print("0. Назад в меню")

            try:
                choice = int(input("\nВаш выбор: ").strip())
                if choice == 0:
                    return
                elif 1 <= choice <= len(controllers):
                    controller = controllers[choice - 1]
                    self.show_controller_details(controller)
                else:
                    print("Неверный выбор!")
            except ValueError:
                print("Пожалуйста, введите число")

    def show_controller_details(self, controller):
        """Показать детали пульта"""
        info = self.controllers[controller]

        print("\n" + "=" * 50)
        print(f"🎮 {controller.upper()}")
        print("=" * 50)
        print(f"📋 Описание: {info['description']}")
        print(f"💰 Ценовой диапазон: {info['price_range']}")
        print(f"⭐ Особенности: {', '.join(info['features'])}")

        print("\n1. Вид спереди:")
        print(info["views"]["front"])

        print("\n2. Вид сбоку:")
        print(info["views"]["side"])

        print("\n0 - Возврат к списку пультов")
        while True:
            cmd = input().strip()
            if cmd == "0":
                return

    def show_goggles_collection(self):
        """Показ коллекции FPV шлемов"""
        print("\n" + "=" * 50)
        print("🥽 КОЛЛЕКЦИЯ FPV ШЛЕМОВ")
        print("=" * 50)

        goggles_list = list(self.goggles.keys())

        while True:
            print("\nВыберите шлем для осмотра:")
            for i, goggle in enumerate(goggles_list, 1):
                print(f"{i}. {goggle}")
            print("0. Назад в меню")

            try:
                choice = int(input("\nВаш выбор: ").strip())
                if choice == 0:
                    return
                elif 1 <= choice <= len(goggles_list):
                    goggle = goggles_list[choice - 1]
                    self.show_goggle_details(goggle)
                else:
                    print("Неверный выбор!")
            except ValueError:
                print("Пожалуйста, введите число")

    def show_goggle_details(self, goggle):
        """Показать детали шлема"""
        info = self.goggles[goggle]

        print("\n" + "=" * 50)
        print(f"🥽 {goggle.upper()}")
        print("=" * 50)
        print(f"📋 Описание: {info['description']}")
        print(f"💰 Ценовой диапазон: {info['price_range']}")
        print(f"⭐ Особенности: {', '.join(info['features'])}")

        print("\n1. Вид спереди:")
        print(info["views"]["front"])

        print("\n2. Вид сбоку:")
        print(info["views"]["side"])

        print("\n0 - Возврат к списку шлемов")
        while True:
            cmd = input().strip()
            if cmd == "0":
                return

    def data_transfer(self):
        """Система передачи данных на другой телефон"""
        print("\n" + "=" * 50)
        print("📡 ПЕРЕДАЧА ДАННЫХ НА ДРУГОЙ ТЕЛЕФОН")
        print("=" * 50)

        if not self.components_learned:
            print("❌ У вас нет изученных компонентов для передачи!")
            print("Сначала изучите компоненты в обучалке или викторине.")
            print("\n0 - Возврат в меню")
            input()
            return

        # Создаем код передачи
        components_str = ",".join(sorted(self.components_learned))
        self.transfer_code = f"FPV{self.score:04d}{len(self.components_learned):02d}"

        print("✅ Данные готовы к передаче!")
        print(f"📊 Ваш счет: {self.score}")
        print(f"📚 Изучено компонентов: {len(self.components_learned)}")
        print(f"🔢 Код передачи: {self.transfer_code}")

        print("\n" + "=" * 30)
        print("📲 КАК ПЕРЕДАТЬ ДАННЫЕ:")
        print("1. Запомните код передачи выше")
        print("2. На другом телефоне запустите эту программу")
        print("3. Выберите 'Передача данных' -> 'Получить данные'")
        print("4. Введите код передачи")
        print("=" * 30)

        print("\n1. Создать новый код")
        print("2. Получить данные по коду")
        print("0. Назад в меню")

        choice = input("\nВаш выбор: ").strip()

        if choice == "1":
            # Генерируем новый код
            new_code = (
                f"FPV{random.randint(1000, 9999)}{len(self.components_learned):02d}"
            )
            self.transfer_code = new_code
            print(f"🆕 Новый код создан: {new_code}")
            print("Передайте этот код другу!")
        elif choice == "2":
            self.receive_data()
        elif choice == "0":
            return

    def receive_data(self):
        """Получение данных по коду"""
        print("\n" + "=" * 50)
        print("📥 ПОЛУЧЕНИЕ ДАННЫХ ОТ ДРУГОГО ИГРОКА")
        print("=" * 50)

        code = input("Введите код передачи: ").strip().upper()

        if len(code) != 9 or not code.startswith("FPV"):
            print("❌ Неверный формат кода!")
            return

        try:
            score = int(code[3:7])
            components_count = int(code[7:9])

            print(f"✅ Данные успешно получены!")
            print(f"🏆 Счет друга: {score}")
            print(f"📚 Изучено компонентов: {components_count}")

            if score > self.score:
                print("🎯 Ваш друг знает больше вас! Продолжайте учиться!")
            else:
                print("⭐ Вы знаете больше своего друга! Так держать!")

            # "Импортируем" несколько компонентов
            available_components = [
                c for c in self.components.keys() if c not in self.components_learned
            ]
            if available_components:
                imported = random.sample(
                    available_components, min(2, len(available_components))
                )
                for comp in imported:
                    self.components_learned.add(comp)
                print(f"📖 Вы узнали о новых компонентах: {', '.join(imported)}")

        except ValueError:
            print("❌ Ошибка в коде передачи!")

    def show_stats(self):
        """Показать статистику игрока"""
        print("\n" + "=" * 50)
        print("📊 ВАША СТАТИСТИКА")
        print("=" * 50)
        print(f"🏆 Общий счет: {self.score} очков")
        print(f"❓ Отвечено вопросов: {self.questions_answered}")
        print(
            f"📚 Изучено компонентов: {len(self.components_learned)}/{len(self.components)}"
        )

        if self.components_learned:
            print("\n✅ Изученные компоненты:")
            for component in sorted(self.components_learned):
                print(f" • {component}")

        if self.transfer_code:
            print(f"\n🔗 Код передачи: {self.transfer_code}")
        else:
            print("\n🔗 Код передачи: не создан")

        # Прогресс изучения
        progress = len(self.components_learned) / len(self.components) * 100
        print(f"\n📈 Прогресс изучения: {progress:.1f}%")

        if progress < 25:
            print("🎯 Статус: Начинающий пилот")
        elif progress < 50:
            print("🎯 Статус: Любитель FPV")
        elif progress < 75:
            print("🎯 Статус: Опытный пилот")
        else:
            print("🎯 Статус: FPV Эксперт!")

        print("\n0 - Возврат в меню")
        cmd = input().strip()
        while cmd != "0":
            cmd = input().strip()


# Запуск программы
if __name__ == "__main__":
    print("Добро пожаловать в мир FPV дронов!")
    print("Изучайте компоненты, проходите викторины и становитесь экспертом!")
    game = FPVQuizGame()
    game.show_menu()
