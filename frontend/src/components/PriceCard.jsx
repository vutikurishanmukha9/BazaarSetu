import React from 'react';
import { useNavigate } from 'react-router-dom';
import { MapPin, TrendingUp, TrendingDown } from 'lucide-react';
import { useLanguage } from '../context/LanguageContext';

// Get first letter(s) for icon
const getIconText = (name) => {
    const n = name.toLowerCase();
    if (n.includes('chicken')) return 'CK';
    if (n.includes('egg')) return 'EG';
    if (n.includes('tomato')) return 'TM';
    if (n.includes('onion')) return 'ON';
    if (n.includes('potato')) return 'PT';
    if (n.includes('garlic')) return 'GL';
    if (n.includes('ginger')) return 'GI';
    if (n.includes('carrot')) return 'CR';
    if (n.includes('cabbage')) return 'CB';
    if (n.includes('cauliflower')) return 'CF';
    if (n.includes('brinjal')) return 'BJ';
    if (n.includes('beans')) return 'BN';
    if (n.includes('gourd')) return 'GD';
    if (n.includes('spinach')) return 'SP';
    if (n.includes('coriander')) return 'CO';
    if (n.includes('methi')) return 'MT';
    if (n.includes('lemon')) return 'LM';
    if (n.includes('banana')) return 'BA';
    if (n.includes('coconut')) return 'CN';
    if (n.includes('cucumber')) return 'CU';
    if (n.includes('drumstick')) return 'DS';
    if (n.includes('lady finger') || n.includes('okra')) return 'LF';
    if (n.includes('chilli')) return 'CH';
    if (n.includes('pumpkin')) return 'PK';
    if (n.includes('curry')) return 'CL';
    if (n.includes('mint')) return 'MN';
    return name.substring(0, 2).toUpperCase();
};

// Get category from item
const getCategory = (name) => {
    const n = name.toLowerCase();
    if (n.includes('chicken') || n.includes('egg')) return 'poultry';
    return 'vegetable';
};

const PriceCard = ({ item }) => {
    const navigate = useNavigate();
    const { language, t } = useLanguage();

    // Get commodity name based on selected language
    const getCommodityName = () => {
        if (language === 'te' && item.commodity_name_telugu) {
            return item.commodity_name_telugu;
        }
        if (language === 'hi' && item.commodity_name_hindi) {
            return item.commodity_name_hindi;
        }
        return item.commodity_name;
    };

    const trendPercent = item.price_change_percent || 0;
    const trendDirection = trendPercent > 0 ? 'up' : trendPercent < 0 ? 'down' : null;
    const category = item.category || getCategory(item.commodity_name);

    const handleClick = () => {
        if (item.commodity_id) {
            navigate(`/trend/${item.commodity_id}`);
        }
    };

    return (
        <div className="price-card" onClick={handleClick}>
            {category === 'poultry' && (
                <span className="category-badge poultry">{t('poultry')}</span>
            )}

            <div className="card-content">
                <div className="card-header">
                    <div className="commodity-icon">
                        <span className="icon-text">{getIconText(item.commodity_name)}</span>
                    </div>
                    <div className="details">
                        <div className="commodity-name">{getCommodityName()}</div>
                        <div className="market-info">
                            <MapPin />
                            <span>{item.market_name}, {item.district}</span>
                        </div>
                    </div>
                </div>

                <div className="price-info">
                    <div className="price">
                        <span className="currency">₹</span>
                        <span className="amount">{Math.round(item.modal_price)}</span>
                        <span className="unit">/{item.unit || 'kg'}</span>
                    </div>

                    {trendDirection && (
                        <div className={`trend ${trendDirection}`}>
                            {trendDirection === 'up' ? <TrendingUp /> : <TrendingDown />}
                            <span>{Math.abs(trendPercent).toFixed(1)}%</span>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};

export default PriceCard;
