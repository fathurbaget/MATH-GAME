import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random
import pygame

class MathGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Math Games")
        self.root.geometry("1400x750")

        pygame.mixer.init()
        self.sfx_channel = pygame.mixer.Channel(1)
        self.backsound_file = "back.mp3"
        self.sfx_correct = "correct.mp3"
        self.sfx_wrong = "wrongs.mp3"
        self.sfx_win = "sfx win.mp3"
        self.sfx_lose = "loser.mp3"

        self.score = 0
        self.lives = 3
        self.current_game = None

        self.bg_image = Image.open("bcg.jpg").resize((1280, 740))
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)
        self.bg_label = tk.Label(self.root, image=self.bg_photo)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        self.bg_label.lower()

        self.score_label = None
        self.lives_label = None

        self.play_background_music()
        self.create_welcome_screen()

    def play_background_music(self):
        try:
            pygame.mixer.music.load(self.backsound_file)
            pygame.mixer.music.play(-1)
        except Exception as e:
            print("Gagal memutar backsound:", e)

    def stop_background_music(self):
        pygame.mixer.music.stop()

    def play_sfx(self, filename):
        try:
            sound = pygame.mixer.Sound(filename)
            self.sfx_channel.play(sound)
        except Exception as e:
            print(f"Gagal memutar SFX {filename}: {e}")

    def clear_screen(self):
        for widget in self.root.winfo_children():
            if widget not in (self.bg_label, self.score_label, self.lives_label):
                widget.destroy()

    def update_hud(self):
        if self.score_label is None:
            self.score_label = tk.Label(self.root, text=f"Skor: {self.score}",
                                        font=('Montserrat', 18, 'bold'), bg="#FFD54F")
            self.score_label.place(x=20, y=18)
        else:
            self.score_label.config(text=f"Skor: {self.score}")

        if self.lives_label is None:
            self.lives_label = tk.Label(self.root, text=f"Nyawa: {self.lives}",
                                        font=('Montserrat', 18, 'bold'), bg="#FF8A80")
            self.lives_label.place(x=20, y=56)
        else:
            self.lives_label.config(text=f"Nyawa: {self.lives}")

    def create_welcome_screen(self):
        self.clear_screen()
    
        if self.score_label:
            self.score_label.destroy()
            self.score_label = None
        if self.lives_label:
            self.lives_label.destroy()
            self.lives_label = None
        
        self.score, self.lives = 0, 3

        tk.Label(self.root, text="MATH GAMES",
                 font=('Montserrat', 60, 'bold'),
                 bg='#000080', fg='white').place(relx=0.5, rely=0.2, anchor='center')

        tk.Button(self.root, text="PLAY", font=('Montserrat', 30, 'bold'),
                  bg="#009dff", fg="white",
                  command=self.open_game_menu).place(relx=0.5, rely=0.5, anchor='center')

    def open_game_menu(self):
        self.clear_screen()
        self.update_hud()

        tk.Label(self.root, text="Pilih Game",
                 font=('Montserrat', 40, 'bold'),
                 bg="white", fg="black").place(relx=0.5, rely=0.15, anchor='center')

        games = [
            ("Operasi Campuran", 1, '#3498db'),
            ("Tentukan Simbol", 2, '#2ecc71'),
            ("BENAR/SALAH", 3, '#e74c3c')
        ]

        for i, (name, code, color) in enumerate(games):
            tk.Button(self.root, text=name, width=20,
                      font=('Montserrat', 25, 'bold'),
                      bg=color, fg="white",
                      command=lambda c=code: self.game_selected(c)
                      ).place(relx=0.5, rely=0.35 + i * 0.15, anchor='center')

    def game_selected(self, code):
        self.clear_screen()
        self.current_game = code

        game_name = (
            "Operasi Campuran" if code == 1 else
            "Tentukan Simbol" if code == 2 else
            "BENAR/SALAH"
        )

        tk.Label(self.root, text=f"Game: {game_name}",
                 font=('Montserrat', 40, 'bold'),
                 bg="white", fg="black").place(relx=0.5, rely=0.08, anchor='center')

        self.update_hud()

        tk.Button(self.root, text="Kembali ke Menu",
                  font=('Montserrat', 18, 'bold'),
                  bg="#ff8800", fg="white",
                  command=self.create_welcome_screen).place(relx=0.5, rely=0.9, anchor='center')

        self.generate_question()

    def generate_question(self):
        self.clear_screen()
        self.update_hud()

        tk.Button(self.root, text="Kembali ke Menu",
                  font=('Montserrat', 18, 'bold'),
                  bg="#ff8800", fg="white",
                  command=self.create_welcome_screen).place(relx=0.5, rely=0.88, anchor='center')

        if self.current_game == 1:
            self.game_operasi_campuran()
        elif self.current_game == 2:
            self.game_tentukan_simbol()
        else:
            self.game_benar_salah()

    def game_operasi_campuran(self):
        ops = ['+', '-', 'x']
        op1, op2 = random.choice(ops), random.choice(ops)

        if op1 == 'x' and op2 == 'x':
            a, b, c = random.randint(2, 15), random.randint(1, 25), random.randint(2, 10)
        elif op1 == 'x':
            a, b, c = random.randint(2, 5), random.randint(1, 15), random.randint(2, 25)
        elif op2 == 'x':
            a, b, c = random.randint(1, 15), random.randint(2, 25), random.randint(2, 5)
        else:
            a, b, c = random.randint(1, 20), random.randint(1, 15), random.randint(1, 15)

        if op1 == 'x' and op2 in ['+', '-']:
            result = (a * b) + c if op2 == '+' else (a * b) - c
            expression = f"{a} × {b} {op2} {c}"

        elif op2 == 'x' and op1 in ['+', '-']:
            result = a + (b * c) if op1 == '+' else a - (b * c)
            expression = f"{a} {op1} {b} × {c}"

        else:
            temp = a + b if op1 == '+' else a - b if op1 == '-' else a * b
            result = temp + c if op2 == '+' else temp - c if op2 == '-' else temp * c
            expression = f"{a} {op1} {b} {op2} {c}"

        tk.Label(self.root, text="Operasi Campuran",
                 font=('Montserrat', 20, 'bold'), bg="#ffffff").pack(pady=90)

        tk.Label(self.root, text=f"{expression} = ?",
                 font=('Montserrat', 24, 'bold'), bg="#ffffff").pack(pady=5)

        answers = [result]
        while len(answers) < 4:
            wrong = result + random.choice([-8, -5, -3, -2, 2, 3, 5, 8])
            if wrong not in answers:
                answers.append(wrong)

        random.shuffle(answers)

        for ans in answers:
            tk.Button(self.root, text=str(ans),
                      font=('Montserrat', 14), width=12,
                      bg='#ecf0f1',
                      command=lambda a=ans, r=result: self.check_answer(a, r)
                      ).pack(pady=6)

    def game_tentukan_simbol(self):
        a = random.randint(1, 20)
        b = random.randint(1, 15)
        op = random.choice(['+', '-', 'x'])
        result = a + b if op == '+' else a - b if op == '-' else a * b

        tk.Label(self.root, text="Tentukan Simbol",
                 font=('Montserrat', 20, 'bold'),
                 bg="#dff0d8").pack(pady=90)

        tk.Label(self.root, text=f"{a}  ?  {b} = {result}",
                 font=('Montserrat', 24, 'bold'),
                 bg="#b2dfdb").pack(pady=5)

        for symbol in ['+', '-', 'x']:
            tk.Button(self.root, text=symbol, width=10,
                      font=('Montserrat', 14),
                      bg='#f0f0f0',
                      command=lambda s=symbol: self.check_answer_symbol(s, op)
                      ).pack(pady=6)


    def game_benar_salah(self):
        a, b = random.randint(1, 25), random.randint(1, 20)
        op = random.choice(['+', '-', 'x'])

        if op == 'x':
            a, b = random.randint(2, 10), random.randint(2, 15)
            correct = a * b
        elif op == '-':
            a, b = max(a, b), min(a, b)
            correct = a - b
        else:
            correct = a + b

        is_true = random.choice([True, False])
        display = correct if is_true else correct + random.choice([-3, -2, -1, 1, 2, 3])

        tk.Label(self.root, text='BENAR atau SALAH?',
                 font=('Montserrat', 20, 'bold'),
                 bg='#f0f0f0').pack(pady=90)

        tk.Label(self.root, text=f'{a} {op} {b} = {display}',
                 font=('Montserrat', 24, 'bold'),
                 bg='#f0f0f0').pack(pady=5)

        tk.Button(self.root, text='BENAR', width=12,
                  font=('Montserrat', 14),
                  bg='#2ecc71', fg='white',
                  command=lambda: self.check_truth(True, is_true)
                  ).pack(pady=6)

        tk.Button(self.root, text='SALAH', width=12,
                  font=('Montserrat', 14),
                  bg='#e74c3c', fg='white',
                  command=lambda: self.check_truth(False, is_true)
                  ).pack(pady=6)

    def handle_end_condition(self):
        if self.score >= 100:
            self.play_sfx(self.sfx_win)
            messagebox.showinfo("MENANG!", "Selamat — Anda mencapai skor 100!")
            self.create_welcome_screen()
            return True

        if self.lives <= 0:
            self.play_sfx(self.sfx_lose)
            messagebox.showerror("KALAH", "Nyawa Anda habis!")
            self.score = 0
            self.lives = 0
            self.update_hud()
            self.sfx_channel.stop()
            pygame.mixer.music.play(-1)
            self.create_welcome_screen()
            return True

        return False

    def check_answer(self, chosen, correct):
        if chosen == correct:
            self.score += 10
            self.play_sfx(self.sfx_correct)
            messagebox.showinfo("Benar!", "Jawaban tepat!")
            self.sfx_channel.stop()
        else:
            self.lives -= 1
            self.play_sfx(self.sfx_wrong)
            messagebox.showerror("Salah", f"Jawaban benar: {correct}")
            self.sfx_channel.stop()

        self.update_hud()
        if not self.handle_end_condition():
            self.generate_question()

    def check_answer_symbol(self, chosen_symbol, real_symbol):
        if chosen_symbol == real_symbol:
            self.score += 10
            self.play_sfx(self.sfx_correct)
            messagebox.showinfo("Benar!", "Simbol tepat!")
            self.sfx_channel.stop()
        else:
            self.lives -= 1
            self.play_sfx(self.sfx_wrong)
            messagebox.showerror("Salah", f"Simbol yang benar adalah: {real_symbol}")
            self.sfx_channel.stop()

        self.update_hud()
        if not self.handle_end_condition():
            self.generate_question()

    def check_truth(self, chosen, is_true):
        if chosen == is_true:
            self.score += 10
            self.play_sfx(self.sfx_correct)
            messagebox.showinfo("Benar!", "Jawaban tepat!")
            self.sfx_channel.stop()
        else:
            self.lives -= 1
            self.play_sfx(self.sfx_wrong)
            messagebox.showerror("Salah", "Pernyataan tersebut salah!")
            self.sfx_channel.stop()

        self.update_hud()
        if not self.handle_end_condition():
            self.generate_question()



if __name__ == "__main__":
    root = tk.Tk()
    MathGame(root)
    root.mainloop()