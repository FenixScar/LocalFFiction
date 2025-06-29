import csv
import os
import re
import html
from datetime import datetime
import json
import sys
from tqdm import tqdm

# Конфигурация языка
LANGUAGE = 'en'

def clean_text(text):
    """
    Тщательная очистка текста от HTML-тегов, артефактов JSON и лишних пробелов
    """
    if not text or not isinstance(text, str):
        return text

    # Удаление HTML-тегов с атрибутами
    text = re.sub(r'<[a-zA-Z]+[^>]*>|<\/[a-zA-Z]+>', '', text)
    # Удаление оставшихся HTML-сущностей (например, &nbsp;)
    text = html.unescape(text)
    # Удаление остатков разметки JSON
    text = re.sub(r'^\s*".*?":\s*"?|"\s*$', '', text)
    # Нормализация пробелов
    text = ' '.join(text.split()).strip()
    return text

def clean_html_description(html_text):
    """
    Агрессивная очистка HTML-описаний от всех тегов и артефактов
    """
    if not html_text or not isinstance(html_text, str):
        return html_text

    # Удаление всех HTML-тегов и фрагментов
    clean_text = re.sub(r'<[a-zA-Z][^>]*>|<\/[a-zA-Z][^>]*>|<[^>]*$|^[^<]*>', '', html_text)
    # Удаление HTML-сущностей (например, &nbsp; &amp; и т.д.)
    clean_text = html.unescape(clean_text)
    # Удаление оставшихся технических артефактов
    clean_text = re.sub(r'\\["\'\\]', '', clean_text)
    # Нормализация пробелов
    clean_text = ' '.join(clean_text.split()).strip()
    return clean_text

def format_tags(tags_data):
    """
    Улучшенное форматирование тегов с точной группировкой по категориям
    """
    if not tags_data or not isinstance(tags_data, list):
        return ""

    # Словарь нормализации категорий
    CATEGORY_MAP = {
        'character': 'Character',
        'characters': 'Character',
        'genre': 'Genre',
        'genres': 'Genre',
        'series': 'Series',
        'warning': 'Warning',
        'warnings': 'Warning',
        'content': 'Content',
        'language': 'Language',
        'spoiler': 'Spoiler',
        'editor': 'Editor',
        'status': 'Status'
    }

    # Группировка тегов по нормализованным категориям
    tags_by_category = {}
    for tag in tags_data:
        if not isinstance(tag, dict) or 'type' not in tag or 'name' not in tag:
            continue

        # Нормализация категории
        raw_category = tag['type'].lower().strip()
        category = CATEGORY_MAP.get(raw_category, raw_category.capitalize())

        # Очистка названия тега
        tag_name = clean_text(tag['name']).strip()
        if not tag_name:
            continue

        # Добавление в соответствующую категорию
        if category not in tags_by_category:
            tags_by_category[category] = []
        if tag_name not in tags_by_category[category]:  # избегаем дубликатов
            tags_by_category[category].append(tag_name)

    # Определенный порядок вывода категорий
    category_order = ['Character', 'Genre', 'Series', 'Warning', 'Content', 'Language']

    # Сортировка категорий согласно порядку, остальные в конце
    sorted_categories = sorted(
        tags_by_category.keys(),
        key=lambda x: (category_order.index(x) if x in category_order else len(category_order))
    )

    # Форматирование результата
    formatted_tags = []
    for category in sorted_categories:
        # Сортировка тегов внутри категории по алфавиту
        formatted_tags.append(f"{category}: {', '.join(sorted(tags_by_category[category]))}")

    return " | ".join(formatted_tags)

def format_prequel(prequel_data):
    """
    Форматирование информации о приквеле с поддержкой всех форматов
    """
    if prequel_data is None or prequel_data in ["null", "None", "none", None]:
        return ""

    if isinstance(prequel_data, bool):
        return str(prequel_data).lower()

    if isinstance(prequel_data, str):
        # Если это числовая строка (ID приквела)
        if prequel_data.isdigit():
            return f"id: {prequel_data}"
        return clean_text(prequel_data)

    if isinstance(prequel_data, (int, float)):
        return f"id: {prequel_data}"

    if isinstance(prequel_data, dict):
        parts = []
        if 'id' in prequel_data:
            parts.append(f"id: {prequel_data['id']}")
        if 'title' in prequel_data:
            parts.append(f"title: {clean_text(prequel_data['title'])}")
        return " | ".join(parts) if parts else ""

    return str(prequel_data)

def extract_title(line):
    """
    Специальная функция для извлечения чистого заголовка
    """
    title_match = re.search(r'"title":\s*"([^"]*)"[^}]*"total_num_views"', line)
    if not title_match:
        title_match = re.findall(r'"title":\s*"([^"]*)"', line)
        if title_match:
            return clean_text(title_match[-1])
    else:
        return clean_text(title_match.group(1))
    return ""

