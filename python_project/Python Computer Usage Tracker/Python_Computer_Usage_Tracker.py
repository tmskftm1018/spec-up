import os
import time
import ctypes
import atexit
from datetime import datetime
from ctypes import wintypes
from plyer import notification


# ==================================================
# 클래스 + 상속
# ==================================================
class ProgramInfo:
    def show_program_name(self):
        return "컴퓨터 사용 시간 분석 프로그램 V3"


class UsageTracker(ProgramInfo):
    pass


tracker = UsageTracker()


# ==================================================
# Windows idle 체크 구조체
# ==================================================
class LASTINPUTINFO(ctypes.Structure):
    _fields_ = [
        ("cbSize", wintypes.UINT),
        ("dwTime", wintypes.DWORD),
    ]


def get_idle_duration():
    last_input_info = LASTINPUTINFO()
    last_input_info.cbSize = ctypes.sizeof(LASTINPUTINFO)

    ctypes.windll.user32.GetLastInputInfo(
        ctypes.byref(last_input_info)
    )

    millis = ctypes.windll.kernel32.GetTickCount() - last_input_info.dwTime
    return millis / 1000.0


# ==================================================
# 알림
# ==================================================
def notify(title, message):
    try:
        notification.notify(title=title, message=message, timeout=5)
    except:
        pass


# ==================================================
# 설정
# ==================================================
AUTO_SAVE_INTERVAL = 10
HOURLY_NOTIFY = 3600

SOCIAL_AVG = 5 * 3600 + 19 * 60  # 초 기준


# ==================================================
# 상태 변수
# ==================================================
total_saved = 0
session_seconds = 0
start_time = time.time()

warning_sent = False
save_counter = 0
last_hour_notify = -1


# ==================================================
# 날짜 / 로그
# ==================================================
current_date = datetime.now().strftime("%Y-%m-%d")
log_file = f"{current_date}_usage_log.txt"
backup_file = "usage_backup.txt"


# ==================================================
# 복구
# ==================================================
if os.path.exists(backup_file):
    try:
        with open(backup_file, "r", encoding="utf-8") as f:
            lines = f.readlines()

        if len(lines) >= 2:
            saved_date = lines[0].strip()
            saved_time = int(lines[1].strip())

            if saved_date == current_date:
                total_saved = saved_time
                start_time = time.time()

    except:
        total_saved = 0


# ==================================================
# 저장 함수
# ==================================================
def save_data():
    global total_saved, session_seconds, log_file

    total = total_saved + session_seconds
    h = total // 3600
    m = (total % 3600) // 60
    s = total % 60

    try:
        with open(log_file, "w", encoding="utf-8") as f:

            # 🔥 고정 헤더
            f.write(f"==== {current_date} 사용 기록 ====\n\n")

            # 🔥 네가 원하는 4줄 구조
            f.write(f"마지막 저장 시간 : {datetime.now().strftime('%H:%M:%S')}\n")
            f.write(f"현재 상태 : 사용 중\n")
            f.write(f"사용시간 : {h:02}:{m:02}:{s:02}\n")

            if total > SOCIAL_AVG:
                f.write("상태 : 평균 초과\n")
            else:
                f.write("상태 : 평균 이하\n")

    except Exception as e:
        print("저장 오류:", e)


atexit.register(save_data)


# ==================================================
# 날짜 변경 체크
# ==================================================
def check_date():
    global current_date, log_file
    global total_saved, session_seconds, warning_sent, start_time

    new_date = datetime.now().strftime("%Y-%m-%d")

    if new_date == current_date:
        return

    save_data()

    current_date = new_date
    log_file = f"{current_date}_usage_log.txt"

    total_saved = 0
    session_seconds = 0
    warning_sent = False
    start_time = time.time()

    notify("새 날짜 시작", f"{current_date} 기록 시작")


# ==================================================
# 시작 알림
# ==================================================
time.sleep(3)

notify("프로그램 시작", "사용 시간 측정 시작")

avg_h = SOCIAL_AVG // 3600
avg_m = (SOCIAL_AVG % 3600) // 60

notify("일일 평균 스크린 타임", f"{avg_h}시간 {avg_m}분")


print(tracker.show_program_name())
print("실행 중...")


# ==================================================
# 메인 루프
# ==================================================
try:
    while True:

        check_date()

        idle = get_idle_duration()
        current_session = int(time.time() - start_time)

        # 사용 여부 판단
        if idle < 60:
            session_seconds = current_session

        total = total_saved + session_seconds

        h = total // 3600
        m = (total % 3600) // 60
        s = total % 60

        os.system("cls")

        print("==== 사용 시간 분석 ====")
        print(f"상태: {'사용 중' if idle < 60 else '자리 비움'}")
        print(f"사용 시간: {h:02}:{m:02}:{s:02}")

        # ==================================================
        # 자동 저장
        # ==================================================
        save_counter += 1

        if save_counter >= AUTO_SAVE_INTERVAL:
            save_data()
            save_counter = 0
            print("\n[자동 저장 완료]")

        # ==================================================
        # 평균 초과 경고 (1회)
        # ==================================================
        if total > SOCIAL_AVG and not warning_sent:
            notify(
                "경고",
                f"평균 초과!\n{h}시간 {m}분"
            )
            warning_sent = True

        # ==================================================
        # 1시간 알림
        # ==================================================
        if current_session > 0:
            hour_now = current_session // HOURLY_NOTIFY

            if hour_now != last_hour_notify:
                last_hour_notify = hour_now

                notify(
                    "현재 사용 시간",
                    f"{h}시간 {m}분 사용 중"
                )

        time.sleep(1)


except KeyboardInterrupt:
    print("\n종료")
    save_data()