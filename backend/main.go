package main

import (
	"context"
	"fmt"
	"log"
	"zeotap-backend/clickhouse"
	"zeotap-backend/file"
)

func main() {
	// STEP 1: Connect to ClickHouse
	conn, err := clickhouse.ConnectClickHouse("localhost:9000", "default", "", "default", "")
	if err != nil {
		log.Fatalf("Connection failed: %v", err)
	}
	fmt.Println("✅ Connected to ClickHouse")

	// STEP 2: Read CSV File
	records, err := file.ReadCSV("sample.csv") // put sample.csv in the same folder
	if err != nil {
		log.Fatalf("CSV read failed: %v", err)
	}
	fmt.Printf("📄 Read %d rows from CSV\n", len(records))

	// STEP 3: Insert to ClickHouse
	// Example assumes the first row is headers
	if len(records) > 1 {
		batch, err := conn.PrepareBatch(context.Background(), "INSERT INTO your_table (col1, col2) VALUES")
		if err != nil {
			log.Fatalf("Batch prepare error: %v", err)
		}
		for _, row := range records[1:] {
			// Make sure to match your schema with the row data
			batch.Append(row[0], row[1]) // Adjust according to your CSV columns
		}
		if err := batch.Send(); err != nil {
			log.Fatalf("Batch send error: %v", err)
		}
		fmt.Printf("✅ Inserted %d records into ClickHouse\n", len(records)-1)
	}
}