def parse_line(line):
    """
    Разбор строки с данными истории
    """
    data = {}

    try:
        json_data = json.loads("{" + line + "}")
        story_id, story_data = next(iter(json_data.items()))

        data['id'] = story_id
        data['title'] = clean_text(story_data.get('title', ''))

        # Сопоставление основных полей
        fields_mapping = {
            'description_html': 'description_html',
            'short_description': 'short_description',
            'completion_status': 'completion_status',
            'content_rating': 'content_rating',
            'num_words': 'num_words',
            'rating': 'rating',
            'num_views': 'num_views',
            'num_likes': 'num_likes',
            'num_dislikes': 'num_dislikes',
            'num_comments': 'num_comments',
            'date_published': 'date_published',
            'date_updated': 'date_updated'
        }

        for field, source in fields_mapping.items():
            if source in story_data:
                value = story_data[source]
                if field.endswith('_html'):
                    data[field] = clean_html_description(str(value))
                else:
                    data[field] = clean_text(str(value))

        # Автор
        if 'author' in story_data:
            author = story_data['author']
            data['author_name'] = clean_text(author.get('name', ''))
            data['author_id'] = clean_text(str(author.get('id', '')))
            if 'bio_html' in author:
                data['author_bio'] = clean_html_description(author['bio_html'])

        # Путь к файлу
        if 'archive' in story_data and 'path' in story_data['archive']:
            data['archive_path'] = clean_text(story_data['archive']['path'])

        # Теги
        if 'tags' in story_data:
            data['tags'] = format_tags(story_data['tags'])

        # Приквел (обработка всех возможных форматов)
        if 'prequel' in story_data:
            data['prequel'] = format_prequel(story_data['prequel'])

        return data

    except json.JSONDecodeError:
        return parse_line_fallback(line)

def parse_line_fallback(line):
    """
    Резервный метод разбора с использованием regex с надежной обработкой тегов
    """
    data = {}

    # Извлечение ID
    id_match = re.search(r'"(\d+)":\s*{', line)
    if id_match:
        data['id'] = id_match.group(1)

    # Заголовок истории
    data['title'] = extract_title(line)

    # Поиск ВСЕХ совпадений num_words и выбор ПОСЛЕДНЕГО
    num_words_matches = re.findall(r'"num_words":\s*(\d+)', line)
    if num_words_matches:
        data['num_words'] = num_words_matches[-1]  # берем последнее значение

    # Описания
    html_fields = {
        'description_html': r'"description_html":\s*"([^"]*)"',
        'short_description': r'"short_description":\s*"([^"]*)"'
    }

    for field, pattern in html_fields.items():
        match = re.search(pattern, line)
        if match:
            data[field] = clean_html_description(match.group(1))

    # Автор
    author_match = re.search(r'"author":\s*{.*?"name":\s*"([^"]*)".*?"id":\s*(\d+)', line, re.DOTALL)
    if author_match:
        data['author_name'] = clean_text(author_match.group(1))
        data['author_id'] = clean_text(author_match.group(2))
        bio_match = re.search(r'"bio_html":\s*"([^"]*)"', line)
        if bio_match:
            data['author_bio'] = clean_html_description(bio_match.group(1))

    # Другие основные поля
    simple_fields = [
        'completion_status', 'content_rating', 'rating',
        'num_views', 'num_likes', 'num_dislikes', 'num_comments',
        'date_published', 'date_updated'
    ]

    for field in simple_fields:
        match = re.search(fr'"{field}":\s*"([^"]*)"', line)
        if not match:
            match = re.search(fr'"{field}":\s*([^,}}\s]+)', line)
        if match:
            value = match.group(1).strip('"')
            data[field] = clean_text(value)

    # Путь к файлу
    path_match = re.search(r'"archive":\s*{.*?"path":\s*"([^"]+)"', line, re.DOTALL)
    if path_match:
        data['archive_path'] = clean_text(path_match.group(1))

    # Теги
    tags_match = re.search(r'"tags":\s*(\[[^\]]*\])', line)
    if tags_match:
        try:
            tags_data = json.loads(tags_match.group(1))
            if isinstance(tags_data, list):
                data['tags'] = format_tags(tags_data)
        except json.JSONDecodeError:
            # Резервный вариант для ручного разбора, если JSON невалиден
            tag_items = re.finditer(r'\{"type":\s*"([^"]*)".*?"name":\s*"([^"]*)"', tags_match.group(1), re.DOTALL)
            tags_list = []
            for tag in tag_items:
                tags_list.append({
                    'type': tag.group(1),
                    'name': tag.group(2)
                })
            if tags_list:
                data['tags'] = format_tags(tags_list)

    # Приквел (расширенная резервная обработка)
    prequel_match = re.search(r'"prequel":\s*(\{.*?\}|"null"|null|true|false|"[^"]*"|\d+)', line, re.DOTALL)
    if prequel_match:
        prequel_value = prequel_match.group(1)

        if prequel_value in ['"null"', 'null']:
            data['prequel'] = ""
        elif prequel_value in ['true', 'false']:
            data['prequel'] = prequel_value
        elif prequel_value.startswith('"') and prequel_value.endswith('"'):
            data['prequel'] = clean_text(prequel_value[1:-1])
        elif prequel_value.isdigit():
            data['prequel'] = f"id: {prequel_value}"
        else:
            try:
                prequel_data = json.loads(prequel_value)
                data['prequel'] = format_prequel(prequel_data)
            except:
                data['prequel'] = format_prequel(prequel_value)

    return data

