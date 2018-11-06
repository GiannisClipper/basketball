### gc_forms.py ##############################################################
'''Γενική βιβλιοθήκη διαχείρισης φορμών/ οθόνων'''

import tkinter.messagebox as ms
import gc_widgets as gcw

class Event(object):
  '''Για την οργάνωση και διαχείριση των συμβάντων μιας φόρμας'''
  def __init__(self, **kw):
    self.widget=None
    self.typeof=None
    self.action=None
    self.onenable=None
    self.ondisable=None
    for k, v in kw.items(): setattr(self, k, v)

class Basic(object):
  '''Βασική λειτουργικότητα φόρμας/ οθόνης'''
  def __init__(self, **kw):
    self.db=None
    self.table=None
    self.rows_per_page=1
    self.data_box=None #frame type
    self.info_box=None #label type
    self._data_index=-1
    self.state=None
    self.events=[]
    for k, v in kw.items(): setattr(self, k, v)

  @property
  def data_index(self):
    return self._data_index
  @data_index.setter
  def data_index(self, passval):
    self._data_index=min(max(0, passval), self.data_count()-1)
    self.row_select()

  def set_events(self, *passval):
    for e in self.events:
      if e.action in passval:
        if e.onenable: e.onenable(e.widget)
        e.widget.bind(e.typeof, e.action)
      else:
        e.widget.bind(e.typeof, lambda e: False)
        if e.ondisable: e.ondisable(e.widget)

  def nostate(self):
    self.state=None
    self.data_index-=1
    self.page_refresh()
    self.set_events(self.insert, self.select)

  def insert(self, e=None):
    self.state='insert'
    self.table.all.remove_all()
    self.data_index=-1
    self.insert_repeated()

  def insert_repeated(self): 
    _=self.table.__class__()
    self.data_index+=1
    self.page_refresh()
    self.set_events(self.ok, self.cancel) #, self.join_values)
    self.row_edit()

  def select(self, e):
    self.state='select'
    self.table.all.remove_all()
    _=self.table.__class__()
    self.data_index=0
    self.page_refresh()
    self.set_events(self.ok, self.cancel, self.order_select)
    self.row_edit(all=True)

  def selected(self):
    self.state='selected'
    self.set_events(self.insert, self.select, self.update, self.delete, 
    	self.start, self.prev, self.next, self.end, self.row_select)

  def update(self, e=None):
    self.state='update'
    self.set_events(self.ok, self.cancel) #, self.join_values)
    self.row_edit() 

  def delete(self, e=None):
    for v in self.table.all.objects[self.data_index].fields_as_obj({'form_included':True}).values():
      if v.join_on and v.is_function and v.value:
        ms.showwarning('!', 'Δεν επιτρέπεται διαγραφή,'+'\n'+' υπάρχουν συνδεδεμένες εγγραφές.')
        return
    self.state='delete'
    self.set_events(self.ok, self.cancel)

  def ok(self, e):
    if self.state=='insert':
      self.table.all.objects[self.data_index].fields_set(list(map(lambda x: x.value if not type(x) is gcw.Entry_join else (x.value, x.local_value), self.row_current_widgets())), {'form_included':True})
      error_free, message, data=self.db.insert(self.table, self.table.all.objects[self.data_index].fields_as_obj({'save_included':True}))
      if not error_free:
        ms.showerror('X', (message, '\n', data))
      else:
        print(message, data)
        self.insert_repeated()

    elif self.state=='select':
      self.table.all.objects[self.data_index].fields_set(list(map(lambda x: x.value, self.row_current_widgets())), {'form_included':True})
      error_free, message, data=self.db.select(self.table, self.table.all.objects[self.data_index].fields_as_obj({'view_included':True}), list(map(lambda x: x['text'], self.heads())))
      if not error_free:
        ms.showerror('X', (message, '\n', data))
        self.nostate()
      else:
        print(message, len(data))
        if len(data)>0:
          self.table.all.remove_all()
          for row in data:
            _=self.table.__class__() #creates new object
            for i, field in enumerate(_.fields_as_obj({'view_included':True}).values()):
              field.value=row[i]
            self.data_index=0
            self.page_refresh()
            self.selected()
        else:
          ms.showwarning('!', ('Δεν βρέθηκαν σχετικές εγγραφές!'))

    elif self.state=='update':
      backup_values=list(self.table.all.objects[self.data_index].fields_as_val().values())
      self.table.all.objects[self.data_index].fields_set(list(map(lambda x: x.value if not type(x) is gcw.Entry_join else (x.value, x.local_value), self.row_current_widgets())), {'form_included':True})
      error_free, message, data=self.db.update(self.table, self.table.all.objects[self.data_index].fields_as_obj({'save_included':True}))
      if not error_free:
        ms.showerror('X', (message, '\n', data))
        self.table.all.objects[self.data_index].fields_set(backup_values)
        self.row_refresh(self.rows_as_frames()[self.row_current()])
        self.update()
      else:
        print(message, data)
        self.row_noedit()
        self.selected()

    elif self.state=='delete':
      error_free, message, data=self.db.delete(self.table, self.table.all.objects[self.data_index].fields_as_obj({'save_included':True}))
      if not error_free:
        ms.showerror('X', (message, '\n', data))
        self.selected()
      else:
        print(message, data)
        self.table.all.objects.pop(self.data_index)
        self.data_index=self.data_index
        self.page_refresh()
        if self.data_count()>0:
          self.selected()
        else:
          self.nostate()
 
  def cancel(self, e): 
    if self.state=='insert':
      self.table.all.objects.pop()
      if self.data_count()>0:
        self.selected()
      else:
        self.nostate()
    elif self.state=='select':
      self.table.all.objects.pop()
      self.nostate()
    elif self.state=='update':
      self.row_refresh(self.rows_as_frames()[self.row_current()])
      self.selected()
    elif self.state=='delete':
      self.selected()
    self.row_noedit()

  def start(self, e):
    if self.data_index!=0:
      self.data_index=0
      self.page_refresh()

  def prev(self, e):
    if self.data_index!=0:
      self.data_index-=self.rows_per_page
      self.page_refresh()

  def next(self, e):
    if self.data_index!=self.data_count()-1: 
      self.data_index+=self.rows_per_page
      self.page_refresh()

  def end(self, e):
    if self.data_index!=self.data_count()-1: 
      self.data_index=self.data_count()-1
      self.page_refresh()

  def order_select(self, e):
    for w in e.widget.master.winfo_children():
      _='' if w!=e.widget else '>' if not w['text'][0] in '><' else '<' if w['text'][0]=='>' else ''
      w.configure(text=_+w['text'][1:] if w['text'][0] in '><' else _+w['text'])

  def row_select(self, e=None):
    if self.data_count()>0:
      frames=self.rows_as_frames()
      if not e is None: 
        self.data_index=(self.page_current()-1)*self.rows_per_page+frames.index(e.widget.master)
      return frames[self.row_current()]
    return None

  def data_count(self):
    return len(self.table.all.objects)

  def pages_count(self):
    return (self.data_count()//self.rows_per_page+(1 if self.data_count()%self.rows_per_page>0 else 0)) if self.data_count()>0 else 0

  def page_current(self):
    return self.data_index//self.rows_per_page+1

  def page_clear(self):
    for row in self.rows_as_frames():
      for widget in row.winfo_children():
        widget.configure(state='disabled') 
        widget.value=''

  def page_refresh(self):
    self.page_clear()
    self.info_box.configure(text='Σελίδα {}/{} ({} εγγραφές)'.format(self.page_current(), self.pages_count(), self.data_count()))
    for row in self.rows_as_frames():
      if (self.page_current()-1)*self.rows_per_page+(self.rows_as_frames().index(row)+1)>self.data_count() or self.data_count()==0: 
      	break
      self.row_refresh(row)

  def rows_as_frames(self):
  	return self.data_box.winfo_children()[1:]

  def row_current(self):
    return self.data_index%self.rows_per_page

  def row_current_widgets(self):
  	return self.rows_as_frames()[self.row_current()].winfo_children()

  def row_refresh(self, row):
    widgets=row.winfo_children()
    for column, field in enumerate(self.table.all.objects[(self.page_current()-1)*self.rows_per_page+self.rows_as_frames().index(row)].fields_as_obj({'form_included':True}).values()):
      widgets[column].value=field.value

  def heads(self):
    return self.data_box.winfo_children()[0].winfo_children()

  def columns_per_row(self):
    return len(self.rows_as_frames()[0].winfo_children())

  def row_edit(self, e=None, all=False):
    _=None
    fields=list(self.table.fields_as_obj({'form_included':True}).values())
    for i, w in enumerate(self.row_current_widgets()):
      if fields[i].edit_included or all: 
        w.configure(state='normal')
        w.stack=getattr(fields[i], 'stack', 1) if self.state=='select' else 1
        w.seperator=getattr(fields[i], 'seperator', '') if self.state=='select' else ''
        if not _: _=w
    if _: _.focus()

  def row_noedit(self, e=None):
    for w in self.row_current_widgets():
      w.configure(state='disabled')
      
##############################################################################