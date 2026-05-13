import os
import json

with open("config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

DIRS = config.get("directories", [])
OUTPUT_FILE = "straight_quotes.txt"

found = 0
skipped = 0

with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
    for root_dir in DIRS:
        if not os.path.exists(root_dir):
            print(f"[警告] 目录不存在: {root_dir}")
            continue

        for dirpath, dirnames, filenames in os.walk(root_dir):
            for name in dirnames + filenames:
                if "'" not in name:
                    skipped += 1
                    continue

                rel_path = os.path.relpath(os.path.join(dirpath, name), root_dir)
                out.write(rel_path + "\n")
                print(rel_path)
                found += 1

print(f"\n====== 处理完成 ======")
print(f"含直单引号的文件/目录: {found}")
print(f"跳过数量（无单引号）: {skipped}")
print(f"结果已写入: {OUTPUT_FILE}")
