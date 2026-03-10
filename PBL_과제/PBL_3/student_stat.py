import statistics # 통계 계산 모듈(평균, 중앙값 등)
import random # 랜덤 모듈


def get_grade(score): # 등급을 매길 함수
    if score >= 90:
        return "A"
    elif score >= 80:
        return "B"
    elif score >= 70:
        return "C"
    elif score >= 60:
        return "D"
    else:
        return "F"


def print_statistics(students): # 학생 딕셔너리를 받아서 평균, 최고, 최저, 랜덤 칭찬하는 함수

    scores = list(students.values()) # scores라는 리스트는 입력받은 학생 딕셔너리의 value값

    # 평균 (소수점 2자리까지)
    avg = statistics.mean(scores) # 모듈 statistics를 이용해 평균값 계산
    print(f"\n[평균 점수]: {avg:.2f}") # 평균값을 소수점 2자리까지 출력

    # 최고 / 최저 점수
    max_student = max(students, key=students.get) # max 함수를 이용해 가장 큰 값을 찾아서 변수에 저장
    min_student = min(students, key=students.get) # min 함수를 이용해 가장 작은 값을 찾아서 변수에 저장

    print(f"최고 점수 학생: {max_student} ({students[max_student]})")
    print(f"최저 점수 학생: {min_student} ({students[min_student]})")

    # 등급 출력 (이름 오름차순)
    print("\n[학생 등급]")
    for name, score in sorted(students.items(), key=lambda x: x[1], reverse=True):
        # sorted 함수를 이용해 가장 큰 수부터 내림차 순으로 정렬
        # students.items() -> 딕셔너리 데이터를 튜플 형식으로 가져옴
        # 정렬 기준은 점수
        score = students[name]
        grade = get_grade(score) # 등급 함수를 이용해 등급 측정
        print(f"{name} : {score} ({grade})") # 이름, 점수, 등급 출력

    # 랜덤 칭찬 학생
    lucky = random.choice(list(students.keys())) # students 딕셔너리에서 key 값만 가져와 랜덤으로 고른다.
    print(f"\n칭찬 스티커 학생 : {lucky}")