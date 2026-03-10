class StudentScores:

    def __init__(self, filename):
        self.scores = {}

        try:
            with open(filename, "r", encoding="utf-8") as f:
                for line in f:
                    try:
                        name, score = line.strip().split(",")
                        self.scores[name] = int(score)
                    except ValueError:
                        print("데이터 형식 오류:", line)

        except FileNotFoundError:
            print("파일을 찾을 수 없습니다:", filename)


    def get_average(self):
        if len(self.scores) == 0:
            return 0
        return sum(self.scores.values()) / len(self.scores)


    def above_average(self):
        avg = self.get_average()
        result = []

        for name, score in self.scores.items():
            if score >= avg:
                result.append(name)

        return result


    def save_below_average(self):
        avg = self.get_average()

        try:
            with open("below_average_korean.txt", "w", encoding="utf-8") as f:
                for name, score in self.scores.items():
                    if score < avg:
                        f.write(f"{name},{score}\n")

        except IOError:
            print("파일 저장 중 오류 발생")


    def print_result(self):
        avg = self.get_average()
        above = self.above_average()

        print("----------------------------------------")
        print(f"평균 점수: {avg:.1f}")
        print(f"평균 이상을 받은 학생들: {above}")
        print("----------------------------------------")