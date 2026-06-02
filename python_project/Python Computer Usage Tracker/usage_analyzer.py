import os
from datetime import datetime
import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from tkcalendar import Calendar

plt.rcParams["font.family"] = "Malgun Gothic"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

dates = []
hours_list = []

SOCIAL_AVERAGE = 3 + 5/60


# =====================================
# 로그 로딩 (개선 버전)
# =====================================
def load_logs():

    global dates, hours_list
    dates = []
    hours_list = []

    temp_data = []

    for file_name in os.listdir(BASE_DIR):

        if file_name.endswith("_usage_log.txt") and file_name[:4].isdigit():

            file_path = os.path.join(BASE_DIR, file_name)

            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    lines = f.readlines()

                usage_time = None

                for line in lines:
                    if line.startswith("사용시간 :"):
                        usage_time = line.replace("사용시간 :", "").strip()
                        break

                if not usage_time:
                    continue

                h, m, s = map(int, usage_time.split(":"))
                total_hours = h + m/60 + s/3600

                date = file_name.replace("_usage_log.txt", "")

                temp_data.append((date, round(total_hours, 2)))

            except Exception as e:
                print(f"파일 오류: {file_name} -> {e}")

    # 날짜 정렬
    temp_data.sort(key=lambda x: x[0])

    for d, h in temp_data:
        dates.append(d)
        hours_list.append(h)


# =====================================
# 통계 계산 (개선)
# =====================================
def get_statistics():

    load_logs()

    if not hours_list:
        return {
            "daily": 0,
            "weekly": 0,
            "monthly": 0,
            "yearly": 0,
            "max": 0,
            "max_day": "없음"
        }

    def safe_avg(data):
        return round(sum(data) / len(data), 2) if data else 0

    stats = {
        "daily": safe_avg(hours_list),
        "weekly": safe_avg(hours_list[-7:]),
        "monthly": safe_avg(hours_list[-30:]),
        "yearly": safe_avg(hours_list),
    }

    # 최대값 index 정확 처리
    max_index = max(range(len(hours_list)), key=lambda i: hours_list[i])

    stats["max"] = hours_list[max_index]
    stats["max_day"] = dates[max_index]

    return stats


# =====================================
# 그래프 공통 함수
# =====================================
def show_graph(title, x_data, y_data):

    if not x_data:
        messagebox.showwarning("오류", "로그 파일이 없습니다.")
        return

    plt.figure(figsize=(12, 6))
    plt.plot(x_data, y_data, marker="o")

    for i in range(len(x_data)):
        plt.text(x_data[i], y_data[i], f"{y_data[i]}h")

    plt.title(title)
    plt.xlabel("날짜")
    plt.ylabel("사용 시간")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


# =====================================
# 일별 그래프
# =====================================
def daily_graph():
    load_logs()
    show_graph("일별 사용시간", dates, hours_list)


# =====================================
# 주별 그래프 (정렬 개선)
# =====================================
def weekly_graph():

    load_logs()
    week_data = {}

    for i in range(len(dates)):

        d = datetime.strptime(dates[i], "%Y-%m-%d")
        week_key = f"{d.year}-{d.isocalendar().week:02d}주차"

        week_data.setdefault(week_key, []).append(hours_list[i])

    x_data = sorted(week_data.keys())
    y_data = [
        round(sum(week_data[w]) / len(week_data[w]), 2)
        for w in x_data
    ]

    show_graph("주별 평균 사용시간", x_data, y_data)


# =====================================
# 월별 그래프
# =====================================
def monthly_graph():

    load_logs()
    month_data = {}

    for i in range(len(dates)):

        month = dates[i][:7]
        month_data.setdefault(month, []).append(hours_list[i])

    x_data = sorted(month_data.keys())
    y_data = [
        round(sum(month_data[m]) / len(month_data[m]), 2)
        for m in x_data
    ]

    show_graph("월별 평균 사용시간", x_data, y_data)


# =====================================
# 연도별 그래프
# =====================================
def yearly_graph():

    load_logs()
    year_data = {}

    for i in range(len(dates)):

        year = dates[i][:4]
        year_data.setdefault(year, []).append(hours_list[i])

    x_data = sorted(year_data.keys())
    y_data = [
        round(sum(year_data[y]) / len(year_data[y]), 2)
        for y in x_data
    ]

    show_graph("연도별 평균 사용시간", x_data, y_data)


