


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
