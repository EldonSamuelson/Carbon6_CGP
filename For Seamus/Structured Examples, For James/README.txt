FOR PROPER STRUCTURED EXAMPLE, DOWNLOAD THE ZIP AND EXTRACT IT SOMEWHERE. 
THE CSS/HTML WILL FOLLOW A BASIC PATHWAY TO FIND THE CSS AND IMAGES THAT ARE NOW IN THEIR OWN FOLDERS.
THE RAW FILES ARE FOR EASE OF READING IN GITLAB - THEY WILL NOT WORK UNLESS YOU SETUP THE RIGHT FILE STRUCTURE YOURSELF. 
- JUST USE THE ZIP!




Notes on Datapage.css (also within the CSS code as a comment)
The above @media widths are not doing anything as they aren't styled, at all (they are functionally empty). Setting the original min width down
to 600px stopped the screen losing styling until it is 600px (phone width?) and all the elements styled below are still within an aesthetic look (though everything is crumpled together)
Another observation is h5 is causing the screen to be wider than any possible width of screen (creating a width scroll bar) which is a bit unsightly, but I cannot identifiy how to fix that yet.
h5 might just need another margin property to keep it in line with the main container. I suggest removing the above @medias, and just keeping this one as the "main" style that covers all widths.*/