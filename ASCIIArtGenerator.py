# библиотека
from pathlib import Path
from typing import List, Optional
import os
import imageio
from PIL import Image, ImageDraw, ImageFont


# класс для генерации ASCII-арт из изображений и GIF
class ASCIIArtGenerator:
    """Класс для генерации ASCII-арт из изображений и GIF"""

    # конструктор
    def __init__(self, scale_factor: float = 10, ascii_chars: str = r"@%#*+=-:. "):
        """
        Конструктор класса.
        :param scale_factor: коэффициент масштабирования
        :param ascii_chars: строка символов, используемых для преобразования пикселей в ASCII-символы
        """
        self.__scale_factor = scale_factor / 100
        self.__ascii_chars = ascii_chars
        self.__frames = []
        self._path_file = None

    # преобразование GIF в набор PNG
    def gif_to_png(self, gif_path: str) -> List[Path]:
        """
        Преобразование GIF-анимации в отдельные PNG-изображения.
        :param gif_path: путь к GIF-файлу
        :return: директория, в которой сохранены PNG-изображения
        """
        # Получение имени файла без расширения
        base_name = os.path.splitext(os.path.basename(gif_path))[0]

        # Чтение gif
        gif = imageio.mimread(gif_path)

        # Создание списка изображений
        images = [Image.fromarray(frame) for frame in gif]

        # Определение директории gif_path
        gif_dir = os.path.dirname(gif_path)

        # Создание папки для сохранения PNG-файлов
        png_dir = os.path.join(gif_dir, f"{base_name}")
        os.makedirs(png_dir, exist_ok=True)

        # Сохранение PNG-файлов в папку
        for i, image in enumerate(images):
            png_path = os.path.join(png_dir, f"{base_name}_frame_{i+1}.png")
            image.save(png_path)

        return png_dir

    def gif_to_ascii(self, gif_path: str) -> List[str]:
        """
        Преобразование GIF-анимации в ASCII-арт.
        :param gif_path: путь к GIF-файлу
        :return: список строк с ASCII-арт для каждого кадра
        """

        # Инициализация списка для хранения Unicode-представления gif
        unicode_frames = []

        # Открываем GIF-файл с помощью Pillow
        with Image.open(gif_path) as gif:
            frames = []

            # Итерируем по всем кадрам GIF-файла
            for i in range(gif.n_frames):
                gif.seek(i)

                # Преобразование изображения в объект PIL
                img = gif.convert("RGBA")

                # Изменение размера изображения
                width, height = img.size
                img = img.resize(
                    (
                        int(self.__scale_factor * width),
                        int(self.__scale_factor * height),
                    )
                )

                # Преобразование в оттенки серого
                pixels = img.convert("L")

                # Преобразование пикселей в символы Unicode
                ascii_str = ""
                for pixel_value in pixels.getdata():
                    # Используем min и max, чтобы гарантировать, что индекс находится в пределах допустимых значений
                    index = max(
                        0,
                        min(
                            pixel_value // (256 // len(self.__ascii_chars)),
                            len(self.__ascii_chars) - 1,
                        ),
                    )
                    ascii_str += self.__ascii_chars[index]

                # Разделение текста на строки для отображения
                ascii_str_len = len(ascii_str)
                img_ascii = ""
                for j in range(0, ascii_str_len, int(self.__scale_factor * width)):
                    img_ascii += (
                        ascii_str[j : j + int(self.__scale_factor * width)] + "\n"
                    )

                # Добавление строки в список
                unicode_frames.append(img_ascii + "\\f")

        self.__frames = unicode_frames
        self._path_file = gif_path
        return unicode_frames

    # преобразование GIF или изображения в ASCII-арт
    def image_to_ascii(self, image_path: str, output_file: str = None) -> str:
        """
        Преобразование изображения в ASCII-арт.
        :param image_path: путь к изображению
        :param output_file: путь к файлу, в который будет сохранен ASCII-арт (по умолчанию, тот же путь, что и изображение)
        :return: строка с ASCII-арт
        """

        # Преобразование изображения в объект PIL
        img = Image.open(image_path)

        # Изменение размера изображения
        width, height = img.size
        img = img.resize(
            (int(self.__scale_factor * width), int(self.__scale_factor * height))
        )

        # Преобразование в оттенки серого
        pixels = img.convert("L")

        # Преобразование пикселей в символы Unicode
        ascii_str = ""
        for pixel_value in pixels.getdata():
            # Используем min и max, чтобы гарантировать, что индекс находится в пределах допустимых значений
            index = max(
                0,
                min(
                    pixel_value // (256 // len(self.__ascii_chars)),
                    len(self.__ascii_chars) - 1,
                ),
            )
            ascii_str += self.__ascii_chars[index]

        # Разделение текста на строки для отображения
        ascii_str_len = len(ascii_str)
        img_ascii = ""
        for j in range(0, ascii_str_len, int(self.__scale_factor * width)):
            img_ascii += ascii_str[j : j + int(self.__scale_factor * width)] + "\n"

        self.__frames = [img_ascii]
        self._path_file = image_path
        return img_ascii

    # преобразование ASCII-арт обратно в изображение
    def ascii_to_image(
        self,
        ascii_art: str,
        font_size: int = 12,
        font_path: str = "consola.ttf",
        output_file: str = None,
        save_factor: bool = True,
    ) -> Image:
        """
        Преобразование ASCII-арт в изображение.
        :param ascii_art: строка с ASCII-арт
        :param font_size: размер шрифта
        :param font_path: путь к файлу шрифта
        :param output_file: путь к файлу, в который будет сохранен ASCII-арт (по умолчанию, будет создан рядом с исходным файлом)
        :return: объект PIL.Image
        :param save_factor: сохранить ли в виде файла
        """

        # Разбиваем ASCII-арт по символам новой строки
        lines = ascii_art.split("\n")

        # Определяем фактическую максимальную ширину изображения
        img_width = max(sum(1 for char in line) * font_size for line in lines)
        img_height = len(lines) * font_size

        # Создание изображения и объекта рисования
        img = Image.new("RGB", (img_width, img_height), color="white")
        draw = ImageDraw.Draw(img)

        # Загрузка шрифта
        font = ImageFont.truetype(font_path, font_size*1.8)

        # Отрисовка ASCII-арт на изображении
        for i, line in enumerate(lines):
            draw.text((0, i * font_size), line, font=font, fill="black")

        if output_file is None:
            # Получение имени файла без расширения из path_file
            base_name = os.path.splitext(os.path.basename(self._path_file))[0]
            # Формирование пути для сохранения
            output_file = os.path.join(
                os.path.dirname(self._path_file), f"{base_name}_ascii.png"
            )

        if save_factor:
            # Сохранение изображения
            img.save(output_file)

        # print(img)
        return img

    # преобразование ASCII-арт в GIF анимацию
    def ascii_to_gif(
        self,
        ascii_frames: List[str],
        output_file: str = None,
        font_size: int = 12,
        font_path: str = "consola.ttf",
        duration: float = 1,
        save_factor: bool = False,
    ) -> Image:
        """
        Преобразование ASCII-арт в GIF-анимацию.
        :param ascii_frames: список строк с ASCII-арт для каждого кадра
        :param output_file: путь для сохранения файла
        :param font_size: размер шрифта
        :param duration: длительность каждого кадра в милисекундах
        :param font_path: путь к файлу шрифта
        :param save_factor: сохранить ли в виде файла
        """
        images = []

        for frame in ascii_frames:
            img = self.ascii_to_image(
                frame, font_size, font_path, save_factor=save_factor
            )
            images.append(img)

        if output_file == None:
            # Получение имени файла без расширения из path_file
            base_name = os.path.splitext(os.path.basename(self._path_file))[0]
            # Формирование пути для сохранения
            output_file = os.path.join(
                os.path.dirname(self._path_file), f"{base_name}_ascii.gif"
            )  # Replace with your desired output path

        # Create GIF animation
        images[0].save(
            output_file,
            save_all=True,
            append_images=images,
            duration=duration,
            loop=0,  # 0 means loop forever
        )

        # print(output_file)
        return Image.open(output_file)

    # сохранение ASCII-арт в файл
    def save_to_file(self, output_file: str = None, duration: float = 0.2) -> None:
        """
        Сохранение ASCII-арт в текстовый файл или GIF-анимацию.
        :param output_file: путь к файлу, в который будет сохранен ASCII-арт (по умолчанию, тот же путь, что и изображение/GIF)
        :param duration: длительность каждого кадра в секундах
        """
        if not self.__frames:
            print("No frames or path_file to save.")
            return

        if output_file == None:
            # Получение имени файла без расширения из path_file
            base_name = os.path.splitext(os.path.basename(self._path_file))[0]
            # Формирование пути для сохранения
            output_file = os.path.join(
                os.path.dirname(self._path_file), f"{base_name}.txt"
            )

        with open(output_file, "w", encoding="utf-8") as f:
            f.write("\n".join(self.__frames))
        return
