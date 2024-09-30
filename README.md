

### Some issues that probably should be fixed
- User uploaded photos
- Stuff in temp.txt and temps (stuff i plan to add but lazy to fix lol)
- Delete Product (This ones bad)
- Non owner accounts trying to edit brings to No permission page (Gotta create those)


Airbnb concept website
---
Names of group members:<br>
- Izzy<br>
- Damar<br>
- William<br>
- Zakiy<br>
- Nala<br>
- Brian<br>


Application Description
--
Our application aims to create a user-friendly platform for travelers looking to explore Bali, offering a range of unique accommodations. From beachfront villas to cozy inland bungalows, users can find a place that suits their needs. The platform will facilitate seamless interactions between hosts and guests, providing features like real-time booking, reviews, and personalized recommendations based on user preferences. This application will not only enhance the travel experience but also support local hosts by giving them a platform to showcase their properties and connect with visitors.

Usefulness
<b>For Travelers</b>: <br>
Access to a diverse range of accommodations, detailed property descriptions, user reviews, and an easy booking process.

<b>For Hosts</b>: <br>
A platform to promote their properties, manage bookings, and engage with guests, ultimately boosting their income and contributing to the local economy.

List of modules to be implemented
### Authentication Module
- **Login View**: Allows users to log in using the `login_view` function.
- **Registration View**: Enables new users to create an account with the `register` function.
- **Logout View**: Logs out users and clears the last login cookie with the `logout` function.

### Property Management Module
- **Add Property**: Allows users to add new properties with the `add_property` function.
- **Edit Property**: Lets users edit their existing properties using the `edit_property` function.
- **Delete Property**: Enables users to delete their properties with the `delete_property` function.
- **Property List**: Displays a list of properties owned by the logged-in user with the `property_list` function.

### Property Detail Module
- **Property Detail View**: Shows detailed information about a specific property using the `property_detail` function.

### Home Page Module
- **Home View**: Displays featured properties and the user's properties on the home page with the `home` function.

### Error Handling Module
- **Error View**: Renders an error page using the `error` function.

### Cookie Management
- The application sets a cookie for the last login time in the `login_view` function and deletes it in the `logout` function.

### Message System
- Utilizes Django's messaging framework to provide user feedback (success or error messages) during registration, login, property addition, editing, and deletion.

### Source of Dataset: <br>
Literally just gonna steal from Airbnb or somewhere in google lol

User roles and their descriptions 
## User Roles and Their Descriptions

### 1. Guests
Guests are users who seek accommodations on the platform. Their primary functions include:
- **Browse Listings**: Search for and view properties available for rent.
- **Make Bookings**: Reserve accommodations based on availability and preferences.
- **Leave Reviews**: Provide feedback and rate their stay to assist future guests in their decision-making.
- **Manage Profile**: Update personal information, view booking history, and manage preferences.

### 2. Hosts
Hosts are property owners who list their accommodations on the platform. Their key responsibilities include:
- **Add Properties**: Create new listings with detailed descriptions and photos of their accommodations.
- **Manage Listings**: Edit, update, and delete their property listings as necessary.
- **Respond to Inquiries**: Communicate with potential guests regarding property details, availability, and bookings.
- **View Bookings**: Monitor reservations made by guests and manage the booking calendar.

## Conclusion
These roles are designed to create a balanced ecosystem within the application, ensuring a seamless experience for both guests and hosts while providing necessary oversight by admin users.


### Application deployment link
https://pbp.cs.ui.ac.id/web/project/william.samuel/airbnb
