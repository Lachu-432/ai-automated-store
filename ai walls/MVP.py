import streamlit as st
import speech_recognition as sr
import json
import sqlite3
import os
from gtts import gTTS
from googletrans import Translator
import streamlit as st
import re

# Translation Map for UI elements
language_map = {
    "en": {
        "title": "🛒 AI Shopping Assistant",
        "lang_select": "Select Language",
        "voice_command": "🎙 Voice Command",
        "start_listening": "🎤 Start Listening",
        "browse_category": "📂 Browse by Category",
        "select_from_list": "📋 Select from List",
        "product_found": "Product found: ",
        "product_not_found": "No matching product found. Try again.",
        "category_found": "Category found: ",
        "no_products_in_category": "No products found in this category.",
        "hear_about": "🔊 Hear about",
        "warning": "Warning",
        "timeout_error": "Timeout: No speech detected. Please try again.",
        "unknown_error": "Could not understand the audio. Please try again.",
        "speech_rec_error": "Speech Recognition service is unavailable. Try later.",
        "choose_product": "Choose a product",
        "weather_recommendations": "🌦 Weather-Based Recommendations",
         "weather_recommendations": "🌦 Weather-Based Recommendations",
        "past_purchases": "🛒 Because You Previously Bought…",
        "Available product in store(select_from_list)": "Available products in store (select from list)",
        "choose_product": "Choose a product" # ✅ Added this line
    },
    "ta": {
        "title": "🛒 செயற்கை நன்கு வாங்க உதவி",
        "lang_select": "மொழியை தேர்ந்தெடு",
        "voice_command": "🎙 குரல் கட்டளை",
        "start_listening": "🎤 கேட்க துவங்கு",
        "browse_category": "📂 பிரிவைப் பார்க்க",
        "select_from_list": "📋 பட்டியலில் இருந்து தேர்ந்தெடுக்கவும்",
        "product_found": "பொருள் கண்டுபிடிக்கப்பட்டது: ",
        "product_not_found": "ஒத்து பொருள் கண்டறியவில்லை. மறுபடி முயற்சிக்கவும்.",
        "category_found": "பிரிவு கண்டுபிடிக்கப்பட்டது: ",
        "no_products_in_category": "இந்த பிரிவில் எந்தப் பொருட்களும் கிடைக்கவில்லை.",
        "hear_about": "🔊 இதைப் பற்றி கேளுங்கள்",
        "warning": "எச்சரிக்கை",
        "timeout_error": "தடை: பேசுவது கண்டறியப்படவில்லை. தயவுசெய்து மீண்டும் முயற்சிக்கவும்.",
        "unknown_error": "ஒலியை புரிந்து கொள்ள முடியவில்லை. தயவுசெய்து மீண்டும் முயற்சிக்கவும்.",
        "speech_rec_error": "குரல் அங்கீகாரம் சேவை கிடைக்கவில்லை. பிறகு முயற்சிக்கவும்.",
        "choose_product": "பொருளை தேர்வு செய்யவும்",
        "weather_recommendations": "🌦 வானிலை அடிப்படையிலான பரிந்துரைகள்",
        "weather_recommendations": "🌦 காலநிலை அடிப்படையிலான பரிந்துரைகள்",
        "past_purchases": "🛒 நீங்கள் முன்பு வாங்கியது காரணமாக…",
        "title": "🛒 செயற்கை நன்கு வாங்க உதவி",
        "add_to_cart": "🛒 வண்டியில் சேர்க்க",  # ✅ Added this
        "choose_product": "ஒரு பொருளை தேர்ந்தெடுக்கவும்",  # Tamil (example)
        "choose_product": "ஒரு பொருளை தேர்ந்தெடுக்கவும்",  # ✅ Added this line
        "Available product in store(select_from_list)": "கடை உள்ள பொருட்கள் (பட்டியலில் இருந்து தேர்ந்தெடுக்கவும்)",
       "Available product in store(select_from_list)": "கடை உள்ள பொருட்கள் (பட்டியலில் இருந்து தேர்ந்தெடுக்கவும்)"  # Existing keys...
    },
    "hi": {
        "title": "🛒 एआई शॉपिंग सहायक",
        "lang_select": "भाषा चुनें",
        "voice_command": "🎙 आवाज़ आदेश",
        "start_listening": "🎤 सुनना शुरू करें",
        "browse_category": "📂 श्रेणी ब्राउज़ करें",
        "select_from_list": "📋 सूची से चुनें",
        "product_found": "उत्पाद पाया गया: ",
        "product_not_found": "कोई मेल खाने वाला उत्पाद नहीं मिला। कृपया फिर से प्रयास करें।",
        "category_found": "श्रेणी पाई गई: ",
        "no_products_in_category": "इस श्रेणी में कोई उत्पाद नहीं मिला।",
        "hear_about": "🔊 इसके बारे में सुनें",
        "warning": "चेतावनी",
        "timeout_error": "समय समाप्त: कोई आवाज़ नहीं मिली। कृपया फिर से प्रयास करें।",
        "unknown_error": "आवाज़ को समझा नहीं जा सका। कृपया फिर से प्रयास करें।",
        "speech_rec_error": "स्पीच रिकग्निशन सेवा उपलब्ध नहीं है। बाद में प्रयास करें।",
        "choose_product": "उत्पाद चुनें",
        "weather_recommendations": "🌦 मौसम-आधारित अनुशंसाएँ",
        "weather_recommendations": "🌦 मौसम आधारित सिफारिशें",
        "past_purchases": "🛒 क्योंकि आपने पहले खरीदा था…",
        "add_to_cart": "🛒 कार्ट में जोड़ें",
          "title": "🛒 एआई शॉपिंग सहायक",
        "add_to_cart": "🛒 कार्ट में जोड़ें",  # ✅ Added this
        "choose_product": "एक उत्पाद चुनें",  # Hindi (example)
        "choose_product": "एक उत्पाद चुनें",# ✅ Added this line
        "Available product in store(select_from_list)": "स्टोर में उपलब्ध उत्पाद (सूची से चुनें)"
        
        }
}

