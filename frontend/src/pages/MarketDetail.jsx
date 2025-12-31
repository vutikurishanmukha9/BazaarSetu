import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { ArrowLeft, MapPin, Phone } from 'lucide-react';
import { fetchMarketDetails, fetchTodayPrices } from '../services/api';
import PriceCard from '../components/PriceCard';
import { useLanguage } from '../context/LanguageContext';

const MarketDetail = () => {
    const { marketId } = useParams();
    const navigate = useNavigate();
    const { t } = useLanguage();
    const [market, setMarket] = useState(null);
    const [prices, setPrices] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        loadData();
    }, [marketId]);

    const loadData = async () => {
        try {
            setLoading(true);
            const [marketData, pricesData] = await Promise.all([
                fetchMarketDetails(marketId),
                fetchTodayPrices(null, marketId)
            ]);
            setMarket(marketData);
            setPrices(pricesData);
        } catch (err) {
            console.error('Error loading market:', err);
        } finally {
            setLoading(false);
        }
    };

    if (loading) return <div className="loading">{t('loading')}</div>;
    if (!market) return <div className="error">{t('no_data')}</div>;

    return (
        <div className="market-detail-page">
            <div className="container">
                <div className="market-header">
                    <button className="back-btn" onClick={() => navigate(-1)}>
                        <ArrowLeft size={20} />
                        Back
                    </button>

                    <div className="market-info-card">
                        <h1>{market.name}</h1>
                        <div className="market-meta">
                            <span><MapPin size={16} /> {market.district}, {market.state_name}</span>
                        </div>
                    </div>
                </div>

                <h2>Today's Prices ({prices.length} items)</h2>

                {prices.length > 0 ? (
                    <div className="price-grid">
                        {prices.map((item) => (
                            <PriceCard key={`${item.commodity_name}-${item.market_name}`} item={item} />
                        ))}
                    </div>
                ) : (
                    <div className="no-prices">No prices available for this market today.</div>
                )}
            </div>
        </div>
    );
};

export default MarketDetail;
