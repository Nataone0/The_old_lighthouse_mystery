import pygame
import sys
from pygame.locals import *
import os

SCREEN_WIDTH = 1024  # размеры окна выбрал такими, потому что картинки 1024 х 512,
SCREEN_HEIGHT = 600  # можно обрезать картинки (или заново сгенерить) если нужен другой размер

class Location:    # класс локации, все атрибуты можно хранить и загружать из SQLite
    def __init__(self, background_image_path, music_path, options=None):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.background = pygame.image.load(background_image_path)
        self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.font = pygame.font.Font(None, 24)
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Тайна старого маяка")
        self.music_path = music_path
        self.dialog = []
        self.next_locations = []
        self.options = options if options else []
        self.character_images = {}  # словарь для хранения изображений персонажей
        self.voice_clips = {}  # словарь для хранения звуковых файлов диалогов

    def load_character_image(self, character_name, image_path):
        image = pygame.image.load(image_path)
        self.character_images[character_name] = pygame.transform.scale(image, (200, 300))

    def load_voice_clip(self, dialog_id, clip_path):
        self.voice_clips[dialog_id] = pygame.mixer.Sound(clip_path)

    def play_voice_clip(self, dialog_id):
        if dialog_id in self.voice_clips:
            # Приглушение фоновой музыки во время диалога
            pygame.mixer.music.set_volume(0.2)
            self.voice_clips[dialog_id].play()
            # Ожидание окончания воспроизведения звукового файла
            while pygame.mixer.get_busy():
                pygame.time.delay(100)
            # Восстановление громкости фоновой музыки
            pygame.mixer.music.set_volume(1.0)

    def run_dialog(self):  # функция диалогов
        index = 0
        while index < len(self.dialog):        # цикл перебора всех фраз диалога от 0-го до последнего индекса
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()         # выход из игры
                    sys.exit()
                elif event.type == KEYDOWN:
                    if event.key == K_SPACE: # листаем фразы диалога клавишей Пробела
                        if index < len(self.dialog) - 1:
                            index += 1
                        else:
                            return  # выход из диалога
                    elif event.key == K_ESCAPE:
                        pygame.quit()
                        sys.exit()
            self.screen.blit(self.background, (0, 0))
            speaker, text = self.dialog[index]
            if speaker in self.character_images:
                character_image = self.character_images[speaker]
                self.screen.blit(character_image, (50, 250))  # Позиция изображения персонажа
            self.draw_text(f"{speaker}: {text}", (100, 550))
            self.play_voice_clip(index)  # Воспроизведение звукового файла для текущей реплики по индексу
            pygame.display.update()
            self.clock.tick(60)

    def start_music(self):                            # запускает звуковой файл
        pygame.mixer.music.load(self.music_path)
        pygame.mixer.music.play(-1,0.0)                   # бесконечное воспроизведение звука

    def draw_text(self, text, position, font_size=24, color=(250, 250, 200)):  # отрисовка текста
        font = pygame.font.Font(None, font_size)
        text_surface = font.render(text, True, color)
        self.screen.blit(text_surface, position)

    def choose_action(self):  # выбор перехода к следующей локации
        opt = None            # opt - переменная сделанного выбора
        while opt is None:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN:
                    if event.key == K_1 and len(self.options) >= 1:    # выбор из двух вариантов
                        opt = 0                                        # можно сделать больше при большом желании,
                    elif event.key == K_2 and len(self.options) >= 2:  # но я думаю нам двух достаточно
                        opt = 1
                    if opt is not None:                                # когда выбор сделан, opt is not None, - остановка воспроизведения звука
                        pygame.mixer.music.stop()
            self.screen.blit(self.background, (0, 0))
            for i, option in enumerate(self.options):
                self.draw_text(f"{i + 1}. {option}", (100, 50 + 30 * i), font_size=22) # вывод надписей для выбора следующей локации
            pygame.display.update()
            self.clock.tick(60)
        return opt

    def run(self):  # запуск всех методов локации
        self.start_music()
        self.run_dialog()
        opt = self.choose_action()
        if opt is not None and opt < len(self.next_locations):
            next_location = self.next_locations[opt]
            if next_location:
                next_location.run()
        else:
            pygame.quit()

