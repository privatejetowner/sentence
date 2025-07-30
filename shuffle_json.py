#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random

def split_json_units(text):
    """
    根据大括号层级将文本分割成完整的 JSON 对象列表。
    """
    units = []
    buf = ''
    level = 0
    for ch in text:
        if ch == '{':
            if level == 0:
                buf = ch
            else:
                buf += ch
            level += 1
        elif ch == '}' and level > 0:
            buf += ch
            level -= 1
            if level == 0:
                units.append(buf)
        elif level > 0:
            buf += ch
    return units

def shuffle_json_text(text):
    """
    接受包含多个 {…} 单元的字符串，
    随机打乱后以逗号+换行拼接返回结果字符串。
    """
    units = split_json_units(text)
    random.shuffle(units)
    return ',\n'.join(units)

def shuffle_json_file(input_path, output_path=None):
    """
    从 input_path 读取文本，随机打乱所有 {…} 单元。
    如果提供了 output_path，则结果写入该文件，函数返回 None；
    否则返回结果字符串。
    """
    with open(input_path, 'r', encoding='utf-8') as f:
        text = f.read()

    shuffled = shuffle_json_text(text)

    if output_path:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(shuffled)
        return None
    else:
        return shuffled

def main():
    print("=== JSON 块随机打乱工具 ===")
    inp = input("请输入输入文件路径：").strip()
    out = input("请输入输出文件路径（留空则打印到控制台）：").strip()
    if out == '':
        out = None

    try:
        result = shuffle_json_file(inp, out)
        if out:
            print("✅ 已将打乱结果写入：{0}".format(out))
        else:
            print("\n--- 打乱后的结果开始 ---\n")
            print(result)
            print("\n--- 打乱后的结果结束 ---\n")
    except Exception as e:
        print("❌ 发生错误：{0}".format(e))

if __name__ == '__main__':
    main()
