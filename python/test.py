students = [
    {"name": "철수", "score": 80},
    {"name": "영희", "score": 90},
    {"name": "민수", "score": 70}
]
avg_students = []

def AVG(stud):
    total = 0
    for student in stud:
        total += student["score"]
    return total / len(stud)

for student in students:
    if student["score"] >= AVG(students):
        avg_students.append(student["name"])

print(avg_students)





