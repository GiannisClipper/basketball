### fields.py #########################################################
'''Επέκταση βιβλιοθήκης για τη διαχείριση πεδίων δεδομένων'''

import gc_fields as gcf

class Id(gcf.Field_int, gcf.Stack_values):
  '''Describe id'''
  length=3
  width=6
  label='ID'
  edit_included=False
  not_null=True
  primary_key=True
  auto_increment=True

  def __init__(self, **kw):
    gcf.Field_int.__init__(self, **kw)
    gcf.Stack_values.__init__(self, stack=2, seperator='~')
    for k, v in kw.items(): setattr(self, k, v)

class Club_id(Id):
  '''Describe club id in player, coach tables'''
  form_included=False
  not_null=False
  primary_key=False
  auto_increment=False

  def __init__(self, **kw):
    Id.__init__(self, **kw)
    for k, v in kw.items(): setattr(self, k, v)

class Country_id(Id):
  '''Describe country id in player, coach tables'''
  form_included=False
  not_null=False
  primary_key=False
  auto_increment=False

  def __init__(self, **kw):
    Id.__init__(self, **kw)
    for k, v in kw.items(): setattr(self, k, v)

class Position_id(Id):
  '''Describe position id in player table'''
  form_included=False
  not_null=False
  primary_key=False
  auto_increment=False

  def __init__(self, **kw):
    Id.__init__(self, **kw)
    for k, v in kw.items(): setattr(self, k, v)

class Name(gcf.Field):
  '''Describe name'''
  length=40
  width=40
  label='Όνομα'
  unique=True
  not_null=True

  def __init__(self, **kw):
    gcf.Field.__init__(self, **kw)
    for k, v in kw.items(): setattr(self, k, v)

class Club_name(Name):
  '''Describe club name when joined'''
  width=15
  label='Ομάδα'
  save_included=False
  unique=False
  not_null=False
  join_on='club_id=club.id'

  def __init__(self, **kw):
    Name.__init__(self, **kw)
    for k, v in kw.items(): setattr(self, k, v)

class Country_name(Name):
  '''Describe country name when joined'''
  width=15
  label='Χώρα'
  save_included=False
  unique=False
  not_null=False
  join_on='country_id=country.id'

  def __init__(self, **kw):
    Name.__init__(self, **kw)
    for k, v in kw.items(): setattr(self, k, v)

class Position_name(Name):
  '''Describe position name when joined'''
  width=15
  label='Θέση'
  save_included=False
  unique=False
  not_null=False
  join_on='position_id=position.id'

  def __init__(self, **kw):
    Name.__init__(self, **kw)
    for k, v in kw.items(): setattr(self, k, v)

class Birth(gcf.Field_int, gcf.Stack_values):
  '''Describe birth year'''
  length=4
  width=8
  label='Έτος γέννησης'

  def __init__(self, **kw):
    gcf.Field_int.__init__(self, **kw)
    gcf.Stack_values.__init__(self, stack=2, seperator='~')
    for k, v in kw.items(): setattr(self, k, v)

class Height(gcf.Field_float, gcf.Stack_values):
  '''Describe persons height'''
  length=4
  width=8
  label='Ύψος'

  def __init__(self, **kw):
    gcf.Field_float.__init__(self, **kw)
    gcf.Stack_values.__init__(self, stack=2, seperator='~')
    for k, v in kw.items(): setattr(self, k, v)

class Dorsal(gcf.Field):
  '''Describe dorsal number'''
  length=4
  width=8
  label='Φανέλα'

  def __init__(self, **kw):
    gcf.Field.__init__(self, **kw)
    for k, v in kw.items(): setattr(self, k, v)

class Player_count(gcf.Field_int, gcf.Stack_values):
  '''Count players'''
  length=4
  width=8
  label='Παίκτες'
  save_included=False
  edit_included=False
  join_on=None #id=player.club_id / .country_id / .position_id
  is_function='count(player.id)'

  def __init__(self, **kw):
    gcf.Field_int.__init__(self, **kw)
    gcf.Stack_values.__init__(self, stack=2, seperator='~')
    for k, v in kw.items(): setattr(self, k, v)

class Coach_count(gcf.Field_int, gcf.Stack_values):
  '''Count coaches'''
  length=4
  width=8
  label='Προπονητές'
  save_included=False
  edit_included=False
  join_on=None #id=player.club_id / .country_id / .position_id
  is_function='count(coach.id)'

  def __init__(self, **kw):
    gcf.Field_int.__init__(self, **kw)
    gcf.Stack_values.__init__(self, stack=2, seperator='~')
    for k, v in kw.items(): setattr(self, k, v)

class Player_avg_age(gcf.Field_int, gcf.Stack_values):
  '''Calculate players average height'''
  length=4
  width=8
  label='ΜΟ Ηλικίας'
  save_included=False
  edit_included=False
  join_on=None #'id=player.club_id / .country_id / .position_id
  is_function='cast(strftime("%Y", date("now")) as int)-cast(round(avg(player.birth),0) as int)'

  def __init__(self, **kw):
    gcf.Field_int.__init__(self, **kw)
    gcf.Stack_values.__init__(self, stack=2, seperator='~')
    for k, v in kw.items(): setattr(self, k, v)

class Player_avg_height(gcf.Field_float, gcf.Stack_values):
  '''Calculate players average height'''
  length=4
  width=8
  label='ΜΟ Ύψους'
  save_included=False
  edit_included=False
  join_on=None #'id=player.club_id / .country_id / .position_id
  is_function='avg(player.height)'

  def __init__(self, **kw):
    gcf.Field_float.__init__(self, **kw)
    gcf.Stack_values.__init__(self, stack=2, seperator='~')
    for k, v in kw.items(): setattr(self, k, v)

##############################################################################