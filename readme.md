2/1/2024 4:59

removed unccessary and extra lines of code making it little optimized (model.py)


2/1/2024 4:51

updated response for getting image and rate in extra facilities user booked 

1/30/2024 8:13

updated :
create_booking and booking_details and model as per the requirements for extra faciltiies used booked.


1/22/2024 7:49

Update create_booking api for booking multiple extra facilities with respect to hours or units for an event
With updated json-content for create_booking


1/22/2024 6:03

updated model.py
updated apis for extra facility 
updated database 


1/12/2024 1:15

updated event's location_name (event name) in the response for inquiry's apis

1/12/2024 6:02

1 - /create_inquiry (for user only)
2 - /get_all_my_inquiries_user (for user to get all his/her inquiries irrespective of any event)
3 - /get_specific_inquiry/<int:inquiry_id> (for both user and vendor (each one will get their own) )
4 - /get_all_my_inquiries_vendor (for vendor , vendor can get all the inquiries, irrespective of the events)
5 - /get_my_inquiry/<int:inquiry_id> (for both vendor and user, both will get the same inquiry details if inquiry id is passed )
 


1/11/2024 2:49

updated the :
    update_event_hours 


1/11/2024 7:06

APIS done :
~ update_event_hours

~ create_inquiry
~ get_my_inquiry_vendor/<int:event_id>
~ get_all_my_inquiries_user 
changes on commit
 



1/11/2024 3:32

updated:
model.py
api : 
    ~ create_event  (start_time and end_time will be set to 00:00:00 and availability will be set to false for passing null to any day of the week)         
    ~ create_booking
    ~ get_event/
    ~ get_my_events
and updated database


1/10/2024 6:19

updated some apis to return the operating hours in responses

1/10/2024 12:52

model and create_event api changes 


1/9/2024 6:50

Timings Functionality Added In:
    ~ create_event
    ~ create_booking
new api :
~ update_event_hours



1/8/2024 6:50
refactoring and optimization of some apis



<<<<<<< HEAD
1/5/2024 7:20

favorite events api done in accordance with airbnb platform.





=======
>>>>>>> c7160a90fb45613af1a8767ba26718c44b184e20
12/29/2023 6:28

Updated search_event api with dynamic distancing etc.



12/22/2023 6:35


pending :  notification work 



12/22/2023 03:10
Added event_type in response from the booking table.
For :
Event icons in respnse : 1 - all_reviews 2 - pending_reviews 3 - booking_history 4 - get_my_events

top_venues 5 - bookings_today 6 - booking_details 7 - vendor_events




12/22/2023 12:59

all_reviews set for user_profile



12/21/2023 12:38

Event icons in respnse :
1 - all_reviews
2 - pending_reviews
3 - booking_history
4 - get_my_events
- - top_venues
5 - bookings_today
6 - booking_details
7 - vendor_events
