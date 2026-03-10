import student_input
from student_scores import StudentScores


def save_students_txt(students):

    try:
        with open("scores_korean.txt", "w", encoding="utf-8") as f:
            for name, score in students.items():
                f.write(f"{name},{score}\n")

    except IOError:
        print("파일 저장 오류 발생")


def main():

    students = student_input.input_students()

    save_students_txt(students)

    ss = StudentScores("scores_korean.txt")

    ss.print_result()

    ss.save_below_average()


if __name__ == "__main__":
    main()