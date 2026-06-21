#!/usr/bin/env python3
"""
Simple script to manage scripts-config.json for Js-Scripts
Run this script to add, list, or remove scripts from your collection
"""

import json
import os
from pathlib import Path

CONFIG_FILE = "scripts-config.json"


def load_config():
    """Load the scripts configuration from JSON file"""
    if not os.path.exists(CONFIG_FILE):
        return {"fivem_scripts": [], "paid_scripts": []}
    
    with open(CONFIG_FILE, 'r') as f:
        config = json.load(f)
        if "paid_scripts" not in config:
            config["paid_scripts"] = []
        return config


def save_config(config):
    """Save the scripts configuration to JSON file"""
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)
    print(f"\n✓ Configuration saved to {CONFIG_FILE}")


def list_scripts(config):
    """List all current scripts"""
    free_scripts = config.get("fivem_scripts", [])
    paid_scripts = config.get("paid_scripts", [])
    
    if not free_scripts and not paid_scripts:
        print("\nNo scripts found in configuration.")
        return
    
    print(f"\n{'='*60}")
    print(f"Current Scripts")
    print(f"{'='*60}")
    
    if free_scripts:
        print(f"\n--- Free Scripts ({len(free_scripts)} total) ---")
        for i, script in enumerate(free_scripts, 1):
            print(f"\n{i}. {script['name']}")
            if script.get('repo'):
                print(f"   Repo: {script['repo']}")
            if script.get('tebex_url'):
                print(f"   Tebex: {script['tebex_url']}")
                print(f"   Description: {script.get('description', 'No description')}")
            print(f"   YouTube ID: {script['youtube_id']}")
    
    if paid_scripts:
        print(f"\n--- Paid Scripts ({len(paid_scripts)} total) ---")
        for i, script in enumerate(paid_scripts, 1):
            print(f"\n{i}. {script['name']} 💎")
            print(f"   Description: {script.get('description', 'No description')}")
            print(f"   YouTube ID: {script['youtube_id']}")
            print(f"   Tebex URL: {script['tebex_url']}")


def add_script(config, batch_mode=False):
    """Add a new script to the configuration"""
    print("\n--- Add New Script ---")
    
    script_type = input("Script type (free/paid): ").strip().lower()
    if script_type not in ['free', 'paid']:
        print("❌ Please enter 'free' or 'paid'")
        return False
    
    name = input("Script name: ").strip()
    if not name:
        print("❌ Script name is required!")
        return False
    
    youtube_id = input("YouTube video ID: ").strip()
    if not youtube_id:
        print("❌ YouTube ID is required!")
        return False
    
    new_script = {
        "name": name,
        "youtube_id": youtube_id
    }
    
    if script_type == 'paid':
        description = input("Description: ").strip()
        tebex_url = input("Tebex purchase URL: ").strip()
        if not tebex_url:
            print("❌ Tebex URL is required for paid scripts!")
            return False
        new_script["description"] = description
        new_script["tebex_url"] = tebex_url
        config["paid_scripts"].append(new_script)
    else:
        # Free scripts can have Tebex, GitHub, or both
        has_tebex = input("Host on Tebex? (y/n): ").strip().lower() == 'y'
        has_github = input("Host on GitHub? (y/n): ").strip().lower() == 'y'
        
        if not has_tebex and not has_github:
            print("❌ Script must be hosted on at least Tebex or GitHub!")
            return False
        
        if has_tebex:
            description = input("Description: ").strip()
            tebex_url = input("Tebex URL: ").strip()
            if not tebex_url:
                print("❌ Tebex URL is required!")
                return False
            new_script["description"] = description
            new_script["tebex_url"] = tebex_url
        
        if has_github:
            repo = input("GitHub repository (username/repo-name): ").strip()
            if not repo:
                print("❌ Repository is required!")
                return False
            new_script["repo"] = repo
        
        config["fivem_scripts"].append(new_script)
    
    save_config(config)
    print(f"\n✓ Added '{name}' to configuration!")
    
    if batch_mode:
        continue_adding = input("\nAdd another script? (y/n): ").strip().lower()
        return continue_adding == 'y'
    return False


