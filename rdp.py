import os
import subprocess
import time
import sys
import re

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
    # আগের কন্টেইনার থাকলে রিমুভ করে নেওয়া
    subprocess.run("docker rm -f my-gui-container", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    run_cmd = "docker run -d -p 6080:6080 --name my-gui-container ubuntu-gui"
    subprocess.run(run_cmd, shell=True)
    
    time.sleep(2)

    # ৩. Cloudflared ডাউনলোড করা
    if not os.path.exists("./cloudflared"):
        print("🔄 Cloudflared ডাউনলোড করা হচ্ছে...")
        download_cmd = "curl -L https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64 -o cloudflared && chmod +x cloudflared"
        subprocess.run(download_cmd, shell=True)
        time.sleep(2)

    # ৪. Trycloudflare টানেল चालू করা
    print("🌐 Cloudflare Tunnel তৈরি করা হচ্ছে...")
    tunnel_cmd = "./cloudflared tunnel --url http://localhost:6080"
    
    # stderr এবং stdout দুটোই রিড করার জন্য প্রসেস ওপেন করা
    tunnel_proc = subprocess.Popen(tunnel_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

    print("\n⌛ আপনার অরিজিনাল লিংকের জন্য অপেক্ষা করুন (কয়েক সেকেন্ড সময় লাগবে)...")
    
    link_found = False
    start_time = time.time()
    
    while True:
        output = tunnel_proc.stdout.readline()
        if output == '' and tunnel_proc.poll() is not None:
            break
        
        # Regex ব্যবহার করে সম্পূর্ণ trycloudflare.com লিংকটি খুঁজে বের করা
        match = re.search(r'https://[a-zA-Z0-9-]+\.trycloudflare\.com', output)
        if match:
            clean_url = match.group(0)
            print("\n" + "="*60)
            print("🟢 আপনার লিনাক্স ডেস্কটপ একদম রেডি!")
            print(f"🔗 ORIGINAL URL: {clean_url}")
            print("🔑 VNC Password: bullet123")
            print("="*60 + "\n")
            link_found = True
            break
            
        # ৩০ সেকেন্ড সেফটি টাইমআউট
        if time.time() - start_time > 30:
            print("\n⚠️ স্ক্রিপ্ট থেকে লিংকটি ফিল্টার করা যায়নি।")
            print("💡 বিকল্প বুদ্ধি: Codespaces-এর নিচে 'Ports' ট্যাবে যান এবং 6080 পোর্টের পাশে থাকা লিংকে ক্লিক করুন।")
            break

    try:
        tunnel_proc.wait()
    except KeyboardInterrupt:
        print("\n🛑 টানেল বন্ধ করা হচ্ছে...")
        subprocess.run("docker stop my-gui-container", shell=True)
        tunnel_proc.terminate()

if __name__ == "__main__":
    main()
