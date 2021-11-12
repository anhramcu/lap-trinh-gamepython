from time import time
import pygame
pygame.font.init()
pygame.mixer.init() # gaming sound
import random
import sys
from pygame.locals import *
font = pygame.font.SysFont('arial', 40)
def terminate():
    pygame.quit()
    sys.exit()
def drawText(text, font, surface, x, y):
    TEXTCOLOR = (255, 255, 255)
    textobj = font.render(text, 1,TEXTCOLOR )
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)
def waitForPlayerToPressKey():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE: #
                    terminate()
                if event.key == K_RETURN:
                    return
IMAGE_PATH = 'imgs/'
scrrr_width=800
scrrr_height =560
GAMEOVER = False
#4 Xử lý lỗi tải hình ảnh
LOG = 'tài liệu:{}Phương pháp trong:{}Lỗi'.format(__file__,__name__)
class Map():
    #3 Lưu tên của hai bức tranh có màu sắc khác nhau
    map_names_list = [IMAGE_PATH + 'map1.png', IMAGE_PATH + 'map2.png']
    #3hởi tạo bản đồ
    def __init__(self, x, y, img_index):
        self.image = pygame.image.load(Map.map_names_list[img_index])
        self.position = (x, y)
        # Có thể trồng nó không
        self.can_grow = True
    #3 Tải bản đồ
    def load_map(self):
         MainGame.window.blit(self.image,self.position)
#4 Cây
class Plant(pygame.sprite.Sprite):
    def __init__(self):
        super(Plant, self).__init__()
        self.live=True

    # Tải hình ảnh
    def load_image(self):
        if hasattr(self, 'image') and hasattr(self, 'rect'):
            MainGame.window.blit(self.image, self.rect)
        else:
            print(LOG)
