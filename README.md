# Document Search documents from a cloud storage using Flask & Elasticsearch

## Overview

This project is a Flask-based web application that connects to Google Drive, extracts content from `.txt`, `.csv`, `.pdf`, and `.png` files, and indexes them using Elasticsearch. It allows you to search the contents of documents and returns matching filenames.

---

## Features

- Authentication with Google Drive
- Downloads documents (.txt, .csv, .pdf, .png)
- Extracts text content using PDFMiner, Tesseract.
- Indexes text content in Elasticsearch
- REST API to:
  - `/search?q=term` – Search files from content
- Sync logic: removes files from index that no longer exist in Drive

---

## Folder Structure

```
project_root/
├── app/
│   ├── app.py                  
│   ├── content_extractor.py   
│   ├── drive_connector.py     
│   ├── es_indexer.py          
│   ├── extract_and_index.py   
│   └── sync_drive_to_es.py    
├── files/                     
├── credentials.json           
├── token.pickle               
├── requirements.txt           
└── README.md   
```

---

## Setup Instructions

### 1. UnZip Folder search_document_cloud_storage

### 2. Install Dependencies

```bash
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

### 3. Configure Google API

- Go to Google Developers Console
- Create OAuth client ID
- Download `credentials.json` and place it in the project root

### 4. Start Elasticsearch

Ensure Elasticsearch is running locally with basic auth (user: `elastic`, password: `<your-password>`).

### 5. Run the Application

```bash
python app/app.py
```

Access: `http://127.0.0.1:5000`

### 6. Sync Drive & Index

```bash
python app/sync_drive_to_es.py
```

---

## API Endpoints

### 1. Search With Term

```bash
curl "http://127.0.0.1:5000/search?q=Cloud"
```

---

## Author

Muhammad Murtaza