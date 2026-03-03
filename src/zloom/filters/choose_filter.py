from zloom.filters import all_filters


def _get_available_filters() -> list:
    filters = [f for f in all_filters.keys()]
    print("Available filters:", filters)
    return filters


def _choose_filter(filters) -> str:
    while True:
        choice = input("Enter the name of the filter you want to use: ")
        if choice in filters:
            print(f"Selected filter: {choice}")
            active_filter = choice
            return active_filter
        else:
            print("Invalid choice. Please try again.")


def choose_filter() -> str:
    filter_names = _get_available_filters()
    if not filter_names:
        print("No filters available.")
        return None
    else:
        chosen_filter = _choose_filter(filter_names)
        user_filter = all_filters[chosen_filter]
        return user_filter

def main():
    choose_filter()

if __name__ == "__main__":
    main()