if __name__ == '__main__':
    loc1_1 = Location('loc1_1.jpg', 'loc1_1.mp3', ["Изучить записку", "Расспросить посетителей бара"]) # создание локаций: loc1 - первая локация, _1 - первая сцена
    loc1_2 = Location('loc1_2.jpg', 'loc1_2.mp3', ["Дом сторожа маяка", "Вариант 2"])                  # локация: loc1_2 - первая локация, вторая сцена
    loc1_3 = Location('loc1_3.jpg', 'loc1_3.mp3', ["Дом сторожа маяка", "Вариант 2"])
    loc2_1 = Location('loc2_1.jpg', 'loc2_1.mp3', ["Прибрежный лес", "Вариант 2"])
    loc3_1 = Location('loc3_1.jpg', 'loc3_1.mp3', ["Старый маяк", "Вариант 2"])
    loc4_1 = Location('loc4_1.jpg', 'loc4_1.mp3', ["Призрак старого хозяина маяка", "Вариант 2"])       # локация: loc4_1 - четвертая локация, первая сцена
    loc4_2 = Location('loc4_2.jpg', 'loc4_2.mp3', ["Вариант 1", "Вариант 2"])

    loc1_1.next_locations = [loc1_2, loc1_3] # Выбор варианта следующей локации: либо loc1_2, либо loc1_3
    loc1_2.next_locations = [loc2_1, loc1_1] # Поскольку еще нет ветвления сюжета, при выборе второго варианта
    loc1_3.next_locations = [loc2_1, loc1_1] # во всех локациях кроме первой записан переход на loc1_1
    loc2_1.next_locations = [loc3_1, loc1_1]
    loc3_1.next_locations = [loc4_1, loc1_1]
    loc4_1.next_locations = [loc4_2, loc1_1]
    loc4_2.next_locations = [loc1_1, loc1_1]

    loc1_1.dialog = [("Кирилл", "Здравствуйте, я Кирилл, новенький здесь."),         # диалоги: loc1_1.dialog - диалог первой локации первой сцены
                     ("Бармен", "Приветствую, Кирилл! Что вам налить?"),
                     ("Кирилл",
                      "Кофе, пожалуйста! Я слышал, что вы можете рассказать много интересного о старом маяке."),
                     ("Бармен", "Да, маяк... Он уже много лет беспокоит умы местных."),
                     ("Кирилл", "Я весь во внимании, Расскажите."),
                     ("Бармен", " Странности начались, когда последний сторож исчез без вести."),
                     ("Бармен",
                      "А недавно кто-то видел странные огни там. Кстати, вы не первый, кто интересуется маяком."),
                     ("Бармен", "Недавно тут был детектив, оставил записку, но так и не вернулся."),
                     ("Кирилл", "Записка? Можно мне её посмотреть?"),
                     ("Бармен", "Конечно, держите. Надеюсь, она поможет вам больше, чем тому бедняге.")]
    loc1_2.dialog = [("Персонаж 1", "Текст к локации: Записка с криптографической загадкой, оставленная предыдущим детективом."),
                     ("Персонаж 2", "Текст к локации."),
                     ("Персонаж 1", "Текст к локации."),
                     ("Персонаж 2", "Текст к локации.")]
    loc1_3.dialog = [("Персонаж 1", "Текст к локации: Диалог с посетителем бара."),
                     ("Персонаж 2", "Текст к локации."),
                     ("Персонаж 1", "Текст к локации."),
                     ("Персонаж 2", "Текст к локации.")]
    loc2_1.dialog = [("Персонаж 1", "Текст к локации: Дом сторожа маяка."),         # диалог loc2_1.dialog - диалог второй локации первой сцены
                     ("Персонаж 2", "Текст к локации."),
                     ("Персонаж 1", "Текст к локации."),
                     ("Персонаж 2", "Текст к локации.")]
    loc3_1.dialog = [("Персонаж 1", "Текст к локации: Прибрежный лес."),
                     ("Персонаж 2", "Текст к локации."),
                     ("Персонаж 1", "Текст к локации."),
                     ("Персонаж 2", "Текст к локации.")]
    loc4_1.dialog = [("Персонаж 1", "Текст к локации: Старый маяк."),
                     ("Персонаж 2", "Текст к локации."),
                     ("Персонаж 1", "Текст к локации."),
                     ("Персонаж 2", "Текст к локации.")]
    loc4_2.dialog = [("Персонаж 1", "Текст к локации: Призрак старого хозяина маяка."),
                     ("Персонаж 2", "Текст к локации."),
                     ("Персонаж 1", "Текст к локации."),
                     ("Персонаж 2", "Текст к локации.")]

    loc1_1.load_voice_clip = {(0, 'Location1_dialogs/01 - (Кирилл) Здравствуйте я Кирил.mp3'),
                              (1, 'Location1_dialogs/02 - (Бармен) Приветствую, Кирилл.mp3'),
                              (2, 'Location1_dialogs/03 - (Кирилл) Кофе пожалуйста Я слышал что вы можете рассказать.mp3'),
                              (3, 'Location1_dialogs/04 - (бармен) Да, маяк, Он уже много лет .mp3'),
                              (4, 'Location1_dialogs/05 - (Кирилл) Я весь во внимании Расскажите.mp3'),
                              (5, 'Location1_dialogs/06 - (бармен) Странности начались .mp3'),
                              (6, 'Location1_dialogs/07 - (бармен) А недавно кто-то видел странные огни там.mp3'),
                              (7, 'Location1_dialogs/10 - (бармен) Недавно тут был детектив.mp3'),
                              (8, 'Location1_dialogs/11 - (Кирилл) Записка? Можно мне её посмотреть.mp3'),
                              (9, 'Location1_dialogs/12 - (бармен) Конечно Держите Надеюсь она поможет.mp3'),
                              }
    loc1_1.play_voice_clip(0)



    loc1_1.run()   # запуск первой локации, первой сцены
