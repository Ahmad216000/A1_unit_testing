import json
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
    #Look for user in database
    with open('users.json', "r") as file:
        data = json.load(file)
        for entry in data:
            if entry["username"] == username and entry["password"] == password:
                print("Successfully logged in")
                return {"username": entry["username"], "wallet": entry["wallet"] }

        register = input("The username does not exist in the users file.\nDo you like to register (Y/N)?")
        if register.lower() == "y":
            password_for_new_user = input(
                "\nEnter a password:\n 1-At least 1 capital letter.\n 2-At least 1 special symbol.\n 3-At least 8' tall: ")
            if is_valid_password(password_for_new_user):
                new_user = {"username": username, "password": password_for_new_user, "wallet": 0}
                data.append(new_user)
                with open('users.json', "w") as file:
                    json.dump(data, file, indent=4)
                print("User registered successfully.")
                return {"username": username, "wallet": 0}
            else:
                print("The password does not meet the criteria. \n Registration failed.\n")

    print("Either username or password were incorrect")
    return None
