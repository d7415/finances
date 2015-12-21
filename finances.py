#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy import *
#from sqlalchemy import create_engine
from sqlalchemy.orm import relation, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import text

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

# Create connection
engine = create_engine('sqlite:///finances')
Session = sessionmaker(bind=engine)
session = Session()

# Create maps
Base = declarative_base()

class Method(Base):
    __tablename__ = 'method'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    @staticmethod
    def load(name):
        Q = session.query(Method)
        for filter in (
                        Method.name.ilike(name),
                        Method.name.ilike(name+"%"),
                        Method.name.ilike("%"+name+"%"),
                        ):
            result = Q.filter(filter).first()
            if result is not None:
                break
        return result
    @staticmethod
    def get(name, session):
        new = False
        m = Method.load(name)
        if not m:
            new = True
            m = Method(name=name)
            session.add(m)
            session.commit()
        return (m, new)


class Place(Base):
    __tablename__ = 'place'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    @staticmethod
    def load(name):
        Q = session.query(Place)
        for filter in (
                        Place.name.ilike(name),
                        Place.name.ilike(name+"%"),
                        Place.name.ilike("%"+name+"%"),
                        ):
            result = Q.filter(filter).first()
            if result is not None:
                break
        return result
    @staticmethod
    def get(name, session):
        new = False
        p = Place.load(name)
        if not p:
            new = True
            p = Place(name=name)
            session.add(p)
            session.commit()
        return (p, new)

class Category(Base):
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    @staticmethod
    def load(name):
        Q = session.query(Category)
        for filter in (
                        Category.name.ilike(name),
                        Category.name.ilike(name+"%"),
                        Category.name.ilike("%"+name+"%"),
                        ):
            result = Q.filter(filter).first()
            if result is not None:
                break
        return result
    @staticmethod
    def get(name, session):
        new = False
        c = Category.load(name)
        if not c:
            new = True
            c = Category(name=name)
            session.add(c)
            session.commit()
        return (c, new)

class Transaction(Base):
    __tablename__ = 'transactions'
    id = Column(Integer, primary_key=True)
    date = Column(Integer)
    mid = Column(Integer, ForeignKey(Method.id, ondelete='cascade'))
    pid = Column(Integer, ForeignKey(Place.id, ondelete='cascade'))
    cid = Column(Integer, ForeignKey(Category.id, ondelete='cascade'))
    pence = Column(Integer)
    comment = Column(String)
    method = relation(Method)
    place = relation(Place)
    category = relation(Category)

    def amount(self):
        return float(self.pence)/100

    def pounds(self):
        return self.pence//100

    @staticmethod
    def header(sep=""):
        return "ID   %s Date     %s Method       %s Place               %s Category      %s Cost      %s Comments" % (sep, sep, sep, sep, sep, sep)

    def view(self, sep=""):
        return "%4s %s %s %s %-12s %s %-19s %s %-13s %s %9.2f %s %s" % (self.id, sep, self.date, sep, self.method.name, sep, self.place.name, sep, self.category.name, sep, self.amount(), sep, self.comment)

    @staticmethod
    def load(id):
        return session.query(Transaction).filter(Transaction.id==id).first()

class Template(Base):
    __tablename__ = 'templates'
    id = Column(Integer, primary_key=True)
    date = Column(Integer)
    mid = Column(Integer, ForeignKey(Method.id, ondelete='cascade'))
    pid = Column(Integer, ForeignKey(Place.id, ondelete='cascade'))
    cid = Column(Integer, ForeignKey(Category.id, ondelete='cascade'))
    pence = Column(Integer)
    comment = Column(String)
    method = relation(Method)
    place = relation(Place)
    category = relation(Category)

    def amount(self):
        return float(self.pence)/100

    def pounds(self):
        return self.pence//100

    @staticmethod
    def header(sep=""):
        return "ID   %s Date     %s Method       %s Place               %s Category      %s Cost      %s Comments" % (sep, sep, sep, sep, sep, sep)

    def view(self, sep=""):
        return "%4s %s ######%s %s %-12s %s %-19s %s %-13s %s %9.2f %s %s" % (self.id, sep, self.date, sep, self.method.name, sep, self.place.name, sep, self.category.name, sep, self.amount(), sep, self.comment)

    @staticmethod
    def load(id):
        return session.query(Template).filter(Template.id==id).first()

    def transaction(self, date):
        t = Transaction()
        t.date = date
        t.method = self.method
        t.place = self.place
        t.category = self.category
        t.pence = self.pence
        t.comment = self.comment
        return t


