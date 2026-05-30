import streamlit as st

# Initialize a larger hotel roster with more room options
if "rooms" not in st.session_state:
    st.session_state.rooms = {
        101: {"type": "Standard Single", "price": 80, "booked": False, "guest": ""},
        102: {"type": "Standard Single", "price": 80, "booked": False, "guest": ""},
        103: {"type": "Standard Single", "price": 80, "booked": False, "guest": ""},
        201: {"type": "Deluxe Double", "price": 140, "booked": False, "guest": ""},
        202: {"type": "Deluxe Double", "price": 140, "booked": False, "guest": ""},
        203: {"type": "Deluxe Double", "price": 140, "booked": False, "guest": ""},
        301: {"type": "Executive Suite", "price": 250, "booked": False, "guest": ""},
        302: {"type": "Executive Suite", "price": 250, "booked": False, "guest": ""},
        401: {"type": "Presidential Penthouse", "price": 600, "booked": False, "guest": ""},
    }

st.title("Grand Horizon Luxury Hotel")

# Section 1: View Rooms Matrix
st.header("Current Room Availability Matrix")

# Let's show a quick count overview
total_rooms = len(st.session_state.rooms)
booked_count = sum(1 for r in st.session_state.rooms.values() if r["booked"])
avail_count = total_rooms - booked_count

col1, col2, col3 = st.columns(3)
col1.metric("Total Rooms", total_rooms)
col2.metric("🟢 Available", avail_count)
col3.metric("🔴 Occupied", booked_count)

st.markdown("---")

# Display the rooms neatly
for room, info in st.session_state.rooms.items():
    if info["booked"]:
        status = f"🔴 Booked by **{info['guest']}**"
    else:
        status = "🟢 Available"
    st.write(f"**Room {room}** | {info['type']} | ${info['price']}/night | {status}")

st.markdown("---")

# Section 2: Book a Room with Guest Name
st.header("Check-In / Book a Room")
available_rooms = [r for r, info in st.session_state.rooms.items() if not info["booked"]]

if available_rooms:
    guest_name = st.text_input("Enter Guest Name:")
    room_to_book = st.selectbox("Select an Available Room:", available_rooms)
    
    if st.button("Confirm Check-In"):
        if guest_name.strip() == "":
            st.error("Please enter a guest name before booking!")
        else:
            st.session_state.rooms[room_to_book]["booked"] = True
            st.session_state.rooms[room_to_book]["guest"] = guest_name
            st.success(f"Success! {guest_name} has been checked into Room {room_to_book}.")
            st.rerun()
else:
    st.warning("All rooms are currently full!")

st.markdown("---")

# Section 3: Check-out with Bill Calculation
st.header("💸 Check-Out & Billing")
booked_rooms = [r for r, info in st.session_state.rooms.items() if info["booked"]]

if booked_rooms:
    room_to_vacate = st.selectbox("Select a Room for Departure:", booked_rooms)
    nights = st.number_input("Number of Nights Stayed:", min_value=1, value=1, step=1)
    
    # Get details for the receipt text
    current_guest = st.session_state.rooms[room_to_vacate]["guest"]
    price_per_night = st.session_state.rooms[room_to_vacate]["price"]
    total_bill = price_per_night * nights
    
    if st.button("Generate Invoice & Check-Out"):
        # Clear the room
        st.session_state.rooms[room_to_vacate]["booked"] = False
        st.session_state.rooms[room_to_vacate]["guest"] = ""
        
        # Show a pretty receipt summary
        st.balloons()
        st.info(f"""
        ### 🧾 Invoice for {current_guest} (Room {room_to_vacate})
        * **Room Type:** {st.session_state.rooms[room_to_vacate]['type']}
        * **Rate:** ${price_per_night} / night
        * **Duration:** {nights} night(s)
        * ----------------------------------
        * **Total Amount Due:** **${total_bill}**
        
        Check-out successful! Room is now vacant.
        """)
        # We don't trigger st.rerun() immediately so they can actually read the invoice popup!
else:
    st.write("No guests are currently checked in.")
