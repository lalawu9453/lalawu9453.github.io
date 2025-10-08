# scripts/tag_processor.py
# This script is the "Central Controller" for managing tags.

import json
import frontmatter
from pathlib import Path
from dotenv import load_dotenv
import google.generativeai as genai
import os

# --- CONFIGURATION ---
CONTENT_DIR = "content/posts"
TAGS_DB_FILE = "data/tags.json"
GEMINI_API_KEY_NAME = "GEMINI_API_KEY"

# --- CONSTANTS ---
GEMINI_PROMPT_TEMPLATE = """
You are an expert SEO and content strategist specializing in generating relevant, concise, and impactful tags for blog posts.

Analyze the following article content and generate a list of the most relevant tags.

**Instructions:**
1.  **Analyze Content:** Read the article content carefully to understand its main topics, themes, and keywords.
2.  **Generate Tags:** Based on your analysis, suggest 3 to 5 highly relevant tags.
3.  **Maintain Consistency:** Here is a list of globally used tags for your reference. Prefer these if they are relevant: {global_tags}
4.  **Avoid Duplicates:** The article already has the following tags. Do not suggest them again: {existing_tags}
5.  **Format:** Return ONLY a comma-separated list of the new tags. Do not include any other text, titles, or explanations.

**Example Output:**
AI, Python, Web Development, SEO

**Article Content:**
---
{content}
---
"""

def get_project_root() -> Path:
    """Gets the absolute path of the project root directory."""
    return Path(__file__).resolve().parent.parent

def load_tags_database(root_dir: Path) -> list[str]:
    """Loads the global list of tags from the JSON database."""
    db_path = root_dir / TAGS_DB_FILE
    if not db_path.exists():
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

def call_gemini_api_for_tags(content: str, existing_tags: list[str], global_tags: list[str]) -> list[str]:
    """
    Calls the Gemini API to get tag suggestions for the given content.
    """
    cleaned_content = content[:300].strip().replace('\n', ' ')
    print(f"  - Calling Gemini API for content starting with: '{cleaned_content}...'")
    
    model = genai.GenerativeModel('gemini-2.0-flash')
    
    prompt = GEMINI_PROMPT_TEMPLATE.format(
        global_tags=', '.join(global_tags),
        existing_tags=', '.join(existing_tags),
        content=content
    )

    try:
        generation_config = genai.types.GenerationConfig(
            max_output_tokens=300,
            temperature=0.2
        )
        
        safety_settings = [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
        ]

        response = model.generate_content(
            prompt, 
            generation_config=generation_config,
            safety_settings=safety_settings
        )
        
        if response.parts:
            new_tags_str = "".join(part.text for part in response.parts).strip()
        else:
            print("  - Gemini API returned no valid parts. It might have been blocked.")
            new_tags_str = ""

        if not new_tags_str:
            print("  - Gemini API returned an empty response.")
            return []
            
        suggested_tags = [tag.strip() for tag in new_tags_str.split(',') if tag.strip()]
        
        existing_tags_lower = {t.lower() for t in existing_tags}
        new_suggestions = [tag for tag in suggested_tags if tag.lower() not in existing_tags_lower]
        
        return new_suggestions

    except Exception as e:
        print(f"  - Error calling Gemini API: {e}")
        return []


def save_post(post: frontmatter.Post, filepath: Path):
    """Saves the post object back to the markdown file."""
    try:
        # The frontmatter.dump function writes bytes, so we need to open the file in 'wb' mode.
        with open(filepath, 'wb') as f:
            frontmatter.dump(post, f)
        print(f"  - Successfully updated file: {filepath.name}")
    except Exception as e:
        print(f"  - Error saving file {filepath}: {e}")

def update_tags_database(tags_to_add: list[str], root_dir: Path):
    """Adds new tags to the global tag database."""
    if not tags_to_add:
        print("  - No new tags to sync to the database.")
        return

    db_path = root_dir / TAGS_DB_FILE
    try:
        with open(db_path, 'r', encoding='utf-8') as f:
            content = f.read()
            db_tags = json.loads(content) if content else []
        
        added_count = 0
        db_tags_lower = {t.lower() for t in db_tags}
        for tag in tags_to_add:
            if tag.lower() not in db_tags_lower:
                db_tags.append(tag)
                added_count += 1
        
        if added_count > 0:
            db_tags.sort(key=str.lower)
            with open(db_path, 'w', encoding='utf-8') as f:
                json.dump(db_tags, f, indent=2, ensure_ascii=False)
            print(f"  - Synced {added_count} new tags to the database.")
        else:
            print("  - All suggested tags already exist in the database.")

    except Exception as e:
        print(f"  - Error updating tag database: {e}")

def main():
    """Main execution function."""
    print("Starting the Central Controller: Tag Processor...")
    
    # --- Phase 0: Setup and Configuration ---
    print("\n--- Phase 0: Setup and Configuration ---")
    load_dotenv()
    project_root = get_project_root()
    print(f"Project root detected: {project_root}")

    api_key = os.getenv(GEMINI_API_KEY_NAME)
    if not api_key:
        print(f"Error: Gemini API key not found. Please set the '{GEMINI_API_KEY_NAME}' environment variable.")
        return
    genai.configure(api_key=api_key)
    print("Gemini API configured successfully.")

    global_tags = load_tags_database(project_root)
    print(f"Loaded {len(global_tags)} tags from the database.")

    # --- Phase 1: Quick Scan & Validation ---
    print("\n--- Phase 1: Quick Scan & Validation ---")
    files_to_process = []
    content_path = project_root / CONTENT_DIR
    if not content_path.is_dir():
        print(f"Error: Content directory not found at {content_path}")
        return

    for filepath in sorted(content_path.glob("**/*.md")):
        if 'mock' in filepath.parts:
            continue
        files_to_process.append(filepath)

    print(f"Scan complete. Found {len(files_to_process)}  files to process.")

    # --- Phase 2 & 3: AI Processing, Update & Sync ---
    print("\n--- Phase 2 & 3: AI Processing, Update & Sync ---")
    
    if not files_to_process:
        print("No markdown files found to process.")
        return

    for filepath in files_to_process:
        relative_filepath = filepath.relative_to(project_root)
        print(f"\nProcessing file: {relative_filepath}")
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                post = frontmatter.load(f)
            
            # We will process files that have few tags (e.g., less than 3)
            existing_tags = post.metadata.get('tags', [])
            if not isinstance(existing_tags, list):
                existing_tags = [existing_tags] if existing_tags else []

            if len(existing_tags) >= 3:
                print(f"  - Skipping: Already has {len(existing_tags)} tags.")
                continue
                
            print(f"  - Existing tags: {existing_tags}")

            suggested_new_tags = call_gemini_api_for_tags(post.content, existing_tags, global_tags)
            print(f"  - AI suggested new tags: {suggested_new_tags}")

            if suggested_new_tags:
                print("  --- Starting Update & Sync ---")
                combined_tags = existing_tags + suggested_new_tags
                post.metadata['tags'] = combined_tags
                save_post(post, filepath)
                update_tags_database(suggested_new_tags, project_root)
            else:
                print("  - No new tags suggested, skipping update.")
        except Exception as e:
            print(f"Error processing file {relative_filepath}: {e}")
    
    print("\nScript finished.")

if __name__ == "__main__":
    main()