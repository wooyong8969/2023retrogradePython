#######################################################################
### 활용: https://github.com/sarvagya2545/retrograde-simulation.git ###
#######################################################################

import pygame
import math
import imageio

# pygame 초기화
pygame.init()

# 창 초기화
WIDTH, HEIGHT = 800, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Retrograde motion Simulation")

# 사용될 색상 정의
Colors = {
    "WHITE": (255, 255, 255),
    "BLACK": (0, 0, 0),
    "YELLOW": (255, 255, 0),
    "EARTH": (100, 149, 237),
    "MARS": (188, 39, 50)
}

# 행성 데이터 정의
planets_dict = {
    "SUN": {
        "start_x": 0,
        "start_y": 0,
        "radius": 30,
        "color": Colors["YELLOW"],
        "mass": 1.989 * 10**30,
        "init_y_vel": 0,
        "init_x_vel": 0
    },
    "EARTH": {
        "start_x": -1,
        "start_y": 0,
        "radius": 16,
        "color": Colors["EARTH"],
        "mass": 5.9722 * 10**24,
        "init_y_vel": 29.78 * 1000,
        "init_x_vel": 0
    },
    "MARS": {
        "start_x": -1.5,
        "start_y": 0,
        "radius": 12,
        "color": Colors["MARS"],
        "mass": 6.4169 * 10**23,
        "init_y_vel": 24.07 * 1000,
        "init_x_vel": 0
    }
}

# 초당 프레임 수 제한
FPS = 60

# 화면 중앙 좌표
OFFSET_X, OFFSET_Y = WIDTH / 2, HEIGHT / 2

# 행성 클래스 정의
class Planet:
    AU = 1.496e+11  # 태양으로부터의 거리 (미터 단위)
    G = 6.67e-11    # 중력 상수
    SCALE = 50 / AU  # 화면 거리 스케일 (1 AU = 20픽셀)
    TIMESTEP = 3600 * 24  # 시간 단계 (1일)

    def __init__(self, planet, name) -> None:
        self.x = planet["start_x"] * self.AU
        self.y = planet["start_y"] * self.AU
        self.radius = planet["radius"]
        self.color = planet["color"]
        self.mass = planet["mass"]

        self.orbit = []  # 궤도 데이터
        self.sun = (name == "SUN")
        self.name = name

        self.x_vel = planet["init_x_vel"]
        self.y_vel = planet["init_y_vel"]

    def draw(self, win):
        x = self.x * self.SCALE + OFFSET_X
        y = self.y * self.SCALE + OFFSET_Y

        # 궤도 그리기
        if len(self.orbit) > 2:
            orbit_points = []
            for point in self.orbit:
                point_x, point_y = point
                point_x = point_x * self.SCALE + OFFSET_X
                point_y = point_y * self.SCALE + OFFSET_Y
                orbit_points.append((point_x, point_y))

            pygame.draw.lines(win, self.color, False, orbit_points, 2)
        
        # 행성 그리기
        pygame.draw.circle(win, self.color, (x, y), self.radius)

    # 중력력 계산
    def get_force(self, sun):
        sun_x, sun_y = sun.x, sun.y
        dist_x = sun_x - self.x
        dist_y = sun_y - self.y
        dist = math.sqrt(dist_y * dist_y + dist_x * dist_x)
        
        # F = G * M * m / R^2
        # 힘의 크기와 방향 계산
        magnitude = (self.G * self.mass * sun.mass) / (dist ** 2)
        angle = math.atan2(dist_y, dist_x)
        fx = math.cos(angle) * magnitude
        fy = math.sin(angle) * magnitude
        return fx, fy

    # 위치 업데이트
    def update_position(self, sun):
        fx, fy = self.get_force(sun)

        self.x_vel += fx / self.mass * self.TIMESTEP
        self.y_vel += fy / self.mass * self.TIMESTEP

        self.x += self.x_vel * self.TIMESTEP
        self.y += self.y_vel * self.TIMESTEP
        self.orbit.append((self.x, self.y))

# 지구와 화성 사이 교점 계산
def get_intersection(R, center, coor1, coor2):
    # 원점 이동
    x1, y1 = (coor1[0] - center[0]), (coor1[1] - center[1])
    x2, y2 = (coor2[0] - center[0]), (coor2[1] - center[1])

    # 두 점을 직선 방정식으로 변환: ax + by + c = 0
    A = y1 - y2
    B = x2 - x1
    C = y2 * x1 - x2 * y1

    x0 = (-1 * A * C) / (A ** 2 + B ** 2)
    y0 = (-1 * B * C) / (A ** 2 + B ** 2)
    d = (R ** 2) - ((C ** 2) / (A ** 2 + B ** 2))
    m = math.sqrt(d / (A ** 2 + B ** 2))

    ax, ay = x0 + B * m, y0 - A * m
    bx, by = x0 - B * m, y0 + A * m

    # 두 점이 직선에 대해 같은 쪽에 있는지 확인
    a1, b1, c1 = -B, A, (B * x1 - A * y1)
    if (a1 * ax + b1 * ay + c1 > 0) == (a1 * x2 + b1 * y2 + c1 > 0):
        return ax + center[0], ay + center[1]
    
    return bx + center[0], by + center[0]

# 메인 함수
def main():
    run = True
    clock = pygame.time.Clock()
    frame_count = 0

    sun = Planet(planets_dict["SUN"], "SUN")
    earth = Planet(planets_dict["EARTH"], "EARTH")
    mars = Planet(planets_dict["MARS"], "MARS")

    planets = [sun, earth, mars]

    while run:
        clock.tick(FPS)
        WIN.fill(Colors["BLACK"])
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # 행성 업데이트 및 그리기``
        for planet in planets:
            if planet != sun:
                planet.update_position(sun)
            planet.draw(WIN)

        # 지구와 화성 사이의 선 그리기
        EARTH_COOR = (earth.x * Planet.SCALE + OFFSET_X, earth.y * Planet.SCALE + OFFSET_Y)
        MARS_COOR = (mars.x * Planet.SCALE + OFFSET_X, mars.y * Planet.SCALE + OFFSET_Y)

        # 지구와 화성 사이 교점 찾기 및 표시
        RADIUS = 380
        CENTER = (OFFSET_X, OFFSET_Y)
        pygame.draw.circle(WIN, Colors["WHITE"], CENTER, RADIUS, 1)

        point = get_intersection(RADIUS, CENTER, EARTH_COOR, MARS_COOR)
        pygame.draw.circle(WIN, mars.color, point, mars.radius)
        pygame.draw.line(WIN, Colors["WHITE"], EARTH_COOR, point)

        pygame.display.update()

        # 스크린샷
        pygame.image.save(WIN, f"frame_{frame_count}.jpg")
        frame_count += 1
    
    pygame.quit()

    # gif로 결과 저장
    images = []
    for i in range(frame_count):
        filename = os.path.join('Orbit_pygame', f'frame_{i}.jpg')
        images.append(imageio.imread(filename))

    imageio.mimsave('animation.gif', images, fps=FPS)

main()
