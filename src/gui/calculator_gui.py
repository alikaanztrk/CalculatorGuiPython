import tkinter as tk
from tkinter import ttk

class Calculator:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Modern Hesap Makinesi")
        self.window.geometry("400x600")
        self.window.configure(bg="#2c3e50")
        # Pencere boyutlandırmayı aktif et
        self.window.resizable(True, True)
        self.window.minsize(300, 400)  # Minimum pencere boyutu

        # Ekran
        self.display = tk.Entry(
            self.window,
            width=20,
            font=('Helvetica', 30),
            justify='right',
            bd=10,
            bg="#ecf0f1"
        )
        self.display.grid(row=0, column=0, columnspan=4, padx=10, pady=20, sticky='nsew')

        # Grid yapılandırması - tüm hücrelere ağırlık ver
        self.window.grid_rowconfigure(0, weight=2)  # Ekran satırına daha fazla ağırlık
        for i in range(1, 6):  # Buton satırları
            self.window.grid_rowconfigure(i, weight=1)
        for i in range(4):  # Sütunlar
            self.window.grid_columnconfigure(i, weight=1)

        # Buton düzeni
        self.buttons = [
            'C', '⌫', '%', '/',
            '7', '8', '9', '*',
            '4', '5', '6', '-',
            '1', '2', '3', '+',
            '00', '0', '.', '='
        ]

        # Buton stilleri
        self.styles = {
            'normal': {'bg': '#3498db', 'fg': 'white', 'font': ('Helvetica', 18)},
            'operator': {'bg': '#e67e22', 'fg': 'white', 'font': ('Helvetica', 18)},
            'clear': {'bg': '#e74c3c', 'fg': 'white', 'font': ('Helvetica', 18)},
            'equals': {'bg': '#2ecc71', 'fg': 'white', 'font': ('Helvetica', 18)}
        }

        self.create_buttons()
        
        # Klavye tuşlarını bağla - KeyPress yerine KeyRelease kullanıyoruz
        self.window.bind('<KeyRelease>', self.handle_keypress)
        self.window.bind('<Return>', lambda event: self.click('='))
        self.window.bind('<BackSpace>', lambda event: self.click('⌫'))
        self.window.bind('<Delete>', lambda event: self.click('C'))
        self.window.bind('<space>', lambda event: self.click('C'))  # Boşluk tuşu için

    def create_buttons(self):
        row = 1
        col = 0
        for button in self.buttons:
            # Buton stilini belirle
            style = self.styles['normal']
            if button in ['+', '-', '*', '/', '%']:
                style = self.styles['operator']
            elif button in ['C', '⌫']:
                style = self.styles['clear']
            elif button == '=':
                style = self.styles['equals']

            # Butonu oluştur - width ve height parametrelerini kaldır
            btn = tk.Button(
                self.window,
                text=button,
                bg=style['bg'],
                fg=style['fg'],
                font=style['font'],
                relief='raised',
                bd=3,
                command=lambda x=button: self.click(x)
            )
            # Butonun tüm alana yayılması için sticky parametresini kullan
            btn.grid(row=row, column=col, padx=5, pady=5, sticky='nsew')
            
            col += 1
            if col > 3:
                col = 0
                row += 1

    def click(self, value):
        if value == 'C':
            self.display.delete(0, tk.END)
        elif value == '⌫':
            current = self.display.get()
            self.display.delete(len(current)-1, tk.END)
        elif value == '=':
            try:
                result = eval(self.display.get())
                self.display.delete(0, tk.END)
                self.display.insert(tk.END, str(result))
            except:
                self.display.delete(0, tk.END)
                self.display.insert(tk.END, "Hata")
        elif value == '%':
            try:
                current = self.display.get()
                if current:
                    # Eğer ekranda bir işlem varsa (örn: 100 + 50%)
                    if any(op in current for op in ['+', '-', '*', '/']):
                        parts = current.replace('+', ' + ').replace('-', ' - ').replace('*', ' * ').replace('/', ' / ').split()
                        if len(parts) >= 3:
                            base = float(parts[0])
                            operator = parts[1]
                            percent = float(parts[2]) / 100
                            
                            if operator == '+':
                                result = base + (base * percent)
                            elif operator == '-':
                                result = base - (base * percent)
                            elif operator == '*':
                                result = base * percent
                            elif operator == '/':
                                result = base / percent if percent != 0 else "Hata"
                    else:
                        # Sadece bir sayı varsa direkt yüzdesini al
                        result = float(current) / 100
                    
                    self.display.delete(0, tk.END)
                    self.display.insert(tk.END, str(result))
            except:
                self.display.delete(0, tk.END)
                self.display.insert(tk.END, "Hata")
        else:
            self.display.insert(tk.END, value)

    def handle_keypress(self, event):
        # event.char boş değilse işlem yap
        if event.char and event.char in '0123456789.+-*/%':
            self.click(event.char)
        # Diğer özel tuşlar için event.keysym kullan
        elif event.keysym == 'Return':
            self.click('=')
        elif event.keysym == 'BackSpace':
            self.click('⌫')
        elif event.keysym == 'space':
            self.click('C')

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    calc = Calculator()
    calc.run()