# Load Store Data
def load_store_data():
    try:
        with open("store_data.json", "r", encoding="utf-8") as file:
            return json.load(file)
    except Exception as e:
        st.error(f"Error loading store data: {e}")
        return {}

# Speak Text in Selected Language
# Speak Text in Selected Language (Fixed)
def speak_text(text, language="en"):
    try:
        # Map language to gTTS-supported codes
        gtts_languages = {"en": "en", "ta": "ta", "hi": "hi"}
        lang_code = gtts_languages.get(language, "en")  # Default to English if unsupported

        tts = gTTS(text=text, lang=lang_code)
        tts.save("output.mp3")

        # Ensure the file is properly read before passing to Streamlit
        with open("output.mp3", "rb") as audio_file:
            st.audio(audio_file, format="audio/mp3")

    except Exception as e:
        st.error(f"Error in Text-to-Speech: {e}")


# Recognize Speech
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("🎙 Listening... Please speak now.")
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=8)
            command = recognizer.recognize_google(audio)
            return command.lower()
        except sr.WaitTimeoutError:
            return language_map[selected_language]["timeout_error"]
        except sr.UnknownValueError:
            return language_map[selected_language]["unknown_error"]
        except sr.RequestError:
            return language_map[selected_language]["speech_rec_error"]

# Translate Text
translator = Translator()
def translate_text(text, lang):
    try:
        return translator.translate(text, dest=lang).text
    except Exception as e:
        return f"Translation Error: {e}"
# Fetch Weather Data & Recommend Products
def get_weather_recommendations():
    API_KEY = "your_api_key"  # Replace with your OpenWeatherMap API Key
    CITY = "your_city"  # Set your city
    weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"

    try:
        response = requests.get(weather_url).json()
        weather_condition = response["weather"][0]["main"].lower()

        recommendations = {
            "clear": ["Sunglasses", "Cold Drinks", "Ice Cream"],
            "rain": ["Umbrella", "Raincoat", "Hot Tea"],
            "snow": ["Gloves", "Soup", "Heater"],
            "clouds": ["Coffee", "Snacks"],
        }

        return recommendations.get(weather_condition, ["No special recommendations"])
    except:
        return ["SUMMER : Try products like Sunscreen, Cooling Towels, Fresh Juices, and Sunglasses."]
    # Store & Retrieve User Search History
def init_db():
    conn = sqlite3.connect("user_data.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS search_history (product TEXT)")
    conn.commit()
    return conn, cursor

def save_search(product):
    conn, cursor = init_db()
    cursor.execute("INSERT INTO search_history VALUES (?)", (product,))
    conn.commit()
    conn.close()

def get_past_recommendations():
    conn, cursor = init_db()
    cursor.execute("SELECT product FROM search_history ORDER BY ROWID DESC LIMIT 3")
    past_searches = cursor.fetchall()
    conn.close()

    recommended_items = {
        "bread": ["Butter", "Jam"],
        "milk": ["Cereal", "Chocolate Syrup"],
        "pasta": ["Tomato Sauce", "Cheese"]
    }

    suggestions = []
    for search in past_searches:
        product = search[0]
        suggestions.extend(recommended_items.get(product, []))

    return suggestions if suggestions else ["No past recommendations"]


