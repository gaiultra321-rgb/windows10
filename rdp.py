import os
import subprocess
import time
import sys

def run_command(command, description):
    print(f"🔄 {description}...")
    try:
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        return process
    except Exception as e:
        print(f"❌ ভুল হয়েছে: {e}")
        sys.exit(1)

def main():
    # ১. ডকার ইমেজ বিল্ড করা
    print("🐳 Docker GUI Setup Started")
    build_cmd = "docker build -t ubuntu-gui ./rdp"
    build_proc = subprocess.run(build_cmd, shell=True)
    if build_proc.returncode != 0:
        print("❌ Docker Build ব্যর্থ হয়েছে!")
        sys.exit(1)
    print("✅ Docker Image সফলভাবে বিল্ড হয়েছে।")

    # ২. ডকার কন্টেইনার রান করা
    print("🚀 কন্টেইনার চালু করা হচ্ছে...")
    run_cmd = "docker run -d -p 6080:6080 --name my-gui-container ubuntu-gui"
    # আগের কন্টেইনার থাকলে রিমুভ করে নেওয়া
    subprocess.run("docker rm -f my-gui-container", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(run_cmd, shell=True)
    
    # কন্টেইনার বুট হওয়ার জন্য ২ সেকেন্ড সময় দেওয়া
    time.sleep(2)

    # ৩. Cloudflared ডাউনলোড করা (যদি আগে থেকে না থাকে)
    if not os.path.exists("./cloudflared"):
        download_cmd = "curl -L https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64 -o cloudflared && chmod +x cloudflared"
        run_command(download_cmd, "Cloudflared ডাউনলোড করা হচ্ছে")
        time.sleep(5)

    # ৪. Trycloudflare টানেল চালু করা এবং লিংক খোঁজা
    print("🌐 Cloudflare Tunnel তৈরি করা হচ্ছে...")
    tunnel_cmd = "./cloudflared tunnel --url http://localhost:6080"
    tunnel_proc = subprocess.Popen(tunnel_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

    print("\n⌛ আপনার লিংকের জন্য অপেক্ষা করুন (কয়েক সেকেন্ড সময় লাগতে পারে)...")
    
    # Cloudflare-এর আউটপুট থেকে trycloudflare.com লিংকটি খুঁজে বের করা
    link_found = False
    start_time = time.time()
    
    while True:
        output = tunnel_proc.stdout.readline()
        if output == '' and tunnel_proc.poll() is not None:
            break
        if "trycloudflare.com" in output:
            for word in output.split():
                if "trycloudflare.com" in word:
                    # পরিষ্কার লিংক বের করা
                    clean_url = word.strip().replace("https://", "").replace("http://", "")
                    clean_url = f"https://{clean_url}"
                    
                    print("\n" + "="*50)
                    print("🟢 আপনার লিনাক্স ডেস্কটপ রেডি!")
                    print(f"🔗 URL: {clean_url}")
                    print("🔑 VNC Password: bullet123")
                    print("="*50 + "\n")
                    link_found = True
                    break
        if link_found:
            break
            
        # ৩০ সেকেন্ড পার হয়ে গেলে লুপ বন্ধ করা (সেফটি চেক)
        if time.time() - start_time > 30:
            print("⚠️ লিংক পেতে একটু সময় লাগছে, অনুগ্রহ করে Codespaces-এর 'Ports' ট্যাব চেক করুন।")
            break

    # টানেল চালু রাখার জন্য স্ক্রিপ্টটিকে ধরে রাখা
    try:
        tunnel_proc.wait()
    except KeyboardInterrupt:
        print("\n🛑 টানেল বন্ধ করা হচ্ছে...")
        subprocess.run("docker stop my-gui-container", shell=True)
        tunnel_proc.terminate()

if __name__ == "__main__":
    main()