## 
def add():
    t = Transaction()
    date = raw_input("Date: ")
    if date == "":
        date = today
    t.date = int(date)
    p = raw_input("Place: ")
    while p[0] in '%/':
        for r in session.query(Place.name).filter(Place.name.ilike("%"+p[1:]+"%")).all():
            print "  > %s" % (r)
        p = raw_input("Place: ")
    (t.place, new) = Place.get(p, session)
    print ">> %s%s" % ("New Place: " if new else "", t.place.name)
    c = raw_input("Category: ")
    while c[0] in '%/':
        for r in session.query(Category.name).filter(Category.name.ilike("%"+c[1:]+"%")).all():
            print "  > %s" % (r)
        c = raw_input("Category: ")
    (t.category, new) = Category.get(c, session)
    print ">> %s%s" % ("New Category: " if new else "", t.category.name)
    (t.method, new) = Method.get(raw_input("Method: "), session)
    print ">> %s%s" % ("New Method: " if new else "", t.method.name)
    t.pence = int(raw_input("Cost (p): "))
    t.comment = raw_input("Comments: ")
    session.add(t)
    session.commit()
    print t.header()
    print t.view()

def add_template():
    t = Template()
    date = raw_input("Date (Day of Month) [01]: ")
    if date == "":
        date = "01"
    t.date = int(date)
    p = raw_input("Place: ")
    while p[0] in '%/':
        for r in session.query(Place.name).filter(Place.name.ilike("%"+p[1:]+"%")).all():
            print "  > %s" % (r)
        p = raw_input("Place: ")
    (t.place, new) = Place.get(p, session)
    print ">> %s%s" % ("New Place: " if new else "", t.place.name)
    c = raw_input("Category: ")
    while c[0] in '%/':
        for r in session.query(Category.name).filter(Category.name.ilike("%"+c[1:]+"%")).all():
            print "  > %s" % (r)
        c = raw_input("Category: ")
    (t.category, new) = Category.get(c, session)
    print ">> %s%s" % ("New Category: " if new else "", t.category.name)
    (t.method, new) = Method.get(raw_input("Method: "), session)
    print ">> %s%s" % ("New Method: " if new else "", t.method.name)
    t.pence = int(raw_input("Cost (p): "))
    t.comment = "[Auto] " + raw_input("Comments: ")
    session.add(t)
    session.commit()
    print t.header()
    print t.view()


def add_from_templates():
    import datetime
    s_date = raw_input("Statement Date: ")
    if s_date == "":
        s_date = today
    lastmonth = (datetime.datetime.strptime(s_date, '%Y%m%d') - datetime.timedelta(int(s_date[6:8]))).strftime('%Y%m%d')
    print Transaction.header()

    Ts = session.query(Template).all()
    for T in Ts:
        if int(s_date[6:8]) >= T.date:
            t = T.transaction(int("%s%02d" % (s_date[:6],T.date)))
            session.add(t)
            print t.view()
        else:
            if int(lastmonth[6:8]) >= T.date:
                t = T.transaction(int("%s%02s" % (lastmonth[:6],T.date)))
            else:
                t = T.transaction(lastmonth)
            session.add(t)
            print t.view()
    session.commit()


def edit(t):
    newval = raw_input("Date (%s): " % t.date)
    if newval:
        t.date = int(newval)
    newval = raw_input("Place (%s): " % t.place.name)
    if newval:
        (t.place, new) = Place.get(newval, session)
        print ">> %s%s" % ("New Place: " if new else "", t.place.name)
    newval = raw_input("Category (%s): " % t.category.name)
    if newval:
        (t.category, new) = Category.get(newval, session)
        print ">> %s%s" % ("New Category: " if new else "", t.category.name)
    newval = raw_input("Method (%s): " % t.method.name)
    if newval:
        (t.method, new) = Method.get(newval, session)
        print ">> %s%s" % ("New Method: " if new else "", t.method.name)
    newval = raw_input("Cost (%s): " % t.pence)
    if newval:
        t.pence = int(newval)
    newval = raw_input("Comments (%s): " % t.comment)
    if newval:
        t.comment = newval
    session.commit()
    print t.header()
    print t.view()


