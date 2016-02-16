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
    xlsx_format = workbook.add_format()
    xlsx_format.set_bg_color('gray')
    pattern = r"^/"
    dirpattern = re.compile(pattern)
    pattern = r"^total "
    totalpattern = re.compile(pattern)
    pattern = r" +"
    spacepattern = re.compile(pattern)
    pattern = r".png|.jpg|.gif"
    pngpattern = re.compile(pattern)
    pattern = r"200[0-9]|2015"
    yearpattern = re.compile(pattern)

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
                # Permission
                worksheet.write(count, 1, split_line[0])
                # Hardlink
                worksheet.write(count, 2, split_line[1])
                # User
                worksheet.write(count, 3, split_line[2])
                # Group
                worksheet.write(count, 4, split_line[3])
                # Byte
                worksheet.write(count, 5, split_line[4])
                # Month
                worksheet.write(count, 6, split_line[5])
                # Day
                worksheet.write(count, 7, split_line[6])
                # Year or Time
                if yearpattern.match(split_line[7]):
                    worksheet.write(count, 8, split_line[7], xlsx_format)
                else:
                    worksheet.write(count, 8, split_line[7])
                # Filename
                filename = " ".join(split_line[8:])
                if pngpattern.search(filename):
                    worksheet.write(count, 9, filename, xlsx_format)
                else:
                    worksheet.write(count, 9, filename)
            line = f_obj.readline()
            count += 1

if __name__ == '__main__':
    main()
