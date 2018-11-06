### gc_tables.py #########################################################
'''Γενική βιβλιοθήκη για τη διαχείριση πινάκων δεδομένων'''

import re

class Table(object):
  '''General table operations'''  
  def __init__(self):
    pass

  def class_name(self):
    return type(self).__name__.lower()

  def superclass_name(self):
    return type(self).__bases__[0].__name__.lower()

  def fields_as_obj(self, attr=None):
    if attr==None:
      return dict(self.__dict__.items())  
    else:
      key=tuple(attr.keys())[0]
      value=tuple(attr.values())[0]
      return dict(filter(lambda x: getattr(x[1], key)==value, self.__dict__.items()))

  def fields_as_val(self, attr=None):
    _=self.fields_as_obj(attr)
    for k, v in _.items(): 
      _[k]=v.value
    return _

  def fields_set(self, values=[], attr=None):
    fields=self.fields_as_obj(attr)
    for f in fields.values(): 
      _=values.pop(0)
      if type(_) is str:
        f.value=_
      else:
        f.value=_[0]
        if not _[1] is None or _[0]=='': #no modify if no change happens
          lf=self.field_by_name(f.local_field())
          lf.value=_[1]
 
  def field_by_name(self, name):
    return self.fields_as_obj()[name.lower()]

  def field_as_fullname(self, obj): #ex. 'table.field'
    if obj.is_function is None:
      if obj.join_on is None:
        return self.class_name()+'.'+obj.class_name()
      else:
        return obj.remote_table()+'.'+obj.superclass_name()
    else:
      retval=obj.is_function
      while True:
        _=re.findall(r'[\(\+\-\*\/\//,]\s*[a-zA-Z]\w+\s*[\)\+\-\*\/\//,]', retval)
        #[1ος χαρκτ. από (+-*/,] [προαιρετικά κενά] [απαραίτητο ένα γράμμα (όχι αριθμ.)] [σειρά χαρκτ.] [προαιρετικά κενά] [τελ. χαρκτ. από )+-*/,]
        #ex. count(field), sum(field1+field2), avg(field1 + field2 - round(field3, 0))
        if len(_)==0: break
        retval=re.sub(r'[\(\+\-\*\/\//,]\s*[a-zA-Z]\w+\s*[\)\+\-\*\/\//,]', '{}', retval)
        _=map(lambda x: x[0]+self.class_name()+'.'+x[1:-1].strip()+x[-1] if obj.join_on is None else x[0]+obj.remote_table()+'.'+x[1:-1].strip()+x[-1], _)
        retval=retval.format(*_)
      return retval

##############################################################################