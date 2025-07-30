#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import csv
import json

def parse_input(lines):
    """
    解析制表符分隔的输入，每行依次对应：
      sentence, cp, time, background, statements...
    返回一个 dict 列表，缺失用 None 表示
    """
    reader = csv.reader(lines, delimiter='\t')
    result = []
    for row in reader:
        if not row or all(not cell.strip() for cell in row):
            continue

        sentence   = row[0].strip() if len(row) >= 1 and row[0].strip() else None
        cp         = row[1].strip() if len(row) >= 2 and row[1].strip() else None
        time_field = row[2].strip() if len(row) >= 3 and row[2].strip() else None
        background = row[3].strip() if len(row) >= 4 and row[3].strip() else None

        if len(row) >= 5:
            stmts = [cell.strip() for cell in row[4:] if cell.strip()]
            statements = stmts if stmts else None
        else:
            statements = None

        result.append({
            "sentence":   sentence,
            "cp":         cp,
            "time":       time_field,
            "background": background,
            "statements": statements
        })
    return result

def format_entry(e):
    """
    将单条记录 e 格式化为:
    {
        "sentence": "...",
        "cp": "...",
        "time": "...",
        "background": "" or "...",
        "statements": [] or [ "...", ... ]
    },
    最后带逗号
    """
    # 专门处理 background：空用 ""，否则用 JSON 编码
    def dump_background(val):
        return json.dumps(val, ensure_ascii=False) if val is not None else '""'

    # 专门处理 statements：空用 []，否则生成列表
    def dump_statements(val):
        if val is None:
            return "[]"
        items = []
        for stmt in val:
            items.append("        {0},".format(json.dumps(stmt, ensure_ascii=False)))
        if items:
            # 最后一行去掉逗号
            items[-1] = items[-1].rstrip(",")
        body = "\n".join(items)
        return "[\n{0}\n    ]".format(body)

    parts = []
    parts.append("{\n")
    parts.append("    \"sentence\": {0},\n".format(json.dumps(e["sentence"], ensure_ascii=False) if e["sentence"] is not None else "NULL"))
    parts.append("    \"cp\": {0},\n".format(json.dumps(e["cp"], ensure_ascii=False)       if e["cp"]       is not None else "NULL"))
    parts.append("    \"time\": {0},\n".format(json.dumps(e["time"], ensure_ascii=False)   if e["time"]    is not None else "NULL"))
    parts.append("    \"background\": {0},\n".format(dump_background(e["background"])))
    parts.append("    \"statements\": {0}\n".format(dump_statements(e["statements"])))
    parts.append("},")
    return "".join(parts)

def main():
    # 从标准输入读取；也可改为打开文件
    if sys.stdin.isatty():
        lines = open('data.txt', 'r', encoding='utf-8')
    else:
        lines = sys.stdin

    records = parse_input(lines)

    # 写入到 output.txt
    with open('output.txt', 'w', encoding='utf-8') as fout:
        for rec in records:
            fout.write(format_entry(rec) + '\n')

if __name__ == '__main__':
    main()