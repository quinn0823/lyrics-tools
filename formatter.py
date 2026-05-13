import os
import re
import json
from decimal import Decimal, ROUND_HALF_UP

CONFIG_PATH = "config.json"
TIMESTAMP_PATTERN = re.compile(r"\[(\d{2}):(\d{2})\.(\d{2,3})\]")

# ------------------ 工具函数 ------------------
def round_timestamp(m, s, ms):
    total = int(m) * 60000 + int(s) * 1000 + int(ms)
    rounded = Decimal(total / 10).quantize(0, ROUND_HALF_UP)
    total = int(rounded) * 10
    mm = total // 60000
    ss = (total % 60000) // 1000
    cs = (total % 1000) // 10
    return f"[{mm:02d}:{ss:02d}.{cs:02d}]", total

def parse_ms(m, s, cs):
    if len(cs) == 2:
        ms = int(cs) * 10
    else:
        ms = int(cs)
    return int(m) * 60000 + int(s) * 1000 + ms

def format_ms(total):
    mm = total // 60000
    ss = (total % 60000) // 1000
    cs = (total % 1000) // 10
    return f"[{mm:02d}:{ss:02d}.{cs:02d}]"

# ------------------ 核心处理 ------------------
def process_lrc_file(path):
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    modified_format = False
    modified_order = False

    # 收集所有时间戳（按出现顺序）
    timeline = []  # 每项：{line_idx, span, text, ms}

    # ---------- 第一步：格式处理 ----------
    new_lines = lines.copy()

    for i, line in enumerate(lines):
        matches = list(TIMESTAMP_PATTERN.finditer(line))
        if not matches:
            continue

        rebuilt = ""
        last_pos = 0

        for mobj in matches:
            start, end = mobj.span()
            m, s, cs = mobj.groups()
            orig = mobj.group()

            # 拼接前段
            rebuilt += line[last_pos:start]

            if len(cs) == 3:
                new_ts, ms = round_timestamp(m, s, cs)
                if new_ts != orig:
                    modified_format = True
            else:
                ms = parse_ms(m, s, cs)
                new_ts = orig

            rebuilt += new_ts

            timeline.append({
                "line": i,
                "text": new_ts,
                "ms": ms
            })

            last_pos = end

        rebuilt += line[last_pos:]
        new_lines[i] = rebuilt

    # ---------- 第二步：递增修正（从后往前） ----------
    for i in range(len(timeline) - 2, -1, -1):
        if timeline[i]["ms"] > timeline[i + 1]["ms"]:
            timeline[i]["ms"] = timeline[i + 1]["ms"]
            timeline[i]["text"] = format_ms(timeline[i + 1]["ms"])
            modified_order = True

    # ---------- 第三步：重新写回（按顺序逐个替换） ----------
    if modified_order:
        # 每行重新构建（避免 replace 问题）
        line_map = {}

        for item in timeline:
            line_map.setdefault(item["line"], []).append(item)

        final_lines = new_lines.copy()

        for line_idx, items in line_map.items():
            original_line = new_lines[line_idx]
            matches = list(TIMESTAMP_PATTERN.finditer(original_line))

            rebuilt = ""
            last = 0

            for idx, mobj in enumerate(matches):
                start, end = mobj.span()

                rebuilt += original_line[last:start]
                rebuilt += items[idx]["text"]  # 用修正后的
                last = end

            rebuilt += original_line[last:]
            final_lines[line_idx] = rebuilt

    else:
        final_lines = new_lines

    # ---------- 输出 ----------
    if modified_format or modified_order:
        with open(path, "w", encoding="utf-8") as f:
            f.writelines(final_lines)

        reasons = []
        if modified_format:
            reasons.append("时间戳格式")
        if modified_order:
            reasons.append("时间戳递增")

        print(f"修改文件: {path} ({' & '.join(reasons)})")
        return True
    else:
        # print(f"未修改文件: {path}")
        return False


# ------------------ 遍历 ------------------
def traverse(dirs):
    m, s = 0, 0
    for d in dirs:
        for root, _, files in os.walk(d):
            for f in files:
                if f.lower().endswith(".lrc"):
                    p = os.path.join(root, f)
                    if process_lrc_file(p):
                        m += 1
                    else:
                        s += 1

    print("\n==== 统计 ====")
    print("修改文件数量:", m)
    print("跳过文件数量:", s)


# ------------------ 主程序 ------------------
if __name__ == "__main__":
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        cfg = json.load(f)

    traverse(cfg.get("directories", []))
