### gc_fields.py #########################################################
'''Γενική βιβλιοθήκη για τη διαχείριση πεδίων δεδομένων'''

class Field(object):
  '''Describe string fields'''
  typeof='str'
  length=15 #value length
  width=15 #widget width
  unique=False
  not_null=False
  primary_key=False
  join_on=None #ex. 'field=table.field'
  is_function=None #ex. 'count(table.field)', 'sum(field1+field2)'
  save_included=True #insert/update operations 
  view_included=True #select operations
  form_included=True #display in form
  edit_included=True #edit by user

  def __init__(self, **kw):
    self.value=''
    for k, v in kw.items(): setattr(self, k, v)

  def class_name(self):
    return type(self).__name__.lower()

  def superclass_name(self):
    return type(self).__bases__[0].__name__.lower()

  def remote_table(self): #ex. 'club_id=club.id' results 'club'
    return '' if self.join_on is None else list(filter(lambda x: '.' in x, self.join_on.split('=')))[0].split('.')[0]

  def remote_field(self): #ex. 'club_id=club.id' results 'id'
    return '' if self.join_on is None else list(filter(lambda x: '.' in x, self.join_on.split('=')))[0].split('.')[1]

  def local_field(self): #ex. 'club_id=club.id' results 'club_id'
    return '' if self.join_on is None else list(filter(lambda x: not '.' in x, self.join_on.split('=')))[0]

class Field_int(Field):
  '''Describe integer fields'''
  typeof='int'
  length=8
  width=8
  auto_increment=False

  def __init__(self, **kw):
    Field.__init__(self, **kw)
    for k, v in kw.items(): setattr(self, k, v)

class Field_float(Field):
  '''Describe float fields'''
  typeof='float'
  length=8
  width=8
  def __init__(self, **kw):
    Field.__init__(self, **kw)
    for k, v in kw.items(): setattr(self, k, v)

class Stack_values(object):
  '''To manage multiple values''' 
  stack=0 #number of values together with a seperator
  seperator=',' #(like range 1-10 or list 1,2,3) 0 for unlimited values
  def __init__(self, **kw):
    for k, v in kw.items(): setattr(self, k, v)

##############################################################################