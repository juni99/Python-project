def input_students(): # 학생 정보를 입력받는 함수 생성
    n = int(input("학생 수 입력: ")) # 학생 수를 정수로 입력받음
    students = {} # 학생 정보를 저장할 딕셔너리 변수

    for i in range(n): # 학생 수 만큼 반복
        name = input("학생 이름 입력: ") 

        while True: # 무한 반복을 이용해서 정확한 점수를 입력받음
            score = int(input("점수 입력 (0~100): ")) # 학생 점수를 정수로 입력받음
            if 0 <= score <= 100: # 조건문을 이용해서 점수가 0에서 100 사이인지 확인, 만약 아니라면 재입력
                break # 정확한 입력 시 반복문 종료
            else:
                print("점수는 0~100 사이로 입력하세요.")

        students[name] = score   # 이름 중복 시 덮어쓰기 (딕셔너리는 key 값이 중복이면 덮어씀)

    return students # 반환값은 학생 정보를 담은 딕셔너리