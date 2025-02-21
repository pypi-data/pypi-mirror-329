import numpy as np
import pandas as pd
from tffs import get_frequency_of_feature_by_percent
from sklearn.feature_selection import mutual_info_classif

file_name= "../Brain.csv"
file_path=file_name
data = df = pd.read_csv(file_path)

def get_features_by_fs_and_tffs(data, percent_tffs, number_run, n_estimators, percent_fs):
    index_TFFS_percent = get_frequency_of_feature_by_percent(df, number_run, percent_tffs, n_estimators)
    X = data.iloc[:, 1:]
    X_original = data.iloc[:, 1:]
    y = data.iloc[:, 0]
    X_new = X_original.iloc[:, index_TFFS_percent]
    total_features = data.shape[1] - 1
    num_selected_features = max(1, round(percent_fs * total_features / 100))  # Lấy 1% số lượng cột, tối thiểu 1 cột
    fisher_scores = np.zeros(len(index_TFFS_percent))
    # Tính Fisher Score cho từng đặc trưng
    for i in range(len(index_TFFS_percent)):
        feature_values = X_new.iloc[:, i].values  # Lấy giá trị của cột thứ i
        num = 0  # Tử số (sự khác biệt giữa trung bình)
        den = 0  # Mẫu số (phương sai trong từng lớp)
        for label in y:
            class_values = feature_values[y == label]  # Giá trị của lớp hiện tại
            n_class = len(class_values)  # Số lượng mẫu trong lớp
            mean_class = np.mean(class_values)  # Trung bình của lớp
            var_class = np.var(class_values)  # Phương sai của lớp

            num += n_class * (mean_class - np.mean(feature_values)) ** 2
            den += n_class * var_class

        fisher_scores[i] = num / den if den != 0 else 0  # Tránh chia cho 0
    # Sắp xếp tên các đặc trưng theo Fisher Score
    sorted_indices = np.argsort(fisher_scores)[::-1]  # Sắp xếp giảm dần
    selected_features = X.columns[sorted_indices[:num_selected_features]]
    return selected_features

selected_features = get_features_by_fs_and_tffs(data, 5, 20, 50, 1)
print("\nTop features selected:")
print(selected_features)
