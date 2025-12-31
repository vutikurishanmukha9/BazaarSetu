import 'package:flutter/material.dart';
import '../models/models.dart';
import '../services/api_service.dart';

/// State provider for price data
class PriceProvider extends ChangeNotifier {
  List<PriceWithDetails> _todayPrices = [];
  List<Commodity> _commodities = [];
  List<Market> _markets = [];
  PriceTrend? _currentTrend;
  
  bool _isLoading = false;
  String? _error;
  
  // Filters
  int? _selectedStateId;
  int? _selectedCommodityId;
  int? _selectedMarketId;
  String _searchQuery = '';

  // Getters
  List<PriceWithDetails> get todayPrices => _todayPrices;
  List<Commodity> get commodities => _commodities;
  List<Market> get markets => _markets;
  PriceTrend? get currentTrend => _currentTrend;
  bool get isLoading => _isLoading;
  String? get error => _error;
  int? get selectedStateId => _selectedStateId;
  int? get selectedCommodityId => _selectedCommodityId;
  int? get selectedMarketId => _selectedMarketId;
  String get searchQuery => _searchQuery;

  /// Filtered prices based on search query
  List<PriceWithDetails> get filteredPrices {
    if (_searchQuery.isEmpty) return _todayPrices;
    
    final query = _searchQuery.toLowerCase();
    return _todayPrices.where((price) {
      return price.commodityName.toLowerCase().contains(query) ||
             (price.commodityNameTelugu?.toLowerCase().contains(query) ?? false) ||
             (price.commodityNameHindi?.toLowerCase().contains(query) ?? false) ||
             price.marketName.toLowerCase().contains(query);
    }).toList();
  }

  /// Load today's prices
  Future<void> loadTodayPrices() async {
    _isLoading = true;
    _error = null;
    notifyListeners();

    try {
      _todayPrices = await apiService.getTodayPrices(
        stateId: _selectedStateId,
        commodityId: _selectedCommodityId,
        marketId: _selectedMarketId,
      );
    } catch (e) {
      _error = e.toString();
      // Load demo data for development
      _todayPrices = _getDemoPrices();
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }

  /// Load commodities
  Future<void> loadCommodities() async {
    try {
      _commodities = await apiService.getCommodities();
    } catch (e) {
      // Demo data
      _commodities = _getDemoCommodities();
    }
    notifyListeners();
  }

  /// Load markets
  Future<void> loadMarkets({int? stateId}) async {
    try {
      _markets = await apiService.getMarkets(stateId: stateId);
    } catch (e) {
      _markets = [];
    }
    notifyListeners();
  }

  /// Load price trend
  Future<void> loadPriceTrend(int commodityId, {int? marketId}) async {
    _isLoading = true;
    notifyListeners();

    try {
      _currentTrend = await apiService.getPriceTrend(commodityId, marketId: marketId);
    } catch (e) {
      _error = e.toString();
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }

  /// Set search query
  void setSearchQuery(String query) {
    _searchQuery = query;
    notifyListeners();
  }

  /// Set state filter
  void setStateFilter(int? stateId) {
    _selectedStateId = stateId;
    loadTodayPrices();
  }

  /// Set commodity filter
  void setCommodityFilter(int? commodityId) {
    _selectedCommodityId = commodityId;
    loadTodayPrices();
  }

  /// Set market filter
  void setMarketFilter(int? marketId) {
    _selectedMarketId = marketId;
    loadTodayPrices();
  }

  /// Clear all filters
  void clearFilters() {
    _selectedStateId = null;
    _selectedCommodityId = null;
    _selectedMarketId = null;
    _searchQuery = '';
    loadTodayPrices();
  }

  /// Demo data for development
  List<PriceWithDetails> _getDemoPrices() {
    return [
      PriceWithDetails(
        commodityName: 'Tomato',
        commodityNameTelugu: 'టమాటా',
        commodityNameHindi: 'टमाटर',
        marketName: 'Hyderabad',
        district: 'Hyderabad',
        stateName: 'Telangana',
        minPrice: 25,
        maxPrice: 35,
        modalPrice: 30,
        priceDate: DateTime.now(),
        priceChange: -5.2,
      ),
      PriceWithDetails(
        commodityName: 'Onion',
        commodityNameTelugu: 'ఉల్లిపాయ',
        commodityNameHindi: 'प्याज',
        marketName: 'Vijayawada',
        district: 'Krishna',
        stateName: 'Andhra Pradesh',
        minPrice: 35,
        maxPrice: 45,
        modalPrice: 40,
        priceDate: DateTime.now(),
        priceChange: 2.5,
      ),
      PriceWithDetails(
        commodityName: 'Potato',
        commodityNameTelugu: 'బంగాళాదుంప',
        commodityNameHindi: 'आलू',
        marketName: 'Warangal',
        district: 'Warangal',
        stateName: 'Telangana',
        minPrice: 20,
        maxPrice: 28,
        modalPrice: 24,
        priceDate: DateTime.now(),
        priceChange: 0,
      ),
      PriceWithDetails(
        commodityName: 'Green Chilli',
        commodityNameTelugu: 'పచ్చిమిర్చి',
        commodityNameHindi: 'हरी मिर्च',
        marketName: 'Guntur',
        district: 'Guntur',
        stateName: 'Andhra Pradesh',
        minPrice: 60,
        maxPrice: 80,
        modalPrice: 70,
        priceDate: DateTime.now(),
        priceChange: 10.5,
      ),
      PriceWithDetails(
        commodityName: 'Brinjal',
        commodityNameTelugu: 'వంకాయ',
        commodityNameHindi: 'बैंगन',
        marketName: 'Karimnagar',
        district: 'Karimnagar',
        stateName: 'Telangana',
        minPrice: 30,
        maxPrice: 40,
        modalPrice: 35,
        priceDate: DateTime.now(),
        priceChange: -3.0,
      ),
    ];
  }

  List<Commodity> _getDemoCommodities() {
    return [
      Commodity(id: 1, name: 'Tomato', nameTelugu: 'టమాటా', nameHindi: 'टमाटर'),
      Commodity(id: 2, name: 'Onion', nameTelugu: 'ఉల్లిపాయ', nameHindi: 'प्याज'),
      Commodity(id: 3, name: 'Potato', nameTelugu: 'బంగాళాదుంప', nameHindi: 'आलू'),
      Commodity(id: 4, name: 'Green Chilli', nameTelugu: 'పచ్చిమిర్చి', nameHindi: 'हरी मिर्च'),
      Commodity(id: 5, name: 'Brinjal', nameTelugu: 'వంకాయ', nameHindi: 'बैंगन'),
    ];
  }
}
