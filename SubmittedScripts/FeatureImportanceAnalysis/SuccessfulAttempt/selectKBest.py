import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.feature_selection import SelectKBest, f_regression
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
    
    selector = SelectKBest(score_func=f_regression, k='all')
    selector.fit(features, current_target)
    scores = selector.scores_

    sorted_indices = scores.argsort()[::-1]
    sorted_scores = scores[sorted_indices]
    sorted_features = features.columns[sorted_indices]

    plt.figure(figsize=(10, 6))
    sns.barplot(x=sorted_scores, y=sorted_features)
    plt.title(f'Feature Importance for {target}')
    plt.xlabel('Importance Score')
    plt.ylabel('Features')
    plt.xscale('log')

    pdf_filename = os.path.join(output_dir, f'{target}_feature_importance.pdf')
    with PdfPages(pdf_filename) as pdf:
        pdf.savefig()
        plt.close()
    
    pdf_files.append(pdf_filename)

if pdf_files:
    print("PDF files created:")
    for file in pdf_files:
        print(os.path.abspath(file))
