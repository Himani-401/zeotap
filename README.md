# Bidirectional ClickHouse & Flat File Data Ingestion Tool

This is a web-based application that facilitates bidirectional data ingestion between ClickHouse and flat files (CSV). The tool allows users to easily ingest data from ClickHouse to flat files and vice versa, while handling JWT token-based authentication for secure access to ClickHouse. Users can select columns for ingestion, view progress, and receive completion reports.

## Table of Contents
1. [Installation](#installation)
2. [Configuration](#configuration)
3. [Usage](#usage)
4. [API Endpoints](#api-endpoints)
5. [Testing](#testing)
6. [Contributing](#contributing)
7. [License](#license)


## Installation

### Prerequisites

- Python 3.7 or higher
- Node.js and npm
- ClickHouse instance (local or cloud-based)

### Backend Setup (Python with Flask)

1. Clone the repository:
   ```bash
   git clone https://github.com/bidirectional-ingestion-tool.git
   cd bidirectional-ingestion-tool/backend

start the backend :
run the backned by running command flask run 
start teh frontend :
run the frontend by npm i and npm run dev

