import pandas as pd
from sklearn.feature_selection import mutual_info_classif
import pandas as pd
import pandas as pd
from mlxtend.feature_selection import SequentialFeatureSelector as SFS
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.linear_model import  LogisticRegression
import pandas as pd
from sklearn.model_selection import train_test_split
from tffs import get_frequency_of_feature_by_percent
from sklearn.feature_selection import SelectFromModel
from sklearn.linear_model import LassoCV, Lasso
import numpy as np
from sklearn.feature_selection import RFE


def get_features_by_backward_and_tffs(data, percent_tffs, number_run, n_estimators, percent_forward):
    index_TFFS_percent = get_frequency_of_feature_by_percent(data, number_run, percent_tffs, n_estimators)
    X = data.iloc[:, 1:]
    X_original = data.iloc[:, 1:]
    y = data.iloc[:, 0]
    X_new = X_original.iloc[:, index_TFFS_percent]
    total_features = data.shape[1] - 1
    num_selected_features = max(1, round(percent_forward * total_features / 100))  # Lấy 1% số lượng cột, tối thiểu 1 cột

    X_train, X_test, y_train, y_test = train_test_split(X_new, y, test_size=0.2, random_state=42)
    class_counts = data.iloc[:, 0].value_counts()
    min1 = min(class_counts)
    lr = LogisticRegression(max_iter=500, random_state=42)

    sfs = SFS(
        lr,
        k_features=num_selected_features,  # Số lượng đặc trưng muốn chọn
        forward=False,  # Chọn forward selection
        floating=False,  # Không sử dụng SFFS (Sequential Forward Floating Selection)
        verbose=2,
        scoring='accuracy',  # Đánh giá bằng accuracy
        cv=min1,  # Sử dụng cross-validation
        n_jobs=-1  # Dùng tất cả CPU để tăng tốc
    )

    # 6. Huấn luyện bộ chọn đặc trưng
    sfs.fit(X_train, y_train)

    # 7. Lấy danh sách các đặc trưng được chọn
    selected_features = list(sfs.k_feature_names_)

    return selected_features

def get_features_by_fs_and_tffs(data, percent_tffs, number_run, n_estimators, percent_fs):
    index_TFFS_percent = get_frequency_of_feature_by_percent(data, number_run, percent_tffs, n_estimators)
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

def get_features_by_forward_and_tffs(data, percent_tffs, number_run, n_estimators, percent_forward):
    index_TFFS_percent = get_frequency_of_feature_by_percent(data, number_run, percent_tffs, n_estimators)
    X = data.iloc[:, 1:]
    X_original = data.iloc[:, 1:]
    y = data.iloc[:, 0]
    X_new = X_original.iloc[:, index_TFFS_percent]
    total_features = data.shape[1] - 1
    num_selected_features = max(1, round(percent_forward * total_features / 100))  # Lấy 1% số lượng cột, tối thiểu 1 cột

    X_train, X_test, y_train, y_test = train_test_split(X_new, y, test_size=0.2, random_state=42)
    class_counts = data.iloc[:, 0].value_counts()
    min1 = min(class_counts)
    lr = LogisticRegression(max_iter=500, random_state=42)
    # max = data.shape[0]
    # print(max)
    sfs = SFS(
        lr,
        k_features=num_selected_features,  # Số lượng đặc trưng muốn chọn
        forward=True,  # Chọn forward selection
        floating=False,  # Không sử dụng SFFS (Sequential Forward Floating Selection)
        verbose=2,
        scoring='accuracy',  # Đánh giá bằng accuracy
        cv=min1,  # Sử dụng cross-validation
        n_jobs=-1  # Dùng tất cả CPU để tăng tốc
    )

    # 6. Huấn luyện bộ chọn đặc trưng
    sfs.fit(X_train, y_train)

    # 7. Lấy danh sách các đặc trưng được chọn
    selected_features = list(sfs.k_feature_names_)

    return selected_features

def get_features_by_mi_and_tffs(data, percent_tffs, number_run, n_estimators, percent_mi):
    index_TFFS_percent = get_frequency_of_feature_by_percent(data, number_run, percent_tffs, n_estimators)
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

def get_features_by_pc_and_tffs(data, percent_tffs, number_run, n_estimators, percent_pc):
    index_TFFS_percent = get_frequency_of_feature_by_percent(data, number_run, percent_tffs, n_estimators)
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

def get_features_by_lasso_and_tffs(data, percent_tffs, number_run, n_estimators, percent_forward):
    index_TFFS_percent = get_frequency_of_feature_by_percent(data, number_run, percent_tffs, n_estimators)
    X = data.iloc[:, 1:]
    X_original = data.iloc[:, 1:]
    y = data.iloc[:, 0]
    X_new = X_original.iloc[:, index_TFFS_percent]
    total_features = data.shape[1] - 1
    num_selected_features = max(1, round(percent_forward * total_features / 100))  # Lấy 1% số lượng cột, tối thiểu 1 cột

    X_train, X_test, y_train, y_test = train_test_split(X_new, y, test_size=0.2, random_state=42)

    lasso = LogisticRegression(penalty='l1', solver='liblinear', max_iter=500, C=0.01, random_state=42)

    lasso.fit(X_train, y_train)

    selector = SelectFromModel(lasso, prefit=True)
    X_train_selected = selector.transform(X_train)
    X_test_selected = selector.transform(X_test)
    max_iter = 100  # Số lần thử để điều chỉnh alpha

    # Tìm alpha tốt nhất bằng LassoCV
    class_counts = data.iloc[:, 0].value_counts()
    min1 = min(class_counts)
    lasso_cv = LassoCV(cv=min1, random_state=42)
    lasso_cv.fit(X_train, y_train)
    best_alpha = lasso_cv.alpha_  # Giá trị alpha ban đầu từ LassoCV

    # Điều chỉnh alpha để đạt đúng số lượng đặc trưng mong muốn
    for _ in range(max_iter):
        lasso = Lasso(alpha=best_alpha, random_state=42)
        lasso.fit(X_train, y_train)
        selected_features = np.where(lasso.coef_ != 0)[0]

        if len(selected_features)==num_selected_features:
            break  # Dừng nếu số đặc trưng gần với mong muốn

        # Điều chỉnh alpha (giảm alpha nếu chọn quá ít đặc trưng, tăng nếu chọn quá nhiều)
        if len(selected_features) > num_selected_features:
            best_alpha *= 1.1  # Giảm độ phạt (chọn nhiều đặc trưng hơn)
        else:
            best_alpha *= 0.9  # Tăng độ phạt (giảm số đặc trưng)
    feature_names = X_new.columns.tolist();
    selected_features_name = [feature_names[i] for i in selected_features if i < len(feature_names)]
    return selected_features_name

def get_features_by_recusive_and_tffs(data, percent_tffs, number_run, n_estimators, percent_recusive):
    index_TFFS_percent = get_frequency_of_feature_by_percent(data, number_run, percent_tffs, n_estimators)
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