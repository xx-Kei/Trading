inventory = {}
sales_log = []

def add_item(item, qty):
    if item in inventory:
        inventory[item] += qty
    else:
        inventory[item] = qty
    print(f"Added {qty} {item}(s)")

def remove_item(item, qty):
    inventory[item] -= qty
    if inventory[item] <= 0:
        print(f"{item} removed from inventory")
        del inventory[item]

def sell_item(item, qty):
    inventory[item] -= qty
    sales_log.append((item, qty))
    print(f"Sold {qty} {item}(s)")

def restock_item(item, qty):
    inventory[item] += qty
    print(f"Restocked {qty} {item}(s)")

def update_item(old_item, new_item):
    inventory[new_item] = inventory[old_item]
    del inventory[old_item]
    print(f"{old_item} renamed to {new_item}")

def show_inventory():
    print("\nInventory:")
    for item, qty in inventory.items():
        print(f"{item}: {qty}")

def show_sales():
    print("\nSales Log:")
    for s in sales_log:
        print(f"{s[0]}: {s[1]} sold")

def total_stock():
    total = sum(inventory.values())
    print(f"Total items in stock: {total}")

def main():
    add_item("Apple", 10)
    add_item("Banana", 5)
    add_item("Orange", 8)
    sell_item("Apple", 3)
    sell_item("Banana", 7)
    remove_item("Orange", 2)
    restock_item("Banana", 10)
    update_item("Apple", "Green Apple")
    show_inventory()
    show_sales()
    total_stock()

    # More operations
    add_item("Grapes", 15)
    sell_item("Grapes", 20)
    remove_item("Banana", 5)
    update_item("Banana", "Yellow Banana")
    restock_item("Orange", 5)
    show_inventory()
    show_sales()
    total_stock()

if __name__ == "__main__":
    main()