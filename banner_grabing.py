import socket
import concurrent.futures
import time

ip = "192.168.133.128"
up_ports = []
closed_ports = []

# Tüm portlar 0-10000 arasında taranacak
taranacak_portlar = range(0,100)


def scan_port(port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(4.0)  # Bağlantı için maksimum 1 saniye bekle
        s.connect((ip, port))
        banner = s.recv(1024) #banner bilgileri alınıyor

        # Bağlantı başarılı ise veri almaya çalış
        try:
            #response = s.recv(1024)
            print(f"{port}: {banner.decode()}")
        except Exception:
            pass  # Veri alınamadıysa geç

        # Açık portları listeye ekle
        up_ports.append(port)

    except Exception:
        closed_ports.append(port)
    except socket.timeout as t:
        print(f"Timeout{t}")
    finally:
        s.close()


# Başlangıç zamanını al
stime = time.time()

# Thread havuzu kullanarak portları tarıyoruz
with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
    executor.map(scan_port, taranacak_portlar)

# Bitiş zamanını al
end_time = time.time()

# Sonuçları yazdır
print("Geçen süre:", end_time - stime)
print("Açık Portlar:", up_ports)
