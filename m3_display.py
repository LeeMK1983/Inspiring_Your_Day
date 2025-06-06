import tkinter as tk # tkinter and ttk are for building the GUI
from tkinter import ttk
from m1_keyword_scoring import mood_keywords, task_keywords, goal_keywords, FALLBACKS, map_input_to_keyword, fuzzy_match_input, get_best_keyword
from m2_matching import load_quote_dataset, load_image_pool, select_relevant_quote, get_image_url, load_image_from_url
from m4_insight import generate_insight

# Main GUI Function _ This wraps the entire display logic -> It will be called from execution.py as the app entry point
def launch_gui():
    # Load quotes and images at the start of the app
    quotes = load_quote_dataset()
    image_pool = load_image_pool()

    # Set up main window
    root = tk.Tk()                   # .TK() _ Initializes the main application window
    root.title("Inspiring Your Day") # Set the title
    root.geometry("750x600")         # Set the dimensions (750px wide x 600px high) 

    # Input Fields Frame
    input_frame = tk.Frame(root)     # .Frame() _ A container for organizing widgets
    input_frame.pack(pady=10)        # .pack() _ add vertical spacing

    # Input Labels & Entry Boxes _ For each of the 3 user inputs, add a text label in the first column, add an input box (entry) in the second column
    # Mood input
    tk.Label(input_frame, text="How are you feeling today?").grid(row=0, column=0, sticky="w")
    mood_entry = tk.Entry(input_frame, width=50)
    mood_entry.grid(row=0, column=1)

    # task input
    tk.Label(input_frame, text="What's your main task today?").grid(row=1, column=0, sticky="w")
    task_entry = tk.Entry(input_frame, width=50)
    task_entry.grid(row=1, column=1)

    # goal input
    tk.Label(input_frame, text="What kind of person do you want to be?").grid(row=2, column=0, sticky="w")
    goal_entry = tk.Entry(input_frame, width=50)
    goal_entry.grid(row=2, column=1)

    # Quote Display Label
    # Display the matched quote
    # wraplength=600: wraps long quotes into multiple lines
    quote_title = tk.Label(root, text="Today's Quote", font=("Helvetica", 15, "bold"))
    quote_title.pack(pady=(20,0))
    quote_label = tk.Label(root, text="", wraplength=600, font=("Helvetica", 12), justify="center")
    quote_label.pack(pady=5)

    # Image Display _ A blank label to later hold the selected image which is dynamically updated
    image_title = tk.Label(root, text="Visual Inspiration", font=("Helvetica", 15, "bold"))
    image_title.pack(pady=(10,0))
    image_label = tk.Label(root)
    image_label.pack(pady=10)

    insight_title = tk.Label(root, text="Reflective Insight", font=("Hevetica", 15, "bold"))
    insight_title.pack(pady=(10.0))
    insight_label = tk.Label(root, text="", wraplength=600, font=("Hevetica", 12), fg="black")
    insight_label.pack(pady=5)

    # Placeholder for Tags: Holds the most recent tags, Used for regeneration if needed
    current_tags = []

    def generate_inspiration():
        nonlocal current_tags

        # Get mapped keywords or fallback
        mood = get_best_keyword(mood_entry.get(), mood_keywords, "mood")
        task = get_best_keyword(task_entry.get(), task_keywords, "task")
        goal = get_best_keyword(goal_entry.get(), goal_keywords, "goal")

        # Save those tags
        current_tags = [mood, task, goal] # Save those tags
        print("Currnet tags:", current_tags)

        # Selet quote based on tags
        quote = select_relevant_quote(current_tags, quotes)

        # Display the quote
        if quote:
            quote_label.config(text=f"{quote['quote']}")
            # Get image and show it
            mood_tag = mood # Use mood as image category
            print("Mood tag:", mood_tag)
            image_url = get_image_url(mood_tag, image_pool)
            print("image_url:", image_url)
            img = load_image_from_url(image_url)
            # Update the image widget
            if img:
                image_label.config(image=img)
                image_label.image = img # prevent garbage collection
            else:
                image_label.config(image="", text="Image unavailable")
        else:
            quote_label.config(text="No matching quote found.")
            image_label.config(image="", text="")
        
        # Show the insight
        insight_text = generate_insight(mood, task, goal)
        insight_label.config(text=insight_text)
    
    # Regeneration Function
    def regenerate_inspiration():
        generate_inspiration()
    
    # Action Buttons _ Horizontal frame with two buttons
    btn_frame = tk.Frame(root)
    btn_frame.pack(pady=20)

    ttk.Button(btn_frame, text="Generate Inspiration", command=generate_inspiration).grid(row=0, column=0, padx=10)
    ttk.Button(btn_frame, text="Regenerate", command=regenerate_inspiration).grid(row=0, column=1, padx=10)

    # Start the App
    root.mainloop()