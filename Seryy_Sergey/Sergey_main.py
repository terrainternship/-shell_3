from datetime import timedelta, datetime
import cv2
import numpy as np
import os

SAVING_FRAMES_PER_SECOND = 5
BLUR_THRESHOLD = 1000.0

def format_timedelta(td):
    """Служебная функция для классного форматирования объектов timedelta (например, 00:00:20.05)
    исключая микросекунды и сохраняя миллисекунды"""
    result = str(td)
    try:
        result, ms = result.split(".")
    except ValueError:
        return result + ".00".replace(":", "-")
    ms = int(ms)
    ms = round(ms / 1e4)
    return f"{result}.{ms:02}".replace(":", "-")


def get_saving_frames_durations(cap, saving_fps):
    """Функция, которая возвращает список длительностей, в которые следует сохранять кадры."""
    s = []
    # получаем продолжительность клипа, разделив количество кадров на количество кадров в секунду
    clip_duration = cap.get(cv2.CAP_PROP_FRAME_COUNT) / cap.get(cv2.CAP_PROP_FPS)
    # используйте np.arange () для выполнения шагов с плавающей запятой
    for i in np.arange(0, clip_duration, 1 / saving_fps):
        s.append(i)
    return s

def calculate_blur_score(frame):
    """
    Рассчитывает оценку размытия изображения.

    Аргументы:
    - frame: Массив NumPy, представляющий изображение в формате BGR.

    Возвращает:
    - Оценку размытия изображения (blur score).
    """
    # Преобразование изображения в оттенки серого
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Рассчитываем градиенты по осям x и y с помощью оператора Собеля
    gradient_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
    gradient_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)

    # Рассчитываем величину градиента
    gradient_magnitude = cv2.magnitude(gradient_x, gradient_y)

    # Рассчитываем среднее значение величины градиента как оценку размытия
    blur_score = np.mean(gradient_magnitude)

    return blur_score


def movie_to_img(video_file):
    filename, _ = os.path.splitext(video_file)
    filename += "-opencv"
    # создаем папку по названию видео файла
    if not os.path.isdir(filename):
        os.mkdir(filename)
    # читать видео файл
    cap = cv2.VideoCapture(video_file)
    # получить FPS видео
    fps = cap.get(cv2.CAP_PROP_FPS)
    # если SAVING_FRAMES_PER_SECOND выше видео FPS, то установите его на FPS (как максимум)
    saving_frames_per_second = min(fps, SAVING_FRAMES_PER_SECOND)
    # получить список длительностей для сохранения
    saving_frames_durations = get_saving_frames_durations(cap, saving_frames_per_second)
    # запускаем цикл
    count = 0
    # время для дополнительной маркировки фреймов
    current_datetime = datetime.now()
    str_time = f'{current_datetime.hour}{current_datetime.minute}{current_datetime.second}'

    while True:
        is_read, frame = cap.read()
        if not is_read:
            # выйти из цикла, если нет фреймов для чтения
            break
        # получаем продолжительность, разделив количество кадров на FPS
        frame_duration = count / fps
        try:
            # получить самую раннюю продолжительность для сохранения
            closest_duration = saving_frames_durations[0]
        except IndexError:
            # список пуст, все кадры длительности сохранены
            break
        if frame_duration >= closest_duration:
            # если ближайшая длительность меньше или равна длительности кадра,
            # затем проверяем коэффициент размытия
            blur_score = calculate_blur_score(frame)

            if blur_score <= BLUR_THRESHOLD:
                # сохраняем фрейм, только если коэффициент размытия удовлетворяет порогу
                frame_duration_formatted = format_timedelta(timedelta(seconds=frame_duration))
                cv2.imwrite(os.path.join(filename, f"{str_time}frame{frame_duration_formatted}.jpg"), frame)

            # удалить точку продолжительности из списка, так как эта точка длительности уже сохранена
            try:
                saving_frames_durations.pop(0)
            except IndexError:
                pass
        # увеличить количество кадров
        count += 1


if __name__ == '__main__':
    print("Текущая директория:", os.getcwd())
    cur_dir = str(input("Введите новую директорию: "))

    if cur_dir == '':
        cur_dir = os.getcwd()
    os.chdir(cur_dir)
    print("Текущая директория:", os.getcwd())
    all_files = os.listdir(cur_dir)
    for file in all_files:
        if file[-4:].lower() == '.mp4':
            print(file)
            movie_to_img(file)



