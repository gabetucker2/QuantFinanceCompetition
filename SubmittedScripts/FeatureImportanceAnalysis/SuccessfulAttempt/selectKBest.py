import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.feature_selection import SelectKBest, f_regression
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
    
    # Perform feature selection
    selector = SelectKBest(score_func=f_regression, k='all')
    selector.fit(features, current_target)
    scores = selector.scores_

    # Sort the scores and corresponding features
    sorted_indices = scores.argsort()[::-1]  # Get the indices that would sort the array
    sorted_scores = scores[sorted_indices]
    sorted_features = features.columns[sorted_indices]

    # Plot the feature importances
    plt.figure(figsize=(10, 6))
    sns.barplot(x=sorted_scores, y=sorted_features)
    plt.title(f'Feature Importance for {target}')
    plt.xlabel('Importance Score')
    plt.ylabel('Features')
    plt.xscale('log')
    
    # Save the plot to a PDF file named after the target column
    pdf_filename = f'{target}_feature_importance.pdf'
    with PdfPages(pdf_filename) as pdf:
        pdf.savefig()
        plt.close()
    
    # Append the PDF filename to the list
    pdf_files.append(pdf_filename)

# Print out the list of PDF files created
print("PDF files created:")
for file in pdf_files:
    print(file)
