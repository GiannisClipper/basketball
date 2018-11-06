### main.py #################################################################
'''Έναρξη της εφαρμογής και διαχείριση του μενού επιλογών'''

import os
import sys
sys.path.append('..\\gclib')

import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as ms

import gc_database as gcdb
import tables as ta
import gc_widgets as gcw
import forms as fo
import url as ur

class App(tk.Frame):
  def __init__(self):
    self.db=gcdb.Database('basketball.db', ta.Club(as_structure=True), ta.Player(as_structure=True),
      ta.Coach(as_structure=True), ta.Country(as_structure=True), ta.Position(as_structure=True))
    root.geometry('1024x600')
    root.resizable(False, False)
    root.title('Basketball app')
    root.configure(bg='lightgreen')
    self.center()
    self.menu()
    self.img=tk.PhotoImage(file='basketball.gif')
    self.show_image()

  def center(self):
    root.update_idletasks()
    width=root.winfo_width()
    height=root.winfo_height()
    x=int(root.winfo_screenwidth()/2-width/2)
    y=int(root.winfo_screenheight()/2-height/1.8)
    root.geometry('{}x{}+{}+{}'.format(width, height, x, y))

  def clear_screen(self):
    widgets=root.pack_slaves()
    for w in widgets:
      w.destroy()

  def show_image(self):
    self.clear_screen()
    tk.Label(root, background='lightgreen', image=self.img).pack(fill="both", expand=True, side="bottom")

  def menu(self):
    main=tk.Menu(root) #σύνδεση του μενού main με το παράθυρο root
    root.config(menu=main)  #επίσης σύνδεσε το παράθυρο με το μενού

    manage_data=tk.Menu(main, tearoff=False) #file: ένα νέο αντικείμενο τύπου Menu
    main.add_cascade(label='Διαχείριση πινάκων', menu=manage_data, underline=0) #σύνδεση του μενού manage με το main
    manage_data.add_command(label='Ομάδες', command=self.club, underline=0)
    manage_data.add_separator()
    manage_data.add_command(label='Παίκτες', command=self.player, underline=0)
    manage_data.add_command(label='Προπονητές', command=self.coach, underline=0)
    manage_data.add_separator()
    manage_data.add_command(label='Χώρες', command=self.country, underline=0)
    manage_data.add_command(label='Θέσεις', command=self.position, underline=0)

    manage_app=tk.Menu(main, tearoff=False)
    main.add_cascade(label='Διαχείριση βάσης', menu=manage_app, underline=0)
    manage_app.add_command(label='Διαγραφή βάσης δεδομένων', command=self.drop_database, underline=0)
    manage_app.add_command(label='Δημιουργία βάσης δεδομένων', command=self.create_database, underline=0)
    manage_app.add_separator()
    manage_app.add_command(label='Αίτηση δεδομένων από ιστοσελίδα στο διαδίκτυο', command=self.request_and_extract_data_1, underline=0)
    manage_app.add_command(label='Αίτηση δεδομένων από αρχεία html στο δίσκο', command=self.request_and_extract_data_2, underline=0)
    manage_app.add_separator()
    manage_app.add_command(label='Αποθήκευση στη βάση δεδομένων', command=self.save_data, underline=0)

    exit_app=tk.Menu(main, tearoff=False)
    main.add_cascade(label='Κλείσιμο', menu=exit_app, underline=0)
    exit_app.add_command(label='Καθαρισμός οθόνης', command=self.show_image, underline=0)
    exit_app.add_command(label='Τέλος προγράμματος', command=root.destroy, underline=0)

  def club(self):
    self.clear_screen()
    fo.Club(root, self.db).draw()

  def player(self):
    self.clear_screen()
    fo.Player(root, self.db).draw()

  def coach(self):
    self.clear_screen()
    fo.Coach(root, self.db).draw()

  def country(self):
    self.clear_screen()
    fo.Country(root, self.db).draw()

  def position(self):
    self.clear_screen()
    fo.Position(root, self.db).draw()

  def request_and_extract_data_1(self):
    #request urls and extract data
    self.clear_screen()
    text=tk.Text(root, bg=root.cget('bg'))
    text.pack(fill='both', expand=True, side='top')
    text.insert('end', 'Διαδικασία αίτησης δεδομένων από ιστοσελίδα στο διαδίκτυο...\n')
    if not self.verify():
      self.clear_screen()
      self.show_image()
      return
    ta.Club.all.remove_all()
    ta.Player.all.remove_all()
    ta.Coach.all.remove_all()
    ta.Country.all.remove_all()
    ta.Position.all.remove_all()
    request=ur.Request()
    request.output=lambda x: text.insert('end', x)
    base_url='http://www.euroleague.net'
    request.league_page(base_url+'/?geoip=disabled')
    for club in ta.Club.all.objects[0:]:
      request.club_page(club.name.value, base_url+club._url.value)
    request.normalise_data()
    text.insert('end', '\nΛήξη διαδικασίας.\n')    

  def request_and_extract_data_2(self):
    #request urls and extract data
    self.clear_screen()
    text=tk.Text(root, bg=root.cget('bg'))
    text.pack(fill='both', expand=True, side='top')
    text.insert('end', 'Διαδικασία αίτησης δεδομένων από html αρχεία στο δίσκο...\n')
    if not self.verify():
      self.clear_screen()
      self.show_image()
      return
    ta.Club.all.remove_all()
    ta.Player.all.remove_all()
    ta.Coach.all.remove_all()
    ta.Country.all.remove_all()
    ta.Position.all.remove_all()
    request=ur.Request()
    request.output=lambda x: text.insert('end', x)
    for fi in os.listdir(os.getcwd()+'\\html'):
      if fi[-5:]=='.html' or fi[-4:]=='.htm':
        request.club_page(fi.split('.')[0], os.getcwd()+'\\html\\'+fi)
    request.normalise_data()
    text.insert('end', '\nΛήξη διαδικασίας.\n')    

  def save_data(self):
    #save data on disk (database)
    self.clear_screen()
    text=tk.Text(root, bg=root.cget('bg'))
    text.pack(fill='both', expand=True, side='top')
    text.insert('end', 'Διαδικασία αποθήκευσης στη βάση δεδομένων...\n')
    if len(ta.Club.all.objects)==0:
      ms.showwarning('X','Δεν υπάρχουν δεδομένα για αποθήκευση')
    elif ms.askyesno('?', str(len(ta.Club.all.objects))+' ομάδες, παρακαλώ επιβεβαιώστε την επιλογή σας:'):
      print(self.db.insert(ta.Club(as_structure=True), list(map(lambda x: x.fields_as_obj({'save_included':True}), ta.Club.all.objects))))
      print(self.db.insert(ta.Player(as_structure=True), list(map(lambda x: x.fields_as_obj({'save_included':True}), ta.Player.all.objects))))
      print(self.db.insert(ta.Coach(as_structure=True), list(map(lambda x: x.fields_as_obj({'save_included':True}), ta.Coach.all.objects))))
      print(self.db.insert(ta.Country(as_structure=True), list(map(lambda x: x.fields_as_obj({'save_included':True}), ta.Country.all.objects))))
      print(self.db.insert(ta.Position(as_structure=True), list(map(lambda x: x.fields_as_obj({'save_included':True}), ta.Position.all.objects))))
      ta.Club.all.remove_all()
      ta.Player.all.remove_all()
      ta.Coach.all.remove_all()
      ta.Country.all.remove_all()
      ta.Position.all.remove_all()
      text.insert('end', '\nΛήξη διαδικασίας.\n')
      return
    self.clear_screen()
    self.show_image()
    return

  def create_database(self):
    '''create database tables'''
    self.clear_screen()
    text=tk.Text(root, bg=root.cget('bg'))
    text.pack(fill='both', expand=True, side='top')
    text.insert('end', 'Διαδικασία δημιουργίας βάσης δεδομένων...\n')
    if not self.verify():
      self.clear_screen()
      self.show_image()
      return
    text.insert('end', self.db.create_table())
    text.insert('end', '\nΛήξη διαδικασίας.\n')

  def drop_database(self):
    '''drop database tables'''
    self.clear_screen()
    text=tk.Text(root, bg=root.cget('bg'))
    text.pack(fill='both', expand=True, side='top')
    text.insert('end', 'Διαδικασία διαγραφής βάσης δεδομένων...\n')
    if not self.verify():
      self.clear_screen()
      self.show_image()
      return
    text.insert('end', self.db.drop_table())
    text.insert('end', '\nΛήξη διαδικασίας.\n')

  def verify(self):
    return ms.askyesno('?',
      'Η τυπική διαδικασία εισαγωγής δεδομένων από το διαδίκτυο\n'+
      'ή από αρχεία στο δίσκο απαιτεί την ακόλουθη σειρά εργασιών:\n\n'+
      '1. Διαγραφή της βάσης δεδομένων\n'+
      ' (τυχόν προηγούμενων εγγραφών)\n\n'+
      '2. Δημιουργία της βάσης δεδομένων\n\n'+
      '3. Αίτηση δεδομένων από ιστοσελίδα στο διαδίκτυο\n'+
      ' (ή από html αρχεία στο δίσκο)\n\n'+
      '4. Αποθήκευση των δεδομένων στη βάση\n\n'+
      'Παρακαλώ επιβεβαιώστε ή ακυρώστε την επιλογή σας:')
      
if __name__ == '__main__':
  root=tk.Tk()
  App()
  root.mainloop()