def edit_template(t):
    newval = raw_input("Date (%s): " % t.date)
    if newval:
        t.date = int(newval)
    newval = raw_input("Place (%s): " % t.place.name)
    if newval:
        (t.place, new) = Place.get(newval, session)
        print ">> %s%s" % ("New Place: " if new else "", t.place.name)
    newval = raw_input("Category (%s): " % t.category.name)
    if newval:
        (t.category, new) = Category.get(newval, session)
        print ">> %s%s" % ("New Category: " if new else "", t.category.name)
    newval = raw_input("Method (%s): " % t.method.name)
    if newval:
        (t.method, new) = Method.get(newval, session)
        print ">> %s%s" % ("New Method: " if new else "", t.method.name)
    newval = raw_input("Cost (%s): " % t.pence)
    if newval:
        t.pence = int(newval)
    newval = raw_input("Comments (%s): " % t.comment)
    if newval:
        t.comment = "[Auto] " + newval
    session.commit()
    print t.header()
    print t.view()


def datemdays(days):
    import datetime
    return datetime.datetime.strftime(
        (datetime.datetime.today()-datetime.timedelta(days)), '%Y%m%d')


def view(params):
    # Set defaults
    items = 5
    days = 0
    min_date = ''
    max_date = ''
    
    place = ''
    method = ''
    ttype = ''
    
    sortby = 'date'
    sort = 'DESC'

    exp = True

    tid = 0
    ids = False

    # Check for inputs
    while len(params) > 0:
        p1 = params.pop()
        p2 = p1.split('=')
        if (len(p2[1]) <= 2) and (not p2[1].isdigit()):
            p1 = p2[0] + '=\'' + codes[p2[1]] + '\''
        exec(p1)

    get_list(items=items, days=days, min_date=min_date, max_date=max_date,
             place=place, method=method, ttype=ttype, sortby=sortby, sort=sort,
             exp=exp, tid=tid, ids=ids)
        
    if exp:
        if ids:
            pad_print('idtrit')
        else:
            pad_print('trit')
    else:
        if ids:
            pad_print('idtr')
        else:
            pad_print('tr')


quit = False

# decide if I need this for default / autocomplete stuff. Otherwise check the
# import is elsewhere where necessary and remove.
import time
today  = int(time.strftime('%Y%m%d'))
back7  = int(time.strftime('%Y%m%d', time.localtime(time.time()-7*86400)))
back30 = int(time.strftime('%Y%m%d', time.localtime(time.time()-30*86400)))
numdays = (time.time() - time.mktime(time.strptime(str(session.query(func.min(Transaction.date)).first()[0]), '%Y%m%d')))/86400

