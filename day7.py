#!/usr/bin/env python3
from typing import List

example = """$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k"""

def mkdirp(tree, path):
    sub = tree
    for part in path.split("/"):
        if path == "":
            continue
        if part not in sub:
            sub[part] = {}
        sub = sub[part]

def touch(tree, path, fn, size):
    sub = tree
    for part in path.split("/"):
        if path == "":
            continue
        if part not in sub:
            sub[part] = {}
        sub = sub[part]
    
    sub[fn] = (size)


def resolve_relative(path):
    parts = path.split("/")
    i = len(parts) -1
    res = []
    while i > 0:
        if parts[i] == "..":
            i -= 2
        elif parts[i] == "":
            i -= 1
        else:
            res.append(parts[i])
            i -= 1

    res = "/" + "/".join(res[::-1])
    return res

with open("input-7") as f:
    lines = [l.strip() for l in f.readlines()]

    cmds = []
    curcmd = None
    for line in lines:
        if line.startswith("$"):
            if curcmd != None:
                cmds.append(curcmd)
            cmd = line.lstrip("$ ")
            if cmd.startswith("cd"):
                curcmd = ("cd", cmd.split("cd ")[1])
            else:
                curcmd = (cmd, [])
        else:
            curcmd[1].append(line)
    cmds.append(curcmd)

    cursor = None
    tree = {}
    for cmd in cmds:
        if cmd[0] == "ls":
            for file in cmd[1]:
                if file.startswith("dir"):
                    continue
                sz, fn = file.split(" ")
                touch(tree, cursor, fn, int(sz))

        if cmd[0] == "cd":
            if cursor == None:
                cursor = cmd[1]
            else:
                cursor += f"/{cmd[1]}"
        cursor = resolve_relative(cursor)
        mkdirp(tree, cursor)
        
    result = 0
    def traverse(sub):
        global result
        dir_size = 0
        for key in sub:
            if type(sub[key]) != int:
                continue
            dir_size += sub[key]
        for key in sub:
            if type(sub[key]) is dict:
                sub_size = traverse(sub[key])
                dir_size += sub_size
        if dir_size <= 100000:
            result += dir_size
        return dir_size
            
    traverse(tree)
        
    print(result)
