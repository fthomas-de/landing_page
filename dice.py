from random import randint
from models import History, Base


class DiceController:
    def __init__(self, db):
        self.db = db

    def reset_db(self):
        Base.metadata.drop_all(bind=self.db.engine)
        Base.metadata.create_all(bind=self.db.engine)

        for i in xrange(0, 5):
            if len(list(self.db.session.query(History).filter(History.hist_id == i))) == 0:
                h = History(hist_id=i, value=-1, dice="dice" + str(i), name="name" + str(i))
                self.db.session.add(h)

        self.db.session.commit()

    def add_to_history(self, value, name, dice):
        last = self.db.session.query(History).order_by(History.hist_id.desc()).limit(1).all()[0].hist_id
        h = History(hist_id=last + 1, value=value, name=name, dice=dice)
        self.db.session.add(h)
        self.db.session.commit()

    def roll(self, value, name):
        result = randint(1, value)
        self.add_to_history(result, name, 'd' + str(value))
        return result

    def get_item(self, idx):
        lst = list(self.db.session.query(History).order_by(History.hist_id.desc()).limit(10).all())
        lst.reverse()
        return lst[idx].value, lst[idx].name, lst[idx].dice

    def get_history_as_tuple(self):
        h = list(self.db.session.query(History).order_by(History.hist_id.desc()).limit(10).all())
        h.reverse()
        return h

    def last_ten_players(self):
        p = [x[0] for x in list(
            self.db.session.query(History).with_entities(History.name).order_by(History.hist_id.desc()).limit(
                10).all())]
        return p

    def last_ten_dices(self, name=None):
        d = None
        if name is None:
            d = [x[0] for x in list(
                self.db.session.query(History).with_entities(History.dice).order_by(History.hist_id.desc()).limit(
                    10).all())]
        else:
            d = [x[0] for x in list(
                self.db.session.query(History).filter(History.name == name).with_entities(History.dice).order_by(
                    History.hist_id.desc()).limit(10).all())]

        d = map(str, d)
        if len(d) < 10:
            for i in range(10 - len(d)):
                d.append("d-1")
        return d

    def last_ten_results(self, name=None):
        r = None
        if name is None:
            r = [x[0] for x in list(
                self.db.session.query(History).with_entities(History.value).order_by(History.hist_id.desc()).limit(
                    10).all())]
        else:
            r = [x[0] for x in list(
                self.db.session.query(History).filter(History.name == name).with_entities(History.value).order_by(
                    History.hist_id.desc()).limit(10).all())]

        if len(r) < 10:
            for i in range(10 - len(r)):
                r.append(-1)
        return r

    def crit_chance(self, name):
        #dices = [('d4', 4), ('d6', 6), ('d8', 8), ('d10', 10), ('d12', 12), ('d20', 20)]
        dices = [('d20', 20)]

        crits = 0.0
        divider = 0.0
        avg = 0.0
        for (dice, max_value) in dices:
            lst = [x[0] for x in
                   self.db.session.query(History).filter(History.name == name).filter(
                       History.dice == dice).with_entities(History.value).order_by(History.value.desc()).all()]
            crits += lst.count(max_value)
            divider += len(lst)
            if not len(lst) == 0:
                avg = round(sum(lst)/float(len(lst)), 1)

        if not crits == 0:
            return round((100 * (crits / divider)), 2), int(divider), avg
        else:
            return 0.0, int(divider), avg