def process_fimfiction_log(input_path, output_csv):
    """
    Обработка лог-файла Fimfiction с индикатором прогресса и детальной статистикой
    """

    # Подсчет общего количества строк в файле
    print("\n🔍 Подсчет общего количества строк...")
    with open(input_path, 'r', encoding='utf-8') as f:
        total_lines = sum(1 for _ in f)

    print(f"\n🚀 Начало обработки {total_lines:,} строк в {datetime.now().strftime('%H:%M:%S')}")
    print(f"📂 Входной файл: {input_path} ({os.path.getsize(input_path) / 1024 / 1024:.1f} MB)")
    print(f"📝 Выходной файл: {output_csv}")

    fieldnames = [
        'id', 'title', 'author_name', 'author_id', 'author_bio',
        'description_html', 'short_description',
        'completion_status', 'content_rating',
        'tags', 'prequel',
        'num_words', 'rating',
        'num_views', 'num_likes', 'num_dislikes', 'num_comments',
        'date_published', 'date_updated', 'archive_path'
    ]

    # Статистика обработки
    stats = {
        'processed': 0,
        'skipped_empty': 0,
        'skipped_338': 0,
        'skipped_errors': 0,
        'skipped_no_id_title': 0,
        'errors': []
    }

    with open(output_csv, 'w', encoding='utf-8-sig', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        with open(input_path, 'r', encoding='utf-8') as f:
            # Инициализация индикатора прогресса
            with tqdm(total=total_lines,
                      desc="⏳ Обработка",
                      unit="строка",
                      bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]") as pbar:

                for line_num, line in enumerate(f, 1):
                    line = line.strip()
                    pbar.update(1)

                    if not line:
                        stats['skipped_empty'] += 1
                        continue

                    if line.startswith('338.1'):
                        stats['skipped_338'] += 1
                        continue

                    try:
                        data = parse_line(line)
                        if 'id' in data and 'title' in data:
                            # Финальная очистка всех полей
                            for field in data:
                                if isinstance(data[field], str):
                                    if field.endswith('_html') or field == 'author_bio':
                                        data[field] = clean_html_description(data[field])
                                    else:
                                        data[field] = clean_text(data[field])

                            row = {field: data.get(field, '') for field in fieldnames}
                            writer.writerow(row)
                            stats['processed'] += 1
                        else:
                            stats['skipped_no_id_title'] += 1
                            stats['errors'].append(f"Строка {line_num}: нет id или заголовка")
                    except Exception as e:
                        stats['skipped_errors'] += 1
                        stats['errors'].append(f"Строка {line_num}: {str(e)}")

    # Вывод итоговой статистики
    print("\n✅ Готово! Результаты:")
    print(f"├─ Успешно обработано: {stats['processed']:,}")
    print(f"├─ Пропущено пустых строк: {stats['skipped_empty']:,}")
    print(f"├─ Пропущено строк '338.1': {stats['skipped_338']:,}")
    print(f"├─ Пропущено из-за ошибок: {stats['skipped_errors']:,}")
    print(f"└─ Пропущено (нет id/заголовка): {stats['skipped_no_id_title']:,}")

    total_skipped = (stats['skipped_empty'] + stats['skipped_338'] +
                     stats['skipped_errors'] + stats['skipped_no_id_title'])
    print(f"\n📊 Итого: {stats['processed']:,} из {total_lines:,} строк ({stats['processed'] / total_lines:.1%})")
    print(f"⏱ Время выполнения: {datetime.now().strftime('%H:%M:%S')}")
    print(f"💾 Результат сохранен в: {output_csv}")

    # Вывод первых 5 ошибок (если есть)
    if stats['errors']:
        print("\n⚠ Первые 5 ошибок:")
        for err in stats['errors'][:5]:
            print(f"  - {err}")
        if len(stats['errors']) > 5:
            print(f"  ... и еще {len(stats['errors']) - 5} ошибок")

        # Сохранение полного лога ошибок в файл
        error_log_path = os.path.splitext(output_csv)[0] + '_errors.log'
        with open(error_log_path, 'w', encoding='utf-8') as err_file:
            err_file.write("\n".join(stats['errors']))
        print(f"📝 Полный лог ошибок сохранен в: {error_log_path}")

if __name__ == "__main__":
    input_file = 'index.json'
    output_file = 'fimfiction_result.csv'

    process_fimfiction_log(input_file, output_file)