"""
Logistics Network Simulation & Exploratory Data Analysis (EDA)
Author: SUMIT KUMAR
Email: SUMIT277203YT@GMAIL.COM
Contact: 9120329201
Role: Senior Data Scientist & Lead Logistics Analyst
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

def generate_logistics_data(n_samples=500, random_seed=42):
    """
    Generates a realistic 500-shipment logistics dataset with controlled statistical distributions.
    """
    np.random.seed(random_seed)
    
    # 1. Shipment_ID (Format: SHP_001, SHP_002... SHP_500)
    shipment_ids = [f"SHP_{i:03d}" for i in range(1, n_samples + 1)]
    
    # 2. Shipment_Volume_m3 (Uniform distribution between 5.0 and 50.0 m3)
    volume = np.random.uniform(5.0, 50.0, size=n_samples)
    
    # 3. Distance_km (Uniform distribution between 50 and 1500 km)
    distance = np.random.uniform(50.0, 1500.0, size=n_samples)
    
    # 4. Transportation_Cost_USD (Base $100 + $1.2/km + $5/m3 + Gaussian white noise N(0, 45^2))
    cost_noise = np.random.normal(0.0, 45.0, size=n_samples)
    cost = 100.0 + (1.2 * distance) + (5.0 * volume) + cost_noise
    # Ensure all costs are strictly positive
    cost = np.clip(cost, 120.0, None)
    
    # 5. Delivery_Time_Hours (Base 4h + speed factor distance/65 + exponential operational delay noise)
    # Exponential noise generates realistic right-skewed operational bottlenecks (handling delays, customs, traffic)
    operational_delay = np.random.exponential(scale=3.5, size=n_samples)
    delivery_time = 4.0 + (distance / 65.0) + operational_delay
    
    df = pd.DataFrame({
        'Shipment_ID': shipment_ids,
        'Shipment_Volume_m3': np.round(volume, 2),
        'Distance_km': np.round(distance, 2),
        'Transportation_Cost_USD': np.round(cost, 2),
        'Delivery_Time_Hours': np.round(delivery_time, 2)
    })
    
    return df

def perform_eda(df):
    """
    Computes comprehensive central tendencies, dispersion metrics, shape statistics, and correlation matrix.
    """
    num_cols = ['Shipment_Volume_m3', 'Distance_km', 'Transportation_Cost_USD', 'Delivery_Time_Hours']
    
    stats_dict = {}
    for col in num_cols:
        series = df[col]
        stats_dict[col] = {
            'Mean': series.mean(),
            'Median': series.median(),
            'Mode': series.mode()[0],
            'Variance': series.var(),
            'Std Dev': series.std(),
            'Min': series.min(),
            'Max': series.max(),
            'IQR': series.quantile(0.75) - series.quantile(0.25),
            'Skewness': series.skew(),
            'Kurtosis': series.kurtosis()
        }
    
    stats_df = pd.DataFrame(stats_dict).T
    corr_matrix = df[num_cols].corr()
    
    return stats_df, corr_matrix

def generate_visualizations(df, output_dir="."):
    """
    Generates and saves 3 high-definition visualization charts.
    """
    sns.set_theme(style="whitegrid", font="sans-serif")
    plt.rcParams.update({'font.size': 11, 'figure.autolayout': True})
    
    # ---------------------------------------------------------
    # Chart 1: Right-skewed Distribution of Delivery Times (Histogram with KDE)
    # ---------------------------------------------------------
    fig, ax = plt.subplots(figsize=(9, 5), dpi=300)
    sns.histplot(
        df['Delivery_Time_Hours'],
        kde=True,
        color='#1f77b4',
        bins=25,
        ax=ax,
        edgecolor='black',
        alpha=0.65
    )
    
    mean_val = df['Delivery_Time_Hours'].mean()
    median_val = df['Delivery_Time_Hours'].median()
    
    ax.axvline(mean_val, color='#d62728', linestyle='--', linewidth=2, label=f'Mean: {mean_val:.2f} hrs')
    ax.axvline(median_val, color='#2ca02c', linestyle='-', linewidth=2, label=f'Median: {median_val:.2f} hrs')
    
    ax.set_title('Right-Skewed Distribution of Delivery Times (Operational Delays)', fontsize=14, fontweight='bold', pad=12)
    ax.set_xlabel('Delivery Time (Hours)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Shipment Frequency', fontsize=12, fontweight='bold')
    ax.legend(loc='upper right', frameon=True, facecolor='white', framealpha=0.9)
    
    chart1_path = os.path.join(output_dir, 'delivery_time_distribution.png')
    plt.savefig(chart1_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"[+] Saved Chart 1: {chart1_path}")
    
    # ---------------------------------------------------------
    # Chart 2: Scatter Plot with Red Linear Regression Line (Distance vs Transportation Cost)
    # ---------------------------------------------------------
    fig, ax = plt.subplots(figsize=(9, 5), dpi=300)
    sns.regplot(
        data=df,
        x='Distance_km',
        y='Transportation_Cost_USD',
        ax=ax,
        scatter_kws={'alpha': 0.6, 'color': '#1f77b4', 's': 35},
        line_kws={'color': '#d62728', 'linewidth': 2.5, 'label': 'OLS Regression Fit: Cost = 100 + 1.20*Distance + 5.0*Volume'}
    )
    
    ax.set_title('Distance (km) vs. Transportation Cost ($USD)', fontsize=14, fontweight='bold', pad=12)
    ax.set_xlabel('Route Distance (km)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Transportation Cost ($USD)', fontsize=12, fontweight='bold')
    ax.legend(loc='upper left', frameon=True, facecolor='white', framealpha=0.9)
    
    chart2_path = os.path.join(output_dir, 'distance_vs_cost_scatter.png')
    plt.savefig(chart2_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"[+] Saved Chart 2: {chart2_path}")
    
    # ---------------------------------------------------------
    # Chart 3: Clean, Annotated Correlation Heatmap ('coolwarm')
    # ---------------------------------------------------------
    num_cols = ['Shipment_Volume_m3', 'Distance_km', 'Transportation_Cost_USD', 'Delivery_Time_Hours']
    corr = df[num_cols].corr()
    
    fig, ax = plt.subplots(figsize=(8, 6), dpi=300)
    sns.heatmap(
        corr,
        annot=True,
        fmt='.3f',
        cmap='coolwarm',
        vmin=-1,
        vmax=1,
        square=True,
        linewidths=1.5,
        cbar_kws={"shrink": 0.8, "label": "Pearson Correlation Coefficient"},
        ax=ax,
        annot_kws={'size': 12, 'weight': 'bold'}
    )
    
    ax.set_title('Logistics Key Performance Indicators Correlation Heatmap', fontsize=14, fontweight='bold', pad=12)
    plt.xticks(rotation=15, ha='right', fontweight='bold')
    plt.yticks(rotation=0, fontweight='bold')
    
    chart3_path = os.path.join(output_dir, 'correlation_heatmap.png')
    plt.savefig(chart3_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"[+] Saved Chart 3: {chart3_path}")

def main():
    print("================================================================")
    print("LOGISTICS NETWORK SIMULATION & STATISTICAL ANALYSIS PIPELINE")
    print("Lead Analyst: SUMIT KUMAR | SUMIT277203YT@GMAIL.COM | 9120329201")
    print("================================================================\n")
    
    # Generate Dataset
    df = generate_logistics_data(n_samples=500, random_seed=42)
    csv_path = "logistics_simulation_data.csv"
    df.to_csv(csv_path, index=False)
    print(f"[+] Dataset generated successfully: {len(df)} rows saved to '{csv_path}'\n")
    
    # Perform Statistical EDA
    stats_df, corr_matrix = perform_eda(df)
    
    print("--- CENTRAL TENDENCIES & DESCRIPTIVE STATISTICS ---")
    print(stats_df.to_string())
    print("\n--- PEARSON CORRELATION MATRIX ---")
    print(corr_matrix.to_string())
    print("\n================================================================")
    
    # Save statistics table to text file for reference
    with open("summary_statistics.txt", "w") as f:
        f.write("LOGISTICS NETWORK SIMULATION - STATISTICAL SUMMARY\n")
        f.write("Author: SUMIT KUMAR (SUMIT277203YT@GMAIL.COM | 9120329201)\n\n")
        f.write("DESCRIPTIVE STATISTICS:\n")
        f.write(stats_df.to_string())
        f.write("\n\nPEARSON CORRELATION MATRIX:\n")
        f.write(corr_matrix.to_string())
        
    # Generate Visualizations
    generate_visualizations(df)
    print("\n[+] EDA Execution & Visualization Pipeline Completed Successfully!")

if __name__ == "__main__":
    main()
