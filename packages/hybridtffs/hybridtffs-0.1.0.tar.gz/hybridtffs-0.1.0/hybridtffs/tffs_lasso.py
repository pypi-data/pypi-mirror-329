from sklearn.linear_model import  LogisticRegression
import pandas as pd
from sklearn.model_selection import train_test_split
from tffs import get_frequency_of_feature_by_percent
from sklearn.feature_selection import SelectFromModel
from sklearn.linear_model import LassoCV, Lasso
import numpy as np


file_name= "../Brain.csv"
file_path=file_name
data = df = pd.read_csv(file_path)

def get_features_by_lasso_and_tffs(data, percent_tffs, number_run, n_estimators, percent_forward):
    index_TFFS_percent = get_frequency_of_feature_by_percent(df, number_run, percent_tffs, n_estimators)
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
    lasso_cv = LassoCV(cv=5, random_state=42)
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

selected_features = get_features_by_lasso_and_tffs(data, 5, 20, 50, 1)
print("\nTop features selected:")
print(selected_features)
print(len(selected_features))
