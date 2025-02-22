import os
import random
import string
from copy import deepcopy
import platform
import subprocess
from collections import OrderedDict

from general import (
	Casting,
	Timetools,
	ListDicts,
	Mongo,
	Mainroad,
)
class SyslsMeta(type):
	_instances = {}
	def __call__(cls, *args, **kwargs):
		if cls not in cls._instances:
			instance = super().__call__(*args, **kwargs)
			cls._instances[cls] = instance
		return cls._instances[cls]

	@classmethod
	def destroy(metacls, cls):
		if cls in metacls._instances:
			del metacls._instances[cls]
class Sysls(metaclass=SyslsMeta):
	_systempath = ''
	_sysls = [
		's_gender',

		's_origin',
		's_uni',
		's_program',

		's_year',
		's_term',
		's_lang',
		's_ec',
		's_course',
		's_stream',

		's_grading',
		's_group',
		's_status',
		's_circular',
	]
	_sysmem = dict()
	error_in_sysmem = False
	m = None

	def __init__(self):
		self.init_mongo()

	def init_mongo(self):
		self.m = Mongo(collection="sys")
		all = self.m.read(where={'sysl': {'$in': self._sysls}})
		self._sysmem = dict()

		for item in all:
			syslname = item["sysl"]
			id = item["id"]
			# add syslname to dict
			if not syslname in self._sysmem:
				self._sysmem[syslname] = dict()
			self._sysmem[syslname][id] = item
		for syslname in self._sysmem:
			self._sysmem[syslname] = self.sorteer_by_ordering(self._sysmem[syslname])
		self.make_stud_statussen()

	def refresh_groups(self, all: list):
		self._sysmem['s_group'] = OrderedDict()
		for item in all:
			if not item['sysl'] == 's_group':
				continue
			id = item['id']
			self._sysmem['s_group'][id] = item
		self._sysmem['s_group'] = self.sorteer_by_ordering(self._sysmem['s_group'])

	def is_valid(self):
		return not self.error_in_sysmem

	def sorteer_by_ordering(self, d: dict) -> OrderedDict:
		ll = list(d.values())
		ll = ListDicts.sortlistofdicts(ll, 'ordering')
		# back to id-based dict
		d = OrderedDict()
		for l in ll:
			d[l['id']] = l
		return d

	def nice_name(self, key: str):
		ss= self._sysls.copy()
		if not key in ss:
			return ''
		return key.replace('s_', '').capitalize()

	def get_lijsten_nicename(self) -> dict:
		eruit = dict()
		for sys in self._sysls.copy():
			eruit[sys] = self.nice_name(sys)
		return eruit

	def get(self):
		return deepcopy(self._sysmem)

	def get_sysl(self, syslname: str) -> OrderedDict|None:
		# gets dict with id:int as key
		try:
			return deepcopy(self._sysmem[syslname])
		except:
			return None

	def get_sysl_as_list(self, syslname: str) -> list|None:
		if not syslname in self._sysmem:
			return None
		sd = deepcopy(self._sysmem[syslname])
		return list(sd.values())

	def get_sysl_item(self, syslname: str, id: int) -> any:
		try:
			id = int(id)
			return self._sysmem[syslname][id]
		except:
			return None

	def get_sysl_item_first_active(self, syslname: str) -> dict|None:
		d = self.get_sysl(syslname)
		for item in d.values():
			if item['status'] == 1:
				return item
		return None

	def set_sysl_item(self, syslname: str, id, value) -> bool:
		try:
			self._sysmem[syslname][id] = value
			return self.upsert_sysl_mongo(where={'sysl': syslname, 'id': id}, d=value)
		except:
			return False

	def del_sysl_item(self, syslname: str, id: int) -> bool:
		try:
			del(self._sysmem[syslname][id])
			return self.del_sysl_mongo(where={'sysl': syslname, 'id': id})
		except:
			return False
		# return self.save_sysl(syslname)

	def del_sysl_mongo(self, where: dict) -> bool:
		self.m.set_collection('sys')
		return self.m.delete_single(filter=where)

	def upsert_sysl_mongo(self, where: dict, d: dict) -> bool:
		# only complete sysl item
		self.m.set_collection('sys')
		return self.m.update_one(
			where=where,
			what={'$set': d},
			upsert=True,
			onerror=False,
		) is not False

	def store_sysl_mongo(self, where: dict, what: dict) -> bool:
		self.m.set_collection('sys')
		return self.m.update_one(
			where=where,
			what=what,
			upsert=False,
			onerror=False,
		) is not False

	def make_sysl(self, syslname: str, d, other=False) -> bool:
		if not other and syslname not in self._sysls:
			return False
		self.m.set_collection('sys')
		r = self.m.update_one(
			where={'name': syslname},
			what={'$set': {'d': d}},
			onerror=None,
		)
		self.init_mongo()
		return not r is None

	def get_model(self, welk: str="") -> dict:
		model = dict(
			id = {'default': 0},
			name = {'default': ''},
			color = {'default': ''},
			extra = {'default': ''},
			status = {'default': 'actief'},
			ordering = {'default': 0},
		)
		if welk in ['s_group',]:
			model['notes'] = {'default': list()}
		return model

	def get_fields(self) -> list:
		return list(self.get_model().keys())

	def get_empty(self) -> dict:
		m = self.get_model()
		d = dict()
		for field, val in m.items():
			d[field] = val['default']
		return d

	def make_stud_statussen(self):
		# makes a list like:
		default = dict(
			registratie=[0, 10, 11, 12],
			studenten=[20],
			beoordelen=[21],
			resit=[22],
			alumni=[39],
			niet=[31, 38],
			noshow=[14, 16, 18, 30],
			alle=list(range(0, 100)),
		)
		ss = self.get_sysl('s_status')
		statussen = dict(alle=list())
		for item in ss.values():
			statussen['alle'].append(item['id'])
			if item['extra'] == '' or item['extra'] == None:
				continue
			if not item['extra'] in statussen:
				statussen[item['extra']] = list()
			statussen[item['extra']].append(item['id'])
		self.stud_statussen = statussen

	def get_stud_statussen(self):
		return self.stud_statussen

