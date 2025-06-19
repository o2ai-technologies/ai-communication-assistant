from datetime import datetime


# Get current date in a readable format
def get_current_date():
    return datetime.now().strftime("%B %d, %Y")


# query_writer_instructions = """Your goal is to generate sophisticated and diverse web search queries.
# These queries are intended for an advanced automated web research tool capable of analyzing complex results, following links, and synthesizing information.

# Instructions:
# - Always prefer a single search query, only add another query if the original question requests multiple aspects or elements and one query is not enough.
# - Each query should focus on one specific aspect of the original question.
# - Don't produce more than {number_queries} queries.
# - Queries should be diverse, if the topic is broad, generate more than 1 query.
# - Don't generate multiple similar queries, 1 is enough.
# - Query should ensure that the most current information is gathered. The current date is {current_date}.

# Format: 
# - Format your response as a JSON object with ALL three of these exact keys:
#    - "rationale": Brief explanation of why these queries are relevant
#    - "query": A list of search queries

# Example:

# Topic: What revenue grew more last year apple stock or the number of people buying an iphone
# ```json
# {{
#     "rationale": "To answer this comparative growth question accurately, we need specific data points on Apple's stock performance and iPhone sales metrics. These queries target the precise financial information needed: company revenue trends, product-specific unit sales figures, and stock price movement over the same fiscal period for direct comparison.",
#     "query": ["Apple total revenue growth fiscal year 2024", "iPhone unit sales growth fiscal year 2024", "Apple stock price growth fiscal year 2024"],
# }}
# ```

# Context: the speaker going to some event to prepare to the presentation
# Here are details about event and speaker's intention in structured format in ukrainian language: {research_topic}"""
query_writer_instructions = """
Для кожної категорії аудиторії: {target_audience} яка присутня на конференції: {event_name} проведи дослідження і збери інформацію, яка буде використана в якості аргументації щоб змінити уявлення теперішнього, яке існує в цих людей: {audience_knowledge} на те що я хочу щоб вони зрозуміли після мого виступу: {key_message}
Підкріпи знайдену інформацію відповідними дослідженнями, цікавими прикладами від світових компаній, цитатами лідерів галузі, які будуть релевантними для визначених вище аудиторій 
Зверни особливу увагу на ті матеріали які допоможуть змінити їхнє уявлення про теперішнє 
Структуруй знайдену інформацію у форматі звіту
"""


web_searcher_instructions = """Виконуй цільові пошукові запити в Google, щоб зібрати найновішу та достовірну інформацію про тему: "{research_topic}" і синтезуй її у перевірений текстовий артефакт.

Інструкції:

Запити повинні забезпечити отримання максимально актуальної інформації. Поточна дата: {current_date}.

Проведи кілька різноманітних пошуків, щоб зібрати всебічну інформацію.

Узагальни ключові висновки, ретельно відстежуючи джерело кожного конкретного фрагмента інформації.

Результатом має бути добре написане резюме або звіт на основі знайдених даних.

Включай лише ту інформацію, яка була знайдена в результатах пошуку. Не вигадуй дані.

Тема дослідження:
{research_topic}
"""

reflection_instructions = """Ви — досвідчений науковий асистент, який аналізує резюме з теми "{research_topic}".

Інструкції:

Визначте прогалини в знаннях або аспекти, які потребують глибшого вивчення, і сформулюйте уточнювальний запит (один або декілька).

Якщо надані резюме містять достатньо інформації для відповіді на запит користувача, не створюйте уточнюючий запит.

Якщо є інформаційна прогалина, сформулюйте уточнюючий запит, який допоможе розширити розуміння теми.

Зосередьтеся на технічних деталях, особливостях реалізації або нових тенденціях, які були розкриті недостатньо.

Вимоги:

Уточнюючий запит має бути самодостатнім і містити достатньо контексту для пошуку в Інтернеті.

Формат вихідних даних:

Відповідь оформлюється у форматі JSON з такими ключами:

"is_sufficient": true або false

"knowledge_gap": Опишіть, якої інформації не вистачає або що потребує уточнення

"follow_up_queries": Сформулюйте конкретне питання (або питання), яке допоможе заповнити цю прогалину

Приклад:
```json
{{
    "is_sufficient": true, // or false
    "knowledge_gap": "The summary lacks information about performance metrics and benchmarks", // "" if is_sufficient is true
    "follow_up_queries": ["What are typical performance benchmarks and metrics used to evaluate [specific technology]?"] // [] if is_sufficient is true
}}
```

Уважно проаналізуйте надані резюме, щоб визначити інформаційні прогалини, і сформулюйте уточнюючі запити. Потім сформуйте відповідь у вказаному форматі JSON:

Резюме:
{summaries}
"""

answer_instructions = """Згенеруйте високоякісну відповідь на запит користувача на основі наданих резюме.

Інструкції:

Поточна дата: {current_date}.

Ви не згадуєте, що є фінальним етапом багатоступеневого дослідження.

Ви маєте доступ до всієї зібраної інформації з попередніх етапів.

Ви маєте доступ до запитання користувача.

Згенеруйте якісну, змістовну відповідь на запит користувача, спираючись на надані резюме та запитання.

Ви обов’язково повинні правильно включити всі цитати з резюме у відповідь.

Контекст користувача:

{research_topic}

Резюме:
{summaries}"""
