import time
import requests
import pygame
from screens import racescreen, pausescreen, loadingscreen

#                   mGameState mSessionState mRaceState
# Loading:          1 0 0
# Waiting:          4 6 1
# Flying Start:     2 6 1
# Racing:           2 6 2
# Paused Racing:    3 6 2

pygame.init()

remote_ip = "192.168.1.69"
remote_url = "http://" + remote_ip + ":8180/crest2/v1/api"

headers = {
    "Accept-Encoding": "gzip"
}

resolution = (1280//2, 720//2)

fps = 20

screen = pygame.display.set_mode((0, 0), flags=pygame.NOFRAME)
pygame.display.set_caption("Project Cars 2")
clock = pygame.time.Clock()

race_screen = racescreen.RaceScreen(True)
pause_screen = pausescreen.PauseScreen()
loading_screen = loadingscreen.LoadingScreen()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_x or event.key == pygame.K_q:
                pygame.quit()
                exit(0)
            elif event.key == pygame.K_f:
                pygame.display.toggle_fullscreen()
                time.sleep(1)

    # Clear screen
    screen.fill((0, 0, 0))

    try:
        # TODO: Future. Put this in its own thread ti prevent it from haulting the FPS.
        req = requests.get(remote_url, headers=headers, timeout=0.2)
        data = req.json()
        if req.status_code == 200:
            states = (data['gameStates']['mGameState'], data['gameStates']['mSessionState'], data['gameStates']['mRaceState'])

            # Show race screen during flying start & racing
            if states == (2, 6, 2) or states == (2, 6, 1):
                race_screen.render_screen(data, screen)
            # Pause while flying & while racing
            elif states == (3, 6, 2) or states == (3, 6, 1):
                pause_screen.render_screen(data, screen, race_screen)
            elif states == (4, 6, 1):
                loading_screen.render_screen(data, screen)
            else:
                screen.fill((0, 200, 200))
                print("{}\t{}\t{}".format(data['gameStates']['mGameState'],
                                          data['gameStates']['mSessionState'],
                                          data['gameStates']['mRaceState']))
        elif req.status_code == 503:
            print("503 Error: {}".format(data['status']))
            time.sleep(5)
        else:
            print("Got status code: {}".format(req.status_code))
            print("\tData: {}".format(data))
        pygame.display.update()

        # print(clock.get_fps())
        clock.tick(fps)
    except (requests.ReadTimeout, requests.ConnectTimeout, requests.ConnectionError) as e:
        # screen.fill((101, 59, 124))
        pygame.display.update()
        print("Error communicating with CREST2 server.")
        print(e)
