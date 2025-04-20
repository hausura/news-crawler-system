import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Đọc dữ liệu từ file CSV
df = pd.read_csv('da_task/labeled_train_data2.csv')  # thay bằng tên file thực tế nếu khác

# Hiển thị 5 dòng đầu tiên để kiểm tra
print("Dữ liệu đầu vào:")
print(df.head())

# Tính ma trận tương quan
correlation_matrix = df.corr(numeric_only=True)

print("\nMa trận tương quan:")
print(correlation_matrix)

# Vẽ heatmap để trực quan hóa tương quan
plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f", square=True)
plt.title("Ma trận hệ số tương quan")
plt.tight_layout()
plt.show()
