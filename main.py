import ASCIIArtGenerator
from tkinter import Tk, filedialog

def get_file_path():
    root = Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(title="Выберите файл")
    if file_path == "":
        print("Invalid file path")
        exit(1)
    print("File path:", file_path)
    return file_path

def process_image_conversion(file_path, scale_factor, font_size, save_option, ascii_generator):
    ascii_generator.ascii_to_image(ascii_generator.image_to_ascii(file_path), font_size=font_size)
    if save_option:
        ascii_generator.save_to_file()

def process_gif_conversion(file_path, scale_factor, font_size, save_option, speed_gif, ascii_generator):
    if speed_gif is None:
        speed_gif = float(input("Speed of gif (milliseconds): ") or 1)
    ascii_generator.ascii_to_gif(ascii_generator.gif_to_ascii(file_path), font_size=font_size, duration=speed_gif)
    if save_option:
        ascii_generator.save_to_file()

def main():
    print("1 - img to ascii\n2 - gif")
    file_type = int(input("File type: "))
    if file_type not in [1, 2]:
        print("Invalid option")
        exit(1)

    file_path = get_file_path()
    ascii_generator = ASCIIArtGenerator.ASCIIArtGenerator()

    if file_type == 2:
        print("y - gif to png \nor gif to ascii")
        sub_choice = input("> ").lower()
        if sub_choice == "y":
            ascii_generator.gif_to_png(file_path)
            print("Conversion complete.")
            exit(0)

    scale_factor = int(input("Enter the scale factor: ")) or 100
    font_size = int(input("Enter the font size: ")) or 5
    save_option = str(input("Save the ascii animation to a file? (y/n): ").lower()) == "y"

    ascii_generator = ASCIIArtGenerator.ASCIIArtGenerator(scale_factor)
    
    if file_type == 1:
        process_image_conversion(file_path, scale_factor, font_size, save_option, ascii_generator)
    elif file_type == 2:
        process_gif_conversion(file_path, scale_factor, font_size, save_option, None, ascii_generator)

if __name__ == "__main__":
    main()
