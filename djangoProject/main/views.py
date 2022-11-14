import datetime
from typing import Optional
from django.http import request
from psycopg2 import sql
from rest_framework import response
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView, exception_handler
from django.utils.datastructures import MultiValueDictKeyError
import psycopg2
import os


# Create your views here.

# подключеник к postgres
def init_connection(user: str, password: str):
    conn = psycopg2.connect(dbname='demo',
                            user=user,
                            password=password,
                            #host='95.165.30.171',
                            host='localhost',
                            port='54321'
                            )

    cursor = conn.cursor()

    return conn, cursor


def execute_post_query(query: sql, login: str, password: str):
    try:
        conn, cursor = init_connection(user=login, password=password)
    except psycopg2.OperationalError as e:
        return {"errer": "error in login or password"}

    try:
        cursor.execute(query.as_string(conn))
        cursor.execute("COMMIT")
    except psycopg2.errors.DuplicateObject:
        return {"error": "task eexists"}
    except psycopg2.errors.InsufficientPrivilege:
        return{"error": "permishon_denied"}

    return {"status": 200}


def execute_command(query: str, login: str, password: str) -> list:
    try:
        conn, cursor = init_connection(user=login, password=password)
    except psycopg2.OperationalError as e:
        return {"error": "incorect login or password"}

    cursor.execute(query)

    response_data = cursor.fetchall()
    close_conn(conn, cursor)
    return response_data


# отключчение от postgres
def close_conn(conn, cursor):
    cursor.close()
    conn.close()


# Api для заданий
class TasksApiView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        
        login = self.request.query_params.get('username')
        password = self.request.query_params.get('password')

        sql_script = "SELECT * FROM public.tasks LEFT JOIN public.contract USING(contract_number)"

        response_data = execute_command(sql_script, login, password)
        if type(response_data) is dict:
            return Response(response_data)

        tasksList: list = []
        for i in response_data:
            rez = {
                'task_number': i[1],
                'date_of_creation': i[2],
                'date_of_completion': i[3],
                'term_of_execution': i[4],
                'contact_number': i[0],
                'author_number': i[5],
                'performer_number': i[6],
                'status': i[7],
                'priority_code': i[8],
                'task_type_code': i[9],
                'contract_details': i[10],
                'vin': i[11],
                'license_plate': i[12]
            }
            tasksList.append(rez)

        return Response({'tasks': tasksList})

    def post(self, request):
        login = self.request.query_params.get('username')
        password = self.request.query_params.get('password')

        try:
            term_of_execution = request.data['term_of_execution']
            contract_number: Optional[int] = request.data['contract_number']
            priority_code: int = request.data['priority_code']
            task_type_code: int = request.data['task_type_code']
            performer_number = request.data['performer_number']
        except Exception:
            return Response({"error": "body was incorrect"})

        # Переводим дату в нужный формат из строки
        term_of_execution = datetime.date(*map(int, term_of_execution.split('-')))
        if term_of_execution < datetime.date.today():
            return Response({"error": "term_of_execution must be greater than today"})

        if performer_number == '':
            sql_script = sql.SQL(
            f"INSERT INTO tasks(term_of_execution, contract_number, author_number, priority_code, task_type_code) VALUES ('{term_of_execution}', {contract_number}, 1 , {priority_code}, {task_type_code})")
        else: 
             sql_script = sql.SQL(
            f"INSERT INTO tasks(term_of_execution, contract_number, author_number, performer_number, priority_code, task_type_code) VALUES ('{term_of_execution}', {contract_number}, 1 ,{performer_number}, {priority_code}, {task_type_code})")


        response_data = execute_post_query(query=sql_script,
                                           login=login,
                                           password=password
                                           )
        return Response(response_data)

    def put(self, request):
        login = self.request.query_params.get('username')
        password = self.request.query_params.get('password')

        update_dict = {}
        try:
            task_number: int = request.data['task_number']

            if 'performer_number' in request.data.keys():
                update_dict['performer_number'] =  request.data['performer_number']
            if 'contract_number' in request.data.keys():
                update_dict['contact_number'] =  request.data['contact_number']
            if 'term_of_execution' in request.data.keys():
                update_dict['term_of_execution'] =  request.data['term_of_execution']
            if 'status' in request.data.keys():
                update_dict['status'] =  request.data['status']

            if 'priority_code' in request.data.keys():
                update_dict['priority_code'] =  request.data['priority_code']

            if 'task_type_code' in request.data.keys():
                update_dict['task_type_code'] =  request.data['task_type_code']
 
        except Exception:
            return Response({"error": "body was incorrect"})
        
        if 'status' in update_dict.keys():
            if int(update_dict['status']) > 1:
                return Response({'errer': "inncoorect status"})

        sql_script = f"UPDATE tasks SET "
        for key, value in update_dict.items():
            one_update_script = f"{key}='{value}', "
            sql_script += one_update_script
        
        sql_script = sql_script[:-2]
        sql_script += f" WHERE task_number={task_number}"
        
        sql_script = sql.SQL(sql_script)

        try:  
            response_data = execute_post_query(query=sql_script,
                                           login=login,
                                           password=password
                                           )
        except psycopg2.errors.UniqueViolation:
            return Response({'errer': "you can't edit this task"})

        return Response(response_data)