while not quit:
    
    user_input = raw_input("What do you want to do today? ")
    command = user_input.split(" ", 1)[0]
    params=[]
    try:
        [paramstr] = user_input.split(" ", 1)[1:]
        params.extend(paramstr.split(" "))
    except ValueError:
        pass

    if command in ["view", "v"]:
        print Transaction.header()
        for t in session.query(Transaction).order_by(Transaction.date.desc()).order_by(Transaction.id.desc()).limit(params[0] if params else 5).from_self().order_by(Transaction.date.asc()).order_by(Transaction.id.asc()).all():
            print t.view()
    elif command in ["add", "a"]:
        add()
    elif command in ["newt", "nt"]:
        add_template()
    elif command in ["aft"]: # Add From Templates
        add_from_templates()
    elif command in ["edit", "e"]:
        if params:
            t = Transaction.load(params[0])
            if t:
                edit(t)
            else:
                print "Invalid transaction ID"
        else:
            print "Invalid Syntax"
    elif command in ["editt", "et"]:
        if params:
            t = Template.load(params[0])
            if t:
                edit_template(t)
            else:
                print "Invalid transaction ID"
        else:
            print "Invalid Syntax"
    elif command in ["delete", "del", "d"]:
        if params:
            t = Transaction.load(params[0])
            if t:
                print t.header()
                print t.view()
                if raw_input("Delete this row? (Y/N): ").lower() == "y":
                    session.delete(t)
                    session.commit()
            else:
                print "Invalid transaction ID"
        else:
            print "Invalid Syntax"
    elif command in ["search", "s", "/"]:
        print Transaction.header()
        Q = session.query(Transaction)
        for i in range(0, len(params), 2):
            if params[i][0].lower() == "i":
                Q = Q.filter(Transaction.id.ilike(params[i+1]))
            elif params[i][0].lower() == "d":
                Q = Q.filter(Transaction.date.ilike(params[i+1]))
            elif params[i][0].lower() == "m":
                Q = Q.join(Method).filter(Method.name.ilike(params[i+1]))
            elif params[i][0].lower() == "p":
                Q = Q.join(Place).filter(Place.name.ilike(params[i+1]))
            elif params[i].lower() == "c" or params[i][:2].lower() == "ca":
                Q = Q.join(Category).filter(Category.name.ilike(params[i+1]))
            elif len(params[i]) > 1 and params[i][:2].lower() == "co":
                Q = Q.filter(Transaction.comment.ilike(params[i+1]))
        Q = Q.order_by(Transaction.date.desc()).order_by(Transaction.id.desc()).limit(params[-1] if len(params) % 2 else 10)
        Q = Q.from_self().order_by(Transaction.date.asc()).order_by(Transaction.id.asc())
        for t in Q.all():
            print t.view()
    elif command in ["exact", "es", "//"]:
        print Transaction.header()
        Q = session.query(Transaction)
        for i in range(0, len(params), 2):
            if params[i][0].lower() == "i":
                Q = Q.filter(Transaction.id == params[i+1])
            elif params[i][0].lower() == "d":
                Q = Q.filter(Transaction.date == params[i+1])
            elif params[i][0].lower() == "m":
                Q = Q.join(Method).filter(Method.name == params[i+1])
            elif params[i][0].lower() == "p":
                Q = Q.join(Place).filter(Place.name == params[i+1])
            elif params[i].lower() == "c" or params[i][:2].lower() == "ca":
                Q = Q.join(Category).filter(Category.name == params[i+1])
            elif len(params[i]) > 1 and params[i][:2].lower() == "co":
                Q = Q.filter(Transaction.comment == params[i+1])
        Q = Q.order_by(Transaction.date.desc()).order_by(Transaction.id.desc()).limit(params[-1] if len(params) % 2 else 10)
        Q = Q.from_self().order_by(Transaction.date.asc()).order_by(Transaction.id.asc())
        for t in Q.all():
            print t.view()
    elif command in ["stats", "st"]:
        sep = ""
        num = int(params[0]) if params else 3
        print "Today   %9.2f %s Last 7 %9.2f %s Last 30 %9.2f" % ((session.query(func.sum(Transaction.pence), Transaction.date).filter(Transaction.date== today).first()[0] or 0)/100.0, sep,
                                                                  (session.query(func.sum(Transaction.pence), Transaction.date).filter(Transaction.date>= back7).first()[0] or 0)/100.0, sep,
                                                                  (session.query(func.sum(Transaction.pence), Transaction.date).filter(Transaction.date>=back30).first()[0] or 0)/100.0)
        gtotal = session.query(func.sum(Transaction.pence)).first()[0]/100
        print "Avg Day %9.2f %s  Avg 7 %9.2f %s  Avg 30 %9.2f" % (gtotal/numdays, sep, 7*gtotal/numdays, sep, 30*gtotal/numdays)
        print ""
        print "Method                  %s  Place                          %s  Category" % (sep, sep)
        print "------------------------%s---------------------------------%s-------------------------" % (sep, sep)
#         print "Last 30 %s
#         print "Total   %s"
        topm = session.query(func.sum(Transaction.pence).label("total"), Method.name).outerjoin(Method, Transaction.mid==Method.id).group_by(Method.name).order_by(text("total desc")).limit(num).all()
        topp = session.query(func.sum(Transaction.pence).label("total"), Place.name).outerjoin(Place, Transaction.pid==Place.id).group_by(Place.name).order_by(text("total desc")).limit(num).all()
        topc = session.query(func.sum(Transaction.pence).label("total"), Category.name).outerjoin(Category, Transaction.cid==Category.id).group_by(Category.name).order_by(text("total desc")).limit(num).all()
        for i in range(num):
            print "%-12s %9s  %s  %-19s %9s  %s  %-13s %9s" % (topm[i][1] if i < len(topm) and topm[i][0] > 0 else "", 
                                                               "%9.2f" % (topm[i][0]/100.0) if i < len(topm) and topm[i][0] > 0 else "", sep, 
                                                               topp[i][1] if i < len(topp) and topp[i][0] > 0 else "", 
                                                               "%9.2f" % (topp[i][0]/100.0) if i < len(topp) and topp[i][0] > 0 else "", sep, 
                                                               topc[i][1] if i < len(topc) and topc[i][0] > 0 else "", 
                                                               "%9.2f" % (topc[i][0]/100.0) if i < len(topc) and topc[i][0] > 0 else "")
    elif command in ["help", "h", "?"]:
        pass
    elif command in ["quit", "exit", "q", "x"]:
        quit = True
    else:
        print("Command not recognised.")
    session.commit()

session.close()
