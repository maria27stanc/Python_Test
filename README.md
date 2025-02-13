1. Webpage Creation:
• Create a simple webpage with a textbox for entering a city name and a submit button.
• Upon submitting the city name, fetch the weather forecast for the previous 5 days and for the next 3 days
from the www.weatherapi.com service using their API.
• Display the weather forecast for each day in a table format on the webpage.
2. Data Storage with any ORM:
• Use an ORM to create a SQLite database table to store the weather forecast data.
• The database table should have columns for date, city, max temperature, min temperature, total
precipitation, sunrise hour, and sunset hour and any other columns that are relevant to you.
• If a combination of date and city already exists in the database, the existing data should be replaced with
the new data.
3. Create a new page that contains:
• Dropdown for selecting the locations from the database.
• Table with column filter showing the data from the database for the selected location.
• A chart that shows the temperatures for the selected location.
