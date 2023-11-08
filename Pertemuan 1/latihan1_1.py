# Import Module
import os
# Folder Path
path = "C:/Users/FEZA/My Drive/00. Drive PC/1.STIS/5. Semester 5/Information Retrieval [IR] P/Pertemuan 1/berita"

# List all files in a directory using os.listdir
print("Print nama file dalam sebuah directory using os.listdir : ")

for file in os.listdir(path):
    if os.path.isfile(os.path.join(path, file)):
        print(file)

print("\nPrint isi file : ")
def read_text_file(file_path):
    with open(file_path, 'r') as f:
        print(f.read())

# iterate through all file
for file in os.listdir(path):
# Check whether file is in text format or not
    if file.endswith(".txt"):
        file_path = f"{path}\{file}"

        # call read text file function
        read_text_file(file_path)

# E. Kode untuk Mencari Informasi dengan Query Tertentu
print("\n")
text_1 = "Wilayah Kamu Sudah 'Bebas' COVID-19? Cek 34 Kab/Kota Zona Hijau Terbaru"
text_2 = "Vaksin COVID-19 Bakal Rutin Setiap Tahun? Tergantung, Ini Penjelasannya"
text_3 = "RI Mulai Suntikkan Booster di 2022, Masihkah Ampuh Lawan Varian Delta Cs?"
query = "COVID-19"
docs = [text_1, text_2, text_3]
print("\nMembaca isi file yang terdapat query 'COVID-19'")
for doc in docs:
    if query in doc:
        print(doc)  

#Penugasan
path = "C:/Users/FEZA/My Drive/00. Drive PC/1.STIS/5. Semester 5/Information Retrieval [IR] P/Pertemuan 1/berita"

queries = ["Corona", "corona"]

print("\n[PENUGASAN] Menampilkan daftar nama dokumen pada folder 'berita' yang terdapat query 'corona' atau 'Corona'.")
for file in os.listdir(path):
    if os.path.isfile(os.path.join(path, file)):
         with open(os.path.join(path, file), 'r', encoding='utf-8') as f:
            content = f.read()
            if any(query in content for query in queries):
                print(file)

# with open(os.path.join(path, file), 'r', encoding='utf-8') as f:
# Ini membuka file untuk dibaca. os.path.join(path, file) 
# menggabungkan direktori path dengan nama file untuk mendapatkan
# jalur lengkap ke file tersebut. 'r' menunjukkan bahwa kita ingin membuka file dalam mode baca. 
# 'utf-8' adalah skema encoding yang digunakan saat membaca file.
