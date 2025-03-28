import tkinter as tk
from tkinter import filedialog, messagebox
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageTk
import os


class ImageGrayConverter:
    def __init__(self, master):
        self.master = master
        master.title("Conversor de Imagem para Escala de Cinza")
        master.geometry("600x500")

        # Variável para armazenar o caminho da imagem
        self.image_path = None
        self.original_image = None

        # Botão para selecionar imagem
        self.select_button = tk.Button(
            master,
            text="Selecionar Imagem",
            command=self.load_image,
            font=("Arial", 12)
        )
        self.select_button.pack(pady=10)

        # Checkbox para escolher tipo de conversão
        self.luma_var = tk.BooleanVar()
        self.luma_checkbox = tk.Checkbutton(
            master,
            text="Usar Coeficientes Luma",
            variable=self.luma_var,
            font=("Arial", 10)
        )
        self.luma_checkbox.pack(pady=5)

        # Botão para converter
        self.convert_button = tk.Button(
            master,
            text="Converter para Escala de Cinza",
            command=self.convert_to_gray,
            state=tk.DISABLED,
            font=("Arial", 12)
        )
        self.convert_button.pack(pady=10)

        # Label para mostrar imagens
        self.image_label = tk.Label(master)
        self.image_label.pack(pady=10)

    def load_image(self):
        # Abre diálogo para selecionar imagem
        file_path = filedialog.askopenfilename(
            filetypes=[
                ("Imagens", "*.png *.jpg *.jpeg *.bmp *.gif"),
                ("Todos os arquivos", "*.*")
            ]
        )

        if file_path:
            try:
                # Carrega a imagem
                self.original_image = plt.imread(file_path)
                self.image_path = file_path

                # Habilita botão de conversão
                self.convert_button.config(state=tk.NORMAL)

                # Mostra miniatura da imagem original
                self.show_image(self.original_image)

            except Exception as e:
                messagebox.showerror("Erro", f"Não foi possível carregar a imagem: {str(e)}")

    def convert_to_gray(self):
        if self.original_image is None:
            messagebox.showwarning("Aviso", "Selecione uma imagem primeiro")
            return

        # Verifica se a imagem tem 3 canais
        if len(self.original_image.shape) < 3:
            messagebox.showwarning("Aviso", "A imagem já está em escala de cinza")
            return

        # Parâmetros de conversão
        if self.luma_var.get():
            params = [0.299, 0.589, 0.114]
            metodo = "Luma"
        else:
            params = [0.2125, 0.7154, 0.0721]
            metodo = "Padrão"

        # Conversão
        gray_image = np.ceil(np.dot(self.original_image[..., :3], params))
        gray_image[gray_image > 255] = 255

        # Salva imagem convertida no mesmo diretório
        if self.image_path:
            base, ext = os.path.splitext(self.image_path)
            gray_path = f"{base}_gray{ext}"
            plt.imsave(gray_path, gray_image, cmap='gray')
            messagebox.showinfo("Sucesso", f"Imagem convertida com método {metodo}.\nSalva em: {gray_path}")

        # Mostra imagem convertida
        self.show_image(gray_image, is_gray=True)

    def show_image(self, image, is_gray=False):
        # Redimensiona a imagem para caber na interface
        height = 300
        aspect = image.shape[1] / image.shape[0]
        new_width = int(height * aspect)

        # Redimensiona a imagem
        resized_image = Image.fromarray(
            image.astype('uint8') if is_gray else (image * 255).astype('uint8')
        )
        resized_image = resized_image.resize((new_width, height), Image.LANCZOS)

        # Converte para PhotoImage do Tkinter
        tk_image = ImageTk.PhotoImage(resized_image)

        # Mostra a imagem
        self.image_label.config(image=tk_image)
        self.image_label.image = tk_image


def main():
    root = tk.Tk()
    app = ImageGrayConverter(root)
    root.mainloop()


if __name__ == "__main__":
    main()