/// Data models for the BazaarSetu app

/// Commodity (vegetable/fruit) model
class Commodity {
  final int id;
  final String name;
  final String? nameTelugu;
  final String? nameHindi;
  final String category;
  final String? imageUrl;
  final String unit;

  Commodity({
    required this.id,
    required this.name,
    this.nameTelugu,
    this.nameHindi,
    this.category = 'vegetable',
    this.imageUrl,
    this.unit = 'kg',
  });

  factory Commodity.fromJson(Map<String, dynamic> json) {
    return Commodity(
      id: json['id'],
      name: json['name'],
      nameTelugu: json['name_telugu'],
      nameHindi: json['name_hindi'],
      category: json['category'] ?? 'vegetable',
      imageUrl: json['image_url'],
      unit: json['unit'] ?? 'kg',
    );
  }

  String getLocalizedName(String locale) {
    switch (locale) {
      case 'te':
        return nameTelugu ?? name;
      case 'hi':
        return nameHindi ?? name;
      default:
        return name;
    }
  }
}

/// Market model
class Market {
  final int id;
  final String name;
  final String? nameTelugu;
  final String district;
  final int stateId;
  final double? latitude;
  final double? longitude;

  Market({
    required this.id,
    required this.name,
    this.nameTelugu,
    required this.district,
    required this.stateId,
    this.latitude,
    this.longitude,
  });

  factory Market.fromJson(Map<String, dynamic> json) {
    return Market(
      id: json['id'],
      name: json['name'],
      nameTelugu: json['name_telugu'],
      district: json['district'],
      stateId: json['state_id'],
      latitude: json['latitude']?.toDouble(),
      longitude: json['longitude']?.toDouble(),
    );
  }
}

/// Price with details model (for today's prices)
class PriceWithDetails {
  final String commodityName;
  final String? commodityNameTelugu;
  final String? commodityNameHindi;
  final String? commodityImage;
  final String marketName;
  final String district;
  final String stateName;
  final double minPrice;
  final double maxPrice;
  final double modalPrice;
  final DateTime priceDate;
  final String unit;
  final double? priceChange;

  PriceWithDetails({
    required this.commodityName,
    this.commodityNameTelugu,
    this.commodityNameHindi,
    this.commodityImage,
    required this.marketName,
    required this.district,
    required this.stateName,
    required this.minPrice,
    required this.maxPrice,
    required this.modalPrice,
    required this.priceDate,
    this.unit = 'kg',
    this.priceChange,
  });

  factory PriceWithDetails.fromJson(Map<String, dynamic> json) {
    return PriceWithDetails(
      commodityName: json['commodity_name'],
      commodityNameTelugu: json['commodity_name_telugu'],
      commodityNameHindi: json['commodity_name_hindi'],
      commodityImage: json['commodity_image'],
      marketName: json['market_name'],
      district: json['district'],
      stateName: json['state_name'],
      minPrice: json['min_price'].toDouble(),
      maxPrice: json['max_price'].toDouble(),
      modalPrice: json['modal_price'].toDouble(),
      priceDate: DateTime.parse(json['price_date']),
      unit: json['unit'] ?? 'kg',
      priceChange: json['price_change']?.toDouble(),
    );
  }

  String getLocalizedName(String locale) {
    switch (locale) {
      case 'te':
        return commodityNameTelugu ?? commodityName;
      case 'hi':
        return commodityNameHindi ?? commodityName;
      default:
        return commodityName;
    }
  }

  bool get isPriceUp => priceChange != null && priceChange! > 0;
  bool get isPriceDown => priceChange != null && priceChange! < 0;
}

/// Price trend point
class PriceTrendPoint {
  final DateTime date;
  final double modalPrice;

  PriceTrendPoint({required this.date, required this.modalPrice});

  factory PriceTrendPoint.fromJson(Map<String, dynamic> json) {
    return PriceTrendPoint(
      date: DateTime.parse(json['date']),
      modalPrice: json['modal_price'].toDouble(),
    );
  }
}

/// Price trend model
class PriceTrend {
  final int commodityId;
  final String commodityName;
  final int? marketId;
  final String? marketName;
  final List<PriceTrendPoint> trendData;
  final double avgPrice;
  final double minPrice;
  final double maxPrice;
  final double? priceChange7d;
  final double? priceChange30d;

  PriceTrend({
    required this.commodityId,
    required this.commodityName,
    this.marketId,
    this.marketName,
    required this.trendData,
    required this.avgPrice,
    required this.minPrice,
    required this.maxPrice,
    this.priceChange7d,
    this.priceChange30d,
  });

  factory PriceTrend.fromJson(Map<String, dynamic> json) {
    return PriceTrend(
      commodityId: json['commodity_id'],
      commodityName: json['commodity_name'],
      marketId: json['market_id'],
      marketName: json['market_name'],
      trendData: (json['trend_data'] as List)
          .map((e) => PriceTrendPoint.fromJson(e))
          .toList(),
      avgPrice: json['avg_price'].toDouble(),
      minPrice: json['min_price'].toDouble(),
      maxPrice: json['max_price'].toDouble(),
      priceChange7d: json['price_change_7d']?.toDouble(),
      priceChange30d: json['price_change_30d']?.toDouble(),
    );
  }
}

/// Price alert model
class PriceAlert {
  final int id;
  final int commodityId;
  final String commodityName;
  final int? marketId;
  final double thresholdPrice;
  final String alertType; // 'below' or 'above'
  final bool isActive;

  PriceAlert({
    required this.id,
    required this.commodityId,
    required this.commodityName,
    this.marketId,
    required this.thresholdPrice,
    required this.alertType,
    required this.isActive,
  });

  factory PriceAlert.fromJson(Map<String, dynamic> json) {
    return PriceAlert(
      id: json['id'],
      commodityId: json['commodity_id'],
      commodityName: json['commodity']?['name'] ?? 'Unknown',
      marketId: json['market_id'],
      thresholdPrice: json['threshold_price'].toDouble(),
      alertType: json['alert_type'],
      isActive: json['is_active'],
    );
  }
}
