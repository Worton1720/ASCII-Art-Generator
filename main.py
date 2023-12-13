import ASCIIArtGenerator
from tkinter import Tk, filedialog


def main():
    print("1 - img to ascii \n2 - gif")
    cher = int(input("File type: "))
    if cher not in [1, 2]:
        print("no such option")
        exit(1)

    # Создаем главное окно
    root = Tk()
    root.withdraw()  # Скрываем окно

    while True:
        # Просим пользователя выбрать файл
        file_path = filedialog.askopenfilename(title="Выберите файл")
        if file_path != "":
            print("File path: ", file_path)
            break
    if cher == 2:
        print("1 - ascii to gif \n2 - gif to png")
        cher = int(input(">_ "))
        if cher not in [1, 2]:
            print("no such option")
            exit(1)
        else:
            save_factor = True if save_factor == 2 else False
        if save_factor:
            ag.gif_to_png(file_path)
            exit(1)

    scale_factor = int(input("Enter the scale factor: ") or 10)

    font_size = int(input("Enter the font size: ") or 5)

    while True:
        save_factor = str(input("Save?(y, n): ")).lower()
        if save_factor in ["y", "n"]:
            save_factor = True if save_factor == "y" else False
            break

    ag = ASCIIArtGenerator(scale_factor)
    if cher == 1:
        ag.ascii_to_image(ag.image_to_ascii(file_path), font_size=font_size)
        if save_factor:
            ag.save_to_file()

    elif cher == 2:
        speed_gif = float(input("speed gif (miliseconds): "))
        ag.ascii_to_gif(
            ag.gif_to_ascii(file_path),
            font_size=font_size,
            save_factor=save_factor,
            duration=speed_gif,
        )
        if save_factor:
            ag.save_to_file()


if __name__ == "__main__":
    main()
