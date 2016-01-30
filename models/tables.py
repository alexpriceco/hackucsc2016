## This file defines the tables to be used

db.define_table('users',
                Field('user_id', db.auth_user, default=auth.user_id),
                Field('preferred_named', db.auth_user, default=auth.user_id),
                Field('photo_id', db.auth_user, default=auth.user_id),
                Field('karma_points', db.auth_user, default=0),
                Field('lessons_competed', db.auth_user, default=0)
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

db.define_table('responses',
                Field('q1', ), ##this is where we will put answers to the questions. for now there is nothing
                ## this is just a place holder
                Field('qn', ),

)

