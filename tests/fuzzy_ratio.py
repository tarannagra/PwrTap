import re
from thefuzz import fuzz

def main(check: str) -> None:
    check = check.lower()

    if fuzz.partial_ratio(check, "turn off the computer") >= 70:
        print("Turning off the computer...")
    
    elif fuzz.partial_ratio(check, "open {app} on the computer") >= 70:
        pattern = r"open (.+?)(?: on the computer)?$"
        print(f"Opening: {re.search(pattern, check).group(1)}")
    
    elif fuzz.partial_ratio(check, "restart the computer") >= 70:
        print("Restaring the computer")
    
    elif fuzz.partial_ratio(check, "turn the volume up") >= 70:
        print("Volume up!")
    
    elif fuzz.partial_ratio(check, "turn the volume down") >= 70:
        print("Volume down!")
    
    else:
        print("Option not found!")

while True:
    check = input("> ")
    main(check=check)