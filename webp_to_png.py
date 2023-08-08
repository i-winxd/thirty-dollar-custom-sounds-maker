from PIL import Image
import os


def convert_webp_to_png(input_file: str) -> None:
    output_file = os.path.splitext(input_file)[0] + ".png"
    im = Image.open(input_file)
    im.save(output_file, "PNG")
    print(f"Converted {input_file} to {output_file}")


def convert_webp_files_recursive(directory: str) -> None:
    for root, _, files in os.walk(directory):
        for filename in files:
            if filename.lower().endswith(".webp"):
                input_file = os.path.join(root, filename)
                convert_webp_to_png(input_file)


def main() -> None:
    current_directory = os.getcwd()
    convert_webp_files_recursive(current_directory)


if __name__ == "__main__":
    main()
