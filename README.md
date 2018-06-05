//////// Daniel Rosenblatt & Amy Danoff’s CS50 Final Project - “my.Tour" ////////

This web-based application is designed for users to be able to search the collections of the Harvard Art Museum and
create custom tours based on interest and other parameters. The functionality of the website is primarily contained
within two main pathways, accessible through the index page: “Get Help from a Curator!” and “Design your own tour!”.
Other functionality exists through the “View Saved Tours” pathway, which is only accessible when users are logged in.

//// Get Help from a Curator! ////
The first pathway, “Get Help from a Curator!”, creates pre-curated tours for the user depending on custom input from
the user. Users are directed to a page with a search bar that says “type your interest here,” where users can free-formly
input interests such as keywords, genres of art, etc. On this page, there is also a button for “Additional Parameters,” where
users have the option of choosing one “Preferred Era,” one “Preferred Color,” and/or an “On-View Preference.” Each of
these parameters modifies the algorithm used to return images from the database in order to preference images that will be
most closely related to the users’ input. (the 3 parameters for “Preferred Era:” “Way way back,” “Way Back,” and “Not so
Far Back,” will preference searches for antiquity, post-classical, and modern-dated images, respectively, whereas clicking
the black-colored box under preferred color will preference images whose primary color is black, and checking the
“on-view preference” box will preference images that are currently on display in the Harvard Art museum galleries (as
opposed to in reserve)). After parameters and keywords have been chosen, users can click the “Explore” button to see a
curated slideshow of 4 images from the Harvard Art Museum collection. Users can click through these images using the arrows
on the sides of the slideshow to see the images in order, along with the titles, origins, and dates of each piece. Then, if
users are not satisfied with their results or wish to see more with the same search parameters, they can click the “See More
Like This!” button to see 4 different images with the same parameters as their original search. This button can be clicked
an infinite number of times to keep seeing tours with the same parameters, for as many as exist in the art museum collections.
Additionally, if users are logged in, they have the option to name and save this tour to their collection of Saved Tours.

//// Design your own tour! ////
The second pathway, “Design your own tour!”, allows users to create a 4-image tour, image-by-image, with each image having
different parameters. When users click on this pathway, they are directed to a page that allows them to input their interests
free-form into a search bar. Then, they will receive a page with 16 different image options, all related to their search
parameters. Users can click one of these images to save it as the first stop in their tour. Users are prompted to repeat
this process 4 times, with the option of searching for different parameters each time. Users can also quit out of the
process or return to the home page at any time to start a completely new tour. After 4 consecutive images have been
chosen through this route, the program displays a custom tour with the 4 stops the user has chosen. Again, these images
are displayed in slideshow form, and users can click through the stops in the slide show by clicking the arrows on the
images to display information about each image’s title, genre, and era. Finally, if the user is logged in, they have the
option to name and save this tour to their collection of Saved Tours.

//// Saved Tours ////
This function, which is available only when users are logged in, allows users to view and modify their previously saved tours.
The index of this page shows a list of each of the tours the user has saved to their account. Users can rename any tours
by double-clicking on its name. When this is done, a text box will pop up, where the user can type in a new name and
press enter to rename the tour. Users can also delete a tour by pressing the delete button and confirming deletion.
Finally, users can view any of their saved tours by pressing “view tour.” This will display that tour in a format that
reminds the user which tour they are looking at and shows each of the 4 images in the tour in slideshow form, along with
information about each of the images.

//// Other basic functions ////
In the header bar, which is always on the top right of the page, users can Log In or Register if they are not logged in.
If they are currently logged in, they can view their saved tours or Log Out. Users can also return home to the index
or view the About page at all times.
