import os
import json
from markdownify import markdownify as md
import frontmatter

# Define the base directory where your Anki JSON exports are located
base_dir = '/media/manansharma/583a4f1d-8c93-4f7c-83cc-719f228369bf/Anki-notes-export/anarchy1923-anki'

output_dir = '/media/manansharma/583a4f1d-8c93-4f7c-83cc-719f228369bf/Anki-notes-export/anarchy1923-obsidian'

# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)

def sanitize_filename(filename):
    # Remove any characters that are not allowed in filenames
    return "".join(c for c in filename if c.isalnum() or c in (' ', '_', '-')).rstrip()

def process_deck(deck_path, output_path, deck_name):
    # Load the deck.json file
    with open(os.path.join(deck_path, 'deck.json'), 'r', encoding='utf-8') as f:
        deck_data = json.load(f)

    # Process each card in the deck
    for idx, card in enumerate(deck_data['notes']):
        # Determine if the card is a cloze card
        is_cloze = '{{c' in card['fields'][0]

        # Create the markdown content
        front = card['fields'][0]  # Assuming the first field is the front (question)
        back = card['fields'][1] if len(card['fields']) > 1 else ''  # Assuming the second field is the back (answer)
        card_tags = card.get('tags', [])
        
        # Prepare front matter with tags and deck name
        post = frontmatter.loads(md(back))
        post['tags'] = card_tags
        post['deck'] = deck_name

        # Use the front (question) as the filename, sanitized
        if is_cloze:
            filename = sanitize_filename(front.split('{{c')[0])[:50]  # Use part of the cloze text
        else:
            filename = sanitize_filename(front)[:50]  # Use the front text

        card_name = f"{filename}.md"
        card_output_path = os.path.join(output_path, card_name)
        with open(card_output_path, 'w', encoding='utf-8') as f:
            f.write(frontmatter.dumps(post))

    # Copy media files if present
    media_path = os.path.join(deck_path, 'media')
    if os.path.exists(media_path):
        output_media_path = os.path.join(output_path, 'media')
        os.makedirs(output_media_path, exist_ok=True)
        for media_file in os.listdir(media_path):
            full_media_file = os.path.join(media_path, media_file)
            if os.path.isfile(full_media_file):
                os.system(f'cp "{full_media_file}" "{output_media_path}/"')

def process_all_decks(base_dir, output_dir):
    for root, dirs, files in os.walk(base_dir):
        for dir_name in dirs:
            deck_path = os.path.join(root, dir_name)
            relative_path = os.path.relpath(deck_path, base_dir)
            output_path = os.path.join(output_dir, relative_path)

            # Create the corresponding output directory
            os.makedirs(output_path, exist_ok=True)

            # Process the deck
            process_deck(deck_path, output_path, dir_name)

# Run the conversion process
process_all_decks(base_dir, output_dir)
