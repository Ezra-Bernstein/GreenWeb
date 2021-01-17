# GreenNet
 Try it out: https://greenweb.space

 
 ## Inspiration
I wanted to make a good hack for the Environmental track at CruzHacks, but and through research I found that it was difficult for many people to contribute to the environment. But I realized that because social media is so widely used and needs many resources to stay up and running, it was contributing to CO2 pollution.

## What it does
GreenWeb allows users to use social media like Twitter, while ensuring they offset their carbon footprint before use. After authenticating, users can upload images of items that they recycle, which decreases their footprint. The site will then allow them to tweet up until they have a positive footprint, at which point they have to upload an image to recycle again.

## How I built it
For hosting, I used Google App Engine. For the backend, I used Flask. For the front end I used HTML/CSS with Bootstrap v5 for styling and Jinja2 for templating. I used MongoDB as my database, and used the TwitterAPI for interfacing with twitter and GCP's Vision API for labeling the images.

## Challenges I ran into
Although I had some trouble figuring out how to do 3-legged oauth with Twitter, I was able to get it working relatively quickly. The trouble came towards the end, however, when I tried to deploy my site to Google App Engine with the MongoDB database. Unfortunately, the App Engine instance could only connect with the database 

## Accomplishments that I'm proud of
After the MongoDB workshop, I decided on the spot to incorporate it into my project. I'm really proud that I got it working so quickly. I'm also proud that I made a fully functional website with a custom domain.

NOTE: The website is up and running on greenweb.space, but in the demo I used localhost because my A and CNAME records were still authenticating between Google and Domain.com, and I didn't have time to wait for them before recording. 

## What I learned
I learned so much, from authenticating with APIs, to using MongoDB, to finding out how people can help save the environment!

## What's next for GreenWeb
In the future, I plan to add authentication for YouTube and Twitch, as watching videos uses far more energy than just tweeting.
