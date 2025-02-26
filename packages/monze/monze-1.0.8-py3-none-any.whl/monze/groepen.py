# groepen
from flask import redirect, request, Blueprint, render_template
from general import Casting, Timetools, ListDicts, JINJAstuff
from singletons import UserSettings, Sysls, Students, Views

from studenten import (
	Student,
	Note,
	StudentJinja,
	filter_stuff,
	get_student_filter,
	get_active_statusses,
)

# =============== ENDPOINTS =====================
ep_groepen = Blueprint(
	'ep_groepen', __name__,
	url_prefix="/groepen",
	template_folder='templates',
    static_folder='static',
	static_url_path='static',
)

menuitem = 'groups'

@ep_groepen.get('/<int:groepnr>/<int:viewid>')
@ep_groepen.get('/<int:groepnr>')
def studenten_groep(groepnr=0, viewid=0):
	jus = UserSettings()
	sta, fil, act = filter_stuff()
	filter = ''

	sysls_o = Sysls()
	# views always renews on call, also renews groups in Sysl object
	views_o = Views(slim=True)
	mijngroepen = views_o.mijn_groepen()

	all = sysls_o.get_sysl('s_group')
	allegroepen = ListDicts.sortlistofdicts(list(all.values()), 'ordering')

	dezegroep = None
	groepen = list()
	for g in allegroepen:
		if g['id'] == groepnr:
			dezegroep = g
		groepen.append(g)
	if dezegroep is None:
		return redirect(f'/groepen')

	# views
	allfieldnames = list(Students.get_empty().keys())
	groupviews = views_o.get_views_by_groupid(groepnr, activeonly=True)
	selectprimary = False

	# get view if current or previous
	previous_viewid = 0
	if viewid == 0:
		viewid = previous_viewid = jus.get_prop('viewid', default=0)
		view = views_o.get_single_by_key(viewid)
	else:
		view = views_o.get_single_by_key(viewid)

	# check if groep in view, gives False if viewid == 0
	if not views_o.is_group_in_view(groepnr, viewid):
		selectprimary = True
		viewid = 0
		view = None

	# if not preselected viewid yet
	if selectprimary:
		# first look for similar view
		if previous_viewid != 0:
			viewid = views_o.get_by_similar_viewname(groepnr, previous_viewid)
			if viewid > 0:
				# if found, redirect
				return redirect(f'/groepen/{groepnr}/{viewid}')

	# if not preselected viewid,
	if selectprimary:
		# redirect to first active or all
		for k, v in groupviews.items():
			if v['status'] == 1:
				return redirect(f'/groepen/{groepnr}/{k}')
		return redirect(f'/groepen/{groepnr}/1')

	# get the view, if 1
	if view is None:
		# make view empty with all fields
		view = views_o.empty_view()
		view['fields'] = allfieldnames
	view['fields'].append('id')
	jus.set_prop('viewid', viewid)
	# normalize view
	views_o.void_normalize(view)

	# jinjafy
	for key in list(groupviews.keys()):
		# del default view, not to be shown or used
		if key == views_o.get_defaultkey():
			del (groupviews[key])
			continue
		groupviews[key] = JINJAstuff(groupviews[key], {})

	# make field list and ignore field list
	fixedfields = ['id', 'assessment', 'firstname', 'lastname']

	if viewid > 1:
		skip = []
		for fname in allfieldnames:
			if fname in fixedfields:
				continue
			if fname in ['s_status', 'circulars', 'customs', 'password']:
				continue
			if fname in view['fields']:
				continue
			if fname in skip:
				continue
			skip.append(fname)
	else:
		skip = ['todo', 'alias', 'notes', 'circulars', 'customs']
		view['fields'].remove('alias')

	view['nicenames'] = dict()
	for f in view['fields']:
		view['nicenames'][f] = Student.get_nicename(f)

	# notes for group
	if 'notes' in dezegroep:
		dezegroep['notes'].reverse()
	circular = sysls_o.get_sysl('s_circular')
	issumma = view['alias'] == 'summative'

	# studenten
	students_o = Students()
	active_statusses = get_active_statusses(sta)
	# print(f"DB LEZEN: s_group={groepnr} AND s_status in {active_statusses}")
	where = {
		's_status': {'$in': active_statusses},
		's_group': {'$in': [groepnr]},
	}
	students = students_o.agg_students_mongo(match=where, skip=skip)
	for i in range(len(students)):
		students[i]['filter'] = get_student_filter(students[i], sta)
		students[i] = StudentJinja(students[i], Student.get_model())

	return render_template(
		'groep-studenten.html',
		menuitem=menuitem,
		props=jus,
		students=students,
		fixedfields=fixedfields,
		groepen=groepen,
		groep=dezegroep,
		filter=filter,
		filters=fil,
		actiefstats=act,
		sysls=sysls_o.get(),
		allviews=groupviews,
		view=view,
		viewsumma=issumma,
		mijngroepen=mijngroepen,
		viewid=viewid,
		afns=allfieldnames,
		circular=circular,
		sortpath=f"/groepen/{groepnr}/{viewid}",
	)

