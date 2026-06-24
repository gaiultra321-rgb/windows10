import os
import subprocess
import sys

IMAGE_NAME = "windows10-vm"
CONTAINER_NAME = "windows10_running_vm"

def run_command(command):
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ এরর হয়েছে: {e}")
        sys.exit(1)

def main():
    print("🚀 উইন্ডোজ আরডিপি (RDP) সেটআপ স্ক্রিপ্ট চালু হচ্ছে...")

    # rdp/Dockerfile পাথ ব্যবহার করে বিল্ড করা হচ্ছে
    print("\n📦 rdp ফোল্ডার থেকে ডকার ইমেজ বিল্ড করা হচ্ছে...")
    run_command(f"docker build -t {IMAGE_NAME} -f rdp/Dockerfile rdp/")

    print("\n🧹 পুরোনো কন্টেইনার ক্লিন করা হচ্ছে (যদি থাকে)...")
    subprocess.run(f"docker rm -f {CONTAINER_NAME} >/dev/null 2>&1", shell=True)

    print("\n🔥 উইন্ডোজ কন্টেইনার রান করা হচ্ছে...")
    
    docker_run_cmd = (
        f"docker run -it --rm "
        f"--name {CONTAINER_NAME} "
        f"--device /dev/kvm "
        f"-p 6080:6080 "
        f"-p 3389:3389 "
        f"-v windows_data:/data "
        f"-v windows_iso:/iso "
        f"{IMAGE_NAME}"
    )
    
    run_command(docker_run_cmd)

if __name__ == "__main__":
    main()
