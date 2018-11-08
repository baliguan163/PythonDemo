#!/usr/bin/env python
# coding=utf-8

import os
import random


def scan_files(directory, prefix=None, postfix=None):
    files_list = []

    for root, sub_dirs, files in os.walk(directory):
        for special_file in files:
            if postfix:
                if special_file.endswith(postfix):
                    files_list.append(os.path.join(root, special_file))
            elif prefix:
                if special_file.startswith(prefix):
                    files_list.append(os.path.join(root, special_file))
            else:
                files_list.append(os.path.join(root, special_file))

    return files_list

file_list=scan_files(r'H:\开发视频\temp\mm131')
file_sum=len(file_list)
print(file_sum)
index=random.randint(0, file_sum)
print(index)
print(file_list[index])
