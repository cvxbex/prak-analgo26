# Panduan Template JSON Dataset

Folder `data/` ini menampung berbagai file dataset dalam format JSON yang digunakan oleh simulasi *Last-Mile Delivery*.

Setiap file `.json` wajib mengikuti struktur (skema) berikut agar dapat dibaca oleh `src/main.py` dan algoritma utama tanpa menyebabkan *error*.

## Struktur Dasar JSON
contoh : 
```json
{
  "description": "dataset diambil dari sala satu hub dan berbagai tempat real untuk pelanggan",
  "locations": [
    "Hub Pusat Gedebage", "Jatinangor", "Cileunyi", "Cibiru", "Tanjungsari",
    "Ujung Berung", "Rancaekek", "Antapani", "Pamulihan", "Buah Batu", "Sumedang Selatan"
  ],
  #berat dari paket tiap pelanggan
  "package_weights": [
    0, 2.5, 1.0, 3.0, 1.5, 5.0, 2.0, 1.2, 4.0, 3.5, 2.2
  ],

  # jarak dari hub ke daerah pelanggan
  # 0.0 berarti tempat itu sendiri, (0,0) -> hub pusat, (1,2) -> pelanggan daerah Jatinangor, dst
  "distance_matrix": [
    [0.0, 4.2, 5.1, 6.3, 7.5, 12.0, 3.5, 8.1, 14.5, 15.2, 18.0],
    [4.2, 0.0, 1.5, 3.2, 4.1, 9.5, 2.0, 5.0, 11.2, 12.5, 15.0],
    [5.1, 1.5, 0.0, 2.5, 3.8, 8.8, 1.8, 4.5, 10.5, 11.8, 14.2],
    [6.3, 3.2, 2.5, 0.0, 2.1, 7.5, 3.0, 3.8, 9.2, 10.5, 13.0],
    [7.5, 4.1, 3.8, 2.1, 0.0, 6.2, 4.5, 2.5, 8.0, 9.5, 12.5],
    [12.0, 9.5, 8.8, 7.5, 6.2, 0.0, 10.0, 8.5, 3.5, 4.2, 17.5],
    [3.5, 2.0, 1.8, 3.0, 4.5, 10.0, 0.0, 5.5, 12.0, 13.5, 14.5],
    [8.1, 5.0, 4.5, 3.8, 2.5, 8.5, 5.5, 0.0, 7.2, 8.0, 14.0],
    [14.5, 11.2, 10.5, 9.2, 8.0, 3.5, 12.0, 7.2, 0.0, 2.5, 19.5],
    [15.2, 12.5, 11.8, 10.5, 9.5, 4.2, 13.5, 8.0, 2.5, 0.0, 21.0],
    [18.0, 15.0, 14.2, 13.0, 12.5, 17.5, 14.5, 14.0, 19.5, 21.0, 0.0]
  ],
  # harga dari bbm
  "scenarios": {
    "subsidi": 5000,
    "krisis": 20000
  }
}
```

# Cara Menjalankan Program
  "python main.py --scenario all --dataset all"
  -> Perintah ini akan memproses semua file JSON sekaligus, mengeksekusi perhitungan rute, dan menampilkan perbandingan biayanya

# Pemilihan Algoritma
Program ini mengimplementasikan dua algoritma untuk memecahkan Travelling Salesperson Problem (TSP) dengan pertimbangan bobot muatan:
##Algoritma Heuristik (Greedy): Dipilih karena kecepatannya. Algoritma ini mencari titik terdekat selanjutnya dari titik saat ini (Nearest Neighbour).
  - Trade-off: Keunggulannya adalah waktu komputasi yang instan (kurang dari $0.05$ ms). Namun, karena bersifat miopia (hanya melihat keuntungan jangka pendek), algoritma ini rawan terjebak pada Greedy Trap di mana jarak pendek di awal memaksanya mengambil rute memutar yang sangat panjang di akhir, serta kurang optimal mendistribusikan beban paket berat.
##Algoritma Eksak (Branch and Bound dengan DFS): Dipilih karena memberikan jaminan hasil yang 100% optimal dengan rute keseluruhan terpendek dan pertimbangan konsumsi BBM paling hemat.
  - Trade-off: Memiliki Total Cost rute paling murah, tetapi mengorbankan biaya komputasi yang luar biasa besar (tercatat melonjak hingga di atas $300$ ms untuk 11 lokasi). Biaya server komputasi meningkat drastis seiring bertambahnya titik lokasi.

# Analisis Kompleksitas
##Algoritma Eksak (Branch and Bound DFS)
- Kompleksitas Waktu: O(N!)
  Penjelasan: Menggunakan penelusuran Depth First Search (DFS), fungsi rekursif akan mencoba seluruh permutasi rute yang mungkin. Walaupun terdapat mekanisme pruning (memotong cabang rekursi jika current_fuel_cost >= best_fuel_cost), pada kasus terburuk (worst-case) di mana semua cabang harus diperiksa, waktu komputasi tetap akan bertumbuh secara faktorial terhadap jumlah lokasi (N).

