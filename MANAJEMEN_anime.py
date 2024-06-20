import tkinter as tk
from tkinter import messagebox, filedialog
import csv

FILE_DATA_PENGGUNA = 'users.csv'

class Node:
    def _init_(self, data):
        self.data = data
        self.next = None

class CircularlyLinkedList:
    def _init_(self):
        self.head = None

    def append(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            self.head.next = self.head
        else:
            temp = self.head
            while temp.next != self.head:
                temp = temp.next
            temp.next = new_node
            new_node.next = self.head

    def display(self):
        if self.head:
            nodes = []
            temp = self.head
            while True:
                nodes.append(temp.data)
                temp = temp.next
                if temp == self.head:
                    break
            return nodes
        else:
            return []

    def get_node(self, index):
        if self.head:
            temp = self.head
            count = 0
            while True:
                if count == index:
                    return temp.data
                count += 1
                temp = temp.next
                if temp == self.head:
                    break
        return None

    def remove(self, index):
        if not self.head:
            return False
        temp = self.head
        prev = None
        count = 0
        while True:
            if count == index:
                if prev is None:  # Menghapus kepala
                    if temp.next == self.head:  # Hanya satu node
                        self.head = None
                    else:
                        last = self.head
                        while last.next != self.head:
                            last = last.next
                        last.next = temp.next
                        self.head = temp.next
                else:
                    prev.next = temp.next
                return True
            prev = temp
            temp = temp.next
            count += 1
            if temp == self.head:
                break
        return False

def pastikan_file_pengguna():
    try:
        with open(FILE_DATA_PENGGUNA, mode='r', newline='') as file:
            pass
    except FileNotFoundError:
        with open(FILE_DATA_PENGGUNA, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["username", "password", "animes"])

def pengguna_ada(username):
    with open(FILE_DATA_PENGGUNA, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['username'] == username:
                return True
    return False

def validasi_login(username, password):
    with open(FILE_DATA_PENGGUNA, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['username'] == username and row['password'] == password:
                return True
    return False

def daftar_pengguna(username, password):
    with open(FILE_DATA_PENGGUNA, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([username, password, ""])

def dapatkan_anime_pengguna(username):
    with open(FILE_DATA_PENGGUNA, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['username'] == username:
                return row.get('animes', '').split(';') if row.get('animes') else []
    return []

def tambah_anime_pengguna(username, anime):
    pengguna = []
    with open(FILE_DATA_PENGGUNA, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['username'] == username:
                row['animes'] = row['animes'] + ';' + anime if row['animes'] else anime
            pengguna.append(row)
    
    with open(FILE_DATA_PENGGUNA, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=["username", "password", "animes"])
        writer.writeheader()
        writer.writerows(pengguna)

def hapus_anime_pengguna(username, index):
    pengguna = []
    with open(FILE_DATA_PENGGUNA, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['username'] == username:
                animes = row['animes'].split(';')
                if index < len(animes):
                    del animes[index]
                row['animes'] = ';'.join(animes)
            pengguna.append(row)
    
    with open(FILE_DATA_PENGGUNA, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=["username", "password", "animes"])
        writer.writeheader()
        writer.writerows(pengguna)

def urutkan_anime_pengguna(username):
    animes = dapatkan_anime_pengguna(username)
    animes.sort()
    pengguna = []
    with open(FILE_DATA_PENGGUNA, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['username'] == username:
                row['animes'] = ';'.join(animes)
            pengguna.append(row)
    
    with open(FILE_DATA_PENGGUNA, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=["username", "password", "animes"])
        writer.writeheader()
        writer.writerows(pengguna)

def cari_anime_pengguna(username, anime):
    animes = dapatkan_anime_pengguna(username)
    try:
        return animes.index(anime)
    except ValueError:
        return -1

class AnimeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Pengelola Anime")
        self.root.geometry("600x400")
        self.username = None
        self.playlist = CircularlyLinkedList()

        # Definisikan frame
        self.login_frame = tk.Frame(self.root, padx=20, pady=20)
        self.main_frame = tk.Frame(self.root, padx=20, pady=20)
        self.register_frame = tk.Frame(self.root, padx=20, pady=20)
        self.add_anime_frame = tk.Frame(self.root, padx=20, pady=20)
        self.view_anime_frame = tk.Frame(self.root, padx=20, pady=20)
        self.remove_anime_frame = tk.Frame(self.root, padx=20, pady=20)
        self.sort_anime_frame = tk.Frame(self.root, padx=20, pady=20)
        self.search_anime_frame = tk.Frame(self.root, padx=20, pady=20)

        # Pengaturan frame
        self.setup_login_frame()
        self.setup_register_frame()
        self.setup_main_frame()
        self.setup_add_anime_frame()
        self.setup_view_anime_frame()
        self.setup_remove_anime_frame()
        self.setup_sort_anime_frame()
        self.setup_search_anime_frame()

        # Mulai dengan frame login
        self.login_frame.pack()

    def setup_login_frame(self):
        tk.Label(self.login_frame, text="Login", font=('Arial', 24)).pack(pady=10)
        tk.Label(self.login_frame, text="Username", font=('Arial', 14)).pack(pady=5)
        self.login_username_entry = tk.Entry(self.login_frame, font=('Arial', 14), width=30)
        self.login_username_entry.pack(pady=5)
        tk.Label(self.login_frame, text="Password", font=('Arial', 14)).pack(pady=5)
        self.login_password_entry = tk.Entry(self.login_frame, font=('Arial', 14), width=30, show="*")
        self.login_password_entry.pack(pady=5)
        tk.Button(self.login_frame, text="Login", font=('Arial', 14), command=self.login).pack(pady=10)
        tk.Button(self.login_frame, text="Daftar", font=('Arial', 14), command=self.show_register_frame).pack(pady=10)

    def setup_register_frame(self):
        tk.Label(self.register_frame, text="Daftar", font=('Arial', 24)).pack(pady=10)
        tk.Label(self.register_frame, text="Username", font=('Arial', 14)).pack(pady=5)
        self.register_username_entry = tk.Entry(self.register_frame, font=('Arial', 14), width=30)
        self.register_username_entry.pack(pady=5)
        tk.Label(self.register_frame, text="Password", font=('Arial', 14)).pack(pady=5)
        self.register_password_entry = tk.Entry(self.register_frame, font=('Arial', 14), width=30, show="*")
        self.register_password_entry.pack(pady=5)
        tk.Button(self.register_frame, text="Daftar", font=('Arial', 14), command=self.register).pack(pady=10)
        tk.Button(self.register_frame, text="Kembali", font=('Arial', 14), command=self.show_login_frame).pack(pady=10)

    def setup_main_frame(self):
        tk.Label(self.main_frame, text="Menu Utama", font=('Arial', 24)).pack(pady=10)
        tk.Button(self.main_frame, text="Tambah Anime", font=('Arial', 14), command=self.show_add_anime_frame).pack(pady=10)
        tk.Button(self.main_frame, text="Lihat Daftar Anime", font=('Arial', 14), command=self.show_view_anime_frame).pack(pady=10)
        tk.Button(self.main_frame, text="Hapus Anime", font=('Arial', 14), command=self.show_remove_anime_frame).pack(pady=10)
        tk.Button(self.main_frame, text="Impor Anime CSV", font=('Arial', 14), command=self.import_anime_csv).pack(pady=10)
        tk.Button(self.main_frame, text="Urutkan Anime", font=('Arial', 14), command=self.show_sort_anime_frame).pack(pady=10)
        tk.Button(self.main_frame, text="Cari Anime", font=('Arial', 14), command=self.show_search_anime_frame).pack(pady=10)
        tk.Button(self.main_frame, text="Logout", font=('Arial', 14), command=self.logout).pack(pady=10)

    def setup_add_anime_frame(self):
        tk.Label(self.add_anime_frame, text="Tambah Anime", font=('Arial', 24)).pack(pady=10)
        tk.Label(self.add_anime_frame, text="Nama atau Path Anime", font=('Arial', 14)).pack(pady=5)
        self.add_anime_entry = tk.Entry(self.add_anime_frame, font=('Arial', 14), width=30)
        self.add_anime_entry.pack(pady=5)
        tk.Button(self.add_anime_frame, text="Tambah", font=('Arial', 14), command=self.add_anime).pack(pady=10)
        tk.Button(self.add_anime_frame, text="Kembali ke Menu", font=('Arial', 14), command=self.show_main_frame).pack(pady=10)

    def setup_view_anime_frame(self):
        tk.Label(self.view_anime_frame, text="Daftar Anime", font=('Arial', 24)).pack(pady=10)
        self.anime_listbox = tk.Listbox(self.view_anime_frame, font=('Arial', 14), width=50, height=10)
        self.anime_listbox.pack(pady=10)

        button_frame = tk.Frame(self.view_anime_frame)
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Urutkan Anime", font=('Arial', 14), command=self.sort_anime).grid(row=0, column=0, padx=5)
        tk.Button(button_frame, text="Kembali ke Menu", font=('Arial', 14), command=self.show_main_frame).grid(row=0, column=1, padx=5)

    def setup_remove_anime_frame(self):
        tk.Label(self.remove_anime_frame, text="Hapus Anime", font=('Arial', 24)).pack(pady=10)
        self.remove_anime_listbox = tk.Listbox(self.remove_anime_frame, font=('Arial', 14), width=50, height=10)
        self.remove_anime_listbox.pack(pady=10)
        
        # Membuat frame untuk menempatkan tombol secara berdampingan
        button_frame = tk.Frame(self.remove_anime_frame)
        button_frame.pack(pady=10)
        
        tk.Button(button_frame, text="Hapus", font=('Arial', 14), command=self.remove_anime).grid(row=0, column=0, padx=5)
        tk.Button(button_frame, text="Kembali ke Menu", font=('Arial', 14), command=self.show_main_frame).grid(row=0, column=1, padx=5)

    def setup_sort_anime_frame(self):
        tk.Label(self.sort_anime_frame, text="Urutkan Anime", font=('Arial', 24)).pack(pady=10)
        tk.Button(self.sort_anime_frame, text="Urutkan", font=('Arial', 14), command=self.sort_anime).pack(pady=10)
        tk.Button(self.sort_anime_frame, text="Kembali ke Menu", font=('Arial', 14), command=self.show_main_frame).pack(pady=10)

    def setup_search_anime_frame(self):
        tk.Label(self.search_anime_frame, text="Cari Anime", font=('Arial', 24)).pack(pady=10)
        tk.Label(self.search_anime_frame, text="Nama Anime", font=('Arial', 14)).pack(pady=5)
        self.search_anime_entry = tk.Entry(self.search_anime_frame, font=('Arial', 14), width=30)
        self.search_anime_entry.pack(pady=5)
        tk.Button(self.search_anime_frame, text="Cari", font=('Arial', 14), command=self.search_anime).pack(pady=10)
        tk.Button(self.search_anime_frame, text="Kembali ke Menu", font=('Arial', 14), command=self.show_main_frame).pack(pady=10)

    def login(self):
        username = self.login_username_entry.get()
        password = self.login_password_entry.get()
        if validasi_login(username, password):
            self.username = username
            self.show_main_frame()
        else:
            messagebox.showerror("Kesalahan Login", "Username atau password salah")

    def register(self):
        username = self.register_username_entry.get()
        password = self.register_password_entry.get()
        if not username or not password:
            messagebox.showerror("Kesalahan Pendaftaran", "Kedua kolom harus diisi")
            return
        if pengguna_ada(username):
            messagebox.showerror("Kesalahan Pendaftaran", "Username sudah ada")
            return
        daftar_pengguna(username, password)
        messagebox.showinfo("Sukses Pendaftaran", "Pengguna berhasil didaftarkan")
        self.show_login_frame()

    def logout(self):
        self.username = None
        self.show_login_frame()

    def add_anime(self):
        anime = self.add_anime_entry.get()
        if anime:
            tambah_anime_pengguna(self.username, anime)
            messagebox.showinfo("Tambah Anime", "Anime berhasil ditambahkan")
            self.add_anime_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Tambah Anime", "Harap masukkan nama atau path anime")

    def show_login_frame(self):
        self.clear_frames()
        self.login_frame.pack()

    def show_register_frame(self):
        self.clear_frames()
        self.register_frame.pack()

    def show_main_frame(self):
        self.clear_frames()
        self.main_frame.pack()

    def show_add_anime_frame(self):
        self.clear_frames()
        self.add_anime_frame.pack()

    def show_view_anime_frame(self):
        self.clear_frames()
        self.anime_listbox.delete(0, tk.END)
        animes = dapatkan_anime_pengguna(self.username)
        for anime in animes:
            self.anime_listbox.insert(tk.END, anime)
        self.view_anime_frame.pack()

    def show_remove_anime_frame(self):
        self.clear_frames()
        self.remove_anime_listbox.delete(0, tk.END)
        animes = dapatkan_anime_pengguna(self.username)
        for anime in animes:
            self.remove_anime_listbox.insert(tk.END, anime)
        self.remove_anime_frame.pack()

    def show_sort_anime_frame(self):
        self.clear_frames()
        self.sort_anime_frame.pack()

    def show_search_anime_frame(self):
        self.clear_frames()
        self.search_anime_frame.pack()

    def sort_anime(self):
        urutkan_anime_pengguna(self.username)
        self.show_view_anime_frame()

    def search_anime(self):
        anime = self.search_anime_entry.get()
        if anime:
            index = cari_anime_pengguna(self.username, anime)
            if index != -1:
                messagebox.showinfo("Cari Anime", f"Anime ditemukan pada indeks {index + 1}")
            else:
                messagebox.showerror("Cari Anime", "Anime tidak ditemukan")
        else:
            messagebox.showerror("Cari Anime", "Harap masukkan nama anime")

    def remove_anime(self):
        selected_index = self.remove_anime_listbox.curselection()
        if selected_index:
            hapus_anime_pengguna(self.username, selected_index[0])
            messagebox.showinfo("Hapus Anime", "Anime berhasil dihapus")
            self.show_remove_anime_frame()
        else:
            messagebox.showerror("Hapus Anime", "Harap pilih anime untuk dihapus")

    def import_anime_csv(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            try:
                with open(file_path, mode='r', newline='') as file:
                    reader = csv.reader(file)
                    for row in reader:
                        anime = row[0]  # Mengasumsikan setiap baris hanya memiliki satu kolom dengan nama anime
                        tambah_anime_pengguna(self.username, anime)
                messagebox.showinfo("Impor Anime CSV", "Anime berhasil diimpor")
            except Exception as e:
                messagebox.showerror("Impor Anime CSV", f"Gagal mengimpor CSV: {e}")

    def clear_frames(self):
        for frame in [self.login_frame, self.main_frame, self.register_frame, self.add_anime_frame, self.view_anime_frame, self.remove_anime_frame, self.sort_anime_frame, self.search_anime_frame]:
            frame.pack_forget()

if __name__ == "__main__":
    pastikan_file_pengguna()
    root = tk.Tk()
    app = AnimeApp(root)
    root.mainloop()
