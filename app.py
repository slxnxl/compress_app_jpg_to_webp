import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ExifTags


class ImageConverterApp:
    def __init__(self, master):
        self.master = master
        master.title("Image Converter")

        self.label = tk.Label(master, text="Выберите изображение для конвертации:")
        self.label.pack()

        self.button_browse = tk.Button(master, text="Обзор", command=self.browse_file)
        self.button_browse.pack()

        self.label_filename = tk.Label(master, text="")
        self.label_filename.pack()

        self.label_quality = tk.Label(master, text="Выберите качество изображения:")
        self.label_quality.pack()

        self.scale_quality = tk.Scale(master, from_=0, to=100, orient=tk.HORIZONTAL)
        self.scale_quality.set(80)
        self.scale_quality.pack()

        self.button_convert = tk.Button(master, text="Конвертировать", command=self.convert_image)
        self.button_convert.pack()

    def browse_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("JPG files", "*.JPG")])
        if file_path:
            self.label_filename.config(text=f"Выбран файл: {file_path}")
            self.file_path = file_path

    def convert_image(self):
        if hasattr(self, 'file_path'):
            quality = self.scale_quality.get()
            output_path = filedialog.asksaveasfilename(defaultextension=".webp", filetypes=[("WebP files", "*.webp")])
            if output_path:
                try:
                    image = Image.open(self.file_path)

                    # Удаление метаданных EXIF
                    if hasattr(image, '_getexif'):
                        exif_data = image._getexif()
                        if exif_data:
                            exif_copy = exif_data.copy()  # Создаем копию словаря, чтобы избежать ошибки "dictionary changed size during iteration"
                            for tag, value in exif_copy.items():
                                decoded = ExifTags.TAGS.get(tag, tag)
                                if decoded == 'Orientation':
                                    del exif_data[tag]
                            image.save(output_path, 'WEBP', quality=quality, exif=image.info.get('exif'))
                        else:
                            image.save(output_path, 'WEBP', quality=quality)
                    else:
                        image.save(output_path, 'WEBP', quality=quality)

                    messagebox.showinfo("Готово", "Изображение успешно сконвертировано в формат WebP!")
                except Exception as e:
                    messagebox.showerror("Ошибка", f"Ошибка конвертации: {str(e)}")


if __name__ == "__main__":
    root = tk.Tk()
    app = ImageConverterApp(root)
    root.mainloop()
