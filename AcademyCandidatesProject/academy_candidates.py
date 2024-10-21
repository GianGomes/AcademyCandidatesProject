import csv
import os
import math

def is_perfect_square(n):
    return int(math.sqrt(n)) ** 2 == n

def process_candidates(file_path):
    candidates = []
    states = set()

    with open(file_path, 'r') as file:
        for line in file:
            name, position, age, state = line.strip().split(';')
            age = int(age)
            candidates.append({'name': name, 'position': position, 'age': age, 'state': state})
            states.add(state)

    return candidates, states

def calculate_metrics(candidates):
    positions = {}
    
    for candidate in candidates:
        pos = candidate['position']
        age = candidate['age']

        if pos not in positions:
            positions[pos] = {'count': 0, 'age_sum': 0, 'ages': [], 'oldest': age, 'youngest': age}
        
        positions[pos]['count'] += 1
        positions[pos]['age_sum'] += age
        positions[pos]['ages'].append(age)
        positions[pos]['oldest'] = max(positions[pos]['oldest'], age)
        positions[pos]['youngest'] = min(positions[pos]['youngest'], age)

    return positions

def generate_sorted_csv(candidates):
    sorted_candidates = sorted(candidates, key=lambda x: x['name'])
    with open('Sorted_Academy_Candidates.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Nome', 'Vaga', 'Idade', 'Estado'])
        for candidate in sorted_candidates:
            writer.writerow([candidate['name'], candidate['position'], candidate['age'], candidate['state']])


def find_instructors(candidates):
    qa_instructor = None
    mobile_instructor = None

    for candidate in candidates:
        name = candidate['name']
        age = candidate['age']
        state = candidate['state']
        position = candidate['position']

        if position == "QA" and state == "SC":
            if 18 <= age <= 30 and is_perfect_square(age):
                if name == name[::-1]:
                    qa_instructor = name

        if position == "Mobile" and state == "PI":
            if 30 <= age <= 40 and age % 2 == 0 and name.split()[-1].startswith("C"):
                mobile_instructor = name

    return qa_instructor, mobile_instructor

def main():
    file_path = 'Academy_Candidates.txt'
    candidates, states = process_candidates(file_path)
    metrics = calculate_metrics(candidates)
    
    print("Porcentagem de candidatos por vaga:")
    for position, data in metrics.items():
        percentage = (data['count'] / len(candidates)) * 100
        print(f"{position}: {percentage:.2f}%")
    
    print("\nIdade média dos candidatos de QA:")
    if 'QA' in metrics:
        average_age_qa = metrics['QA']['age_sum'] / metrics['QA']['count']
        print(f"{average_age_qa:.2f}")
    
    print("\nIdade do candidato mais velho de Mobile:")
    if 'Mobile' in metrics:
        print(metrics['Mobile']['oldest'])
    
    print("\nIdade do candidato mais novo de Web:")
    if 'Web' in metrics:
        print(metrics['Web']['youngest'])
    
    print("\nSoma das idades dos candidatos de QA:")
    if 'QA' in metrics:
        print(metrics['QA']['age_sum'])
    
    print("\nNúmero de estados distintos presentes entre os candidatos:")
    print(len(states))
    
    generate_sorted_csv(candidates)
    print("\nArquivo 'Sorted_Academy_Candidates.csv' foi criado.")
    
    qa_instructor, mobile_instructor = find_instructors(candidates)
    print("\nInstrutor de QA descoberto:", qa_instructor)
    print("Instrutor de Mobile descoberto:", mobile_instructor)

if __name__ == "__main__":
    main()
