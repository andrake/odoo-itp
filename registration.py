# registration received
# try to match/update Contact- 1st by email then phone
# if no Contact match try same process with Leads.
## if Leads matched remove from Lead and create Contact
## no Leads match, create Contact

import json

# data setup list of Contacts and Leads object as proxy for database
class Contacts:
    def __init__(self, name, email, phone):
        self.name = name
        self.email = email
        self.phone = phone

class Leads:
    def __init__(self, name, email, phone):
        self.name = name
        self.email = email
        self.phone = phone

contacts = [{'name':'Alice Brown', 'email':None, 'phone':1231112223},
           {'name':'Bob Crown', 'email':'bob@crowns.com', 'phone':None},
           {'name':'Carlos Drew', 'email': 'carl@drewess.com', 'phone':3453334445},
           {'name':'Doug Emerty', 'email':None, 'phone':4564445556},
           {'name':'Egan Fair', 'email': 'eg@fairness.com', 'phone':5675556667}]

leads = [{'name':None, 'email': 'kevin@keith.com', 'phone': None},
           {'name':'Lucy', 'email':'lucy@liu.com', 'phone': 3210001112},
           {'name':'Mary Middle', 'email': 'mary@middle.com', 'phone': 33331112223},
           {'name': None, 'email': None, 'phone': 4442223334},
           {'name': None, 'email': 'ole@olson.com', 'phone': None}]

def databaseContacts():
    dbproxy = []
    for c in contacts:
        dbproxy.append(Contacts(c['name'], c['email'], c['phone']))
    return dbproxy

def databaseLeads():
    dbproxy = []
    for l in leads:
        dbproxy.append(Leads(l['name'], l['email'], l['phone']))
    return dbproxy


contactsDb = databaseContacts()
leadsDb = databaseLeads()

# class to Process Registration

class Registration:
    def __init__(self, name, email, phone, contactsDb, leadsDb):
        self.name = name
        self.email = email
        self.phone = phone
        self.contactsDb = contactsDb
        self.leadsDb = leadsDb

    def _matchEmail(self, obj):
        for o in obj:
            if o.email == self.email:
                return o
        return None

    def _matchPhone(self, obj):
        for o in obj:
            if str(o.phone) == str(self.phone):
                return o
        return None

    def _updateContact(self, orig):
        if self.name and len(self.name.split(' ')) >= len(orig.name.split(' ')):
            orig.name = self.name
        if self.email:
            orig.email = self.email
        if self.phone:
            orig.phone = int(self.phone)
        return orig

    def _createContact(self, cont):
        self.contactsDb.append(cont)
        return cont

    def _deleteLead(self, lead):
        self.leadsDb.remove(lead)


    def processRegistration(self):
        contactEmail = self._matchEmail(contactsDb)
        contactPhone = self._matchPhone(contactsDb)
        if contactEmail:
            update = self._updateContact(contactEmail)
            print('Contact updated based on email: ', update.__dict__)
        elif contactPhone:
            update = self._updateContact(contactPhone)
            print('Contact updated based on phone: ', update.__dict__)
        else:
            leadEmail = self._matchEmail(self.leadsDb)
            leadPhone = self._matchPhone(self.leadsDb)
            if leadEmail:
                update = self._updateContact(leadEmail)
                self._deleteLead(leadEmail)
                print('Lead converted and deleted: ', leadEmail.__dict__)
                print('New Contact based on lead email: ', update.__dict__)
            elif leadPhone:
                update = self._updateContact(leadPhone)
                self._deleteLead(leadPhone)
                print('Lead converted and deleted: ', leadPhone.__dict__)
                print('New Contact based on lead Phone: ', update.__dict__)
            else:
                newcontact = self._createContact(Contacts(self.name, self.email, self.phone))
                contactsDb.append(newcontact)
                print('New Contact added: ', newcontact.__dict__)


# Recieve json form data

def recieveRegistration(regstring):
    reg = json.loads(regstring)['registrant']
#     print(reg)
    newreg = Registration(reg['name'], reg['email'], reg['phone'], contactsDb, leadsDb)
    newreg.processRegistration()

recieveRegistration('{"registrant": {"name": "Lucy Liu", "email": "lucy@liu.com", "phone": ""}}')
recieveRegistration('{"registrant": {"name": "Doug", "email": "doug@emmy.com", "phone": "4564445556"}}')
recieveRegistration('{"registrant": {"name": "Uma Thurman", "email": "uma@thurs.com", "phone": ""}}')
