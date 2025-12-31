import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../providers/price_provider.dart';
import '../l10n/app_localizations.dart';

/// Custom search bar for filtering vegetables
class CustomSearchBar extends StatefulWidget {
  const CustomSearchBar({super.key});

  @override
  State<CustomSearchBar> createState() => _CustomSearchBarState();
}

class _CustomSearchBarState extends State<CustomSearchBar> {
  final TextEditingController _controller = TextEditingController();

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final l10n = AppLocalizations.of(context);
    final provider = context.read<PriceProvider>();
    
    return Padding(
      padding: const EdgeInsets.all(16),
      child: SearchBar(
        controller: _controller,
        hintText: l10n.search,
        leading: const Padding(
          padding: EdgeInsets.only(left: 8),
          child: Icon(Icons.search),
        ),
        trailing: [
          if (_controller.text.isNotEmpty)
            IconButton(
              icon: const Icon(Icons.clear),
              onPressed: () {
                _controller.clear();
                provider.setSearchQuery('');
              },
            ),
        ],
        onChanged: (value) {
          provider.setSearchQuery(value);
          setState(() {}); // Update trailing icon visibility
        },
        elevation: WidgetStateProperty.all(1),
        padding: WidgetStateProperty.all(
          const EdgeInsets.symmetric(horizontal: 8),
        ),
      ),
    );
  }
}
