from main import *

while True:
    print("\nMenu:")
    print("1. Create Customer")
    print("2. Add Products")
    print("3. Add to Cart")
    print("4. Show Cart")
    print("5. Make Order")
    print("6. Show Orders")
    print("7. Exit")
    
    choice = input("Enter your choice: ")

    if choice == '1':
        create_customer()
    elif choice == '2':
        add_products()
    elif choice == '3':
        add_to_cart()
    elif choice == '4':
        show_cart()
    elif choice == '5':
        make_order()
    elif choice == '6':
        show_orders()
    elif choice == '7':
        print("Closed ❌❌❌❌❌")
        break

    else:
        print("Invalid choice. Please try again.")

# Close the connection when done
conn.close()
