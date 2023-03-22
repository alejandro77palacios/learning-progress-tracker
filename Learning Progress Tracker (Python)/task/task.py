import re
import string


class Validator:
    extra_characters = "'-"
    valid_characters = string.ascii_letters + extra_characters
    mail_pattern = re.compile(r"""
                               ^[a-zA-Z0-9_.+-]+
                               @
                               [a-zA-Z0-9-]+
                               \.
                               [a-zA-Z0-9-.]+$
                               """, flags=re.VERBOSE)

    def __init__(self, text):
        if len(text.split()) < 3:
            raise ValueError('Not enough fields')
        self.text = text

    def separate_fields(self):
        fields = self.text.split()
        first_name = fields[0]
        last_name = ' '.join(fields[1:-1])
        mail = fields[-1]
        data = {'first_name': first_name, 'last_name': last_name, 'email': mail}
        return data

    @staticmethod
    def valid_student(data, registered_mails):
        if not Validator.valid_name(data['first_name']):
            print('Incorrect first name')
            return False
        if not Validator.valid_last_name(data['last_name']):
            print('Incorrect last name.')
            return False
        if not Validator.valid_mail(data['email'], registered_mails):
            return False
        return True

    @staticmethod
    def valid_mail(mail, registered_mails):
        if mail in registered_mails:
            print('This email is already taken.')
            return False
        if not Validator.mail_pattern.match(mail):
            print('Incorrect email.')
            return False
        return True

    @staticmethod
    def valid_name(name):
        if len(name) < 2:
            return False
        if name[0] in Validator.extra_characters or name[-1] in Validator.extra_characters:
            return False
        if not set(name).issubset(Validator.valid_characters):
            return False
        return Validator.valid_double_extra(name)

    @staticmethod
    def valid_last_name(last_name):
        if ' ' in last_name:
            for name in last_name.split():
                if not Validator.valid_name(name):
                    return False
            return True
        return Validator.valid_name(last_name)

    @staticmethod
    def valid_double_extra(name):
        for i in range(1, len(name)):
            if name[i - 1] in Validator.extra_characters:
                if name[i] in Validator.extra_characters:
                    return False
        return True


class Student:
    courses = ('python', 'dsa', 'databases', 'flask')
    graduate_points = {'python': 600, 'dsa': 400, 'databases': 480, 'flask': 550}
    id = 1

    def __init__(self, first_name, last_name, email):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.progress = dict.fromkeys(Student.courses, 0)
        self.submissions = dict.fromkeys(Student.courses, 0)
        self.id = Student.id
        Student.id += 1
        self.notified = False

    def update_course(self, course, points):
        self.progress[course] += points
        self.submissions[course] += 1

    def add_points(self, text):
        try:
            data = [int(points) for points in text.split()]
        except ValueError:
            print('Incorrect points format')
        else:
            if len(data) != 4:
                print('Incorrect points format')
            else:
                for course, points in zip(Student.courses, data):
                    self.update_course(course, points)
                print('Points updated')

    def show_progress(self):
        print(f'{self.id} points:', end=' ')
        for course in Student.courses:
            if course != 'flask':
                print(f'{course}={self.progress[course]}', end='; ')
            else:
                print(f'{course}={self.progress[course]}')

    def is_enrolled(self, course):
        return self.progress[course] > 0

    def enrolled_courses(self):
        return [course for course in Student.courses if self.is_enrolled(course)]

    def candidate_graduation(self, course):
        return self.progress[course] >= self.graduate_points[course]

    def send_graduation(self, course):
        print(f'To: {self.email}')
        print('Re: Your Learning Progress')
        print(f'Hello, {self.first_name} {self.last_name}! You have accomplished our {course.title()} course!')

    def notify(self, course):
        if self.candidate_graduation(course):
            self.send_graduation(course)
            self.notified = True
            return True
        return False


