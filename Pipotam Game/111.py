import pygame
import os
import math
import random
import json

WIDTH, HEIGHT = 480, 800
FPS = 60
SHOWER_FADEOUT_MS = 700

# Примерная «живая» зона тела на исходном спрайте Пипотама (пиксели арта).
PIPETAM_BODY_REF_W = 550
PIPETAM_BODY_REF_H = 880

UI_TOP_PANEL_H = 76
UI_BOTTOM_PANEL_H = 110

HUD_COLUMNS = [
    ("1", "Кухня", "Сытость", "hunger", (220, 60, 60)),
    ("2", "Ванная", "Чистота", "cleanliness", (80, 200, 120)),
    ("3", "Туалет", "Бак", "bak", (200, 90, 220)),
    ("4", "Сон", "Сон", "sleep", (80, 160, 240)),
    ("5", "Игра", "Счастье", "happiness", (240, 210, 60)),
]


class Pet:

    def __init__(self, name):

        self.name = name

        self.hunger = 100
        self.cleanliness = 100
        self.sleep = 50
        self.happiness = 50
        self.bak = 50
        self.level = 1
        self.xp = 0
        self.xp_to_next = 100

    def add_xp(self, amount):
        if amount <= 0:
            return

        self.xp += float(amount)

        while self.xp >= self.xp_to_next:
            self.xp -= self.xp_to_next
            self.level += 1
            self.xp_to_next = int(self.xp_to_next * 1.25)

    def xp_progress(self):
        return max(0.0, min(1.0, self.xp / self.xp_to_next))

    def apply_progress(self, attr, delta):
        old_val = float(getattr(self, attr))
        new_val = max(0.0, min(100.0, old_val + float(delta)))
        setattr(self, attr, new_val)
        actual_delta = new_val - old_val

        # XP is awarded only for real useful progress:
        # +stats for hunger/cleanliness/sleep/happiness, -bak for toilet.
        if attr == "bak":
            if actual_delta < 0:
                self.add_xp(-actual_delta)
        else:
            if actual_delta > 0:
                self.add_xp(actual_delta)

        return actual_delta

    def sleep_action(self):
        self.apply_progress("sleep", 0.03)

    def update(self):

        self.hunger -= 0.006
        self.cleanliness -= 0.008
        self.sleep -= 0.003
        self.happiness -= 0.003
        self.bak += 0.002

        self.hunger = max(0, min(100, self.hunger))
        self.cleanliness = max(0, min(100, self.cleanliness))
        self.sleep = max(0, min(100, self.sleep))
        self.happiness = max(0, min(100, self.happiness))
        self.bak = max(0, min(100, self.bak))


