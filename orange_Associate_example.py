
# Modules to Evaluate
import Orange
import re
from orangecontrib.associate.fpgrowth import *

# _______________________________________________________________________________
# read the dataset (basket format)
Xbasket = Orange.data.Table("final_basket.basket")
# __________________________________________________
#  make the OneHot transform in order to apply the "associate" methods
# cf., http://orange3-associate.readthedocs.io/en/latest/scripting.html
X, mapping = OneHot.encode(Xbasket)


# ______________________________________________________________________________
# search for the set of "frequent itemsets"
# "frequent_itemsets" returns an "iterator" (or generator)
# therefore if must be "consumed" after being invoked
# (the frequent_itemsets" function uses internally a "yield" function)

# setOf_itemset = frequent_itemsets( X, support )


# _______________________________________________________________________________
# the "setOf_itemset" has already been "consumed" (in the previous "print" loop)
# so we must invoke it again
iterations = 0
questions = dict()
# q1 supports %  3.12  ->  7.8
questions = [40, 100, 60, 99]
file = 1
interesting_points = dict()
rule_books_accepted = []
support = [x for x in range(questions[0], questions[1]) if x % 5 == 0]
confidence = [x/100 for x in range(questions[2], questions[3]) if x % 1 == 0]
# to plot points
points = []

for supp in support:
    for conf in confidence:

            setOf_itemset = frequent_itemsets(X, supp)
            iterations += 1
            print("%%%%%%%%%%%%", "-------------------------------------",
                  "min support allowed ", supp/1282*100, "-", "conf", conf)
            #print("creando itemset")

            # the next line "consumes" all the "setOf_itemset" and builds a dictionary from it
            # (this way we can use it for future operations)
            dict_setOf_itemset = dict(setOf_itemset)
            # print("association rule")
            setOf_rule = association_rules(dict_setOf_itemset, conf)

            # the next line "consumes" all the "setOf_rule" and builds a list from it
            # (this way we can use it for future operations)
            #
            list_setOf_rule = list(setOf_rule)


            for itemset in dict_setOf_itemset.keys():
                supp = dict_setOf_itemset[itemset]
                decoded_itemset = [var.name for _, var, _ in OneHot.decode(itemset, Xbasket, mapping)]
                tuple_itemset = (decoded_itemset, supp)
                # print(tuple_itemset)

            # _______________________________________________________________________________
            # decode the setOf-rules back to their original values
            print("found", len(list_setOf_rule), "rules")
            rule_book = []

            if 15 > len(list_setOf_rule) > 6:
                if list_setOf_rule not in rule_books_accepted:

                    rule_books_accepted.append(list_setOf_rule)
                    points.append([supp, conf])
                    print("CHOOSING POINT")

                for rule in list_setOf_rule:
                    LHS, RHS, supp, conf = rule

                    decoded_LHS = [var.name for _, var, _ in OneHot.decode(LHS, Xbasket, mapping)]
                    decoded_RHS = [var.name for _, var, _ in OneHot.decode(RHS, Xbasket, mapping)]
                    tuple_rule = (decoded_LHS, " ---> ", decoded_RHS, "supp", (supp/1282*100), "conf", conf)
                    rule_book.append(str(decoded_LHS)+" -> "+str(decoded_RHS))

                    print_value = True
                    for el in tuple_rule[0]:
                        if not re.match("lon_[0-9]{4}", el):
                            print_value = False
                    for el in tuple_rule[2]:
                        if not re.match("lon_[0-9]{4}", el):
                            print_value = False
                    if print_value:
                        out_file = open("Rule_books.txt", "a+")
                        out_file.write("\n" + str(tuple_rule) + "\n")
                        out_file.close()
                    print(tuple_rule)


                out_file = open("Rule_books.txt", "a+")
                out_file.write("\n------------------------------------------------  RULE_BOOK\n\n\n")
                out_file.close()

                points_as_key = str(supp) + "  -  " + str(conf)
                print(points_as_key)


            print("collected", len(rule_books_accepted), "rule_books")


for el in points:
    print(round(el[0],3))

for el in points:
    print(el[1])

print("iterations  ", iterations)



