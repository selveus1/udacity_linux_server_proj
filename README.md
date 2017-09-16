## CONTENTS OF THIS FILE
------------------------
* Introduction
* Requirements
* Installation / Usage
* Known Issues / Limitations
* Software Upgrades, Installs and Third-Party Applications 

### INTRODUCTION
----------------
This is a catalog web application with a user account registration and authenticaton system and item entry and modification capabilities. 
Using a Google Account, a user login into the site and browse the catalog. They can add items which they themselves can edit and delete at their leisure. The user can also view items that other users have added to the catalog. 

Guest users can also view the public version of the catalog and look through the items. 

Those wishing to gather the catalog information can see the stripped down JSON formatted version of the site.


### REQUIREMENTS
----------------
You must have a valid Google Account in order to log into the site and add items to the different categories. Without a Google Account, a user can only view the items of the catalog.

You must also have a web browser installed and Internet access. 


### INSTALLATION / USAGE
------------------------
To view online, simply head to the following URL : http://ec2-18-221-132-70.us-east-2.compute.amazonaws.com. This will bring you to the public site at which point you can login or view items as a guest.

To review the app on the server, ssh using the IP address : 18.221.132.70 on port 2200 with the user name 'grader'. Utilize the following command:

`<terminal prompt>$ ssh grader@18.221.132.70 -p 2200 -i ~/.ssh/<provided SSH key>`

The SSH key is in the 'Notes To Reviewer' field. 


### KNOWN ISSUES / LIMITATIONS
------------------------------- 
A user can only add items to the catalog, not categories.


### SOFTWARE UPGRADES, INSTALLS AND THIRD PARTY APPLICATIONS 
------------------------------------------------------------
All software packages on the used server were updated. Software that was installed was PostgreSQL, OAuth2, and Git. Server is an Amazon Lightsail instances.
