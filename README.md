# **Forked from ashtrobe/grasswoex. Many thanks**

# **HOW TO GET GRASS USER ID USING ANDROID DEVICE [COMMUNITY EDITION]**  

Download and install [Kiwi Browser](https://play.google.com/store/apps/details?id=com.kiwibrowser.browser&hl=en).

Login to grass web and go to the dashboard, then open the Developer Tools in the Kiwi browser.

Go to the **Console** tab and paste this code:

> localStorage.getItem('userId')

If you can't paste, type `allow pasting` and press Enter, then paste the line above.

## **CONFIGURE TERMUX**

After Installing Termux, Make Sure You Allowed Storage Permission On Termux (device app) Settings. Or Run This Command In Termux -

> termux-setup-storage

> pkg install git

**Install Python**

> pkg install python
 
# **GIT CLONE THIS SCRIPT**

> git clone https://github.com/justmejay/grasscommscript.git

**CHANGE DIRECTORY TO SCRIPT FOLDER**

> cd grasscommscript

**Install Requirements**

> pip install -r requirements.txt

# RUN SCRIPT
> python lite.py

