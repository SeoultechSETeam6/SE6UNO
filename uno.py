from scene.main import Main
from controller import game_view
import pygame
import sys

if __name__ == '__main__':
    # 해상도 변경 이벤트 발생 시 game_view.resolution_changed = True가 되고,
    # 메인 화면 Scene을 닫으므로, 새로 만든 메인 화면 Scene 객체를 생성하여 다시 실행
    while game_view.resolution_changed:
        game_view.resolution_changed = not game_view.resolution_changed
        main = Main()
        main.run()

    # 해상도 변경 이벤트 발생하지 않았을 경우 메인 화면 Scene를 닫은 후 프로그램 종료
    pygame.quit()
    sys.exit()
