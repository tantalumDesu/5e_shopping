import pandas as pd
import numpy as np
import math
from random import randint
pd.set_option('display.max_rows', 500)
inventory=pd.read_csv("5e_item_list.csv")
## changed size mod
settlement_sizes={"Thorpe": 20, "Hamlet": 50, "Village": 200, "Township": 400, "Town": 800, "Burg": 1500, "City": 5000, "Metropolis": 10000}
settlement_wealths={"Looted": 5000, "Needy": 3000, "Poor": 1500, "Comfortable": 500, "Wealthy": 150, "Opulent": 100}
settlement_pricelow={"Looted":40, "Needy":65, "Poor":85, "Comfortable":95, "Wealthy":100, "Opulent":120}
settlement_pricehigh={"Looted":65, "Needy":85, "Poor":105, "Comfortable":115, "Wealthy":130, "Opulent":200}
gold_pouch=0
shopping_cart = {}

def title():
    print     ("\n\n\n      *******      *                                 * ***                         ")
    print     ("    *       ***  **                                *  ****  *                      ")
    print     ("   *         **  **                               *  *  ****                       ")
    print     ("   **        *   **                              *  **   **                        ")
    print     ("    ***          **           ****     ****     *  ***                             ")
    print     ("   ** ***        **  ***     * ***  * * ***  * **   **            ***  ***  ****   ")
    print     ("    *** ***      ** * ***   *   **** *   ****  **   **   ***     * ***  **** **** *")
    print     ("      *** ***    ***   *** **    ** **    **   **   **  ****  * *   ***  **   **** ")
    print     ("        *** ***  **     ** **    ** **    **   **   ** *  **** **    *** **    **  ")
    print     ("          ** *** **     ** **    ** **    **   **   ***    **  ********  **    **  ")
    print     ("           ** ** **     ** **    ** **    **    **  **     *   *******   **    **  ")
    print     ("            * *  **     ** **    ** **    **     ** *      *   **        **    **  ")
    print     ("  ***        *   **     **  ******  *******       ***     *    ****    * **    **  ")
    print     (" *  *********    **     **   ****   ******         *******      *******  ***   *** ")
    print     ("*     *****       **    **          **               ***         *****    ***   ***")
    print     ("*                       *           **                                              ")
    print     ("**                    *            **                                              ")
    print     ("                    *              **                                             ")
    print     ("                    *                                                              ")
    print("\n")

def funds():
    global gold_pouch
    while True:
        try:
            platinum=int(input("\nInput your budget\nPlatinum coins: "))
            gold=int(input("Gold coins: "))
            electrum=int(input("Electrum coins: "))
            silver=int(input("Silver coins: ")) 
            copper=int(input("Copper coins: "))   
            total=(platinum*10)+gold+(electrum/2)+(silver/10)+(copper/100)
            if input(f"\n{total}gp\nIs this correct? y/n")=="y":
                gold_pouch=total
                return
        except (ValueError, IndexError):
            print("Invalid input. Please choose a valid option.")        

def choose_size():
    for i, v in enumerate(settlement_sizes):
        print(i, v)
    while True:
        try:
            choose = int(input("Choose the settlement's size: "))
            settlement_size = list(settlement_sizes.values())[choose]
            return settlement_size
        except (ValueError, IndexError):
            print("Invalid input. Please choose a valid option.")

def choose_wealth():
    for i , v in enumerate(settlement_wealths):
        print(i , v)
    while True:
        try:
            choose = int(input("Choose the settlement's wealth: "))
            settlement_wealth = list(settlement_wealths.values())[choose]
            price_low= list(settlement_pricelow.values())[choose] 
            price_high= list(settlement_pricehigh.values())[choose]
            return settlement_wealth, price_low, price_high
        except (ValueError, IndexError):
            print("Invalid input. Please choose a valid option.")

def dice():
    dice_rolls=[]
    for i in range(inventory.shape[0]):
        dice_rolls=np.random.randint(50,150, inventory.shape[0])/100
    inventory["dice roll"]=dice_rolls

def price_dice(price_low, price_high):
    dice_rolls=[]
    for i in range(inventory.shape[0]):
        dice_rolls=np.random.randint(price_low,price_high, inventory.shape[0])/100
    inventory["price dice"]=dice_rolls

def calculate_stock(settlement_size, settlement_wealth, rarity):
    base_chance={'C': 100, 'U': 80, 'R': 8, 'E': 1, 'L': 1}
    roll_multiplier={'C': 1, 'U': 0.5, 'R': 0.25, 'E': 0.2, 'L': 0.08}
    stock_count = 0
    for i in range(int(settlement_size*roll_multiplier[rarity])):
        stock_roll = randint(1, settlement_wealth)
        if stock_roll <= base_chance[rarity]:
            stock_count += 1
    return stock_count

