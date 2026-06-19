# Panduan Template JSON Dataset

Folder `data/` ini menampung berbagai file dataset dalam format JSON yang digunakan oleh simulasi *Last-Mile Delivery*.

Setiap file `.json` wajib mengikuti struktur (skema) berikut agar dapat dibaca oleh `src/main.py` dan algoritma utama tanpa menyebabkan *error*.

## Struktur Dasar JSON

```json
{
  "description": "dataset diambil dari hub di berbagai tempat real",
  "locations": [
    "Hub Pusat Gedebage", "Jatinangor", "Cileunyi", "Cibiru", "Tanjungsari",
    "Ujung Berung", "Rancaekek", "Antapani", "Pamulihan", "Buah Batu", "Sumedang Selatan"
  ],
  #berat dari paket tiap hub
  "package_weights": [
    0, 2.5, 1.0, 3.0, 1.5, 5.0, 2.0, 1.2, 4.0, 3.5, 2.2
  ],

  # jarak dari hub ke hub lain
  # 0.0 berarti tempat itu sendiri, (0,0) -> hub pusat, (1,2) -> hub Jatinangor, dst
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

## Penjelasan Properti / Key

1. **`description`**
   - Dataset greedyTrap.json untuk menjebak algoritma Greedy pada 5 titik awal. untuk pengecekan
   - Dataset heavyLoads.json untuk mengecek kasus beban berat pada pengiriman untuk melihat seberapa pengaruh beban pada bbm yang terpakai.
   - Dataset locate.json adalah dataset utama yang menggunakan tempat real untuk melakukan pengecekan algoritma ini

2. **`locations`** (Array of Strings)
   daftar nama titik (node). 
   - node indeks ke-0 (paling awal) **wajib** merupakan "Hub Pusat" atau tempat awal keberangkatan kurir.
   - sisa elemennya adalah pelanggan-pelanggan tujuan.

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
