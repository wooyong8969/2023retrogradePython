import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import animation
import numpy as np

file_path = r'DATA\mars_results.csv'
# Data: UTC / R.A.: DEG / DEC: DEF /delta: km / deldot: km/s

data = pd.read_csv(file_path, parse_dates=['Date__(UT)__HR:MN'])

# 구면 좌표를 카테시안 좌표로 변환
def polar2cart(r, theta, phi):
    # theta(R.A.)와 phi(DEC)를 라디안으로 변환
    theta = np.deg2rad(theta)
    phi = np.deg2rad(phi)
    x = r * np.cos(phi) * np.cos(theta)
    y = r * np.cos(phi) * np.sin(theta)
    z = r * np.sin(phi)
    return x, y, z

# 변환 함수 적용하여 x, y, z 좌표 계산
data['x'], data['y'], data['z'] = zip(*[polar2cart(row['delta'], row['R.A._(ICRF)'], row['DEC_(ICRF)']) for index, row in data.iterrows()])

# 그래프 생성
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
line, = ax.plot([], [], [], 'o-', markersize=2, color='gray')

ax.set_xlim([min(data['x']), max(data['x'])])
ax.set_ylim([min(data['y']), max(data['y'])])
ax.set_zlim([min(data['z']), max(data['z'])])

ax.set_xlabel('X (km)')
ax.set_ylabel('Y (km)')
ax.set_zlabel('Z (km)')
ax.set_title('Mars Orbit from Earths Perspective')

# 애니메이션 함수
def update(num, data, line):
    line.set_data(data['x'][:num], data['y'][:num])
    line.set_3d_properties(data['z'][:num])
    return line,

# 애니메이션 객체 생성 및 저장
ani = animation.FuncAnimation(fig, update, frames=len(data), fargs=(data, line), interval=1, blit=True)
ani.save('only_mars_orbit.gif', writer='imagemagick')

plt.show()