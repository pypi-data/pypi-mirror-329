from flask import redirect, request, Blueprint, render_template

from general import Casting, Timetools, JINJAstuff
from singletons import UserSettings, Sysls, Views
from emails import EmailBaseClass

from studenten import Student, upload_summative
from singletons import Students


# VIEWS WORDEN ALLEEN LOSGELATEN OP GROEPEN, NIET OP STUDENTEN!!!
def jinja_object(ding):
	sysls_o = Sysls()
	return JINJAstuff(ding, sysls_o.get_model())

# =============== endpoints =====================
ep_editviews = Blueprint(
	'ep_editviews', __name__,
	url_prefix="/editviews",
	template_folder='templates',
    static_folder='static',
	static_url_path='static',
)

menuitem = 'editviews'

@ep_editviews.get('/<int:viewid>/<path:copie>')
@ep_editviews.get('/<int:viewid>')
@ep_editviews.get('/')
def view(viewid=0, copie=None):
	copie = not copie is None

	sysls_o = Sysls()
	views_o = Views(slim=False)
	if viewid == 0:
		viewid = views_o.get_defaultkey()
	allviews = views_o.get()
	mijnviews = views_o.mijn_views()
	singleview = views_o.get_single_by_key(viewid)

	if singleview is None:
		return redirect(f'/editviews/{views_o.get_defaultkey()}')

	# fieldnames are standard db field names
	fieldnames = list(Students.get_empty().keys())
	# eruit are fieldnames that cannot be used in a view, or that are always included
	eruit = ['id', 'firstname', 'lastname', 'assessment', 's_gender', 'grade_ts', 'kom_code', 'notes', 'circulars', 'customs']

	fields = dict()
	for s in fieldnames:
		if s in eruit:
			continue
		fields[s] = Student.get_nicename(s)
	# fields now contains all the standard available fields for a view

	# single[fields] contains the fields in this single view
	for s in singleview['fields']:
		if s in fieldnames:
			fields[s] = Student.get_nicename(s)
		else:
			# these are the circulars fields
			fields[s] = s

	# these are the available groups
	groepen = sysls_o.get_sysl('s_group')

	# available email buttons:
	emailbuttons = EmailBaseClass().alle_emails()

	singleview = jinja_object(singleview)
	defaultview = None
	for key in allviews:
		if key == views_o.get_defaultkey():
			defaultview = jinja_object(allviews[key])
		else:
			allviews[key] = jinja_object(allviews[key])

	del(allviews[views_o.get_defaultkey()])

	return render_template(
		'editviews.html',
		menuitem=menuitem,
		props=UserSettings(),
		all=allviews,
		single=singleview,
		default=defaultview,
		mijnviews=mijnviews,
		kopie=copie,
		fields=fields,
		fixedfields=fieldnames,
		groepen=groepen,
		emailbuttons=emailbuttons,
	)

# for editing the view itself (topright in html)
@ep_editviews.post('/<int:viewid>')
def views_post(viewid):
	try:
		color = Casting.str_(request.form['color'], '#ffffff')
		status = Casting.int_(request.form['status'], 1)
		name = Casting.str_(request.form['changename'], '#ffffff')
	except Exception as e:
		print(f"view posts error: {e}")
		return redirect(f'/editviews/{viewid}')

	views_o = Views(slim=False)
	single = views_o.get_single_by_key(viewid)
	if single is None:
		print(f"view posts error: None")
		return redirect(f'/editviews/{viewid}')

	single['color'] = color
	single['status'] = status
	single['name'] = name
	views_o.update_view_mongo(viewid, single)
	return redirect(f"/editviews/{viewid}")

# for editing stuff in a view
@ep_editviews.post('/edit/<int:viewid>')
def view_edit_post(viewid):
	views_o = Views(slim=False)
	single = views_o.get_single_by_key(viewid)

	if single is None:
		return redirect('/editviews/default')

	if not ('fieldname' in request.form and 'fieldnamelist' in request.form):
		return redirect(f"/editviews/{viewid}")

	try:
		veldnamen = request.form['fieldnamelist'].split(',')
	except:
		return redirect(f"/editviews/{viewid}")
	veldnaam = Casting.str_(request.form['fieldname'], '')

	if veldnaam != '':
		if 'add-field' in request.form:
			veldnamen.append(veldnaam)

		elif 'delete-field' in request.form:
			veldnamen.remove(veldnaam)

		elif 'new-cycle-field' in request.form:
			if not veldnaam in veldnamen:
				veldnamen.append(f"c_{veldnaam}")

		elif 'new-text-field' in request.form:
			if not veldnaam in veldnamen:
				veldnamen.append(f"t_{veldnaam}")

	single['fields'] = veldnamen
	views_o.update_view_mongo(viewid, single)
	return redirect(f"/editviews/{viewid}")

