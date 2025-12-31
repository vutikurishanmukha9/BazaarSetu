import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { ArrowLeft, TrendingUp, TrendingDown } from 'lucide-react';
import { fetchPriceTrend } from '../services/api';
import { useLanguage } from '../context/LanguageContext';

const PriceTrend = () => {
    const { commodityId } = useParams();
    const navigate = useNavigate();
    const { t } = useLanguage();
    const [trendData, setTrendData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        loadTrend();
    }, [commodityId]);

    const loadTrend = async () => {
        try {
            setLoading(true);
            const data = await fetchPriceTrend(commodityId);
            setTrendData(data);
        } catch (err) {
            setError('Failed to load trend data');
        } finally {
            setLoading(false);
        }
    };

    if (loading) return <div className="loading">{t('loading')}</div>;
    if (error) return <div className="error">{error}</div>;
    if (!trendData) return <div className="error">{t('no_data')}</div>;

    const chartData = trendData.prices?.map(p => ({
        date: new Date(p.date).toLocaleDateString('en-IN', { day: '2-digit', month: 'short' }),
        min: p.min_price,
        max: p.max_price,
        modal: p.modal_price
    })) || [];

    return (
        <div className="trend-page">
            <div className="container">
                <div className="trend-header">
                    <button className="back-btn" onClick={() => navigate(-1)}>
                        <ArrowLeft size={20} />
                        Back
                    </button>
                    <h1>{trendData.commodity_name} - {t('price_trend')}</h1>
                </div>

                <div className="trend-stats">
                    <div className="stat-card">
                        <span className="stat-label">{t('min_price')}</span>
                        <span className="stat-value">₹{trendData.min_price}</span>
                    </div>
                    <div className="stat-card">
                        <span className="stat-label">{t('modal_price')}</span>
                        <span className="stat-value highlight">₹{trendData.avg_price?.toFixed(0)}</span>
                    </div>
                    <div className="stat-card">
                        <span className="stat-label">{t('max_price')}</span>
                        <span className="stat-value">₹{trendData.max_price}</span>
                    </div>
                    <div className="stat-card">
                        <span className="stat-label">Change</span>
                        <span className={`stat-value ${trendData.change_percent > 0 ? 'up' : 'down'}`}>
                            {trendData.change_percent > 0 ? <TrendingUp size={16} /> : <TrendingDown size={16} />}
                            {Math.abs(trendData.change_percent || 0).toFixed(1)}%
                        </span>
                    </div>
                </div>

                <div className="chart-container">
                    <h3>{t('last_30_days')}</h3>
                    <ResponsiveContainer width="100%" height={400}>
                        <LineChart data={chartData}>
                            <CartesianGrid strokeDasharray="3 3" stroke="var(--border)" />
                            <XAxis dataKey="date" stroke="var(--text-secondary)" />
                            <YAxis stroke="var(--text-secondary)" />
                            <Tooltip
                                contentStyle={{
                                    background: 'var(--surface)',
                                    border: '1px solid var(--border)',
                                    borderRadius: '8px'
                                }}
                            />
                            <Legend />
                            <Line type="monotone" dataKey="min" stroke="#f44336" name="Min" strokeWidth={2} dot={false} />
                            <Line type="monotone" dataKey="modal" stroke="#4caf50" name="Modal" strokeWidth={3} dot={false} />
                            <Line type="monotone" dataKey="max" stroke="#2196f3" name="Max" strokeWidth={2} dot={false} />
                        </LineChart>
                    </ResponsiveContainer>
                </div>
            </div>
        </div>
    );
};

export default PriceTrend;
