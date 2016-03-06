package main

import (
	"bufio"
	"flag"
	"fmt"
	"os"
	"path/filepath"
	"regexp"
	"time"

	"github.com/tealeg/xlsx"
)

func main() {
	flag.Args()
	flag.Parse()

	args := flag.Args()
	if len(args) < 1 {
		fmt.Println("daily <directory>")
		os.Exit(1)
	}

	dirPath := args[0]
	files := GlobLog(dirPath)
	for _, f := range files {
		fmt.Println(f)
	}
	today := time.Now().Format("20060102")
	xlsxFileName := today + ".xlsx"

	file := xlsx.NewFile()
	for _, f := range files {
		_, sheetName := filepath.Split(f)
		sheet, err := file.AddSheet(sheetName)
		if err != nil {
			fmt.Printf(err.Error())
		}
		row := sheet.AddRow()
		//cell := row.AddCell()
		cell := row.AddCell()
		cell.Value = sheetName
		sheet.AddRow()
		fp, err := os.Open(f)
		if err != nil {
			panic(err)
		}
		defer fp.Close()
		scanner := bufio.NewScanner(fp)
		i := 2
		sheet.AddRow()
		for scanner.Scan() {
			line := scanner.Text()
			rep := regexp.MustCompile(`\s+`)
			splitLine := rep.Split(line, -1)
			if splitLine[5] == "Accepted" {
				//j := 0
				//for _, text := range splitLine {
				//	fmt.Println(text)
				cell = AddCell(sheet, i, 0)
				cell.Value = splitLine[0]
				cell = AddCell(sheet, i, 1)
				cell.Value = splitLine[1]
				cell = AddCell(sheet, i, 3)
				cell.Value = splitLine[3]
				cell = AddCell(sheet, i, 4)
				cell.Value = splitLine[8]
				cell = AddCell(sheet, i, 5)
				cell.Value = splitLine[10]
				//j++
				//}
				i++
			}
		}
		if err := scanner.Err(); err != nil {
			panic(err)
		}
	}
	err := file.Save(xlsxFileName)
	if err != nil {
		fmt.Printf(err.Error())
	}
}

//AddCell sheet
func AddCell(sheet *xlsx.Sheet, row, col int) *xlsx.Cell {
	// hhh
	for row >= len(sheet.Rows) {
		sheet.AddRow()
	}
	for col >= len(sheet.Rows[row].Cells) {
		sheet.Rows[row].AddCell()
	}
	return sheet.Cell(row, col)
}

//GlobLog path
func GlobLog(path string) []string {
	files, _ := filepath.Glob(path)
	for _, f := range files {
		fmt.Println(f)
	}
	return files
}
