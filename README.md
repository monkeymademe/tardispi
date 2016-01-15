# TardisPi

The TardisPi is a laser cut Tardis made from MDF. Its supposed to be connected to a Raspberry Pi and will host a few features.

## Laser Cut Tardis 

I used the laser cut template from thingiverse - http://www.thingiverse.com/thing:19824

So all you need to do is cut paint and glue.

## Project Tweeting Tardis

First project was to turn lights inside the tardis on and off on twitter commands. Tweepy is installed on the pi and its streaming looking for the following keywords '#tardislightson' '#tardislightsoff' and '#tardisstatus'. The Pi also have a Pimoroni exploere hat pro with some small LED chirstmas tree lights connect to the motor h bridge... The idea is that I can control the brightness using the explorerhat.motor.forwards(x)

# #tardislightsoff
This will turn off the lights and the pi will take a picture of the tradis and replies with the picture

# #tardislightson
This will turn on the lights and the pi will take a picture of the tradis and replies with the picture

#tardisstatus
This will reply to the tweet with the information on the tardis. What is the light status on/off and also who made the last action with the time when it happened.




