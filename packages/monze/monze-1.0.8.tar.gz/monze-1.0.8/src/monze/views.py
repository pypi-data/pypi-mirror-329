from flask import redirect, request, Blueprint, render_template
from general import JINJAstuff
from singletons import UserSettings, Sysls, Students, Views

from studenten import (
	Student,
	StudentJinja,
	filter_stuff,
	get_student_filter,
	get_active_statusses,
)

# =============== ENDPOINTS =====================
ep_views = Blueprint(
	'ep_views', __name__,
	url_prefix="/views",
	template_folder='templates',
    static_folder='static',
	static_url_path='static',
)

menuitem = 'views'

@ep_views.get('/<int:viewid>')
def view_get_viewid(viewid=0):
	jus = UserSettings()
	sta, fil, act = filter_stuff()

	sysls_o = Sysls()
	views_o = Views(slim=True)
	# get all active views
	active_views = views_o.active_views()

	# get and check current view
	current_view = views_o.get_single_by_key(viewid)
	# if no view_id get first own, or others
	if current_view is None:
		return redirect('/views')

	# at this point we have an active existing current_view
	views_o.void_normalize(current_view)

	# append nice names to view
	current_view['nicenames'] = dict()
	for f in current_view['fields']:
		current_view['nicenames'][f] = Student.get_nicename(f)

	# get all groups in this view
	allgroups = sysls_o.get_sysl('s_group')
	groups = dict()
	for id in allgroups.keys():
		# alleen groepen in deze view
		if not id in current_view['groups']:
			continue
		groups[id] = JINJAstuff(sysls_o.get_sysl_item('s_group', id), dict())

	default_fieldnames = list(Students.get_empty().keys())
	issumma = current_view['alias'] == 'summative'

	# get all students in these groups
	students_o = Students()
	active_statusses = get_active_statusses(sta)
	# print(f"DB LEZEN: s_group={groepnr} AND s_status in {active_statusses}")
	where = {
		's_status': {'$in': active_statusses},
		's_group': {'$in': list(groups.keys())},
	}

	skip = ['notes']
	for fname in default_fieldnames:
		if fname in current_view['fields']:
			continue
		if fname in ['customs', 'circulars', 's_group', 's_status', 'password']:
			continue
		if fname in skip:
			continue
		skip.append(fname)

	students = students_o.agg_students_mongo(match=where, skip=skip)
	for i in range(len(students)):
		students[i]['filter'] = get_student_filter(students[i], sta)
		students[i] = StudentJinja(students[i], Student.get_model())

	return render_template(
		'view-studenten.html',
		menuitem=menuitem,
		props=jus,
		students=students,
		groups=groups,
		allviews=active_views,
		view=current_view,
		viewid=viewid,
		viewsumma=issumma,
		sysls=sysls_o.get(),
		dfns=default_fieldnames,
		circular=sysls_o.get_sysl('s_circular'),
		filter='',
		actiefstats=act,
		sortpath=f"/views/{viewid}"
	)
@ep_views.get('')
def view_get():
	jus = UserSettings()
	sta, fil, act = filter_stuff()

	sysls_o = Sysls()
	views_o = Views(slim=True)
	# get all active views
	active_views = views_o.active_views()
	# get and check current view
	current_view = None

	return render_template(
		'view-studenten.html',
		menuitem=menuitem,
		props=jus,
		students=list(),
		groups=list(),
		allviews=active_views,
		view=current_view,
		viewid=None,
		viewsumma=False,
		sysls=sysls_o.get(),
		dfns=list(),
		circular=sysls_o.get_sysl('s_circular'),
		filter='',
		actiefstats=act,
		sortpath=f"/views"
	)

