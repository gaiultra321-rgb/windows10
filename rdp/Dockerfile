FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends \
    lxde \
    tightvncserver \
    autocutsel \
    curl \
    git \
    python3 \
    ca-certificates \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/novnc/noVNC.git /root/novnc

RUN mkdir /root/.vnc && \
    echo "bullet123" | vncpasswd -f > /root/.vnc/passwd && \
    chmod 600 /root/.vnc/passwd

# স্ক্রিপ্টটি একটু মডিফাই করা হয়েছে যাতে লক ফাইল ও ডিসপ্লে আগে থেকেই ক্লিন থাকে
RUN echo '#!/bin/bash\n\
rm -rf /tmp/.X11-unix/X1 /tmp/.X1-lock\n\
vncserver :1 -geometry 1280x720 -depth 24\n\
sleep 2\n\
/root/novnc/utils/novnc_proxy --vnc localhost:5901 --listen 6080\n\
' > /root/start.sh && chmod +x /root/start.sh

EXPOSE 6080

CMD ["/root/start.sh"]