# Initialize Database
def init_db():
    conn = sqlite3.connect("user_data.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS search_history (product TEXT)")
    conn.commit()
    return conn, cursor

def find_item_details(item_name, store_data):
    """
    Searches for an item in the store data and returns its details.
    :param item_name: The name of the item to search for.
    :param store_data: The dictionary containing store items and their details.
    :return: Dictionary containing item details if found, else an empty dictionary.
    """
    item_name_lower = item_name.strip().lower()
    
    # Search for the item in store_data
    for item, details in store_data.items():
        if item.strip().lower() == item_name_lower:
            return {item: details}
    
    return {}  # Return empty dictionary if no match is found
# Initialize Cart
if "cart" not in st.session_state:
    st.session_state.cart = []



# Save Search History
def save_search(product):
    conn, cursor = init_db()
    cursor.execute("INSERT INTO search_history VALUES (?)", (product,))
    conn.commit()
    conn.close()
    # Initialize session state for the shopping cart
if "shopping_cart" not in st.session_state:
    st.session_state.shopping_cart = []

# Function to add items to the cart
def add_to_cart(product):
    if product not in st.session_state.shopping_cart:
        st.session_state.shopping_cart.append(product)
        st.success(f"{product} added to cart!")
    else:
        st.warning(f"{product} is already in the cart.")

# Display cart contents
def show_cart():
    st.sidebar.header("🛒 Shopping Cart")
    if st.session_state.shopping_cart:
        for item in st.session_state.shopping_cart:
            st.sidebar.write(f"- {item}")
    else:
        st.sidebar.write("Your cart is empty.")
        # Initialize User Database
