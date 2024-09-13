import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

df = pd.read_csv('data.csv')

encoder = OneHotEncoder(sparse=False)
categorical_features = ['Customer_Segment', 'Subscription_Tier']
encoded_features = encoder.fit_transform(df[categorical_features])
encoded_df = pd.DataFrame(encoded_features, columns=encoder.get_feature_names_out(categorical_features))

df = pd.concat([df.drop(categorical_features, axis=1), encoded_df], axis=1)

scaler = StandardScaler()
numerical_features = ['Spending_History', 'Num_Products_Bought', 'Avg_Price_Products', 'Frequency_Purchases']
df[numerical_features] = scaler.fit_transform(df[numerical_features])

X = df.drop(columns=['Upgrade_in_6_Months'])
y = df['Upgrade_in_6_Months']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

y_pred_proba = model.predict_proba(X_test)[:, 1]

accuracy = accuracy_score(y_test, y_pred_proba > 0.5)
print(f'Accuracy: {accuracy * 100:.2f}%')

print("\nClassification Report:")
print(classification_report(y_test, y_pred_proba > 0.5))

print("Sample of predicted upgrade probabilities:", y_pred_proba[:10])
print("Sample of actual upgrades (0: No, 1: Yes):", y_test.values[:10])

feature_importance = pd.DataFrame({'feature': X.columns, 'importance': model.feature_importances_})
feature_importance = feature_importance.sort_values('importance', ascending=False)
print("\nTop 5 most important features:")
print(feature_importance.head())

def predict_upgrade_probability(business_data):
    # Ensure business_data has the same features as the training data
    business_df = pd.DataFrame([business_data])
    
    # Encode categorical features
    encoded_business = encoder.transform(business_df[categorical_features])
    encoded_business_df = pd.DataFrame(encoded_business, columns=encoder.get_feature_names_out(categorical_features))
    
    # Combine encoded features with numerical features
    business_features = pd.concat([business_df[numerical_features], encoded_business_df], axis=1)
    
    # Scale numerical features
    business_features[numerical_features] = scaler.transform(business_features[numerical_features])
    
    # Predict probability
    upgrade_probability = model.predict_proba(business_features)[0, 1]
    
    return upgrade_probability * 100

# Example usage:
business_1 = {
    'Spending_History': 15000,
    'Num_Products_Bought': 50,
    'Avg_Price_Products': 300,
    'Frequency_Purchases': 6,
    'Customer_Segment': 'Medium',
    'Subscription_Tier': 'Standard'
}

richbusiness = {
    'Spending_History': 50000,
    'Num_Products_Bought': 200,
    'Avg_Price_Products': 500,
    'Frequency_Purchases': 15,
    'Customer_Segment': 'Large',
    'Subscription_Tier': 'Standard'
}

upgrade_probability = predict_upgrade_probability(business_1)
upgrade_probability_2 = predict_upgrade_probability(richbusiness)
print(f"\nProbability of the example business upgrading in the next 6 months: {upgrade_probability:.2f}%")
print(f"\nProbability of the rich business upgrading in the next 6 months: {upgrade_probability_2:.2f}%")
