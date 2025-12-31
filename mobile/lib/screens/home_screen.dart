import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../providers/price_provider.dart';
import '../providers/settings_provider.dart';
import '../l10n/app_localizations.dart';
import '../widgets/price_card.dart';
import '../widgets/search_bar.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  @override
  void initState() {
    super.initState();
    // Load prices on first build
    WidgetsBinding.instance.addPostFrameCallback((_) {
      context.read<PriceProvider>().loadTodayPrices();
      context.read<PriceProvider>().loadCommodities();
    });
  }

  @override
  Widget build(BuildContext context) {
    final l10n = AppLocalizations.of(context);
    final settings = context.watch<SettingsProvider>();
    
    return Scaffold(
      appBar: AppBar(
        title: Column(
          children: [
            Text(l10n.appTitle),
            Text(
              l10n.tagline,
              style: const TextStyle(fontSize: 12, fontWeight: FontWeight.w400),
            ),
          ],
        ),
        actions: [
          // Language toggle
          IconButton(
            icon: const Icon(Icons.language),
            tooltip: l10n.language,
            onPressed: () => settings.cycleLanguage(),
          ),
          // Theme toggle
          IconButton(
            icon: Icon(
              settings.themeMode == ThemeMode.dark 
                ? Icons.light_mode 
                : Icons.dark_mode,
            ),
            tooltip: l10n.theme,
            onPressed: () => settings.toggleTheme(),
          ),
        ],
      ),
      body: Column(
        children: [
          // Search bar
          const CustomSearchBar(),
          
          // Filter chips
          _buildFilterChips(context),
          
          // Prices list
          Expanded(
            child: Consumer<PriceProvider>(
              builder: (context, provider, _) {
                if (provider.isLoading) {
                  return const Center(
                    child: CircularProgressIndicator(),
                  );
                }
                
                if (provider.error != null && provider.todayPrices.isEmpty) {
                  return Center(
                    child: Column(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        const Icon(Icons.error_outline, size: 64, color: Colors.red),
                        const SizedBox(height: 16),
                        Text(l10n.error),
                        const SizedBox(height: 16),
                        ElevatedButton(
                          onPressed: () => provider.loadTodayPrices(),
                          child: Text(l10n.retry),
                        ),
                      ],
                    ),
                  );
                }
                
                final prices = provider.filteredPrices;
                
                if (prices.isEmpty) {
                  return Center(
                    child: Column(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        const Icon(Icons.inbox, size: 64, color: Colors.grey),
                        const SizedBox(height: 16),
                        Text(l10n.noData),
                      ],
                    ),
                  );
                }
                
                return RefreshIndicator(
                  onRefresh: () => provider.loadTodayPrices(),
                  child: ListView.builder(
                    padding: const EdgeInsets.all(16),
                    itemCount: prices.length,
                    itemBuilder: (context, index) {
                      return PriceCard(price: prices[index]);
                    },
                  ),
                );
              },
            ),
          ),
        ],
      ),
      bottomNavigationBar: NavigationBar(
        selectedIndex: 0,
        destinations: [
          NavigationDestination(
            icon: const Icon(Icons.home_outlined),
            selectedIcon: const Icon(Icons.home),
            label: l10n.todayPrices,
          ),
          NavigationDestination(
            icon: const Icon(Icons.store_outlined),
            selectedIcon: const Icon(Icons.store),
            label: l10n.markets,
          ),
          NavigationDestination(
            icon: const Icon(Icons.notifications_outlined),
            selectedIcon: const Icon(Icons.notifications),
            label: l10n.alerts,
          ),
          NavigationDestination(
            icon: const Icon(Icons.settings_outlined),
            selectedIcon: const Icon(Icons.settings),
            label: l10n.settings,
          ),
        ],
        onDestinationSelected: (index) {
          // TODO: Navigate to different screens
        },
      ),
    );
  }

  Widget _buildFilterChips(BuildContext context) {
    final provider = context.watch<PriceProvider>();
    final l10n = AppLocalizations.of(context);
    
    return SingleChildScrollView(
      scrollDirection: Axis.horizontal,
      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
      child: Row(
        children: [
          // State filter
          FilterChip(
            label: Text(
              provider.selectedStateId == 1 
                ? l10n.allStates
                : provider.selectedStateId == 2 
                  ? 'Telangana' 
                  : 'Andhra Pradesh',
            ),
            selected: provider.selectedStateId != null,
            onSelected: (_) {
              // Cycle through states
              if (provider.selectedStateId == null) {
                provider.setStateFilter(1); // AP
              } else if (provider.selectedStateId == 1) {
                provider.setStateFilter(2); // Telangana
              } else {
                provider.setStateFilter(null);
              }
            },
          ),
          const SizedBox(width: 8),
          
          // Clear filters
          if (provider.selectedStateId != null || 
              provider.selectedCommodityId != null ||
              provider.searchQuery.isNotEmpty)
            ActionChip(
              avatar: const Icon(Icons.clear, size: 18),
              label: Text(l10n.clearFilters),
              onPressed: () => provider.clearFilters(),
            ),
        ],
      ),
    );
  }
}
