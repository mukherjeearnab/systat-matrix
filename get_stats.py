import platform
import psutil
import datetime
import socket
import os

def get_system_stats():
    # System info
    uname = platform.uname()
    
    # IP addresses (non-localhost)
    ip_list = []
    for iface_name, iface_addrs in psutil.net_if_addrs().items():
        for addr in iface_addrs:
            if addr.family == socket.AF_INET and not addr.address.startswith("127."):
                ip_list.append(f"{iface_name}: {addr.address}")
    ip_message = "\n | ".join(ip_list) if ip_list else "N/A"

    # CPU load (1, 5, 15 min averages)
    load1, load5, load15 = os.getloadavg()
    cpu_cores = psutil.cpu_count(logical=False)
    cpu_threads = psutil.cpu_count(logical=True)

    # Memory
    svmem = psutil.virtual_memory()
    total_mem = svmem.total // (1024**3)
    used_mem = svmem.used // (1024**3)
    mem_percent = svmem.percent

    # Disk
    partitions = psutil.disk_partitions()
    disk_info = []
    for part in partitions:
        if '/snap' in part.mountpoint:
            continue
        try:
            usage = psutil.disk_usage(part.mountpoint)
            disk_info.append(
                f"{part.mountpoint}: {usage.used // (1024**3)}GB/"
                f"{usage.total // (1024**3)}GB ({usage.percent}%)"
            )
        except PermissionError:
            # Some mountpoints may be restricted
            continue
    disk_infos = '\n | '.join(disk_info)

    # Network
    net = psutil.net_io_counters()
    net_sent = net.bytes_sent // (1024**2)
    net_recv = net.bytes_recv // (1024**2)

    # Uptime
    boot_time = datetime.datetime.fromtimestamp(psutil.boot_time())
    uptime = datetime.datetime.now() - boot_time

    temp_message = "N/A"
    try:
        temps = psutil.sensors_temperatures()
        if temps:
            parts = []
            for name, entries in temps.items():
                for entry in entries:
                    label = entry.label if entry.label else name
                    parts.append(f"{label}: {entry.current}°C")
            temp_message = "\n | ".join(parts)
    except Exception:
        pass

    # GPU stats (NVIDIA only via GPUtil)
    gpu_message = "N/A"
    try:
        import GPUtil
        gpus = GPUtil.getGPUs()
        if gpus:
            gpu_parts = []
            for gpu in gpus:
                gpu_parts.append(
                    f"{gpu.name} | Load: {gpu.load*100:.1f}% | "
                    f"Mem: {gpu.memoryUsed}MB/{gpu.memoryTotal}MB | "
                    f"Temp: {gpu.temperature}°C"
                )
            gpu_message = "\n | ".join(gpu_parts)
    except ImportError:
        gpu_message = "GPUtil not installed"
    except Exception:
        pass

    # Build text message
    message = (
        f"📊 System Stats Report\n\n"
        f"🖥️ Host: {uname.node}\n"
        f"OS: {uname.system} {uname.release} ({uname.version})\n"
        f"Kernel: {uname.machine}\n"
        f"IP(S): {ip_message}\n\n"
        f"⚙️ CPU Load: {load1:.2f}, {load5:.2f}, {load15:.2f}\n"
        f" | Cores: {cpu_cores} | Threads: {cpu_threads}\n\n"
        f"🌡️ Temps: {temp_message}\n\n"
        f"🖼️ GPU: {gpu_message}\n"
        f"🗂️ Memory: {used_mem}GB/{total_mem}GB ({mem_percent}%)\n"
        f"💾 Disk: {disk_infos}\n\n"
        f"🌐 Network: Sent {net_sent}MB | Received {net_recv}MB\n"
        f"⏱️ Uptime: {str(uptime).split('.')[0]}\n"
        
    )

    return message

if __name__ == '__main__':
    print(get_system_stats())