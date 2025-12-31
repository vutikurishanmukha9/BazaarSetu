import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';

/// Settings provider for app preferences
class SettingsProvider extends ChangeNotifier {
  static const String _localeKey = 'locale';
  static const String _themeModeKey = 'theme_mode';
  
  Locale _locale = const Locale('en');
  ThemeMode _themeMode = ThemeMode.system;
  
  Locale get locale => _locale;
  ThemeMode get themeMode => _themeMode;
  
  String get languageName {
    switch (_locale.languageCode) {
      case 'te':
        return 'తెలుగు';
      case 'hi':
        return 'हिंदी';
      default:
        return 'English';
    }
  }

  SettingsProvider() {
    _loadSettings();
  }

  Future<void> _loadSettings() async {
    final prefs = await SharedPreferences.getInstance();
    
    // Load locale
    final localeCode = prefs.getString(_localeKey) ?? 'en';
    _locale = Locale(localeCode);
    
    // Load theme mode
    final themeModeIndex = prefs.getInt(_themeModeKey) ?? 0;
    _themeMode = ThemeMode.values[themeModeIndex];
    
    notifyListeners();
  }

  Future<void> setLocale(Locale locale) async {
    _locale = locale;
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString(_localeKey, locale.languageCode);
    notifyListeners();
  }

  Future<void> setThemeMode(ThemeMode mode) async {
    _themeMode = mode;
    final prefs = await SharedPreferences.getInstance();
    await prefs.setInt(_themeModeKey, mode.index);
    notifyListeners();
  }

  /// Toggle between light and dark mode
  Future<void> toggleTheme() async {
    if (_themeMode == ThemeMode.light) {
      await setThemeMode(ThemeMode.dark);
    } else {
      await setThemeMode(ThemeMode.light);
    }
  }

  /// Cycle through languages: en -> te -> hi -> en
  Future<void> cycleLanguage() async {
    switch (_locale.languageCode) {
      case 'en':
        await setLocale(const Locale('te'));
        break;
      case 'te':
        await setLocale(const Locale('hi'));
        break;
      default:
        await setLocale(const Locale('en'));
    }
  }
}