class UI:

    def __init__(self):

        self.small_font = pygame.font.SysFont("Arial", 14)
        self.meter_value_font = pygame.font.SysFont("Arial", 20)
        self.button_font = pygame.font.SysFont("Arial", 16, bold=True)

        self.buttons = []
        self._xp_smooth_xp = None

    def _draw_ring_meter(
        self,
        screen,
        cx,
        cy,
        radius,
        thickness,
        label,
        value,
        color,
        label_top_y
    ):

        value = max(0, min(100, float(value)))

        pygame.draw.circle(
            screen,
            (60, 60, 60),
            (cx, cy),
            radius,
            thickness
        )

        start_ang = -math.pi / 2

        if value >= 99.5:

            pygame.draw.circle(
                screen,
                color,
                (cx, cy),
                radius,
                thickness
            )

        elif value > 0:

            end_ang = start_ang + 2 * math.pi * (value / 100)

            rect = pygame.Rect(
                cx - radius,
                cy - radius,
                radius * 2,
                radius * 2
            )

            pygame.draw.arc(
                screen,
                color,
                rect,
                start_ang,
                end_ang,
                thickness
            )

        val_text = self.meter_value_font.render(
            str(int(value)),
            True,
            (255, 255, 255)
        )

        screen.blit(
            val_text,
            (
                cx - val_text.get_width() // 2,
                cy - val_text.get_height() // 2,
            ),
        )

        label_text = self.small_font.render(
            label,
            True,
            (235, 235, 235)
        )

        screen.blit(
            label_text,
            (
                cx - label_text.get_width() // 2,
                label_top_y,
            ),
        )

    def _draw_panel(self, screen, x, y, w, h, alpha=140):

        panel = pygame.Surface((w, h), pygame.SRCALPHA)
        panel.fill((0, 0, 0, alpha))

        screen.blit(panel, (x, y))

    def draw_top(self, screen, pet,game):

        self._draw_panel(
            screen,
            0,
            0,
            WIDTH,
            UI_TOP_PANEL_H,
            alpha=140
        )

        hud_margin = 10
        n = len(HUD_COLUMNS)

        cell_w = (WIDTH - 20) / n

        centers_x = [
            hud_margin + (i + 0.5) * cell_w
            for i in range(n)
        ]

        radius = 18
        thickness = 6

        label_top_y = 52


        cy = 28

        for i, (_key, _room, stat_label, attr, color) in enumerate(HUD_COLUMNS):

            value = getattr(pet, attr)

            cx = int(centers_x[i])

            self._draw_ring_meter(
                screen,
                cx,
                cy,
                radius,
                thickness,
                stat_label,
                value,
                color,
                label_top_y
            )

        mute_button = pygame.Rect(
            WIDTH - 68,
            78,
            52,
            52
        )

        if game.sound_muted:

            pygame.draw.circle(
                screen,
                (190, 60, 60),
                mute_button.center,
                28
            )

            screen.blit(
                game.sound_off_img,
                mute_button.topleft
            )

        else:

            pygame.draw.circle(
                screen,
                (60, 190, 90),
                mute_button.center,
                28
            )

            screen.blit(
                game.sound_on_img,
                mute_button.topleft
            )

    def draw_bottom(self, screen, current_room,pet):

        self.buttons.clear()

        bottom_y = HEIGHT - UI_BOTTOM_PANEL_H

        self._draw_panel(
            screen,
            0,
            bottom_y,
            WIDTH,
            UI_BOTTOM_PANEL_H,
            alpha=140
        )

        xp_bar_margin = 18
        xp_bar_w = WIDTH - xp_bar_margin * 2
        xp_bar_h = 18
        xp_bar_x = xp_bar_margin
        xp_bar_y = bottom_y -8

        pygame.draw.rect(
            screen,
            (40, 40, 52),
            (xp_bar_x, xp_bar_y, xp_bar_w, xp_bar_h),
            border_radius=9
        )

        pygame.draw.rect(
            screen,
            (110, 110, 130),
            (xp_bar_x, xp_bar_y, xp_bar_w, xp_bar_h),
            2,
            border_radius=9
        )

        self.xp_bar_rect = pygame.Rect(xp_bar_x, xp_bar_y, xp_bar_w, xp_bar_h)

        # Кнопка имени под XP
        rename_button = pygame.Rect(
            xp_bar_x,
            xp_bar_y + 18,
            xp_bar_w,
            24
        )

        pygame.draw.rect(
            screen,
            (65, 65, 82),
            rename_button,
            border_radius=8
        )

        rename_text = self.small_font.render(
            f"Имя: {current_room if False else ''}",
            True,
            (255, 255, 255)
        )

        rename_text = self.small_font.render(
            f"{pet.name}",
            True,
            (255, 255, 255)
        )

        screen.blit(
            rename_text,
            (
                rename_button.centerx
                - rename_text.get_width() // 2,

                rename_button.centery
                - rename_text.get_height() // 2
            )
        )
        button_w = 78
        button_h = 52
        gap = 10

        total_w = button_w * 5 + gap * 4

        start_x = (WIDTH - total_w) // 2

        for i, (key, room, _stat, attr, color) in enumerate(HUD_COLUMNS):

            x = start_x + i * (button_w + gap)
            y = bottom_y + 33

            rect = pygame.Rect(x, y, button_w, button_h)

            self.buttons.append((rect, attr))

            if current_room == attr:
                fill = color
            else:
                fill = (50, 50, 60)

            pygame.draw.rect(
                screen,
                fill,
                rect,
                border_radius=12
            )

            pygame.draw.rect(
                screen,
                (255, 255, 255),
                rect,
                3,
                border_radius=12
            )

            key_text = self.button_font.render(
                key,
                True,
                (255, 255, 255)
            )

            room_text = self.small_font.render(
                room,
                True,
                (255, 255, 255)
            )

            screen.blit(
                key_text,
                (
                    x + (button_w - key_text.get_width()) // 2,
                    y + 4
                )
            )

            screen.blit(
                room_text,
                (
                    x + (button_w - room_text.get_width()) // 2,
                    y + 28
                )
            )

    def update_xp_display(self, pet, dt):
        if self._xp_smooth_xp is None:
            self._xp_smooth_xp = float(pet.xp)
            return

        if dt <= 0:
            dt = 1.0 / FPS

        k = 14.0
        t = min(1.0, k * dt)
        self._xp_smooth_xp += (float(pet.xp) - self._xp_smooth_xp) * t

    def draw_xp(self, screen, pet):
        if not hasattr(self, "xp_bar_rect"):
            return

        if self._xp_smooth_xp is None:
            self._xp_smooth_xp = float(pet.xp)

        smooth = max(0.0, min(float(pet.xp_to_next), self._xp_smooth_xp))
        progress = 0.0 if pet.xp_to_next <= 0 else smooth / float(pet.xp_to_next)
        progress = max(0.0, min(1.0, progress))

        progress_w = int(self.xp_bar_rect.w * progress)

        if progress_w > 0:
            pygame.draw.rect(
                screen,
                (90, 210, 255),
                (
                    self.xp_bar_rect.x,
                    self.xp_bar_rect.y,
                    progress_w,
                    self.xp_bar_rect.h
                ),
                border_radius=9
            )

        xp_show = int(round(smooth))
        xp_text = self.small_font.render(
            f"Ур. {pet.level} | XP {xp_show}/{pet.xp_to_next}",
            True,
            (250, 250, 255)
        )

        screen.blit(
            xp_text,
            (
                self.xp_bar_rect.centerx - xp_text.get_width() // 2,
                self.xp_bar_rect.centery - xp_text.get_height() // 2
            )
        )


