import os
import subprocess

def run_automated_tests():
    # Membuat folder docs jika belum ada
    docs_dir = os.path.join(os.path.dirname(__file__), '..', 'docs')
    os.makedirs(docs_dir, exist_ok=True)
    
    # Menentukan lokasi file output log dan file utama main.py
    output_file = os.path.join(docs_dir, 'simulation_output_log.txt')
    main_script = os.path.join(os.path.dirname(__file__), 'main.py')
    
    print(f"[*] Menjalankan seluruh simulasi pipeline secara otomatis...")
    print(f"[*] Hasil output akan diekspor langsung ke: {output_file}")
    
    # Menjalankan main.py dengan parameter mengeksekusi seluruh dataset dan skenario
    try:
        result = subprocess.run(
            ['python', main_script, '--scenario', 'all', '--dataset', 'all'],
            capture_output=True,
            text=True,
            check=True
        )
        
        # Menulis hasil output terminal ke dalam file teks di folder docs/
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(result.stdout)
            
        print("[+] Sukses! Seluruh log pengujian berhasil dicatat.")
        print(result.stdout[:500] + "\n... (Output lengkap tersimpan di folder docs/)")
        
    except subprocess.CalledProcessError as e:
        print(f"[-] Terjadi kesalahan saat menjalankan testing: {e}")
        print(e.stderr)

if __name__ == "__main__":
    run_automated_tests()
