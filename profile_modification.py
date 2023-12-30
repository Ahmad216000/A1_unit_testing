import re
import json


def add_user_details(username):
    with open('users.json', 'r+') as file:
        data = json.load(file)
        user_found = False
        for user in data:
            if user["username"] == username:
                address = input("Enter your address: ")

                # Validate the address is not empty
                while not address.strip():
                    print("Address cannot be empty. Please enter your address.")
                    address = input("Enter your address: ")

                while True:
                    phone_number = input("Enter your phone number: ")
                    if re.match(r"^\d{10}$",
                                phone_number):  # Adjust the regex pattern for the correct phone number format
                        break
                    else:
                        print("Invalid phone number format. Please enter a 10-digit number.")

                while True:
                    email = input("Enter your email address: ")
                    if re.match(r"[^@]+@[^@]+\.[^@]+", email):
                        break
                    else:
                        print("Invalid email format. Please enter a valid email.")

                while True:
                    card_number = input("Enter your credit card number: ")
                    if len(card_number) == 16 and card_number.isdigit():
                        break
                    else:
                        print("Invalid credit card number format. Please enter a 16-digit number.")

                while True:
                    expiry_date = input("Enter expiry date (MM/YY): ")
                    if re.match(r"\d{2}/\d{2}", expiry_date):
                        break
                    else:
                        print("Invalid expiry date format. Please enter in MM/YY format.")
                # Validate for at least two names including Å, Ö, Ä along with standard alphabetical characters
                while True:
                    name_on_card = input("Enter name on card (First Last): ")
                    names = name_on_card.split()
                    if len(names) >= 2 and all(re.match(r"^[\w\sÅÖÄåöä]+$", name) for name in names):
                        break
                    else:
                        print("Invalid name format. Please enter at least two valid names.")

                while True:
                    cvv = input("Enter CVV: ")
                    if len(cvv) == 3 and cvv.isdigit():
                        break
                    else:
                        print("Invalid CVV. Please enter a 3-digit number.")

                user.update({
                    "address": address,
                    "phone_number": phone_number,
                    "email": email,
                    "credit_cards": [
                        {
                            "card_number": card_number,
                            "expiry_date": expiry_date,
                            "name_on_card": name_on_card,
                            "cvv": cvv
                        }
                    ]
                })
                user_found = True

        if user_found:
            with open('users.json', 'w') as file:
                json.dump(data, file, indent=4)
            print("User details have been added successfully.")
            updated_user = next((user for user in data if user["username"] == username), None)
            return updated_user  # Return the updated user dictionary
        else:
            print(f"User '{username}' not found.\n")
            return None  # Return None if the user is not found

def update_user_details(username):
    with open('users.json', 'r+') as file:
        data = json.load(file)
        user_found = False
        for user in data:
            if user["username"] == username:
                address = input("Enter your address: ")

                # Validate the address is not empty
                while not address.strip():
                    print("Address cannot be empty. Please enter your address.")
                    address = input("Enter your address: ")

                while True:
                    phone_number = input("Enter your phone number: ")
                    if re.match(r"^\d{10}$",
                                phone_number):  # Adjust the regex pattern for the correct phone number format
                        break
                    else:
                        print("Invalid phone number format. Please enter a 10-digit number.")

                while True:
                    email = input("Enter your email address: ")
                    if re.match(r"[^@]+@[^@]+\.[^@]+", email):
                        break
                    else:
                        print("Invalid email format. Please enter a valid email.")

                while True:
                    card_number = input("Enter your credit card number: ")
                    if len(card_number) == 16 and card_number.isdigit():
                        break
                    else:
                        print("Invalid credit card number format. Please enter a 16-digit number.")

                while True:
                    expiry_date = input("Enter expiry date (MM/YY): ")
                    if re.match(r"\d{2}/\d{2}", expiry_date):
                        break
                    else:
                        print("Invalid expiry date format. Please enter in MM/YY format.")
                # Validate for at least two names including Å, Ö, Ä along with standard alphabetical characters
                while True:
                    name_on_card = input("Enter name on card (First Last): ")
                    names = name_on_card.split()
                    if len(names) >= 2 and all(re.match(r"^[\w\sÅÖÄåöä]+$", name) for name in names):
                        break
                    else:
                        print("Invalid name format. Please enter at least two valid names.")

                while True:
                    cvv = input("Enter CVV: ")
                    if len(cvv) == 3 and cvv.isdigit():
                        break
                    else:
                        print("Invalid CVV. Please enter a 3-digit number.")

                user.update({
                    "address": address,
                    "phone_number": phone_number,
                    "email": email,
                    "credit_cards": [
                        {
                            "card_number": card_number,
                            "expiry_date": expiry_date,
                            "name_on_card": name_on_card,
                            "cvv": cvv
                        }
                    ]
                })
                user_found = True

        if user_found:
            with open('users.json', 'w') as file:
                json.dump(data, file, indent=4)
            print("User details have been updated successfully.")
            updated_user = next((user for user in data if user["username"] == username), None)
            return updated_user  # Return the updated user dictionary
        else:
            print(f"User '{username}' not found.\n")
            return None  # Return None if the user is not found


# Example usage to update user details
# update_user_details("Maximus")
