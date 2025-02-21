from sklearn.linear_model import  LogisticRegression
import pandas as pd
from sklearn.model_selection import train_test_split
from tffs import get_frequency_of_feature_by_percent
from sklearn.feature_selection import RFE



file_name="Brain.csv"
file_path=file_name
data = df = pd.read_csv(file_path)

def get_features_by_recusive_and_tffs(data, percent_tffs, number_run, n_estimators, percent_recusive):
    index_TFFS_percent = get_frequency_of_feature_by_percent(df, number_run, percent_tffs, n_estimators)
    X = data.iloc[:, 1:]
    X_original = data.iloc[:, 1:]
    y = data.iloc[:, 0]
    X_new = X_original.iloc[:, index_TFFS_percent]
    total_features = data.shape[1] - 1
    num_selected_features = max(1, round(percent_recusive * total_features / 100))  # Lấy 1% số lượng cột, tối thiểu 1 cột

    X_train, X_test, y_train, y_test = train_test_split(X_new, y, test_size=0.2, random_state=42)

    return recursive_feature_elimination(X_train, y_train, num_selected_features)


def recursive_feature_elimination(X, y, num_features):
    if X.shape[1] <= num_features:
        return list(X.columns)

    # Khởi tạo mô hình Logistic Regression
    model = LogisticRegression(max_iter=5000, random_state=42)

    # Áp dụng Recursive Feature Elimination (RFE)
    selector = RFE(model, n_features_to_select=X.shape[1] - 1)  # Loại bỏ 1 feature mỗi lần
    selector.fit(X, y)

    # Chọn các đặc trưng còn lại sau khi loại bỏ
    selected_columns = X.columns[selector.support_]

    # Gọi đệ quy tiếp tục loại bỏ đặc trưng cho đến khi đạt số lượng mong muốn
    return recursive_feature_elimination(X[selected_columns], y, num_features)

selected_features = get_features_by_recusive_and_tffs(data, 5, 20, 50, 1)
print("\nTop features selected:")
print(selected_features)
print(len(selected_features))
