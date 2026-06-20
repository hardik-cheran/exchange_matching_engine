class Order:
    def __init__(self, order_id, side, price, quantity):
        self.order_id = order_id
        self.side = side
        self.price = price
        self.quantity = quantity


    def __repr__(self):
        return f"Order(id={self.order_id}, qty={self.quantity})"


class OrderBook:
    def __init__(self):
        self.bids = {}
        self.asks = {}
        self.next_order_id = 1
        self.trade_history = []

    def add_limit_buy(self,price,quantity):

        while quantity > 0 and self.asks:
            best_ask = min(self.asks)
            if best_ask > price:
                break
            oldest_order = self.asks[best_ask][0]
            available = oldest_order.quantity
            if quantity < available:
                print(f"TRADE: {quantity}@{best_ask}")
                self.trade_history.append({"price" : best_ask, "quantity" : quantity})
                oldest_order.quantity -= quantity
                quantity = 0
                
            else:
                quantity -= available
                print(f"TRADE: {available} @ {best_ask}")
                self.trade_history.append({"price" : best_ask, "quantity" : available})
                self.asks[best_ask].pop(0)
                if not self.asks[best_ask]:
                    del self.asks[best_ask]
            

        if quantity > 0:
            order =Order(self.next_order_id,"BUY",price,quantity)
            self.next_order_id +=1

            if price not in self.bids:
                self.bids[price] = []
            self.bids[price].append(order)

    def add_limit_sell(self,price,quantity):
        while quantity > 0 and self.bids:
            best_bid = max(self.bids)
            if best_bid < price:
                break
            oldest_order = self.bids[best_bid][0]
            available = oldest_order.quantity
            if quantity < available:
                print(f"TRADE: {quantity}@{best_bid}")
                self.trade_history.append({"price" : best_bid, "quantity" : quantity})
                oldest_order.quantity -= quantity
                quantity = 0
            else:
                quantity -= available
                print(f"TRADE: {available} @ {best_bid}")
                self.trade_history.append({"price" : best_bid, "quantity" : available})
                self.bids[best_bid].pop(0)
                if not self.bids[best_bid]:
                    del self.bids[best_bid]

        if quantity > 0:
            order = Order(self.next_order_id,"SELL",price,quantity)
            self.next_order_id +=1

            if price not in self.asks:
                self.asks[price] = []
            self.asks[price].append(order)

    def print_book(self):
        print("ASKS")
        for price in sorted(self.asks):
            print(price, ";", self.asks[price])

        print()
        print("BIDS")
        for price in sorted(self.bids, reverse = True):
            print(price, ":", self.bids[price])

    def market_buy(self, quantity):
        if not self.asks:
            print("No liquidity available")
            return
        best_ask = min(self.asks)
        oldest_order = self.asks[best_ask][0]
        available = oldest_order.quantity
        if quantity <= available:
            self.trade_history.append({"price" : best_ask, "quantity" : quantity})
            oldest_order.quantity -= quantity
            if oldest_order.quantity == 0:
                self.asks[best_ask].pop(0)
                if not self.asks[best_ask]:
                    del self.asks[best_ask]
        else:
            self.trade_history.append({"price":best_ask, "quantity" : available})
            self.asks[best_ask].pop(0)
            quantity -= available
            self.market_buy(quantity)

    def market_sell(self,quantity):
        if not self.bids:
            print("No liquidity available")
            return
        best_bid = max(self.bids)
        oldest_order = self.bids[best_bid][0]
        available = oldest_order.quantity
        if quantity <= available:
            self.trade_history.append({"price": best_bid, "quantity" : quantity})
            oldest_order.quantity -= quantity
            if oldest_order.quantity == 0:
                 self.bids[best_bid].pop(0)
                 if not self.bids[best_bid]:
                     del self.bids[best_bid]
        else:
            self.trade_history.append({"price" : best_bid, "quantity": available})
            self.bids[best_bid].pop(0)
            quantity -= available 
            self.market_sell(quantity)

    def cancel_order(self, order_id):
        for price in self.bids:
            for order in self.bids[price]:
                if order.order_id == order_id:
                    self.bids[price].remove(order)
                    if not self.bids[price]:
                        del self.bids[price]
                        return
        
        for price in self.asks:
            for order in self.asks[price]:
                if order.order_id == order_id:
                    self.asks[price].remove(order)
                    if not self.asks[price]:
                        del self.asks[price]
                        return
                    
    def best_bid(self):
        if not self.bids:
            return None
        return max(self.bids)
    
    def best_ask(self):
        if not self.asks:
            return None
        return min(self.asks)
    
    def mid_price(self):
        best_bid = self.best_bid()
        best_ask = self.best_ask()
        if best_bid is not None and best_ask is not None:
            return (best_bid + best_ask)/2
        return None

    def spread(self):
        if not self.bids or not self.asks:
            return None
        return self.best_ask() - self.best_bid()
    

book = OrderBook()

book.add_limit_buy(100,10)
book.add_limit_sell(102,10)

print(book.best_bid())
print(book.best_ask())
print(book.spread())
