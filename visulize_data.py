import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from matplotlib.ticker import FuncFormatter

# Read the CSV file
df = pd.read_csv(r'C:\\Users\\ASUS\\Downloads\\vs code\\\.vscode\\python\\data_science\\data\\stocks.csv')

# Set style for better visualizations
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_context("talk")
colors = sns.color_palette("husl", 8)

# Format market cap data
df['market_cap'] = df['market_cap'].str.replace('$', '').str.replace('B', '').astype(float)

# Helper function for billions formatter
def billions_formatter(x, pos):
    return f'${x:,.1f}B'

# 1. Enhanced Market Cap Distribution by Sector
plt.figure(figsize=(14, 8))
sector_market_cap = df.groupby('sector')['market_cap'].sum().sort_values(ascending=True)
bars = plt.barh(sector_market_cap.index, sector_market_cap.values, color=colors)
plt.title('Total Market Cap by Sector', fontsize=16, pad=20)
plt.xlabel('Market Cap (Billions USD)', fontsize=12)
plt.gca().xaxis.set_major_formatter(FuncFormatter(billions_formatter))

# Add value labels
for bar in bars:
    width = bar.get_width()
    plt.text(width, bar.get_y() + bar.get_height()/2,
             f'${width:,.1f}B', 
             ha='left', va='center', fontsize=10)
plt.tight_layout()
plt.savefig('market_cap_by_sector.png', dpi=300, bbox_inches='tight')
plt.close()

# 2. Enhanced Top 10 Companies Visualization
plt.figure(figsize=(14, 8))
top_10 = df.nlargest(10, 'market_cap')
bars = sns.barplot(data=top_10, x='company_name', y='market_cap', palette='viridis')
plt.xticks(rotation=45, ha='right')
plt.title('Top 10 Companies by Market Cap', fontsize=16, pad=20)
plt.xlabel('Company Name', fontsize=12)
plt.ylabel('Market Cap (Billions USD)', fontsize=12)

# Add value labels
for bar in bars.patches:
    bars.annotate(f'${bar.get_height():.1f}B',
                 (bar.get_x() + bar.get_width() / 2, bar.get_height()),
                 ha='center', va='bottom')
plt.tight_layout()
plt.savefig('top_10_market_cap.png', dpi=300, bbox_inches='tight')
plt.close()

# 3. Enhanced Price vs Volume Scatter Plot with Plotly
fig = px.scatter(df, x='current_price', y='volume',
                 hover_data=['company_name', 'symbol'],
                 title='Stock Price vs Trading Volume',
                 labels={'current_price': 'Current Price (USD)',
                        'volume': 'Trading Volume'},
                 color='sector',
                 size='market_cap',
                 size_max=60)
fig.update_layout(title_x=0.5, title_font_size=20)
fig.write_html('price_vs_volume_interactive.html')

# 4. Enhanced PE Ratio Distribution
plt.figure(figsize=(14, 8))
pe_data = df[df['pe_ratio'] != 'N/A']
pe_data['pe_ratio'] = pd.to_numeric(pe_data['pe_ratio'])

# Create violin plot with overlaid box plot
sns.violinplot(data=pe_data, x='sector', y='pe_ratio', color='lightgray', inner=None)
sns.boxplot(data=pe_data, x='sector', y='pe_ratio', width=0.2, 
            palette='viridis', showfliers=False)

plt.xticks(rotation=45, ha='right')
plt.title('PE Ratio Distribution by Sector', fontsize=16, pad=20)
plt.xlabel('Sector', fontsize=12)
plt.ylabel('PE Ratio', fontsize=12)
plt.tight_layout()
plt.savefig('pe_ratio_distribution.png', dpi=300, bbox_inches='tight')
plt.close()

# Additional Statistics with formatted output
print("\n=== Stock Market Analysis Summary ===")
print(f"\nTotal Companies Analyzed: {len(df):,}")
print(f"Sectors Represented: {len(df['sector'].unique())}")
print("\nMarket Statistics by Sector:")
sector_stats = df.groupby('sector').agg({
    'current_price': ['mean', 'min', 'max'],
    'market_cap': 'sum'
}).round(2)
print(sector_stats.to_string())