class Game:

    def __init__(self):

        pygame.init()

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))

        pygame.display.set_caption("Pipotam")

        self.clock = pygame.time.Clock()

        self.pet = self.load_pet()

        self.current_room = "happiness"


        self.match3_open = False
        self.match3_score = 0

        # КНОПКА ПОДНЯТА ВЫШЕ
        self.open_game_button = pygame.Rect(140, 620, 200, 58)

        self.close_game_button = pygame.Rect(335, 20, 120, 44)

        self.match3_rows = 6
        self.match3_cols = 6
        self.match3_cell = 64

        self.match3_offset_x = (
                                       WIDTH - self.match3_cols * self.match3_cell
                               ) // 2

        self.match3_offset_y = 150

        self.selected_cell = None

        self.animating_swap = False
        self.swap_progress = 0.0
        # Медленнее и плавнее
        self.swap_speed = 0.045

        # Анимация исчезновения
        self.removing_matches = False
        self.remove_progress = 0.0
        self.remove_speed = 0.08

        self.current_matches = set()

        self.swap_a = None
        self.swap_b = None

        self.falling_tiles = []

        self.match3_board = []

        for row in range(self.match3_rows):

            line = []

            for col in range(self.match3_cols):
                line.append(random.randint(0, 3))

            self.match3_board.append(line)

        self.ui = UI()

        self.running = True

        base_dir = os.path.dirname(os.path.abspath(__file__))

        # Загружаем картинки для 3 в ряд
        self.match3_imgs = [
            pygame.transform.smoothscale(
                pygame.image.load(
                    os.path.join(base_dir, "hippo1.png")
                ).convert_alpha(),
                (58, 58)
            ),

            pygame.transform.smoothscale(
                pygame.image.load(
                    os.path.join(base_dir, "hippo2.png")
                ).convert_alpha(),
                (58, 58)
            ),

            pygame.transform.smoothscale(
                pygame.image.load(
                    os.path.join(base_dir, "hippo3.png")
                ).convert_alpha(),
                (58, 58)
            ),

            pygame.transform.smoothscale(
                pygame.image.load(
                    os.path.join(base_dir, "hippo4.png")
                ).convert_alpha(),
                (58, 58)
            ),
        ]
        self.sound_on_img = pygame.transform.smoothscale(
            pygame.image.load(
                os.path.join(base_dir, "sound1.png")
            ).convert_alpha(),
            (52, 52)
        )

        self.sound_off_img = pygame.transform.smoothscale(
            pygame.image.load(
                os.path.join(base_dir, "sound2.png")
            ).convert_alpha(),
            (52, 52)
        )

        self.backgrounds = {
            "happiness": self.load_bg(os.path.join(base_dir, "background.png")),
            "hunger": self.load_bg(os.path.join(base_dir, "kitchen.png")),
            "cleanliness": self.load_bg(os.path.join(base_dir, "bathroom.png")),
            "bak": self.load_bg(os.path.join(base_dir, "toilet.png")),
            "sleep": self.load_bg(os.path.join(base_dir, "sleep.png")),
        }

        self.pipotam_img = pygame.image.load(
            os.path.join(base_dir, "pipotam.png")
        ).convert_alpha()

        self.dirt_img = pygame.image.load(
            os.path.join(base_dir, "dirt.png")
        ).convert_alpha()

        self.sponge_img = pygame.image.load(
            os.path.join(base_dir, "sponge.png")
        ).convert_alpha()

        self.food_imgs = [
            pygame.transform.smoothscale(
                pygame.image.load(
                    os.path.join(base_dir, "food1.png")
                ).convert_alpha(),
                (100, 100)
            ),

            pygame.transform.smoothscale(
                pygame.image.load(
                    os.path.join(base_dir, "food2.png")
                ).convert_alpha(),
                (100, 100)
            ),

            pygame.transform.smoothscale(
                pygame.image.load(
                    os.path.join(base_dir, "food3.png")
                ).convert_alpha(),
                (100, 100)
            ),
        ]

        self.foods = [
            {
                "img": self.food_imgs[0],
                "rect": pygame.Rect(40, 590, 100, 100),
                "start": (40, 590),
                "food": 15,
                "drag": False,
                "eating": False,
                "scale": 1.0,
            },

            {
                "img": self.food_imgs[1],
                "rect": pygame.Rect(190, 600, 100, 100),
                "start": (190, 600),
                "food": 20,
                "drag": False,
                "eating": False,
                "scale": 1.0,
            },

            {
                "img": self.food_imgs[2],
                "rect": pygame.Rect(340, 590, 100, 100),
                "start": (340, 590),
                "food": 25,
                "drag": False,
                "eating": False,
                "scale": 1.0,
            },
        ]

        self.sponge_rect = pygame.Rect(340, 600, 110, 110)

        self.dragging_sponge = False

        self.foam_marks = []

        self.shower_on = False
        self.shower_audio_ready = False

        self.click_sound = pygame.mixer.Sound(
            os.path.join(base_dir, "sounds", "click.ogg")
        )
        self.click_sound.set_volume(0.4)
        self.eat_sound = pygame.mixer.Sound(
            os.path.join(base_dir, "sounds", "food.ogg")
        )

        self.eat_sound.set_volume(0.5)
        self.sleep_sound = pygame.mixer.Sound(
            os.path.join(base_dir, "sounds", "snore.ogg")
        )

        self.sleep_sound.set_volume(0.35)

        self.sleep_channel = pygame.mixer.Channel(3)
        # Фоновая музыка
        music_path = os.path.join(
            base_dir,
            "sounds",
            "Ingame_Music_01.ogg"
        )

        pygame.mixer.music.load(music_path)

        pygame.mixer.music.set_volume(0.35)

        pygame.mixer.music.play(-1)


        self.shower_channel = None
        self.shower_sound = None
        self.flush_sound = None
        
        self.snore_sound = None
        self.snore_channel = None

        if pygame.mixer.get_init():
            try:
                self.snore_sound = pygame.mixer.Sound(
                    os.path.join(base_dir, "sounds", "snore.ogg")
                )
                self.snore_channel = pygame.mixer.Channel(2)
                self.snore_sound.set_volume(0.4)
            except pygame.error:
                self.snore_sound = None

        if pygame.mixer.get_init():
            try:
                self.flush_sound = pygame.mixer.Sound(
                    os.path.join(base_dir, "sounds", "flush.ogg")
                )
            except pygame.error:
                self.flush_sound = None
        self.shower_button = pygame.Rect(30, 180, 42, 70)

        self.raindrops = []

        for i in range(60):

            self.raindrops.append({
                "x": random.randint(80, WIDTH - 80),
                "y": random.randint(-HEIGHT, 0),
                "speed": random.randint(12, 20),
                "len": random.randint(12, 24)
            })

        self.switch_rect = pygame.Rect(WIDTH // 2, 220, 42, 70)

        self.light_off = False

        self.darkness_alpha = 0
        self.pipotam_rect = pygame.Rect(95, 340, 290, 290)

        self.toilet_paper_img = pygame.transform.smoothscale(
            pygame.image.load(
                os.path.join(base_dir, "toilet_paper.png")
            ).convert_alpha(),
            (88, 88)
        )

        self.toilet_paper = {
            "img": self.toilet_paper_img,
            "rect": pygame.Rect(352, 598, 88, 88),
            "start": (352, 598),
            "drag": False,
            "using": False,
            "scale": 1.0,
        }

        self.toilet_paper_delivered = False

        self.flush_switch_rect = pygame.Rect(400, 200, 42, 70)

        self.flush_cooldown = 0
        self.flush_anim = 0

        self.toilet_paper_respawn_ticks = 0

        shower_sound_path = os.path.join(
            base_dir,
            "sounds",
            "water_noise_shower.ogg"
        )

        if pygame.mixer.get_init():
            try:
                self._prepare_shower_audio(shower_sound_path)
                self.shower_audio_ready = True
            except (pygame.error, ValueError):
                self.shower_audio_ready = False

        self.naming_pet = False
        self.name_input = ""

        self.rename_button = pygame.Rect(15, 38, 120, 28)

        self.name_font = pygame.font.SysFont(
            "Arial",
            26,
            bold=True
        )

        self.sound_muted = False

        self.mute_button = pygame.Rect(
            WIDTH - 60,
            14,
            44,
            44
        )

    def load_bg(self, path):

        img = pygame.image.load(path).convert()

        return pygame.transform.smoothscale(
            img,
            (WIDTH, HEIGHT)
        )
    
    def _start_snore(self):
        if self.snore_sound and self.snore_channel:
            if not self.snore_channel.get_busy():
                self.snore_channel.play(self.snore_sound, loops=-1)

    def _stop_snore(self):
        if self.snore_channel:
            self.snore_channel.fadeout(500)

    def update_sleep_animation(self):

        if self.current_room == "sleep" and self.light_off:

            self.darkness_alpha = min(
                180,
                self.darkness_alpha + 3
            )

            self.pet.sleep_action()

            if not self.sound_muted:

                if not self.sleep_channel.get_busy():
                    self.sleep_channel.play(
                        self.sleep_sound,
                        loops=-1
                    )

        else:

            self.darkness_alpha = max(
                0,
                self.darkness_alpha - 5
            )

            self.sleep_channel.stop()


    def draw_match3_button(self):

        if self.current_room != "happiness":
            return

        if self.match3_open:
            return

        pygame.draw.rect(
            self.screen,
            (70, 120, 240),
            self.open_game_button,
            border_radius=14
        )

        pygame.draw.rect(
            self.screen,
            (255, 255, 255),
            self.open_game_button,
            3,
            border_radius=14
        )

        font = pygame.font.SysFont("Arial", 28, bold=True)

        text = font.render(
            "ИГРАТЬ",
            True,
            (255, 255, 255)
        )

        self.screen.blit(
            text,
            (
                self.open_game_button.centerx
                - text.get_width() // 2,

                self.open_game_button.centery
                - text.get_height() // 2
            )
        )

    # ПОЛНОСТЬЮ ЗАМЕНИ draw_match3 НА ЭТУ ВЕРСИЮ

    def draw_match3(self):

        if not self.match3_open:
            return

        self.update_swap_animation()
        self.update_remove_animation()

        bg = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        bg.fill((0, 0, 0, 220))

        self.screen.blit(bg, (0, 0))

        title_font = pygame.font.SysFont("Arial", 34, bold=True)
        score_font = pygame.font.SysFont("Arial", 24)

        title = title_font.render(
            "3 В РЯД",
            True,
            (255, 255, 255)
        )

        score = score_font.render(
            f"Очки: {self.match3_score}",
            True,
            (255, 255, 255)
        )

        self.screen.blit(
            title,
            (
                WIDTH // 2 - title.get_width() // 2,
                40
            )
        )

        self.screen.blit(
            score,
            (
                WIDTH // 2 - score.get_width() // 2,
                90
            )
        )

        pygame.draw.rect(
            self.screen,
            (180, 60, 60),
            self.close_game_button,
            border_radius=10
        )

        close_font = pygame.font.SysFont("Arial", 22, bold=True)

        close_text = close_font.render(
            "ВЫХОД",
            True,
            (255, 255, 255)
        )

        self.screen.blit(
            close_text,
            (
                self.close_game_button.centerx
                - close_text.get_width() // 2,

                self.close_game_button.centery
                - close_text.get_height() // 2
            )
        )

        # СЕТКА
        for row in range(self.match3_rows):

            for col in range(self.match3_cols):
                x = (
                        self.match3_offset_x
                        + col * self.match3_cell
                )

                y = (
                        self.match3_offset_y
                        + row * self.match3_cell
                )

                rect = pygame.Rect(
                    x,
                    y,
                    self.match3_cell,
                    self.match3_cell
                )

                pygame.draw.rect(
                    self.screen,
                    (45, 45, 60),
                    rect,
                    border_radius=10
                )

                pygame.draw.rect(
                    self.screen,
                    (120, 120, 140),
                    rect,
                    2,
                    border_radius=10
                )

        # ФИШКИ
        for row in range(self.match3_rows):

            for col in range(self.match3_cols):

                value = self.match3_board[row][col]

                if value is None:
                    continue

                draw_x = (
                        self.match3_offset_x
                        + col * self.match3_cell
                        + 3
                )

                draw_y = (
                        self.match3_offset_y
                        + row * self.match3_cell
                        + 3
                )

                # АНИМАЦИЯ ОБМЕНА
                if self.animating_swap:

                    if (row, col) == self.swap_a:

                        ar, ac = self.swap_a
                        br, bc = self.swap_b

                        dx = (bc - ac) * self.match3_cell
                        dy = (br - ar) * self.match3_cell

                        draw_x += dx * self.swap_progress
                        draw_y += dy * self.swap_progress

                    elif (row, col) == self.swap_b:

                        ar, ac = self.swap_a
                        br, bc = self.swap_b

                        dx = (ac - bc) * self.match3_cell
                        dy = (ar - br) * self.match3_cell

                        draw_x += dx * self.swap_progress
                        draw_y += dy * self.swap_progress

                img = self.match3_imgs[value]

                # АНИМАЦИЯ ИСЧЕЗНОВЕНИЯ
                if (
                        self.removing_matches
                        and (row, col) in self.current_matches
                ):

                    scale = max(
                        0.0,
                        1.0 - self.remove_progress
                    )

                    size = int(58 * scale)

                    if size > 0:
                        scaled = pygame.transform.smoothscale(
                            img,
                            (size, size)
                        )

                        offset = (58 - size) // 2

                        self.screen.blit(
                            scaled,
                            (
                                draw_x + offset,
                                draw_y + offset
                            )
                        )

                else:

                    self.screen.blit(
                        img,
                        (
                            int(draw_x),
                            int(draw_y)
                        )
                    )

                if self.selected_cell == (row, col):
                    rect = pygame.Rect(
                        self.match3_offset_x
                        + col * self.match3_cell,

                        self.match3_offset_y
                        + row * self.match3_cell,

                        self.match3_cell,
                        self.match3_cell
                    )

                    pygame.draw.rect(
                        self.screen,
                        (255, 255, 0),
                        rect,
                        4,
                        border_radius=10
                    )

    def get_match3_cell(self, mx, my):

        for row in range(self.match3_rows):

            for col in range(self.match3_cols):

                x = (
                        self.match3_offset_x
                        + col * self.match3_cell
                )

                y = (
                        self.match3_offset_y
                        + row * self.match3_cell
                )

                rect = pygame.Rect(
                    x,
                    y,
                    self.match3_cell,
                    self.match3_cell
                )

                if rect.collidepoint((mx, my)):
                    return (row, col)

        return None

    def are_neighbors(self, a, b):

        ar, ac = a
        br, bc = b

        return abs(ar - br) + abs(ac - bc) == 1

    def swap_cells(self, a, b):

        ar, ac = a
        br, bc = b

        self.match3_board[ar][ac], self.match3_board[br][bc] = (
            self.match3_board[br][bc],
            self.match3_board[ar][ac]
        )

    def find_matches(self):

        matches = set()

        # ГОРИЗОНТАЛЬ
        for row in range(self.match3_rows):

            count = 1

            for col in range(1, self.match3_cols):

                current = self.match3_board[row][col]
                prev = self.match3_board[row][col - 1]

                if current == prev:
                    count += 1

                else:

                    if count >= 3:

                        for k in range(count):
                            matches.add((
                                row,
                                col - 1 - k
                            ))

                    count = 1

            if count >= 3:

                for k in range(count):
                    matches.add((
                        row,
                        self.match3_cols - 1 - k
                    ))

        # ВЕРТИКАЛЬ
        for col in range(self.match3_cols):

            count = 1

            for row in range(1, self.match3_rows):

                current = self.match3_board[row][col]
                prev = self.match3_board[row - 1][col]

                if current == prev:
                    count += 1

                else:

                    if count >= 3:

                        for k in range(count):
                            matches.add((
                                row - 1 - k,
                                col
                            ))

                    count = 1

            if count >= 3:

                for k in range(count):
                    matches.add((
                        self.match3_rows - 1 - k,
                        col
                    ))

        return matches

    def remove_matches(self, matches):

        for row, col in matches:
            self.match3_board[row][col] = None

        self.match3_score += len(matches) * 10

        self.pet.apply_progress(
            "happiness",
            len(matches) * 1.8
        )

    def drop_tiles(self):

        for col in range(self.match3_cols):

            new_col = []

            for row in range(self.match3_rows):

                value = self.match3_board[row][col]

                if value is not None:
                    new_col.append(value)

            missing = self.match3_rows - len(new_col)

            new_tiles = []

            for i in range(missing):
                new_tiles.append(random.randint(0, 3))

            new_col = new_tiles + new_col

            for row in range(self.match3_rows):
                self.match3_board[row][col] = new_col[row]

    def process_board(self):

        while True:

            matches = self.find_matches()

            if not matches:
                break

            self.remove_matches(matches)

            self.drop_tiles()


    def _point_on_pipotam_body(self, x, y):

        r = self.pipotam_rect

        if not r.collidepoint((x, y)):
            return False

        scale = min(r.w / PIPETAM_BODY_REF_W, r.h / PIPETAM_BODY_REF_H)

        body_w = PIPETAM_BODY_REF_W * scale
        body_h = PIPETAM_BODY_REF_H * scale

        cx = r.centerx
        cy = r.y + body_h * 0.5 + (r.h - body_h) * 0.5

        rx = body_w * 0.5 * 0.98
        ry = body_h * 0.5 * 0.98

        nx = (x - cx) / rx
        ny = (y - cy) / ry

        return nx * nx + ny * ny <= 1.0

    def switch_room(self, room_name):

        if self.current_room == "bak" and room_name != "bak":

            self.toilet_paper_delivered = False
            self.toilet_paper["drag"] = False
            self.toilet_paper["using"] = False
            self.toilet_paper["scale"] = 1.0
            self.toilet_paper["rect"].topleft = self.toilet_paper["start"]

            self.toilet_paper_respawn_ticks = 0

        if self.current_room == "cleanliness" and room_name != "cleanliness":

            self.shower_on = False
            self._stop_shower_sound()

        self.current_room = room_name

    def _start_shower_sound(self):

        if not self.shower_audio_ready:
            return

        if self.shower_channel is None or self.shower_sound is None:
            return

        if self.shower_channel.get_busy():
            return

        self.shower_channel.play(self.shower_sound, loops=-1)

    def _stop_shower_sound(self):

        if not self.shower_audio_ready:
            return

        if self.shower_channel is None:
            return

        self.shower_channel.fadeout(SHOWER_FADEOUT_MS)

    def _prepare_shower_audio(self, shower_sound_path):

        self.shower_sound = pygame.mixer.Sound(shower_sound_path)
        self.shower_channel = pygame.mixer.Channel(1)

    def draw_sleep_switch(self):

        if self.current_room != "sleep":
            return

        pygame.draw.rect(
            self.screen,
            (230, 230, 230),
            self.switch_rect,
            border_radius=6
        )

        pygame.draw.rect(
            self.screen,
            (40, 40, 40),
            self.switch_rect,
            2,
            border_radius=6
        )

        if self.light_off:
            inner_y = self.switch_rect.y + 35
        else:
            inner_y = self.switch_rect.y + 6

        inner_rect = pygame.Rect(
            self.switch_rect.x + 6,
            inner_y,
            30,
            28
        )

        pygame.draw.rect(
            self.screen,
            (70, 70, 70),
            inner_rect,
            border_radius=4
        )

    def draw_toilet_flush_switch(self):

        if self.current_room != "bak":
            return

        if self.toilet_paper_delivered:
            pygame.draw.rect(
                self.screen,
                (70, 200, 120),
                self.flush_switch_rect.inflate(8, 8),
                3,
                border_radius=10
            )

        pygame.draw.rect(
            self.screen,
            (230, 230, 230),
            self.flush_switch_rect,
            border_radius=6
        )

        pygame.draw.rect(
            self.screen,
            (40, 40, 40),
            self.flush_switch_rect,
            2,
            border_radius=6
        )

        if self.flush_anim > 0:
            inner_y = self.flush_switch_rect.y + 35
        else:
            inner_y = self.flush_switch_rect.y + 6

        inner_rect = pygame.Rect(
            self.flush_switch_rect.x + 6,
            inner_y,
            30,
            28
        )

        pygame.draw.rect(
            self.screen,
            (70, 70, 70),
            inner_rect,
            border_radius=4
        )

    def draw_toilet_paper(self):

        if self.current_room != "bak":
            return

        if self.toilet_paper_respawn_ticks > 0:
            return

        paper = self.toilet_paper

        if paper["using"]:

            paper["scale"] -= 0.035

            if paper["scale"] <= 0:

                paper["using"] = False
                paper["scale"] = 1.0

                paper["rect"].topleft = paper["start"]

                self.toilet_paper_delivered = True

        size = int(88 * paper["scale"])

        if size <= 0:
            size = 1

        img = pygame.transform.smoothscale(
            paper["img"],
            (size, size)
        )

        draw_x = paper["rect"].x + (88 - size) // 2
        draw_y = paper["rect"].y + (88 - size) // 2

        self.screen.blit(img, (draw_x, draw_y))

    def draw_darkness(self):

        if self.darkness_alpha <= 0:
            return

        dark = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

        dark.fill((0, 0, 0, self.darkness_alpha))

        self.screen.blit(dark, (0, 0))

    # ДОБАВЬ В CLASS GAME

    def start_swap_animation(self, a, b):

        self.animating_swap = True
        self.swap_progress = 0.0

        self.swap_a = a
        self.swap_b = b

    # ПОЛНОСТЬЮ ЗАМЕНИ update_swap_animation

    def update_swap_animation(self):

        if not self.animating_swap:
            return

        self.swap_progress += self.swap_speed

        if self.swap_progress < 1.0:
            return

        self.swap_progress = 1.0

        self.animating_swap = False

        # ===== ПЕРВЫЙ ПРОХОД =====
        if not hasattr(self, "swap_returning"):
            self.swap_returning = False

        if not self.swap_returning:

            # Меняем реально местами
            self.swap_cells(
                self.swap_a,
                self.swap_b
            )

            matches = self.find_matches()

            # ЕСТЬ СОВПАДЕНИЕ
            if matches:

                self.start_remove_animation(matches)

            # НЕТ СОВПАДЕНИЯ → ДЕЛАЕМ ВОЗВРАТ
            else:

                self.swap_returning = True

                self.animating_swap = True
                self.swap_progress = 0.0

                # Меняем направление
                self.swap_a, self.swap_b = (
                    self.swap_b,
                    self.swap_a
                )

        # ===== ВОЗВРАТ НАЗАД =====
        else:

            # Возвращаем обратно
            self.swap_cells(
                self.swap_a,
                self.swap_b
            )

            self.swap_returning = False

    def start_swap_back_animation(self):

        self.swap_cells(
            self.swap_a,
            self.swap_b
        )

        self.animating_swap = True
        self.swap_progress = 0.0

        self.swap_a, self.swap_b = (
            self.swap_b,
            self.swap_a
        )

    # ДОБАВЬ В CLASS GAME

    def start_remove_animation(self, matches):

        self.removing_matches = True

        self.remove_progress = 0.0

        self.current_matches = matches

    def update_remove_animation(self):

        if not self.removing_matches:
            return

        self.remove_progress += self.remove_speed

        if self.remove_progress >= 1.0:

            self.remove_progress = 1.0

            self.removing_matches = False

            self.remove_matches(self.current_matches)

            self.drop_tiles_animated()

            new_matches = self.find_matches()

            if new_matches:
                self.start_remove_animation(new_matches)

    def process_board_animated(self):

        while True:

            matches = self.find_matches()

            if not matches:
                break

            self.remove_matches(matches)

            self.drop_tiles_animated()

    def drop_tiles_animated(self):

        for col in range(self.match3_cols):

            values = []

            for row in range(self.match3_rows):

                value = self.match3_board[row][col]

                if value is not None:
                    values.append(value)

            missing = self.match3_rows - len(values)

            new_tiles = []

            for i in range(missing):
                new_tiles.append(random.randint(0, 3))

            values = new_tiles + values

            for row in range(self.match3_rows):
                self.match3_board[row][col] = values[row]

    def draw_dirty_pipotam(self):

        dirt_alpha = int((100 - self.pet.cleanliness) * 2.55)

        scale = self.pipotam_rect.w / 290

        dirt_size = int(55 * scale)

        dirt_scaled = pygame.transform.smoothscale(
            self.dirt_img,
            (dirt_size, dirt_size)
        )

        dirt_scaled.set_alpha(dirt_alpha)

        base_positions = [
            (0.22, 0.28),
            (0.52, 0.24),
            (0.36, 0.48),
            (0.58, 0.56),
            (0.26, 0.66),
        ]

        for px, py in base_positions:
            x = self.pipotam_rect.x + int(self.pipotam_rect.w * px)
            y = self.pipotam_rect.y + int(self.pipotam_rect.h * py)

            self.screen.blit(dirt_scaled, (x, y))
    def draw_bath_system(self):

        if self.current_room != "cleanliness":
            return

        for foam in self.foam_marks:

            foam_surface = pygame.Surface((54, 54), pygame.SRCALPHA)

            pygame.draw.circle(
                foam_surface,
                (255, 255, 255, foam["alpha"]),
                (27, 27),
                24
            )

            pygame.draw.circle(
                foam_surface,
                (235, 235, 255, foam["alpha"]),
                (18, 18),
                11
            )

            pygame.draw.circle(
                foam_surface,
                (235, 235, 255, foam["alpha"]),
                (36, 30),
                10
            )

            self.screen.blit(
                foam_surface,
                (foam["x"], foam["y"])
            )

        pygame.draw.rect(
            self.screen,
            (230, 230, 230),
            self.shower_button,
            border_radius=6
        )

        pygame.draw.rect(
            self.screen,
            (40, 40, 40),
            self.shower_button,
            2,
            border_radius=6
        )

        if self.shower_on:
            inner_y = self.shower_button.y + 35
        else:
            inner_y = self.shower_button.y + 6

        inner_rect = pygame.Rect(
            self.shower_button.x + 6,
            inner_y,
            30,
            28
        )

        pygame.draw.rect(
            self.screen,
            (70, 70, 70),
            inner_rect,
            border_radius=4
        )

        if self.shower_on:

            removed_foam = 0

            for drop in self.raindrops:

                pygame.draw.line(
                    self.screen,
                    (170, 220, 255),
                    (drop["x"], drop["y"]),
                    (drop["x"], drop["y"] + drop["len"]),
                    3
                )

                drop["y"] += drop["speed"]

                if drop["y"] > HEIGHT:

                    drop["y"] = random.randint(-200, -20)

                    drop["x"] = random.randint(90, WIDTH - 90)

            for foam in self.foam_marks:

                foam["alpha"] -= 2

                if foam["alpha"] <= 0:
                    removed_foam += 1

            self.foam_marks = [
                foam for foam in self.foam_marks
                if foam["alpha"] > 0
            ]

            if removed_foam > 0:
                self.pet.apply_progress("cleanliness", removed_foam * 0.45)

        sponge_scaled = pygame.transform.smoothscale(
            self.sponge_img,
            (110, 110)
        )

        self.screen.blit(
            sponge_scaled,
            self.sponge_rect
        )

    def draw_food_system(self):

        if self.current_room != "hunger":
            return

        for food in self.foods:

            if food["eating"]:

                food["scale"] -= 0.03

                self.pet.apply_progress("hunger", food["food"] * 0.01)

                if food["scale"] <= 0:

                    food["eating"] = False
                    food["scale"] = 1.0
                    food["rect"].topleft = food["start"]

                    continue

            size = int(100 * food["scale"])

            if size <= 0:
                size = 1

            img = pygame.transform.smoothscale(
                food["img"],
                (size, size)
            )

            draw_x = food["rect"].x + (100 - size) // 2
            draw_y = food["rect"].y + (100 - size) // 2

            self.screen.blit(img, (draw_x, draw_y))

    def save_pet(self):

        data = {
            "name": self.pet.name,
            "hunger": self.pet.hunger,
            "cleanliness": self.pet.cleanliness,
            "sleep": self.pet.sleep,
            "happiness": self.pet.happiness,
            "bak": self.pet.bak,
            "level": self.pet.level,
            "xp": self.pet.xp,
            "xp_to_next": self.pet.xp_to_next
        }

        with open("save.json", "w", encoding="utf-8") as f:
            json.dump(data, f)

    def load_pet(self):

        if not os.path.exists("save.json"):
            return Pet("Пипотам")

        with open("save.json", "r", encoding="utf-8") as f:
            data = json.load(f)

        pet = Pet(data["name"])

        pet.hunger = data["hunger"]
        pet.cleanliness = data["cleanliness"]
        pet.sleep = data["sleep"]
        pet.happiness = data["happiness"]
        pet.bak = data["bak"]

        pet.level = data["level"]
        pet.xp = data["xp"]
        pet.xp_to_next = data["xp_to_next"]

        return pet

    def run(self):

        while self.running:

            self.clock.tick(FPS)

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame.KEYDOWN:

                    if self.naming_pet:

                        if event.key == pygame.K_RETURN:

                            if self.name_input.strip():
                                self.pet.name = self.name_input.strip()

                                self.naming_pet = False

                                self.save_pet()

                        elif event.key == pygame.K_BACKSPACE:

                            self.name_input = self.name_input[:-1]

                        else:

                            if len(self.name_input) < 14:
                                self.name_input += event.unicode

                        continue

                    if event.key == pygame.K_1:
                        self.switch_room("hunger")

                    elif event.key == pygame.K_2:
                        self.switch_room("cleanliness")

                    elif event.key == pygame.K_3:
                        self.switch_room("bak")

                    elif event.key == pygame.K_4:
                        self.switch_room("sleep")

                    elif event.key == pygame.K_5:
                        self.switch_room("happiness")

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    mute_button = pygame.Rect(
                        WIDTH - 68,
                        78,
                        52,
                        52
                    )
                    if mute_button.collidepoint(mouse_pos):
                        self.toggle_sound()
                    if self.naming_pet:

                        if hasattr(self, "close_name_button"):

                            if self.close_name_button.collidepoint(mouse_pos):
                                self.naming_pet = False
                    rename_rect = pygame.Rect(
                        18,
                        HEIGHT - UI_BOTTOM_PANEL_H + 10,
                        WIDTH - 36,
                        24
                    )

                    if rename_rect.collidepoint(mouse_pos):
                        self.naming_pet = True

                        self.name_input = ""

                    if self.rename_button.collidepoint(mouse_pos):
                        self.naming_pet = True

                        self.name_input = self.pet.name



                    for rect, room_name in self.ui.buttons:

                        if rect.collidepoint(mouse_pos):

                            self.switch_room(room_name)

                    if self.current_room == "cleanliness":

                        if self.sponge_rect.collidepoint(mouse_pos):

                            self.dragging_sponge = True

                        if self.shower_button.collidepoint(mouse_pos):

                            self.shower_on = not self.shower_on
                            if not self.sound_muted:
                                self.click_sound.play()

                            if self.shower_on:
                                if not self.sound_muted:
                                    self._start_shower_sound()
                            else:
                                self._stop_shower_sound()

                    # В event.type == pygame.MOUSEBUTTONDOWN ДОБАВЬ:

                    if self.current_room == "happiness":

                        if (
                                self.open_game_button.collidepoint(mouse_pos)
                                and not self.match3_open
                        ):

                            self.match3_open = True

                        elif self.match3_open:

                            if self.close_game_button.collidepoint(mouse_pos):

                                self.match3_open = False
                                self.selected_cell = None

                            else:

                                cell = self.get_match3_cell(
                                    mouse_pos[0],
                                    mouse_pos[1]
                                )

                                if (
                                        cell
                                        and not self.animating_swap
                                        and not self.removing_matches
                                ):

                                    if self.selected_cell is None:

                                        self.selected_cell = cell

                                    else:

                                        if self.are_neighbors(
                                                self.selected_cell,
                                                cell
                                        ):
                                            self.start_swap_animation(
                                                self.selected_cell,
                                                cell
                                            )

                                        self.selected_cell = None

                    if self.current_room == "sleep":

                        if self.switch_rect.collidepoint(mouse_pos):

                            self.light_off = not self.light_off
                            if not self.sound_muted:
                                self.click_sound.play()

                    if self.current_room == "hunger":

                        for food in self.foods:

                            if food["rect"].collidepoint(mouse_pos):

                                food["drag"] = True

                    if self.current_room == "bak":

                        if (
                            self.toilet_paper_respawn_ticks <= 0
                            and self.toilet_paper["rect"].collidepoint(mouse_pos)
                        ):
                            self.toilet_paper["drag"] = True

                        elif (
                            self.flush_switch_rect.collidepoint(mouse_pos)
                            and not self.toilet_paper["rect"].collidepoint(mouse_pos)
                            and self.toilet_paper_delivered
                            and self.flush_cooldown <= 0
                        ):

                            if self.flush_sound is not None:
                                if not self.sound_muted:
                                    self.flush_sound.play()

                            self.pet.apply_progress("bak", -100)

                            self.toilet_paper_delivered = False

                            self.toilet_paper["drag"] = False
                            self.toilet_paper["using"] = False
                            self.toilet_paper["scale"] = 1.0

                            self.toilet_paper["rect"].topleft = (
                                self.toilet_paper["start"]
                            )

                            self.flush_cooldown = 36
                            self.flush_anim = 22

                            self.toilet_paper_respawn_ticks = int(2.0 * FPS)

                if event.type == pygame.MOUSEBUTTONUP:

                    self.dragging_sponge = False

                    if self.toilet_paper["drag"]:

                        self.toilet_paper["drag"] = False

                        cx = self.toilet_paper["rect"].centerx
                        cy = self.toilet_paper["rect"].centery

                        if self._point_on_pipotam_body(cx, cy):

                            self.toilet_paper["using"] = True

                        else:

                            self.toilet_paper["rect"].topleft = (
                                self.toilet_paper["start"]
                            )

                    for food in self.foods:

                        if food["drag"]:

                            food["drag"] = False

                            if food["rect"].colliderect(self.pipotam_rect):

                                food["eating"] = True
                                if not self.sound_muted:
                                    self.eat_sound.play()

                            else:

                                food["rect"].topleft = food["start"]

                if event.type == pygame.MOUSEMOTION:

                    if self.dragging_sponge:

                        mx, my = pygame.mouse.get_pos()

                        self.sponge_rect.center = (mx, my)

                        if self._point_on_pipotam_body(mx, my):

                            self.foam_marks.append({
                                "x": mx - 22,
                                "y": my - 22,
                                "alpha": 210
                            })

                        if len(self.foam_marks) > 220:

                            self.foam_marks.pop(0)

                    for food in self.foods:

                        if food["drag"]:

                            mx, my = pygame.mouse.get_pos()

                            food["rect"].center = (mx, my)

                    if self.toilet_paper["drag"]:

                        mx, my = pygame.mouse.get_pos()

                        self.toilet_paper["rect"].center = (mx, my)

            self.pet.update()
            self.update_pipotam_size()
            if pygame.time.get_ticks() % 5000 < 16:
                self.save_pet()

            if self.flush_cooldown > 0:
                self.flush_cooldown -= 1

            if self.flush_anim > 0:
                self.flush_anim -= 1

            if self.toilet_paper_respawn_ticks > 0:
                self.toilet_paper_respawn_ticks -= 1

            self.update_sleep_animation()

            dt = self.clock.get_time() / 1000.0

            self.ui.update_xp_display(self.pet, dt)

            self.screen.blit(
                self.backgrounds[self.current_room],
                (0, 0)
            )

            self.draw_toilet_flush_switch()

            pipotam_scaled = pygame.transform.smoothscale(
                self.pipotam_img,
                self.pipotam_rect.size
            )

            self.screen.blit(
                pipotam_scaled,
                self.pipotam_rect.topleft
            )

            self.draw_dirty_pipotam()

            self.draw_food_system()

            self.draw_bath_system()

            self.draw_toilet_paper()

            self.draw_sleep_switch()

            self.draw_darkness()

            self.ui.draw_top(
                self.screen,
                self.pet,
                self
            )

            self.ui.draw_bottom(
                self.screen,
                self.current_room,
                self.pet
            )

            self.ui.draw_xp(self.screen, self.pet)

            # Кнопка мини-игры
            self.draw_match3_button()

            # Сама игра 3 в ряд
            self.draw_match3()

            self.draw_name_input()

            pygame.display.flip()

        self.save_pet()
        pygame.quit()

    def draw_name_input(self):

        if not self.naming_pet:
            return

        overlay = pygame.Surface(
            (WIDTH, HEIGHT),
            pygame.SRCALPHA
        )

        overlay.fill((0, 0, 0, 210))

        self.screen.blit(overlay, (0, 0))

        box = pygame.Rect(60, 300, 360, 120)

        pygame.draw.rect(
            self.screen,
            (255, 255, 255),
            box,
            border_radius=16
        )

        title = self.name_font.render(
            "Имя бегемота",
            True,
            (20, 20, 20)
        )

        self.screen.blit(
            title,
            (
                WIDTH // 2 - title.get_width() // 2,
                315
            )
        )

        show_text = self.name_input

        if pygame.time.get_ticks() % 1000 < 500:
            show_text += "|"

        text = self.name_font.render(
            show_text,
            True,
            (40, 40, 40)
        )

        self.screen.blit(
            text,
            (
                box.x + 20,
                360
            )
        )

        # Кнопка закрытия
        self.close_name_button = pygame.Rect(
            box.right - 42,
            box.y + 10,
            32,
            32
        )

        pygame.draw.rect(
            self.screen,
            (220, 80, 80),
            self.close_name_button,
            border_radius=8
        )

        x_text = self.name_font.render(
            "X",
            True,
            (255, 255, 255)
        )

        self.screen.blit(
            x_text,
            (
                self.close_name_button.centerx
                - x_text.get_width() // 2,

                self.close_name_button.centery
                - x_text.get_height() // 2 - 1
            )
        )

    def update_pipotam_size(self):

        scale = 0.62

        if self.pet.level >= 5:
            scale = 0.72

        if self.pet.level >= 10:
            scale = 0.82

        if self.pet.level >= 15:
            scale = 0.92

        if self.pet.level >= 20:
            scale = 1.0

        w = int(290 * scale)
        h = int(290 * scale)

        self.pipotam_rect = pygame.Rect(
            WIDTH // 2 - w // 2,
            650 - h,
            w,
            h
        )

    def toggle_sound(self):

        self.sound_muted = not self.sound_muted

        if self.sound_muted:

            pygame.mixer.stop()
            pygame.mixer.music.stop()

        else:

            pygame.mixer.music.load(
                os.path.join(
                    os.path.dirname(os.path.abspath(__file__)),
                    "sounds",
                    "Ingame_Music_01.ogg"
                )
            )

            pygame.mixer.music.set_volume(0.35)

            pygame.mixer.music.play(-1)
        self.sleep_channel.stop()

if __name__ == "__main__":
    Game().run()