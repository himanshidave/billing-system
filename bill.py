import datetime
import os


def load_product():
    products = {}
    try:
        with open("product.txt", "r") as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                parts = line.split(",")
                if len(parts) != 2:
                    continue
                name, price = parts[0].strip(), parts[1].strip()
                try:
                    products[name] = float(price)
                except ValueError:
                    # Skip lines with invalid prices
                    continue
    except FileNotFoundError:
        print("Product file not found.")
    return products


def get_product(prompt):
    while True:
        try:
            value = float(input(prompt))
            if value < 0:
                print("Enter positive number.")
            else:
                return value
        except ValueError:
            print("Invalid number.")


def bill(items, customer_name, discount):
    lines = []
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines.append("=" * 54)
    lines.append("         CLOTHING STORE BILLING SYSTEM")
    lines.append("=" * 54)
    lines.append(f"Name: {customer_name}")
    lines.append(f"Date: {now}")
    lines.append(f"{'#':<4} {'Item':<20} {'Qty':>4} {'Price':>8} {'Total':>9}")  # alignment
    lines.append("-" * 54)
    subtotal = 0

    for i, item in enumerate(items, start=1):
        line = (
            f"{i:<4} {item['name']:<20} {item['qty']:>4} "
            f"Rs.{item['price']:>6.2f} Rs.{item['total']:>7.2f}"
        )
        lines.append(line)
        subtotal += item["total"]
    discount_amount = subtotal * discount / 100
    grand_total = subtotal - discount_amount

    if discount > 0:
        lines.append(f"{'Discount':<38} -Rs.{discount_amount:>6.2f}")
    lines.append("=" * 54)
    lines.append(f"{'GRAND TOTAL':<38} Rs.{grand_total:>7.2f}")
    lines.append("=" * 54)

    return lines, grand_total


def print_bill(items, customer_name, discount):
    if not items:
        print("No items yet.")
        return

    lines, grand_total = bill(items, customer_name, discount)
    for line in lines:
        print(line)


def save_bill_to_file(items, customer_name, discount):
    if not items:
        print("No items to save.")
        return

    lines, grand_total = bill(items, customer_name, discount)
    filename = f"bill_{customer_name}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    try:
        with open(filename, "w", encoding="utf-8") as f:
            for line in lines:
                f.write(line + "\n")
        print(f"Bill saved to {filename}")
    except OSError as e:
        print(f"Failed to save bill: {e}")


def add_item(items, products):
    print("\nAvailable Products:")

    product_list = list(products.keys())

    for i, name in enumerate(product_list, start=1):
        print(f"{i}. {name} - Rs.{products[name]}")
    choice = int(get_product("Select product number: "))

    if choice < 1 or choice > len(product_list):
        print("Invalid choice.")
        return

    product_name = product_list[choice - 1]
    price = products[product_name]

    qty = int(get_product("Quantity: "))
    total = qty * price

    items.append({
        "name": product_name,
        "qty": qty,
        "price": price,
        "total": total
    })
    print(f"Added {product_name} x{qty}")


def remove_item(items):
    if not items:
        print("No items to remove.")
        return

    for i, item in enumerate(items, start=1):
        print(i, item["name"])

    num = int(get_product("Enter item number: "))

    if 1 <= num <= len(items):
        items.pop(num - 1)
        print("Item removed.")
    else:
        print("Invalid number.")


def main():

    products = load_product()
    items = []

    print("\nWELCOME TO CLOTHING STORE BILLING SYSTEM")

    customer_name = input("Customer name: ")
    discount = get_product("Discount %: ")

    while True:
        print("\nMENU")
        print("1 Add Item")
        print("2 View Bill")
        print("3 Remove Item")
        print("4 Final Bill")
        print("5 Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            add_item(items, products)

        elif choice == "2":
            print_bill(items, customer_name, discount)

        elif choice == "3":
            remove_item(items)

        elif choice == "4":
            save_bill_to_file(items, customer_name, discount)

        elif choice == "5":
            print("Thank you!")
            break

        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()