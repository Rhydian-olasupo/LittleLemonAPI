# LittleLemonAPI
![Coursera](https://img.shields.io/badge/Coursera-%230056D2.svg?style=for-the-badge&logo=Coursera&logoColor=white)
![Meta](https://img.shields.io/badge/Meta-0668E1?style=flat&logo=meta&logoColor=white)
![Django](https://img.shields.io/badge/Django-092e20?style=flat&logo=django&logoColor=white)
![DjangoREST](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray)
![MySQL](https://img.shields.io/badge/mysql-%2300f.svg?style=for-the-badge&logo=mysql&logoColor=white)

Creating a fully functioning API project for the Littlelemon Restaurant so that client application developers can consume the APIs to develop web and mobile applications. People with different roles will be able to browse, add and edit menu items, place orders, browse orders, assign delivery crew to orders and finally deliver the orders.

## User registration and token generation endpoints
- Using Djoser to automatically create endpoints

    - **POST**: auth/users/: An api endpoint for user registration

    - **GET**:  auth/users/me: Display the current user

    - **POST**: auth/token/login: Generate user's access-token {username and password}


## Menu-Items Endpoints
- api/menu-items 
    Role: Customer and Delivery Crew:

    - **GET**: List all menu items

    - **POST,PUT,PATCH,DELETE**: Denies access and returns 403-Unauthorized HTTP status code

    Role: Manager

    - **GET**: List all menu items
    
    - **POST**: Creates a new menu item

- api/menu-items/{menuItem}:
    Role: Customer and Delivery Crew

    - **GET**: List a single menu item

    - **POST,PUT,PATCH,DELETE**: Denies access and returns 403-Unauthorized HTTP status code

    Role: Manager

    - **GET**: List a single menu item.

    - **PUT,PATCH**: Updates single menu item.

    - **DELETE**: Deletes menu item  

## User group management endpoints

- api/groups/manager/users:

    Role: Manager

    - **GET**: Returns all managers

    - **POST**: Assigns the username in the payload to the manager group

    - api/groups/manager/users/<int:id>:

        - **DELETE**: Removes this particular user from the manager group and returns 200 – Success if everything is okay. If user not found, return 404 - Not Found


- api/groups/delivery-crew/users:

    Role: Manager

    - **GET**: Returns all delivery crew members

    - **POST**: Assigns the username in the payload to the delivery group

    - api/groups/delivery-crew/users/<int:id>:

        - **DELETE**: Removes this particular user from the delivery group and returns 200 – Success if everything is okay. If user not found, return 404 - Not Found


## Cart management endpoints

- api/cart/menu-items:

    Role: Customer

    - **GET**: Returns current items int the cart for the current user 
    
    - **POST**: Adds the menu item to the cart.

    - **DELETES**: Deletes all menu-items created by the current user token

## Order management enpoints

- api/orders:
    Role: Customer

    - **GET**: Returns all orders with order items created by the user

    - **POST**: Creates a new order item for the current user. Gets current cart items from the cart endpoint and adds those items to the order items table. Then deletes all items from the cart for the user.

    Role: Manager

    - **GET**: 	Returns all orders with order items by all users

    Role: Delivery Crew

    - **GET**: Returns all orders with order items assigned to the delivery crew

- api/orders/{orderId}:

    Role: Customer

    - **GET**: Returns all items for this order id. If the order ID doesn’t belong to the current user, it displays an appropriate HTTP error status code.

    Role: Manager

    - **PUT,PATCH**: Updates the order. A manager can use this endpoint to set a delivery crew to this order, and also update the order status to 0 or 1. If a delivery crew is assigned to this order and the status = 0, it means the order is out for delivery. If a delivery crew is assigned to this order and the status = 1, it means the order has been delivered.

    - **DELETE**: Deletes this order

    Role: Delivery Crew

    - **PATCH**: A delivery crew can use this endpoint to update the order status to 0 or 1. The delivery crew will not be able to update anything else in this order.







