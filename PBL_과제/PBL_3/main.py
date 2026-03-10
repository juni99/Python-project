import student_input # 학생 입력 함수
import student_stat # 학생 점수 통계 함수


def main(): # main 함수 생성
    students = student_input.input_students()  # 학생 정보를 입력받아 students 딕셔너리에 저장.
    student_stat.print_statistics(students) # students 데이터를 student_stat 모듈로 전달


if __name__ == "__main__":
    main()