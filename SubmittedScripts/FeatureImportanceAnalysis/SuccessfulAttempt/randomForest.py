import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestRegressor
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib

# Set global font size for all plots
matplotlib.rcParams.update({'font.size': 8})

# Load the CSV file into a DataFrame
data = pd.read_csv('data.csv')  # Replace with the actual path to your CSV file

# Clean the data by removing rows with missing values
data_clean = data.dropna()

# Extract features and target columns
features = data_clean.loc[:, ~data_clean.columns.str.startswith('target_')]
targets = data_clean.loc[:, data_clean.columns.str.startswith('target_')]

# Prepare a PDF file to save all feature importance graphs
pdf_files = []
for target in targets:
    # Select the current target
    current_target = data_clean[target]
    
    # Initialize the RandomForestRegressor
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(features, current_target)
    
    # Get feature importances from the model
    importances = model.feature_importances_

    # Sort the feature importances in descending order and get the indices
    sorted_indices = importances.argsort()[::-1]
    
    # Plot the feature importances
    plt.figure(figsize=(10, 6))
    sns.barplot(x=importances[sorted_indices], y=features.columns[sorted_indices])
    plt.title(f'Feature Importance for {target} using RandomForest')
    plt.xlabel('Importance Score')
    plt.ylabel('Features')
    plt.xscale('log')
    
    # Save the plot to a PDF file named after the target column
    pdf_filename = f'{target}_RandomForest_feature_importance.pdf'
    with PdfPages(pdf_filename) as pdf:
        pdf.savefig()
        plt.close()
    
    # Append the PDF filename to the list
    pdf_files.append(pdf_filename)

# Print out the list of PDF files created
print("PDF files created:")
for file in pdf_files:
    print(file)