class EmailsMeta(type):
	_instances = {}
	def __call__(cls, *args, **kwargs):
		if cls not in cls._instances:
			instance = super().__call__(*args, **kwargs)
			cls._instances[cls] = instance
		return cls._instances[cls]

	@classmethod
	def destroy(metacls, cls):
		if cls in metacls._instances:
			del metacls._instances[cls]
class Emails: # (metaclass=EmailsMeta)
	_emailspath = ''
	_sysmem = dict()

	def __init__(self):
		self.init_mongo()

	def init_mongo(self):
		self.m = Mongo(collection='sys')
		self._sysmem = dict()
		all = self.m.read(where={'sysl': 'emails'})
		for item in all:
			naam = Casting.name_safe(item['name'], True)
			self._sysmem[naam] = item

	def upsert_email_mongo(self, d: dict) -> bool:
		self.m.set_collection('sys')
		naam = Casting.name_safe(d['name'], True)
		where = {'name': naam, 'sysl': 'emails'}
		return self.m.update_one(where, {'$set': d}, upsert=True, onerror=False) is not False

	def get_single(self, naam: str) -> dict|None:
		try:
			return deepcopy(self._sysmem[naam])
		except:
			return None

	def get(self):
		return deepcopy(self._sysmem)

class ViewsMeta(type):
	_instances = {}

	def __call__(cls, *args, **kwargs):
		if cls not in cls._instances:
			instance = super().__call__(*args, **kwargs)
			cls._instances[cls] = instance
		return cls._instances[cls]

	@classmethod
	def destroy(metacls, cls):
		if cls in metacls._instances:
			del metacls._instances[cls]
