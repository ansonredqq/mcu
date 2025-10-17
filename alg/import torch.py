import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import matplotlib.pyplot as plt

# ====== 1. 模拟非线性系统 ======
np.random.seed(42)
N = 10000
x = np.random.randn(N, 1)
y = x + 0.4 * x**3 + 0.2 * np.sin(2 * np.pi * x)  # 模拟非线性响应
x_train = torch.tensor(x, dtype=torch.float32)
y_train = torch.tensor(y, dtype=torch.float32)

# ====== 2. 定义一维CNN网络 ======
class NonlinearCompensator(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv1d(1, 8, kernel_size=5, padding=2)
        self.conv2 = nn.Conv1d(8, 16, kernel_size=5, padding=2)
        self.fc = nn.Linear(16, 1)
        self.relu = nn.ReLU()

    def forward(self, x):
        x = self.conv1(x)
        x = self.relu(x)
        x = self.conv2(x)
        x = self.relu(x)
        x = x.mean(dim=-1)   # 全局平均池化
        x = self.fc(x)
        return x

model = NonlinearCompensator()

# ====== 3. 训练网络 ======
criterion = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=1e-3)

x_train_cnn = x_train.unsqueeze(1).permute(0, 2, 1)  # [N, 1, 1]
y_train_cnn = y_train.unsqueeze(1).permute(0, 2, 1)  # [N, 1, 1]

for epoch in range(2000):
    optimizer.zero_grad()
    output = model(y_train_cnn)  # 输入非线性后的信号
    loss = criterion(output.squeeze(), x_train.squeeze())  # 输出拟合原始输入
    loss.backward()
    optimizer.step()
    if epoch % 200 == 0:
        print(f"Epoch {epoch}, Loss = {loss.item():.6f}")

with torch.no_grad():
    y_pred = model(y_train_cnn).squeeze().numpy()

plt.figure(figsize=(8,5))
plt.plot(x, y, 'r.', alpha=0.3, label='Nonlinear Output')
plt.plot(x, y_pred, 'b.', alpha=0.3, label='CNN Compensated')
plt.xlabel('Input Signal')
plt.ylabel('Output')
plt.legend()
plt.title('CNN-based Nonlinear Compensation')
plt.show()