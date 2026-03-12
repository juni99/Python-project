import os
import time
import re

# 감시할 디렉터리 이름을 저장하는 변수
WATCH_DIR = "monitor_dir"

# 주의해야 할 파일 확장자를 집합(set)으로 저장
WARNING_EXTENSIONS = {".js", ".class", ".py"}

# 이메일 주소를 찾기 위한 정규표현식 패턴
EMAIL_PATTERN = r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"

# SQL 관련 키워드를 리스트로 저장
SQL_KEYWORDS = ["SELECT", "INSERT", "UPDATE", "DELETE", "DROP", "CREATE"]


def analyze_file(filepath):
    # 현재 분석을 시작하는 파일 경로를 출력
    print(f"[내용 분석 시작] {filepath}")

    try:
        # 파일을 읽기 모드로 열고, 한글 깨짐 방지를 위해 utf-8 인코딩 사용
        # errors="ignore"는 읽을 수 없는 문자가 있어도 무시하고 진행하게 해줌
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            # 파일의 모든 줄을 리스트 형태로 읽어옴
            lines = f.readlines()

        # 파일 안에서 주석, 이메일, SQL 코드 중 하나라도 찾았는지 기록하는 변수
        found_any = False

        # enumerate를 사용해 줄 번호와 줄 내용을 함께 가져옴
        # start=1은 줄 번호를 1번부터 시작하게 함
        for line_number, line in enumerate(lines, start=1):
            # 줄 양쪽의 공백과 줄바꿈 문자를 제거한 문자열
            stripped_line = line.strip()

            # 파이썬 주석(#) 또는 자바스크립트 한 줄 주석(//)인지 검사
            if stripped_line.startswith("#") or stripped_line.startswith("//"):
                # 주석을 발견하면 줄 번호와 내용을 출력
                print(f"  [주석 발견] {line_number}줄: {stripped_line}")
                # 하나라도 찾았다는 표시를 True로 변경
                found_any = True

            # C/JS 스타일의 여러 줄 주석 시작 또는 끝 기호가 있는지 검사
            if "/*" in stripped_line or "*/" in stripped_line:
                # 주석 관련 문자열을 발견하면 출력
                print(f"  [주석 발견] {line_number}줄: {stripped_line}")
                # 하나라도 찾았다는 표시를 True로 변경
                found_any = True

            # 현재 줄에서 이메일 주소 패턴과 일치하는 문자열을 모두 찾음
            emails = re.findall(EMAIL_PATTERN, line)

            # 이메일이 하나 이상 발견되었는지 확인
            if emails:
                # 발견된 이메일들을 하나씩 꺼내서 출력
                for email in emails:
                    print(f"  [이메일 발견] {line_number}줄: {email}")
                    # 하나라도 찾았다는 표시를 True로 변경
                    found_any = True

            # SQL 키워드 비교를 쉽게 하기 위해 현재 줄을 모두 대문자로 변환
            upper_line = line.upper()

            # 미리 준비한 SQL 키워드 목록을 하나씩 검사
            for keyword in SQL_KEYWORDS:
                # 현재 줄 안에 SQL 키워드가 포함되어 있는지 확인
                if keyword in upper_line:
                    # SQL 관련 내용이 있으면 줄 번호와 원래 내용 출력
                    print(f"  [SQL 코드 발견] {line_number}줄: {stripped_line}")
                    # 하나라도 찾았다는 표시를 True로 변경
                    found_any = True
                    # 한 줄에서 여러 SQL 키워드가 중복 출력되지 않도록 반복 종료
                    break

        # 파일 전체를 확인했는데 아무것도 발견하지 못한 경우 안내 문구 출력
        if not found_any:
            print("  특별한 정보가 발견되지 않았습니다.")

    # 파일 경로가 실제 파일이 아니라 디렉터리일 때 발생하는 예외 처리
    except IsADirectoryError:
        print(f"  [오류] {filepath} 는 디렉터리입니다.")

    # 파일이 존재하지 않을 때 발생하는 예외 처리
    except FileNotFoundError:
        print(f"  [오류] {filepath} 파일을 찾을 수 없습니다.")

    # 파일에 접근 권한이 없을 때 발생하는 예외 처리
    except PermissionError:
        print(f"  [오류] {filepath} 파일 접근 권한이 없습니다.")

    # 그 외 예상하지 못한 예외를 한 번에 처리
    except Exception as e:
        print(f"  [오류] 파일 분석 중 예외 발생: {e}")