def remove_script(config):
    """Remove a script from the configuration"""
    free_scripts = config.get("fivem_scripts", [])
    paid_scripts = config.get("paid_scripts", [])
    
    if not free_scripts and not paid_scripts:
        print("\nNo scripts found to remove.")
        return
    
    list_scripts(config)
    
    try:
        choice = input("\nEnter script number to remove (or 'cancel'): ").strip()
        
        if choice.lower() == 'cancel':
            print("Cancelled.")
            return
        
        index = int(choice) - 1
        
        # Check if it's in free scripts
        if 0 <= index < len(free_scripts):
            removed = free_scripts.pop(index)
            save_config(config)
            print(f"\n✓ Removed '{removed['name']}' from configuration!")
        # Check if it's in paid scripts
        elif 0 <= index - len(free_scripts) < len(paid_scripts):
            paid_index = index - len(free_scripts)
            removed = paid_scripts.pop(paid_index)
            save_config(config)
            print(f"\n✓ Removed '{removed['name']}' from configuration!")
        else:
            print("❌ Invalid script number!")
    
    except ValueError:
        print("❌ Please enter a valid number!")


def extract_github_repo(url):
    """Extract username/repo from GitHub URL"""
    if "github.com/" in url:
        parts = url.split("github.com/")
        if len(parts) > 1:
            repo = parts[1].replace(".git", "").strip("/")
            return repo
    return None


def extract_youtube_id(url):
    """Extract video ID from YouTube URL"""
    if "youtube.com/watch?v=" in url:
        parts = url.split("v=")
        if len(parts) > 1:
            return parts[1].split("&")[0]
    elif "youtu.be/" in url:
        parts = url.split("youtu.be/")
        if len(parts) > 1:
            return parts[1].split("?")[0]
    return None


def add_from_urls(config, batch_mode=False):
    """Add a script using full URLs (easier method)"""
    print("\n--- Add Script from URLs ---")
    
    script_type = input("Script type (free/paid): ").strip().lower()
    if script_type not in ['free', 'paid']:
        print("❌ Please enter 'free' or 'paid'")
        return False
    
    name = input("Script name: ").strip()
    if not name:
        print("❌ Script name is required!")
        return False
    
    youtube_url = input("YouTube video URL: ").strip()
    youtube_id = extract_youtube_id(youtube_url)
    
    if not youtube_id:
        print("❌ Could not extract video ID from YouTube URL!")
        return False
    
    new_script = {
        "name": name,
        "youtube_id": youtube_id
    }
    
    if script_type == 'paid':
        description = input("Description: ").strip()
        tebex_url = input("Tebex purchase URL: ").strip()
        if not tebex_url:
            print("❌ Tebex URL is required for paid scripts!")
            return False
        new_script["description"] = description
        new_script["tebex_url"] = tebex_url
        config["paid_scripts"].append(new_script)
    else:
        # Free scripts can have Tebex, GitHub, or both
        has_tebex = input("Host on Tebex? (y/n): ").strip().lower() == 'y'
        has_github = input("Host on GitHub? (y/n): ").strip().lower() == 'y'
        
        if not has_tebex and not has_github:
            print("❌ Script must be hosted on at least Tebex or GitHub!")
            return False
        
        if has_tebex:
            description = input("Description: ").strip()
            tebex_url = input("Tebex URL: ").strip()
            if not tebex_url:
                print("❌ Tebex URL is required!")
                return False
            new_script["description"] = description
            new_script["tebex_url"] = tebex_url
        
        if has_github:
            github_url = input("GitHub repository URL: ").strip()
            repo = extract_github_repo(github_url)
            if not repo:
                print("❌ Could not extract repository from GitHub URL!")
                return False
            new_script["repo"] = repo
        
        config["fivem_scripts"].append(new_script)
    
    save_config(config)
    print(f"\n✓ Added '{name}' to configuration!")
    if script_type == 'paid':
        print(f"  Description: {description}")
        print(f"  YouTube ID: {youtube_id}")
        print(f"  Tebex URL: {tebex_url}")
    else:
        if new_script.get("tebex_url"):
            print(f"  Description: {new_script.get('description', 'N/A')}")
            print(f"  Tebex URL: {new_script['tebex_url']}")
        if new_script.get("repo"):
            print(f"  Repo: {new_script['repo']}")
        print(f"  YouTube ID: {youtube_id}")
    
    if batch_mode:
        continue_adding = input("\nAdd another script? (y/n): ").strip().lower()
        return continue_adding == 'y'
    return False


