## This file defines the tables to be used

db.define_table('users',
                Field('user_id', db.auth_user, default=auth.user_id),
                Field('preferred_named', db.auth_user, default=auth.user_id),
                Field('photo_id', db.auth_user, default=auth.user_id),
                Field('karma_points', db.auth_user, default=0)
)
db.define_table('points',
                )

