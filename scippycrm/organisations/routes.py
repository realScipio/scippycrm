from flask import render_template, flash, redirect, url_for, session, g, request, Markup
from flask import current_app as app
from bson.objectid import ObjectId

from scippycrm import login_required
from . import organisations_blueprint
from .forms import OrganisationForm

# show organisations overview
@organisations_blueprint.route('/organisations')    
@login_required
def organisations():
    coll = app.mongo.db.organisations
    orgs = coll.find()
    num_orgs = orgs.count()
    return render_template('organisations/organisations.html', title='Organisations', orgs=orgs, num_orgs=num_orgs)

# show / insert / update single organisation data
@organisations_blueprint.route('/organisation/new', methods=['GET', 'POST'])
@organisations_blueprint.route('/organisation/<ObjectId:org_id>', methods=['GET', 'POST'])
@login_required
def organisation(org_id='new'):
    coll = app.mongo.db.organisations
    if org_id == 'new':
        org = {}
        title = 'New organisation'
    else:            
        org = coll.find_one_or_404({'_id': org_id})
        title = 'Organisation: ' + org['name']
    
    form = OrganisationForm(obj=org)        

    # validate form data when submitted via POST request
    if form.validate_on_submit():
        obj_for_update = {}
        for fieldname, value in form.data.items():
            if (fieldname != 'submit' and fieldname != 'csrf_token' and fieldname != 'org_id'):
                obj_for_update[fieldname] = value            

        # insert new organisation record with POST-data from OrganisationForm
        if org_id == 'new':
            org_id = coll.insert_one(obj_for_update).inserted_id

        # update Mongo organisation record with POST-data from OrganisationForm
        else:
            coll.update_one(
                {"_id": ObjectId(org_id)},
                {"$set": obj_for_update}
            )
        
        # clean up Mongo records (no empty keys)
        org = coll.find_one_or_404({'_id': org_id})            
        clean_obj = {}
        for key in org:
            if org[key] != None and org[key] != "":
                clean_obj[key] = org[key]            
        coll.replace_one({'_id': ObjectId(org_id)}, clean_obj)            

        return redirect(url_for('organisations.organisation', org_id=org_id))         

    return render_template('organisations/organisation.html', title=title, org=org, form=form)