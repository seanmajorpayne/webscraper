# Web Scraper V0.0.1

## Thank you

Thank you for the challenge! I was having fun, so I decided to spend some extra time integrating asynchronous requests.
The async functionality is probably not implemented perfectly. I imagine with more time to read documentation and experiment
it could be significantly improved.

I decided to make folders for each website, where all data will be saved. Users might want the ability
to save multiple copies of the website over time (like the wayback machine), or have asset folders to hold images, etc.

## If I had more time...

1) Remove existing redundancy
2) Figure out how to write to disk concurrently, so it would run faster
3) Improve async functionality
4) The command line argument processing needs improvements
5) Replace general exceptions with nuanced ones
6) Test to see if the program will break with certain inputs
7) More checks for Null values, bad data, etc
8) Possibly make a website a class, which has a number of functions to extract data from the response.
9) Add asset downloading for the images, javascript, and css
10) Improve the path handling in the file processing
11) Add more content-types (currently only handles text/html)
12) Add more functions to handle non-2XX cases. Should 3XX or 4XX be saved?
13) Pull user_id & group_id from user in dockerfile so files aren't created with locked permissions

## Building and Running

Clone the repository

```
git clone git@github.com:seanmajorpayne/webscraper.git
```

Navigate to the directory with the cloned repository.

Run the following commands

Omit sudo if not needed on your system:

```
sudo docker build -t scraper .
sudo docker run -v /path/to/your/app/folder/fetch:/usr/src/app/fetch -dit --name scraper_app scraper
sudo docker exec scraper_app ./main urls https://www.google.com https://www.twitter.com https://www.facebook.com https://www.reddit.com
sudo docker exec scraper_app ./main --metadata https://www.google.com https://www.twitter.com https://www.facebook.com
```

Thank you for reviewing my code!