# =====================================
# 등급 계산
# =====================================
def get_grade(hours):

    if hours < 2:
        return "매우 양호"
    elif hours < 4:
        return "양호"
    elif hours < 6:
        return "보통"
    elif hours < 8:
        return "높음"
    else:
        return "과다 사용"


# =====================================
# 날짜 조회
# =====================================
def show_selected_day():

    selected_date = cal.get_date()
    file_name = selected_date + "_usage_log.txt"
    file_path = os.path.join(BASE_DIR, file_name)

    if not os.path.exists(file_path):
        messagebox.showinfo("조회 결과", "기록 없음")
        return

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        usage_time = "00:00:00"
        state = "정보 없음"

        for line in lines:
            if line.startswith("사용시간 :"):
                usage_time = line.replace("사용시간 :", "").strip()
            elif line.startswith("상태 :"):
                state = line.replace("상태 :", "").strip()

        h, m, s = map(int, usage_time.split(":"))
        total = round(h + m/60 + s/3600, 2)

        messagebox.showinfo(
            "사용 기록",
            f"날짜: {selected_date}\n"
            f"사용시간: {total}시간\n"
            f"상태: {state}\n"
            f"등급: {get_grade(total)}"
        )

    except Exception as e:
        messagebox.showerror("오류", str(e))


# =====================================
# GUI
# =====================================
stats = get_statistics()

window = tk.Tk()
window.title("컴퓨터 사용시간 분석 대시보드")
window.geometry("1100x700")
window.resizable(False, False)


# ===== 제목 =====
tk.Label(
    window,
    text="컴퓨터 사용시간 분석 대시보드",
    font=("맑은 고딕", 20, "bold")
).pack(pady=15)


# ===== 카드 =====
card_frame = tk.Frame(window)
card_frame.pack(pady=10)


def create_card(parent, title, value):

    frame = tk.Frame(parent, relief="solid", borderwidth=1, width=180, height=90)
    frame.pack(side="left", padx=10)
    frame.pack_propagate(False)

    tk.Label(frame, text=title, font=("맑은 고딕", 10, "bold")).pack(pady=5)
    tk.Label(frame, text=value, font=("맑은 고딕", 12)).pack()


create_card(card_frame, "일 평균", f"{stats['daily']}h")
create_card(card_frame, "주 평균", f"{stats['weekly']}h")
create_card(card_frame, "월 평균", f"{stats['monthly']}h")
create_card(card_frame, "연 평균", f"{stats['yearly']}h")
create_card(card_frame, "최대 사용", f"{stats['max']}h")


# ===== 비교 =====
compare = round(stats["daily"] - SOCIAL_AVERAGE, 2)

tk.Label(
    window,
    text=(
        f"사회 평균보다 {abs(compare)}시간 "
        + ("높음" if compare > 0 else "낮음")
    ),
    font=("맑은 고딕", 12, "bold")
).pack()


# ===== 최대 사용일 =====
tk.Label(
    window,
    text=f"최대 사용일: {stats['max_day']}",
    font=("맑은 고딕", 11)
).pack(pady=5)


# ===== 메인 =====
main = tk.Frame(window)
main.pack(expand=True, fill="both", pady=10)


# ===== 캘린더 =====
left = tk.Frame(main)
left.pack(side="left", padx=20)

tk.Label(left, text="날짜 조회", font=("맑은 고딕", 12, "bold")).pack()

cal = Calendar(left, selectmode="day", date_pattern="yyyy-mm-dd")
cal.pack()

tk.Button(left, text="조회", command=show_selected_day, width=20, height=2).pack(pady=10)


# ===== 그래프 =====
right = tk.Frame(main)
right.pack(side="left", padx=50)

tk.Label(right, text="그래프", font=("맑은 고딕", 12, "bold")).pack()

tk.Button(right, text="일별", command=daily_graph, width=20).pack(pady=5)
tk.Button(right, text="주별", command=weekly_graph, width=20).pack(pady=5)
tk.Button(right, text="월별", command=monthly_graph, width=20).pack(pady=5)
tk.Button(right, text="연도별", command=yearly_graph, width=20).pack(pady=5)


window.mainloop()