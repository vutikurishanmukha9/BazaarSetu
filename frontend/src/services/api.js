import axios from 'axios';

// Backend URL
const BASE_URL = 'http://localhost:8000/api/v1';

const api = axios.create({
    baseURL: BASE_URL,
    timeout: 30000,
});

export const fetchStates = async () => {
    try {
        const response = await api.get('/states');
        return response.data;
    } catch (error) {
        console.error('Error fetching states:', error);
        throw error;
    }
};

export const fetchTodayPrices = async (filters = {}) => {
    try {
        const params = {};
        if (filters.stateId) params.state_id = filters.stateId;
        if (filters.marketId) params.market_id = filters.marketId;
        if (filters.category) params.category = filters.category;
        if (filters.sortBy) params.sort_by = filters.sortBy;
        if (filters.sortOrder) params.sort_order = filters.sortOrder;
        if (filters.dateFrom) params.date_from = filters.dateFrom;
        if (filters.dateTo) params.date_to = filters.dateTo;

        const response = await api.get('/prices/today', { params });
        return response.data;
    } catch (error) {
        console.error('Error fetching prices:', error);
        throw error;
    }
};

export const fetchMarkets = async () => {
    try {
        const response = await api.get('/markets/');
        return response.data;
    } catch (error) {
        console.error('Error fetching markets:', error);
        throw error;
    }
};

export const fetchPriceTrend = async (commodityId, marketId = null, days = 30) => {
    try {
        const params = { days };
        if (marketId) params.market_id = marketId;

        const response = await api.get(`/prices/trend/${commodityId}`, { params });
        return response.data;
    } catch (error) {
        console.error('Error fetching trend:', error);
        throw error;
    }
};

export const fetchMarketDetails = async (marketId) => {
    try {
        const response = await api.get(`/markets/${marketId}`);
        return response.data;
    } catch (error) {
        console.error('Error fetching market details:', error);
        throw error;
    }
};

export default api;
