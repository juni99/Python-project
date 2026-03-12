import re # 정규표현식 모듈
from collections import Counter # 개수 세는 모듈


def extract_ip_counts(file_path):
    # 줄 맨 앞의 IPv4 주소만 찾는 정규표현식
    ip_pattern = re.compile(r'^((?:\d{1,3}\.){3}\d{1,3})') # ipv4 주소 찾기
    ip_counter = Counter() # 딕셔너리 형태로 빈도수 저장

    try:
        with open("sample_log_file.txt", "r", encoding="utf-8") as file:
            for line in file: # 파일을 한줄씩 읽음
                match = ip_pattern.match(line) # 맨 앞줄의 패턴이 IP로 시작하는지 확인
                if match: # 만약 IP가 맨 앞에있다면
                    ip = match.group(1)
                    ip_counter[ip] += 1 # 해당 IP가 처음나오면 1로 시작하고 이미 있으면 1을 더함(카운터)

    except FileNotFoundError: # 파일없는 오류
        print("오류: 파일을 찾을 수 없습니다.")
        return None
    except PermissionError: # 권한 오류
        print("오류: 파일에 접근할 권한이 없습니다.")
        return None
    except UnicodeDecodeError: # 인코딩 오류
        print("오류: 파일 인코딩을 읽을 수 없습니다.")
        return None
    except Exception as e: # 외 다른 오류
        print(f"알 수 없는 오류 발생: {e}")
        return None

    return ip_counter # IP별 개수를 저장한 Counter 반환값


def print_result(ip_counter): # 분석 결과 출력 함수
    if not ip_counter:
        print("추출된 IP 주소가 없습니다.")
        return

    print("\n[IP 주소별 접속 빈도]")
    for ip, count in ip_counter.items():
        print(f"{ip}: {count}회")

    print("\n[가장 많이 등장한 상위 3개 IP]")
    for ip, count in ip_counter.most_common(3): # Counter 모듈의 기능으로 가장 많이 나온 항목 3개를 내림차 순으로 반환
        print(f"{ip}: {count}회")


def save_to_csv(ip_counter, output_file="ip_frequency.csv"): # 분석 결과를 CSV파일로 저장 함수
    try:
        with open(output_file, "w", encoding="utf-8") as file:
            file.write("IP,Count\n") # 파일 제목
            for ip, count in ip_counter.items():
                file.write(f"{ip},{count}\n")
        print(f"\nCSV 파일 저장 완료: {output_file}")

    except Exception as e:
        print(f"CSV 저장 중 오류 발생: {e}")


def main():
    ip_counter = extract_ip_counts("sample_log_file.txt")

    if ip_counter is None: # 오류 발생시 종료
        return

    print_result(ip_counter)
    save_to_csv(ip_counter)


if __name__ == "__main__":
    main()