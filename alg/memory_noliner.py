import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import matplotlib.pyplot as plt

# ====== 1. 生成带记忆非线性通道 ======
np.random.seed(42)
N = 10000
M = 5
x = np.random.randn(N)

y = np.zeros_like(x)
for n in range(M, N):
    y[n] = (
        0.8 * x[n] +
        0.4 * x[n-1]**2 -
        0.3 * x[n-2]*x[n-3] +
        0.15*np.sin(2*np.pi*x[n-1])
    )
y += 0.02 * np.random.randn(N)

# ====== 2. 构建序列输入 ======
window = 32
X_seq, Y_seq = [], []
for n in range(M, N - window):
    X_seq.append(y[n:n+window])
    Y_seq.append(x[n+window])
X_seq = torch.tensor(np.array(X_seq), dtype=torch.float32).unsqueeze(1)
Y_seq = torch.tensor(np.array(Y_seq), dtype=torch.float32).unsqueeze(1)

# ====== 3. 改进CNN模型 ======
class DeepResidualCNN(nn.Module):
    def __init__(self, window):
        super().__init__()
        self.conv1 = nn.Conv1d(1, 32, 5, padding=2)
        self.conv2 = nn.Conv1d(32, 64, 5, padding=2)
        self.proj1 = nn.Conv1d(32, 64, 1)  # 1x1 conv for residual projection
        self.conv3 = nn.Conv1d(64, 64, 5, padding=2)
        self.conv4 = nn.Conv1d(64, 32, 5, padding=2)
        self.proj2 = nn.Conv1d(64, 32, 1)  # 1x1 conv for second residual projection
        self.conv5 = nn.Conv1d(32, 16, 3, padding=1)
        self.fc = nn.Linear(16*window, 1)
        self.relu = nn.ReLU()
        self.dropout = nn.Dropout(0.2)
        
    def forward(self, x):
        # 残差块1
        r = self.relu(self.conv1(x))
        x = self.relu(self.conv2(r))
        r_proj = self.proj1(r)
        x = x + r_proj  # 残差连接
        
        # 残差块2
        r2 = self.relu(self.conv3(x))
        x = self.relu(self.conv4(r2))
        r2_proj = self.proj2(r2)
        x = x + r2_proj
        
        x = self.dropout(self.relu(self.conv5(x)))
        x = x.view(x.size(0), -1)
        x = self.fc(x)
        return x

model = DeepResidualCNN(window)
criterion = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=1e-3)

# ====== 4. 训练 ======
num_epochs = 50
for epoch in range(num_epochs):
    optimizer.zero_grad()
    output = model(X_seq)
    loss = criterion(output, Y_seq)
    loss.backward()
    optimizer.step()
    if epoch % 5 == 0:
        print(f"Epoch {epoch}/{num_epochs}  Loss = {loss.item():.6e}")

# ====== 5. 测试 ======
with torch.no_grad():
    x_pred = model(X_seq).squeeze().numpy()

# ====== 6. 可视化结果 ======
plt.figure(figsize=(10,5))
plt.plot(x[M+window:], 'k', alpha=0.6, label='Original Linear Signal')
plt.plot(y[M+window:], 'r', alpha=0.4, label='Distorted Signal')
plt.plot(x_pred, 'b', alpha=0.7, label='Deep CNN Compensation')
plt.legend()
plt.title('Deep CNN Compensation with Memory Effect')
plt.xlabel('Sample Index')
plt.ylabel('Amplitude')
plt.show()