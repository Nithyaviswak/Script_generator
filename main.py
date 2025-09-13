import ollama

story_history = []
character_bible = {}
genre = ""
tone = ""
writing_mode = "story"

def format_character_sheet(bible):
    if not bible:
        return "No characters defined yet."
    sheet = ""
    for name, desc in bible.items():
        sheet += f"- {name}: {desc}\n"
    return sheet

def update_character_bible():
    print("\n--- Character Bible Update ---")
    name = input("Enter character name: ")
    desc = input(f"Enter description for {name}: ")
    character_bible[name] = desc
    print(f"✅ Character '{name}' has been added/updated.")
    print("----------------------------\n")

def get_ai_contribution(current_story_text, user_input):
    if writing_mode == "script":
        rules = """
        **Screenwriting Rules:**
        - You must follow standard screenplay format.
        - **Scene Headings:** Use INT. or EXT. followed by the location and time of day.
        - **Character Cues:** Character names before dialogue should be in ALL CAPS.
        - **Dialogue:** Place dialogue directly under the character's name.
        - **Action Lines:** Describe actions and settings in the present tense.
        """
        response_type = "next part of the script"
    else:
        rules = """
        **Story Writing Rules:**
        - Write in a narrative, paragraph-based format.
        - Weave in descriptive language and character emotions.
        - Keep your response to a single, well-developed paragraph.
        """
        response_type = "next paragraph of the story"

    prompt_template = f"""
    You are "NarratorAI," an expert co-writer specializing in collaborative fiction and screenwriting.
    Your purpose is to help me, the Lead Author, write a compelling narrative.

    **Your Core Directives:**
    1.  **Adhere to the Genre and Tone:** All your contributions must match the established genre and tone.
    2.  **Maintain Consistency:** Ensure your writing is consistent with the plot and characters already established.
    3.  **Be Collaborative:** Build upon my ideas. Don't take over the story.
    4.  **Respond with Narrative Only:** Do not break character or add commentary.

    {rules}

    ---
    [STORY SETUP]
    Genre: {genre}
    Tone: {tone}
    Mode: {writing_mode}

    [CHARACTER BIBLE]
    {format_character_sheet(character_bible)}

    [STORY SO FAR]
    {current_story_text}

    [LEAD AUTHOR'S LATEST ENTRY]
    {user_input}
    ---

    Based on all the information above, write the {response_type} now:
    """
    
    print("\n🤖 Local LLM is thinking...")
    try:
        response = ollama.chat(
            model='llama3:8b',
            messages=[{'role': 'user', 'content': prompt_template}]
        )
        return response['message']['content']
    except Exception as e:
        return f"🚨 Error connecting to Ollama. Is the server running?\n   Details: {e}"

def main():
    global genre, tone, writing_mode

    print("📚 Welcome to the AI Story Room (Ollama Edition)! 📚")
    print("Let's write together. At any time, type:")
    print("  '!char' to add or update a character.")
    print("  '!quit' to end the session and print the story.")
    print("--------------------------------------------------\n")

    genre = input("First, what is the genre? (e.g., Sci-Fi, Fantasy, Mystery)\n> ")
    tone = input("And what is the tone? (e.g., Dark & Gritty, Humorous, Epic)\n> ")
    mode_choice = input("Are we writing a 'story' or a 'script'?\n> ").lower()
    if mode_choice == 'script':
        writing_mode = 'script'
    
    print(f"\nGreat! We're writing a {tone} {genre} {writing_mode}. Let's begin.")
    print("--------------------------------------------------\n")

    user_entry = input("Start us off with the first paragraph or scene:\n> ")
    story_history.append(user_entry + "\n\n")

    while True:
        if user_entry.lower() == '!quit':
            break
        if user_entry.lower() == '!char':
            update_character_bible()
            user_entry = input("Character Bible updated. Write your next part, or use another command:\n> ")
            continue

        full_story_text = "".join(story_history)
        
        ai_entry = get_ai_contribution(full_story_text, user_entry)
        
        print("\n--- 🤖 NarratorAI's Contribution ---\n")
        print(ai_entry)
        print("\n-------------------------------------\n")
        
        story_history.append(ai_entry + "\n\n")

        user_entry = input("Your turn. What happens next?\n> ")
        if user_entry.lower() != '!quit' and user_entry.lower() != '!char':
            story_history.append(user_entry + "\n\n")

    print("\n\n📜 --- YOUR FINAL MASTERPIECE --- 📜\n")
    final_story = "".join(story_history).replace(user_entry, "")
    print(final_story)
    print("\nThanks for writing with me!")

if __name__ == '__main__':
    main()