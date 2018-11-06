### gc_classes.py ############################################################
'''Γενική βιβλιοθήκη για τη λειτουργικότητα κλάσεων και αντικειμένων'''

class Grouped(object):
  '''Ομαδοποίηση αντικειμένων της ίδιας κλάσης. Ορίζουμε γνώρισμα κλάσης 
  smthing=Grouped() και συμπεριλαμβάνουμε στην __init__() την εντολή 
  self.smthing.append(self).'''
  
  def __init__(self):
    self.objects=[]

  def append(self, obj):
    self.objects.append(obj)

  def remove(self, obj):
    for i, x in enumerate(self.objects):
      if obj==x: objects.pop[i]

  def remove_all(self):
    self.objects=[]

  def exists(self, attr):
    for obj in self.objects:
      _=obj
      for x in tuple(attr.keys())[0].split('.'): #ex. 'object.value'
        _=getattr(_, x)
      if _==tuple(attr.values())[0]:
        return True
    return False

  def count(self, attr):
    retval=0
    for obj in self.objects:
      _=obj
      for x in tuple(attr.keys())[0].split('.'): #ex. 'object.value'
        _=getattr(_, x)
      if _==tuple(attr.values())[0]:
        retval+=1
    return retval

  def locate(self, attr):
    retval=[]
    for obj in self.objects:
      _=obj
      for x in tuple(attr.keys())[0].split('.'): #ex. 'object.value'
        _=getattr(_, x)
      if _==tuple(attr.values())[0]:
        retval.append(obj)
    return retval

##############################################################################