def choose_shop():
    unique_types = []
    for t in inventory["type"].unique():
        if (inventory["type"] == t).any() and (inventory[inventory["type"] == t]["Stock"] > 0).any():
            unique_types.append(t)
    for i, t in enumerate(unique_types):
        print(f"{i+1}. {t}")
    while True:
        try:
            selected_type = unique_types[int(input("Select a type: ")) - 1]
            selected_shop = inventory[(inventory["type"] == selected_type)&(inventory["Stock"]>0)]
            print(selected_shop[["item", "Stock", "Cost"]])
            break
        except (ValueError, IndexError):
            print("Invalid input. Please choose a valid option.")       
    if input("Print shopping cart? y/n ") == "y":
        print(shopping_cart)

def buy_prompt():
    global shopping_cart
    global gold_pouch
    while True:
        try:
            choose=input("Buy? y/n or (r)emove ")
            if  choose== "y":
                print(f"Budget: {gold_pouch:.2f}")
                item_index, quantity = input("input index and quantity: ").split()
                selected_item = inventory.at[int(item_index), "item"]
                selected_quantity = int(quantity)
                selected_price = selected_quantity * inventory.at[selected_item.name, 'Cost']
                print(f"Selected item: {selected_item}")
                print(f"Quantity: {selected_quantity}")
                print(f"Price: {selected_price:.2f}")
                print(f"Budget: {gold_pouch:.2f}")
                if input("Are you sure? y/n ") == "y":
                    buy_item(selected_item, selected_quantity, selected_price)
            elif choose== "r":
                remove_item()            
            elif choose=="n":
                print(shopping_cart)
                print(f"Budget: {gold_pouch:.2f}")
                while True:
                    answer = input("Continue shopping? y/n ")
                    if answer == "y":
                        choose_shop()
                        break
                    elif answer == "n":
                        print(shopping_cart)
                        print(f"Remaining funds: {gold_pouch:.2f}")
                        exit()
                    else:
                        print("Invalid input. Please choose a valid option.")
                        continue
            else:
                print("Invalid input. Please choose a valid option.")
                continue
        except (ValueError, IndexError):
            print("Invalid input. Please choose a valid option.")
            continue
        
def buy_item(selected_item, selected_quantity, selected_price):
    global shopping_cart
    global gold_pouch
    if selected_quantity <= selected_item["Stock"]:
        if gold_pouch - float(round(selected_price, 2)) < 0:
            print("Purchase cancelled. Insufficient gold.")
            print(f"Gold in pouch: {gold_pouch:.2f}")
            return
        if selected_item["item"] in shopping_cart:
            shopping_cart[selected_item["item"]]["quantity"] += selected_quantity
            shopping_cart[selected_item["item"]]["Cost"] += selected_price
        else:
            shopping_cart[selected_item["item"]] = {"quantity": selected_quantity, "Cost": selected_price}
        inventory.at[selected_item.name, "Stock"] -= selected_quantity
        gold_pouch -= float(round(selected_price, 2))
        print(f"Bought {selected_quantity} {selected_item['item']} for {selected_price:.2f} gold.")
    else:
        print(f"Insufficient stock for {selected_item['item']}.")

def remove_item():
    global shopping_cart
    global gold_pouch
    print("Items in shopping cart:")
    for i, item in enumerate(shopping_cart):
        print(f"{i}: {item} - {shopping_cart[item]['quantity']} - {shopping_cart[item]['Cost']}(gp)")
    while True:
        try:
            item_index = int(input("Select item to remove: "))
            item = list(shopping_cart.keys())[item_index]
            item_quantity = shopping_cart[item]['quantity']
            quantity = int(input(f"Select quantity to remove (max {item_quantity}): "))
            if quantity <= 0:
                raise ValueError
            elif quantity > item_quantity:
                print(f"Invalid input. Maximum quantity to remove is {item_quantity}.")
                continue
            unit_cost = inventory.loc[inventory['item']==item, 'Cost'].values[0]
            item_cost = unit_cost * quantity
            gold_pouch += item_cost
            inventory.loc[inventory['item'] == item, 'Stock'] += quantity
            shopping_cart[item]['quantity'] -= quantity
            shopping_cart[item]['Cost'] = unit_cost * shopping_cart[item]['quantity']
            if shopping_cart[item]['quantity'] == 0:
                del shopping_cart[item]
            break
        except (ValueError, IndexError):
            print("Invalid input. Please choose a valid option.")
    print("Updated shopping cart:")
    print(shopping_cart)
    print(f"Gold pouch: {gold_pouch:.2f}")
    buy_prompt()

title()
funds()
settlement_size=choose_size()
settlement_wealth, price_low, price_high=choose_wealth()
dice()
price_dice(price_low, price_high)
inventory['base stock'] = inventory.apply(lambda row: calculate_stock(settlement_size, settlement_wealth, row['rarity']), axis=1)
inventory["Stock"]=(inventory["base stock"]*inventory["dice roll"]).apply(lambda x: math.floor(x))
inventory["Cost"]=round((inventory["price"]/100)*inventory["price dice"],2)
choose_shop()
buy_prompt()