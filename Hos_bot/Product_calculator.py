print("-------------Made-by-Hoswoo--------------")
# Price for 8oz is 224g/$1475 = $6.58 per gram

class Product_Calculator:
    def pickup_calc(self, jimSales, joshSales):
        priceOfPickup = 1475

        totalSales = jimSales + joshSales
        profit = totalSales - priceOfPickup
        recap = "Total sales: " + "${:,.2f}".format(totalSales) + ", " \
              "\nProfit: " + "${:,.2f}".format(profit) + " total or " + "${:,.2f}".format(profit / 2) + " each\n"

        jimGives = jimSales - profit / 2
        joshGives = joshSales - profit / 2
        if joshGives < 0:   # If this number is negative, Jim should give Josh money to make the profit even.
            return recap + "Assuming the next batch is " + "${:,.2f}".format(priceOfPickup) + " again " \
                  "\nJim gives: " + "${:,.2f}".format(jimGives) + \
                  "\nJim gives Josh: " + "${:,.2f}".format(abs(joshGives)) + \
                  "\nto pick up for the next batch." + \
                  "\n"
        if jimGives < 0:    # Same concept here
            return recap + "Assuming the next is batch is " + "${:,.2f}".format(priceOfPickup) + " again " \
                  "\nJosh gives: " + "${:,.2f}".format(joshGives) + \
                  "\nJosh gives Jim: " + "${:,.2f}".format(abs(jimGives)) + \
                  "\nto pick up for the next batch." + \
                  "\n"
        return recap + "Assuming the next is " + "${:,.2f}".format(priceOfPickup) + " again, " \
              "\nJim gives: " + "${:,.2f}".format(jimGives) + \
              "\nJosh gives: " + "${:,.2f}".format(joshGives) + \
              "\nto pick up for the next batch." + \
              "\n"
    # End pickup_calc()

    def use_equations(self, pay, omit=False):     # Equations were found using excel to find the line of best fit.
        pay = float(pay)
        price = 6.58
        if pay <= 0:
            quit()
        if 0 < pay <= 10:   # (0 - 10)
            product = round(0.07 * pay, 3)    # y = 0.07 * x
        elif pay <= 45:  # (10 - 45)
            product = round(.08 * pay - 0.1, 3)   # y = 0.08 * x - 0.1
        elif pay <= 80:  # (45 - 80)
            product = round(0.1 * pay - 1, 3)  # y = 0.1 * x - 1
        elif pay <= 140:   # (80 - 140)
            product = round(0.1167 * pay - 2.3333, 3)  # y = 0.1167 * x - 2.3333
        elif pay <= 250:    # (140 - 250)
            product = round(0.1273 * pay - 3.8182, 3)  # y = 0.1273 * x - 3.8182
        else:   # (250+) No more deals after one oz.
            product = round(1.12 * (pay/10), 3)

        ourCost = price * product
        profit = pay - ourCost
        if omit == False:
            return "You should give " + str(product) + "g(s)." + \
                  "\nCost: " + "${:,.2f}".format(ourCost) + \
                  "\nProfit: " + "${:,.2f}".format(profit)
        else:   # omit profits
            return "You will receive " + str(product) + " g(s) for " + "${:,.2f}".format(pay) + "."

    # End use_equations()


    def own_prices(self, product, pay):
        price = 6.58
        if pay <= 0:
            return 0
        if product <= 0:
            quit()
        round(product, 3)
        ourCost = price * product
        profit = pay - ourCost
        return "Giving " + str(product) + "g(s) for " + "${:,.2f}".format(pay) + " will" + "\nCost: " + "${:,.2f}".format(ourCost) \
               + "\nProfit:" + "${:,.2f}".format(profit)