# for deleting view
@ep_editviews.post('/delete/<int:viewid>')
def delete_post(viewid):
	views_o = Views()
	views_o.delete_view_mongo(viewid)
	return redirect(f'/editviews/{views_o.get_defaultkey()}')

# step 2 in copying a view
@ep_editviews.post('/kopie/<int:copyid>')
def kopie_post(copyid):
	jus = UserSettings()
	views_o = Views(slim=False)
	try:
		newname = Casting.name_safe(request.form['newname'], True)
		if newname == '':
			return redirect(f'/editviews/{views_o.get_defaultkey()}')
		if newname in views_o.get():
			return redirect(f'/editviews/{views_o.get_defaultkey()}')
	except:
		return redirect(f'/editviews/{views_o.get_defaultkey()}')

	# make new views with newname
	newview = views_o.get_single_by_key(copyid)
	newid = Timetools.now_secs()
	newview['name'] = newname
	newview['alias'] = jus.alias()
	newview['created_ts'] = newid
	newview['id'] = newid
	newview['groups'] = list()
	newview['color'] = '#ffffff'
	views_o.create_view_mongo(newview)
	return redirect(f"/editviews/{newid}")

@ep_editviews.post('/group/<int:viewid>')
def group_post(viewid):
	views_o = Views(slim=False)
	view = views_o.get_single_by_key(viewid)
	if view is None:
		return redirect(f'/editviews/{views_o.get_defaultkey()}')

	if not 'groups' in view:
		view['groups'] = list()

	groep_id = 0
	for item in request.form:
		if item in ['add-group', 'delete-group']:
			continue
		groep_id = Casting.int_(item, default=0)
	if groep_id == 0:
		return redirect(f"/editviews/{viewid}")

	if 'add-group' in request.form:
		view['groups'].append(groep_id)
	elif 'delete-group' in request.form:
		view['groups'].remove(groep_id)

	views_o.update_view_mongo(viewid, view)
	return redirect(f"/editviews/{viewid}")

@ep_editviews.post('/sort-views')
def sort_views():
	if not 'viewids' in request.form:
		return redirect(f"/editviews")

	try:
		ids: list = Casting.str_(request.form['viewids'], '').split(',')
		for i in range(len(ids)):
			ids[i] = Casting.int_(ids[i], 0)
	except:
		return redirect(f"/editviews")

	views_o = Views()
	views_o.reorder_views(ids)
	return redirect(f"/editviews")

@ep_editviews.post('/emailbutton/<int:viewid>')
def add_emailbutton(viewid):
	views_o = Views(slim=False)
	view = views_o.get_single_by_key(viewid)
	if view is None:
		return redirect(f'/editviews/{views_o.get_defaultkey()}')

	if 'add-emb' in request.form:
		if not 'emailbuttons' in view:
			view['emailbuttons'] = list()
		view['emailbuttons'].append(request.form['add-emb'])

	elif 'delete-emb' in request.form:
		if not 'emailbuttons' in view:
			view['emailbuttons'] = list()
		try:
			view['emailbuttons'].remove(request.form['delete-emb'])
		except:
			pass

	views_o.update_view_mongo(viewid, view)
	return redirect(f"/editviews/{viewid}")

@ep_editviews.post('/summative/<int:viewid>')
def summative_post(viewid):
	# makes a list summative for groups.
	# only admin can edit
	# alias = "summative"
	views_o = Views(slim=False)
	single = views_o.get_single_by_key(viewid)
	if single is None:
		return redirect(f'/editviews')
	single["alias"] = "summative"
	views_o.update_view_mongo(viewid, single)
	return redirect(f'/editviews/{viewid}')

@ep_editviews.post('/unsummative/<int:viewid>')
def unsummative_post(viewid):
	views_o = Views(slim=False)
	single = views_o.get_single_by_key(viewid)
	if single is None:
		return redirect(f'/editviews')
	jus = UserSettings()
	single["alias"] = jus.alias()
	views_o.update_view_mongo(viewid, single)
	return redirect(f'/editviews/{viewid}')

@ep_editviews.post('/uploadsummative/<int:viewid>')
@ep_editviews.post('/uploadsummative')
def uploadsummative_post(viewid=0):
	students_o = Students()
	views = Views(slim=False)
	allstudents = students_o.get_students_mongo(where={'s_status': {'$in': students_o.active_set()}})
	for student in allstudents:
		upload_summative(views, studid=student['id'], student=student)
	return redirect(f'/editviews')
