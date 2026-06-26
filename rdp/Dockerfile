FROM ubuntu:22.04

# এনভায়রনমেন্ট ভ্যারিয়েবল সেট করা (ইউজার ইন্টারঅ্যাকশন এড়ানোর জন্য)
ENV DEBIAN_FRONTEND=noninteractive

# প্রয়োজনীয় প্যাকেজ, LXDE ডেস্কটপ এবং VNC ইনস্টল করা
RUN apt-get update && apt-get install -y \
    lxde \
    tightvncserver \
    autocutsel \
    curl \
    git \
    python3 \
    && apt-get clean

# noVNC ডাউনলোড করা (ব্রাউজারে দেখার জন্য)
RUN git clone https://github.com/novnc/noVNC.git /root/novnc

# VNC পাসওয়ার্ড সেট করা (ডিফল্ট পাসওয়ার্ড: 'bullet123')
RUN mkdir /root/.vnc && \
    echo "bullet123" | vncpasswd -f > /root/.vnc/passwd && \
    chmod 600 /root/.vnc/passwd

# VNC ও noVNC স্টার্ট করার স্ক্রিপ্ট তৈরি
RUN echo '#!/bin/bash\n\
vncserver :1 -geometry 1280x720 -depth 24\n\
/root/novnc/utils/novnc_proxy --vnc localhost:5901 --listen 6080\n\
' > /root/start.sh && chmod +x /root/start.sh

EXPOSE 6080

CMD ["/root/start.sh"]
