FOR PROPER STRUCTURED EXAMPLE, DOWNLOAD THE ZIP AND EXTRACT IT SOMEWHERE. 
THE CSS/HTML WILL FOLLOW A BASIC PATHWAY TO FIND THE CSS AND IMAGES THAT ARE NOW IN THEIR OWN FOLDERS.
THE RAW FILES ARE FOR EASE OF READING IN GITLAB - THEY WILL NOT WORK UNLESS YOU SETUP THE RIGHT FILE STRUCTURE YOURSELF. 
- JUST USE THE ZIP!



(Changelog)
4-1-21(#1)
Notes on Datapage.css (also within the CSS code as a comment)
The above @media widths are not doing anything as they aren't styled, at all (they are functionally empty). Setting the original min width down
to 600px stopped the screen losing styling until it is 600px (phone width?) and all the elements styled below are still within an aesthetic look (though everything is crumpled together)
Another observation is h5 is causing the screen to be wider than any possible width of screen (creating a width scroll bar) which is a bit unsightly, but I cannot identifiy how to fix that yet.
h5 might just need another margin property to keep it in line with the main container. I suggest removing the above @medias, and just keeping this one as the "main" style that covers all widths.*/

5-1-21
New Notes on CSS/HTML (#2, now removed)

'mark.html' renamed to 'DATAPAGE.html' - Does literally nothing to the code or CSS.

The header sections between FRONTPAGE and DATAPAGE have been made uniform. That doesn't mean they are setup the same way though!
i.e. FRONTPAGE has the CSS properties for <ul>, <nav>, <li>, <a>, and <header>. DATAPAGE was styled through <ul.main-nav>, <li>, <a>, and <h2>.
Obviously not very template friendly but with how much time is left there's not a lot I can do to make the code uniform too. 
TLDR: They look the same and function the same, but are completely different beasts. For the love of god don't copy paste regions over, it will badly mess up the look.

The font styles of DATAPAGE have been used on FRONTPAGE. Generally;
- Montserrat for the CAPITURE banner and the short about section
- Jura for the stats
- Darker Grotesque for the Edinburgh city scrolling image text

I fixed the DATAPAGE being slightly wider than any screen (leaving the awful sidescroll bar). ".actionitem 4" (the text between the maps and the nav bar) 
had a width setting at !00% that for some reason was larger than the page. Deleteing it removed it, and sorted some issues I had with the nav bar link styles too.

5-1-21 (version #2-1)
Referenced correctly to the head background for the DATAPAGE. Updated ZIP to #2-1. Removed #2 as that's literally the only difference.

7-1-21 (version #3)
A final merging of html templates, CSS, and python files to now include the FORMPAGE, as well as the oracle file and organised as it were in public_html. This will be the version I export into my own public_html before further editing to get the iframe templates correct. In other notes, the iframe has transparent images now (tree,forest,carbon.png)
