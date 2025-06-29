import streamlit as st

# Настройка максимального размера файла (10 ГБ)
st.set_page_config(
    page_title="LocalFFiction",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Явное указание параметра (если нужно)
st._config.set_option("server.maxUploadSize", 10240)

import pandas as pd
import base64
import warnings
from datetime import datetime

# Игнорировать специфические предупреждения Streamlit
warnings.filterwarnings("ignore", message="Thread 'MainThread': missing ScriptRunContext")

# Настройка темы для темного режима
st.set_page_config(
    page_title="LocalFFiction",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Пользовательские стили CSS для темного режима
st.markdown("""
<style>
    .story-card {
        border: 1px solid #444;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 15px;
        background-color: #2d2d2d;
        color: white;
    }
    .story-header {
        margin-bottom: 5px;
        padding: 10px;
        background-color: #333;
        border-radius: 5px;
    }
    .story-title {
        font-size: 1.3em;
        font-weight: bold;
        margin-bottom: 5px;
    }
    .author-name {
        font-size: 1.1em;
        font-weight: bold;
        margin-bottom: 5px;
    }
    .short-description {
        margin: 10px 0 5px 0;
        font-size: 0.95em;
        line-height: 1.4;
    }
    .author-bio {
        font-size: 0.9em;
        margin: 5px 0 10px 0;
        line-height: 1.4;
    }
    .archive-path {
        font-size: 0.9em;
        margin: 10px 0;
        padding: 8px;
        border: 1px solid #9C27B0;
        border-radius: 5px;
        background-color: #311B92;
        color: #e1bee7;
    }
    .full-description {
        margin: 10px 0;
        font-size: 0.95em;
        line-height: 1.4;
    }
    .tag-content {
        display: inline-block;
        background-color: #555;
        color: white;
        border-radius: 4px;
        padding: 2px 6px;
        margin: 2px;
        font-size: 0.8em;
    }
    .tag-character {
        display: inline-block;
        background-color: #4CAF50;
        color: white;
        border-radius: 4px;
        padding: 2px 6px;
        margin: 2px;
        font-size: 0.8em;
    }
    .tag-genre {
        display: inline-block;
        background-color: #2196F3;
        color: white;
        border-radius: 4px;
        padding: 2px 6px;
        margin: 2px;
        font-size: 0.8em;
    }
    .tag-warning {
        display: inline-block;
        background-color: #f44336;
        color: white;
        border-radius: 4px;
        padding: 2px 6px;
        margin: 2px;
        font-size: 0.8em;
    }
    .tag-series {
        display: inline-block;
        background-color: #9C27B0;
        color: white;
        border-radius: 4px;
        padding: 2px 6px;
        margin: 2px;
        font-size: 0.8em;
    }
    .rating-mature {
        background-color: #ff6b6b;
        color: white;
        padding: 2px 6px;
        border-radius: 4px;
        font-weight: bold;
    }
    .rating-teen {
        background-color: #4d96ff;
        color: white;
        padding: 2px 6px;
        border-radius: 4px;
        font-weight: bold;
    }
    .rating-everyone {
        background-color: #6bcb77;
        color: white;
        padding: 2px 6px;
        border-radius: 4px;
        font-weight: bold;
    }
    .user-rating {
        background-color: #FFC107;
        color: black;
        padding: 2px 6px;
        border-radius: 4px;
        font-weight: bold;
    }
    .status-complete {
        background-color: #4CAF50;
        color: white;
        padding: 2px 6px;
        border-radius: 4px;
        font-weight: bold;
    }
    .status-cancelled {
        background-color: #f44336;
        color: white;
        padding: 2px 6px;
        border-radius: 4px;
        font-weight: bold;
    }
    .status-hiatus {
        background-color: #FF9800;
        color: white;
        padding: 2px 6px;
        border-radius: 4px;
        font-weight: bold;
    }
    .status-incomplete {
        background-color: #FFEB3B;
        color: black;
        padding: 2px 6px;
        border-radius: 4px;
        font-weight: bold;
    }
    .word-count {
        background-color: #9C27B0;
        color: white;
        padding: 2px 6px;
        border-radius: 4px;
        font-weight: bold;
    }
    .meta-line {
        margin: 5px 0 10px 0;
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
    }
    .meta-item {
        display: flex;
        align-items: center;
        gap: 3px;
    }
    .tags-container {
        display: flex;
        flex-wrap: wrap;
        align-items: center;
        gap: 5px;
        margin: 10px 0 15px 0;
    }
    .tags-label {
        font-weight: bold;
        margin-right: 5px;
    }
    .description-label {
        font-weight: bold;
        margin-bottom: 5px;
    }
    .story-header {
        margin-bottom: 5px;
        padding: 15px;
        background-color: #333;
        border-radius: 5px;
    }
    .short-description {
        margin: 10px 0 0 0;
        padding: 10px;
        background-color: #3a3a3a;
        border-radius: 5px;
        font-size: 0.95em;
        line-height: 1.4;
    }
    .prequel-info {
        font-size: 0.9em;
        margin: 10px 0;
        padding: 8px;
        border: 1px solid #4fc3f7;
        border-radius: 5px;
        background-color: #263238;
        color: #e1f5fe;
    }
    .likes {
        background-color: #4CAF50;
        color: white;
        padding: 2px 6px;
        border-radius: 4px;
        font-weight: bold;
    }
    .dislikes {
        background-color: #f44336;
        color: white;
        padding: 2px 6px;
        border-radius: 4px;
        font-weight: bold;
    }
    .comments {
        background-color: #4fc3f7;
        color: white;
        padding: 2px 6px;
        border-radius: 4px;
        font-weight: bold;
    }
    .dates-line {
        font-size: 0.9em;
        margin: 10px 0;
        color: #bbb;
    }
    .archive-path {
        font-size: 0.9em;
        margin: 10px 0;
        padding: 8px;
        border: 1px solid #9C27B0;
        border-radius: 5px;
        background-color: #2d2d2d;
        color: #e1bee7;
    }
    .prequel-info {
        font-size: 0.9em;
        margin: 10px 0;
        padding: 8px;
        border: 1px solid #4fc3f7;
        border-radius: 5px;
        background-color: #2d2d2d;
        color: #e1f5fe;
    }
</style>
""", unsafe_allow_html=True)


def optimize_dataframe(df):
    """Оптимизация DataFrame для уменьшения размера"""
    for col in df.select_dtypes(include=['object']):
        if len(df[col].unique()) / len(df[col]) < 0.5:
            df[col] = df[col].astype('category')

    for col in df.select_dtypes(include=['int64']):
        df[col] = pd.to_numeric(df[col], downcast='integer')

    for col in df.select_dtypes(include=['float64']):
        df[col] = pd.to_numeric(df[col], downcast='float')

    return df


def format_content_rating(rating):
    """Форматирование возрастного рейтинга с цветными значками"""
    if not rating or not isinstance(rating, str):
        return ""

    rating = rating.lower()
    if 'mature' in rating:
        return '<span class="rating-mature">M</span>'
    elif 'teen' in rating:
        return '<span class="rating-teen">T</span>'
    elif 'everyone' in rating:
        return '<span class="rating-everyone">E</span>'
    return rating.capitalize()


def format_user_rating(rating):
    """Форматирование пользовательского рейтинга"""
    if pd.isna(rating):
        return ""
    return f'<span class="user-rating">{int(rating)}%</span>'


def get_tag_class(tag_type):
    """Получение класса CSS для тега по его типу"""
    tag_type = str(tag_type).lower()
    if 'character' in tag_type:
        return 'tag-character'
    elif 'genre' in tag_type:
        return 'tag-genre'
    elif 'warning' in tag_type:
        return 'tag-warning'
    elif 'series' in tag_type:
        return 'tag-series'
    return 'tag-content'


def parse_tags(tag_string):
    """Парсинг строки тегов в список тегов с классами"""
    if not tag_string or not isinstance(tag_string, str):
        return []

    tags = []
    categories = tag_string.split(' | ')

    for category in categories:
        if ': ' in category:
            cat_name, tag_names = category.split(': ', 1)
            for tag in tag_names.split(','):
                tag_class = get_tag_class(cat_name)
                tags.append((tag.strip(), tag_class))

    return tags


def load_data_in_chunks(uploaded_file, chunksize=10000):
    """Загрузка данных по частям"""
    chunks = []
    for chunk in pd.read_csv(uploaded_file, chunksize=chunksize):
        chunks.append(chunk)
    return pd.concat(chunks, ignore_index=True)


def safe_range_slider(label, min_val, max_val, default_min, default_max):
    """Безопасный слайдер диапазона с проверкой значений"""
    if min_val >= max_val:
        max_val = min_val + 1
    if default_min >= default_max:
        default_max = default_min + 1
    return st.slider(
        label,
        min_value=min_val,
        max_value=max_val,
        value=(default_min, default_max)
    )


def safe_count_slider(label, min_val, max_val, default_val):
    """Безопасный слайдер для количества с проверкой значений"""
    if min_val >= max_val:
        max_val = min_val + 1
    if default_val > max_val:
        default_val = max_val
    return st.slider(
        label,
        min_value=min_val,
        max_value=max_val,
        value=default_val
    )


def format_status(status):
    """Форматирование статуса завершения с цветами"""
    if not status or not isinstance(status, str):
        return ""

    status = status.lower()
    if status == 'complete':
        return '<span class="status-complete">Complete</span>'
    elif status == 'cancelled':
        return '<span class="status-cancelled">Cancelled</span>'
    elif status == 'hiatus':
        return '<span class="status-hiatus">Hiatus</span>'
    elif status == 'incomplete':
        return '<span class="status-incomplete">Incomplete</span>'
    return status.capitalize()


def format_likes_dislikes_comments(likes, dislikes, comments):
    """Форматирование лайков, дизлайков и комментариев"""
    result = []
    if likes is not None and likes != -1:
        result.append(f'<span class="likes">👍 {int(likes)}</span>')
    if dislikes is not None and dislikes != -1:
        result.append(f'<span class="dislikes">👎 {int(dislikes)}</span>')
    if comments is not None and comments != -1:
        result.append(f'<span class="comments">💬 {int(comments)}</span>')
    return ' '.join(result)


def format_dates(published, updated):
    """Форматирование дат публикации и обновления"""
    parts = []
    if pd.notna(published):
        published_str = published.strftime('%Y-%m-%d') if hasattr(published, 'strftime') else str(published)
        parts.append(f'Опубликовано: {published_str}')
    if pd.notna(updated):
        updated_str = updated.strftime('%Y-%m-%d') if hasattr(updated, 'strftime') else str(updated)
        parts.append(f'Обновлено: {updated_str}')
    return ' | '.join(parts)


def get_prequel_title(prequel_id, df):
    """Получение названия приквела по его ID"""
    if pd.isna(prequel_id) or not str(prequel_id).strip():
        return None

    # Очищаем ID от возможного префикса "id: "
    prequel_id = str(prequel_id).strip().replace('id:', '').strip()

    # Ищем точное совпадение ID
    match = df[df['id'].astype(str).str.strip() == prequel_id]
    if not match.empty:
        return match.iloc[0]['title']
    return None


def display_story_card(row, df):
    """Отображение карточки истории с новым форматом"""
    with st.container():
        # Основной блок с заголовком и автором
        st.markdown(f"""
        <div class="story-card">
            <div class="story-header">
                <div class="story-title">{row.get('title', 'Без названия')}</div>
                <div class="author-name">Автор: {row.get('author_name', 'Неизвестен')}</div>
                <div class="short-description">
                    {row['short_description'] if 'short_description' in row and pd.notna(row['short_description']) else "Короткое описание отсутствует"}
                </div>
            </div>
        """, unsafe_allow_html=True)

        # Полное описание (свернутое по умолчанию)
        if 'description_html' in row and pd.notna(row['description_html']):
            with st.expander("🔽 Полное описание", expanded=False):
                st.markdown(f"""
                <div class="full-description">
                    {row['description_html']}
                </div>
                """, unsafe_allow_html=True)

        # Даты публикации и обновления
        if 'date_published' in row or 'date_updated' in row:
            published = row.get('date_published')
            updated = row.get('date_updated')
            dates_str = format_dates(published, updated)
            if dates_str:
                st.markdown(f'<div class="dates-line">{dates_str}</div>', unsafe_allow_html=True)

        # Мета-информация (рейтинг, оценка и т.д.)
        meta_html = '<div class="meta-line">'

        if 'content_rating_formatted' in row:
            meta_html += f'<div class="meta-item"><strong>Рейтинг:</strong> {row["content_rating_formatted"]}</div>'

        if 'user_rating_formatted' in row:
            meta_html += f'<div class="meta-item"><strong>Оценка:</strong> {row["user_rating_formatted"]}</div>'

        # Лайки, дизлайки и комментарии
        likes = row.get('num_likes', -1)
        dislikes = row.get('num_dislikes', -1)
        comments = row.get('num_comments', -1)
        reactions = format_likes_dislikes_comments(likes, dislikes, comments)
        if reactions:
            meta_html += f'<div class="meta-item">{reactions}</div>'

        if 'completion_status' in row:
            meta_html += f'<div class="meta-item"><strong>Статус:</strong> {format_status(row["completion_status"])}</div>'

        if 'num_words' in row:
            meta_html += f'<div class="meta-item"><strong>Слов:</strong> <span class="word-count">{row["num_words"]:,}</span></div>'

        meta_html += '</div>'
        st.markdown(meta_html, unsafe_allow_html=True)

        # Теги
        if 'parsed_tags' in row and isinstance(row['parsed_tags'], list) and row['parsed_tags']:
            tags_html = '<div class="tags-container"><span class="tags-label">Теги:</span>'
            for tag, tag_class in row['parsed_tags']:
                tags_html += f'<span class="{tag_class}">{tag}</span>'
            tags_html += '</div>'
            st.markdown(tags_html, unsafe_allow_html=True)

        # Приквел (с поиском названия по ID)
        if 'prequel' in row and pd.notna(row['prequel']):
            prequel_id = str(row['prequel']).replace('id:', '').strip()
            prequel_match = df[df['id'].astype(str).str.strip() == prequel_id]
            if not prequel_match.empty:
                prequel_title = prequel_match.iloc[0]['title']
                st.markdown(f"""
                <div class="prequel-info">
                    <strong>Приквел:</strong> {prequel_title}
                </div>
                """, unsafe_allow_html=True)

        # Путь в архиве
        if 'archive_path' in row and pd.notna(row['archive_path']):
            st.markdown(f"""
            <div class="archive-path">
                <strong>Путь в архиве:</strong> {row['archive_path']}
            </div>
            """, unsafe_allow_html=True)

        # Биография автора
        if 'author_bio' in row and pd.notna(row['author_bio']) and row['author_bio'].strip():
            with st.expander("👤 Биография автора", expanded=False):
                st.markdown(f"""
                <div class="author-bio">
                    {row['author_bio']}
                </div>
                """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)  # Закрываем story-card


def main():
    st.title("📚 LocalFFiction")
    st.markdown("Локальный архив Fimfiction. Создан с помощью DeepSeek и опубликован FenixScar.")

    # Загрузка файла
    uploaded_file = st.sidebar.file_uploader(
        "Загрузите CSV-файл Fimfiction",
        type=['csv'],
        help="Используйте конвертер для создания CSV-файла"
    )

    if not uploaded_file:
        st.info("Пожалуйста, загрузите CSV-файл Fimfiction для начала работы")
        return

    # Загрузка данных
    with st.spinner('Загрузка и оптимизация данных...'):
        try:
            df = load_data_in_chunks(uploaded_file)
            df = optimize_dataframe(df)

            # Обработка данных
            date_cols = ['date_published', 'date_updated']
            for col in date_cols:
                if col in df.columns:
                    df[col] = pd.to_datetime(df[col], errors='coerce')

            if 'content_rating' in df.columns:
                df['content_rating_formatted'] = df['content_rating'].apply(format_content_rating)

            if 'rating' in df.columns:
                df['user_rating_formatted'] = df['rating'].apply(format_user_rating)

            # Подготовка тегов
            all_tags = []
            if 'tags' in df.columns:
                df['parsed_tags'] = df['tags'].apply(parse_tags)
                all_tags_set = set()
                for tags_list in df['parsed_tags']:
                    if isinstance(tags_list, list):
                        for tag, _ in tags_list:
                            all_tags_set.add(tag.strip())
                all_tags = sorted(all_tags_set)

            st.success(f"Успешно загружено {len(df)} историй!")
        except Exception as e:
            st.error(f"Ошибка загрузки файла: {str(e)}")
            return

    # Боковая панель - Поиск
    st.sidebar.header("Поиск")

    # Раздельные поля поиска
    search_everywhere = st.sidebar.text_input("Поиск везде:")
    search_title = st.sidebar.text_input("Поиск по названию:")
    search_author = st.sidebar.text_input("Поиск по автору:")
    search_description = st.sidebar.text_input("Поиск по описанию:")

    # Фильтры в боковой панели
    st.sidebar.header("Фильтры")

    # Инициализация фильтров
    filters = {
        'selected_rating': 'Все',
        'selected_status': 'Все',
        'min_words': 0,
        'max_words': float('inf'),
        'min_rating': 0,
        'selected_tags': [],
        'sort_rating': 'Нет',
        'sort_words': 'Нет',
        'sort_published': 'Нет',
        'sort_updated': 'Нет'
    }

    # Фильтр по рейтингу
    if 'content_rating' in df.columns:
        rating_options = ['Все'] + sorted(df['content_rating'].dropna().unique().tolist())
        filters['selected_rating'] = st.sidebar.selectbox(
            "Возрастной рейтинг",
            rating_options,
            index=0
        )

    # Фильтр по статусу
    if 'completion_status' in df.columns:
        status_options = ['Все'] + sorted(df['completion_status'].dropna().unique().tolist())
        filters['selected_status'] = st.sidebar.selectbox(
            "Статус",
            status_options,
            index=0
        )

    # Фильтр по словам (ручной ввод)
    if 'num_words' in df.columns:
        col1, col2 = st.sidebar.columns(2)
        with col1:
            filters['min_words'] = st.number_input(
                "Мин. кол-во слов",
                min_value=0,
                value=0,
                step=1000
            )
        with col2:
            filters['max_words'] = st.number_input(
                "Макс. кол-во слов",
                min_value=0,
                value=int(df['num_words'].max()) if 'num_words' in df.columns else 0,
                step=1000
            )

    # Фильтр по оценке
    if 'rating' in df.columns:
        filters['min_rating'] = st.sidebar.slider(
            "Минимальная оценка (%)",
            min_value=0,
            max_value=100,
            value=0
        )

    # Фильтр по тегам
    if 'parsed_tags' in df.columns and all_tags:
        filters['selected_tags'] = st.sidebar.multiselect(
            "Поиск по тегам",
            options=all_tags,
            default=[],
            help="История должна содержать ВСЕ выбранные теги"
        )

    # Сортировка
    st.sidebar.header("Сортировка")
    sort_options = ['Нет', 'По возрастанию', 'По убыванию']
    col1, col2 = st.sidebar.columns(2)
    with col1:
        filters['sort_rating'] = st.selectbox(
            "По рейтингу",
            options=sort_options,
            index=0
        )
    with col2:
        filters['sort_words'] = st.selectbox(
            "По словам",
            options=sort_options,
            index=0
        )

    col3, col4 = st.sidebar.columns(2)
    with col3:
        filters['sort_published'] = st.selectbox(
            "По публикации",
            options=sort_options,
            index=0
        )
    with col4:
        filters['sort_updated'] = st.selectbox(
            "По обновлению",
            options=sort_options,
            index=0
        )

    # Количество историй (без ограничений)
    display_count = st.sidebar.number_input(
        "Количество отображаемых записей",
        min_value=1,
        value=50,
        step=10
    )

    # Применение фильтров
    filtered_df = df.copy()

    if filters['selected_rating'] != 'Все':
        filtered_df = filtered_df[filtered_df['content_rating'] == filters['selected_rating']]

    if filters['selected_status'] != 'Все':
        filtered_df = filtered_df[filtered_df['completion_status'] == filters['selected_status']]

    if 'num_words' in df.columns:
        filtered_df = filtered_df[
            (filtered_df['num_words'] >= filters['min_words']) &
            (filtered_df['num_words'] <= filters['max_words'])
            ]

    filtered_df = filtered_df[filtered_df['rating'] >= filters['min_rating']]

    # Фильтрация по тегам
    if filters['selected_tags']:
        filtered_df = filtered_df[
            filtered_df['parsed_tags'].apply(
                lambda tags: isinstance(tags, list) and
                             all(any(tag == selected for tag, _ in tags)
                                 for selected in filters['selected_tags'])
            )
        ]

    # Применение поисковых запросов
    if search_everywhere:
        mask = pd.concat([
            filtered_df[col].astype(str).str.contains(search_everywhere, case=False, na=False)
            for col in ['title', 'author_name', 'description_html', 'short_description']
            if col in filtered_df.columns
        ], axis=1).any(axis=1)
        filtered_df = filtered_df[mask]

    if search_title and 'title' in filtered_df.columns:
        mask = filtered_df['title'].astype(str).str.contains(search_title, case=False, na=False)
        filtered_df = filtered_df[mask]

    if search_author and 'author_name' in filtered_df.columns:
        mask = filtered_df['author_name'].astype(str).str.contains(search_author, case=False, na=False)
        filtered_df = filtered_df[mask]

    if search_description:
        mask = pd.concat([
            filtered_df[col].astype(str).str.contains(search_description, case=False, na=False)
            for col in ['description_html', 'short_description']
            if col in filtered_df.columns
        ], axis=1).any(axis=1)
        filtered_df = filtered_df[mask]

    # Применение сортировки
    sort_columns = []
    sort_orders = []

    # Определяем порядок сортировки для каждого критерия
    sorting_options = [
        ('rating', filters['sort_rating']),
        ('num_words', filters['sort_words']),
        ('date_published', filters['sort_published']),
        ('date_updated', filters['sort_updated'])
    ]

    for column, sort_option in sorting_options:
        if sort_option != 'Нет' and column in filtered_df.columns:
            sort_columns.append(column)
            sort_orders.append(sort_option == 'По возрастанию')

    # Применяем сортировку, если есть критерии
    if sort_columns:
        filtered_df = filtered_df.sort_values(
            by=sort_columns,
            ascending=sort_orders
        )

    # Основное отображение
    st.header(f"📖 Показано {len(filtered_df)} из {len(df)} историй")

    # Режимы просмотра
    view_mode = st.radio(
        "Режим просмотра",
        ["Карточки", "Таблица", "Статистика"],
        horizontal=True
    )

    if view_mode == "Таблица":
        cols_to_show = ['title', 'author_name', 'content_rating_formatted',
                        'user_rating_formatted', 'num_words', 'completion_status',
                        'date_published', 'date_updated']
        cols_to_show = [col for col in cols_to_show if col in filtered_df.columns]

        st.dataframe(
            filtered_df[cols_to_show],
            use_container_width=True,
            height=600
        )

    elif view_mode == "Статистика":
        st.subheader("Статистика коллекции")

        if 'num_words' in filtered_df.columns:
            st.metric("Общее количество слов", f"{filtered_df['num_words'].sum():,}")

        col1, col2, col3 = st.columns(3)

        with col1:
            if 'content_rating' in filtered_df.columns:
                st.write("**Распределение по рейтингам:**")
                st.bar_chart(filtered_df['content_rating'].value_counts())

        with col2:
            if 'completion_status' in filtered_df.columns:
                st.write("**Статус завершения:**")
                st.bar_chart(filtered_df['completion_status'].value_counts())

        with col3:
            if 'rating' in filtered_df.columns:
                st.write("**Распределение оценок:**")
                st.bar_chart(filtered_df['rating'].value_counts(bins=10))

    else:  # Карточки
        if len(filtered_df) > 0:
            for _, row in filtered_df.head(display_count).iterrows():
                display_story_card(row, df)
        else:
            st.warning("Нет историй, соответствующих выбранным фильтрам")

    # Отступ внизу
    st.markdown("<div style='margin-bottom: 50px;'></div>", unsafe_allow_html=True)


if __name__ == "__main__":
    main()