#!/usr/bin/python

import cgi
import parser
import item

store_list = parser.get_inventory('inventory.csv')
num_items = len(store_list)

form = cgi.FieldStorage()


money = int(form["points"].value)

for y in range(0, num_items):
    if "q%d" % y not in form:
        continue

    if form["a%d" % y].value == "buy":

        num_buy = int(form["q%d" % y].value)
        price_buy = store_list[y].cur_price
        subtotal = num_buy * price_buy
        store_list[y].updateQnty(-num_buy)
        money -= subtotal

    elif form["a%d" % y].value == "sell":

        num_sell = int(form["q%d" % y].value)
        price_sell = store_list[y].cur_price
        subtotal = num_sell * price_sell
        store_list[y].updateQnty(num_sell)
        money += subtotal
        

parser.write_inventory("inventory.csv", store_list)

print "Content-Type: text/html"
print
print "<html>"
print "<head>"
print "<title>Proof of Concept</title>"
print "</head>"
print "<body>"
print "<form method=\"post\" action=\"generator.py\">"
print "<table border=\"1\" cellpadding=\"5px\">"
print "<tr>"
print "<td>ITEM IN THE STORE</td>"
print "<td># LEFT</td>"
print "<td>PRICE</td>"
print "<td># ACT</td>"
print "<td>ACTION</td>"
print "</tr>"

for x in range(0, num_items):
    store_list[x].newPrice()
    print "<tr>"
    print "<td>" + store_list[x].name + "</td>"
    print "<td>%d</td>" % store_list[x].quantity
    print "<td>%d</td>" % store_list[x].cur_price
    print "<td><input name=\"q%d\" maxlength=\"2\" size=\"2\"></td>" % x
    print "<td>"
    print "<select name=\"a%d\">" % x
    print "<option value=\"buy\">Buy</option>"
    print "<option value=\"sell\">Sell</option>"
    print "</select>"
    print "</td>"
    print "</tr>"
    
print "</table>"
print "<input type=\"hidden\" name=\"points\" value=\"%d\">" % money
print "<input type=\"submit\" name=\"submit\" value=\"Submit order\"/>"
print "</form>"
print "<br />"
print "You have %d Space Dollars remaining." % money
print "</body>"
print "</html>"

        
        
        
