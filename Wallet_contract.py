import smartpy as sp

class Balance_contract(sp.Contract):
    def __init__(self, address, top_amount):
        self.init(owner = address, max_amount = sp.utils.nat_to_tez(top_amount), last_call = sp.none)


    @sp.entry_point
    def collect(self, amount):
        sp.verify(self.data.owner == sp.sender, "You are not the owner!")

        tz_amount = sp.utils.nat_to_tez(amount) 
        sp.verify(sp.balance > tz_amount, "Not enough tokens!")
        sp.verify(tz_amount < self.data.max_amount, "You want to withdraw too much!")

        sp.if self.data.last_call == sp.none:
            self.data.last_call = sp.some(sp.now)
        sp.else:
            deadline = self.data.last_call.open_some().add_minutes(2)
            sp.verify(sp.now > deadline, "You have to wait more!" )
        
        sp.send(sp.sender, tz_amount)

    @sp.entry_point
    def donate(self):
        pass


    @sp.add_test("Balance_contract")
    def test():
        alice = sp.test_account("Alice").address
        r = Balance_contract(alice, 15)

        scenario = sp.test_scenario()
        scenario.h1("Tests")
        scenario += r
        r.collect(5).run(sender = alice, valid = False)
        r.donate().run(sender = alice, amount = sp.tez(100))
        r.collect(7).run(sender = alice, valid = True)
        r.donate()