class Views: # (metaclass=ViewsMeta)
	_viewspath = ''
	_defaultkey = 1723028433
	_defaultname = 'default'
	_sysmem = OrderedDict()
	m = None

	def __init__(self, slim=False):
		# also manipulates and refreshes groups
		self.init_mongo(slim=slim)

	def init_mongo(self, slim=True):
		self.m = Mongo(collection='sys')
		if slim:
			all = self.m.read(where={'sysl': {'$in': ['views', 's_group']}, 'status': 1}, onerror=list())
		else:
			all = self.m.read(where={'sysl': {'$in': ['views', 's_group']}}, onerror=list())
		self._sysmem = OrderedDict()
		for item in all:
			id = item['id']
			if item['sysl'] == 'views':
				self._sysmem[id] = item
		sysls_o = Sysls()
		sysls_o.refresh_groups(all)

	def empty_view(self):
		jus = UserSettings()
		d = dict(
			sysl='views',
			name=self._defaultname,
			created_ts=Timetools.now_secs(),
			alias=jus.alias(),
			color='#ffffff',
			status=1,
			fields=['id', 'assessment', 'firstname', 'lastname'],
			groups=[],
			emailbuttons=[],
		)
		d['id'] = d['created_ts']
		return d

	def void_normalize(self, view):
		empty = self.empty_view()
		nview = deepcopy(view)
		for key in empty:
			if not key in view:
				view[key] = empty[key]
		try:
			del(view['_id'])
		except:
			pass

	def get_defaultkey(self) -> int:
		return self._defaultkey

	def get_defaultname(self) -> str:
		return self._defaultname

	def create_view_mongo(self, d: dict) -> bool:
		self.void_normalize(d)
		self.m = Mongo(collection='sys')
		return self.m.create(d, onerror=False) is not False

	def update_view_mongo(self, id, d: dict) -> bool:
		self.void_normalize(d)
		where = {'sysl': 'views', 'id': id}
		what = {'$set': d}
		if not self.m.update_one(where=where, what=what, upsert=False, onerror=False):
			return False
		return True

	def delete_view_mongo(self, id) -> bool:
		where = {'sysl': 'views', 'id': id}
		return self.m.delete_single(where, onerror=False) is not False

	def get(self) -> OrderedDict:
		d = deepcopy(self._sysmem)
		return self.sorteer_by_created(d)

	def sorteer_by_created(self, d: dict) -> OrderedDict:
		ll = list(d.values())
		ll = ListDicts.sortlistofdicts(ll, 'created_ts', reverse=True)
		# back to id-based dict
		d = OrderedDict()
		for l in ll:
			d[l['id']] = l
		return d

	def get_single_by_key(self, key) -> dict|None:
		try:
			return deepcopy(self._sysmem[key])
		except:
			return None

	def get_by_similar_viewname(self, groupid: int, viewid: int) -> int:
		def firstpart(viewname: str) -> str:
			viewname = viewname.replace('-', ' ').replace('_', ' ')
			return viewname.split(' ')[0].strip()

		if not viewid in self._sysmem:
			return 0
		simname = firstpart(self._sysmem[viewid]['name'])
		for k, v in self._sysmem.items():
			if not groupid in self._sysmem[k]['groups']:
				continue
			fp = firstpart(v['name'])
			if simname == fp:
				return k
		return 0

	def is_group_in_view(self, groupid: int, viewid: int) -> bool:
		if viewid == 1:
			return True
		if not viewid in self._sysmem:
			return False
		return groupid in self._sysmem[viewid]['groups']

	def is_view_active(self, viewid: int) -> bool:
		if viewid == 1:
			return True
		if not viewid in self._sysmem:
			return False
		return self._sysmem[viewid]['status'] == 1

	def get_views_by_groupid(self, groupid: int, activeonly=False) -> OrderedDict:
		g_views = OrderedDict()
		for key in self._sysmem:
			if activeonly and not self.is_view_active(key):
				continue
			if self.is_group_in_view(groupid, key):
				g_views[key] = deepcopy(self._sysmem[key])
		return g_views

	def reorder_views(self, idslist: list) -> bool:
		for id in idslist:
			if not id in self._sysmem:
				continue
			self._sysmem.move_to_end(id, last=True)
		return True

	def mijn_views(self) -> list:
		jus = UserSettings()
		all = self._sysmem
		mijnviews = list()
		for key, val in all.items():
			if jus.alias() == val['alias']:
				mijnviews.append(key)
		return mijnviews

	def active_views(self, no_default=True) -> list:
		all = self._sysmem
		active = list()
		for key, val in all.items():
			if no_default and key == self.get_defaultkey():
				continue
			if self.is_view_active(key):
				active.append(val)
		return active

	def summative_views(self) -> dict:
		# returns list with active summative views
		all = self._sysmem
		active = dict()
		for key, val in all.items():
			if not self.is_view_active(key):
				continue
			if val['alias'] != "summative":
				continue
			active[key] = val
		return active

	def mijn_groepen(self) -> list:
		# groepen waarbij ik een view heb
		jus = UserSettings()
		# alle views
		all = self._sysmem
		mijngroepen = list()
		for key, val in all.items():
			if (jus.alias() == val['alias'] or val['alias'] == 'summative') and val['status'] > 0:
				for g in val['groups']:
					if not g in mijngroepen:
						mijngroepen.append(g)

		return mijngroepen

class StudentsMeta(type):
	_instances = {}
	def __call__(cls, *args, **kwargs):
		if cls not in cls._instances:
			instance = super().__call__(*args, **kwargs)
			cls._instances[cls] = instance
		return cls._instances[cls]

	@classmethod
	def destroy(metacls, cls):
		if cls in metacls._instances:
			del metacls._instances[cls]