# Api для типов заданий
class TaskTypeApiView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        
        login = os.getenv('ADMIN_LOGIN')
        password = os.getenv('ADMIN_PASSWORD')
        sql_script = "SELECT * FROM public.task_type_classifier"

        response_data = execute_command(sql_script, login, password)
        if type(response_data) is dict:
            return Response(response_data)

        tasksClasses: list = []
        for i in response_data:
            rez = {
                'task_type_code': i[0],
                'task_type': i[1]
            }
            tasksClasses.append(rez)

        return Response({'tasks classifier': tasksClasses})


# Api для приоритетов заданий
class TaskPriorityApiView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        login = os.getenv('ADMIN_LOGIN')
        password = os.getenv('ADMIN_PASSWORD')
        sql_script = "SELECT * FROM public.priority_classifier"

        response_data = execute_command(sql_script, login, password)
        if type(response_data) is dict:
            return Response(response_data)

        tasksTypeClasses: list = []
        for i in response_data:
            rez = {
                'priority_code': i[0],
                'classifier': i[1]
            }
            tasksTypeClasses.append(rez)

        return Response({'tasks priority': tasksTypeClasses})


# Api для работников
class EmlpoyeeApiView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request):

        login = self.request.query_params.get('username')
        password = self.request.query_params.get('password')

        sql_script = "SELECT employee_id, login FROM public.employees "
        response_data = execute_command(sql_script, login, password)
        if type(response_data) is dict:
            return Response(response_data)

        employeeList: list = []
        for i in response_data:
            rez = {
                'employee_id': i[0],
                'login': i[1]
            }
            employeeList.append(rez)

        return Response({'employees': employeeList})


# Api для контрактов
class ContractApiView(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        login = self.request.query_params.get('username')
        password = self.request.query_params.get('password')

        try:
            contract_details: Optional[str] = request.data['contract_details']
            vin = request.data['vin']
            license_plate = request.data['license_plate']
        except Exception:
            return Response({"error": "body was incorrect"})

        print(contract_details, vin, license_plate)

        sql_script = sql.SQL(
            f"INSERT INTO contract(contract_details, vin, license_plate, contact_person_number) VALUES ('{contract_details}', '{vin}', '{license_plate}', null)")

        response_contract = execute_post_query(query=sql_script,
                                               login=login,
                                               password=password
                                               )
        sql_script = f"SELECT contract_number FROM contract WHERE contract_details='{contract_details}' AND vin='{vin}' AND license_plate='{license_plate}' ORDER BY contract_number DESC LIMIT 1"
        response_contract = execute_command(query=sql_script, login=login, password=password)

        return Response({'id': response_contract})


# API для пользоователей
class UserApiView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        login_for_check = self.request.query_params.get('login')
        login = os.getenv('ADMIN_LOGIN')
        password = os.getenv('ADMIN_PASSWORD')
        sql_script = f"SELECT login, employee_position FROM public.employees " \
                     f"JOIN position_classifier USING(position_code) WHERE login='{login_for_check}'"

        response_data = execute_command(sql_script, login, password)[0]

        rez = {
            "name": response_data[0],
            "role": response_data[1],
        }

        return Response({"iAm": rez})

    def post(self, request):
        login = self.request.query_params.get('username')
        password = self.request.query_params.get('password')

        try:
            login_for_user: str = request.data['login']
            password_for_user: str = request.data['password']
            name_for_user: str = request.data['name']
            role_for_user: str = request.data['role']
        except Exception:
            return Response({"error": "body was incorrect"})

        sql_script = f"SELECT position_code FROM position_classifier WHERE " \
                     f" employee_position='{role_for_user}';"


        try:
            id_role = execute_command(sql_script, os.getenv('ADMIN_LOGIN'), os.getenv('ADMIN_PASSWORD'))[0][0]
        except:
            return Response({"error": "incorrect role"})

        sql_script = sql.SQL(
            f"SET ROLE elefant; CREATE ROLE {login_for_user} WITH PASSWORD '{password_for_user}' LOGIN; GRANT {role_for_user} TO {login_for_user}; INSERT INTO employees(employee_name, position_code, login, employee_password) VALUES ('{name_for_user}', {id_role}, '{login_for_user}', '{password_for_user}');")

        response_data = execute_post_query(query=sql_script,
                                           login=login,
                                           password=password
                                           )
        return Response(response_data)


# API для контактный лиц
class ContactPersonAPIView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        login = os.getenv('ADMIN_LOGIN')
        password = os.getenv('ADMIN_PASSWORD')
        sql_script = "SELECT * FROM contact_person"

        response_data = execute_command(sql_script, login, password)
        if type(response_data) is dict:
            return Response(response_data)

        ContactPersons: list = []
        for i in response_data:
            rez = {
                'contact_person_number': i[0],
                'contact_person_name': i[1],
                'phone': i[2],
                'email': i[3],
                'city': i[4],
                'organization_number': i[5]
            }
            ContactPersons.append(rez)

        return Response({'Contact persons': ContactPersons})


# API для организаций
class OrganizationAPIView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        login = os.getenv('ADMIN_LOGIN') 
        password = os.getenv('ADMIN_PASSWORD')
        sql_script = "SELECT * FROM organization"

        response_data = execute_command(sql_script, login, password)
        if type(response_data) is dict:
            return Response(response_data)

        organizations: list = []
        for i in response_data:
            rez = {
                'organization_number': i[0],
                'organization_name': i[1],
                'organization_type': i[2],
                'email': i[3],
                'address': i[4],
                'city': i[5]
            }
            organizations.append(rez)

        return Response({'organizations': organizations})


