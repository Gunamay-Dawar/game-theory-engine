import streamlit as st #importing streamlit and storing it in a nickname st
from engine import get_nim_value, find_best_move # importing fucntions get_nim_value and find_best_move from the python file engine

# Configure the look of the web page
st.set_page_config(page_title="Math Engine: Nim Solver", page_icon="🎲", layout="centered")

# HEADER
st.title("Combinatorial Game Theory Solver")
st.markdown("""
This engine evaluates mathematical game states using the **Minimum Excludant (Mex)** property 
and **Dynamic Programming (Memoization)**. 
* Currently configured for a standard **3-Heap Game of Nim**.
""")


st.divider() #draws a horizontal line ont he page that seperates sectionis. 

# --- SIDEBAR CONTROLS ---
st.sidebar.header("Game Settings") # st.sidebar is the panel on the left side of the page. This adds a heading to it that says “Game Settings”.
st.sidebar.write("Adjust the slider to change the initial number of counters in each heap.")

# Set up sliders so users can visually customize the board layout
heap_1 = st.sidebar.slider("Heap 1 Size", min_value=0, max_value=15, value=3)
heap_2 = st.sidebar.slider("Heap 2 Size", min_value=0, max_value=15, value=4)
heap_3 = st.sidebar.slider("Heap 3 Size", min_value=0, max_value=15, value=5)

# Group the UI inputs into our standard mathematical state tuple
current_state = tuple(sorted([heap_1, heap_2, heap_3]))

# --- MAIN DASHBOARD VISUALS ---
st.subheader("Current Board Analysis") # A section label comment, then a mid-sized heading on the page. subheader is smaller than title.


# Create three columns to display the status of each heap elegantly
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="Heap 1", value=heap_1)
with col2:
    st.metric(label="Heap 2", value=heap_2)
with col3:
    st.metric(label="Heap 3", value=heap_3)

#st.metric(...) shows a label with a big number underneath, like a dashboard stat card.


st.write(f"Sorted Mathematical Tuple: `{current_state}`")

# --- ENGINE MATHEMATICS IN ACTION ---
# Calculate values using our engine backend
nim_value = get_nim_value(current_state)

st.markdown(f"### Calculated Nim-Value: `{nim_value}`")

if nim_value == 0:
    st.error("🔴 **Status: P-Position (Losing)**. If you make a move from here, a perfect opponent will win.")
else:
    st.success("🟢 **Status: N-Position (Winning)**. There is a guaranteed winning move available!")
    
# st.error draws a red box and st.success draws a green one. The **...** makes text bold.

st.divider()

# --- INTERACTIVE AI BOT OPPONENT ---
st.subheader("Ask the Math Engine for the Perfect Move")
st.write("Click the button below to have the backend engine look ahead and calculate the perfect game-theoretic move.")

if st.button("Calculate Optimal Move"):
    # Check if the game is already completely over
    if sum(current_state) == 0:
        st.warning("The game is already over! All heaps are empty.")
    else:
        best_move = find_best_move(current_state)
        
        st.markdown("### Recommended Strategy:")
        st.info(f"You should change the board state from `{current_state}` to **`{best_move}`**.")
        st.write("This safely hands your opponent a Nim-Value of `0`, leaving them in a mathematically forced losing cycle.")
