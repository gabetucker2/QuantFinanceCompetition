# SCRIPTS
import datasets
import functions_modelBased
import functions_classBased

# STATIC
DATASET = datasets.dataset_high
ANALYSIS_FUNCTION = functions_modelBased.modelBased_randomForest
OUTPUT_NAME = "importanceGraph"

OUTPUT_FOLDER = "graphs"
SHOW_FEATURE_COUNT = -1 # -1 means all features
