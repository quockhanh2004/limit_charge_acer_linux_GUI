import socket
import subprocess
import os

sock_path = "/tmp/acer-battery-control.sock"
default_module_path = "/etc/acer-battery-control-gui/"

if os.path.exists(sock_path):
    os.remove(sock_path)

def run_command(command):
    print("run command: %s" % command)
    try:
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(result.stdout.decode())
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return f"Error: {e.stderr.strip()}"

def check_and_insert_module(module_name):
    # Kiểm tra nếu module đã được tải vào
    check_command = f"lsmod | grep {module_name}"
    check_result = run_command(check_command)
    
    # Nếu module chưa được tải, tiến hành load nó
    if not check_result:
        # Nếu module chưa có, build lại và insmod module
        make_result = run_command(f"make -C {default_module_path}")
        make_result_str = make_result.stdout.decode()

        if "error" not in make_result_str.lower():  # Kiểm tra xem make có thành công không
            insmod_command = f"insmod {default_module_path}acer-wmi-battery.ko"
            insmod_result = run_command(insmod_command)
            return f"Make output:\n{make_result}\n\nInsmod output:\n{insmod_result}"
        else:
            return f"Make error:\n{make_result}"
    else:
        return f"Module {module_name} is already loaded.\nNo need to add it again."

def main():
    # Kiểm tra và load module nếu chưa có
    module_name = "acer_wmi"
    module_check_response = check_and_insert_module(module_name)

    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

    try:
        print("Binding socket...")
        sock.bind(sock_path)
        print("Socket bound, waiting for connections...")
        sock.listen(5)
    except Exception as e:
        print(f"Error binding socket: {e}")
        return

    os.chmod(sock_path, 0o666)  # Đặt quyền cho file socket
    print("backend started successfully")
    
    # In thông tin kiểm tra module
    print(module_check_response)
    
    while True:
        conn, _ = sock.accept()
        with conn:
            while True:
                data = conn.recv(1024).decode("utf-8")
                if not data:
                    break

                command = data.strip()  # Lấy command từ GUI
                       
                if command == "health_mode_on":
                    response = run_command("echo 1 | sudo tee /sys/bus/wmi/drivers/acer-wmi-battery/health_mode")
                elif command == "health_mode_off":
                    response = run_command("echo 0 | sudo tee /sys/bus/wmi/drivers/acer-wmi-battery/health_mode")
                elif command == "calibration_mode_on":
                     response = run_command("echo 1 | sudo tee /sys/bus/wmi/drivers/acer-wmi-battery/calibration_mode")
                elif command == "calibration_mode_off":
                     response = run_command("echo 0 | sudo tee /sys/bus/wmi/drivers/acer-wmi-battery/calibration_mode")
                elif command.startswith("insmod"):  # Ví dụ: "insmod /path/to/module.ko"
                    response = run_command(f"{command}")  # Chạy insmod với sudo
                elif command == "ping":
                    response = "pong"
                else:
                    response = "Invalid command"

                if isinstance(response, bytes):
                    conn.sendall(response)  # Gửi bytes như là nó
                elif isinstance(response, str):
                    conn.sendall(response.encode("utf-8"))  # Mã hóa string thành bytes trước khi gửi
                else:
                    conn.sendall(str(response).encode("utf-8"))  # Mã hóa các kiểu khác thành bytes

if __name__ == "__main__":
    main()
