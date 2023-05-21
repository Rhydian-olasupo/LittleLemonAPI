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




