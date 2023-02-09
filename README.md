# SpotiCloud

SpotCloud is a tool that gives you insight into the emotional tone of your favorite Spotify playlists.<br>
With this project, you can analyze the lyrics of all the songs in a playlist and get a sentiment analysis score for a playlist.<br>
This score indicates whether the lyrics of the song are generally positive or negative.<br>
You can also visualize the most frequently used words in the lyrics with a word cloud.<br>
The word cloud provides a visual representation of the words that are used the most in the playlist,
allowing you to get a quick overview of the common themes in the lyrics.<br> 
Whether you're a music lover or a data enthusiast, SpotCloud is a fun and easy way to dive into the emotional
content of your playlists.<br>

## Installation

Copy the code from repo and navigate in terminal to the code directory.<br> To install the required packages, run the following command in your terminal:
<br><code>pip install -r requirements.txt</code>

## Using Docker

<code>docker pull reventaine/spoticloud</code>
<code>docker run -p 5000:5000 -d reventaine/spoticloud</code>

Access on <code>http://localhost:5000/</code>

## Usage

To run the application, navigate to the project directory and run the following command in your terminal: <br><code>python webapp.py</code> <br>
This will start the Flask development server and you can access the application in your web browser.

![Screenshot 2023-02-09 125259](https://user-images.githubusercontent.com/56644580/217774853-2ff1b29b-55ea-4af5-b2d8-a1ab50dc7f3e.jpg)
