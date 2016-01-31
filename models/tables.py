## This file defines the tables to be used

from datetime import datetime

# This is a table for all users.
db.define_table('people',
    Field('user_id', db.auth_user, default=auth.user_id),
    Field('name', required=True),
    Field('description', 'text'),
    )

db.people.id.readable = False
db.people.user_id.readable = False
db.people.description.represent = lambda v, r: DIV(v, _class="msg_content")


# Here is a table for messages.
db.define_table('messages',
    Field('user0', db.auth_user),
    Field('user1', db.auth_user),
    Field('sender',  db.auth_user, default=auth.user_id),
    Field('msg_time', 'datetime', default=datetime.utcnow()),
    Field('msg_id', 'text')) # Stored as a string

db.messages.user0.readable = db.messages.user0.writable = False
db.messages.user1.readable = db.messages.user1.writable = False
db.messages.msg_time.label = "Time"
db.messages.msg_id.label = "Message"
db.messages.msg_id.represent = lambda v, r: get_text(v)

def get_text(v):
    r = db2.textblob(v)
    return '' if r is None else r.mytext

# Table for big chunks of text.
db2.define_table('textblob',
    Field('mytext', 'text'),
    )



db.define_table('users',
                Field('user_id', db.auth_user, default=auth.user_id, writable=False),
                Field('first_name', ),
                Field('last_name', ),
                Field('preferred_named', ),
                Field('photo_id', db.auth_user, default=auth.user_id),
                Field('karma_points', db.auth_user, default=0),
                Field('admin_prefix', db.auth_user, default=0),
                Field('lessons_completed', db.auth_user, default=0)
)

db.users.id.readable = db.users.id.writable = False
db.users.user_id.readable = db.users.user_id.writable = False


db.define_table('points',
                )

db.define_table('experiences',
                Field('user_id', 'reference users' ),
                Field('kind', label='type', requires=IS_IN_SET(['Discrimination', 'Workplace_Issue', 'Wage', 'Safety',
                                                  'Health', 'Protection', 'Wage/hours/scheduling' ]), ),

                Field('story', label='Your Story', type='string'),
                )

db.experiences.id.readable = db.experiences.id.writable = False
db.experiences.user_id.readable = db.experiences.user_id.writable = False

db.define_table('user_responses',
                Field('user_id', 'reference users'),
                Field('q1', ), ##this is where we will put answers to the questions. for now there is nothing
                ## this is just a place holder
                Field('qn', ),

)

db.user_responses.id.readable = db.user_responses.id.writable = False


##---------------------
## Creating a form for users to post and read other peoples stories, or create a disccsutuon betwween
##--------------------

db.define_table('story',
                Field('user_id',)
                )

db.define_table('stories',
    Field('Kind', requires=IS_IN_SET(['Discrimination', 'Workplace_Issue', 'Wage', 'Safety',
                                                  'Health', 'Protection', 'Wage/hours/scheduling' ]),),
    Field('author', db.auth_user, default=auth.user_id, readable=False, writable=False),
    Field('posting_time', 'datetime', readable=False, writable=False, default=datetime.utcnow()),
    Field('post_number', 'integer', readable=False, writable=False),
    )

db.define_table('post',
    Field('preferred_name', 'reference users'),
    Field('description', 'text'),
    Field('author', db.auth_user, default=auth.user_id, readable=False, writable=False),
    Field('stories_id', 'reference stories', readable=False, writable=False),
    Field('posting_time', 'datetime', readable=False, writable=False, default=datetime.utcnow())
    )

db.define_table('person',
                Field('name', ),
                )