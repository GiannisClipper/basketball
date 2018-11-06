### tables.py #########################################################
'''Επέκταση βιβλιοθήκης για τη διαχείριση πινάκων δεδομένων'''

import gc_classes as gcc
import gc_tables as gct
import gc_fields as gcf
import fields as fi

class Basic(gct.Table):
  '''Describe common fields'''
  def __init__(self):
    self.id=fi.Id()
    self.name=fi.Name()

class Club(Basic):
  '''Describe basketball club'''
  all=gcc.Grouped()
  def __init__(self, as_structure=False):
    if not as_structure: self.all.append(self)
    Basic.__init__(self)
    self.name.label='Όνομα ομάδας'
    self.coach_count=fi.Coach_count(join_on='id=coach.club_id')
    self.player_count=fi.Player_count(join_on='id=player.club_id')
    self.player_avg_age=fi.Player_avg_age(join_on='id=player.club_id')
    self.player_avg_height=fi.Player_avg_height(join_on='id=player.club_id')
    self._url=gcf.Field(save_included=False, view_included=False, form_included=False)

class Person(Basic):
  '''Describe persons (players, coaches) common fields'''
  def __init__(self):
    Basic.__init__(self)
    self.club_id=fi.Club_id()
    self.club_name=fi.Club_name()
    self.country_id=fi.Country_id()
    self.country_name=fi.Country_name()
    self.birth=fi.Birth()
 
class Coach(Person):
  '''Describe coaches'''
  all=gcc.Grouped()
  def __init__(self, as_structure=False):
    if not as_structure: self.all.append(self)
    Person.__init__(self)
    self.name.label='Όνομα προπονητή'

class Player(Person):
  '''Describe players'''
  all=gcc.Grouped()
  def __init__(self, as_structure=False):
    if not as_structure: self.all.append(self)
    Person.__init__(self)
    self.name.label='Όνομα παίκτη'
    self.position_id=fi.Position_id()
    self.position_name=fi.Position_name()
    self.height=fi.Height()
    self.dorsal=fi.Dorsal()

class Country(Basic):
  '''Describe persons countries'''
  all=gcc.Grouped()
  def __init__(self, as_structure=False):
    if not as_structure: self.all.append(self)
    Basic.__init__(self)
    self.name.label='Όνομα χώρας'
    self.coach_count=fi.Coach_count(join_on='id=coach.country_id')
    self.player_count=fi.Player_count(join_on='id=player.country_id')
    self.player_avg_age=fi.Player_avg_age(join_on='id=player.country_id')
    self.player_avg_height=fi.Player_avg_height(join_on='id=player.country_id')
    
class Position(Basic):
  '''Describe players positions'''
  all=gcc.Grouped()
  def __init__(self, as_structure=False):
    if not as_structure: self.all.append(self)
    Basic.__init__(self)
    self.name.label='Όνομα θέσης'
    self.player_count=fi.Player_count(join_on='id=player.position_id')
    self.player_avg_age=fi.Player_avg_age(join_on='id=player.position_id')
    self.player_avg_height=fi.Player_avg_height(join_on='id=player.position_id')

##############################################################################