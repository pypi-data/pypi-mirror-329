from flask import Blueprint, render_template
import sys
from singletons import UserSettings, Students, Sysls
from general import Mainroad, JINJAstuff

from studenten import (
	StudentJinja,
	Student,
	Note,
)
# =============== endpoints =====================
ep_home = Blueprint(
	'ep_home', __name__,
	url_prefix="/home",
	template_folder='templates',
    static_folder='static',
	static_url_path='static',
)

menuitem = 'home'

@ep_home.get('/')
def home():
	jus = UserSettings()

	if not jus._is():
		Mainroad.loglog('Iets mis met login')
		sys.exit(1)

	students_o = Students()
	sysls_o = Sysls()
	todos = list()
	mijn = list()
	dijn = list()

	studenten = students_o.get_students_mongo(where={"notes.todo": 1})
	groepen = sysls_o.get_sysl('s_group')
	for s in studenten:
		for n in s['notes']:
			Note.normalize(n)
			if n['to_alias'] == '':
				n['to_alias'] = n['alias']

			if n['to_alias'] in [jus.alias(), 'all']:
				# door andere aan mij gericht
				mijn.append(StudentJinja(s, Student.get_model()))
			else:
				dijn.append(StudentJinja(s, Student.get_model()))

	for k, v in groepen.items():
		groepen[k] = JINJAstuff(v, {})

	bericht = Mainroad.get_message(newline='<br>')
	if bericht == '':
		bericht = None

	return render_template(
		'home.html',
		menuitem='home',
		props=jus,
		mijn=mijn,
		dijn=dijn,
		groepen=groepen,
		bericht=bericht,
		logging=Mainroad.logging,
	)