def init_user_db():
    conn = sqlite3.connect("user_data.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE,
            password TEXT
        )
    """)
    conn.commit()
    return conn, cursor

# Function to register a new user
def register_user(email, password):
    conn, cursor = init_user_db()
    try:
        cursor.execute("INSERT INTO users (email, password) VALUES (?, ?)", (email, password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False  # Email already exists
    finally:
        conn.close()

# Function to authenticate user
def authenticate_user(email, password):
    conn, cursor = init_user_db()
    cursor.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, password))
    user = cursor.fetchone()
    conn.close()
    return user is not None  # Returns True if user exists


# Load Store Data at the beginning
store_data = load_store_data()

# Streamlit UI
# Language Selection
language = st.sidebar.radio("Choose Language:", ["English", "தமிழ் (Tamil)", "हिन्दी (Hindi)"])

# Mapping User's language selection to language code
language_map_reverse = {"English": "en", "தமிழ் (Tamil)": "ta", "हिन्दी (Hindi)": "hi"}
selected_language = language_map_reverse[language]

# Display UI Elements
st.sidebar.header(language_map[selected_language]["lang_select"])

# Title
st.title(language_map[selected_language]["title"])

# Voice Command
st.header(language_map[selected_language]["voice_command"])
if st.button(language_map[selected_language]["start_listening"]):
    command = recognize_speech()
    st.write("You said:", command)

    if command and "timeout" not in command.lower() and "could not understand" not in command.lower():
        item_details = find_item_details(command, store_data)
    else:
        item_details = {}

    if not item_details:
        st.warning(language_map[selected_language]["product_not_found"])
    else:
        for item, details in item_details.items():
            translated_item = translate_text(item.capitalize(), selected_language)
            st.subheader(f"🛒 {translated_item}")

            explanation = f"{translated_item} details:\n"
            for key, value in details.items():
                translated_key = translate_text(key.capitalize(), selected_language)
                translated_value = translate_text(str(value), selected_language)
                st.write(f"**{translated_key}**: {translated_value}")
                explanation += f"{translated_key}: {translated_value}\n"

            save_search(item)

            if st.checkbox(f"{language_map[selected_language]['hear_about']} {translated_item}", key=item):
                speak_text(explanation, selected_language)

# Category Buttons
# Category Selection - Show Only Product Names
st.header(language_map[selected_language]["browse_category"])
category_list = ["Vegetables", "Fruits", "Dairy", "Cars", "Dress", "Bikes", "Sports"]

selected_category = st.radio("Choose a category:", category_list)

if selected_category:
    category_lower = selected_category.lower()
    category_items = [
        item for item, details in store_data.items() 
        if details.get("category", "").strip().lower() == category_lower
    ]

    if not category_items:
        st.warning(language_map[selected_language]["no_products_in_category"])

    else:
        st.subheader("Available Products:")
        selected_product_from_category = st.selectbox("Choose a product", ["Select"] + category_items)

        if selected_product_from_category != "Select":
            product_details = store_data[selected_product_from_category]

            translated_product = translate_text(selected_product_from_category.capitalize(), selected_language)
            st.subheader(f"🛒 {translated_product}")

            explanation = f"{translated_product} details:\n"
            for key, value in product_details.items():
                translated_key = translate_text(key.capitalize(), selected_language)
                translated_value = translate_text(str(value), selected_language)
                if st.button(f"{translated_key}: {translated_value}", key=f"{selected_product_from_category}_{key}"):
                    st.write(f"**{translated_key}**: {translated_value}")

                explanation += f"{translated_key}: {translated_value}\n"

            save_search(selected_product_from_category)

            if st.checkbox(f"{language_map[selected_language]['hear_about']} {translated_product}", key=selected_product_from_category):
                speak_text(explanation, selected_language)


# Product Selection Dropdown
# Product Selection Dropdown
st.header(language_map[selected_language]["Available product in store(select_from_list)"])
selected_product = st.selectbox(language_map[selected_language]["choose_product"], ["Select"] + list(store_data.keys()))


if selected_product != "Select":
    if selected_product in store_data:
        product_details = store_data[selected_product]

        translated_product = translate_text(selected_product.capitalize(), selected_language)
        st.subheader(f"🛒 {translated_product}")

        explanation = f"{translated_product} details:\n"
        for key, value in product_details.items():
            translated_key = translate_text(key.capitalize(), selected_language)
            translated_value = translate_text(str(value), selected_language)
            # Create separate buttons for each property
            if st.button(f"{translated_key}: {translated_value}", key=f"{selected_product}_{key}"):
                st.write(f"**{translated_key}**: {translated_value}")

            explanation += f"{translated_key}: {translated_value}\n"

        save_search(selected_product)

        if st.checkbox(f"{language_map[selected_language]['hear_about']} {translated_product}", key=selected_product):
            speak_text(explanation, selected_language)
            # Initialize session state for login
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_email = ""


            

# Weather-Based Recommendations
st.header(language_map[selected_language]["weather_recommendations"])
weather_recommendations = get_weather_recommendations()
st.write(", ".join(weather_recommendations))

#past purchase recommendations
st.header(language_map[selected_language]["past_purchases"])
past_recommendations = get_past_recommendations()
st.write(", ".join(past_recommendations))


# Example product selection (Replace with actual product selection logic)
st.header(language_map[selected_language].get("add_to_cart", "🛒 Add to Cart"))



# Localized text for "Choose a product" and "Select"
choose_product_text = language_map[selected_language]["choose_product"]
select_text = "Select"  

# Translate "Select" based on the selected language
if selected_language == "ta":
    select_text = "தேர்ந்தெடு"
elif selected_language == "hi":
    select_text = "चुनें"

# Ensure category-based product filtering works
if selected_category:
    category_lower = selected_category.lower()
    category_items = [item for item, details in store_data.items() if details.get("category", "").strip().lower() == category_lower]
else:
    category_items = list(store_data.keys())  # Show all products if no category is selected

# Create product selection dropdown with translated labels
selected_product_to_add = st.selectbox(
    choose_product_text,  # Use translated "Choose a product"
    [select_text] + category_items,  # Use translated "Select" & filtered category items
    key="add_cart_dropdown"
)

# Button to add selected product to the cart
if selected_product_to_add != select_text:  # Prevent adding "Select" option to cart
    st.button("Add to Cart", on_click=add_to_cart, args=(selected_product_to_add,))

# Show the shopping cart in the sidebar
show_cart()

# Function to validate email format
def is_valid_email(email):
    email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(email_regex, email)

with st.sidebar:
    st.subheader("🔑 User Login")

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        email = st.text_input("📧 Email", key="login_email")
        password = st.text_input("🔒 Password", type="password", key="login_password")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("Login", key="login_button"):
                if not email or not is_valid_email(email):
                    st.error("❌ Invalid email format! Please enter a valid email.")
                elif authenticate_user(email, password):
                    st.session_state.logged_in = True
                    st.session_state.user_email = email
                    st.success("✅ Login Successful!")
                else:
                    st.error("❌ Invalid email or password!")

        with col2:
            if st.button("Register", key="register_button"):
                if not email or not is_valid_email(email):
                    st.error("❌ Invalid email format! Please enter a valid email.")
                elif register_user(email, password):
                    st.success("✅ Registration Successful! Please login.")
                else:
                    st.error("❌ Email already exists!")

    else:
        st.success(f"✅ Logged in as {st.session_state.user_email}")
        if st.button("Logout", key="logout_button"):
            st.session_state.logged_in = False
            st.session_state.user_email = ""
            st.warning("🚪 Logged out successfully.")