- Kompleksitas Ruang: O(N)
  Penjelasan: Memori tambahan dialokasikan murni untuk call stack akibat rekursi dengan kedalaman maksimal N, serta dua buah array/list (visited dan current_route) yang berukuran N.

##Algoritma Heuristik (Greedy)
- Kompleksitas Waktu: O(N^2)
  Penjelasan: Terdapat nested loop pada fungsi greedy_tsp. Loop luar berjalan sebanyak N-1 kali untuk menentukan titik selanjutnya, sedangkan loop dalam melakukan iterasi sebanyak N kali untuk menyeleksi jarak minimum dari lokasi saat ini.

- Kompleksitas Ruang: O(N)
  Penjelasan: Kompleksitas memori sangat efisien. Tidak ada rekursi yang menumpuk di memori; algoritma hanya memerlukan array satu dimensi visited dan route untuk menyimpan urutan berukuran konstan N.

# Kesimpulan
Dalam menentukan algoritma terbaik secara bisnis, kita menghitung Total Cost of Ownership (TCO) yang merupakan akumulasi dari biaya BBM ditambah biaya server komputasi (ditetapkan sebesar 50 Rupiah per millisecond eksekusi).
Titik impas (Break-Even Point/BEP) harga bensin—di mana Algoritma Eksak mulai lebih menguntungkan—sangat fluktuatif tergantung distribusi lokasi dan bobot:
  - Pada Dataset Normal (penyebaran merata), penghematan BBM dari Algoritma Eksak kecil (karena jarak rute hampir mirip), sementara lonjakan biaya komputasinya tinggi. Titik Break-Even baru tercapai ketika harga BBM menyentuh Rp 41.055 / liter. Di bawah harga ini, algoritma Heuristik jauh lebih untung.
  - Pada Dataset Heavy Loads (beban ekstrem), efisiensi BBM dari algoritma Eksak melonjak. Titik Break-Even bergeser drastis ke Rp 10.191 / liter.
  - Pada kasus Greedy Trap, rute acak Heuristik sangat melenceng dan boros BBM, sehingga Titik Break-Even sudah tercapai di angka harga bensin Rp 2.732 / liter.
Kesimpulan: Mengingat harga subsidi maupun krisis BBM di dunia nyata berada pada rentang Rp 5.000 hingga Rp 20.000 per liter, bisnis disarankan menggunakan model hibrida. Secara default, terapkan algoritma Heuristik (Greedy) untuk pengiriman reguler/normal agar server tidak terbebani. Namun, rancang pemicu sistem untuk secara otomatis beralih menggunakan algoritma Eksak (Branch & Bound) hanya jika terdeteksi adanya paket dengan overweight atau sebaran titik rawan yang memenuhi kriteria Greedy Trap.

## Penjelasan Properti / Key
1. **`description`**
   - Dataset greedyTrap.json untuk menjebak algoritma Greedy pada 5 titik awal. untuk pengecekan
   - Dataset heavyLoads.json untuk mengecek kasus beban berat pada pengiriman untuk melihat seberapa pengaruh beban pada bbm yang terpakai.
   - Dataset locate.json adalah dataset utama yang menggunakan tempat real untuk melakukan pengecekan algoritma ini

2. **`locations`** (Array of Strings)
   daftar nama titik (node). 
   - node indeks ke-0 (paling awal) **wajib** merupakan "Hub Pusat" atau tempat awal keberangkatan kurir.
   - sisa elemennya adalah daerah pelanggan-pelanggan tujuan.

3. **`package_weights`**
   daftar beban barang (dalam satuan kilogram) untuk masing-masing titik yang bersesuaian urutannya dengan `locations`.
   - indeks ke-0 (Hub) disarankan bernilai `0` karena hub tidak menerima barang.
   - nilai akan diproses secara dinamis pada fungsi *Cost* untuk memengaruhi rasio pemakaian bensin per kilometernya.

4. **`distance_matrix`** (2D Array of Floats)
   matriks ketetanggaan (Adjacency Matrix) yang mewakili bobot jarak antar titik dalam kilometer (km).
   - ukuran baris dan kolom **harus sama (N x N)**, di mana N adalah jumlah elemen pada `locations`.
   - nilai diagonal matriks `distance_matrix[i][i]` harus `0`.
   - direkomendasikan menggunakan bentuk simetris (jarak A ke B sama dengan B ke A), walau kode algoritma eksak tetap bisa berjalan dengan metrik asimetris.

5. **`scenarios`**
   menyimpan parameter harga untuk variabel skenario ekonomi utama. 
   - `subsidi`: 5000.
   - `krisis`: 20000.

## Aturan Tambahan
* pastiin panjang array `locations`, `package_weights`, serta ukuran dimensi `distance_matrix` **selalu sama**. Jika ada 11 titik, matriksnya `11x11`.
* Tidak ada batasan jumlah lokasi untuk algorima Heuristik (Greedy). Namun untuk algoritma Eksak (DFS Pruning), amat sangat disarankan membatasi **maksimal 11-13 node** karena sifat kompleksitasnya yang berbentuk Faktorial ($O(N!)$). Menaruh angka lebih dari itu bisa membuat program menggantung (hang) karena lamanya eksekusi.
