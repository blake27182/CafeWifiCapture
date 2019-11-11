# CafeWifiCapture

Imagine you are in a crowded coffee shop and you're ready to pay for your order. After paying you ask for the wifi, and the cashier gestures to a small blackboard easel on the counter. You open this app, take a picture, and you are instantly logged in to the correct network, and the credentials are saved in your phones network settings.

My current roadmap looks like this:

I have a Python script that authenticates with the google cloud vision api, and can make GET and POST requests with it. I have fed it an example image provided by google to test it out, and it works great on that.

	Next Steps:

make a little script to draw bounding boxes on the letters, words, and blocks etc and show the confidence and label

learn react native

Build a mvp in either Node.js or React Native, prefferably React because it will run natively on mobile, and so I'm assuming it will have more access to system files like network preferences.