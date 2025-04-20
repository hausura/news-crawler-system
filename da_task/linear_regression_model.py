import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

# 1. Đọc dữ liệu
df = pd.read_csv("da_task\labeled_train_data2.csv")  # thay bằng đường dẫn file thực tế

# 2. Chọn đặc trưng và nhãn
features = ['num_p', 'num_scripts', 'num_a', 'num_events', 'html_length']
X = df[features]
y = df['score']

# 3. Chia dữ liệu train/test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 4. Tạo và huấn luyện mô hình
model = LinearRegression()
model.fit(X_train, y_train)

# 5. Dự đoán và đánh giá mô hình
y_pred = model.predict(X_test)

mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

# 6. In kết quả
print("Hệ số hồi quy:", model.coef_)
print("Intercept:", model.intercept_)
print("Mean Squared Error:", mse)
print("R-squared:", r2)

# 7. (Tuỳ chọn) Dự đoán thử với một dòng dữ liệu
sample = pd.DataFrame([{
    'num_p': 20,
    'num_scripts': 30,
    'num_a': 60,
    'num_events': 5,
    'html_length': 250000
}])
predicted_score = model.predict(sample)
print("Dự đoán score cho mẫu thử:", predicted_score[0])
