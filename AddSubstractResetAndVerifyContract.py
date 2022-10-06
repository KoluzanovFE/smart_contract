import smartpy as sp

class Verification(sp.Contract):
    def __init__(self, admin):
        self.init(number = sp.int(0), last_caller = sp.none, owner = admin)

    @sp.entry_point
    def add_number(self, value):
        sp.verify(value < 10, "Number is greater or equal to 10!")
        sp.verify(sp.some(sp.sender) != self.data.last_caller, "You can not add numbers twice in a row!")
        sp.set_type(value, sp.TInt)
        self.data.last_caller = sp.some(sp.sender)
        self.data.number += value

    @sp.entry_point
    def substraction(self, value):
        sp.verify(sp.sender == self.data.owner, "You are not the owner!")
        sp.set_type(value, sp.TInt)
        self.data.number -= value

    @sp.entry_point
    def reset(self):
        sp.verify(sp.sender == self.data.owner, "You are not the owner!")
        self.data.number = sp.int(0)

    @sp.add_test(name = "Verification")
    def test():
        alice = sp.test_account("Alice").address
        r = Verification(alice)
        scenario = sp.test_scenario()
        scenario.h1("Test number 1")
        scenario += r
        r.add_number(1).run(sender = alice, valid = True)
        r.add_number(1).run(sender = alice, valid = False)
        r.add_number(7).run(sender = sp.test_account("Bob"), valid = True)
        r.add_number(12).run(sender = sp.test_account("Kith"), valid = False)
        r.substraction(5).run(sender = sp.test_account("Kith"), valid = False)
        r.substraction(6).run(sender = alice, valid = True)
        r.reset().run(sender = sp.test_account("Kith"), valid = False)
        r.reset().run(sender = alice, valid = True)
