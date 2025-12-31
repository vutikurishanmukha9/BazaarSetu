import 'package:flutter/material.dart';
import 'package:flutter_localizations/flutter_localizations.dart';

/// App localization class
class AppLocalizations {
  final Locale locale;

  AppLocalizations(this.locale);

  static AppLocalizations of(BuildContext context) {
    return Localizations.of<AppLocalizations>(context, AppLocalizations)!;
  }

  static const LocalizationsDelegate<AppLocalizations> delegate = _AppLocalizationsDelegate();

  static const List<LocalizationsDelegate<dynamic>> localizationsDelegates = [
    delegate,
    GlobalMaterialLocalizations.delegate,
    GlobalWidgetsLocalizations.delegate,
    GlobalCupertinoLocalizations.delegate,
  ];

  static final Map<String, Map<String, String>> _localizedValues = {
    'en': {
      'appTitle': 'BazaarSetu',
      'tagline': 'Live Vegetable Prices',
      'todayPrices': "Today's Prices",
      'search': 'Search vegetables...',
      'markets': 'Markets',
      'alerts': 'Alerts',
      'settings': 'Settings',
      'pricePerKg': '₹/kg',
      'minPrice': 'Min',
      'maxPrice': 'Max',
      'modalPrice': 'Modal',
      'priceUp': 'Price Up',
      'priceDown': 'Price Down',
      'noChange': 'No Change',
      'priceTrend': 'Price Trend',
      'last7Days': 'Last 7 Days',
      'last30Days': 'Last 30 Days',
      'compareMarkets': 'Compare Markets',
      'setAlert': 'Set Alert',
      'alertBelow': 'Alert when below',
      'alertAbove': 'Alert when above',
      'myAlerts': 'My Alerts',
      'language': 'Language',
      'theme': 'Theme',
      'darkMode': 'Dark Mode',
      'lightMode': 'Light Mode',
      'nearbyVendors': 'Nearby Vendors',
      'noData': 'No data available',
      'loading': 'Loading...',
      'error': 'Error loading data',
      'retry': 'Retry',
      'filterByState': 'Filter by State',
      'filterByMarket': 'Filter by Market',
      'clearFilters': 'Clear Filters',
      'andhrapradesh': 'Andhra Pradesh',
      'telangana': 'Telangana',
      'allStates': 'All States',
      'allMarkets': 'All Markets',
    },
    'te': {
      'appTitle': 'బజార్‌సేతు',
      'tagline': 'లైవ్ కూరగాయల ధరలు',
      'todayPrices': 'ఈరోజు ధరలు',
      'search': 'కూరగాయలు వెతకండి...',
      'markets': 'మార్కెట్లు',
      'alerts': 'హెచ్చరికలు',
      'settings': 'సెట్టింగ్‌లు',
      'pricePerKg': '₹/కేజీ',
      'minPrice': 'కనిష్ట',
      'maxPrice': 'గరిష్ట',
      'modalPrice': 'మోడల్',
      'priceUp': 'ధర పెరిగింది',
      'priceDown': 'ధర తగ్గింది',
      'noChange': 'మార్పు లేదు',
      'priceTrend': 'ధర ట్రెండ్',
      'last7Days': 'గత 7 రోజులు',
      'last30Days': 'గత 30 రోజులు',
      'compareMarkets': 'మార్కెట్లను పోల్చండి',
      'setAlert': 'హెచ్చరిక సెట్ చేయండి',
      'alertBelow': 'ధర తగ్గినప్పుడు హెచ్చరిక',
      'alertAbove': 'ధర పెరిగినప్పుడు హెచ్చరిక',
      'myAlerts': 'నా హెచ్చరికలు',
      'language': 'భాష',
      'theme': 'థీమ్',
      'darkMode': 'డార్క్ మోడ్',
      'lightMode': 'లైట్ మోడ్',
      'nearbyVendors': 'సమీపంలో విక్రేతలు',
      'noData': 'డేటా అందుబాటులో లేదు',
      'loading': 'లోడ్ అవుతోంది...',
      'error': 'డేటా లోడ్ చేయడంలో లోపం',
      'retry': 'మళ్ళీ ప్రయత్నించండి',
      'filterByState': 'రాష్ట్రం ద్వారా ఫిల్టర్',
      'filterByMarket': 'మార్కెట్ ద్వారా ఫిల్టర్',
      'clearFilters': 'ఫిల్టర్లు క్లియర్ చేయండి',
      'andhrapradesh': 'ఆంధ్ర ప్రదేశ్',
      'telangana': 'తెలంగాణ',
      'allStates': 'అన్ని రాష్ట్రాలు',
      'allMarkets': 'అన్ని మార్కెట్లు',
    },
    'hi': {
      'appTitle': 'बाज़ारसेतु',
      'tagline': 'लाइव सब्ज़ी भाव',
      'todayPrices': 'आज के भाव',
      'search': 'सब्ज़ियाँ खोजें...',
      'markets': 'मंडी',
      'alerts': 'अलर्ट',
      'settings': 'सेटिंग्स',
      'pricePerKg': '₹/किलो',
      'minPrice': 'न्यूनतम',
      'maxPrice': 'अधिकतम',
      'modalPrice': 'मोडल',
      'priceUp': 'भाव बढ़ा',
      'priceDown': 'भाव गिरा',
      'noChange': 'कोई बदलाव नहीं',
      'priceTrend': 'भाव ट्रेंड',
      'last7Days': 'पिछले 7 दिन',
      'last30Days': 'पिछले 30 दिन',
      'compareMarkets': 'मंडियों की तुलना',
      'setAlert': 'अलर्ट सेट करें',
      'alertBelow': 'भाव कम होने पर अलर्ट',
      'alertAbove': 'भाव बढ़ने पर अलर्ट',
      'myAlerts': 'मेरे अलर्ट',
      'language': 'भाषा',
      'theme': 'थीम',
      'darkMode': 'डार्क मोड',
      'lightMode': 'लाइट मोड',
      'nearbyVendors': 'आस-पास के विक्रेता',
      'noData': 'कोई डेटा नहीं',
      'loading': 'लोड हो रहा है...',
      'error': 'डेटा लोड करने में त्रुटि',
      'retry': 'पुनः प्रयास करें',
      'filterByState': 'राज्य द्वारा फ़िल्टर',
      'filterByMarket': 'मंडी द्वारा फ़िल्टर',
      'clearFilters': 'फ़िल्टर साफ़ करें',
      'andhrapradesh': 'आंध्र प्रदेश',
      'telangana': 'तेलंगाना',
      'allStates': 'सभी राज्य',
      'allMarkets': 'सभी मंडी',
    },
  };

