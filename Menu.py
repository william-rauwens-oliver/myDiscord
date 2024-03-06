import pygame
import cv2
import pygame_gui
import subprocess

class VideoPlayerBase:
    def __init__(self):
        pygame.init()

        self.window_size = (1283, 762)
        self.window = pygame.display.set_mode(self.window_size)
        self.ui_manager = pygame_gui.UIManager(self.window_size)

        self.video_path = "Data/img-son23/geek.mp4"
        self.cap = cv2.VideoCapture(self.video_path)

        self.video_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.video_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        self.playing = True
        self.play_video = True
        self.video_finished = False

        pygame.mixer.music.load("Data/img-son23/music.mp3")
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(1)

    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
            self.ui_manager.process_events(event)

    def update_ui(self, delta_time):
        self.ui_manager.update(delta_time)

    def display_frame(self, frame):
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, self.window_size)
        frame_surface = pygame.image.frombuffer(frame.tobytes(), self.window_size, 'RGB')
        self.window.blit(frame_surface, (0, 0))

    def release_resources(self):
        self.cap.release()
        cv2.destroyAllWindows()
        pygame.quit()

    def play(self):
        clock = pygame.time.Clock()

        while self.playing:
            delta_time = clock.tick(60) / 1000.0

            self.process_events()

            self.update_ui(delta_time)

            if self.play_video and not self.video_finished:
                ret, frame = self.cap.read()
                if not ret:
                    self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                    ret, frame = self.cap.read()
                    self.video_finished = True

                self.display_frame(frame)

            self.update_ui(delta_time)

            pygame.display.update()

            if self.video_finished:
                self.playing = False

        self.release_resources()

class VideoPlayer(VideoPlayerBase):
    def __init__(self):
        super().__init__()

    def run(self):
        self.play()

        subprocess.run(["python", "Messages.py"])

if __name__ == "__main__":
    player = VideoPlayer()
    player.run()