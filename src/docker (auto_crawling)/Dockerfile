FROM python:3.10.12-slim

# 워크디렉토리 설정
WORKDIR /app

# 가상환경 생성
RUN python -m venv /app/venv

# 가상환경 실행
# cron을 위한 run-script를 실행시키기 때문에 python file copy를 우선 진행
COPY google_flight_osaka_27.py /app
COPY run-script.sh /app/run-script.sh 
COPY cronjob /etc/cron.d/cronjob

# 권한 부여
RUN chmod +x /app/run-script.sh

RUN apt-get update \
    && apt-get install -y wget gnupg unzip \
    && wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
    && apt-get install -y ./google-chrome-stable_current_amd64.deb \
    && rm google-chrome-stable_current_amd64.deb \
    && CHROMEDRIVER_VERSION=$(wget -qO- chromedriver.storage.googleapis.com/LATEST_RELEASE) \
    && wget -O /tmp/chromedriver_linux64.zip http://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip \
    && unzip /tmp/chromedriver_linux64.zip -d /usr/local/bin/ \
    && rm /tmp/chromedriver_linux64.zip \
    && rm -rf /var/lib/apt/lists/*


# 라이브러리 설치
RUN /app/venv/bin/pip install pandas beautifulsoup4 selenium schedule tqdm requests user-agent

# 업데이트, cron 경로 지정
RUN apt-get update && apt-get -y install cron \
    && chmod 0644 /etc/cron.d/cronjob \
    && crontab /etc/cron.d/cronjob \
    && touch /var/log/cron.log

RUN apt-get update && apt-get install -y tzdata
ENV TZ Asia/Seoul
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# cron 실행
CMD cron -f