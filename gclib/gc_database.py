### database.py ############################################################
'''Κώδικας για τη διαχείριση της βάσης δεδομένων''' 

import sqlite3 as lite

class Database(object):
  '''Manage database operations'''

  def sql_type(field):
    if field.typeof=='int': return 'INTEGER'
    if field.typeof=='float': return 'REAL'
    return 'TEXT'

  def sql_value(field, value=None): #seperated field and value can handle fields with stack values ex. stack=2
    if value is None: value=field.value
    if field.typeof=='str': return '"{}"'.format(value) if value else 'NULL'
    if field.typeof=='int': return value if value else 'NULL'
    if field.typeof=='float': return value if value else 'NULL'
  
  def __init__(self, file_name='', *tables):
    self.file_name=file_name
    self.tables=tables

  def table_by_name(self, name):
    return list(filter(lambda x: x.class_name()==name, self.tables))[0]

  def create_table(self, *tables):
    if len(tables)==0: tables=self.tables
    if type(tables[0]) is list: tables=tables[0]

    retval=''
    try:
      conn=lite.connect(self.file_name)
      with conn:
        for table in tables:
          fields=table.fields_as_obj({'save_included':True})
          curs=conn.cursor()
          sql='CREATE TABLE IF NOT EXISTS {} ('.format(table.class_name())
          for k, v in fields.items(): 
            sql+='{} {}{}{}{}, '.format(k, Database.sql_type(v), 
              ' PRIMARY KEY' if v.primary_key else '', 
              ' UNIQUE' if v.unique else '', 
              ' NOT NULL' if v.not_null else '')
              #' AUTOINCREMENT' if getattr(v, 'auto_increment', False) else ''
          sql=sql[0:-2]+');'
          retval+=sql
          curs.execute(sql)
        return True, retval
    except lite.Error as e:
      return False, retval, e

  def drop_table(self, *tables):
    if len(tables)==0: tables=self.tables
    if type(tables[0]) is list: tables=tables[0]

    retval=''
    try:
      conn=lite.connect(self.file_name)
      with conn:
        for table in tables:
          curs=conn.cursor()
          sql='DROP TABLE IF EXISTS {};'.format(table.class_name())
          retval+=sql
          curs.execute(sql)
        return True, retval
    except lite.Error as e:
      return False, retval, e
    
  def insert(self, table, fields):
    if len(fields)==0: return

    fields=fields if type(fields) is list else [fields] #using list saves multiple records at once
    try:
      conn=lite.connect(self.file_name)
      with conn:
        curs=conn.cursor()
        sql='INSERT INTO {} ('.format(table.class_name())
        for k, v in fields[0].items():
          if not v.primary_key or v.value: #id included only if has value
            sql+='{}, '.format(k)
        sql=sql[0:-2]+') VALUES '
        for i in range(0, len(fields)):
          sql+='('
          for k, v in fields[i].items():
            if not v.primary_key or v.value:
              sql+='{}, '.format(Database.sql_value(v))
          sql=sql[0:-2]+'), '
        sql=sql[0:-2]+';'
        curs.execute(sql)
        return True, sql, curs.fetchall()
    except lite.Error as e:
      return False, sql, e

  def update(self, table, fields):
    try:
      conn=lite.connect(self.file_name)
      with conn:
        curs=conn.cursor()
        sql='UPDATE {} SET '.format(table.class_name())
        for k, v in fields.items():
          if v.primary_key:
            where='{}={}'.format(k, Database.sql_value(v))
          else:
            sql+='{}={}, '.format(k, Database.sql_value(v))
        sql=sql[0:-2]+'{};'.format(' WHERE '+where)
        curs.execute(sql)
        return True, sql, []
    except lite.Error as e:
      return False, sql, curs.fetchall()

  def delete(self, table, fields):
    try:
      conn=lite.connect(self.file_name)
      with conn:
        curs=conn.cursor()
        for k, v in fields.items():
          if v.primary_key:
            where='{}={}'.format(k, Database.sql_value(v))
        sql='DELETE FROM {}{};'.format(table.class_name(), ' WHERE '+where)
        curs.execute(sql)
        return True, sql, curs.fetchall()
    except lite.Error as e:
      return False, sql, e

  def select(self, table, fields='*', order=None):
    if type(fields) is str:
      fields=table.fields_as_obj() if fields=='*' else dict(map(lambda x: [x.strip(), table.field_by_name(x.strip())], fields.split(','))) 

    #συμπλήρωση λεξικού με πλήρη ονόματα πεδίων 'table.field' 
    fields=dict(map(lambda x: [table.field_as_fullname(x), x], fields.values()))
 
    #δημιουργία fields_string με ενδεχόμενα subqueries και προετοιμασία ενδεχόμενων join, επιλέγω τα joins (θεωρούνται ταχύτερα) 
    #όταν πρόκειται για εμφάνιση απλών πεδίων ενώ τα subqueries για υπολογισμό πολλαπλών πεδίων με function (count, sum, )
    #για να υποστηρίζονται υπολογισμοί σε πεδία πολλαπλών πινάκων (δεν έγινε εφικτό με το συνδυασμό join και group by)
    fields_string=''
    joins={}
    for k, v in fields.items():
      if v.join_on is None: 
        fields_string+=k+', '
      else:
        _='='.join(map(lambda x: x if '.' in x else table.class_name()+'.'+x, v.join_on.split('=')))
        if v.is_function is None:
          fields_string+=k+', '
          joins[v.remote_table()]=_
        else: #σε περίπτωση function όπως count, sum
          fields_string+='(SELECT {} FROM {} WHERE {}) {}, '.format(table.field_as_fullname(v), v.remote_table(), _, v.class_name())
    fields_string=fields_string[0:-2]

    where=''
    for k, v in fields.items():
      if v.value:
        if getattr(v, 'stack', 1)==2 and len(v.value.split(v.seperator))>1:
          _=v.value.split(v.seperator)
          if Database.sql_value(v, _[0])!='NULL':
            where+='{}{}{}{}'.format(' AND ' if where else '', k if not v.is_function else v.class_name(), '>=', Database.sql_value(v, _[0]))
          if Database.sql_value(v, _[1])!='NULL':
            where+='{}{}{}{}'.format(' AND ' if where else '', k if not v.is_function else v.class_name(), '<=', Database.sql_value(v, _[1]))
        else:
          where+='{}{}{}{}'.format(' AND ' if where else '', k if not v.is_function else v.class_name(), ' LIKE ' if '%' in v.value else '=', Database.sql_value(v))

    if order:
      i=-1
      for k, v in fields.items():
        if v.form_included:
          i+=1
          if order[i][0] in '><':
            order=(v.class_name() if v.join_on and v.is_function else k)+(' DESC' if order[i][0]=='<' else '')
            break

    return self.simple_select(table.class_name(), fields_string, joins, where, order)

  def simple_select(self, table, fields='*', joins={}, where='', order=None):
    try:
      conn=lite.connect(self.file_name)
      with conn:
        curs=conn.cursor()
        sql='SELECT {} FROM {}{}{}{};'.format(fields, table,
             ''.join([' LEFT JOIN '+k+' ON '+v for k, v in joins.items()]),
             ' WHERE '+where if where!='' else '',
             ' ORDER BY '+order if type(order) is str else '')
        curs.execute(sql)
        return True, sql, curs.fetchall()
    except lite.Error as e:
      return False, sql, e

  def count(self, table):
    try:
      conn=lite.connect(self.file_name)
      with conn:
        curs=conn.cursor()
        sql='SELECT count(*) FROM {};'.format(table.class_name())
        curs.execute(sql)
        return True, sql, curs.fetchone()[0]
    except lite.Error as e:
      return False, sql, e

###############################################################################
