import 'dart:convert';
import 'package:http/http.dart' as http;
import '../models/models.dart';

/// API service for communicating with the BazaarSetu backend
class ApiService {
  // TODO: Update this to your deployed backend URL
  static const String baseUrl = 'http://localhost:8000/api/v1';
  
  final http.Client _client;

  ApiService({http.Client? client}) : _client = client ?? http.Client();

  /// Get today's prices with optional filters
  Future<List<PriceWithDetails>> getTodayPrices({
    int? stateId,
    int? commodityId,
    int? marketId,
    int page = 1,
    int pageSize = 50,
  }) async {
    final queryParams = {
      'page': page.toString(),
      'page_size': pageSize.toString(),
      if (stateId != null) 'state_id': stateId.toString(),
      if (commodityId != null) 'commodity_id': commodityId.toString(),
      if (marketId != null) 'market_id': marketId.toString(),
    };

    final uri = Uri.parse('$baseUrl/prices/today').replace(queryParameters: queryParams);
    final response = await _client.get(uri);

    if (response.statusCode == 200) {
      final List<dynamic> data = json.decode(response.body);
      return data.map((e) => PriceWithDetails.fromJson(e)).toList();
    } else {
      throw Exception('Failed to load prices: ${response.statusCode}');
    }
  }

  /// Get price trend for a commodity
  Future<PriceTrend> getPriceTrend(int commodityId, {int? marketId, int days = 30}) async {
    final queryParams = {
      'days': days.toString(),
      if (marketId != null) 'market_id': marketId.toString(),
    };

    final uri = Uri.parse('$baseUrl/prices/trend/$commodityId').replace(queryParameters: queryParams);
    final response = await _client.get(uri);

    if (response.statusCode == 200) {
      return PriceTrend.fromJson(json.decode(response.body));
    } else {
      throw Exception('Failed to load price trend: ${response.statusCode}');
    }
  }

  /// Compare prices across markets for a commodity
  Future<Map<String, dynamic>> comparePrices(int commodityId, {DateTime? date}) async {
    final queryParams = <String, String>{};
    if (date != null) {
      queryParams['price_date'] = date.toIso8601String().split('T')[0];
    }

    final uri = Uri.parse('$baseUrl/prices/compare/$commodityId').replace(queryParameters: queryParams);
    final response = await _client.get(uri);

    if (response.statusCode == 200) {
      return json.decode(response.body);
    } else {
      throw Exception('Failed to compare prices: ${response.statusCode}');
    }
  }

  /// Search commodities
  Future<List<Commodity>> searchCommodities(String query) async {
    final uri = Uri.parse('$baseUrl/prices/search').replace(queryParameters: {'q': query});
    final response = await _client.get(uri);

    if (response.statusCode == 200) {
      final List<dynamic> data = json.decode(response.body);
      return data.map((e) => Commodity.fromJson(e)).toList();
    } else {
      throw Exception('Failed to search commodities: ${response.statusCode}');
    }
  }

  /// Get all commodities
  Future<List<Commodity>> getCommodities({String? category}) async {
    final queryParams = <String, String>{};
    if (category != null) queryParams['category'] = category;

    final uri = Uri.parse('$baseUrl/commodities').replace(queryParameters: queryParams);
    final response = await _client.get(uri);

    if (response.statusCode == 200) {
      final List<dynamic> data = json.decode(response.body);
      return data.map((e) => Commodity.fromJson(e)).toList();
    } else {
      throw Exception('Failed to load commodities: ${response.statusCode}');
    }
  }

  /// Get markets
  Future<List<Market>> getMarkets({int? stateId}) async {
    final queryParams = <String, String>{};
    if (stateId != null) queryParams['state_id'] = stateId.toString();

    final uri = Uri.parse('$baseUrl/markets').replace(queryParameters: queryParams);
    final response = await _client.get(uri);

    if (response.statusCode == 200) {
      final List<dynamic> data = json.decode(response.body);
      return data.map((e) => Market.fromJson(e)).toList();
    } else {
      throw Exception('Failed to load markets: ${response.statusCode}');
    }
  }

  /// Create a price alert
  Future<PriceAlert> createAlert({
    required int userId,
    required int commodityId,
    int? marketId,
    required double thresholdPrice,
    required String alertType,
  }) async {
    final uri = Uri.parse('$baseUrl/alerts/');
    final response = await _client.post(
      uri,
      headers: {'Content-Type': 'application/json'},
      body: json.encode({
        'user_id': userId,
        'commodity_id': commodityId,
        'market_id': marketId,
        'threshold_price': thresholdPrice,
        'alert_type': alertType,
      }),
    );

    if (response.statusCode == 200 || response.statusCode == 201) {
      return PriceAlert.fromJson(json.decode(response.body));
    } else {
      throw Exception('Failed to create alert: ${response.statusCode}');
    }
  }

  /// Get user's alerts
  Future<List<PriceAlert>> getUserAlerts(int userId) async {
    final uri = Uri.parse('$baseUrl/alerts/user/$userId');
    final response = await _client.get(uri);

    if (response.statusCode == 200) {
      final List<dynamic> data = json.decode(response.body);
      return data.map((e) => PriceAlert.fromJson(e)).toList();
    } else {
      throw Exception('Failed to load alerts: ${response.statusCode}');
    }
  }
}

// Singleton instance
final apiService = ApiService();
