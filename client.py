import requests
import json
import random
import string
from decimal import Decimal


BASE_URL = "http://localhost:8000"


def handle_response(response):
    if response.status_code == 200 or response.status_code == 201:
        print(json.dumps(response.json(), indent=4))
    elif response.status_code == 404:
        print("Resource not found.")
    else:
        print(f"Error: {response.status_code} - {response.text}")


def create_user():
    username = input("Enter username: ")
    email = input("Enter email: ")

    data = {
        "username": username,
        "email": email,
        "password_hash": ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(15))
    }

    response = requests.post(f"{BASE_URL}/users", json=data)
    handle_response(response)


def get_user():
    user_id = int(input("Enter user ID: "))
    response = requests.get(f"{BASE_URL}/users/{user_id}")
    handle_response(response)


def update_user():
    user_id = int(input("Enter user ID to update: "))
    username = input("Enter new username (leave blank to keep current): ")
    email = input("Enter new email (leave blank to keep current): ")

    data = {}
    if username:
        data["username"] = username
    if email:
        data["email"] = email

    response = requests.put(f"{BASE_URL}/users/{user_id}", json=data)
    handle_response(response)


def delete_user():
    user_id = int(input("Enter user ID to delete: "))
    response = requests.delete(f"{BASE_URL}/users/{user_id}")
    handle_response(response)


def create_product():
    name = input("Enter product name: ")
    description = input("Enter product description (optional): ")
    price = Decimal(input("Enter product price: "))

    data = {
        "name": name,
        "price": float(price)
    }

    if description:
        data["description"] = description

    response = requests.post(f"{BASE_URL}/products", json=data)
    handle_response(response)


def get_product():
    product_id = int(input("Enter product ID: "))
    response = requests.get(f"{BASE_URL}/products/{product_id}")
    handle_response(response)


def update_product():
    product_id = int(input("Enter product ID to update: "))
    name = input("Enter new name (leave blank to keep current): ")
    description = input(
        "Enter new description (leave blank to keep current): ")
    price_str = input("Enter new price (leave blank to keep current): ")
    price = Decimal(price_str) if price_str else None

    data = {}
    if name:
        data["name"] = name
    if description:
        data["description"] = description
    if price:
        data["price"] = float(price)

    response = requests.put(f"{BASE_URL}/products/{product_id}", json=data)
    handle_response(response)


def delete_product():
    product_id = int(input("Enter product ID to delete: "))
    response = requests.delete(f"{BASE_URL}/products/{product_id}")
    handle_response(response)


def main():
    while True:
        print("\nChoose an action:")
        print("1. Create User")
        print("2. Get User")
        print("3. Update User")
        print("4. Delete User")
        print("5. Create Product")
        print("6. Get Product")
        print("7. Update Product")
        print("8. Delete Product")
        print("0. Exit")

        choice = input("Enter your choice: ")

        try:
            if choice == '1':
                create_user()
            elif choice == '2':
                get_user()
            elif choice == '3':
                update_user()
            elif choice == '4':
                delete_user()
            elif choice == '5':
                create_product()
            elif choice == '6':
                get_product()
            elif choice == '7':
                update_product()
            elif choice == '8':
                delete_product()

            elif choice == '0':
                break
            else:
                print("Invalid choice. Please try again.")
        except (requests.exceptions.RequestException, ValueError, json.JSONDecodeError) as e:
            print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
