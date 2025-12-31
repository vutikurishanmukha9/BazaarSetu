# BazaarSetu

> **Connecting You to Real Bazaar Prices** - Live vegetable market prices from AP & Telangana

[![Backend](https://img.shields.io/badge/Backend-FastAPI-009688?style=flat&logo=fastapi)](./backend)
[![Mobile](https://img.shields.io/badge/Mobile-Flutter-02569B?style=flat&logo=flutter)](./mobile)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](./LICENSE)

## What is BazaarSetu?

BazaarSetu is a mobile-first application that brings **live vegetable prices** directly to your phone. No need to visit the market just to check prices!

### Features

- **Live Prices** - Real-time vegetable prices from AP & Telangana markets
- **Price Trends** - Track price history (daily, weekly, monthly)
- **Price Alerts** - Get notified when prices drop below your threshold
- **Market Comparison** - Compare prices across different mandis
- **Vendor Mapping** - Find nearby vegetable vendors
- **Multi-language** - Available in English, Telugu, and Hindi

## Tech Stack

| Component | Technology |
|-----------|------------|
| Mobile App | Flutter |
| Backend | FastAPI (Python) |
| Database | PostgreSQL |
| Hosting | Render |

## Project Structure

```
BazaarSetu/
├── backend/         # FastAPI backend
├── mobile/          # Flutter app
└── README.md
```

## Getting Started

### Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Mobile App

```bash
cd mobile
flutter pub get
flutter run
```

## Data Sources

- [data.gov.in](https://data.gov.in) - Government Catalog API for mandi prices
- [eNAM (APISetu)](https://apisetu.gov.in) - Electronic National Agriculture Market
- Web scraping for additional vendor data

## License

MIT License - see [LICENSE](./LICENSE)
