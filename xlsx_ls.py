#!/usr/bin/env python
#-*- coding:utf-8 -*-
"""Doc string
"""
import sys
import re
import xlsxwriter

def main():
    """
    Main
    """
    params = sys.argv
    log = params[1]
    name = params[2]

    workbook = xlsxwriter.Workbook(name + ".xlsx")
    worksheet = workbook.add_worksheet(name)

    pattern = r"^/"
    dirpattern = re.compile(pattern)
    pattern = r"^total "
    totalpattern = re.compile(pattern)
    pattern = r" +"
    spacepattern = re.compile(pattern)

    with open(log) as f_obj:
        line = f_obj.readline()
        headers = [
            "Directory",
            "Permission",
            "Hardlink",
            "User",
            "Group",
            "Byte",
            "Month",
            "Day",
            "Year or Time",
            "File"
        ]
        count = 0
        for header in headers:
            worksheet.write(0, count, header)
            count += 1
        count = 1
        while line:
            line = line.rstrip()
            if dirpattern.match(line):
                worksheet.write(count, 0, line[:-1])
            elif totalpattern.match(line):
                count -= 1
            elif len(line) == 0:
                count -= 1
            else:
                line = spacepattern.sub(" ", line)
                split_line = line.split(" ")
                worksheet.write(count, 1, split_line[0])
                worksheet.write(count, 2, split_line[1])
                worksheet.write(count, 3, split_line[2])
                worksheet.write(count, 4, split_line[3])
                worksheet.write(count, 5, split_line[4])
                worksheet.write(count, 6, split_line[5])
                worksheet.write(count, 7, split_line[6])
                worksheet.write(count, 8, split_line[7])
                worksheet.write(count, 9, str(split_line[8:]))
            line = f_obj.readline()
            count += 1

if __name__ == '__main__':
    main()
