import os
import json
from markdownify import markdownify as md
import frontmatter

# Define the base directory where your Anki JSON exports are located
base_dir = '/media/manansharma/583a4f1d-8c93-4f7c-83cc-719f228369bf/Anki-notes-export/anarchy1923-anki'

output_dir = '/media/manansharma/583a4f1d-8c93-4f7c-83cc-719f228369bf/Anki-notes-export/anarchy1923-ankitoobsidian'

# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)

def process_deck(deck_path, output_path):
    # Load the deck.json file
    with open(os.path.join(deck_path, 'deck.json'), 'r', encoding='utf-8') as f:
        deck_data = json.load(f)

    # Process each card in the deck
    for idx, card in enumerate(deck_data['notes']):
        # Create the markdown content
        card_content = md(card['fields'][0])  # Assuming the first field is the card content
        card_tags = card.get('tags', [])
        
        # Prepare front matter with tags
        post = frontmatter.loads(card_content)
        post['tags'] = card_tags

        # Use a fallback for the filename if 'noteId' is not present
        card_name = f"{card.get('noteId', f'card_{idx}')}.md"  # You can customize the filename format
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
            process_deck(deck_path, output_path)

# Run the conversion process
process_all_decks(base_dir, output_dir)
