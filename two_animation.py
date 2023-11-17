import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import animation
import numpy as np

# 올바른 파일 경로 사용
mars_file_path = r'DATA\mars_results.csv'
earth_file_path = r'DATA\sun_earth_results.csv'
# Data: UTC / R.A.: DEG / DEC: DEF /delta: km / deldot: km/s

mars_data = pd.read_csv(mars_file_path)
earth_data = pd.read_csv(earth_file_path)

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
mars_data['x'], mars_data['y'], mars_data['z'] = zip(*[polar2cart(row['delta'], row['R.A._(ICRF)'], row['DEC_(ICRF)']) for index, row in mars_data.iterrows()])
earth_data['x'], earth_data['y'], earth_data['z'] = zip(*[polar2cart(row['delta'], row['R.A._(ICRF)'], row['DEC_(ICRF)']) for index, row in earth_data.iterrows()])

# 그래프 생성
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
# Mars 데이터 플롯 초기화
mars_line, = ax.plot([], [], [], 'o-', markersize=2, color='red', label='Mars')
# Earth 데이터 플롯 초기화
earth_line, = ax.plot([], [], [], 'o-', markersize=2, color='blue', label='Earth')

# 초기화 함수: 그래프의 배경을 그리는 함수
def init():
    mars_line.set_data([], [])
    mars_line.set_3d_properties([])
    
    earth_line.set_data([], [])
    earth_line.set_3d_properties([])
    
    return mars_line, earth_line

# 애니메이션 업데이트 함수
def update(num, mars_data, earth_data, mars_line, earth_line):
    mars_line.set_data(mars_data['x'][:num], mars_data['y'][:num])
    mars_line.set_3d_properties(mars_data['z'][:num])
    
    earth_line.set_data(earth_data['x'][:num], earth_data['y'][:num])
    earth_line.set_3d_properties(earth_data['z'][:num])
    
    return mars_line, earth_line

# 애니메이션 생성
ani = animation.FuncAnimation(fig, update, frames=len(mars_data), init_func=init, fargs=(mars_data, earth_data, mars_line, earth_line), interval=50, blit=False)

# 범례 추가
ax.legend()

# 축 라벨 및 제목 설정
ax.set_xlabel('X (km)')
ax.set_ylabel('Y (km)')
ax.set_zlabel('Z (km)')
ax.set_title('Mars and Earth Orbits Animation')

plt.show()