import os
import json
import re

# -------------------------
# 读取配置文件
# -------------------------
with open("config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

MUSIC_DIRS = config.get("directories", [])
MUSIC_FORMATS = config.get("music_formats", [])
LYRICS_FORMATS = config.get("lyrics_formats", [])

# -------------------------
# 辅助函数
# -------------------------
def is_music_file(filename):
    return any(filename.lower().endswith(f".{ext.lower()}") for ext in MUSIC_FORMATS)

def is_lyrics_file(filename):
    return any(filename.lower().endswith(f".{ext.lower()}") for ext in LYRICS_FORMATS)

def extract_track_number(filename):
    match = re.match(r'^(\d+(?:-\d+)?)[\s\.]', filename)
    return match.group(1) if match else None

# -------------------------
# 主处理函数
# -------------------------
def process_directory(root_dir):
    success_count = 0
    skipped_only_song_or_lyrics = 0
    skipped_same_name = 0

    for dirpath, dirnames, filenames in os.walk(root_dir):

        # 当前目录的音乐文件
        music_files = [f for f in filenames if is_music_file(f)]

        # 构建音乐编号映射（编号 -> 文件名）
        music_map = {}
        for f in music_files:
            num = extract_track_number(f)
            if num:
                music_map[num] = f

        # 遍历每一个歌词文件（关键修改点）
        for lyr_file in filenames:
            if not is_lyrics_file(lyr_file):
                continue

            num = extract_track_number(lyr_file)
            if not num:
                print(f"[跳过] 无编号歌词文件: {os.path.join(dirpath, lyr_file)}")
                skipped_only_song_or_lyrics += 1
                continue

            music_file = music_map.get(num)
            if not music_file:
                print(f"[跳过] 未找到对应歌曲: {os.path.join(dirpath, lyr_file)}")
                skipped_only_song_or_lyrics += 1
                continue

            # 新歌词文件名 = 音乐文件名 + 原歌词扩展名
            lyr_ext = os.path.splitext(lyr_file)[1]
            new_lyr_name = os.path.splitext(music_file)[0] + lyr_ext

            if lyr_file == new_lyr_name:
                skipped_same_name += 1
                continue

            old_path = os.path.join(dirpath, lyr_file)
            new_path = os.path.join(dirpath, new_lyr_name)

            try:
                os.rename(old_path, new_path)
                success_count += 1
            except Exception as e:
                print(f"[错误] 重命名失败 {os.path.join(dirpath, lyr_file)} -> {new_lyr_name}: {e}")

    return success_count, skipped_only_song_or_lyrics, skipped_same_name

# -------------------------
# 执行
# -------------------------
total_success = 0
total_skipped_only = 0
total_skipped_same = 0

for root in MUSIC_DIRS:
    if not os.path.exists(root):
        print(f"[警告] 目录不存在: {root}")
        continue

    s, so, ss = process_directory(root)
    total_success += s
    total_skipped_only += so
    total_skipped_same += ss

# -------------------------
# 输出统计
# -------------------------
print("\n====== 处理完成 ======")
print(f"成功重命名: {total_success}")
print(f"跳过（缺少匹配）: {total_skipped_only}")
print(f"跳过（已一致）: {total_skipped_same}")
