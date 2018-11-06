### gc_widgets.py ############################################################
'''Γενική βιβλιοθήκη για την προσαρμογή των widget της tkinter'''

import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as ms

class Valued(object):
  '''Διασύνδεση/διαχείριση μεταβλητής/αντικειμένου stringvar με widget'''
  def __init__(self):
    self._value=tk.StringVar()
 
  @property
  def value(self):
    return self._value.get()

  @value.setter
  def value(self, passval):
    self._value.set(passval)
  
class Entry(ttk.Entry, Valued):
  '''Custom ttk.Entry widget for text'''
  @staticmethod
  def type_converted(val):
    return val
    
  @staticmethod
  def value_formatted(val):
    return val

  stack=1 #number of values can inserted together with a seperator
  seperator='' #(like range 1-10 or list 1,2,3) 0 for unlimited values

  def __init__(self, parent, **kw):
    Valued.__init__(self) 
    ttk.Entry.__init__(self, parent, textvariable=self._value, **kw)
    self._value.trace("w", self.validate)
    self.backup_value=''
    for k, v in kw.items(): setattr(self, k, v)

  @property
  def values(self):
    return self.value.split(self.seperator)

  @values.setter
  def values(self, passval):
    self.seperator.join(passval)

  def validate(self, *args):
    _=[]
    self.backup_value=[self.backup_value] if type(self).seperator=='' else self.backup_value.split(type(self).seperator)
    for i, v in enumerate([self.value] if type(self).seperator=='' else self.value.split(type(self).seperator)[0:self.stack if self.stack>0 else None]):
      try:
        if not v in ' -': #for negative numbers
          v=self.value_formatted(self.type_converted(v))
        _.append(v)
      except:
        _.append('' if i>=len(self.backup_value) else self.backup_value[i])
    self.value=type(self).seperator.join(_)
    self.backup_value=self.value

class Entry_int(Entry):
  '''Custom ttk.Entry widget for integers'''
  @staticmethod
  def type_converted(val):
    return int(val)
    
  @staticmethod
  def value_formatted(val):
    return str(val)

class Entry_float(Entry):
  '''Custom ttk.Entry widget for floats'''
  @staticmethod
  def type_converted(val):
    return float(val)

  @staticmethod
  def value_formatted(val):
    return '{:.2f}'.format(val)

class Entry_join(Entry):
  '''Custom ttk.Entry widget calling values from joined tables'''
  def __init__(self, parent, form=None, **kw):
    Entry.__init__(self, parent, **kw)
    self.form=form
    self.field=list(self.form.table.fields_as_obj({'form_included':True}).values())[len(self.master.winfo_children())-1]
    self.local_value=None
    self.bind('<Up>', self.update)
    self.bind('<Down>', self.update)
    self.bind('<Return>', self.update)
    self.bind('<FocusOut>', self.update)
 
  def update(self, e):
    if self.value=='':
      self.value=''
      self.local_value=None
    else:
      if self.value.isdigit(): where='{} = {}'.format(e.widget.field.remote_field(), e.widget.value)
      else: where='{} LIKE "{}"'.format(e.widget.field.superclass_name(), e.widget.value+('%' if not '%' in e.widget.value else ''))
      error_free, message, data=self.form.db.simple_select(e.widget.field.remote_table(), '{}, {}'.format(e.widget.field.remote_field(), e.widget.field.superclass_name()), where=where)
      if not error_free:
        ms.showerror('X', (message, '\n', data))
        self.value=''
        self.local_value=None
      elif len(data)==0:
        self.value=''
        self.local_value=None
      elif len(data)>0:
        self.value=data[0][1]
        self.local_value=data[0][0]

##############################################################################