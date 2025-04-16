package clickhouse

import (
	"context"
	"time"

	"github.com/ClickHouse/clickhouse-go/v2"
)

func ConnectClickHouse(host, username, password, database, jwt string) (clickhouse.Conn, error) {
	conn, err := clickhouse.Open(&clickhouse.Options{
		Addr: []string{host}, // e.g. "localhost:9000"
		Auth: clickhouse.Auth{
			Database: database,
			Username: username,
			Password: password,
		},
		DialTimeout:  5 * time.Second,
		Compression: &clickhouse.Compression{Method: clickhouse.CompressionLZ4},
	})

	if err != nil {
		return nil, err
	}

	// Optional: test the connection
	if err := conn.Ping(context.Background()); err != nil {
		return nil, err
	}

	return conn, nil
}