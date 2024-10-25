from dataclasses import dataclass
from enum import Enum
from typing import List, Dict

applicants = []


class Department(Enum):
    BIO = "Biotech"  # Does not have a score, replace with Chemistry
    CHE = "Chemistry"
    ENG = "Engineering"  # Computer Science
    MAT = "Mathematics"
    PHY = "Physics"


D = Department


@dataclass
class Applicant:
    first: str
    last: str
    grades: Dict[Department, float]
    exam: int
    priorities: List[Department]


n = int(input())
for line in open('applicants.txt', 'r'):
    first, last, *destructure = line.split()
    order = [D.PHY, D.CHE, D.MAT, D.ENG]
    grades = dict(zip(order, list(map(int, destructure[:4]))))
    grades[D.BIO] = grades[D.CHE]
    composite = dict()
    composite[D.PHY] = (grades[D.PHY]+grades[D.MAT])/2
    composite[D.CHE] = grades[D.CHE]
    composite[D.MAT] = grades[D.MAT]
    composite[D.ENG] = (grades[D.MAT]+grades[D.ENG])/2
    composite[D.BIO] = (grades[D.CHE]+grades[D.PHY])/2
    exam = int(destructure[4])
    priorities = list(map(Department, destructure[5:]))

    applicants.append(Applicant(first, last, composite, exam, priorities))


def algo(a: Applicant):
    return -max(a.grades[dep], a.exam), a.first, a.last


admission: Dict[Department, List[Applicant]] = {d: [] for d in Department}
for p in range(3):
    for dep in Department:
        if len(admission[dep]) < n:
            extend = list(filter(lambda x: x.priorities[p] == dep, applicants))  # 1. only consider current priority
            extend = sorted(extend, key=algo)
            d = n - len(admission[dep])
            extend = extend[:d]  # 3. add up to n students
            admission[dep].extend(extend)
            applicants = [a for a in applicants if a not in extend]  # 4. accepted students removed

# thanks to comment https://hyperskill.org/projects/163/stages/847/implement#comment-2667069
# for noting that you need to sort the full list to pass the test in stage 4/7
for dep, adm_list in admission.items():
    admission[dep] = sorted(adm_list, key=algo)

for dep, adm_list in admission.items():
    with open(dep.value.lower()+'.txt', 'w') as f:
        for a in adm_list:
            f.write(f'{a.first} {a.last} {max(a.grades[dep], a.exam)}\n')
