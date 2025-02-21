from sklearn.linear_model import  LogisticRegression
import pandas as pd
from sklearn.model_selection import train_test_split
from tffs import get_frequency_of_feature_by_percent
from mlxtend.feature_selection import SequentialFeatureSelector as SFS


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

    X_train, X_test, y_train, y_test = train_test_split(X_new, y, test_size=0.2, random_state=42)

    lr = LogisticRegression(max_iter=500, random_state=42)

    sfs = SFS(
        lr,
        k_features=num_selected_features,  # Số lượng đặc trưng muốn chọn
        forward=True,  # Chọn forward selection
        floating=False,  # Không sử dụng SFFS (Sequential Forward Floating Selection)
        verbose=2,
        scoring='accuracy',  # Đánh giá bằng accuracy
        cv=5,  # Sử dụng cross-validation
        n_jobs=-1  # Dùng tất cả CPU để tăng tốc
    )

    # 6. Huấn luyện bộ chọn đặc trưng
    sfs.fit(X_train, y_train)

    # 7. Lấy danh sách các đặc trưng được chọn
    selected_features = list(sfs.k_feature_names_)

    return selected_features

selected_features = get_features_by_forward_and_tffs(data, 5, 20, 50, 1)
print("\nTop features selected:")
print(selected_features)
print(len(selected_features))
