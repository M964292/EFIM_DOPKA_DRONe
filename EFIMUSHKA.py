# app.py

from flask import Flask, request, render_template_string, redirect, url_for
import random
import os # Добавляем для получения PORT

# --- Класс игры (остаётся без изменений, кроме методов отображения) ---
class FPVQuizGame:
    def __init__(self):
        self.score = 0
        self.questions_answered = 0
        self.components_learned = set()
        self.transfer_code = ""

        # --- База данных компонентов (остаётся без изменений) ---
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

        # --- Популярные модели дронов (остаётся без изменений) ---
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

        # --- Модели пультов управления (остаётся без изменений) ---
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
          │ ┌─────┐ │
          │ │ LCD │ │
          │ └─────┘ │
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
          │ ┌─────┐ │
          │ │ │ │
          │ │ LCD │ │
          │ │ │ │
          │ └─────┘ │
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

        # --- Модели FPV шлемов (остаётся без изменений) ---
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
        """Возвращает HTML-страницу с главным меню"""
        menu_html = f"""
        <html>
        <head>
            <title>🎯 FPV ДРОНЫ: Викторина и Обучение</title>
            <style>
                body {{ font-family: Arial, sans-serif; background-color: #f0f0f0; margin: 0; padding: 20px; }}
                .container {{ max-width: 800px; margin: auto; background-color: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
                h1 {{ color: #2c3e50; text-align: center; }}
                .menu-item {{ margin: 10px 0; padding: 10px; background-color: #3498db; color: white; text-decoration: none; display: block; text-align: center; border-radius: 5px; }}
                .menu-item:hover {{ background-color: #2980b9; }}
                .stats {{ margin-top: 20px; padding: 10px; background-color: #ecf0f1; border-radius: 5px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🎯 FPV ДРОНЫ: Викторина и Обучение 🎯</h1>
                <a href="/quiz_components" class="menu-item">1 - Викторина: Угадай компонент</a>
                <a href="/quiz_drones" class="menu-item">2 - Викторина: Угадай дрон</a>
                <a href="/learning_components" class="menu-item">3 - Обучалка: Компоненты FPV дрона</a>
                <a href="/show_controllers" class="menu-item">4 - Осмотреть FPV пульты</a>
                <a href="/show_goggles" class="menu-item">5 - Осмотреть FPV шлемы</a>
                <a href="/data_transfer" class="menu-item">6 - Передача данных на другой телефон</a>
                <a href="/stats" class="menu-item">7 - Статистика</a>
                <div class="stats">
                    <p><strong>Счет:</strong> {self.score}</p>
                    <p><strong>Отвечено вопросов:</strong> {self.questions_answered}</p>
                    <p><strong>Изучено компонентов:</strong> {len(self.components_learned)}/{len(self.components)}</p>
                </div>
            </div>
        </body>
        </html>
        """
        return menu_html

    def quiz_components(self):
        """Возвращает HTML-страницу с викториной компонентов"""
        components = list(self.components.keys())
        random.shuffle(components)
        num_questions = random.randint(3, min(8, len(components)))

        questions_html = ""
        for i, component in enumerate(components[:num_questions], 1):
            question_type = random.choice(["description", "function", "fact"])
            if question_type == "description":
                text = self.components[component]["description"]
            elif question_type == "function":
                text = self.components[component]["function"]
            else:
                text = random.choice(self.components[component]["facts"])

            options = [component]
            wrong_options = [c for c in components if c != component]
            random.shuffle(wrong_options)
            num_options = random.randint(3, 5)
            options.extend(wrong_options[: num_options - 1])
            random.shuffle(options)

            options_html = ""
            for j, opt in enumerate(options, 1):
                options_html += f'<input type="radio" name="q{i}" value="{opt}" required> {opt}<br>'

            questions_html += f"""
            <div style="margin-bottom: 20px;">
                <h3>Вопрос {i}/{num_questions}</h3>
                <p><strong>{question_type.upper()}:</strong> {text}</p>
                <div>
                    {options_html}
                </div>
            </div>
            """

        quiz_html = f"""
        <html>
        <head>
            <title>🧩 Викторина: Угадай компонент</title>
            <style>
                body {{ font-family: Arial, sans-serif; background-color: #f0f0f0; margin: 0; padding: 20px; }}
                .container {{ max-width: 800px; margin: auto; background-color: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
                .back {{ margin-top: 20px; }}
                .back a {{ color: #3498db; text-decoration: none; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🧩 Викторина: Угадай компонент дрона</h1>
                <form method="POST">
                    {questions_html}
                    <input type="hidden" name="num_questions" value="{num_questions}">
                    <input type="hidden" name="components" value="{'|'.join(components[:num_questions])}">
                    <input type="submit" value="Отправить ответы">
                </form>
                <div class="back"><a href="/">← Назад в меню</a></div>
            </div>
        </body>
        </html>
        """
        return quiz_html

    def handle_quiz_components_submit(self, form_data):
        """Обрабатывает отправку формы викторины компонентов"""
        num_questions = int(form_data.get('num_questions', 0))
        components_str = form_data.get('components', '')
        submitted_components = components_str.split('|')

        score_increment = 0
        results_html = "<h2>Результаты викторины:</h2>"
        for i in range(1, num_questions + 1):
            user_answer = form_data.get(f'q{i}')
            correct_answer = submitted_components[i - 1]

            if user_answer == correct_answer:
                result = "✅ ПРАВИЛЬНО!"
                score_increment += 10
                self.components_learned.add(correct_answer)
            else:
                result = f"❌ НЕПРАВИЛЬНО! Правильный ответ: {correct_answer}"

            self.questions_answered += 1

            # Получаем информацию о компоненте для отображения
            comp_info = self.components[correct_answer]
            results_html += f"""
            <div style="margin-bottom: 20px;">
                <p>{result}</p>
                <pre>{comp_info['image']}</pre>
                <p><strong>Функция:</strong> {comp_info['function']}</p>
                <p><strong>Интересный факт:</strong> {random.choice(comp_info['facts'])}</p>
            </div>
            """

        self.score += score_increment
        results_html += f"<p><strong>Получено очков за раунд:</strong> {score_increment}</p>"

        results_page = f"""
        <html>
        <head>
            <title>Результаты викторины</title>
            <style>
                body {{ font-family: Arial, sans-serif; background-color: #f0f0f0; margin: 0; padding: 20px; }}
                .container {{ max-width: 800px; margin: auto; background-color: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
                .back a {{ color: #3498db; text-decoration: none; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Результаты викторины</h1>
                {results_html}
                <p><a href="/">← Назад в меню</a></p>
            </div>
        </body>
        </html>
        """
        return results_page

    # --- НОВАЯ РЕАЛИЗАЦИЯ: Викторина дронов ---
    def quiz_drones(self):
        """Возвращает HTML-страницу с викториной дронов"""
        drones = list(self.drones.keys())
        random.shuffle(drones)
        num_questions = random.randint(2, min(4, len(drones)))

        questions_html = ""
        for i, drone in enumerate(drones[:num_questions], 1):
            drone_info = self.drones[drone]
            question_type = random.choice(["type", "features", "description"])
            if question_type == "type":
                text = drone_info["type"]
            elif question_type == "features":
                features = random.sample(drone_info["features"], min(2, len(drone_info["features"])))
                text = ", ".join(features)
            else:
                text = drone_info["description"]

            options = [drone]
            wrong_options = [d for d in drones if d != drone]
            random.shuffle(wrong_options)
            options.extend(wrong_options[:2])
            random.shuffle(options)

            options_html = ""
            for j, opt in enumerate(options, 1):
                options_html += f'<input type="radio" name="q{i}" value="{opt}" required> {opt}<br>'

            questions_html += f"""
            <div style="margin-bottom: 20px;">
                <h3>Вопрос {i}/{num_questions}</h3>
                <p><strong>{question_type.upper()}:</strong> {text}</p>
                <div>
                    {options_html}
                </div>
            </div>
            """

        quiz_html = f"""
        <html>
        <head>
            <title>🚁 Викторина: Угадай дрон</title>
            <style>
                body {{ font-family: Arial, sans-serif; background-color: #f0f0f0; margin: 0; padding: 20px; }}
                .container {{ max-width: 800px; margin: auto; background-color: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
                .back {{ margin-top: 20px; }}
                .back a {{ color: #3498db; text-decoration: none; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🚁 Викторина: Угадай дрон</h1>
                <form method="POST">
                    {questions_html}
                    <input type="hidden" name="num_questions" value="{num_questions}">
                    <input type="hidden" name="drones" value="{'|'.join(drones[:num_questions])}">
                    <input type="submit" value="Отправить ответы">
                </form>
                <div class="back"><a href="/">← Назад в меню</a></div>
            </div>
        </body>
        </html>
        """
        return quiz_html

    def handle_quiz_drones_submit(self, form_data):
        """Обрабатывает отправку формы викторины дронов"""
        num_questions = int(form_data.get('num_questions', 0))
        drones_str = form_data.get('drones', '')
        submitted_drones = drones_str.split('|')

        score_increment = 0
        results_html = "<h2>Результаты викторины дронов:</h2>"
        for i in range(1, num_questions + 1):
            user_answer = form_data.get(f'q{i}')
            correct_answer = submitted_drones[i - 1]

            if user_answer == correct_answer:
                result = "✅ ПРАВИЛЬНО!"
                score_increment += 15
            else:
                result = f"❌ НЕПРАВИЛЬНО! Правильный ответ: {correct_answer}"

            self.questions_answered += 1

            # Получаем информацию о дроне для отображения
            drone_info = self.drones[correct_answer]
            results_html += f"""
            <div style="margin-bottom: 20px;">
                <p>{result}</p>
                <pre>{drone_info['image']}</pre>
                <p><strong>Назначение:</strong> {drone_info['function']}</p>
            </div>
            """

        self.score += score_increment
        results_html += f"<p><strong>Получено очков за раунд:</strong> {score_increment}</p>"

        results_page = f"""
        <html>
        <head>
            <title>Результаты викторины дронов</title>
            <style>
                body {{ font-family: Arial, sans-serif; background-color: #f0f0f0; margin: 0; padding: 20px; }}
                .container {{ max-width: 800px; margin: auto; background-color: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
                .back a {{ color: #3498db; text-decoration: none; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Результаты викторины дронов</h1>
                {results_html}
                <p><a href="/">← Назад в меню</a></p>
            </div>
        </body>
        </html>
        """
        return results_page

    # --- НОВАЯ РЕАЛИЗАЦИЯ: Обучалка компонентов ---
    def learning_components(self):
        """Возвращает HTML-страницу с обучалкой компонентов"""
        components = list(self.components.keys())
        random.shuffle(components) # Рандомный порядок

        components_html = ""
        for i, component in enumerate(components, 1):
            learned = "✅" if component in self.components_learned else " "
            components_html += f'<a href="/learning_component/{component}" class="menu-item">{learned} {component}</a>\n'

        learning_page = f"""
        <html>
        <head>
            <title>📚 Обучалка: Компоненты FPV дрона</title>
            <style>
                body {{ font-family: Arial, sans-serif; background-color: #f0f0f0; margin: 0; padding: 20px; }}
                .container {{ max-width: 800px; margin: auto; background-color: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
                .menu-item {{ margin: 10px 0; padding: 10px; background-color: #3498db; color: white; text-decoration: none; display: block; text-align: center; border-radius: 5px; }}
                .menu-item:hover {{ background-color: #2980b9; }}
                .back {{ margin-top: 20px; }}
                .back a {{ color: #3498db; text-decoration: none; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>📚 Обучалка: Компоненты FPV дрона</h1>
                {components_html}
                <div class="back"><a href="/">← Назад в меню</a></div>
            </div>
        </body>
        </html>
        """
        return learning_page

    def show_component_info(self, component_name):
        """Возвращает HTML-страницу с информацией о конкретном компоненте"""
        if component_name not in self.components:
            return "<h1>Компонент не найден</h1><a href='/'>← Назад в меню</a>"

        info = self.components[component_name]
        self.components_learned.add(component_name) # Отмечаем как изученное

        component_page = f"""
        <html>
        <head>
            <title>🔧 {component_name.upper()}</title>
            <style>
                body {{ font-family: Arial, sans-serif; background-color: #f0f0f0; margin: 0; padding: 20px; }}
                .container {{ max-width: 800px; margin: auto; background-color: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
                .back a {{ color: #3498db; text-decoration: none; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🔧 {component_name.upper()}</h1>
                <pre>{info['image']}</pre>
                <p><strong>Описание:</strong> {info['description']}</p>
                <p><strong>Функция:</strong> {info['function']}</p>
                <p><strong>Интересные факты:</strong></p>
                <ul>
        """
        for fact in info['facts']:
            component_page += f"<li>{fact}</li>"
        component_page += """
                </ul>
                <a href="/learning_components">← Назад к обучалке</a> | <a href="/">← Назад в меню</a>
            </div>
        </body>
        </html>
        """
        return component_page

    # --- НОВАЯ РЕАЛИЗАЦИЯ: Показ пультов ---
    def show_controllers(self):
        """Возвращает HTML-страницу с коллекцией пультов"""
        controllers = list(self.controllers.keys())

        controllers_html = ""
        for controller in controllers:
            controllers_html += f'<a href="/show_controller/{controller}" class="menu-item">{controller}</a>\n'

        controller_page = f"""
        <html>
        <head>
            <title>🎮 Коллекция FPV пультов</title>
            <style>
                body {{ font-family: Arial, sans-serif; background-color: #f0f0f0; margin: 0; padding: 20px; }}
                .container {{ max-width: 800px; margin: auto; background-color: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
                .menu-item {{ margin: 10px 0; padding: 10px; background-color: #3498db; color: white; text-decoration: none; display: block; text-align: center; border-radius: 5px; }}
                .menu-item:hover {{ background-color: #2980b9; }}
                .back a {{ color: #3498db; text-decoration: none; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🎮 Коллекция FPV пультов</h1>
                {controllers_html}
                <a href="/">← Назад в меню</a>
            </div>
        </body>
        </html>
        """
        return controller_page

    def show_controller_details(self, controller_name):
        """Возвращает HTML-страницу с деталями пульта"""
        if controller_name not in self.controllers:
            return "<h1>Пульт не найден</h1><a href='/'>← Назад в меню</a>"

        info = self.controllers[controller_name]

        controller_details_page = f"""
        <html>
        <head>
            <title>🎮 {controller_name.upper()}</title>
            <style>
                body {{ font-family: Arial, sans-serif; background-color: #f0f0f0; margin: 0; padding: 20px; }}
                .container {{ max-width: 800px; margin: auto; background-color: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
                .back a {{ color: #3498db; text-decoration: none; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🎮 {controller_name.upper()}</h1>
                <p><strong>Описание:</strong> {info['description']}</p>
                <p><strong>Ценовой диапазон:</strong> {info['price_range']}</p>
                <p><strong>Особенности:</strong> {', '.join(info['features'])}</p>
                <h3>Вид спереди:</h3>
                <pre>{info['views']['front']}</pre>
                <h3>Вид сбоку:</h3>
                <pre>{info['views']['side']}</pre>
                <a href="/show_controllers">← Назад к коллекции</a> | <a href="/">← Назад в меню</a>
            </div>
        </body>
        </html>
        """
        return controller_details_page

    # --- НОВАЯ РЕАЛИЗАЦИЯ: Показ шлемов ---
    def show_goggles(self):
        """Возвращает HTML-страницу с коллекцией шлемов"""
        goggles = list(self.goggles.keys())

        goggles_html = ""
        for goggle in goggles:
            goggles_html += f'<a href="/show_goggle/{goggle}" class="menu-item">{goggle}</a>\n'

        goggles_page = f"""
        <html>
        <head>
            <title>🥽 Коллекция FPV шлемов</title>
            <style>
                body {{ font-family: Arial, sans-serif; background-color: #f0f0f0; margin: 0; padding: 20px; }}
                .container {{ max-width: 800px; margin: auto; background-color: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
                .menu-item {{ margin: 10px 0; padding: 10px; background-color: #3498db; color: white; text-decoration: none; display: block; text-align: center; border-radius: 5px; }}
                .menu-item:hover {{ background-color: #2980b9; }}
                .back a {{ color: #3498db; text-decoration: none; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🥽 Коллекция FPV шлемов</h1>
                {goggles_html}
                <a href="/">← Назад в меню</a>
            </div>
        </body>
        </html>
        """
        return goggles_page

    def show_goggle_details(self, goggle_name):
        """Возвращает HTML-страницу с деталями шлема"""
        if goggle_name not in self.goggles:
            return "<h1>Шлем не найден</h1><a href='/'>← Назад в меню</a>"

        info = self.goggles[goggle_name]

        goggle_details_page = f"""
        <html>
        <head>
            <title>🥽 {goggle_name.upper()}</title>
            <style>
                body {{ font-family: Arial, sans-serif; background-color: #f0f0f0; margin: 0; padding: 20px; }}
                .container {{ max-width: 800px; margin: auto; background-color: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
                .back a {{ color: #3498db; text-decoration: none; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🥽 {goggle_name.upper()}</h1>
                <p><strong>Описание:</strong> {info['description']}</p>
                <p><strong>Ценовой диапазон:</strong> {info['price_range']}</p>
                <p><strong>Особенности:</strong> {', '.join(info['features'])}</p>
                <h3>Вид спереди:</h3>
                <pre>{info['views']['front']}</pre>
                <h3>Вид сбоку:</h3>
                <pre>{info['views']['side']}</pre>
                <a href="/show_goggles">← Назад к коллекции</a> | <a href="/">← Назад в меню</a>
            </div>
        </body>
        </html>
        """
        return goggle_details_page

    # --- НОВАЯ РЕАЛИЗАЦИЯ: Передача данных ---
    def data_transfer(self):
        """Возвращает HTML-страницу для передачи данных"""
        if not self.components_learned:
            transfer_page = f"""
            <html>
            <body>
                <h1>📡 Передача данных</h1>
                <p>❌ У вас нет изученных компонентов для передачи!</p>
                <p>Сначала изучите компоненты в обучалке или викторине.</p>
                <a href="/">← Назад в меню</a>
            </body>
            </html>
            """
        else:
            # Создаем код передачи
            components_str = ",".join(sorted(self.components_learned))
            self.transfer_code = f"FPV{self.score:04d}{len(self.components_learned):02d}"

            transfer_page = f"""
            <html>
            <head>
                <title>📡 Передача данных</title>
                <style>
                    body {{ font-family: Arial, sans-serif; background-color: #f0f0f0; margin: 0; padding: 20px; }}
                    .container {{ max-width: 800px; margin: auto; background-color: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
                    .back a {{ color: #3498db; text-decoration: none; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>📡 Передача данных</h1>
                    <p><strong>Ваш счет:</strong> {self.score}</p>
                    <p><strong>Изучено компонентов:</strong> {len(self.components_learned)}</p>
                    <p><strong>Код передачи:</strong> <code>{self.transfer_code}</code></p>
                    <h3>КАК ПЕРЕДАТЬ ДАННЫЕ:</h3>
                    <ol>
                        <li>Запомните код передачи выше</li>
                        <li>На другом телефоне запустите эту программу</li>
                        <li>Выберите 'Передача данных' -> 'Получить данные'</li>
                        <li>Введите код передачи</li>
                    </ol>
                    <h3>Получить данные по коду</h3>
                    <form method="POST" action="/receive_data">
                        <input type="text" name="code" placeholder="Введите код передачи" required>
                        <input type="submit" value="Получить">
                    </form>
                    <a href="/">← Назад в меню</a>
                </div>
            </body>
            </html>
            """
        return transfer_page

    def receive_data(self, form_data):
        """Обрабатывает получение данных по коду"""
        code = form_data.get('code', '').strip().upper()

        if len(code) != 9 or not code.startswith("FPV"):
            result_message = "❌ Неверный формат кода!"
        else:
            try:
                score = int(code[3:7])
                components_count = int(code[7:9])

                result_message = f"""
                ✅ Данные успешно получены!<br>
                🏆 Счет друга: {score}<br>
                📚 Изучено компонентов: {components_count}
                """
                if score > self.score:
                    result_message += "<br>🎯 Ваш друг знает больше вас! Продолжайте учиться!"
                else:
                    result_message += "<br>⭐ Вы знаете больше своего друга! Так держать!"

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
                    result_message += f"<br>📖 Вы узнали о новых компонентах: {', '.join(imported)}"

            except ValueError:
                result_message = "❌ Ошибка в коде передачи!"

        receive_result_page = f"""
        <html>
        <head>
            <title>📥 Результат получения данных</title>
            <style>
                body {{ font-family: Arial, sans-serif; background-color: #f0f0f0; margin: 0; padding: 20px; }}
                .container {{ max-width: 800px; margin: auto; background-color: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
                .back a {{ color: #3498db; text-decoration: none; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>📥 Результат получения данных</h1>
                <p>{result_message}</p>
                <a href="/data_transfer">← Назад к передаче данных</a> | <a href="/">← Назад в меню</a>
            </div>
        </body>
        </html>
        """
        return receive_result_page


    def show_stats(self):
        progress = len(self.components_learned) / len(self.components) * 100
        if progress < 25:
            status = "Начинающий пилот"
        elif progress < 50:
            status = "Любитель FPV"
        elif progress < 75:
            status = "Опытный пилот"
        else:
            status = "FPV Эксперт!"

        stats_html = f"""
        <html>
        <head>
            <title>📊 Ваша статистика</title>
            <style>
                body {{ font-family: Arial, sans-serif; background-color: #f0f0f0; margin: 0; padding: 20px; }}
                .container {{ max-width: 800px; margin: auto; background-color: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
                .back a {{ color: #3498db; text-decoration: none; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>📊 Ваша статистика</h1>
                <p><strong>Общий счет:</strong> {self.score}</p>
                <p><strong>Отвечено вопросов:</strong> {self.questions_answered}</p>
                <p><strong>Изучено компонентов:</strong> {len(self.components_learned)}/{len(self.components)}</p>
                <p><strong>Прогресс изучения:</strong> {progress:.1f}%</p>
                <p><strong>Статус:</strong> {status}</p>
                <a href="/">← Назад в меню</a>
            </div>
        </body>
        </html>
        """
        return stats_html

