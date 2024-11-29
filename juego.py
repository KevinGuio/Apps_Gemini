import streamlit as st
import re
import random

# Word lists
word_categories = {
    "Animals": ["elephant", "giraffe", "leopard", "penguin", "dolphin"],
    "Countries": ["france", "brazil", "canada", "japan", "mexico"],
    "Programming": ["python", "javascript", "golang", "kotlin", "swift"]
}

def generate_regex_challenge():
    """Generate a regex challenge based on word characteristics."""
    category = random.choice(list(word_categories.keys()))
    words = word_categories[category]
    target_word = random.choice(words)
    
    challenges = [
        {
            "description": f"Find a word with exactly {len(target_word)} letters",
            "regex": f"^.{{{len(target_word)}}}$"
        },
        {
            "description": f"Find a word starting with '{target_word[0]}'",
            "regex": f"^{target_word[0]}.*"
        },
        {
            "description": f"Find a word ending with '{target_word[-1]}'",
            "regex": f".*{target_word[-1]}$"
        },
        {
            "description": f"Find a word containing '{target_word[1:-1]}'",
            "regex": f".*{target_word[1:-1]}.*"
        }
    ]
    
    challenge = random.choice(challenges)
    return {
        "category": category,
        "words": words,
        "target_word": target_word,
        "challenge": challenge
    }

def check_regex_match(regex, words):
    """Check how many words match the given regex."""
    matches = [word for word in words if re.match(regex, word)]
    return matches

def app():
    st.title("🧩 Regex Word Guessing Game")
    
    # Initialize or retrieve game state
    if 'game' not in st.session_state:
        st.session_state.game = generate_regex_challenge()
        st.session_state.attempts = 0
        st.session_state.solved = False
    
    game = st.session_state.game
    
    # Display challenge
    st.write(f"Category: {game['category']}")
    st.write(f"Challenge: {game['challenge']['description']}")
    
    # User input for regex
    user_regex = st.text_input("Enter your Regex pattern:")
    
    if st.button("Check Regex"):
        try:
            matches = check_regex_match(user_regex, game['words'])
            
            if game['target_word'] in matches:
                st.success(f"🎉 Congratulations! You found the target word: {game['target_word']}")
                st.session_state.solved = True
            else:
                st.warning(f"Not quite! Matches: {matches}")
            
            st.session_state.attempts += 1
        
        except re.error:
            st.error("Invalid Regular Expression!")
    
    if st.button("New Challenge"):
        st.session_state.game = generate_regex_challenge()
        st.session_state.attempts = 0
        st.session_state.solved = False
        st.experimental_rerun()
    
    # Show stats
    st.write(f"Attempts: {st.session_state.attempts}")

if __name__ == "__main__":
    app()
