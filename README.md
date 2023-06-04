# capstone-1
Capstone Project Proposal 

What goal will your website be designed to achieve? 

This is an app to help art fair goers plan and organize their visits, save artworks that they like and stay informed of artworks for sale even if they don’t attend the art fair event in person.

What kind of users will visit your site? In other words, what is the demographic of your users? 

Fine art enthusiasts, Interior Designers, Art collectors, Journalists, Art advisors/consultants and other art professionals will use the web app. 

What data do you plan on using? You may have not picked your actual API yet, which is fine, just outline what kind of data you would like it to contain. 

The Artsy API. They have a ‘fairs’ API that lists the ‘shows’.. From the ‘Shows’ API I will be able to query the ‘partner’(gallery) and  ‘arworks’; from the ‘artworks’ API I can query the artist. 

In brief, outline your approach to creating your project (knowing that you may not know everything in advance and that these details might change later). 

Art fair assistant: 
Find out what galleries, artists and artworks are being offered at art fairs (tracked by Artsy)

Users are presented with current art fairs.  
Route: Lists current art fairs and descriptions for each
Route: Lists the galleries that are showing at each fair, and allow users to favorite galleries

Users can login.
Route: User page shows their favorited galleries. 

Schema image: 

![QuickDBD-export (3)](https://user-images.githubusercontent.com/116580308/236690854-61418f50-c788-4549-a3e8-c09a6f5c2098.png)

API: Artsy
https://developers.artsy.net/v1/

Update June 4/23: 

I had to adjust my proposal to not include artworks, because that information was not made available to me from the Artsy API. 

Instead of favoriting artworks, I let the users login and favorite certain galleries. There are still a few bugs to work out with editing user profiles, but the main routes are working at the moment to let a user sign up for an account, choose an art fair, list galleries in the fair, and favorite certain galleries. 

The user information, gallery information and user favorites are saved in separate database tables.

I could have made this a bit more smooth if I used javascript (no page refresh), but I opted to use only python and html for this project. 

