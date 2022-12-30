# Motion_Detector_Sender

Running this programm allow us to start the camera and when an object(a person/animal/etc...) come inside,
it capture it, make a rectanguler around the object and start following it.

After the object disappear, the programm send via email the middle picure to the root (if we have 50 picures, the middle picure will be 25 pic)

In order email, to be send, please provide your email and its password in email_sender function.
The program is using gmail service.
In order to use other, change the port and the service in email_sender fuction.

Please also create(or change) the folder where the picture will be saved.
