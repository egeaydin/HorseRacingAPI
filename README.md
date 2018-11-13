# Horse Racing API
*API for getting horse race data from the official Turkish Jokey Organization!*

![alt text][banner]

Official Web site of Turkish Jokey Organization:[Turkish](http://www.tjk.org/)|[English](http://www.tjk.org/EN/YarisSever/YarisSever/Index)

## How to use
### Installation
Install the requirements with pip:
`pip install -r requirements.txt`

### Running the application
#### Local Machine
To run the API on your local machine, you can simply call ```python manage.py runserver``` on your favorite CLI inside the project directory.

#### Server
Please follow [django documentation](https://docs.djangoproject.com/en/2.1/howto/deployment/) for deploying on server

## API Call
Returns json data containing the information about the races run in the given city

* **URL**

  /race_day?&:year&:month&:day&:city

* **Method:**

  `GET`
  
*  **Query Params**

   **Required:**
 
   `year=[integer]`: The year of the desired race day
   `month=[integer]`: The month of the desired race day 
   `day=[integer]`: The day of the desired race day
   `city=[integer or string]`: City id or name for the desired city. Please refer to the table below:  
    
    | Name       | ID  |
    | ---------- |:---:|
    | Adana      | 1   |
    | Izmir      | 2   |
    | Istanbul   | 3   |
    | Bursa      | 4   |
    | Ankara     | 5   |
    | Urfa       | 6   |
    | Elazig     | 7   |
    | Diyarbakir | 8   |
    | Kocaeli    | 9   |

* **Error Response:**

  * **Code:** 400 NOT FOUND <br />
    **Content:** `{ message: "Could not find the race! Please make sure race is available on TJK.org.", 
    generated_url: [URL that is giving the error],
    status_code: 400}`

* **Examples:** 
    * ```/race_day?year=2018&month=11&day=12&city=Bursa```
    * ```/race_day?year=2018&month=11&day=12&city=4```  
    Both will fetch the races on 2018/11/12 from the city Bursa. 


[banner]: github/banner.jpg "Horse Racing API banner"