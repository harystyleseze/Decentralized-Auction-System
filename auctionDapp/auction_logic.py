import logging

class Auction:
    def __init__(self):
        self.bids = {}
        self.highest_bid = 0
        self.highest_bidder = None

    def submit_bid(self, user, amount):
        if amount > self.highest_bid:
            self.highest_bid = amount
            self.highest_bidder = user
            self.bids[user] = amount
            return True
        return False

    def get_winner(self):
        return self.highest_bidder, self.highest_bid

    def get_bid_history(self):
        return self.bids
