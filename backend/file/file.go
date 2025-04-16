// file/csv.go
package file

import (
	"encoding/csv"
	"os"
)

func ReadCSV(filePath string) ([][]string, error) {
	f, err := os.Open(filePath)
	if err != nil {
		return nil, err
	}
	defer f.Close()

	reader := csv.NewReader(f)
	return reader.ReadAll()
}