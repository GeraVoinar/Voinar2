import sqlite3
from datetime import datetime

class StaffAgency:
    def __init__(self):
        self.conn = sqlite3.connect('staff_agency.db')
        self.cursor = self.conn.cursor()
        self.create_tables()
    
    def create_tables(self):
        """Создание таблиц в базе данных"""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS candidates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name TEXT NOT NULL,
                birth_date TEXT,
                skills TEXT,
                experience INTEGER,
                phone TEXT,
                email TEXT,
                reg_date TEXT
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS vacancies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                position TEXT NOT NULL,
                company TEXT,
                salary INTEGER,
                requirements TEXT,
                description TEXT,
                pub_date TEXT
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS applications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                candidate_id INTEGER,
                vacancy_id INTEGER,
                status TEXT DEFAULT 'Рассмотрение',
                app_date TEXT,
                FOREIGN KEY (candidate_id) REFERENCES candidates (id),
                FOREIGN KEY (vacancy_id) REFERENCES vacancies (id)
            )
        ''')
        self.conn.commit()
    
    def add_candidate(self):
        """Добавление нового кандидата"""
        print("\nДобавление нового кандидата")
        full_name = input("ФИО: ")
        birth_date = input("Дата рождения (ГГГГ-ММ-ДД): ")
        skills = input("Навыки (через запятую): ")
        experience = input("Опыт работы (лет): ")
        phone = input("Телефон: ")
        email = input("Email: ")
        
        try:
            self.cursor.execute('''
                INSERT INTO candidates 
                (full_name, birth_date, skills, experience, phone, email, reg_date)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (full_name, birth_date, skills, experience, phone, email, datetime.now().strftime("%Y-%m-%d")))
            self.conn.commit()
            print("Кандидат успешно добавлен!")
        except Exception as e:
            print(f"Ошибка: {e}")
    
    def add_vacancy(self):
        """Добавление новой вакансии"""
        print("\nДобавление новой вакансии")
        position = input("Должность: ")
        company = input("Компания: ")
        salary = input("Зарплата: ")
        requirements = input("Требования: ")
        description = input("Описание: ")
        
        try:
            self.cursor.execute('''
                INSERT INTO vacancies 
                (position, company, salary, requirements, description, pub_date)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (position, company, salary, requirements, description, datetime.now().strftime("%Y-%m-%d")))
            self.conn.commit()
            print("Вакансия успешно добавлена!")
        except Exception as e:
            print(f"Ошибка: {e}")
    
    def create_application(self):
        """Создание заявки (связь кандидат-вакансия)"""
        print("\nСоздание новой заявки")
        
        # Показать список кандидатов
        print("\nСписок кандидатов:")
        self.cursor.execute("SELECT id, full_name FROM candidates")
        candidates = self.cursor.fetchall()
        for cand in candidates:
            print(f"{cand[0]}: {cand[1]}")
        
        # Показать список вакансий
        print("\nСписок вакансий:")
        self.cursor.execute("SELECT id, position, company FROM vacancies")
        vacancies = self.cursor.fetchall()
        for vac in vacancies:
            print(f"{vac[0]}: {vac[1]} ({vac[2]})")
        
        try:
            candidate_id = int(input("\nID кандидата: "))
            vacancy_id = int(input("ID вакансии: "))
            
            self.cursor.execute('''
                INSERT INTO applications 
                (candidate_id, vacancy_id, status, app_date)
                VALUES (?, ?, ?, ?)
            ''', (candidate_id, vacancy_id, "Рассмотрение", datetime.now().strftime("%Y-%m-%d")))
            self.conn.commit()
            print("Заявка успешно создана!")
        except ValueError:
            print("Ошибка: введите числовые ID")
        except Exception as e:
            print(f"Ошибка: {e}")
    
    def show_candidates(self):
        """Показать список кандидатов"""
        print("\nСписок кандидатов:")
        self.cursor.execute("SELECT * FROM candidates")
        candidates = self.cursor.fetchall()
        
        if not candidates:
            print("Кандидатов нет")
            return
        
        for cand in candidates:
            print(f"\nID: {cand[0]}")
            print(f"ФИО: {cand[1]}")
            print(f"Дата рождения: {cand[2]}")
            print(f"Навыки: {cand[3]}")
            print(f"Опыт: {cand[4]} лет")
            print(f"Контакты: {cand[5]}, {cand[6]}")
            print(f"Дата регистрации: {cand[7]}")
    
    def show_vacancies(self):
        """Показать список вакансий"""
        print("\nСписок вакансий:")
        self.cursor.execute("SELECT * FROM vacancies")
        vacancies = self.cursor.fetchall()
        
        if not vacancies:
            print("Вакансий нет")
            return
        
        for vac in vacancies:
            print(f"\nID: {vac[0]}")
            print(f"Должность: {vac[1]}")
            print(f"Компания: {vac[2]}")
            print(f"Зарплата: {vac[3]}")
            print(f"Требования: {vac[4]}")
            print(f"Описание: {vac[5]}")
            print(f"Дата публикации: {vac[6]}")
    
    def show_applications(self):
        """Показать список заявок"""
        print("\nСписок заявок:")
        self.cursor.execute('''
            SELECT a.id, c.full_name, v.position, v.company, a.status, a.app_date
            FROM applications a
            JOIN candidates c ON a.candidate_id = c.id
            JOIN vacancies v ON a.vacancy_id = v.id
        ''')
        apps = self.cursor.fetchall()
        
        if not apps:
            print("Заявок нет")
            return
        
        for app in apps:
            print(f"\nID: {app[0]}")
            print(f"Кандидат: {app[1]}")
            print(f"Вакансия: {app[2]} ({app[3]})")
            print(f"Статус: {app[4]}")
            print(f"Дата заявки: {app[5]}")
    
    def update_application_status(self):
        """Обновление статуса заявки"""
        self.show_applications()
        try:
            app_id = int(input("\nВведите ID заявки для изменения статуса: "))
            new_status = input("Новый статус (Рассмотрение/Принята/Отклонена): ")
            
            self.cursor.execute('''
                UPDATE applications SET status = ? WHERE id = ?
            ''', (new_status, app_id))
            self.conn.commit()
            print("Статус заявки обновлен!")
        except ValueError:
            print("Ошибка: введите числовой ID")
        except Exception as e:
            print(f"Ошибка: {e}")
    
    def menu(self):
        """Главное меню системы"""
        while True:
            print("\n=== Кадровое агентство ===")
            print("1. Добавить кандидата")
            print("2. Добавить вакансию")
            print("3. Создать заявку")
            print("4. Показать кандидатов")
            print("5. Показать вакансии")
            print("6. Показать заявки")
            print("7. Изменить статус заявки")
            print("0. Выход")
            
            choice = input("Выберите действие: ")
            
            if choice == "1":
                self.add_candidate()
            elif choice == "2":
                self.add_vacancy()
            elif choice == "3":
                self.create_application()
            elif choice == "4":
                self.show_candidates()
            elif choice == "5":
                self.show_vacancies()
            elif choice == "6":
                self.show_applications()
            elif choice == "7":
                self.update_application_status()
            elif choice == "0":
                print("Выход из системы...")
                self.conn.close()
                break
            else:
                print("Неверный ввод, попробуйте снова")

if __name__ == "__main__":
    agency = StaffAgency()
    agency.menu()