# 🍫 Menstrual Cycle & Sweet Consumption — DSA210 Fall 2025 Project

---

##  Motivation
Many people report that they crave sweets or chocolate more intensely **when they are on their period**.  
This project aims to test that idea using **real self-recorded data**.  
Is there a measurable difference in my sweet consumption **during menstruation** compared to other days?

By collecting daily data on sweet intake and period status, this project seeks to uncover whether this common belief has statistical support. The goal is identifying if being on a period correlates with increased sugar cravings or dessert consumption.  



---

##  Data Sources

| Data Type | Source | Description |
|------------|---------|-------------|
| **Period Tracking Data** | Personal log (Clue, Flo, Apple Health, or manual entry) | Daily record of whether I am on my period (1 = yes, 0 = no) |
| **Sweet Consumption** | Self-recorded daily intake (portion count, grams) | Quantitative measure of how much sweet food was consumed each day |
| **Purchase Data (Optional)** | Getir, Yemeksepeti, Trendyol Go order history | Used to validate or supplement self-reported sweet consumption |

---

##  Methodology

1. **Data Collection:**  
   - Track daily sweet consumption using a simple self-log (e.g., how many sweets/desserts consumed or a 1–5 craving scale).  
   - Mark each day as **"on period" (1)** or **"not on period" (0)** based on personal tracking apps like Clue or Flo.  
   - Gather order history from apps such as Getir or Yemeksepeti to confirm sweet purchases.  
   - Collect data for at least **one full menstrual cycle (≈ 28–35 days)** to ensure a balanced sample of both conditions.

2. **Data Cleaning:**  
   - Merge the two sources (consumption + period tracking) by date.  
   - Remove missing or duplicate records.  
   - Create a binary variable: `on_period` = 1 (yes) / 0 (no).  
   - Normalize sweet consumption scale if using mixed units (e.g., portions, grams).  

3. **Exploratory Data Analysis (EDA):**  
   - Compare **average sweet consumption on period days vs non-period days**.  
   - Visualize the distribution of consumption (histograms, boxplots).  

4. **Hypothesis:**  
   - My sweet consumption is higher on period days compared to non-period days.

5. **Visualization:**  
   - Boxplot comparing “on period” vs “not on period” sweet consumption.  
   - Line plot showing day-to-day variation in consumption with shaded regions marking period days.  
     

---

##  Expected Outcomes
- Determine whether sweet consumption significantly increases during period days.  
- Quantify the difference between average consumption on vs off period.

##  Dataset Summary

The final dataset consists of 81 consecutive daily observations.

Category	Count
Period days	20
Non-period days	61
Sweet consumption days	41
Non-sweet days	40

Sweet consumption is nearly perfectly balanced, whereas period days are less frequent.

##  Exploratory Data Analysis Results

The visualizations revealed that:

-Average sweet consumption on period days is only slightly higher than non-period days.

**-The distribution of sweet consumption does not show a clear separation between the two conditions.**

-Period days are scattered throughout the time series without a consistent pattern of increased sweet intake.

**-This suggests that any potential relationship between period status and sweet consumption is weak.**

##  Hypothesis Test Results

Null Hypothesis (H₀):
Mean sweet consumption on period days ≤ Mean sweet consumption on non-period days

Alternative Hypothesis (H₁):
Mean sweet consumption on period days > Mean sweet consumption on non-period days

A manual Welch’s t-test was applied.

Result:
At α = 0.05, the null hypothesis could not be rejected.
**There is no statistically significant evidence that sweet consumption is higher on period days.**

##  Machine Learning Modeling

A binary classification framework was implemented.

Feature	Target
on_period	sweets_consumed

Models used:

-Logistic Regression

-Decision Tree

-Random Forest

All models achieved similar accuracy (≈ 52%) and predicted only the majority class.

**This indicates that menstrual period status alone does not contain sufficient predictive information to reliably classify sweet consumption behavior.**

##  Final Conclusion

Although popular belief suggests that sweet cravings increase during menstruation, this data-driven analysis indicates that:
Menstrual period status alone is not a strong predictor of sweet consumption behavior.

##  Future Work

To improve predictive performance, future studies may incorporate:
-Day of week
-Emotional stress levels
-Previous day’s sweet consumption
-Rolling average consumption trends

