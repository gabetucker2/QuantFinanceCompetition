import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestRegressor
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib
import os

matplotlib.rcParams.update({'font.size': 8})

data = pd.read_csv('../../../TrainingData/ManualCSVs/data.csv')

data_clean = data.dropna()

features = data_clean.loc[:, ~data_clean.columns.str.startswith('target_')]
targets = data_clean.loc[:, data_clean.columns.str.startswith('target_')]

output_dir = os.path.abspath('../../../OutputData')
os.makedirs(output_dir, exist_ok=True)

pdf_files = []
for target in targets:
    current_target = data_clean[target]
    
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(features, current_target)
    
    importances = model.feature_importances_
    sorted_indices = importances.argsort()[::-1]
    
    plt.figure(figsize=(10, 6))
    sns.barplot(x=importances[sorted_indices], y=features.columns[sorted_indices])
    plt.title(f'Feature Importance for {target} using RandomForest')
    plt.xlabel('Importance Score')
    plt.ylabel('Features')
    plt.xscale('log')
    
    pdf_filename = os.path.join(output_dir, f'{target}_RandomForest_feature_importance.pdf')
    with PdfPages(pdf_filename) as pdf:
        pdf.savefig()
        plt.close()
    
    pdf_files.append(pdf_filename)

if pdf_files:
    print("PDF files created:")
    for file in pdf_files:
        print(os.path.abspath(file))