class Students: #(metaclass=StudentsMeta):
	_stud_p_path = ''
	_stud_dir_path = ''
	_sysmem = dict()
	m = None

	def __init__(self):
		self._stud_dir_path = Mainroad.get_student_dirs_path()
		self.init_mongo()

	def init_mongo(self):
		self.m = Mongo(collection='students')


	def get_stud_dir_path(self):
		return self._stud_dir_path

	@classmethod
	def get_empty(cls):
		return dict(
			# about the student - per enrollment. So enroll twice, twice in database
			id={'default': 0},
			firstname={'default': ''},
			lastname={'default': ''},
			s_gender={'default': 0, 'from': 's_gender'},
			email={'default': ''},
			created_ts={'default': 0},
			pf_url={'default': ''},
			kom_code={'default': ''},  # student code for KOM students (other school)
			nhls_code={'default': 0},  # student code at nhlstenden also for KOM
			password={'default': ''},
			grade={'default': 0},
			grade_ts={'default': 0},
			assessment={'default': 0},

			s_group={'default': 0, 'from': 's_group'},
			s_status={'default': 0, 'from': 's_status'},

			# about the students current situation
			s_origin={'default': 0, 'from': 's_origin'},
			s_uni={'default': 0, 'from': 's_uni'},
			s_program={'default': 0, 'from': 's_program'},

			# about the students minor course
			s_year={'default': 0, 'from': 's_year'},
			s_term={'default': 0, 'from': 's_term'},
			s_lang={'default': 0, 'from': 's_lang'},
			s_ec={'default': 0, 'from': 's_ec'},
			s_course={'default': 0, 'from': 's_course'},
			s_stream={'default': 0, 'from': 's_stream'},
			# see also
			samestudent={'default': []},  # llist with ids of same student

			# list of notes models
			notes={'default': [], 'model': 'm_note'},

			# list of soc's on this student
			circulars={'default': {}, 'model': 'm_setofcirculars'},

			# list of custom text fields
			customs={'default': {}, 'model': 'm_custom'},
			alias={'default': ''},
			todo={'default': 0},
		)

	@classmethod
	def get_nicenames(cls):
		return dict(
			s_group='group',
			s_status='status',
			s_year='year',
			s_term='period',
			s_ec='ecs',
			s_lang='lang',
			s_course='minor',
			s_stream='stream',
			s_origin='origin',
			s_uni='institute',
			s_program='program',
			created_ts='created',
			grade_ts='dd',
			s_gender='mfo',
			assessment='ass',
		)

	def project(self, skip=[]):
		# projectie voor studenten menu
		p = dict()
		for k in self.get_empty().keys():
			if k in skip:
				continue
			p[k] = 1
		return p

	def zoek_studenten_mongo(self, zoektermen: str) -> list:
		self.m.set_collection('students')
		zoektermen = zoektermen.split(' ')
		orlist = list()
		needles = list()
		for needle in zoektermen:
			needle = needle.strip()
			if needle == '':
				continue
			needle = f"{needle}"
			needles.append(needle)
		if len(needles) == 0:
			return list()

		for needle in needles:
			for field in ['firstname', 'lastname', 'email']:
				orlist.append({field: {'$regex': needle, '$options': 'i'}})

		match = {'$match': {'$or': orlist}}
		sort = {'$sort': {'firstname': 1}}
		project = {'$project': self.project(skip = ['notes', 'circulars', 'customs', 'alias'])}
		res = self.m.aggregate([match, sort, project], onerror=list())
		return res

	def agg_students_mongo(self, match: dict, skip=[]) -> list:
		andlist = list()
		for k, v in match.items():
			andlist.append({k: v})
		match = {'$match': {'$and': andlist}}
		pr = self.project(skip=skip)
		pr['notestodo'] = {'$sum': '$notes.todo'}
		project = {'$project': pr}
		res = self.m.aggregate([match, project], onerror=list())
		return res

	def get_students_mongo(self, where={}, skip=[]):
		self.m.set_collection('students')
		select = self.project(skip=skip)
		res = self.m.read(where=where, select=select, onerror=list())
		return res

	@classmethod
	def active_set(cls):
		return [0, 10, 11, 12, 20, 21, 22, 23]

	def get_by_id_mongo(self, id: int, skip=[]) -> dict|None:
		self.m.set_collection('students')
		where = {'id': id}
		select = self.project(skip=skip)
		return self.m.read_one(where=where, select=select, onerror=None)

	@classmethod
	def generate_safename_full_from_d(cls, d: dict) -> str:
		first = Casting.name_safe(d['firstname'], False)
		last = Casting.name_safe(d['lastname'], False)
		return f"{first}-{last}-{d['id']}"

	@classmethod
	def cleanup_before_save(cls, d: dict) -> dict:
		if 'pf_url' in d:
			cont = True
			if d['pf_url'] is None:
				d['pf_url'] = ''
				# klaar
				cont = False
			if d['pf_url'] == '':
				# klaar
				cont = False

			head, sep, tail = d['pf_url'].partition('/edit')
			if cont and sep == '/edit':
				d['pf_url'] = head
				cont = False

			head, sep, tail = d['pf_url'].partition('?usp')
			if cont and sep == '?usp':
				d['pf_url'] = head
				cont = False

		# other fields
		return d

	def update_student_mongo(self, where, what):
		self.m.set_collection('students')
		return self.m.update_one(where=where, what=what, upsert=False, onerror=0)

	def create_student_mongo(self, d: dict) -> bool:
		self.m.set_collection('students')
		r = self.m.create(d, onerror=None)
		return not r is None

	def delete_student_mongo(self, where) -> bool:
		self.m.set_collection('students')
		return self.m.delete_single(where, onerror=False) != False

	def make_student_folder_path(self, id):
		d = self.get_by_id_mongo(id)
		if d is None:
			return None
		return self.make_student_folder_path_from_d(d)

	def get_term(self, key: int) -> str:
		sysls_o = Sysls()
		return sysls_o.get_sysl_item('s_term', key)['name']

	def get_year(self, key: int) -> str:
		sysls_o = Sysls()
		return sysls_o.get_sysl_item('s_year', key)['name']

	def make_student_folder_path_from_d(self, d):
		sysls_o = Sysls()
		if d['s_year'] < 2020:
			# print('WRONG YEAR', d['s_year'])
			return None
		if not d['s_term'] in [1, 2, 3, 4, 5, 6]:
			print('WRONG TERM', d['s_term'])
			return None
		jaar = sysls_o.get_sysl_item('s_year', d['s_year'])['name']
		term = self.get_term(d['s_term'])
		safename = self.generate_safename_full_from_d(d)
		studpath = os.path.join(self._stud_dir_path, jaar, term, safename)
		return studpath


	@classmethod
	def new_password(cls, id):
		x = ''.join(random.choices(string.ascii_lowercase+string.digits+'', k=13))
		return f"{id*13}-{x}"

	def new_student_id_mongo(self) -> int|None:
		agg = { '$group' : { '_id': 0, 'id': { '$max' : "$id" }}}
		self.m.set_collection('students')
		res = self.m.aggregate([agg], onerror=None)
		try:
			return res[0]['id'] + 1
		except Exception as e:
			print(e)
			return None

	def open_student_dir(self, id):
		pad = self.make_student_folder_path(id)
		if pad is None:
			return
		try:
			if platform.system() == "Windows":
				os.startfile(pad)
			elif platform.system() == "Darwin":
				subprocess.Popen(["open", pad])
			else:
				subprocess.Popen(["xdg-open", pad])
		except Exception as e:
			pass

	def as_html(self, id: int, d: dict|None, views: Views) -> bool:
		sysls_o = Sysls()
		if d is None:
			self.m.set_collection('students')
			d = self.get_by_id_mongo(id)
		else:
			pass
		if not isinstance(d, dict):
			print('NO STUDENT DICT', d)
			return False

		studfields = list(d.keys())
		# get circular model from system
		circfields = sysls_o.get_sysl('s_circular')

		def view_get(viewid) -> dict|None:
			try:
				viewid = int(viewid)
				return views.get_single_by_key(viewid)
			except:
				return None

		def view_is_summa(viewid) -> bool:
			v = view_get(viewid)
			if v is None:
				return False
			return v['alias'] == 'summative'

		def view_get_name(viewid) -> str|None:
			v = view_get(viewid)
			if v is None:
				return ''
			return v['name']

		def view_val_from_student(view: dict):
			# maakt een list [key, val] van de view
			vl = dict() # want op volgorde
			for fieldname in view['fields']:
				if not fieldname.startswith(('c_', 't_')):
					continue
				# name of field
				# value in student dict
				if fieldname.startswith('t_'):
					try:
						val = d['customs'][str(view['id'])][fieldname]
					except:
						val = ''
				else:
					try:
						val = d['circulars'][str(view['id'])][fieldname]
					except:
						val = 0
				vl[fieldname] = val
			return vl

		def ccolor(val: int):
			try:
				return circfields[val]['color']
			except:
				return '#eeeeee'

		def make_li(htm, label: str, waarde: str, direct=False):
			try:
				if direct:
					waarde = waarde
				else:
					waarde = d[waarde]
			except:
				waarde = ''
			return f"{htm}\n\t\t\t<li><span>{label}</span>{waarde}</li>"

		def from_list(thing):
			try:
				return sysls_o.get_sysl_item(thing, d[thing])['name']
			except:
				return ''

		def make_note(htm, note):
			try:
				notitie = note['note']
				alias = note['alias']
				if 'to_alias' in note:
					to_alias = note['to_alias']
				else:
					to_alias = 'self'
				dd = Timetools.ts_2_td(note['created_ts'], rev=True)
				return f"{htm}\n\t\t\t<p><span>{alias} for {to_alias} op {dd}</span><br>{notitie}</p>"
			except:
				return f"{htm}\n\t\t\t<p><span></span></p>"

		def make_html_view(html, cv: dict):
			# creates one line for one circular
			html = f'{html}\n\t\t\t<table class="circular">'
			html = f'{html}\n\t\t\t\t<thead><tr>'
			for field in cv['fields']:
				if not field.startswith(('c_', 't_')):
					continue
				fieldname = field[2:] # remove c_ or t_
				html = f'{html}\n\t\t\t\t\t<td>{fieldname}</td>'
			html = f'{html}\n\t\t\t\t</tr></thead>'

			html = f'{html}\n\t\t\t\t<tbody><tr>'
			for field in cv['fields']:
				if not field.startswith(('c_', 't_')):
					continue
				if field.startswith('c_'):
					# kleurveld
					try:
						kleur = ccolor(cv['student'][field])
					except:
						kleur = '#eeeeee'
					html = f'{html}\n\t\t\t\t\t<td style="background-color: {kleur}"></td>'
				else:
					# text field
					try:
						val = cv['student'][field]
					except:
						val = ''
					html = f'{html}\n\t\t\t\t\t<td>{val}</td>'

			html = f'{html}\n\t\t\t\t</tr></tbody>'
			html = f'{html}\n\t\t\t</table>'
			return html

		def combine_view_student():
			# combines view names and student values
			allviewids = views.get().copy()

			# filter only view ids that are in student also
			viewids = list()
			for ss in d['circulars'].keys():
				ss = Casting.int_(ss, default=-1)
				if ss in allviewids:
					if not ss in viewids:
						viewids.append(int(ss))
			for ss in d['customs'].keys():
				ss = Casting.int_(ss, default=-1)
				if ss in allviewids:
					if not ss in viewids:
						viewids.append(int(ss))

			# make complete list
			cviews = list()
			for viewid in viewids:
				view = view_get(viewid)
				if view is None:
					continue
				view['student'] = view_val_from_student(view)
				cviews.append(view)
			return cviews


		# ======= main van de html def =======
		if d is None:
			return
		if d['s_status'] in [39]:  # passed
			kleur = 'dodgerblue'
		elif d['s_status'] in [10, 11, 12]:  # ingeschreven
			kleur = 'rgb(254, 232, 86)'  # geel
		elif d['s_status'] in [20, 21, 22]:  # bezig
			kleur = 'darkgreen'
		elif d['s_status'] in [30, 31, 38]:  # gezakt oid
			kleur = 'rgb(221, 53, 110)'  # signaal
		else:
			kleur = "#eee"

		html = self.basic_student_html() % (d['firstname'], d['lastname'], kleur, kleur, id, d['firstname'], d['lastname'])

		html = f'{html}<ul>\n\t\t'
		# velden
		html = make_li(html, 'Voornaam', 'firstname')
		html = make_li(html, 'Achternaam', 'lastname')
		html = make_li(html, 'Groep', from_list('s_group'), direct=True)
		html = make_li(html, 'Email', 'email')
		html = make_li(html, 'MVO', from_list('s_gender'), direct=True)

		try:
			url = d["pf_url"]
			link = f'<a href="{url}">{url}</a>'
		except:
			url = ''
			link = ''
		html = make_li(html, 'portfolio', link, direct=True)

		html = make_li(html, 'Wachtwoord', 'password')
		html = make_li(html, 'Cijfer', 'grade')

		if d['grade'] < 1:
			datum = ''
		else:
			try:
				datum = Timetools.ts_2_td(d['grade_ts'], rev=True)
			except:
				datum = ''
		html = make_li(html, 'Cijferdatum', datum, direct=True)

		html = make_li(html, 'Status', from_list('s_status'), direct=True)
		html = make_li(html, 'Herkomst', from_list('s_origin'), direct=True)
		html = make_li(html, 'Uni', from_list('s_uni'), direct=True)
		html = make_li(html, 'Programma', from_list('s_program'), direct=True)
		html = make_li(html, 'Jaar', from_list('s_year'), direct=True)
		html = make_li(html, 'Periode', from_list('s_term'), direct=True)
		html = make_li(html, 'Minor', from_list('s_course'), direct=True)
		html = make_li(html, 'ECs', from_list('s_ec'), direct=True)
		html = make_li(html, 'Taal', from_list('s_lang'), direct=True)

		html = make_li(html, 'KOM-code', 'kom_code')
		html = make_li(html, 'NHLS-code', 'nhls_code')

		html = f'{html}\n\t\t</ul>\n\t\t'

		# nu per view een kader
		cviews = combine_view_student()
		# summative first
		for cv in cviews:
			if not cv['alias'] == 'summative':
				continue
			html = f'{html}<h2>SUMMATIVE: {cv["name"]}</h2>\n\t\t<div class="circulars">'
			html = make_html_view(html, cv)
			html = f'{html}</div>\n\t\t'
		# andere views
		for cv in cviews:
			if cv['alias'] == 'summative':
				continue
			html = f'{html}<h2>View: {cv["name"]}</h2>\n\t\t<div class="circulars">'
			html = make_html_view(html, cv)
			html = f'{html}</div>\n\t\t'

		html = f'{html}<h2>Notities</h2>\n\t\t<div class="notes">'
		if 'notes' in d:
			for note in d['notes']:
				html = make_note(html, note)
		html = f'{html}\n\t\t</div>\n\t\t'

		html = f'{html}</body>\n</html>'
		filename = self.generate_safename_full_from_d(d) + '.html'
		dirpath = self.make_student_folder_path_from_d(d)
		filepath = os.path.join(dirpath, filename)
		try:
			with open(filepath, 'w') as f:
				f.write(html)
			return True
		except:
			print(f'Fout in naam: {dirpath}')
			return False

	def basic_student_html(self):
		return '''<!DOCTYPE html>
	<html lang="en">
		<head>
			<title>%s %s</title>
			<style>
				*{
					font-family: Arial, Helvetica, sans-serif;
					font-size: 14px;
					border-radius: 3px;
				}
				body{
					padding: 1em;
				}
				ul{
					list-style: inside;
	                list-style-type: none;
	                margin: 0;
	                border: 2px solid %s;
					padding: 1em;
	            }
	            li{
	                margin: 0 0 0.5em 0;
	                padding: 0;
	                border-bottom: 1px solid #ddd;
	            }
	            li span{
	                display: inline-block;
	                width: 10em;
	                font-size: 0.8em;
	            }
	            div.notes,
	            div.circulars,
	            div.customs{
	                margin: 1em 0 0 0;
	                border: 2px solid %s;
					padding: 1em;
	            }
	            p span{
	                border-bottom: 1px solid #ddd;
	                font-size: 0.8em;
	            }
	            .circular{
	                overflow: hidden;
					white-space: nowrap;
	            }
	            .circular td,
	            .circular th{
	                font-size: 0.8em;
	                padding: 0.25em 0.5em;
	            }
	
			</style>
		</head>
		<body>
			<h1>%s %s %s</h1>
	'''

	def maak_html_tabelletje(self, d: dict) -> str:
		kleuren = ['zilver', 'groen', 'oranje', 'rood', 'blauw', 'grijs', 'wit']
		tabel = f'<table><thead><tr><td>{d["name"]}</td><td>&nbsp;</td>'
		# itereer kopjes
		for inh in d['fields']:
			tabel = f'{tabel}<td class="paars">{inh}</td>'

		# make assessment field if required
		if d['ass'] > 0:
			tabel += f'<td class="paars">oral assessment</td>'

		# add grade field and close row
		tabel = f'{tabel}<td class="paars">grade</td></tr></thead>'

		# row with first attempts
		tabel = f'{tabel}<tbody><tr><td>{d["course"]}</td><td class="paars">first</td>'

		resit = list()
		failed = False
		needsresit = False
		# itereer summatieve items
		for i in range(len(d['fieldvals'])):
			# logica...
			inh = d['fieldvals'][i]
			if inh == 1:  # gehaald
				resit.append(5)  # niet nodig
				kleur = kleuren[1]
			elif inh == 2:
				resit.append(4)  # blauw
				kleur = kleuren[2]
				needsresit = True
			elif inh == 3:  # def gezakt
				resit.append(3)  # resit rij op rood
				failed = True
				kleur = kleuren[3]
				# IN DIT GEVAL kunnen alle andere vakken in resit donkergrijs worden en het eindresultaat op rood
				# ook oral is dan niet meer nodig
			else:
				resit.append(0)
				kleur = kleuren[0]
			tabel = f'{tabel}<td class="first {kleur}">&nbsp;</td>'

		if failed:
			# if one part failed, no more resits for other parts
			needsresit = False

		# fill assessment field
		if d['ass'] > 0:
			if failed:
				# failed so not nec.
				kleur = kleuren[5]
				tabel = f'{tabel}<td class="{kleur}">&nbsp;</td>'
			elif needsresit:
				# color in resit row, so silver here
				kleur = kleuren[5]
				tabel = f'{tabel}<td class="resit {kleur}">&nbsp;</td>'
			else:
				kleur = kleuren[4]
				tabel = f'{tabel}<td class="first {kleur}">&nbsp;</td>'

		# grade field IN ROWSPAN, so only once
		if d['grade'] > 0:
			grade = str(d['grade'])
		else:
			grade = '&nbsp;'
		if failed:
			kleur = kleuren[3]
		elif d['grade'] >= 6:
			kleur = kleuren[1]
		elif d['grade'] > 1:
			kleur = kleuren[2]
		else:
			kleur = kleuren[0]
		if len(resit) > 0:
			tabel = f'{tabel}<td rowspan="2" class="{kleur}" style="text-align: center;">{grade}</td>'
		else:
			tabel = f'{tabel}<td>{grade}</td>'

		# close row
		tabel = f'{tabel}</tr>'

		# open new row if resit
		if needsresit:
			tabel = f'{tabel}<tr><td style="text-align: center;">&nbsp;</td><td class="paars">resit</td>'

			# itereer resit
			for inh in resit:
				kleur = kleuren[inh]
				tabel = f'{tabel}<td class="resit {kleur}">&nbsp;</td>'

			if d['ass'] > 0:
				kleur = kleuren[4]
				tabel = f'{tabel}<td class="first {kleur}">&nbsp;</td>'

		tabel = tabel + f'</tr></tbody></table>'
		return tabel

