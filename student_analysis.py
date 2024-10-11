import numpy as np
import json
import matplotlib.pyplot as plt
from typing import List, Tuple
import os
import sys

# Ensure proper encoding for console output
sys.stdout.reconfigure(encoding='utf-8')

# ANSI color codes for prettier console output
class Color:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_colored(text: str, color: str):
    print(f"{color}{text}{Color.ENDC}")

def initialize_data() -> Tuple[List[str], List[str], np.ndarray]:
    try:
        with open('students_data.json', 'r') as file:
            data = json.load(file)
            subjects = data['subjects']
            students = data['students']
            marks = np.array(data['marks'])
        print_colored("Data loaded successfully.", Color.GREEN)
    except (FileNotFoundError, json.JSONDecodeError):
        print_colored("No existing data found. Initializing with default subjects.", Color.YELLOW)
        subjects = ['English', 'Maths', 'Science', 'Social', 'History']
        students = []
        marks = np.array([])
        save_data(subjects, students, marks)
    return subjects, students, marks

def save_data(subjects: List[str], students: List[str], marks: np.ndarray):
    with open('students_data.json', 'w') as file:
        json.dump({'subjects': subjects, 'students': students, 'marks': marks.tolist()}, file)
    print_colored("Data saved successfully.", Color.GREEN)

def add_record(subjects: List[str], students: List[str], marks: np.ndarray) -> Tuple[List[str], np.ndarray]:
    print_colored("\nAdding a new student record", Color.HEADER)
    student_name = input("Enter student name: ")
    new_marks = []
    for subject in subjects:
        while True:
            try:
                mark = int(input(f"Enter mark for {subject} (0-100): "))
                if 0 <= mark <= 100:
                    new_marks.append(mark)
                    break
                else:
                    print_colored("Mark should be between 0 and 100.", Color.RED)
            except ValueError:
                print_colored("Please enter a valid integer.", Color.RED)
    students.append(student_name)
    marks = np.vstack((marks, new_marks)) if marks.size else np.array([new_marks])
    save_data(subjects, students, marks)
    print_colored("Record added successfully.", Color.GREEN)
    return students, marks

def display_results(subjects: List[str], students: List[str], marks: np.ndarray):
    if not students:
        print_colored("No data available.", Color.YELLOW)
        return
    print_colored("\nStudent Results:", Color.HEADER)
    header = "Student Name".ljust(20) + " | " + " | ".join(subject.ljust(8) for subject in subjects) + " | Average"
    print_colored(header, Color.BOLD)
    print_colored("-" * len(header), Color.BOLD)
    for student, student_marks in zip(students, marks):
        avg = np.mean(student_marks)
        row = f"{student.ljust(20)} | " + " | ".join(f"{mark:8.2f}" for mark in student_marks) + f" | {avg:8.2f}"
        print(row)

def analyze_trend(subjects: List[str], students: List[str], marks: np.ndarray):
    if len(students) < 2:
        print_colored("Not enough data to analyze trends.", Color.YELLOW)
        return
    
    plt.figure(figsize=(12, 6))
    years = np.arange(len(students))

    for subject_index, subject in enumerate(subjects):
        subject_marks = marks[:, subject_index] if marks.size else []
        plt.plot(years, subject_marks, marker='o', label=subject)

    plt.title('Trend of Marks by Subject', fontsize=16)
    plt.xlabel('Student Index', fontsize=12)
    plt.ylabel('Marks', fontsize=12)
    plt.legend()
    plt.xticks(years, students, rotation=45)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

def subject_comparison(subjects: List[str], students: List[str], marks: np.ndarray):
    if marks.size == 0:
        print_colored("No data available for comparison.", Color.YELLOW)
        return

    subject_averages = np.mean(marks, axis=0)
    
    plt.figure(figsize=(12, 6))
    bars = plt.bar(subjects, subject_averages, color='skyblue', edgecolor='navy')
    plt.title('Average Performance by Subject', fontsize=16)
    plt.xlabel('Subjects', fontsize=12)
    plt.ylabel('Average Marks', fontsize=12)
    plt.ylim(0, 100)

    # Adding value labels on top of each bar
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                 f'{height:.2f}',
                 ha='center', va='bottom')

    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

def main():
    print_colored("Starting Student Performance Analysis Program...", Color.BOLD)
    subjects, students, marks = initialize_data()
    print(f"Loaded data: {len(subjects)} subjects, {len(students)} students")

    while True:
        print_colored("\n--- Student Performance Analysis ---", Color.HEADER)
        print("1. Add new student record")
        print("2. Display results")
        print("3. Analyze trend")
        print("4. Subject comparison")
        print("5. Exit")
        
        choice = input("Enter your choice (1-5): ")
        
        if choice == '1':
            students, marks = add_record(subjects, students, marks)
        elif choice == '2':
            display_results(subjects, students, marks)
        elif choice == '3':
            analyze_trend(subjects, students, marks)
        elif choice == '4':
            subject_comparison(subjects, students, marks)
        elif choice == '5':
            print_colored("Thank you for using the Student Performance Analysis Program. Goodbye!", Color.BOLD)
            break
        else:
            print_colored("Invalid choice. Please try again.", Color.RED)

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print_colored(f"An unexpected error occurred: {e}", Color.RED)
        import traceback
        traceback.print_exc()