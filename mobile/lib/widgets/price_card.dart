import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../providers/price_provider.dart';
import '../providers/settings_provider.dart';
import '../models/models.dart';

/// Card widget displaying a vegetable price
class PriceCard extends StatelessWidget {
  final PriceWithDetails price;

  const PriceCard({super.key, required this.price});

  @override
  Widget build(BuildContext context) {
    final settings = context.watch<SettingsProvider>();
    final localeCode = settings.locale.languageCode;
    final theme = Theme.of(context);
    
    final localizedName = price.getLocalizedName(localeCode);
    
    return Card(
      margin: const EdgeInsets.only(bottom: 12),
      child: InkWell(
        borderRadius: BorderRadius.circular(16),
        onTap: () {
          // TODO: Navigate to detail screen
        },
        child: Padding(
          padding: const EdgeInsets.all(16),
          child: Row(
            children: [
              // Vegetable icon/image
              _buildVegetableIcon(context),
              const SizedBox(width: 16),
              
              // Details
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    // Vegetable name
                    Text(
                      localizedName,
                      style: theme.textTheme.titleMedium?.copyWith(
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                    const SizedBox(height: 4),
                    
                    // Market & location
                    Row(
                      children: [
                        const Icon(Icons.store, size: 14, color: Colors.grey),
                        const SizedBox(width: 4),
                        Expanded(
                          child: Text(
                            '${price.marketName}, ${price.district}',
                            style: theme.textTheme.bodySmall?.copyWith(
                              color: Colors.grey[600],
                            ),
                            overflow: TextOverflow.ellipsis,
                          ),
                        ),
                      ],
                    ),
                  ],
                ),
              ),
              
              // Price
              Column(
                crossAxisAlignment: CrossAxisAlignment.end,
                children: [
                  // Modal price
                  Text(
                    '₹${price.modalPrice.toStringAsFixed(0)}',
                    style: theme.textTheme.titleLarge?.copyWith(
                      fontWeight: FontWeight.bold,
                      color: theme.colorScheme.primary,
                    ),
                  ),
                  Text(
                    '/${price.unit}',
                    style: theme.textTheme.bodySmall?.copyWith(
                      color: Colors.grey[600],
                    ),
                  ),
                  
                  // Price change
                  if (price.priceChange != null)
                    _buildPriceChange(context),
                ],
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildVegetableIcon(BuildContext context) {
    final theme = Theme.of(context);
    
    // Map vegetable names to emojis
    String emoji = _getVegetableEmoji(price.commodityName);
    
    return Container(
      width: 56,
      height: 56,
      decoration: BoxDecoration(
        color: theme.colorScheme.primaryContainer,
        borderRadius: BorderRadius.circular(12),
      ),
      child: Center(
        child: Text(
          emoji,
          style: const TextStyle(fontSize: 28),
        ),
      ),
    );
  }

  Widget _buildPriceChange(BuildContext context) {
    final change = price.priceChange!;
    final isUp = change > 0;
    final isDown = change < 0;
    
    Color color = Colors.grey;
    IconData icon = Icons.remove;
    
    if (isUp) {
      color = Colors.red;
      icon = Icons.arrow_upward;
    } else if (isDown) {
      color = Colors.green;
      icon = Icons.arrow_downward;
    }
    
    return Row(
      mainAxisSize: MainAxisSize.min,
      children: [
        Icon(icon, size: 14, color: color),
        Text(
          '${change.abs().toStringAsFixed(1)}%',
          style: TextStyle(
            fontSize: 12,
            color: color,
            fontWeight: FontWeight.w500,
          ),
        ),
      ],
    );
  }

  String _getVegetableEmoji(String name) {
    final lowercaseName = name.toLowerCase();
    
    if (lowercaseName.contains('tomato')) return '🍅';
    if (lowercaseName.contains('onion')) return '🧅';
    if (lowercaseName.contains('potato')) return '🥔';
    if (lowercaseName.contains('chilli') || lowercaseName.contains('pepper')) return '🌶️';
    if (lowercaseName.contains('brinjal') || lowercaseName.contains('eggplant')) return '🍆';
    if (lowercaseName.contains('cabbage')) return '🥬';
    if (lowercaseName.contains('cauliflower')) return '🥦';
    if (lowercaseName.contains('carrot')) return '🥕';
    if (lowercaseName.contains('bean')) return '🫘';
    if (lowercaseName.contains('lady finger') || lowercaseName.contains('okra')) return '🥒';
    if (lowercaseName.contains('gourd')) return '🥒';
    if (lowercaseName.contains('cucumber')) return '🥒';
    if (lowercaseName.contains('pumpkin')) return '🎃';
    if (lowercaseName.contains('spinach') || lowercaseName.contains('leafy')) return '🥬';
    if (lowercaseName.contains('ginger')) return '🫚';
    if (lowercaseName.contains('garlic')) return '🧄';
    if (lowercaseName.contains('lemon') || lowercaseName.contains('lime')) return '🍋';
    if (lowercaseName.contains('coconut')) return '🥥';
    if (lowercaseName.contains('banana')) return '🍌';
    if (lowercaseName.contains('coriander') || lowercaseName.contains('curry')) return '🌿';
    
    return '🥬'; // Default vegetable emoji
  }
}
