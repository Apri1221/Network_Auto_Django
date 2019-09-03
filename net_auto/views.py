from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from .models import Device, Log
import paramiko
import telnetlib
import time
from datetime import datetime

def bits_to_mask(n):
    if n < 0 or n > 32:
        raise ValueError('Bit count must be between 0 and 32')
    mask = (~((1 << (32 - n)) - 1)) & 0xFFFFFFFF
    return '.'.join(map(str, ((mask >> (8 * i)) & 0xFF for i in range(3, -1, -1))))

# Create your views here.
def beranda(request):

    if request.method == 'POST':
        try:
            selected_menu = request.POST['menu']
            ip_address = request.POST['ip_address']
            username = request.POST['username']
            password = request.POST['password']
            interface = 'int ' + request.POST['interface']
            ip_gateway = request.POST['ip_gateway']
            net_mask = request.POST['net_mask']
            delete = request.POST.get("checkbox")

            net_mask = bits_to_mask(int(net_mask))
            eigrp_name = request.POST['eigrp_name']
            ip_network = request.POST['network']

            ssh_client = paramiko.SSHClient()
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh_client.connect(hostname=ip_address, port=22, username=username, password=password)

            if selected_menu == 'set_interface':
                
                cmd_ip = 'ip add ' + ip_gateway + ' ' + str(net_mask)
                if delete == 'yes':
                    cmd_ip = 'no ' + cmd_ip
                
                command = [interface, cmd_ip]
                conn = ssh_client.invoke_shell()
                conn.send("conf t\n")
                for cmd in command:
                    conn.send(cmd + '\n')
                    time.sleep(1)

                log = Log(target=ip_address, action="Konfigurasi {}".format(
                    selected_menu), status="Success", time=datetime.now(), messages='Tidak ada Error')
                log.save()
            

            elif selected_menu == 'set_routing':
                
                cmd_ip = 'router eigrp ' + eigrp_name
                ip_network = "network {}".format(ip_network) + " {}\n".format(ip_network)

                command = [cmd_ip, 'no auto', ip_network]
                conn = ssh_client.invoke_shell()
                conn.send("conf t\n")
                for cmd in command:
                    conn.send(cmd + '\n')
                    time.sleep(1)

                log = Log(target=ip_address, action="Konfigurasi {}".format(
                    selected_menu), status="Success", time=datetime.now(), messages='Tidak ada Error')
                log.save()
            
        except Exception as e:
            log = Log(target=ip_address, action="Konfigurasi {}".format(selected_menu), status="Error", time=datetime.now(), messages=e)
            log.save()

        return redirect('beranda')

    else:
        all_devices = Device.objects.all()
        # daftar perangkat masih 2 jenis
        cisco_devices = Device.objects.filter(vendor="cisco")
        mikrotik_devices = Device.objects.filter(vendor="mikrotik")

        # ambil riwayat konfigurasi dan batasi hanya 10 list
        last_event = Log.objects.all().order_by('-id')[:10]

        context = {
            'all_devices': len(all_devices),
            'cisco_devices': len(cisco_devices),
            'mikrotik_devices': len(mikrotik_devices),
            'last_event': last_event
        }

        return render(request, 'beranda.html', context)


def perangkat(request):
    all_devices = Device.objects.all()
    context = {
        'all_devices': all_devices
    }
    return render(request, 'daftar_perangkat.html', context)


def konfigurasi(request):
    if request.method == 'POST':
        selected_device_id = request.POST.getlist('device')
        mikrotik_command = request.POST['mikrotik_command'].splitlines()
        cisco_command = request.POST['cisco_command'].splitlines()
        for x in selected_device_id:
            try:
                # simpan device yg id nya x ke variabel dev
                dev = get_object_or_404(Device, pk=x)
                ssh_client = paramiko.SSHClient()
                # The authenticity of host '10.10.10.1 (10.10.10.1)' can't be established.
                # RSA key fingerprint is SHA256:edMvj7985fDDDCVAlXb+1n8IWDmo1dSqQ4hVSD+plEg.
                # Are you sure you want to continue connecting (yes/no)? y

                # Auto add policy di bawah ini untuk membuat dan menjawab rules di atas
                ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh_client.connect(hostname=dev.ip_address, username=dev.username, password=dev.password)
                if dev.vendor.lower() == 'cisco':
                    conn = ssh_client.invoke_shell()
                    conn.send("conf t\n")
                    for cmd in cisco_command:
                        conn.send(cmd + '\n')
                        time.sleep(1)

                else:
                    for cmd in mikrotik_command:
                        ssh_client.exec_command(cmd)

                log = Log(target=dev.ip_address, action="Konfigurasi",status="Success", time=datetime.now(), messages='Tidak ada Error')
                log.save()

            except Exception as e:
                log = Log(target=dev.ip_address, action="Konfigurasi",
                          status="Error", time=datetime.now(), messages=e)
                log.save()
        return redirect('beranda')

    else:
        devices = Device.objects.all()
        context = {
            'devices': devices,
            'mode': 'Konfigurasi'
        }
        return render(request, "konfigurasi.html", context)


def cek_konfigurasi(request):
    # if ini untuk ngecek apakah di halaman view konfigurasi html terjadi tindakan post, lalu di proses
    if request.method == 'POST':
        result = []
        selected_device_id = request.POST.getlist('device')
        mikrotik_command = request.POST['mikrotik_command'].splitlines()
        cisco_command = request.POST['cisco_command'].splitlines()
        for x in selected_device_id:
            try:
                # simpan device yg id nya x ke variabel dev
                dev = get_object_or_404(Device, pk=x)
                ssh_client = paramiko.SSHClient()
                ssh_client.set_missing_host_key_policy(
                    paramiko.AutoAddPolicy())
                ssh_client.connect(hostname=dev.ip_address,
                                   username=dev.username, password=dev.password)
                if dev.vendor.lower() == 'mikrotik':
                    for cmd in mikrotik_command:
                        stdin, stdout, stderr = ssh_client.exec_command(cmd)
                        # stdout adalah output dari command yang kita eksekusi
                        result.append("Result on {}".format(dev.ip_address))
                        result.append(stdout.read().decode())

                else:
                    conn = ssh_client.invoke_shell()
                    # length 0 maksudnya agar command output nya dieksekusi tanpa 'more'
                    conn.send('terminal length 0\n')
                    for cmd in cisco_command:
                        result.append("Result on {}".format(dev.ip_address))
                        conn.send(cmd + "\n")
                        time.sleep(2)
                        output = conn.recv(65535)
                        result.append(output.decode())

                log = Log(target=dev.ip_address, action="Cek Konfigurasi",
                          status="Success", time=datetime.now(), messages='Tidak ada Error')
                log.save()

            except Exception as e:
                log = Log(target=dev.ip_address, action="Cek Konfigurasi",
                          status="Error", time=datetime.now(), messages=e)
                log.save()

        # setiap item digabung dan dipisahkan dengan enter
        result = '\n'.join(result)
        return render(request, 'cek_konfigurasi.html', {'result': result})

    # else ini untuk nampilin halaman konfigurasi aja
    else:
        devices = Device.objects.all()
        context = {
            'devices': devices,
            'mode': 'Verifikasi'
        }
        return render(request, "konfigurasi.html", context)


def riwayat(request):
    logs = Log.objects.all().order_by('-id')
    context = {
        'logs': logs
    }
    return render(request, 'riwayat.html', context)
