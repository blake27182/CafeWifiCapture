# CafeWifiCapture

Imagine you are in a crowded coffee shop and you're ready to pay for your order. After paying you ask for the wifi, and the cashier gestures to a small blackboard easel on the counter. You open this app, take a picture, and you are instantly logged in to the correct network, and the credentials are saved in your phones network settings.

My current state is this:

I made a Python script that authenticates with the google cloud vision api, and can make requests with it. I have fed it an example image provided by google to test it out, and it works great on that. (This API stuff took me forever to figure out but in the process, I learned about the http protocol, the http header, body, and that its just a json object. I learned how OAuth2 works and why it bounces back and forth so many times (so 3rd parties can log you in), and I learned how to use curl to make http requests manually! I used this tool to save my API response (which contained the token) in a json file. After looking at that file, it was easy to see how I could parse out all the info Google detected in my image. However, Google did email me the next day to tell me they found the token in my public repo and said that it was a very bad idea.

	Original Plan:

Make a little script to draw bounding boxes on the letters, words, and blocks etc and show the confidence and label. It seems irrelavent, but this will get me familiar with how Google vision sees, and it will give me a chance to learn different ways of manipulating image data.

Learn how computers find and authenticate with routers and wifi and all that jazz.

Make a process for finding the network name and password in the jumble of words on the back of a router or near a menu etc.

Make a process for using the words detected in the picture for logging into a network

    Actual Process:

I've finished the bounding box scripts which will make it easy for me to see what the google api is thinking. I have optional boxes for the paragraphs, words, and letters, all of different colors. 

I'm now working on a way to organize the words to easily pair the words together, so we know which is the network name and which is the password. It may be easier to pick a few good options and try every combination.