#5 Hoa hướng dương
class Sunflower(Plant):
    def __init__(self,x,y):
        super(Sunflower, self).__init__()
        self.image = pygame.image.load('imgs/sunflower.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.price = 50
        self.hp = 100
        #5 Bộ đếm thời gian
        self.time_count = 0

    #5 Tạo ra ánh sáng mặt trời
    def produce_money(self):
        self.time_count += 1
        if self.time_count == 25:
            MainGame.money += 5
            self.time_count = 0
    #5 Hướng dương được thêm vào cửa sổ
    def display_sunflower(self):
        MainGame.window.blit(self.image,self.rect)
#6 bắn đậu
class PeaShooter(Plant):
    def __init__(self,x,y):
        super(PeaShooter, self).__init__()
        # self.image 为一个 surface
        self.image = pygame.image.load('imgs/peashooter.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.price = 50
        self.hp = 200
        self.shot_count = 0

    #6 Tăng phương pháp chụp
    def shot(self):
        #6 Ghi lại xem có nên quay hay không
        should_fire = False
        for zombie in MainGame.zombie_list:
            if zombie.rect.y == self.rect.y and zombie.rect.x < 800 and zombie.rect.x > self.rect.x:
                should_fire = True
        #6 th nếu còn sống
        if self.live and should_fire:
            self.shot_count += 1
            if self.shot_count == 25:
                #6 Tạo một viên đạn dựa trên vị trí hiện tại của người bắn đậu
                peabullet = PeaBullet(self)
                #6 Lưu trữ dấu đầu dòng trong danh sách dấu đầu dòng
                MainGame.peabullet_list.append(peabullet)
                self.shot_count = 0

    #6 cách thêm game bắn đậu vào cửa sổ
    def display_peashooter(self):
        MainGame.window.blit(self.image,self.rect)

#7 Đạn hạt đậu
class PeaBullet(pygame.sprite.Sprite):
    def __init__(self,peashooter):
        self.live = True
        self.image = pygame.image.load('imgs/peabullet.png')
        self.damage = 50
        self.speed  = 10
        self.rect = self.image.get_rect()
        self.rect.x = peashooter.rect.x + 60
        self.rect.y = peashooter.rect.y + 15

    def move_bullet(self):
        #7 Di chuyển sang phải trong vùng màn hình
        if self.rect.x < scrrr_width:
            self.rect.x += self.speed
        else:
            self.live = False

    #7 va chạm của đạn và zombie
    def hit_zombie(self):
        for zombie in MainGame.zombie_list:
            if pygame.sprite.collide_rect(self,zombie):
                #Sau khi bắn trúng zombie,sửa đổi trạng thái của viên đạn
                self.live = False
                #chinh hp zombie
                zombie.hp -= self.damage
                if zombie.hp <= 0:
                    zombie.live = False
                    self.nextLevel()
    #7 đột phá
    def nextLevel(self):
        MainGame.score += 20
        MainGame.remnant_score -=20
        for i in range(1,100):
            if MainGame.score==100*i and MainGame.remnant_score==0:
                    MainGame.remnant_score=100*i
                    MainGame.shaoguan+=1
                    MainGame.produce_zombie+=50



    def display_peabullet(self):
        MainGame.window.blit(self.image,self.rect)
#9 zombie
class Zombie(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super(Zombie, self).__init__()
        self.image = pygame.image.load('imgs/zombie.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.hp = 800
        self.damage = 2
        self.speed = 1
        self.live = True
        self.stop = False
    #9 di chuyển zombie
    def move_zombie(self):
        if self.live and not self.stop:
            self.rect.x -= self.speed
            if self.rect.x < -80:
                #8 phương thức kết thúc game
                GAMEOVER=True
                MainGame().gameOver()

    #9 Xác định xem zombie có va chạm với cây không, nếu có va chạm thì gọi phương pháp tấn công cây
    def hit_plant(self):
        for plant in MainGame.plants_list:
            if pygame.sprite.collide_rect(self,plant):
                #8  Sửa đổi trạng thái di chuyển của zombie
                self.stop = True
                self.eat_plant(plant)
    #9 Zombies tấn công cây trồng
    def eat_plant(self,plant):
        #9 hp cây trồng giảm
        plant.hp -= self.damage
        #9 Sửa đổi trạng thái của cây sau khi chết và sửa đổi trạng thái của bản đồ
        if plant.hp <= 0:
            a = plant.rect.y // 80 - 1
            b = plant.rect.x // 80
            map = MainGame.map_list[a][b]
            map.can_grow = True
            plant.live = False
            #8Sửa đổi trạng thái di chuyển của zombie
            self.stop = False



    #9 Nạp zombie vào bản đồ
    def display_zombie(self):
        MainGame.window.blit(self.image,self.rect)
#1 主程序
class MainGame():
    #2 Tạo cấp độ, điểm số, điểm số còn lại, tiền
    shaoguan = 1
    score = 0
    remnant_score = 100
    money = 200
    map_points_list = []
    map_list = []
    plants_list = []
    peabullet_list = []
    zombie_list = []
    count_zombie = 0
    produce_zombie = 100
    def init_window(self):
        #1 khởi tạo mô-đun hiển thị
        pygame.display.init()
        MainGame.window = pygame.display.set_mode([scrrr_width,scrrr_height])

    #2 Bản vẽ văn bản
    def draw_text(self, content, size, color):
        pygame.font.init()
        font = pygame.font.SysFont('kaiti', size)
        text = font.render(content, True, color)
        return text

    #2 Đang tải các mẹo trợ giúp
    def load_help_text(self):
        text1 = self.draw_text('1. Nhấn nút bên trái để tạo bông hoa hướng dương 2. Nhấn nút bên phải để bắn hạt đậu', 26, (255, 0, 0))
        MainGame.window.blit(text1, (5, 5))

    #3 Khởi tạo điểm tọa độ
    def init_plant_points(self):
        for y in range(1, 7):
            points = []
            for x in range(10):
                point = (x, y)
                points.append(point)
            MainGame.map_points_list.append(points)
            print("MainGame.map_points_list", MainGame.map_points_list)

    def init_map(self):
        for points in MainGame.map_points_list:
            temp_map_list = list()
            for point in points:
                # map = None
                if (point[0] + point[1]) % 2 == 0:
                    map = Map(point[0] * 80, point[1] * 80, 0)
                else:
                    map = Map(point[0] * 80, point[1] * 80, 1)
                # Thêm các ô bản đồ vào cửa sổ
                temp_map_list.append(map)
                print("temp_map_list", temp_map_list)
            MainGame.map_list.append(temp_map_list)
        print("MainGame.map_list", MainGame.map_list)

    def load_map(self):
        for temp_map_list in MainGame.map_list:
            for map in temp_map_list:
                map.load_map()

    #6 Tăng tốc độ xử lý khởi chạy game bắn súng đậu
    def load_plants(self):
        for plant in MainGame.plants_list:
            #6 Tối ưu hóa logic xử lý của các cây hoa
            if plant.live:
                if isinstance(plant, Sunflower):
                    plant.display_sunflower()
                    plant.produce_money()
                elif isinstance(plant, PeaShooter):
                    plant.display_peashooter()
                    plant.shot()
            else:
                MainGame.plants_list.remove(plant)

    #7 Cách tải tất cả các viên đạn
    def load_peabullets(self):
        for b in MainGame.peabullet_list:
            if b.live:
                b.display_peabullet()
                b.move_bullet()
                # v1.9 đạn bắn trúng thây ma ko
                b.hit_zombie()
            else:
                MainGame.peabullet_list.remove(b)

    #8事件处理

    def deal_events(self):
        #8 Nhận tất cả các sự kiện
        eventList = pygame.event.get()
        #8 Duyệt qua danh sách các sự kiện và đánh giá
        for e in eventList:
            if e.type == pygame.QUIT:
                self.gameOver()
            elif e.type == pygame.MOUSEBUTTONDOWN:
                # print('Đã nhấn nút chuột')
                print(e.pos)

                x = e.pos[0] // 80
                y = e.pos[1] // 80
                print(x, y)
                map = MainGame.map_list[y - 1][x]
                print(map.position)
                #8 thêm phán đoán tải bản đồ và phán đoán tiền khi tạo
                if e.button == 1:
                    if map.can_grow and MainGame.money >= 50:
                        sunflower = Sunflower(map.position[0], map.position[1])
                        MainGame.plants_list.append(sunflower)
                        print('Độ dài danh sách nhà máy hiện tại:{}'.format(len(MainGame.plants_list)))
                        map.can_grow = False
                        MainGame.money -= 50
                elif e.button == 3:
                    if map.can_grow and MainGame.money >= 50:
                        peashooter = PeaShooter(map.position[0], map.position[1])
                        MainGame.plants_list.append(peashooter)
                        print('Độ dài danh sách hoa sx hiện tại:{}'.format(len(MainGame.plants_list)))
                        map.can_grow = False
                        MainGame.money -= 50

    #9 khởi tạo thây ma
    def init_zombies(self):
        for i in range(1, 7):
            dis = random.randint(1,5) * 300
            zombie = Zombie(800 + dis, i * 80)
            MainGame.zombie_list.append(zombie)

    #9Tải tất cả thây ma vào bản đồ
    def load_zombies(self):
        for zombie in MainGame.zombie_list:
            if zombie.live:
                zombie.display_zombie()
                zombie.move_zombie()
                # v2.0 phương thức để gọi liệu có va chạm với thực vật hay không
                zombie.hit_plant()
            else:
                MainGame.zombie_list.remove(zombie)
    #1 Bắt đầu trò chơi
    def start_game(self):
        #1 Cửa sổ khởi tạo
        self.init_window()
        #3 Khởi tạo tọa độ và bản đồ
        self.init_plant_points()
        self.init_map()
        #9 Gọi phương thức khởi tạo thây ma
        self.init_zombies()
        #1 Miễn là trò chơi chưa kết thúc, nó vẫn tiếp tục lặp lại
        #mở nhạc nền
        pygame.mixer.music.load('imgs/grasswalk.mp3')
        pygame.mixer.music.play(-1,0,0)
        while True:
            #1 Kết xuất nền trắng
            MainGame.window.fill((255, 255, 255))
            #2 Văn bản được hiển thị và vị trí tọa độ
            MainGame.window.blit(self.draw_text('Số tiền hiện tại $: {}'.format(MainGame.money), 26, (255, 0, 0)), (500, 40))
            MainGame.window.blit(self.draw_text(
                'level{}，score{},score man moi{}'.format(MainGame.shaoguan, MainGame.score, MainGame.remnant_score), 26,
                (255, 0, 0)), (5, 40))
            self.load_help_text()
            self.load_map()
            self.load_plants()
            self.load_peabullets()
            self.deal_events()
            self.load_zombies()
            #9 Bộ đếm tăng lên, mỗi khi đạt 100, phương thức khởi tạo thây ma được gọi
            MainGame.count_zombie += 1
            if MainGame.count_zombie == MainGame.produce_zombie:
                self.init_zombies()
                MainGame.count_zombie = 0
            pygame.time.wait(8)
            pygame.display.update()

    #10 Kết thúc chương trình
    def gameOver(self):
        windowSurface = pygame.display.set_mode((scrrr_width, scrrr_height))
        windowSurface.blit((pygame.image.load('imgs/grassland.png')),(0,0))
        drawText('score: %s' % (MainGame.score), font, windowSurface, 10, 30)
        if GAMEOVER ==True:
            MainGame.window.blit(self.draw_text('game over', 50, (255, 0, 0)), (300, 200))
            drawText('YOU HAVE BEEN KISSED BY THE ZOMMBIE', font, windowSurface, (scrrr_width / 4)- 100, (scrrr_height / 3) + 100)
        else:
            drawText('The game is stopping', font, windowSurface, (scrrr_width / 4)- 100, (scrrr_height / 3) + 100)
        drawText('Press enter to continue or escape to exit', font, windowSurface, (scrrr_width / 4) - 100, (scrrr_height / 3) + 150)
        pygame.display.update()
        pygame.mixer.music.stop()
        gameOverSound = pygame.mixer.Sound('imgs/gameover.wav')
        gameOverSound.play()
        waitForPlayerToPressKey()
if __name__ == '__main__':
    game = MainGame()
    game.start_game()
