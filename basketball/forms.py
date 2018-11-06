### forms.py #################################################################
'''Εξειδίκευση βιβλιοθήκης φορμών/ οθόνων για τη συγκεκριμένη εφαρμογή'''

import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as ms

import gc_forms as gcfo
import gc_widgets as gcw
import tables as ta

class Style(object):
  '''Set widgets styling'''
  def frame(): return {'style':'Frame.TFrame'}
  #def popup_frame(): return {'style':'Popup.TFrame'}
  def current_frame(): return {'style':'Current.TFrame'}
  def label(): return {'style':'Label.TLabel'}
  def head_label(): return {'style':'Head.TLabel'}
  def popup_label(): return {'style':'Popup.TLabel'}
  def entry(): return {'style':'Entry.TEntry'}
  def button(): return {'width':12, 'height':2, 'relief':'groove', 'background':'lightgreen'}
  def side_button(): return {'width':5, 'height':4, 'relief':'groove', 'background':'lightgreen'}

  def __init__(self):
    ttk.Style().configure('Frame.TFrame', borderwidth=0, highlightthickness=0, background='lightgreen')
    #ttk.Style().configure('Popup.TFrame', borderwidth=0, highlightthickness=0, background='white')
    ttk.Style().configure('Current.TFrame', borderwidth=0, highlightthickness=0, background='orange')
    ttk.Style().configure('Entry.TEntry', padding=10)
    ttk.Style().configure('Label.TLabel', background='lightgreen')
    ttk.Style().configure('Head.TLabel', padding=10, background='orange')
    ttk.Style().configure('Popup.TLabel', padding=2, background='white')
 
