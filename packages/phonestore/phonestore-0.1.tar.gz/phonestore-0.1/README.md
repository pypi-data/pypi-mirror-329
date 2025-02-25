<h1>Phone Store  Django App</h1>


<h2>Project Overview</h2>

The Phone E-Commerce Store with Django is a web application designed to facilitate online buying and selling of phones. 
It provides a platform for users to browse a catalog of phones, add them to their cart, and complete the purchase process.

<h2>Features</h2>
<hr/>
Product Catalog: Browse a comprehensive catalog of available phones.

User Authentication: Secure user authentication for personalized shopping experiences.

Shopping Cart: Add phones to a shopping cart and complete the purchase.

Order Management: View order history and manage orders.

Admin Panel: Manage products, orders, and users through the Django admin panel.

<h2>Getting Started</h2>
<hr/>
Follow these instructions to set up and run the Phone E-Commerce Store with Django locally.

first thing to do is to clone repository :

    $ git clone https://github.com/WebDevZakaria/phonestore.git
     
    $ cd phonestore
    
Create a virtual environment to install dependencies in and activate it:

    $ virtualenv venv
    
    $ venv\Scripts\activate

    
Then install the dependencies:

    (venv) $ pip install -r requirements.txt
    
Note the (venv) should be in the front of the prompt. this indicate that the terminal session is in a virtual env

Once downloading the dependencies has finished you can start the server by running:

     (env) $ python manage.py runserver

And go to your browser and navigate to http://127.0.0.1:8000.






