import React, { useEffect, useState } from 'react';
import { fetchTodayPrices, fetchStates } from '../services/api';
import PriceCard from '../components/PriceCard';
import ThemeToggle from '../components/ThemeToggle';
import LanguageSelector from '../components/LanguageSelector';
import { useLanguage } from '../context/LanguageContext';
import { Search, MapPin } from 'lucide-react';

const HomeScreen = () => {
    const { t, language } = useLanguage();
    const [prices, setPrices] = useState([]);
    const [states, setStates] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [searchQuery, setSearchQuery] = useState('');

    // Filter states
    const [selectedState, setSelectedState] = useState(null);
    const [selectedCategory, setSelectedCategory] = useState('');
    const [selectedSort, setSelectedSort] = useState('name-asc');

    // Get state name based on language
    const getStateName = (state) => {
        if (language === 'te' && state.name_telugu) return state.name_telugu;
        if (language === 'hi' && state.name_hindi) return state.name_hindi;
        return state.name;
    };

    useEffect(() => {
        loadStates();
    }, []);

    useEffect(() => {
        loadData();
    }, [selectedState, selectedCategory, selectedSort]);

    const loadStates = async () => {
        try {
            const data = await fetchStates();
            setStates(data);
        } catch (err) {
            console.error('Failed to load states', err);
        }
    };

    const loadData = async () => {
        try {
            setLoading(true);
            setError(null);

            const [sortBy, sortOrder] = selectedSort.split('-');

            const data = await fetchTodayPrices({
                stateId: selectedState,
                category: selectedCategory || null,
                sortBy: sortBy,
                sortOrder: sortOrder
            });
            setPrices(data);
        } catch (err) {
            console.error('Fetch error:', err);
            setError(err.message || t('failed_to_load'));
        } finally {
            setLoading(false);
        }
    };

    const filteredPrices = prices.filter(p =>
        p.commodity_name.toLowerCase().includes(searchQuery.toLowerCase()) ||
        p.market_name.toLowerCase().includes(searchQuery.toLowerCase())
    );

    return (
        <div className="home-screen">
            {/* Hero Section */}
            <div className="hero">
                <div className="container">
                    <div className="hero-content">
                        <h1>{t('app_name')}</h1>
                        <p className="tagline">{t('tagline')}</p>

                        <div className="hero-controls">
                            <LanguageSelector />
                            <ThemeToggle />
                        </div>

                        <div className="search-bar">
                            <Search className="search-icon" size={20} />
                            <input
                                type="text"
                                placeholder={t('search_placeholder')}
                                value={searchQuery}
                                onChange={(e) => setSearchQuery(e.target.value)}
                            />
                            <button className="search-btn">{t('search')}</button>
                        </div>

                        {/* State Filters - Inside Hero */}
                        <div className="state-filters">
                            <div
                                className={`state-chip ${selectedState === null ? 'active' : ''}`}
                                onClick={() => setSelectedState(null)}
                            >
                                {t('all_states')}
                            </div>
                            {states.map(state => (
                                <div
                                    key={state.id}
                                    className={`state-chip ${selectedState === state.id ? 'active' : ''}`}
                                    onClick={() => setSelectedState(state.id)}
                                >
                                    {getStateName(state)}
                                </div>
                            ))}
                        </div>
                    </div>
                </div>
            </div>

            {/* Content */}
            <div className="container content-area">
                {/* Category And Sort Panel */}
                <div className="filter-panel">
                    <h3 className="filter-panel-title">{t('category_and_sort')}</h3>

                    <div className="filter-row">
                        <div className="filter-column">
                            <label className="filter-column-label">{t('category')}</label>
                            <select
                                className="filter-select"
                                value={selectedCategory}
                                onChange={(e) => setSelectedCategory(e.target.value)}
                            >
                                <option value="">{t('all')}</option>
                                <option value="vegetable">{t('vegetables')}</option>
                                <option value="poultry">{t('poultry')}</option>
                                <option value="leafy">{t('leafy_greens')}</option>
                                <option value="fruit">{t('fruits')}</option>
                            </select>
                        </div>

                        <div className="filter-column">
                            <label className="filter-column-label">{t('sort')}</label>
                            <select
                                className="filter-select"
                                value={selectedSort}
                                onChange={(e) => setSelectedSort(e.target.value)}
                            >
                                <option value="name-asc">{t('sort_az')}</option>
                                <option value="name-desc">{t('sort_za')}</option>
                                <option value="change-asc">{t('biggest_drops')}</option>
                                <option value="price-desc">{t('price_high_low')}</option>
                                <option value="price-asc">{t('price_low_high')}</option>
                            </select>
                        </div>
                    </div>
                </div>

                {/* Results */}
                {loading ? (
                    <div className="loading">
                        <div className="loading-spinner"></div>
                        <span>{t('loading')}</span>
                    </div>
                ) : error ? (
                    <div className="error">{error}</div>
                ) : filteredPrices.length === 0 ? (
                    <div className="loading">{t('no_data')}</div>
                ) : (
                    <div className="price-grid">
                        {filteredPrices.map((item, index) => (
                            <PriceCard key={`${item.commodity_name}-${item.market_name}-${index}`} item={item} />
                        ))}
                    </div>
                )}
            </div>

            {/* Footer */}
            <footer className="footer">
                <div className="container">
                    <div className="footer-links">
                        <a href="#">{t('footer_about')}</a>
                        <a href="#">{t('footer_data_sources')}</a>
                        <a href="#">{t('footer_contact')}</a>
                        <a href="#">{t('footer_privacy')}</a>
                    </div>
                </div>
            </footer>
        </div>
    );
};

export default HomeScreen;