class Basic(gcfo.Basic):
  '''Skeleton form with common widgets and operations'''
  def __init__(self, root, db):
    gcfo.Basic.__init__(self)
    self.root=root
    self.db=db
    self.style=Style()
    self.rows_per_page=10

  def draw(self):
    '''
    +-header-----------------------------------------------------------------+                                                              (unused)|
    +------------------------------------------------------------------------+
    +-body-------------------------------------------------------------------+
    |+-main-----------------------------------------------------------------+|
    ||+-main_left---++-main_central-------------------------++-main_right--+||
    |||             ||+-central_top------------------------+||             |||
    |||             |||                       (σελίδα 1/1))|||             |||
    |||             ||+------------------------------------+||             |||
    |||             ||+-central_bottom---------------------+||             |||
    |||             |||+-heads----------------------------+|||             |||
    |||             ||||          (id) (όνομα)  ...       ||||             |||
    |||             |||+----------------------------------+|||             |||
    |||             |||+-data_row 1-----------------------+|||             |||
    |||  (buttons)  ||||           ..   .....   ...       ||||  (buttons)  |||
    |||             |||+----------------------------------+|||             |||
    |||             |||+-data_row 2-----------------------+|||             |||
    |||             ||||           ..   .....   ...       ||||             |||
    |||             |||+----------------------------------+|||             |||
    |||             |||+-data_row N-----------------------+|||             |||
    |||             ||||           ..   .....   ...       ||||             |||
    |||             |||+----------------------------------+|||             |||
    |||             ||+------------------------------------+||             |||
    ||+-------------++--------------------------------------++-------------+||
    |+----------------------------------------------------------------------+|
    |+-tools----------------------------------------------------------------+|
    ||                             (buttons)                                ||
    |+----------------------------------------------------------------------+|
    +------------------------------------------------------------------------+
    +-footer-----------------------------------------------------------------+
    |                                                             (copyright)|
    +------------------------------------------------------------------------+
    '''

    header=ttk.Frame(self.root, **Style.frame())
    header.pack(fill='both', expand=True, side='top')

    body=ttk.Frame(self.root, **Style.frame())
    body.pack(fill='both', expand=False, side='top')
    if body:

      #if commands used in the following part of code to show widgets hierarchy 
      main=ttk.Frame(body, **Style.frame())
      main.pack(fill='none', expand=True, side='top')
      if main:

        #left side navigation buttons
        main_left=ttk.Frame(main, **Style.frame())
        main_left.pack(fill='none', expand=True, side='left')
        if main_left:
          self.bt_start=tk.Button(main_left, text='|<', **Style.side_button())
          self.bt_start.pack(padx=4, pady=4)
          self.bt_prev=tk.Button(main_left, text='<', **Style.side_button())
          self.bt_prev.pack(padx=4, pady=4)

        #central
        main_central=ttk.Frame(main, **Style.frame())
        main_central.pack(fill='none', expand=True, side='left')
        if main_central:

          #info message
          central_top=ttk.Frame(main_central, **Style.frame())
          central_top.pack(fill='both', expand=True, side='top')
          if central_top: 
            info=ttk.Frame(central_top, **Style.frame())
            info.pack(fill='none', expand=False, side='right')
            if info:
              self.info_box=ttk.Label(info, text='Σελίδα 0/0 (0 εγγραφές)', **Style.label())
              self.info_box.grid(row=0, column=0, padx=1, pady=1)

          #heads and data rows
          central_bottom=ttk.Frame(main_central, **Style.frame())
          central_bottom.pack(fill='none', expand=False, side='top')
          if central_bottom:

            heads=ttk.Frame(central_bottom, **Style.frame())
            heads.pack(fill='none', expand=False, side='top')
            for col, field in enumerate(self.table.fields_as_obj({'form_included':True}).values()):
              ttk.Label(heads, **Style.head_label(), text=field.label, width=field.width).grid(row=0, column=col, padx=1, pady=1)

            self.data_box=central_bottom
            for row in range(self.rows_per_page):
              data_row=ttk.Frame(central_bottom, **Style.frame())
              data_row.pack(fill='none', expand=False, side='top')
              for col, field in enumerate(self.table.fields_as_obj({'form_included':True}).values()):
                if field.join_on and field.edit_included: _=gcw.Entry_join(data_row, **Style.entry(), width=field.width, form=self)
                elif field.typeof=='float': _=gcw.Entry_float(data_row, **Style.entry(), width=field.width)
                elif field.typeof=='int': _=gcw.Entry_int(data_row, **Style.entry(), width=field.width)
                else: _=gcw.Entry(data_row, **Style.entry(), width=field.width)
                _.grid(row=row, column=col, padx=1, pady=1)
              gcw.Entry.seperator='~'
            self.page_clear()

        #right side navigation buttons
        main_right=ttk.Frame(main, **Style.frame())
        main_right.pack(fill='none', expand=True, side='left')
        if main_right:
          self.bt_next=tk.Button(main_right, text='>', **Style.side_button())
          self.bt_next.pack(padx=4, pady=4)
          self.bt_end=tk.Button(main_right, text='>|', **Style.side_button())
          self.bt_end.pack(padx=4, pady=4)

      #command buttons
      tools=ttk.Frame(body, **Style.frame())
      tools.pack(fill='none', expand=False, side='top')
      if tools:
        self.bt_insert=tk.Button(tools, text='Νέα εγγραφή', **Style.button())
        self.bt_select=tk.Button(tools, text='Αναζήτηση', **Style.button())
        self.bt_update=tk.Button(tools, text='Τροποποίηση', **Style.button())
        self.bt_delete=tk.Button(tools, text='Διαγραφή', **Style.button())
        self.bt_ok=tk.Button(tools, text='ΟΚ', **Style.button())
        self.bt_cancel=tk.Button(tools, text='ΑΚΥΡΟ', **Style.button())

    #footer
    footer=ttk.Frame(self.root, **Style.frame())
    footer.pack(fill='x', expand=False, side='right')
    if footer:
      ttk.Label(footer, text='Athens 2018, Giannis Clipper', **Style.label()).grid(row=0, column=0, padx=1, pady=1)

    #define events
    self.events.append(gcfo.Event(widget=self.bt_insert, typeof='<ButtonRelease-1>', action=self.insert, onenable=lambda x: x.pack(side='left', padx=4, pady=4), ondisable=lambda x: x.pack_forget()))
    self.events.append(gcfo.Event(widget=self.bt_select, typeof='<ButtonRelease-1>', action=self.select, onenable=lambda x: x.pack(side='left', padx=4, pady=4), ondisable=lambda x: x.pack_forget()))
    self.events.append(gcfo.Event(widget=self.bt_update, typeof='<ButtonRelease-1>', action=self.update, onenable=lambda x: x.pack(side='left', padx=4, pady=4), ondisable=lambda x: x.pack_forget()))
    self.events.append(gcfo.Event(widget=self.bt_delete, typeof='<ButtonRelease-1>', action=self.delete, onenable=lambda x: x.pack(side='left', padx=4, pady=4), ondisable=lambda x: x.pack_forget()))
    self.events.append(gcfo.Event(widget=self.bt_ok, typeof='<ButtonRelease-1>', action=self.ok, onenable=lambda x: x.pack(side='left', padx=4, pady=4), ondisable=lambda x: x.pack_forget()))
    self.events.append(gcfo.Event(widget=self.bt_cancel, typeof='<ButtonRelease-1>', action=self.cancel, onenable=lambda x: x.pack(side='left', padx=4, pady=4), ondisable=lambda x: x.pack_forget()))
    self.events.append(gcfo.Event(widget=self.bt_start, typeof='<ButtonRelease-1>', action=self.start, onenable=lambda x: x.pack(side='top', padx=4, pady=4), ondisable=lambda x: x.pack_forget()))
    self.events.append(gcfo.Event(widget=self.bt_prev, typeof='<ButtonRelease-1>', action=self.prev, onenable=lambda x: x.pack(side='top', padx=4, pady=4), ondisable=lambda x: x.pack_forget()))
    self.events.append(gcfo.Event(widget=self.bt_next, typeof='<ButtonRelease-1>', action=self.next, onenable=lambda x: x.pack(side='top', padx=4, pady=4), ondisable=lambda x: x.pack_forget()))
    self.events.append(gcfo.Event(widget=self.bt_end, typeof='<ButtonRelease-1>', action=self.end, onenable=lambda x: x.pack(side='top', padx=4, pady=4), ondisable=lambda x: x.pack_forget()))

    for w in self.heads():
      self.events.append(gcfo.Event(widget=w, typeof='<ButtonRelease-1>', action=self.order_select))
    for row in self.rows_as_frames():
      for w in row.winfo_children():
        self.events.append(gcfo.Event(widget=w, typeof='<ButtonRelease-1>', action=self.row_select))
 
    self.table.all.remove_all()
    self.nostate()

  def row_select(self, e=None):
    _=gcfo.Basic.row_select(self, e)
    for w in self.rows_as_frames():
      w.configure(**Style.frame())
    if _: _.configure(**Style.current_frame())

class Club(Basic):
  '''form configured for clubs'''
  def __init__(self, root, db):
    Basic.__init__(self, root, db)
    self.table=ta.Club(as_structure=True)

class Player(Basic):
  '''Form configured for players'''
  def __init__(self, root, db):
    Basic.__init__(self, root, db)
    self.table=ta.Player(as_structure=True)

class Coach(Basic):
  '''Form configured for coaches'''
  def __init__(self, root, db):
    Basic.__init__(self, root, db)
    self.table=ta.Coach(as_structure=True)

class Country(Basic):
  '''Form configured for countries'''
  def __init__(self, root, db):
    Basic.__init__(self, root, db)
    self.table=ta.Country(as_structure=True)

class Position(Basic):
  '''Form configured for positions'''
  def __init__(self, root, db):
    Basic.__init__(self, root, db)
    self.table=ta.Position(as_structure=True)

##############################################################################