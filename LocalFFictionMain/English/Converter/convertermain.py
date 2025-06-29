import csv
import os
import re
import html
from datetime import datetime
import json
import sys
from tqdm import tqdm

# Language configuration
LANGUAGE = 'en'

def clean_text(text):
    """
    Thorough text cleaning from HTML, JSON artifacts and extra spaces
    """
    if not text or not isinstance(text, str):
        return text

    # Remove HTML tags with attributes
    text = re.sub(r'<[a-zA-Z]+[^>]*>|<\/[a-zA-Z]+>', '', text)
    # Remove remaining HTML entities (e.g., &nbsp;)
    text = html.unescape(text)
    # Remove JSON markup remnants
    text = re.sub(r'^\s*".*?":\s*"?|"\s*$', '', text)
    # Normalize spaces
    text = ' '.join(text.split()).strip()
    return text

def clean_html_description(html_text):
    """
    Aggressive cleaning of HTML descriptions from all tags and artifacts
    """
    if not html_text or not isinstance(html_text, str):
        return html_text

    # Remove all HTML tags and fragments
    clean_text = re.sub(r'<[a-zA-Z][^>]*>|<\/[a-zA-Z][^>]*>|<[^>]*$|^[^<]*>', '', html_text)
    # Remove HTML entities (e.g., &nbsp; &amp; etc.)
    clean_text = html.unescape(clean_text)
    # Remove remaining technical artifacts
    clean_text = re.sub(r'\\["\'\\]', '', clean_text)
    # Normalize spaces
    clean_text = ' '.join(clean_text.split()).strip()
    return clean_text

def format_tags(tags_data):
    """
    Improved tag formatting with precise category grouping
    """
    if not tags_data or not isinstance(tags_data, list):
        return ""

    # Category normalization dictionary
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

    # Group tags by normalized categories
    tags_by_category = {}
    for tag in tags_data:
        if not isinstance(tag, dict) or 'type' not in tag or 'name' not in tag:
            continue

        # Normalize category
        raw_category = tag['type'].lower().strip()
        category = CATEGORY_MAP.get(raw_category, raw_category.capitalize())

        # Clean tag name
        tag_name = clean_text(tag['name']).strip()
        if not tag_name:
            continue

        # Add to corresponding category
        if category not in tags_by_category:
            tags_by_category[category] = []
        if tag_name not in tags_by_category[category]:  # avoid duplicates
            tags_by_category[category].append(tag_name)

    # Defined category output order
    category_order = ['Character', 'Genre', 'Series', 'Warning', 'Content', 'Language']

    # Sort categories according to order, others at the end
    sorted_categories = sorted(
        tags_by_category.keys(),
        key=lambda x: (category_order.index(x) if x in category_order else len(category_order))
    )

    # Format the result
    formatted_tags = []
    for category in sorted_categories:
        # Sort tags within category alphabetically
        formatted_tags.append(f"{category}: {', '.join(sorted(tags_by_category[category]))}")

    return " | ".join(formatted_tags)

