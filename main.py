import ASCIIArtGenerator
from tkinter import Tk, filedialog


def get_file_paths():
    root = Tk()
    root.withdraw()
    file_paths_tuple = filedialog.askopenfilenames(
        title="Выберите файлы",
        filetypes=[
            ("All Files", "*.*"),
            ("Image files", "*.png;*.jpg"),
            ("Gif files", "*.gif"),
        ],
    )

    if not file_paths_tuple:
        print("No files selected")
        exit(1)

    # Если выбран только один файл, преобразуем кортеж в список
    file_paths = (
        list(file_paths_tuple)
        if isinstance(file_paths_tuple, tuple)
        else file_paths_tuple
    )

    print("Selected file paths:")
    for file_path in file_paths:
        print(file_path)

    return file_paths


def process_image_conversion(
    file_path: str,
    ascii_generator: ASCIIArtGenerator.ASCIIArtGenerator,
    font_size: int = 7,
    save_option: bool = False,
):
    ascii_generator.ascii_to_image(
        ascii_generator.image_to_ascii(image_path=file_path, show_progress_bar=True),
        font_size=font_size,
        show_progress_bar=True,
    )
    if save_option:
        ascii_generator.save_to_file()


def process_gif_conversion(
    file_path: str,
    ascii_generator: ASCIIArtGenerator.ASCIIArtGenerator,
    font_size: int = 7,
    save_option: bool = False,
    speed_gif: int = 1,
):
    if speed_gif is None:
        speed_gif = float(input("Speed of gif (milliseconds): ") or 1)
    ascii_generator.ascii_to_gif(
        ascii_generator.gif_to_ascii(gif_path=file_path, show_progress_bar=True),
        font_size=font_size,
        duration=speed_gif,
        show_progress_bar=True,
    )
    if save_option:
        ascii_generator.save_to_file()


def main():
    print("1 - img to ascii\n2 - gif")
    file_type = int(input("File type: "))
    if file_type not in [1, 2]:
        print("Invalid option")
        exit(1)

    file_paths = get_file_paths()
    ascii_generator = ASCIIArtGenerator.ASCIIArtGenerator()

    if file_type == 2:
        print("y - gif to png \nor gif to ascii")
        sub_choice = input("> ").lower()
        if sub_choice == "y":
            ascii_generator.gif_to_png(gif_path=file_paths, show_progress_bar=True)
            print("Conversion complete.")
            exit(0)

    scale_factor = int(input("Enter the scale factor: ")) or 100
    font_size = int(input("Enter the font size: ")) or 5
    save_option = (
        str(input("Save the ascii animation to a file? (y/n): ").lower()) == "y"
    )

    ascii_generator = ASCIIArtGenerator.ASCIIArtGenerator(scale_factor=scale_factor)

    for i, file_path in enumerate(file_paths):
        if len(file_paths) == 1:
            print(f"image generated")
        else:
            print(f"image {i+1}/{len(file_paths)}: ")
        if file_type == 1:
            process_image_conversion(
                file_path=file_path,
                font_size=font_size,
                save_option=save_option,
                ascii_generator=ascii_generator,
            )
        elif file_type == 2:
            process_gif_conversion(
                file_path=file_path,
                font_size=font_size,
                save_option=save_option,
                ascii_generator=ascii_generator,
                speed_gif=1,
            )


if __name__ == "__main__":
    main()
