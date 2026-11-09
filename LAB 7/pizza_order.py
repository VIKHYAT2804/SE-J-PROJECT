
TOPPINGS = {"cheese": 40, "olives": 30, "onion": 20, "paneer": 50}
SIZES = {"S": 8, "M": 10, "L": 12}


def toppings_price(toppings_csv):
    if not isinstance(toppings_csv, str):
        return 0

    total = 0

    for t in toppings_csv.split(','):
        topping = t.strip().lower()

        if topping in TOPPINGS:
            total += TOPPINGS[topping]

    return total


def pizza_inches(size):
    if not isinstance(size, str):
        return 0

    return SIZES.get(size.strip().upper(), 0)


def split_bill(text):
    if not isinstance(text, str):
        return 0.0

    parts = text.split('/')

    if len(parts) != 2:
        return 0.0

    try:
        total = int(parts[0].strip())
        people = int(parts[1].strip())

        if total < 0 or people <= 0:
            return 0.0

        return round(total / people, 2)

    except ValueError:
        return 0.0


def main():
    print("==== Running toppings_price ====")
    user_input = input("Enter toppings as CSV (e.g. cheese,olives): ")
    result = toppings_price(user_input)
    print("Toppings Price:", result)

    print("\n==== Running pizza_inches ====")
    user_input = input("Enter pizza size (S/M/L): ")
    result = pizza_inches(user_input)
    print("Size in Inches:", result)

    print("\n==== Running split_bill ====")
    user_input = input("Enter total and people (e.g. 900/3): ")
    result = split_bill(user_input)
    print("Per Person:", result)


if __name__ == "__main__":
    main()
