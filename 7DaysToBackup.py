import os
import shutil
from tkinter import Tk, Listbox, Button, END, messagebox, Label
from datetime import datetime

# Yedekleme işlemini gerçekleştiren fonksiyon
def backup_folder(selected_map, selected_save):
    source_path = os.path.join(appdata_path, selected_map, selected_save)
    backup_date = datetime.now().strftime("_backup_%Y%m%d_%H%M%S")
    destination_path = f"{source_path}{backup_date}"

    try:
        shutil.copytree(source_path, destination_path)
        messagebox.showinfo("Başarılı", f"Yedekleme başarılı: {destination_path}")
    except Exception as e:
        messagebox.showerror("Hata", f"Yedekleme sırasında bir hata oluştu: {str(e)}")
# Silme işlemini gerçekleştiren fonksiyon       
def delete_folder(selected_map, selected_save):
    source_path = os.path.join(appdata_path, selected_map, selected_save)
    user_response = messagebox.askyesno("Onay", f"'{selected_save}' Dosyasını silmek istediğinize emin misiniz?")
    if user_response:
        try:
            shutil.rmtree(source_path)
            messagebox.showinfo("Başarılı", f"Silme başarılı: {source_path}")
        except Exception as e:
            messagebox.showerror("Hata", f"Silme sırasında bir hata oluştu: {str(e)}")
    else:
        messagebox.showinfo("İptal", "Silme işlemi iptal edildi.")

# Save dosyalarını listelemek için fonksiyon
def list_saves(event):
    selected_map = map_listbox.get(map_listbox.curselection())
    save_listbox.delete(0, END)
    saves_path = os.path.join(appdata_path, selected_map)
    for save in os.listdir(saves_path):
        save_listbox.insert(END, save)

# Yedekleme işlemini başlatan fonksiyon
def start_backup():
    selected_map = map_listbox.get(map_listbox.curselection())
    selected_save = save_listbox.get(save_listbox.curselection())
    backup_folder(selected_map, selected_save)
    list_saves('<<ListboxSelect>>')

def delete_backup():
    selected_map = map_listbox.get(map_listbox.curselection())
    selected_save = save_listbox.get(save_listbox.curselection())
    delete_folder(selected_map, selected_save)
    list_saves('<<ListboxSelect>>')    

# Tkinter arayüzünün oluşturulması
root = Tk()
root.title("7 Days To Die Save Yedekleme Aracı")
root.geometry("500x400")  # Pencere boyutunu başlangıçta ayarla

appdata_path = os.path.expandvars(r"%appdata%\7DaysToDie\Saves")

map_listbox = Listbox(root, height=10, exportselection=0)
map_listbox.bind('<<ListboxSelect>>', list_saves)

save_listbox = Listbox(root, height=10)
backup_button = Button(root, text="Yedekle", command=start_backup)
delete_button = Button(root, text="Sil", command=delete_backup)

# Grid yöneticisi kullanarak widget'ları yerleştir ve boşluk bırak
Label(root, text="Map Listesi").grid(row=0, column=0, sticky='ew', padx=10, pady=5)
map_listbox.grid(row=1, column=0, sticky='nsew', padx=10, pady=5)

Label(root, text="Save Listesi").grid(row=0, column=1, sticky='ew', padx=10, pady=5)
save_listbox.grid(row=1, column=1, sticky='nsew', padx=10, pady=5)

backup_button.grid(row=2, column=0, columnspan=2, sticky='ew', padx=10, pady=10)
delete_button.grid(row=3, column=0, columnspan=2, sticky='ew', padx=10, pady=10)

# Grid sütunlarının ve satırlarının ağırlıklarını ayarla
root.grid_columnconfigure(0, weight=1, pad=10)
root.grid_columnconfigure(1, weight=1, pad=10)
root.grid_rowconfigure(1, weight=1, pad=10)

# Map listesinin doldurulması


for map_name in os.listdir(appdata_path):
    map_listbox.insert(END, map_name)

root.mainloop()
