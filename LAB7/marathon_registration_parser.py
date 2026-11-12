def format_bib_name(name):
    """
    Upper-cases a runner's name and cuts it to 12 characters for the bib.
    Safely handles None and non-string inputs without crashing.
    """
    if not isinstance(name, str):
        return ""
    return name.strip().upper()[:12]

def parse_finish_time(text):
    """
    Converts a finish time written as H:MM:SS into seconds.
    Safely handles None, non-string, or malformed inputs without crashing.
    """
    if not isinstance(text, str):
        return None
    parts = text.split(':')
    if len(parts) != 3:
        return None
    try:
        hours = int(parts[0].strip())
        minutes = int(parts[1].strip())
        seconds = int(parts[2].strip())
        if hours < 0 or minutes < 0 or seconds < 0 or minutes >= 60 or seconds >= 60:
            return None
        return hours * 3600 + minutes * 60 + seconds
    except (ValueError, TypeError):
        return None

def average_split(text):
    """
    Averages split times given in minutes, separated by spaces.
    Safely handles None, empty, or non-numeric inputs without crashing.
    """
    if not isinstance(text, str):
        return 0.0
    tokens = text.split()
    if not tokens:
        return 0.0
    splits = []
    for token in tokens:
        try:
            val = int(token)
            if val < 0:
                return 0.0
            splits.append(val)
        except (ValueError, TypeError):
            return 0.0
    if not splits:
        return 0.0
    return sum(splits) / len(splits)

def main():
    print("==== Running format_bib_name ====")
    value = input("Enter the name to print on the bib: ")
    print("Bib name:", format_bib_name(value))

    print("\n==== Running parse_finish_time ====")
    value = input("Enter a finish time as H:MM:SS (e.g. 3:45:10): ")
    print("Finish time in seconds:", parse_finish_time(value))

    print("\n==== Running average_split ====")
    value = input("Enter your 5 km split times in minutes separated by spaces (e.g. 25 26 24): ")
    print("Average split (minutes):", average_split(value))

if __name__ == "__main__":
    main()