# --- Создание Flask-приложения ---

app = Flask(__name__)

# Создаем один экземпляр игры (в реальности для каждого пользователя нужна сессия)
game_instance = FPVQuizGame()

@app.route('/')
def index():
    return game_instance.show_menu()

@app.route('/quiz_components')
def quiz_components_page():
    return game_instance.quiz_components()

@app.route('/quiz_components', methods=['POST'])
def quiz_components_submit():
    return game_instance.handle_quiz_components_submit(request.form)

# --- НОВЫЕ МАРШРУТЫ ---
@app.route('/quiz_drones')
def quiz_drones_page():
    return game_instance.quiz_drones()

@app.route('/quiz_drones', methods=['POST'])
def quiz_drones_submit():
    return game_instance.handle_quiz_drones_submit(request.form)

@app.route('/learning_components')
def learning_components_page():
    return game_instance.learning_components()

@app.route('/learning_component/<component_name>')
def show_component_detail(component_name):
    return game_instance.show_component_info(component_name)

@app.route('/show_controllers')
def show_controllers_page():
    return game_instance.show_controllers()

@app.route('/show_controller/<controller_name>')
def show_controller_detail(controller_name):
    return game_instance.show_controller_details(controller_name)

@app.route('/show_goggles')
def show_goggles_page():
    return game_instance.show_goggles()

@app.route('/show_goggle/<goggle_name>')
def show_goggle_detail(goggle_name):
    return game_instance.show_goggle_details(goggle_name)

@app.route('/data_transfer')
def data_transfer_page():
    return game_instance.data_transfer()

@app.route('/receive_data', methods=['POST'])
def receive_data_submit():
    return game_instance.receive_data(request.form)

@app.route('/stats')
def stats_page():
    return game_instance.show_stats()

if __name__ == "__main__":
    # Render предоставляет переменную PORT
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
