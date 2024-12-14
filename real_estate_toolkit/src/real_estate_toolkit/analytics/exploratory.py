from typing import List, Dict
import polars as pl
import plotly.express as px
import plotly.graph_objects as go
import os

class MarketAnalyzer:
    def __init__(self, data_path: str):
        """
        Initialize the analyzer with data from a CSV file.
        """
        self.real_state_data = pl.read_csv(data_path)
        self.real_state_clean_data = None

    def clean_data(self) -> None:
        """
        Perform comprehensive data cleaning.
        """
        # Handling missing values and converting data types
        self.real_state_clean_data = self.real_state_data.fill_none("mean")  # Example strategy

    def generate_price_distribution_analysis(self) -> pl.DataFrame:
        """
        Analyze sale price distribution using clean data.
        """
        # Compute price statistics
        price_stats = self.real_state_clean_data.select([
            pl.col('SalePrice').mean().alias('Mean'),
            pl.col('SalePrice').median().alias('Median'),
            pl.col('SalePrice').std().alias('StdDev'),
            pl.col('SalePrice').min().alias('Min'),
            pl.col('SalePrice').max().alias('Max')
        ])
        # Create a histogram
        fig = px.histogram(self.real_state_clean_data.to_pandas(), x='SalePrice')
        fig.update_layout(title='Distribution of Sale Prices')
        output_path = 'src/real_estate_toolkit/analytics/outputs/sale_price_distribution.html'
        fig.write_html(output_path)
        return price_stats

    def neighborhood_price_comparison(self) -> pl.DataFrame:
        """
        Create a boxplot comparing house prices across different neighborhoods.
        """
        # Group by neighborhood and calculate statistics
        neighborhood_stats = self.real_state_clean_data.groupby('Neighborhood').agg([
            pl.col('SalePrice').median().alias('MedianPrice'),
            pl.col('SalePrice').list().alias('Prices')
        ]).sort('MedianPrice', reverse=True)

        # Plotting
        df = neighborhood_stats.to_pandas()
        fig = px.box(df, y='Prices', x='Neighborhood', labels={'Prices': 'Sale Price', 'Neighborhood': 'Neighborhood'})
        fig.update_layout(title='Neighborhood Price Comparison')
        output_path = 'src/real_estate_toolkit/analytics/outputs/neighborhood_price_comparison.html'
        fig.write_html(output_path)
        return neighborhood_stats

    def feature_correlation_heatmap(self, variables: List[str]) -> None:
        """
        Generate a correlation heatmap for selected variables.
        """
        # Compute correlation matrix
        data = self.real_state_clean_data.select(variables).to_pandas()
        corr_matrix = data.corr()
        fig = px.imshow(corr_matrix, text_auto=True, aspect="auto",
                        labels=dict(x="Variable", y="Variable", color="Correlation"),
                        x=variables, y=variables)
        fig.update_layout(title='Feature Correlation Heatmap')
        output_path = 'src/real_estate_toolkit/analytics/outputs/correlation_heatmap.html'
        fig.write_html(output_path)

    def create_scatter_plots(self) -> Dict[str, go.Figure]:
        """
        Create scatter plots exploring relationships between key features.
        """
        plots = {}
        # House price vs. Total square footage
        fig1 = px.scatter(self.real_state_clean_data.to_pandas(), x='GrLivArea', y='SalePrice', trendline="ols",
                          labels={'GrLivArea': 'Total Living Area (sq ft)', 'SalePrice': 'Sale Price'})
        plots['price_vs_sqft'] = fig1

        # Sale price vs. Year built
        fig2 = px.scatter(self.real_state_clean_data.to_pandas(), x='YearBuilt', y='SalePrice', trendline="ols",
                          labels={'YearBuilt': 'Year Built', 'SalePrice': 'Sale Price'})
        plots['price_vs_yearbuilt'] = fig2

        # Overall quality vs. Sale price
        fig3 = px.scatter(self.real_state_clean_data.to_pandas(), x='OverallQual', y='SalePrice', trendline="ols",
                          labels={'OverallQual': 'Overall Quality', 'SalePrice': 'Sale Price'})
        plots['quality_vs_price'] = fig3

        # Saving plots
        for key, fig in plots.items():
            output_path = f'src/real_estate_toolkit/analytics/outputs/{key}.html'
            fig.write_html(output_path)

        return plots


