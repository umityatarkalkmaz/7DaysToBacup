import os
import shutil
from tkinter import Tk, Listbox, Button, END, messagebox, Label
from datetime import datetime

# Yedekleme ve Silme işlemleri için ortak fonksiyonlar
def get_selected_paths():
    #Seçilen harita ve save dosyalarının yollarını döndürür.
    selected_map = map_listbox.get(map_listbox.curselection())
    selected_save = save_listbox.get(save_listbox.curselection())
    source_path = os.path.join(appdata_path, selected_map, selected_save)
    return selected_map, selected_save, source_path

def perform_action(action, success_message, error_message):
    #Verilen işlem (action) üzerinde hata kontrolü ile işlem yapar.
    try:
        action()
        messagebox.showinfo("Başarılı", success_message)
    except Exception as e:
        messagebox.showerror("Hata", f"{error_message} - Hata: {str(e)}")

def backup_folder():
    #Yedekleme işlemini gerçekleştirir.
    selected_map, selected_save, source_path = get_selected_paths()
    backup_date = datetime.now().strftime("_backup_%Y.%m.%d-%H.%M.%S")
    destination_path = f"{source_path}{backup_date}"

    shutil.copytree(source_path, destination_path)
    list_saves()

def delete_folder():
    #Silme işlemini gerçekleştirir.
    selected_map, selected_save, source_path = get_selected_paths()
    if messagebox.askyesno("Onay", f"'{selected_save}' dosyasını silmek istediğinize emin misiniz?"):
        shutil.rmtree(source_path)
        list_saves()

# Save dosyalarını listelemek için fonksiyon
def list_saves(event=None):
    #Map seçildiğinde save dosyalarını listeler.
    try:
        selected_map = map_listbox.get(map_listbox.curselection())
        save_listbox.delete(0, END)
        saves_path = os.path.join(appdata_path, selected_map)
        for save in os.listdir(saves_path):
            save_listbox.insert(END, save)
    except IndexError:
        # İlk başta map seçilmemişse hata oluşur, bunu engellemek için
        pass

# Tkinter arayüzünün oluşturulması
root = Tk()
root.title("7 Days To Die Save Yedekleme Aracı")
root.geometry("500x400")  # Pencere boyutunu başlangıçta ayarla

appdata_path = os.path.expandvars(r"%appdata%\7DaysToDie\Saves")

map_listbox = Listbox(root, height=10, exportselection=0)
map_listbox.bind('<<ListboxSelect>>', list_saves)

save_listbox = Listbox(root, height=10)

backup_button = Button(root, text="Yedekle", command=lambda: perform_action(backup_folder, "Yedekleme başarılı", "Yedekleme sırasında bir hata oluştu"))
delete_button = Button(root, text="Sil", command=lambda: perform_action(delete_folder, "Silme başarılı", "Silme sırasında bir hata oluştu"))

# Grid yöneticisi ile widget'ları yerleştir
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
    if os.path.isdir(os.path.join(appdata_path, map_name)):
        map_listbox.insert(END, map_name)

root.mainloop()