def batch_add_mode(config):
    """Batch mode for adding multiple scripts quickly"""
    print("\n" + "="*60)
    print("BATCH MODE - Add Multiple Scripts")
    print("="*60)
    print("You will be prompted to add scripts continuously.")
    print("Type 'quit' as the script name to exit batch mode.\n")
    
    while True:
        print("\n--- Add New Script ---")
        
        script_type = input("Script type (free/paid): ").strip().lower()
        if script_type not in ['free', 'paid']:
            print("❌ Please enter 'free' or 'paid'")
            continue
        
        name = input("Script name (or 'quit' to exit): ").strip()
        if name.lower() == 'quit':
            print("\nExiting batch mode...")
            break
        
        if not name:
            print("❌ Script name is required!")
            continue
        
        youtube_url = input("YouTube video URL: ").strip()
        youtube_id = extract_youtube_id(youtube_url)
        
        if not youtube_id:
            print("❌ Could not extract video ID from YouTube URL!")
            continue
        
        new_script = {
            "name": name,
            "youtube_id": youtube_id
        }
        
        if script_type == 'paid':
            description = input("Description: ").strip()
            tebex_url = input("Tebex purchase URL: ").strip()
            if not tebex_url:
                print("❌ Tebex URL is required for paid scripts!")
                continue
            new_script["description"] = description
            new_script["tebex_url"] = tebex_url
            config["paid_scripts"].append(new_script)
        else:
            # Free scripts can have Tebex, GitHub, or both
            has_tebex = input("Host on Tebex? (y/n): ").strip().lower() == 'y'
            has_github = input("Host on GitHub? (y/n): ").strip().lower() == 'y'
            
            if not has_tebex and not has_github:
                print("❌ Script must be hosted on at least Tebex or GitHub!")
                continue
            
            if has_tebex:
                description = input("Description: ").strip()
                tebex_url = input("Tebex URL: ").strip()
                if not tebex_url:
                    print("❌ Tebex URL is required!")
                    continue
                new_script["description"] = description
                new_script["tebex_url"] = tebex_url
            
            if has_github:
                github_url = input("GitHub repository URL: ").strip()
                repo = extract_github_repo(github_url)
                if not repo:
                    print("❌ Could not extract repository from GitHub URL!")
                    continue
                new_script["repo"] = repo
            
            config["fivem_scripts"].append(new_script)
        
        save_config(config)
        print(f"\n✓ Added '{name}' to configuration!")
        if script_type == 'paid':
            print(f"  Description: {description}")
            print(f"  YouTube ID: {youtube_id}")
            print(f"  Tebex URL: {tebex_url}")
        else:
            if new_script.get("tebex_url"):
                print(f"  Description: {new_script.get('description', 'N/A')}")
                print(f"  Tebex URL: {new_script['tebex_url']}")
            if new_script.get("repo"):
                print(f"  Repo: {new_script['repo']}")
            print(f"  YouTube ID: {youtube_id}")


def main():
    """Main menu"""
    print("\n" + "="*60)
    print("Js-Scripts - Script Configuration Manager")
    print("="*60)
    
    config = load_config()
    
    while True:
        print("\nOptions:")
        print("1. List all scripts")
        print("2. Add new script (manual entry)")
        print("3. Add new script (from URLs - easier)")
        print("4. Batch mode - Add multiple scripts quickly")
        print("5. Remove a script")
        print("6. Exit")
        
        choice = input("\nChoose an option (1-6): ").strip()
        
        if choice == "1":
            list_scripts(config)
        elif choice == "2":
            add_script(config)
        elif choice == "3":
            add_from_urls(config)
        elif choice == "4":
            batch_add_mode(config)
        elif choice == "5":
            remove_script(config)
        elif choice == "6":
            print("\nGoodbye!")
            break
        else:
            print("❌ Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