@ep_groepen.get('')
def groep_none():
	# toon groepen
	# geen studenten
	jus = UserSettings()
	sta, fil, act = filter_stuff()
	filter = ''

	sysls_o = Sysls()
	# views always renews on call, also renews groups in Sysl object
	views_o = Views(slim=True)
	# list of group ids
	mijngroepen = views_o.mijn_groepen()
	# list of group dicts
	allegroepen = ListDicts.sortlistofdicts(list(sysls_o.get_sysl('s_group').values()), 'ordering')
	for i in range(len(list(allegroepen))):
		if not allegroepen[i]['id'] in mijngroepen:
			allegroepen.pop(i)

	return render_template(
		'groep-studenten.html',
		menuitem=menuitem,
		props=jus,
		students=list(),
		groepen=allegroepen,
		groep=None,
		filter=filter,
		filters=fil,
		actiefstats=act,
		sysls=sysls_o.get(),
		allviews=dict(),
		view=None,
		viewsumma=False,
		mijngroepen=mijngroepen,
		viewid=0,
		afns=list(),
		circular=dict(),
		sortpath=f"/groepen",
	)




@ep_groepen.post('/group-new-note/<int:groepnr>')
def group_new_note_post(groepnr):
	if not ('make-note' in request.form and 'new-note' in request.form):
		return redirect(request.referrer)

	note = Casting.str_(request.form['new-note'], '')
	if note == '':
		return redirect(request.referrer)

	sysl_o = Sysls()
	views_o = Views(slim=True)
	group = sysl_o.get_sysl_item('s_group', groepnr)
	if group is None:
		return redirect(request.referrer)

	jus = UserSettings()
	newnote = Note.get_empty()
	newnote['note'] = note
	newnote['alias'] = jus.alias()
	newnote['created_ts'] = Timetools.now_secs()
	newnote['done'] = 1
	# print(group)
	# print(newnote)
	if not 'notes' in group:
		group['notes'] = list()
	group['notes'].append(newnote)

	sysl_o.set_sysl_item('s_group', str(groepnr), group)
	sysl_o.store_sysl_mongo(
		{'sysl': 's_group', 'id': groepnr},
		{'$set': {'notes': group['notes']}},
	)
	return redirect(request.referrer)


@ep_groepen.post('/group-note/<int:groepnr>/<int:notenr>')
def groep_note_delete(groepnr, notenr):
	if not 'group-note-delete' in request.form:
		return redirect(request.referrer)

	sysl_o = Sysls()
	views_o = Views(slim=True)
	group = sysl_o.get_sysl_item('s_group', groepnr)
	if group is None:
		return redirect(request.referrer)
	if not 'notes' in group:
		return redirect(request.referrer)
	if len(group['notes']) < 1:
		return redirect(request.referrer)

	for i in range(len(list(group['notes']))):
		if group['notes'][i]['created_ts'] == notenr:
			del group['notes'][i]

	sysl_o.set_sysl_item('s_group', str(groepnr), group)
	sysl_o.store_sysl_mongo(
		{'sysl': 's_group', 'id': groepnr},
		{'$set': {'notes': group['notes']}},
	)
	return redirect(request.referrer)



