## TwitchRPC - A universal Discord rich presence for Twitch

This software uses the data read off of your Twitch window to display an accurate and updated Discord presence

## Notice: The asset loader may take a few tries to work after adding your assets

### Getting Started

To get started you're going to need the following information before using the application
- Twitch web app (I recommend Progressive Web Apps for Firefox, but Edge or Chrome apps will work as well)
- Your Discord Application Client ID (see below)
 
### Discord Application

To make your Discord Application, follow these steps:
- Go to https://discord.com/developers/
- Click on "New Application"
- Name your new application "Twitch"
- After making your new application navigate to "General Information"
- Copy the "Application ID" (client ID) for future reference
- Add "twitch" icon from: https://github.com/lasagnapapa/TwitchRPC/blob/main/Assets/twitch_small.png

### Configuring Discord Application ID
- Launch "twitchrpc.exe", and navigate to the "Configuration" tab
- Paste the Application ID (client ID) we copied from earlier into the text box, and click save

### Starting/Stopping the RPC
Now that you've saved your Client ID, you can use the service
- Navigate to the "Home" tab, and click "Start". This will start the presence.
- Click "Stop" to stop the presence at any time

By default, when running Twitch and watching streams, etc, it will display this image on your Discord profile like so:

![image](https://github.com/lasagnapapa/TwitchRPC/assets/68775205/efe281aa-bbec-441c-84db-6f4fa6c8295d)

Additionally, you can upload assets to your Discord Developer Portal to match the name of your streamers as so:

If the streamer you're watching is "Streamer", upload their profile picture to "assets", and name it "streamer"

Note: This may not work at first, or at all in some cases. I am working on an alternative way of automatically retreiving the streamers picture, but for now this is the only potential method that works. However, it only works sometimes.
