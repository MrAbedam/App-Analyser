

# 📱 App Analyser

A distributed data pipeline system for crawling, analyzing, and visualizing Google Play Store application statistics and reviews. This project implements a microservices architecture to track app metrics, ratings, and user reviews over time.

## 🎯 Project Overview

App Analyser is a comprehensive analytics platform that:
- Crawls Google Play Store for app statistics hourly
- Collects and processes user reviews (1000 latest per app)
- Stores historical data for trend analysis
- Provides business intelligence dashboards via Metabase
- Uses distributed message queues for scalable data processing

## 🏗️ System Architecture

```
┌─────────────────┐     ┌──────────────┐     ┌─────────────┐
│  App List API   │────▶│   Crawler    │────▶│   Redis    │
│   (FastAPI)     │     │   (Python)   │     │             │
└─────────────────┘     └──────────────┘     └─────────────┘
                                                      │
                                                      ▼
                                              ┌─────────────┐
                                              │  PostgreSQL │
                                              │   Database  │
                                              └─────────────┘
                                                      │
                                                      ▼
                                              ┌─────────────┐
                                              │  Metabase   │
                                              │     BI      │
                                              └─────────────┘
```

## ✨ Features

### 1. Application Management API
- **Create**: Add new applications to the monitoring list
- **Read**: Retrieve all registered applications
- **Update**: Modify application information
- **Delete**: Deactivate applications from monitoring

### 2. Play Store Crawler
Extracts hourly metrics for each application:
- Minimum installs (`minInstalls`)
- Score rating (`score`)
- Number of ratings (`ratings`)
- Review count (`reviews`)
- Last update date (`updated`)
- Current version (`version`)
- Ad support status (`adSupported`)

### 3. Review Collection
Gathers the latest 1000 reviews with:
- Review ID (`reviewId`)
- Timestamp (`at`)
- Username (`userName`)
- Thumbs up count (`thumbsUpCount`)
- Score rating (`score`)
- Review content (`content`)

### 4. Data Analytics Dashboard
Metabase visualizations for:
- Score trend analysis by category
- Installation count trends
- Most impactful reviews per application
- Custom business intelligence queries

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| **API Framework** | FastAPI |
| **Message Queue** | Redis  |
| **Database** | PostgreSQL |
| **Crawler** | Python (google-play-scraper) |
| **BI Tool** | Metabase |
| **Containerization** | Docker & Docker Compose |
| **Testing** | pytest, unittest |
| **Documentation** | Swagger/OpenAPI |

## 📦 Installation

### Prerequisites
- Docker & Docker Compose
- Python 3.8+
- PostgreSQL 12+
- Redis 6+

## 📁 Project Structure

```
App-Analyser/
├── api/                    # FastAPI application
│   ├── models/            # Database models
│   ├── routes/            # API endpoints
│   ├── schemas/           # Pydantic schemas
│   └── tests/             # API tests
├── crawler/               # Play Store crawler
│   ├── scraper.py         # Main scraper logic
│   ├── queue_producer.py  # Message queue producer
│   └── tests/             # Crawler tests
├── consumer/              # Data consumer service
│   ├── consumer.py        # Queue consumer
│   ├── db_handler.py      # Database operations
│   └── tests/             # Consumer tests
├── metabase/              # Metabase configuration
├── docker/                # Docker configurations
├── scripts/               # Setup and utility scripts
├── docker-compose.yml     # Docker orchestration
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## 🔧 Configuration

### Environment Variables

```bash
# Database
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=app_analyser
POSTGRES_USER=postgres
POSTGRES_PASSWORD=yourpassword

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=yourpassword

# API
API_HOST=0.0.0.0
API_PORT=8000
API_WORKERS=4

# Crawler
CRAWL_INTERVAL_HOURS=1
MAX_REVIEWS_PER_APP=1000
```

## 📊 Monitored Applications

### Default App Categories
- **Messengers**: Telegram, WhatsApp
- **Operators**: Myirancell, Mymci, MyRightel
- **Financial**: Seke, 724, Top
- **Video Streaming**: Namava, Telewebion, Tamashakhane
- **Word Games**: Fandogh, Amirza, Hadsekalamat
- **Social Networks**: Instagram, Facebook, TikTok

*You can add more categories and applications via the API*


## 🗺️ Roadmap

- [ ] Add Kafka support for enterprise scalability
- [ ] Implement sentiment analysis for reviews
- [ ] Add real-time alerting system
- [ ] Expand to other app stores (Apple App Store, etc.)
- [ ] Machine learning for app success prediction
- [ ] API rate limiting and authentication
- [ ] Multi-language support for reviews

---

**Note**: This project is for educational purposes. Ensure compliance with Google Play Store's Terms of Service when using this tool.

[سند پروژه سحابی_نو پایتون.pdf](https://github.com/user-attachments/files/19039940/_.pdf)
