# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
#########################################################################

from datetime import timedelta
from gluon.tools import prettydate

def index():
    return dict()

def menu():
    response.title = "Our Walmart"
    return dict()

def chat_test():
    db.people.name.label = "What's your name?"

    row = db(db.people.user_id == auth.user_id).select().first()
    db.people.user_id.readable = db.people.user_id.writable = False
    form = SQLFORM(db.people, record=row)
    if form.process().accepted:
        session.flash = "Welcome, %s!" % form.vars.name
        redirect(URL('default', 'people'))
    return dict(form=form)



def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()

def test1():
    form = SQLFORM(db.experiences)
    experiences_list = db(db.experiences).select()
    return dict(experiences_list=experiences_list, form=form)


def reset():
    db(db.people.id > 0).delete()
    db(db.messages.id > 0).delete()
    #db(db.textblob.id > 0).delete()
    db(db.users.id >0).delete()
    db(db.points.id >0).delete()
    db(db.experiences.id >0).delete()
    db(db.user_responses.id >0).delete()
    db(db.story.id >0).delete()
    db(db.stories.id >0).delete()
    db(db.post.id >0).delete()
    db(db.person.id>0).delete()

    redirect(URL('default', 'index'))

def people():
    """
    Gives the person a table displaying all the people, to search.
    """
    response.title = "Stories"
    db.people.name.label = "Name"
    # Creates a list of other people, other than myself.
    q = (db.people.id != auth.user_id)
    links = [dict(header='Click to chat',
                 body = lambda r: A(I(_class='fa fa-comments'), 'Chat', _class='btn btn-success',
                                    _href=URL('default', 'chat', args=[r.user_id])))]
    grid = SQLFORM.grid(q,
                        links=links,
                        editable=False,
                        details=False,
                        csv=False)
    return dict(grid=grid)


def store_message(form):
    form.vars.msg_id = str(db2.textblob.insert(mytext = form.vars.msg_id))

def chat():
    """This page enables you to chat with another person."""
    # Let us read the record telling us who is the other person.
    other = db(db.people.user_id == request.args(0)).select().first()
    logger.info("I am %r, chatting with %r" % (auth.user_id, other))
    if other is None:
        # Back to square 0.
        return redirect(URL('default', 'index'))
    # Pair of people involved.
    two_people = [auth.user_id, other.id]
    # We want them in order, so that all messages will be stored under the same pairs of ids.
    two_people.sort()
    # This query selects all messages between the two people.
    q = ((db.messages.user0 == two_people[0]) & (db.messages.user1 == two_people[1]))
    # This is the list of messages.
    db.messages.sender.represent = lambda v, r: 'You' if v == auth.user_id else other.name
    grid = SQLFORM.grid(q,
                        fields=[db.messages.msg_time, db.messages.sender, db.messages.msg_id],
                        details=False,
                        create=False,
                        orderby=~db.messages.msg_time,
                        csv=False,
                        sortable=False,
                        editable=False,
                        deletable=False,
                        searchable=False,
                        user_signature=False)

    # This is a form for adding one more message.

    db.messages.sender.readable = db.messages.sender.writable = False
    db.messages.msg_time.readable = db.messages.msg_time.writable = False
    form = SQLFORM(db.messages)
    form.vars.user0 = two_people[0]
    form.vars.user1 = two_people[1]
    if form.process(onvalidation=store_message).accepted:
        session.flash = "Message sent!"
        redirect(URL('default', 'chat', args=[other.user_id]))

    title = "Chat with %s" % other.name
    return dict(title=title, grid=grid, form=form)



def lessons_template():
    return dict()

def template_menu():
    return dict()

def template_nest():
    return dict()

def lessons():
    response.title='Lessons'
    return dict()

def ourwalmart():
    response.title='Our Walmart'
    return dict()

def logon():
    return dict()
#-----------------------------------------------------------------
# Lessons
#-----------------------------------------------------------------
def lesson01():
    response.title='Discrimination'
    return dict()

def lesson02():
    response.title='Workplace issues'
    return dict()

def lesson03():
    response.title='Wages, hours, schedules'
    return dict()

def lesson04():
    response.title='Safety'
    return dict()

def lesson05():
    response.title='Health'
    return dict()

def lesson06():
    response.title='Protection'
    return dict()

#------------------------------------------------------------------

def test():
    email, password = request.post_vars['email'], request.post_vars['password']
    if not auth.login_bare(email, password):
        db.auth_user.insert(
          first_name=None,
          last_name=None,
          email=email,
          password=db.auth_user.password.requires[0](password)[0]
                            )
    auth.login_bare(email, password)

    return dict()

@auth.requires_login()
def stories():
    response.title ="Stories"
    stories_list = db().select(db.stories.ALL, orderby=~db.stories.posting_time)
    stories = db.stories(request.args(0))
    now= datetime.utcnow()
    yesterday = now - timedelta(days=1)
    for stories_row in stories_list:



        post_number = db((db.post.posting_time > yesterday) & (db.post.stories_id == stories_row['id'])).count()
        stories_row['post_number'] = post_number
    return dict(stories_list=stories_list, stories=stories)

@auth.requires_login()
def create_stories():

    form = SQLFORM(db.stories)
    if form.process().accepted:
        session.flash = "Stories posted!"
        redirect(URL('default', 'stories', args=[form.vars.id]))
    return dict(form=form)

@auth.requires_login()
def post():
    response.title='Create story'
    stories = db.stories(request.args(0))
    post_list = db(db.post.stories_id ==stories).select(orderby=~db.post.posting_time)

    return dict(post_list=post_list, stories=stories)



@auth.requires_login()
@auth.requires_signature()
def create_post():
    response.title='Create story'
    stories_id = request.args(0)
    form = SQLFORM(db.post)
    db(db.stories.id == stories_id).update(posting_time=datetime.utcnow())
    form.vars.stories_id = stories_id
    if form.process().accepted:
        session.flash = "Your story has been added!"
        redirect(URL('default', 'post', args=[request.args(0)]))
    return dict(form=form)

@auth.requires_login()
@auth.requires_signature()
def edit_post():
    response.title='Edit story'
    stories_id = request.args(0)
    post_row = db.post(request.args(1))
    form = SQLFORM(db.post, record=post_row)
    db(db.stories.id == stories_id).update(posting_time=datetime.utcnow())
    form.vars.posting_time = datetime.utcnow()
    if form.process().accepted:
        session.flash = "Post edited!"
        redirect(URL('default', 'post', args=[stories_id]))
    return dict(form=form)

@auth.requires_login()
@auth.requires_signature()
def delete_post():
    response.title='Delete story'
    stories_id = request.args(0)
    db(db.post.id == request.args(1)).delete()
    session.flash = "Post deleted!"
    redirect(URL('default', 'post', args=[stories_id]))



##-----------------
## This is a test
##-----------------

def on_check(form):
    if form.vars.name == db(db.person.name=='Jake')._select():
        form.errors.name = T('User already exists')
        session.flash = ('Yes')
        return dict(form=form)




def onboard():
    response.title='Join'
    return dict()


def onboard():
    response.title='Join'
    return dict()

def logon():
    response.title='Log In'
    return dict()

def person():
    form = SQLFORM(db.person)
    if form.process(onvalidation=on_check).accepted:
        session.flash = T('The data was inserted')
        #redirect(URL('person'))
    else:
        session.flash = ('Nothing happened!')

    rows = db(db.person.name!=None).select()
    for row in rows:
        print row.name
    return dict(form=form)

