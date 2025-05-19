# Описание тестов

## Модели страниц (Page Object Models)

### 1. `LoginPage`
- Обеспечивает вход в систему.
- Методы:
  - `login(username, password)`: переходит по URL и выполняет вход.

### 2. `DisciplinePage`
- Открывает раздел дисциплины.
- Методы:
  - `open_discipline()`: переходит в нужный раздел.

### 3. `NewsBlockPage`
- Управление новостным блоком: добавление, проверка, удаление.
- Методы:
  - `add_news(text)`: добавляет новость.
  - `verify_news(expected_text)`: проверяет наличие новости.
  - `delete_news()`: удаляет новость.

### 4. `AdBlockPage`
- Управление рекламным блоком: добавление кнопки, добавление контента через TinyMCE редактор, проверка содержимого.
- Методы:
  - `add_button_ad()`: открывает блок рекламы.
  - `add_ad(new_value)`: задает заголовок рекламы.
  - `set_content_in_tinymce_body(text)`: вставляет текст в редактор TinyMCE через JavaScript.
  - `verify_add(expected_text)`: проверяет содержимое рекламы.

### 5. `BlockTheManual`
- Добавление ручного блока с заголовком и файлами.
- Методы:
  - `add_button()`: открывает форму добавления блока.
  - `add_new_block(expected_text)`: заполняет форму и загружает файлы.

### 6. `CalendarBlockPage`
- Добавление и проверка лекций в календаре.
- Методы:
  - `add_lecture(text, date, start_time, end_time)`: создает лекцию с указанными параметрами.
  - `verify_lecture(expected_date, expected_time, expected_text)`: проверяет детали лекции.

---
