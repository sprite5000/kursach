import os
import mysql.connector

class Database(object):
    def __init__(self):
        self.conn = mysql.connector.connect(
            database='postreim_tax',
            user='postreim_tax',
            password='Alex1412',
            host='postreim.beget.tech',
            port='3306'
        )
        self.curs = self.conn.cursor(dictionary=True)

    def __enter__(self):
        return self.curs

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.commit()
        self.conn.close()

def get_statuses():
    with Database() as curs:
        _SQL = f"""SELECT * FROM status;"""
        curs.execute(_SQL)
        return curs.fetchall()

def get_status_id(name):
        with Database() as curs:
            _SQL = f"""SELECT id FROM status WHERE name = '{name}' LIMIT 1;"""
            curs.execute(_SQL)
            res = curs.fetchone()
            if res:
                return res['id']
            return 0

def get_source_id(name):
        with Database() as curs:
            _SQL = f"""SELECT id FROM sources WHERE name = '{name}' LIMIT 1;"""
            curs.execute(_SQL)
            res = curs.fetchone()
            if res:
                return res['id']
            return 0

def add_user(name, sname, address, email, passid, phone, status_name, hash):
    status_id = get_status_id(status_name)
    with Database() as curs:
        _SQL = f"""INSERT INTO taxpayers (name, surname, address, email, idPassport, phoneNumber, password, idStatus)
                   VALUES ('{name}', '{sname}', '{address}', '{email}', '{passid}', '{phone}', '{hash}', {status_id});"""
        curs.execute(_SQL)

def get_user_by_email(email):
    with Database() as curs:
        _SQL = f"""SELECT * FROM taxpayers WHERE email = '{email}' LIMIT 1;"""
        curs.execute(_SQL)
        return curs.fetchone()

def get_status(id):
    with Database() as curs:
        _SQL = f"""SELECT * FROM status WHERE id = {id} LIMIT 1;"""
        curs.execute(_SQL)
        return curs.fetchone()

def get_incomes(id):
    with Database() as curs:
        _SQL = f"""SELECT * FROM incomes WHERE idPayer = {id};"""
        curs.execute(_SQL)
        return curs.fetchall()

def get_expenses(id):
    with Database() as curs:
        _SQL = f"""SELECT * FROM expenses WHERE idPayer = {id};"""
        curs.execute(_SQL)
        return curs.fetchall()

def get_income(id):
   with Database() as curs:
        _SQL = f"""SELECT * FROM incomes WHERE id = {id} LIMIT 1;"""
        curs.execute(_SQL)
        return curs.fetchone()

def get_expense(id):
   with Database() as curs:
        _SQL = f"""SELECT * FROM expenses WHERE id = {id} LIMIT 1;"""
        curs.execute(_SQL)
        return curs.fetchone()

def get_sources():
    with Database() as curs:
        _SQL = f"""SELECT * FROM sources;"""
        curs.execute(_SQL)
        return curs.fetchall()

def add_income(id_tax, id_s, value, desc):
    with Database() as curs:
        _SQL = f"""INSERT INTO incomes(value, idSource, idPayer, description)
        VALUES ({value}, {id_s}, {id_tax}, '{desc}');"""
        curs.execute(_SQL)

def add_expense(id_tax, country, value, desc):
    with Database() as curs:
        _SQL = f"""INSERT INTO expenses(value, country, idPayer, description)
        VALUES ({value}, '{country}', {id_tax}, '{desc}');"""
        curs.execute(_SQL)

def delete_income(id):
    with Database() as curs:
        _SQL = f"""DELETE FROM incomes WHERE id = {id}"""
        curs.execute(_SQL)

def delete_expense(id):
    with Database() as curs:
        _SQL = f"""DELETE FROM expenses WHERE id = {id}"""
        curs.execute(_SQL)














