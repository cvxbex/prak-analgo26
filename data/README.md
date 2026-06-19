# Panduan Template JSON Dataset

Folder `data/` ini menampung berbagai file dataset dalam format JSON yang digunakan oleh simulasi *Last-Mile Delivery*.

Setiap file `.json` wajib mengikuti struktur (skema) berikut agar dapat dibaca oleh `src/main.py` dan algoritma utama tanpa menyebabkan *error*.

## Struktur Dasar JSON

```json
{
  "description": "Deskripsi singkat mengenai skenario dataset ini (misal: Dataset Beban Ekstrem)",
  "locations": [
    "Hub Pusat",
    "Pelanggan 1",
    "Pelanggan 2",
    "..."
  ],
  "package_weights": [
    0,
    1.5,
    3.0,
    "..."
  ],
  "distance_matrix": [
    [0.0, 4.2, 5.1],
    [4.2, 0.0, 1.5],
    [5.1, 1.5, 0.0]
  ],
  "scenarios": {
    "subsidi": 5000,
    "krisis": 20000
  }
}
```

## Penjelasan Properti / Key

1. **`description`** (String) *[Opsional]*
   disini berisikan penjelasan singkat atau tujuan dari dataset ini. contoh: "Dataset ini menjebak algoritma Greedy pada 5 titik awal". Deskripsi ini akan dicetak di terminal saat simulasi berjalan.

2. **`locations`** (Array of Strings) *[Wajib]*
   daftar nama titik (node). 
   - node indeks ke-0 (paling awal) **wajib** merupakan "Hub Pusat" atau tempat awal keberangkatan kurir.
   - sisa elemennya adalah pelanggan-pelanggan tujuan.

3. **`package_weights`** (Array of Floats/Integers) *[Wajib]*
   daftar beban barang (dalam satuan kilogram) untuk masing-masing titik yang bersesuaian urutannya dengan `locations`.
   - indeks ke-0 (Hub) disarankan bernilai `0` karena hub tidak menerima barang.
   - nilai ini akan diproses secara dinamis pada fungsi *Cost* untuk memengaruhi rasio pemakaian bensin per kilometernya.

4. **`distance_matrix`** (2D Array of Floats) *[Wajib]*
   matriks ketetanggaan (Adjacency Matrix) yang mewakili bobot jarak antar titik dalam kilometer (km).
   - ukuran baris dan kolom **harus sama (N x N)**, di mana N adalah jumlah elemen pada `locations`.
   - nilai diagonal matriks `distance_matrix[i][i]` harus `0`.
   - direkomendasikan menggunakan bentuk simetris (jarak A ke B sama dengan B ke A), walau kode algoritma eksak tetap bisa berjalan dengan metrik asimetris.

5. **`scenarios`** (Object/Dictionary) *[Wajib]*
   menyimpan parameter harga untuk variabel skenario ekonomi utama. 
   - `subsidi`: Harga bensin per liter saat subsidi (contoh: 5000).
   - `krisis`: Harga bensin per liter saat krisis energi (contoh: 20000).

## Aturan Tambahan
* pastiin panjang array `locations`, `package_weights`, serta ukuran dimensi `distance_matrix` **selalu sama**. Jika ada 11 titik, matriksnya harus `11x11`.
* Tidak ada batasan jumlah lokasi untuk algorima Heuristik (Greedy). Namun untuk algoritma Eksak (DFS Pruning), amat sangat disarankan membatasi **maksimal 11-13 node** karena sifat kompleksitasnya yang berbentuk Faktorial ($O(N!)$). Menaruh angka lebih dari itu bisa membuat program menggantung (hang) karena lamanya eksekusi.
