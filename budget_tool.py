# ---------------------------------------------------------
# Budget Checking Tool
# ---------------------------------------------------------

def check_budget(max_budget: int):

    laptops = [
        {
            "name": "ASUS Vivobook 15",
            "price": 54990
        },
        {
            "name": "Lenovo IdeaPad Slim 5",
            "price": 69990
        },
        {
            "name": "HP Victus 15",
            "price": 74990
        },
        {
            "name": "ASUS TUF Gaming F15",
            "price": 82990
        },
        {
            "name": "Lenovo LOQ 15",
            "price": 89990
        },
        {
            "name": "Acer Aspire 7",
            "price": 62990
        },
        {
            "name": "Dell Inspiron 15",
            "price": 57990
        },
        {
            "name": "MSI Thin 15",
            "price": 77990
        }
    ]

    affordable_laptops = []

    for laptop in laptops:

        if laptop["price"] <= max_budget:

            affordable_laptops.append(laptop)

    return affordable_laptops


# ---------------------------------------------------------
# Test the Budget Tool
# ---------------------------------------------------------

if __name__ == "__main__":

    budget = 80000

    results = check_budget(budget)

    print("\nLaptops within budget:")

    for laptop in results:

        print(
            laptop["name"],
            "- ₹",
            laptop["price"]
        )