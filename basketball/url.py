### url.py ############################################################
'''Κώδικας για την επεξεργασία των url αιτημάτων'''

import re
import gc_url as gcu
import tables as ta

class Request(gcu.Request):
  '''Manage url requests'''

  def __init__(self, **kw):
    gcu.Request.__init__(self, **kw)
    self.output=lambda x: print(x)
    for k, v in kw.items(): setattr(self, k, v)

  def league_page(self, url):
    error_free, data=self.open(url)
    if not error_free:
      self.output(data)
    else:
      data=data.split('\r')
      is_data=0
      for li in data:
        li=li[1:]
        if is_data==0:
          if li=='<ul class="nav-teams nav-teams-16">':
            is_data=1
        elif is_data==1:
          if li=='    <li class="item">':
            is_data=2
          elif li=='</ul>':
            break
        elif is_data==2:
          _=re.findall('title="[\w ]+"', li.strip())
          if len(_)>0:
            club=ta.Club()
            club.field_by_name('name').value=_[0].split('"')[1]
            _=re.findall('href=\S+"', li.strip())
            club.field_by_name('_url').value=_[0].split('"')[1]
            self.output(club.name.value+'=>'+club._url.value)
          is_data=1
        
  def club_page(self, club_name, url):
    self.output(url)
    if 'http://' in url or 'www.' in url:
      error_free, data=self.open(url) 
    else:
      try: 
        data=open(url,'r',encoding='utf-8').read()
        error_free=True
      except:
        data='cannot read file '+url
        error_free=False

    if not error_free:
      self.output(data)
    else:
      if 'http://' in url or 'www.' in url: 
        data=data.split('\r\n') #from internet
      else:
        data=data.split('\n') #from local files
      is_data=''

      for li in data:
        li=li[1:]
        if is_data=='':
          if li=='   <div class="item player">':
            is_data='player'
            obj=ta.Player()
            obj.field_by_name('club_name').value=club_name
          elif li=='   <div class="item coach">':
            is_data='coach'
            obj=ta.Coach()
            obj.field_by_name('club_name').value=club_name
        else:
          if li=='   </div>':
            is_data=''
          elif is_data=='player':
            self.extract(li.strip(), obj, {
              'name':(r'a href=.+>(.*)</a>'),
              'birth':(r'"birth">(\d*)<'),
              'country_name':(r'"country">(.*)<'),
              'position_name':(r'"position">(.*)<'),
              'height':(r'Height:([0-9. ]*)<'),
              'dorsal':(r'"dorsal">([0-9#]*)<')})
          elif is_data=='coach':
            self.extract(li.strip(), obj, {
              'name':(r'a href=.+>(.*)</a>'),
              'birth':(r'"birth">(\d*)<'),
              'country_name':(r'"country">(.*)<')})

  def extract(self, from_str, to_obj, rules):
    for k, v in rules.items():
      _=re.findall(v, from_str)
      if len(_)!=0:
        to_obj.field_by_name(k).value=_[0]
        self.output(k+':'+_[0])
        break

  def normalise_data(self):
    #organise data in ram (objects)

    #extract clubs, countries and positions as unique values in temporary lists
    _clubs=[]
    _countries=[]
    _positions=[]
    for i, player in enumerate(ta.Player.all.objects):
      print('---')
      player.id.value=1+i
      if player.name.value=='':
        player.name.value=str(1+i)
      if player.club_name.value!='':
        try: _clubs.index(player.club_name.value)
        except: _clubs.append(player.club_name.value)
        player.club_id.value=_clubs.index(player.club_name.value)+1
      if player.country_name.value!='':
        try: _countries.index(player.country_name.value)
        except: _countries.append(player.country_name.value)
        player.country_id.value=_countries.index(player.country_name.value)+1
      if player.position_name.value!='':
        try: _positions.index(player.position_name.value)
        except: _positions.append(player.position_name.value)
        player.position_id.value=_positions.index(player.position_name.value)+1
      for k, v in player.__dict__.items():
        print(k, ':', v.value)

    for i, coach in enumerate(ta.Coach.all.objects):
      print('---')
      coach.id.value=1+i
      if coach.club_name.value!='':
        try: _clubs.index(coach.club_name.value)
        except: _clubs.append(coach.club_name.value)
        coach.club_id.value=_clubs.index(coach.club_name.value)+1
      if coach.country_name.value!='':
        try: _countries.index(coach.country_name.value)
        except: _countries.append(coach.country_name.value)
        coach.country_id.value=_countries.index(coach.country_name.value)+1
      for k, v in coach.__dict__.items():
        print(k, ':', v.value)

    #store temporary lists in objects
    ta.Club.all.remove_all()
    for i, x in enumerate(_clubs):
      _=ta.Club()
      _.id.value=i+1
      _.name.value=x
    for i, x in enumerate(_countries):
      _=ta.Country()
      _.id.value=i+1
      _.name.value=x
    for i, x in enumerate(_positions):
      _=ta.Position()
      _.id.value=i+1
      _.name.value=x

    #count players, coaches per club, country, position
    for club in ta.Club.all.objects:
      print('---')
      club.player_count.value=ta.Player.all.count({'club_id.value':club.id.value})
      club.coach_count.value=ta.Coach.all.count({'club_id.value':club.id.value})
      for k, v in club.__dict__.items():
        print(k, ':', v.value)

    for country in ta.Country.all.objects:
      print('---')
      country.player_count.value=ta.Player.all.count({'country_id.value':country.id.value})
      country.coach_count.value=ta.Coach.all.count({'country_id.value':country.id.value})
      for k, v in country.__dict__.items():
        print(k, ':', v.value)
      
    for position in ta.Position.all.objects:
      print('---')
      position.player_count.value=ta.Player.all.count({'position_id.value':position.id.value})
      for k, v in position.__dict__.items():
        print(k, ':', v.value)

##############################################################################