from __future__ import unicode_literals
import re
import bcrypt
from django.db import models
from datetime import datetime,timedelta,time

NAME_REGEX=re.compile(r'^[a-zA-Z+ ]+$')
EMAIL_REGEX=re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')


class UserManager(models.Manager):
# <--- Validate User Login---> #
    def validate_login(self,post_data):
        errors={}
        login=self.filter(email=post_data['email'])
        # <- Get Login email -> #
        if len(login)>0:
            user=login[0]
            # <- Password -> #
            if not bcrypt.checkpw(post_data['password'].encode(), user.password.encode()):
                errors['login']="email/password is incorrect"
        # <- Blank Field -> #
        else:
            errors['login']="email/password is incorrect"

        return errors

# <--- Validate User Registration---> #
    def validate_registration(self,post_data):
        errors={}
        for field,value in post_data.iteritems():
            # <- Blank Entry -> #
            if len(value)<1:
                errors[field]="{} field is required".format(field.replace('_',' '))
            # <- Name Length & Alpha Format -> #
            if field == "name" or field == "alias":
                if not field in errors and len(value) < 3:
                    errors[field]="{} field must be at least 3 characters".format(field.replace('_',' '))
                elif not field in errors and not re.match(NAME_REGEX,post_data[field]):
                    errors[field]="Invalid characters in {} field".format(field.replace('_',' '))
            # <- Password Length & Match-> #
            if field == "password":
                if not field in errors and len(value) <8:
                    errors[field]="{} field must be at least 8 characters".format(field.replace('_',' '))
                elif post_data['password'] != post_data['confirmpw']:
                    errors[field]="{} do not match".format(field.replace('_',''))
            # <- email Format & Exists -> #
            if field == "email":
                if not field in errors and len(value) < 3:
                    errors[field]="{} field must be at least 3 characters".format(field.replace('_',' '))
                elif not field in errors and not re.match(EMAIL_REGEX,post_data[field]):
                    errors[field]="{} Invalid characters in { field}".format(field)
                elif len(self.filter(email=post_data['email']))> 0:
                    errors[field]= "{} is already in use".format(field)
            if field == "dob":
                if not field in errors and datetime.strptime(post_data[field], '%Y-%m-%d').date() > datetime.today().date():
                    errors[field]= "Enter a valid date of birth"

        return errors

# <--- Create User Account ---> #
    def create_user(self,post_data):
        # <- Encode Password w/ Bcrypt -> #
        hashed= bcrypt.hashpw(post_data['password'].encode(), bcrypt.gensalt(5))
        new_user= self.create(
            name= post_data['name'],
            alias= post_data['alias'],
            email= post_data['email'],
            password= hashed,
            dob= post_data['dob'],
        )
        return new_user

class User(models.Model):
# <--- User Attributes ---> #
    name= models.CharField(max_length=255, default=None)
    alias= models.CharField(max_length=255, default=None)
    email= models.CharField(max_length=255, default=None)
    password= models.CharField(max_length=255, default=None)
    dob= models.DateTimeField(default=None)

    created_at= models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)

    objects = UserManager()
    # <- Print class attributes -> #
    def __repr__(self):
        return "id:{} name:{} alias:{} email:{} dob:{} created_at:{} updated_at:{}".format(self.id,self.name, self.alias, self.email, self.dob, self.created_at,self.updated_at)

class PokeManager(models.Manager):
    def count_poke(self, user):
        sum_poke= self.create(poke=1,user_id=user)
        return sum_poke
    def add_pokes(self, user,friend_id):
        add_poke= self.get(user_id=user).poke_users.add(User.objects.get(id=friend_id))
        return add_poke

class Poke(models.Model):
    poke= models.IntegerField(default=0)
    user=models.ForeignKey(User,related_name="pokes_id", null=True)
    poke_users=models.ManyToManyField(User,related_name="pokes", default=0)

    objects= PokeManager()

    def __repr__(self):
        return "id:{} poke: {} user: {} poke_users: {}".format(self.id,self.poke,self.user, self.poke_users)