def monitor_directory():
    # 감시할 폴더가 실제로 존재하는지 확인
    if not os.path.exists(WATCH_DIR):
        # 폴더가 없으면 새로 생성
        os.makedirs(WATCH_DIR)
        # 사용자에게 폴더를 생성했다는 안내 출력
        print(f"[안내] 감시 폴더가 없어 새로 생성했습니다: {WATCH_DIR}")

    # 프로그램 시작 시점의 기존 파일 목록을 set으로 저장
    # 이후 현재 파일 목록과 비교하여 새 파일을 찾는 데 사용
    known_files = set(os.listdir(WATCH_DIR))

    # 프로그램 시작 안내선 출력
    print("=" * 50)
    # 프로그램 제목 출력
    print("시스템 보안 모니터링 시작")
    # 현재 감시 중인 디렉터리 이름 출력
    print(f"감시 디렉터리: {WATCH_DIR}")
    # 프로그램 동작 방식 안내 출력
    print("새 파일이 생성되면 자동으로 탐지합니다.")
    # 구분선 출력
    print("=" * 50)

    # 무한 반복으로 디렉터리를 계속 감시
    while True:
        try:
            # 3초 동안 대기한 뒤 다시 검사
            time.sleep(3)

            # 현재 시점의 파일 목록을 set으로 저장
            current_files = set(os.listdir(WATCH_DIR))

            # 현재 파일 목록 - 기존 파일 목록 = 새로 추가된 파일 목록
            new_files = current_files - known_files

            # 새 파일이 하나라도 있는지 확인
            if new_files:
                # 새 파일 탐지 구역 제목 출력
                print("\n[새 파일 탐지]")

                # 주의 파일만 따로 모아두기 위한 리스트
                warning_files = []

                # 새로 발견된 파일들을 하나씩 처리
                for filename in new_files:
                    # 디렉터리 경로와 파일 이름을 합쳐 전체 경로 생성
                    filepath = os.path.join(WATCH_DIR, filename)

                    # 새 파일 이름 출력
                    print(f"- 새 파일 발견: {filename}")

                    # 파일명과 확장자를 분리
                    _, ext = os.path.splitext(filename)

                    # 확장자를 소문자로 바꿔 주의 확장자 목록에 있는지 검사
                    if ext.lower() in WARNING_EXTENSIONS:
                        # 주의 파일이면 리스트에 추가
                        warning_files.append(filename)

                    # 현재 경로가 일반 파일인지 확인
                    if os.path.isfile(filepath):
                        # 일반 파일이면 내용 분석 함수 호출
                        analyze_file(filepath)
                    else:
                        # 일반 파일이 아니면 분석을 건너뛰었다고 출력
                        print(f"  [안내] {filename} 는 일반 파일이 아니므로 내용 분석을 건너뜁니다.")

                # 주의 파일이 하나라도 있다면 따로 목록 출력
                if warning_files:
                    print("\n[주의 파일 목록]")

                    # 주의 파일들을 한 줄씩 출력
                    for wf in warning_files:
                        print(f"  ⚠ {wf}")

            # 이번 검사 결과를 다음 비교를 위한 기준 목록으로 갱신
            known_files = current_files

        # 사용자가 Ctrl + C를 눌러 프로그램을 종료할 때 예외 처리
        except KeyboardInterrupt:
            # 종료 안내 메시지 출력
            print("\n프로그램을 종료합니다.")
            # 무한 반복 종료
            break

        # 감시 도중 발생할 수 있는 기타 예외 처리
        except Exception as e:
            # 오류 내용을 출력하고 프로그램은 계속 유지
            print(f"[오류] 모니터링 중 예외 발생: {e}")


# 현재 파일이 직접 실행되었을 때만 아래 코드를 실행
if __name__ == "__main__":
    # 디렉터리 감시 함수 실행
    monitor_directory()
