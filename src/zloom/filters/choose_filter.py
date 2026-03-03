from zloom.all_filters import all_filters


def get_available_filters() -> list:
    filters = [f for f in all_filters.keys()]
    print("Available filters:", filters)
    return filters


def choose_filter(filters) -> str:
    while True:
        choice = input("Enter the name of the filter you want to use: ")
        if choice in filters:
            print(f"Selected filter: {choice}")
            active_filter = choice
            return active_filter
        else:
            print("Invalid choice. Please try again.")