class UserSetingsMeta(type):
	_instances = {}
	def __call__(cls, *args, **kwargs):
		if cls not in cls._instances:
			instance = super().__call__(*args, **kwargs)
			cls._instances[cls] = instance
		return cls._instances[cls]

	@classmethod
	def destroy(metacls, cls):
		if cls in metacls._instances:
			del metacls._instances[cls]
class UserSettings(metaclass=UserSetingsMeta):
	_props = dict()
	_all_users = list()
	m = None
	# ROLLEN 'beheer', 'docent', 'administratie', 'admin'

	# sysls leeft in app, leest/schrijft niet zelf props
	# mainroad leeft in monze, leest schrijft settings
	# props in sysl == settings in mainroad.
	def __init__(self):
		self.read_props()
		self._all_users = self.get_users_mongo()

	def read_props(self):
		self._props = Mainroad.get_settings()

	def get_users_mongo(self) -> list:
		self.m = Mongo(collection='sys')
		where = {'sysl': 'users'}
		return self.m.read(where, onerror=[])

	def get_user_aliasses(self, ikook: bool=True) -> list:
		aliasses = list()
		for u in self._all_users:
			if not ikook:
				if u['alias'].strip() == self.alias().strip():
					continue
			aliasses.append(u['alias'])
		return aliasses

	def version(self):
		return Mainroad.get_version()

	def _is(self) -> bool:
		# check if this user has user settings
		try:
			if not 'alias' in self._props or not 'magda' in self._props:
				self.logoff()
				return False
			# known user with settings and login in own computer
			return True
		except:
			self.logoff()
			return False

	def is_new(self):
		return self.get_prop("isnew", default=True)

	def alias(self):
		return self.get_prop("alias", default="stranger")

	def _alias(self):
		return self.alias()

	def odpad(self):
		return self.get_prop("onedrive", default=None)

	def settingspad(self):
		return Mainroad.get_settings_path()

	def magda(self, rol: list, alias: str = None) -> bool:
		# alias is de alias van het ding
		rollen = self.get_prop("magda", default=[])
		if 'admin' in rollen:
			return True
		damag = len(list(set(rol) & set(rollen))) > 0
		if not alias is None:
			damag = damag and alias.strip() == self.alias()

		return damag

	def get_props(self):
		return self._props

	def get_prop(self, key: str, default=None):
		try:
			return self._props[key]
		except:
			return default

	def _prev(self) -> str:
		try:
			return self.get_prop('prev_url', default='')
		except:
			return ''

	def get_searchterms(self) -> list:
		try:
			return self.get_prop('searchterms', default=[])
		except:
			return []

	def get_sort(self, path) -> list|None:
		sorting = self.get_prop('sorting', default={})
		# return is list = [path, fieldname, asc/desc]
		try:
			return sorting[path]
		except:
			return []

	def set_prop(self, key: str, val):
		self._props[key] = val  # update or create
		Mainroad.set_settings(self._props)
		self.read_props()

	def set_searchterm(self, st: str) -> list:
		current = self.get_searchterms()
		if st in current:
			return current
		current.insert(0, st)
		current = current[:10]
		self.set_prop('searchterms', current)
		return current

	def set_sort(self, path, field, direction):
		# sets sorting for specific path
		# as list with two values: fieldname and direction asc, desc
		sorting = self.get_prop('sorting', default={})
		if not isinstance(sorting, dict):
			sorting = dict()
		sorting[path] = [path, field, direction]
		self.set_prop('sorting', sorting)