class LearningTracker:
    title = "Learning progress tracker"
    graduate_points = {'python': 600, 'dsa': 400, 'databases': 480, 'flask': 550}

    def __init__(self):
        self.students = []
        self.active = True
        print(LearningTracker.title)

    def get_emails(self):
        return [student.email for student in self.students]

    def get_ids(self):
        return [student.id for student in self.students]

    def registered_id(self, student_id):
        return student_id in self.get_ids()

    def enrolled_students(self, course):
        return [student for student in self.students if student.is_enrolled(course)]

    def count_enrolled(self, course):
        return len(self.enrolled_students(course))

    def count_submissions(self, course):
        return sum([student.submissions[course] for student in self.students])

    def total_points(self, course):
        return sum([student.progress[course] for student in self.students])

    def average_points(self, course):
        submissions = self.count_submissions(course)
        total = self.total_points(course)
        if total == 0 or submissions == 0:
            return None
        return total / submissions

    @staticmethod
    def format_several(text):
        return ', '.join(text).title()

    def popularity(self):
        enrolled = [self.count_enrolled(course) for course in Student.courses]
        max_popularity = max(enrolled)
        if max_popularity == 0:
            print('Most popular: n/a')
            print('Least popular: n/a')
        else:
            courses_max = [course for course in Student.courses if self.count_enrolled(course) == max_popularity]
            print(f'Most popular: {self.format_several(courses_max)}')
            other_courses = [course for course in Student.courses if course not in courses_max]
            try:
                min_popularity = min([self.count_enrolled(course) for course in other_courses])
            except ValueError:
                print('Least popular: n/a')
            else:
                courses_min = [course for course in Student.courses if self.count_enrolled(course) == min_popularity]
                print(f'Least popular: {self.format_several(courses_min)}')

    def courses_activity(self):
        submissions = [self.count_submissions(course) for course in Student.courses]
        max_submissions = max(submissions)
        if max_submissions == 0:
            print('Highest activity: n/a')
            print('Lowest activity: n/a')
        else:
            courses_max = [course for course in Student.courses if self.count_submissions(course) == max_submissions]
            print(f'Highest activity: {self.format_several(courses_max)}')
            other_courses = [course for course in Student.courses if course not in courses_max]
            try:
                min_submissions = min([self.count_submissions(course) for course in other_courses])
            except ValueError:
                print('Lowest activity: n/a')
            else:
                courses_min = [course for course in Student.courses if
                               self.count_submissions(course) == min_submissions]
                print(f'Lowest activity: {self.format_several(courses_min)}')

    def courses_difficulty(self):
        averages = [self.average_points(course) for course in Student.courses]
        if averages == [None] * len(averages):
            print('Easiest course: n/a')
            print('Hardest course: n/a')
        else:
            max_average = max(averages)
            if max_average == 0:
                print('Easiest course: n/a')
                print('Hardest course: n/a')
            else:
                courses_max = [course for course in Student.courses if self.average_points(course) == max_average]
                print(f'Easiest course: {self.format_several(courses_max)}')
                other_courses = [course for course in Student.courses if course not in courses_max]
                try:
                    min_average = min([self.average_points(course) for course in other_courses])
                except ValueError:
                    print('Hardest course: n/a')
                else:
                    courses_min = [course for course in Student.courses if self.average_points(course) == min_average]
                    print(f'Hardest course: {self.format_several(courses_min)}')

    def top_learners(self, course):
        students_in_course = self.enrolled_students(course)
        students_in_course.sort(key=lambda x: (x.progress[course], - x.id,), reverse=True)
        print(course.title())
        print('id     points completed')
        for student in students_in_course:
            percentage = student.progress[course] / LearningTracker.graduate_points[course] * 100
            print(f'{student.id}     {student.progress[course]} {percentage:.1f}%')

    def list_students(self):
        all_ids = self.get_ids()
        if not all_ids:
            print('No students found')
        else:
            print(*all_ids, sep='\n')

    def add_student(self):
        print("Enter student credentials or 'back' to return:")
        new_students = 0
        while True:
            text = input()
            if text == 'back':
                print(f'Total {new_students} students have been added.')
                break
            try:
                validator = Validator(text)
            except ValueError:
                print('Incorrect credentials.')
                continue
            student_data = validator.separate_fields()
            if validator.valid_student(student_data, self.get_emails()):
                student = Student(**student_data)
                self.students.append(student)
                new_students += 1
                print('The student has been added.')

    def add_points(self, text):
        student_id, points = text.split(maxsplit=1)
        try:
            student_id = int(student_id)
        except ValueError:
            print(f'No student is found for id={student_id}')
        else:
            if student_id not in self.get_ids():
                print(f'No student is found for student_id={student_id}')
            else:
                index_student = self.get_ids().index(student_id)
                self.students[index_student].add_points(points)

    def user_add_points(self):
        print("Enter an id and points or 'back' to return:")
        while True:
            text = input()
            if text == 'back':
                break
            if len(text.split()) != 5:
                print('Incorrect points format')
                continue
            self.add_points(text)

    def find(self, student_id):
        index_student = self.get_ids().index(student_id)
        student = self.students[index_student]
        student.show_progress()

    def user_find(self):
        print("Enter an id or 'back' to return:")
        while True:
            text = input()
            if text == 'back':
                break
            student_id = int(text)
            if student_id not in self.get_ids():
                print(f'No student is found for student_id={student_id}')
            else:
                self.find(student_id)

    def user_statistics(self):
        print("Type the name of a course to see details or 'back' to quit:")
        self.popularity()
        self.courses_activity()
        self.courses_difficulty()
        while True:
            text = input().lower()
            if text == 'back':
                break
            if text not in Student.courses:
                print('Unknown course.')
            else:
                self.top_learners(text)

    def notify(self):
        number_notified = 0
        students_no_notified = [student for student in self.students if not student.notified]
        for student in students_no_notified:
            student_notified = False
            for course in Student.courses:
                if student.notify(course):
                    student_notified = True
            if student_notified:
                number_notified += 1
        print(f'Total {number_notified} students have been notified.')

    def process_action(self):
        while self.active:
            action = input().lower()
            action = action if re.search(r'\S', action) else ''
            match action:
                case 'exit':
                    self.active = False
                    print('Bye!')
                case 'add students':
                    self.add_student()
                case 'list':
                    print('Students:')
                    self.list_students()
                case 'add points':
                    self.user_add_points()
                case 'find':
                    self.user_find()
                case 'statistics':
                    self.user_statistics()
                case 'notify':
                    self.notify()
                case 'back':
                    print("Enter 'exit' to exit the program.")
                case '':
                    print('No input')
                case _:
                    print(f'Unknown command!')


if __name__ == '__main__':
    tracker = LearningTracker()
    tracker.process_action()
