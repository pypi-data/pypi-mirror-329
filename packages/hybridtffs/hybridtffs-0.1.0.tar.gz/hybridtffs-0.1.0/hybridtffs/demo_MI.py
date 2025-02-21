import pandas as pd
from tffs import get_frequency_of_feature_by_percent
from sklearn.feature_selection import mutual_info_classif

file_name= "../Brain.csv"
file_path=file_name
data = df = pd.read_csv(file_path)

def get_features_by_mi_and_tffs(data, percent_tffs, number_run, n_estimators, percent_mi):
    index_TFFS_percent = get_frequency_of_feature_by_percent(df, number_run, percent_tffs, n_estimators)
    X = data.iloc[:, 1:]
    X_original = data.iloc[:, 1:]
    y = data.iloc[:, 0]
    X_new = X_original.iloc[:, index_TFFS_percent]
    total_features = data.shape[1] - 1
    num_selected_features = max(1, round(percent_mi * total_features / 100))  # Lấy 1% số lượng cột, tối thiểu 1 cột
    # Tính Mutual Information cho từng đặc trưng
    mi_scores = mutual_info_classif(X_new, y, random_state=42)
    # Chuyển MI scores thành một Pandas Series
    mi_series = pd.Series(mi_scores, index=X_new.columns)
    # Sắp xếp các đặc trưng theo độ quan trọng giảm dần
    mi_series_sorted = mi_series.sort_values(ascending=False)
    selected_features = mi_series_sorted.head(num_selected_features).index
    return selected_features



selected_features = get_features_by_mi_and_tffs(data, 5, 20, 50, 1)
print("\nTop features selected:")
print(selected_features.array)
