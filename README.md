# BazaarSetu

> **Connecting You to Real Bazaar Prices** - Live vegetable & poultry market prices from AP & Telangana

[![Frontend](https://img.shields.io/badge/Frontend-React%20%2B%20Vite-61DAFB?style=flat&logo=react)](./frontend)
[![Backend](https://img.shields.io/badge/Backend-FastAPI-009688?style=flat&logo=fastapi)](./backend)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](./LICENSE)

## What is BazaarSetu?

BazaarSetu is a modern web application designed to bridge the gap between farmers, consumers, and local markets by providing **real-time mandi prices**. It empowers users with transparent pricing for vegetables and poultry, helping them make informed buying decisions.

### Key Features

- **Live Market Prices** - Real-time data from 20+ mandis in AP & Telangana
- **Multiple Categories** - Filter by Vegetables, Poultry (Chicken/Eggs), Fruits, etc.
- **Premium UI/UX** - Beautiful glassmorphism design with Dark Mode support
- **Multi-language** - Full support for **English**, **Telugu (తెలుగు)**, and **Hindi (हिंदी)**
- **Advanced Filtering** - Sort by Price, A-Z, or identify the **Biggest Price Drops**
- **Price Trends** - Analyze price history with interactive charts (7/30 days)
- **Mobile Optimized** - Responsive grid layout that works perfectly on all devices

## Tech Stack

| Component | Technology | Description |
|-----------|------------|-------------|
| **Frontend** | React + Vite | Fast, responsive web interface |
| **Styling** | CSS Variables | Custom glassmorphism design system |
| **Backend** | FastAPI | High-performance Python API |
| **Database** | SQLite (Dev) | Local development database (moving to PostgreSQL) |
| **Data Source** | Data.gov.in | Government Open Data API |

## Getting Started

### Prerequisites
- Node.js (v16+)
- Python (v3.9+)

### 1. Backend Setup
```bash
cd backend
python -m venv venv
# Windows
.\venv\Scripts\activate
# Install dependencies
pip install -r requirements.txt
# Run server
uvicorn app.main:app --reload
```

### 2. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```
Visit http://localhost:5173 to view the app!

## Roadmap & Future Plans

The application is currently in **Phase 2 (Beta)**. Here is the plan for future development:

### **Phase 3: Robustness & Scale (Next Steps)**
- [ ] **PostgreSQL Migration**: Move from SQLite to Production-grade PostgreSQL
- [ ] **Authentication**: User login/signup to save favorite markets
- [ ] **Price Alerts**: Email/WhatsApp notifications when prices drop
- [ ] **Vendor Portal**: Allow local vendors to update their own prices

### **Phase 4: AI & Intelligence**
- [ ] **Price Prediction**: AI model to forecast prices based on historical trends & weather
- [ ] **Recipe Suggestions**: Suggest recipes based on vegetables with lowest prices
- [ ] **Voice Search**: "What is the price of Tomato in Guntur?"

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## License
MIT License - see [LICENSE](./LICENSE)
