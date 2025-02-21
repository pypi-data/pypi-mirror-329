import numpy as np
import pandas as pd
from tffs import get_frequency_of_feature_by_percent

file_name= "../Brain.csv"
file_path=file_name
data = df = pd.read_csv(file_path)

def get_features_by_pc_and_tffs(data, percent_tffs, number_run, n_estimators, percent_pc):
    index_TFFS_percent = get_frequency_of_feature_by_percent(df, number_run, percent_tffs, n_estimators)
    X = data.iloc[:, 1:]
    X_original = data.iloc[:, 1:]
    y = data.iloc[:, 0]
    X_new = X_original.iloc[:, index_TFFS_percent]
    total_features = data.shape[1] - 1
    num_selected_features = max(1, round(percent_pc * total_features / 100))  # Lấy 1% số lượng cột, tối thiểu 1 cột
    # Tính Pearson Correlation giữa từng đặc trưng và biến mục tiêu
    correlations = []
    for column in X_new.columns:
        correlation = np.corrcoef(X_new[column], y)[0, 1]  # Tính hệ số tương quan Pearson
        correlations.append(abs(correlation))  # Lấy giá trị tuyệt đối để xếp hạng

    # Tạo DataFrame hiển thị tương quan và sắp xếp các đặc trưng
    correlation_df = pd.DataFrame({
        'Feature': X_new.columns,
        'Correlation': correlations
    }).sort_values(by='Correlation', ascending=False)

    # Lấy top N đặc trưng có tương quan cao nhất
    selected_features = correlation_df['Feature'].head(num_selected_features).tolist()
    return selected_features

selected_features = get_features_by_pc_and_tffs(data, 5, 20, 50, 1)
print("\nTop features selected:")
print(selected_features)
print(len(selected_features))
