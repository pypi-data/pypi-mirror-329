from sklearn.linear_model import LinearRegression
import numpy as np
import pandas as pd
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from tffs import get_frequency_of_feature_by_percent

file_name= "../Brain.csv"
file_path=file_name
data = df = pd.read_csv(file_path)

def get_features_by_forward_and_tffs(data, percent_tffs, number_run, n_estimators, percent_forward):
    index_TFFS_percent = get_frequency_of_feature_by_percent(df, number_run, percent_tffs, n_estimators)
    X = data.iloc[:, 1:]
    X_original = data.iloc[:, 1:]
    y = data.iloc[:, 0]
    X_new = X_original.iloc[:, index_TFFS_percent]
    total_features = data.shape[1] - 1
    num_selected_features = max(1, round(percent_forward * total_features / 100))  # Lấy 1% số lượng cột, tối thiểu 1 cột

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Danh sách đặc trưng
    remaining_features = list(X.columns)  # Đặc trưng chưa được chọn
    selected_features = []  # Đặc trưng đã chọn

    # Vòng lặp để chọn đúng số lượng đặc trưng mong muốn
    for _ in range(num_selected_features):
        scores = []  # Lưu điểm của từng đặc trưng khi thử thêm vào
        for feature in remaining_features:
            # Thử thêm từng đặc trưng vào danh sách đã chọn
            current_features = selected_features + [feature]
            model = LinearRegression()
            model.fit(X_train[current_features], y_train)
            y_pred = model.predict(X_test[current_features])
            score = mean_squared_error(y_test, y_pred)
            scores.append((feature, score))

        # Chọn đặc trưng có lỗi thấp nhất
        scores.sort(key=lambda x: x[1])  # Sắp xếp theo MSE tăng dần
        best_feature = scores[0][0]

        # Thêm đặc trưng vào danh sách đã chọn và loại bỏ khỏi danh sách còn lại
        selected_features.append(best_feature)
        remaining_features.remove(best_feature)

        # print(f"Chọn đặc trưng: {best_feature}, MSE: {scores[0][1]}")

    return selected_features

selected_features = get_features_by_forward_and_tffs(data, 5, 20, 50, 1)
print("\nTop features selected:")
print(selected_features)
print(len(selected_features))
