import os

BASE_DIR = "htm_all_linie"

def remove_empty_dirs(base_dir):
    removed = 0
    for dir_name in os.listdir(base_dir):
        dir_path = os.path.join(base_dir, dir_name)
        if os.path.isdir(dir_path) and not os.listdir(dir_path):
            os.rmdir(dir_path)
            print(f"🗑️ Removed empty directory: {dir_path}")
            removed += 1
    print(f"\n✅ Done. Removed {removed} empty directories.")

remove_empty_dirs(BASE_DIR)