  String get appTitle => _localizedValues[locale.languageCode]!['appTitle']!;
  String get tagline => _localizedValues[locale.languageCode]!['tagline']!;
  String get todayPrices => _localizedValues[locale.languageCode]!['todayPrices']!;
  String get search => _localizedValues[locale.languageCode]!['search']!;
  String get markets => _localizedValues[locale.languageCode]!['markets']!;
  String get alerts => _localizedValues[locale.languageCode]!['alerts']!;
  String get settings => _localizedValues[locale.languageCode]!['settings']!;
  String get pricePerKg => _localizedValues[locale.languageCode]!['pricePerKg']!;
  String get minPrice => _localizedValues[locale.languageCode]!['minPrice']!;
  String get maxPrice => _localizedValues[locale.languageCode]!['maxPrice']!;
  String get modalPrice => _localizedValues[locale.languageCode]!['modalPrice']!;
  String get priceUp => _localizedValues[locale.languageCode]!['priceUp']!;
  String get priceDown => _localizedValues[locale.languageCode]!['priceDown']!;
  String get noChange => _localizedValues[locale.languageCode]!['noChange']!;
  String get priceTrend => _localizedValues[locale.languageCode]!['priceTrend']!;
  String get compareMarkets => _localizedValues[locale.languageCode]!['compareMarkets']!;
  String get setAlert => _localizedValues[locale.languageCode]!['setAlert']!;
  String get myAlerts => _localizedValues[locale.languageCode]!['myAlerts']!;
  String get language => _localizedValues[locale.languageCode]!['language']!;
  String get theme => _localizedValues[locale.languageCode]!['theme']!;
  String get darkMode => _localizedValues[locale.languageCode]!['darkMode']!;
  String get nearbyVendors => _localizedValues[locale.languageCode]!['nearbyVendors']!;
  String get noData => _localizedValues[locale.languageCode]!['noData']!;
  String get loading => _localizedValues[locale.languageCode]!['loading']!;
  String get error => _localizedValues[locale.languageCode]!['error']!;
  String get retry => _localizedValues[locale.languageCode]!['retry']!;
  String get clearFilters => _localizedValues[locale.languageCode]!['clearFilters']!;
  String get allStates => _localizedValues[locale.languageCode]!['allStates']!;
  String get allMarkets => _localizedValues[locale.languageCode]!['allMarkets']!;
}

class _AppLocalizationsDelegate extends LocalizationsDelegate<AppLocalizations> {
  const _AppLocalizationsDelegate();

  @override
  bool isSupported(Locale locale) {
    return ['en', 'te', 'hi'].contains(locale.languageCode);
  }

  @override
  Future<AppLocalizations> load(Locale locale) async {
    return AppLocalizations(locale);
  }

  @override
  bool shouldReload(_AppLocalizationsDelegate old) => false;
}
