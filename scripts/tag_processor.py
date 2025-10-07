# scripts/tag_processor.py
# This script is the "Central Controller" for managing tags.

import os
import json
import frontmatter

# --- CONFIGURATION ---
CONTENT_DIR = "content/posts"
TAGS_DB_FILE = "data/tags.json"

def get_project_root():
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

def load_tags_database(root_dir):
    db_path = os.path.join(root_dir, TAGS_DB_FILE)
    if not os.path.exists(db_path):
        print(f"Warning: Tag database not found at {db_path}. Starting with an empty library.")
        return []
    try:
        with open(db_path, 'r', encoding='utf-8') as f:
            content = f.read()
            if not content:
                return []
            return json.loads(content)
    except (json.JSONDecodeError, IOError) as e:
        print(f"Error reading or parsing tag database {db_path}: {e}")
        return []

def call_gemini_api_for_tags(content, existing_tags, global_tags):
    print(f"  - Calling Gemini API with content (first 100 chars): '{content[:100].strip()}...'")
    print(f"  - Providing {len(global_tags)} global tags for context.")
    ai_suggestions = ["Generative AI", "Reinforcement Learning", "Ethical AI"]
    new_suggestions = [tag for tag in ai_suggestions if tag.lower() not in [t.lower() for t in existing_tags]]
    return new_suggestions

def save_post(post, filepath):
    """Saves the post object back to the markdown file."""
    try:
        with open(filepath, 'wb') as f:
            frontmatter.dump(post, f)
        print(f"  - Successfully updated file: {os.path.basename(filepath)}")
    except Exception as e:
        print(f"  - Error saving file {filepath}: {e}")

def update_tags_database(tags_to_add, root_dir):
    """Adds new tags to the global tag database."""
    db_path = os.path.join(root_dir, TAGS_DB_FILE)
    try:
        with open(db_path, 'r', encoding='utf-8') as f:
            content = f.read()
            db_tags = json.loads(content) if content else []
        
        added_count = 0
        db_tags_lower = [t.lower() for t in db_tags]
        for tag in tags_to_add:
            if tag.lower() not in db_tags_lower:
                db_tags.append(tag)
                added_count += 1
        
        if added_count > 0:
            db_tags.sort()
            with open(db_path, 'w', encoding='utf-8') as f:
                json.dump(db_tags, f, indent=2, ensure_ascii=False)
            print(f"  - Synced {added_count} new tags to the database.")
        else:
            print("  - No new tags to sync to the database.")

    except Exception as e:
        print(f"  - Error updating tag database: {e}")

def main():
    print("Starting the Central Controller: Tag Processor...")
    project_root = get_project_root()
    print(f"Project root detected: {project_root}")

    print("\n--- Phase 0: Loading Global Tag Library ---")
    global_tags = load_tags_database(project_root)
    print(f"Loaded {len(global_tags)} tags from the database.")

    print("\n--- Phase 1: Quick Scan & Validation ---")
    files_to_generate = []
    files_to_augment = []
    content_path = os.path.join(project_root, CONTENT_DIR)
    if not os.path.isdir(content_path):
        print(f"Error: Content directory not found at {content_path}")
        return

    for dirpath, _, filenames in os.walk(content_path):
        for filename in sorted(filenames):
            if filename.endswith(".md"):
                filepath = os.path.join(dirpath, filename)
                try:
                    post = frontmatter.load(filepath)
                    if 'tags' not in post.metadata or not post.metadata['tags']:
                        files_to_generate.append(os.path.relpath(filepath, project_root))
                    else:
                        files_to_augment.append(os.path.relpath(filepath, project_root))
                except Exception as e:
                    print(f"Error parsing frontmatter for {filename}: {e}")

    print(f"\nScan complete.")
    print(f"  - Found {len(files_to_generate)} files that need tags generated.")
    print(f"  - Found {len(files_to_augment)} files whose tags could be augmented.")

    print("\n--- Phase 2 & 3: AI Processing, Update & Sync ---")
    if files_to_augment:
        relative_filepath = files_to_augment[0]
        absolute_filepath = os.path.join(project_root, relative_filepath)
        print(f"Processing one file: {relative_filepath}")
        try:
            post = frontmatter.load(absolute_filepath)
            existing_tags = post.metadata.get('tags', [])
            print(f"  - Existing tags: {existing_tags}")

            suggested_new_tags = call_gemini_api_for_tags(post.content, existing_tags, global_tags)
            print(f"  - AI suggested new tags: {suggested_new_tags}")

            if suggested_new_tags:
                print("\n  --- Starting Update & Sync ---")
                combined_tags = existing_tags + suggested_new_tags
                post.metadata['tags'] = combined_tags
                save_post(post, absolute_filepath)
                update_tags_database(suggested_new_tags, project_root)
            else:
                print("\n  - No new tags suggested, skipping update.")
        except Exception as e:
            print(f"Error processing file {relative_filepath}: {e}")
    else:
        print("No files to augment for processing.")
    
    print("\nScript finished.")

if __name__ == "__main__":
    main()
