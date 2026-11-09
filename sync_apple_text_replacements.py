#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Real-time Sync Apple System Text Replacements into Rime custom_phrase.txt
"""

import hashlib
import os
import sqlite3
import subprocess
import sys
import time

USER_DIR = os.path.expanduser('~/Library/Rime')
CUSTOM_PHRASE_FILE = os.path.join(USER_DIR, 'custom_phrase.txt')
APPLE_DB_FILE = os.path.expanduser('~/Library/KeyboardServices/TextReplacements.db')
APPLE_WAL_FILE = os.path.expanduser('~/Library/KeyboardServices/TextReplacements.db-wal')
HASH_CACHE_FILE = os.path.join(USER_DIR, '.apple_text_replacements.hash')

HEADER_TEMPLATE = """# Rime table
# coding: utf-8
#@/db_name	custom_phrase.txt
#@/db_type	tabledb
#
# 自定义短语 (与苹果系统设置文本替换实时双向同步)
# 格式：词汇<Tab>编码<Tab>权重
#
# 此行之后不能写注释"""

def get_db_fingerprint():
    """Calculate a fast fingerprint of the Apple text replacements database state."""
    hasher = hashlib.md5()
    for fpath in [APPLE_DB_FILE, APPLE_WAL_FILE]:
        if os.path.exists(fpath):
            try:
                mtime = os.path.getmtime(fpath)
                size = os.path.getsize(fpath)
                hasher.update(f"{fpath}:{mtime}:{size}".encode('utf-8'))
            except OSError:
                pass
    return hasher.hexdigest()

def fetch_apple_replacements():
    if not os.path.exists(APPLE_DB_FILE):
        return []
    
    uri = f"file:{APPLE_DB_FILE}?mode=ro"
    try:
        conn = sqlite3.connect(uri, uri=True, timeout=3.0)
        cursor = conn.cursor()
        cursor.execute("SELECT ZSHORTCUT, ZPHRASE FROM ZTEXTREPLACEMENTENTRY WHERE ZWASDELETED = 0;")
        rows = cursor.fetchall()
        conn.close()
        return [(shortcut.strip(), phrase.strip()) for shortcut, phrase in rows if shortcut and phrase]
    except Exception as e:
        print(f"Failed to query SQLite DB: {e}", file=sys.stderr)
        return []

def reload_squirrel():
    """Reload Squirrel in-memory dictionary seamlessly."""
    try:
        # 1. Post SquirrelReloadNotification via DistributedNotificationCenter
        from Foundation import NSDistributedNotificationCenter
        center = NSDistributedNotificationCenter.defaultCenter()
        center.postNotificationName_object_userInfo_deliverImmediately_(
            'SquirrelReloadNotification', None, None, True
        )
    except Exception:
        pass

    # 2. Restart Squirrel process (macOS launches it back in 0.05s)
    try:
        subprocess.run(['killall', 'Squirrel'], check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception:
        pass

def sync(force=False):
    current_fp = get_db_fingerprint()
    
    if not force and os.path.exists(HASH_CACHE_FILE):
        try:
            with open(HASH_CACHE_FILE, 'r', encoding='utf-8') as f:
                last_fp = f.read().strip()
            if current_fp == last_fp:
                # No change in Apple database, skip
                return False
        except Exception:
            pass

    apple_entries = fetch_apple_replacements()
    if not apple_entries and not force:
        return False

    custom_lines = []
    seen = set()
    
    # Mandatory pinned entries for Japanese IME
    pinned = [
        ('ん', 'nn', '100'),
        ('ン', 'nn', '99'),
        ('ー', '-', '100'),
    ]
    for phrase, code, weight in pinned:
        seen.add((phrase, code))
        custom_lines.append(f"{phrase}\t{code}\t{weight}")

    # Add Apple text replacements
    apple_count = 0
    for code, phrase in apple_entries:
        phrase_clean = phrase.replace('\r\n', ' ').replace('\n', ' ')
        key = (phrase_clean, code)
        if key not in seen:
            seen.add(key)
            custom_lines.append(f"{phrase_clean}\t{code}\t100")
            apple_count += 1

    # Preserve other existing non-conflicting phrases from custom_phrase.txt
    if os.path.exists(CUSTOM_PHRASE_FILE):
        with open(CUSTOM_PHRASE_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line_str = line.strip()
                if not line_str or line_str.startswith('#') or line_str.startswith('@'):
                    continue
                parts = line_str.split('\t')
                if len(parts) >= 2:
                    p = parts[0].strip()
                    c = parts[1].strip()
                    w = parts[2].strip() if len(parts) >= 3 else '100'
                    if (p, c) not in seen:
                        seen.add((p, c))
                        custom_lines.append(f"{p}\t{c}\t{w}")

    # Write out updated custom_phrase.txt
    with open(CUSTOM_PHRASE_FILE, 'w', encoding='utf-8') as f:
        f.write(HEADER_TEMPLATE + "\n")
        f.write("\n".join(custom_lines) + "\n")

    # Update hash cache
    with open(HASH_CACHE_FILE, 'w', encoding='utf-8') as f:
        f.write(current_fp)

    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Synced {apple_count} text replacements from Apple Keyboard Services into custom_phrase.txt.")

    # Reload Squirrel immediately
    reload_squirrel()
    print("Squirrel reloaded. New phrases are active!")
    return True

if __name__ == '__main__':
    force_run = '--force' in sys.argv
    sync(force=force_run)
