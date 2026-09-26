# SUBMISSION PORTAL DESCRIPTION

**AUTHOR:** SUMIT KUMAR  
**EMAIL:** SUMIT277203YT@GMAIL.COM  
**CONTACT:** +91 9120329201  
**ROLE:** Senior Data Scientist & Lead Logistics Analyst  

---

### SUBMISSION PORTAL TEXT (COPY & PASTE READY)

This project executes a corporate-grade statistical simulation and Exploratory Data Analysis (EDA) of a 500-shipment multimodal logistics network. Developed using a custom Python analytical engine (NumPy, Pandas, Matplotlib, Seaborn), five primary supply chain variables were modeled: shipment identification (SHP_001 to SHP_500), cargo volume (Uniform U(5, 50) m³), transit distance (Uniform U(50, 1500) km), transportation cost ($100 base + $1.20/km + $5/m³ + Gaussian white noise), and operational delivery time (4h base + distance/65 + exponential operational delay noise).

Rigorous descriptive statistics established a mean network spend of $1,141.03 USD per shipment and an average transit duration of 19.05 hours. Delivery time exhibited a right-skewed distribution (skewness = +0.417) driven by compounding exponential operational delays stretching delivery tails up to 46.63 hours. Pearson correlation analysis identified a near-unity correlation between transit distance and total cost (r = 0.988), alongside strong collinearity between distance and delivery time (r = 0.872).

To visualize these operational dynamics, three publication-grade figures were generated: (1) a right-skewed Delivery Time Distribution histogram with overlaid KDE, (2) an OLS Linear Regression scatter plot mapping distance vs. cost scaling, and (3) an annotated 'coolwarm' correlation heatmap. Empirically, the findings justify three executive interventions: dynamic GPS route optimization to reduce distance variance, cross-docking SLA enforcement to eliminate exponential bottleneck delays, and LTL load consolidation to maximize container volume utilization.
