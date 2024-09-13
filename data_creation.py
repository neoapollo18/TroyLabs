import pandas as pd
import numpy as np

# Setting the random seed for reproducibility
np.random.seed(42)

# Parameters for the dataset
n_samples = 1000  # Number of rows

# Define more correlated logic for upgrades
def generate_spending_history_with_trend(segment, tier):
    if tier == 'Basic':
        return np.random.randint(5000, 10000) if segment == 'Small' else np.random.randint(8000, 12000)
    elif tier == 'Standard':
        return np.random.randint(10000, 20000) if segment == 'Medium' else np.random.randint(15000, 25000)
    else:  # Premium
        return np.random.randint(25000, 50000)

# Updated logic for determining upgrades
def determine_upgrade_with_trend(tier, spend, freq, avg_price):
    # Companies in the Basic tier that increase spending, frequency, and product price are likely to upgrade
    if tier == 'Basic' and spend > 10000 and freq > 5:
        return 1
    # Companies in the Standard tier may upgrade if they show strong growth in spending and purchases
    elif tier == 'Standard' and spend > 20000 and freq > 8 and avg_price > 250:
        return 1
    # Premium tier companies usually don't upgrade but stay at their tier
    else:
        return 0

# Recreate the dataset with more correlation
spending_history = []
num_products_bought = []
avg_price_products = []
frequency_purchases = []
subscription_tier = []
upgrade_in_six_months = []

for i in range(n_samples):
    # Assign customer segment and initial subscription tier
    segment = np.random.choice(['Small', 'Medium', 'Large'])
    tier = np.random.choice(['Basic', 'Standard', 'Premium'], p=[0.5, 0.3, 0.2])  # Majority in Basic tier
    
    # Generate spending history and other factors based on tier and segment
    spend = generate_spending_history_with_trend(segment, tier)
    num_products = np.random.randint(5, 50) if tier == 'Basic' else np.random.randint(50, 200)
    avg_price = np.random.randint(50, 200) if tier == 'Basic' else np.random.randint(200, 500)
    freq = np.random.randint(1, 5) if tier == 'Basic' else np.random.randint(5, 15)
    
    # Determine if the company will upgrade
    upgrade = determine_upgrade_with_trend(tier, spend, freq, avg_price)
    
    # Append to the lists
    spending_history.append(spend)
    num_products_bought.append(num_products)
    avg_price_products.append(avg_price)
    frequency_purchases.append(freq)
    subscription_tier.append(tier)
    upgrade_in_six_months.append(upgrade)

# Create the DataFrame
data = {
    'Spending_History': spending_history,
    'Num_Products_Bought': num_products_bought,
    'Avg_Price_Products': avg_price_products,
    'Frequency_Purchases': frequency_purchases,
    'Customer_Segment': np.random.choice(['Small', 'Medium', 'Large'], size=n_samples),
    'Subscription_Tier': subscription_tier,
    'Upgrade_in_6_Months': upgrade_in_six_months
}

df_correlated = pd.DataFrame(data)

# Save the dataset with more correlations
csv_file_path = 'data.csv'
df_correlated.to_csv(csv_file_path, index=False)

csv_file_path
