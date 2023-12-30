import json
import re
def is_valid_password(password):
    # Check if the password has at least 1 capital letter
    has_capital_letter = any(c.isupper() for c in password)

    # Check if the password has at least one special character
    special_chars = "[\p{}~!@©#$%^&*()_+{}|:!=?`€\[\];',./]+"
    has_special_char = any(c in special_chars for c in password)

    # Check if the password meets the length requirement
    has_minimum_length = len(password) >= 8

    # Return True only if all conditions are met
    return has_capital_letter and has_special_char and has_minimum_length

#password = "Rour!2222"
#result = is_valid_password(password)
#print(result)

# Login as a user or offer registration
def login():
    username = input("Enter your username:")
    password = input("Enter your password:")

    with open('users.json', "r") as file:
        data = json.load(file)
        for entry in data:
            if entry["username"] == username and entry["password"] == password:
                print("Successfully logged in")
                return entry  # Return the entire user entry

        register = input("The username does not exist in the users file.\nDo you like to register (Y/N)?")
        if register.lower() == "y":
            password_for_new_user = input(
                "\nEnter a password:\n 1-At least 1 capital letter.\n 2-At least 1 special symbol.\n 3-At least 8 characters: ")
            if is_valid_password(password_for_new_user):
                # Additional details for registration
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


                # Create a new user dictionary with additional details
                new_user = {
                    "username": username,
                    "password": password_for_new_user,
                    "wallet": 0,  # Wallet initialization
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
                }

                # Add the new user to the database
                data.append(new_user)
                with open('users.json', "w") as file:
                    json.dump(data, file, indent=4)
                print("User registered successfully.")
                return new_user  # Return the newly registered user data

            else:
                print("The password does not meet the criteria. \n Registration failed.\n")

    print("Either username or password were incorrect")
    return None


