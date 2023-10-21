import random
import os
from PIL import Image, ImageDraw

def generate_map(room_width, room_height, num_structures, padding):
    # 큰 직사각형의 크기 설정
    rect_width = random.randint(300, 700)
    rect_height = random.randint(300, 700)
    rect_x = 100
    rect_y = 100

    # 큰 직사각형 생성
    room_image = Image.new('RGB', (room_width, room_height), color='white')
    room_draw = ImageDraw.Draw(room_image)

    # 큰 직사각형의 굵은 선 그리기
    room_draw.rectangle([(rect_x, rect_y), (rect_x + rect_width, rect_y + rect_height)], outline='black', width=8)

    structures = []
    for _ in range(num_structures):
        structure_type = random.choice(['rectangle', 'circle'])  # 구조물 유형 선택

        if structure_type == 'rectangle':
            structure_width = random.randint(40, 50)  # 구조물 너비 (랜덤)
            structure_height = random.randint(40, 50)  # 구조물 높이 (랜덤)

            structure_x = random.randint(rect_x + padding, rect_x + rect_width - padding - structure_width)  # 구조물 x 좌표 (랜덤)
            structure_y = random.randint(rect_y + padding, rect_y + rect_height - padding - structure_height)  # 구조물 y 좌표 (랜덤)

            room_draw.rectangle((structure_x, structure_y, structure_x + structure_width, structure_y + structure_height),
                                fill='black')
            structures.append((structure_type, structure_x, structure_y, structure_width, structure_height))
        elif structure_type == 'circle':
            structure_radius = random.randint(5, 25)  # 구조물 반지름 (랜덤)

            # 원의 중심 좌표를 구하기 위해 구조물 반지름과 패딩을 고려하여 좌표 범위를 설정
            min_x = rect_x + padding + structure_radius
            max_x = rect_x + rect_width - padding - structure_radius
            min_y = rect_y + padding + structure_radius
            max_y = rect_y + rect_height - padding - structure_radius

            structure_center_x = random.randint(min_x, max_x)  # 구조물 중심 x 좌표 (랜덤)
            structure_center_y = random.randint(min_y, max_y)  # 구조물 중심 y 좌표 (랜덤)

            room_draw.ellipse((structure_center_x - structure_radius, structure_center_y - structure_radius,
                               structure_center_x + structure_radius, structure_center_y + structure_radius),
                              fill='black')
            structures.append((structure_type, structure_center_x, structure_center_y, structure_radius))

    return room_image, structures

def save_image(image, filename):
    image.save(filename, 'PNG')

def setFilePath(filePath):
    os.chdir(filePath)

def create(width=800, height=800, num_structures=15, padding=10):
    # 방 크기, 구조물 개수, 벽과의 간격

    # 방 생성, 구조물 배치
    room_image, structures = generate_map(width, height, num_structures, padding)

    # 이미지 저장
    save_image(room_image, 'room_map.png')

if __name__ == "__main__":
    setFilePath( os.path.dirname(os.path.abspath(__file__)) )
    create()