def format_prequel(prequel_data):
    """
    Format prequel information with support for all formats
    """
    if prequel_data is None or prequel_data in ["null", "None", "none", None]:
        return ""

    if isinstance(prequel_data, bool):
        return str(prequel_data).lower()

    if isinstance(prequel_data, str):
        # If it's a numeric string (prequel ID)
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
    Special function to extract clean title
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
    Parses story data line
    """
    data = {}

    try:
        json_data = json.loads("{" + line + "}")
        story_id, story_data = next(iter(json_data.items()))

        data['id'] = story_id
        data['title'] = clean_text(story_data.get('title', ''))

        # Main fields mapping
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

        # Author
        if 'author' in story_data:
            author = story_data['author']
            data['author_name'] = clean_text(author.get('name', ''))
            data['author_id'] = clean_text(str(author.get('id', '')))
            if 'bio_html' in author:
                data['author_bio'] = clean_html_description(author['bio_html'])

        # File path
        if 'archive' in story_data and 'path' in story_data['archive']:
            data['archive_path'] = clean_text(story_data['archive']['path'])

        # Tags
        if 'tags' in story_data:
            data['tags'] = format_tags(story_data['tags'])

        # Prequel (handling all possible formats)
        if 'prequel' in story_data:
            data['prequel'] = format_prequel(story_data['prequel'])

        return data

    except json.JSONDecodeError:
        return parse_line_fallback(line)

def parse_line_fallback(line):
    """
    Fallback parsing method using regex with reliable tag processing
    """
    data = {}

    # Extract ID
    id_match = re.search(r'"(\d+)":\s*{', line)
    if id_match:
        data['id'] = id_match.group(1)

    # Story title
    data['title'] = extract_title(line)

    # Find ALL num_words matches and take LAST one
    num_words_matches = re.findall(r'"num_words":\s*(\d+)', line)
    if num_words_matches:
        data['num_words'] = num_words_matches[-1]  # take last value

    # Descriptions
    html_fields = {
        'description_html': r'"description_html":\s*"([^"]*)"',
        'short_description': r'"short_description":\s*"([^"]*)"'
    }

    for field, pattern in html_fields.items():
        match = re.search(pattern, line)
        if match:
            data[field] = clean_html_description(match.group(1))

    # Author
    author_match = re.search(r'"author":\s*{.*?"name":\s*"([^"]*)".*?"id":\s*(\d+)', line, re.DOTALL)
    if author_match:
        data['author_name'] = clean_text(author_match.group(1))
        data['author_id'] = clean_text(author_match.group(2))
        bio_match = re.search(r'"bio_html":\s*"([^"]*)"', line)
        if bio_match:
            data['author_bio'] = clean_html_description(bio_match.group(1))

    # Other main fields
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

    # File path
    path_match = re.search(r'"archive":\s*{.*?"path":\s*"([^"]+)"', line, re.DOTALL)
    if path_match:
        data['archive_path'] = clean_text(path_match.group(1))

    # Tags
    tags_match = re.search(r'"tags":\s*(\[[^\]]*\])', line)
    if tags_match:
        try:
            tags_data = json.loads(tags_match.group(1))
            if isinstance(tags_data, list):
                data['tags'] = format_tags(tags_data)
        except json.JSONDecodeError:
            # Fallback for manual parsing if JSON is invalid
            tag_items = re.finditer(r'\{"type":\s*"([^"]*)".*?"name":\s*"([^"]*)"', tags_match.group(1), re.DOTALL)
            tags_list = []
            for tag in tag_items:
                tags_list.append({
                    'type': tag.group(1),
                    'name': tag.group(2)
                })
            if tags_list:
                data['tags'] = format_tags(tags_list)

    # Prequel (extended fallback processing)
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
    Process Fimfiction log file with progress bar and detailed statistics
    """

    # Count total lines in file
    print("\n🔍 Counting total lines...")
    with open(input_path, 'r', encoding='utf-8') as f:
        total_lines = sum(1 for _ in f)

    print(f"\n🚀 Starting processing of {total_lines:,} lines at {datetime.now().strftime('%H:%M:%S')}")
    print(f"📂 Input file: {input_path} ({os.path.getsize(input_path) / 1024 / 1024:.1f} MB)")
    print(f"📝 Output file: {output_csv}")

    fieldnames = [
        'id', 'title', 'author_name', 'author_id', 'author_bio',
        'description_html', 'short_description',
        'completion_status', 'content_rating',
        'tags', 'prequel',
        'num_words', 'rating',
        'num_views', 'num_likes', 'num_dislikes', 'num_comments',
        'date_published', 'date_updated', 'archive_path'
    ]

    # Processing statistics
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
            # Initialize progress bar
            with tqdm(total=total_lines,
                      desc="⏳ Processing",
                      unit="line",
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
                            # Final cleaning of all fields
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
                            stats['errors'].append(f"Line {line_num}: no id or title")
                    except Exception as e:
                        stats['skipped_errors'] += 1
                        stats['errors'].append(f"Line {line_num}: {str(e)}")

    # Output final statistics
    print("\n✅ Done! Results:")
    print(f"├─ Successfully processed: {stats['processed']:,}")
    print(f"├─ Skipped empty lines: {stats['skipped_empty']:,}")
    print(f"├─ Skipped '338.1' lines: {stats['skipped_338']:,}")
    print(f"├─ Skipped due to errors: {stats['skipped_errors']:,}")
    print(f"└─ Skipped (no id/title): {stats['skipped_no_id_title']:,}")

    total_skipped = (stats['skipped_empty'] + stats['skipped_338'] +
                     stats['skipped_errors'] + stats['skipped_no_id_title'])
    print(f"\n📊 Total: {stats['processed']:,} of {total_lines:,} lines ({stats['processed'] / total_lines:.1%})")
    print(f"⏱ Execution time: {datetime.now().strftime('%H:%M:%S')}")
    print(f"💾 Result saved to: {output_csv}")

    # Output first 5 errors (if any)
    if stats['errors']:
        print("\n⚠ First 5 errors:")
        for err in stats['errors'][:5]:
            print(f"  - {err}")
        if len(stats['errors']) > 5:
            print(f"  ... and {len(stats['errors']) - 5} more errors")

        # Save full error log to file
        error_log_path = os.path.splitext(output_csv)[0] + '_errors.log'
        with open(error_log_path, 'w', encoding='utf-8') as err_file:
            err_file.write("\n".join(stats['errors']))
        print(f"📝 Full error log saved to: {error_log_path}")

if __name__ == "__main__":
    input_file = 'index.json'
    output_file = 'fimfiction_result.csv'

    process_fimfiction_log(input_file, output_file)