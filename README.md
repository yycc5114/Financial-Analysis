##1. Analytical Objective and Target Audience
This project undertakes a rigorous quantitative financial analysis of publicly listed manufacturing enterprises within the Chinese equity market over the fiscal period 2020–2025. The primary objective is to evaluate and contrast key financial metrics pertaining to profitability, short-term solvency, and operational efficiency. The framework is designed to facilitate efficient financial performance assessment for two distinct user cohorts: (1) individual retail investors seeking a low-barrier, data-driven screening methodology, and (2) undergraduate students in accounting and finance who wish to observe the practical application of Python in corporate financial statement analysis.
##2. Data Provenance and Variable Specification
· Database: WRDS–CSMAR Financial Statement Database
· Observation Window: January 1, 2020 – December 31, 2025
· Statement Type: Annual consolidated financial statements (Fiscal Year-End: December)
· Core Financial Variables:
  · Net Profit
  · Total Assets
  · Total Shareholders' Equity
  · Operating Revenue
  · Current Assets / Current Liabilities
· Data Retrieval Date: 2026-04-18
Rationale: The CSMAR database is selected for its authoritative standardization of Chinese corporate disclosures, ensuring the integrity and comparability of the empirical data underlying this analysis.
##3. Computational Methodology and Technical Implementation
The analytical workflow is structured according to a reproducible data science pipeline, implemented entirely in Python.
1. Data Acquisition: A connection to the WRDS cloud server is established via the wrds Python library. Parameterized SQL queries are executed to extract standardized financial statement items, mitigating manual extraction errors.
2. Data Pre-processing: The raw dataset undergoes systematic cleaning, including the exclusion of null observations, filtration to retain only December fiscal year-end records (to maintain temporal consistency), and normalization of stock ticker-to-entity name mapping.
3. Financial Ratio Computation: Five core financial indicators are algorithmically derived from the cleaned absolute values:
   · Return on Assets (ROA)
   · Return on Equity (ROE)
   · Net Profit Margin
   · Current Ratio
   · Total Debt Ratio (Debt-to-Assets)
4. Data Visualization: The matplotlib library is employed to generate standardized time-series trend charts, enabling intuitive cross-sectional and longitudinal comparison of financial trajectories across the selected firms.
5. Result Export: Structured analytical outputs are serialized and exported to the Microsoft Excel Open XML Format (*.xlsx), facilitating ancillary quantitative review or secondary data processing by the user.
##4. Empirical Findings and Insights
Analysis of the sample set yields the following empirical observations:
1. Profitability Dispersion: Metrics of profitability (ROA and ROE) exhibit pronounced cross-sectional differentiation among the sample constituents, indicative of material variance in asset utilization efficiency and return generation capabilities.
2. Margin Stability: Leading enterprises within the sample demonstrate relatively stable net profit margin trajectories, suggesting robust operational resilience against cyclical or idiosyncratic market pressures.
3. Liquidity Adequacy: Current ratio calculations confirm that all sample entities maintain short-term liquidity positions consistent with conventional solvency thresholds, thereby indicating an absence of immediate liquidity distress.
4. Capital Structure Prudence: Aggregate debt-to-asset ratios are observed to reside within a reasonable and sustainable corridor, reflecting a conservative posture toward long-term financial leverage and capital structure management.
##5. Execution and Usage Instructions
To replicate the analysis environment and execute the computational workflow, adhere to the following protocol:
1. Environment Configuration: Install the requisite Python dependencies via pip
2. Authentication: Replace the placeholder WRDS_USERNAME variable within the script with valid WRDS institutional credentials.
3. Execution: Run the primary Python script. The program will prompt interactive input for stock ticker codes and corresponding company identifiers.
4. Output Inspection: Upon successful execution, the root directory will contain:
   · A comprehensive Excel workbook (Financial_Analysis_Results.xlsx) containing the computed ratio panel data.
   · Five discrete time-series trend charts in PNG format.
##6. Demonstration Link
https://www.capcut.cn/share/7631232489608156440?t=1
##7. Limitations and Avenues for Future Enhancement
Current Limitations:
· Sample Scope: The analysis is circumscribed by a limited cross-section of manufacturing firms, which precludes the establishment of robust industry-wide benchmarks or sector-neutral comparative analysis.
· Temporal Granularity: The reliance on annual reporting frequency obscures intra-year volatility and short-term operational dynamics that are more readily discernible in quarterly disclosures.
· Analytical Depth: The current methodological framework is restricted to descriptive diagnostic analysis and does not incorporate inferential modeling or predictive forecasting.
Proposed Future Enhancements:
· Sample Expansion: Increase the coverage to encompass the entire universe of listed manufacturing enterprises within the CSMAR database.
· Frequency Augmentation: Integrate quarterly financial statement data to support high-frequency time-series decomposition and seasonality analysis.
· Model Integration: Implement valuation models and multivariate regression techniques to assess the predictive capacity of the derived financial ratios on future equity performance.
