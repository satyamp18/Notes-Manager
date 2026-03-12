import streamlit as st
import json
import os
from datetime import datetime

FILE = "notes.json"

# Load notes
def load_notes():
    if os.path.exists(FILE):
        with open(FILE, "r") as f:
            return json.load(f)
    return []

# Save notes
def save_notes(notes):
    with open(FILE, "w") as f:
        json.dump(notes, f, indent=4)

notes = load_notes()

st.title("📝 Smart Notes Manager")

# Sidebar
menu = st.sidebar.selectbox(
    "Menu",
    ["Add Note", "View Notes", "Search Notes"]
)

# ---------------- ADD NOTE ----------------

if menu == "Add Note":

    st.subheader("Add a New Note")

    title = st.text_input("Title")
    content = st.text_area("Write your note")

    if st.button("Save Note"):
        if title and content:
            new_note = {
                "title": title,
                "content": content,
                "date": datetime.now().strftime("%Y-%m-%d %H:%M")
            }

            notes.append(new_note)
            save_notes(notes)

            st.success("Note saved successfully!")
            st.rerun()

        else:
            st.warning("Title and note cannot be empty")

# ---------------- VIEW NOTES ----------------

elif menu == "View Notes":

    st.subheader("Your Notes")

    if not notes:
        st.info("No notes available")

    for i, note in enumerate(notes):

        with st.expander(f"{note['title']}  ({note['date']})"):

            st.write(note["content"])

            col1, col2 = st.columns(2)

            # Delete
            if col1.button("Delete", key=f"del{i}"):

                notes.pop(i)
                save_notes(notes)

                st.success("Note deleted")
                st.rerun()

            # Edit
            if col2.button("Edit", key=f"edit{i}"):

                st.session_state["edit_index"] = i
                st.session_state["edit_mode"] = True

# ---------------- EDIT NOTE ----------------

if st.session_state.get("edit_mode"):

    idx = st.session_state["edit_index"]
    note = notes[idx]

    st.subheader("Edit Note")

    new_title = st.text_input("Title", note["title"])
    new_content = st.text_area("Content", note["content"])

    if st.button("Update Note"):

        notes[idx]["title"] = new_title
        notes[idx]["content"] = new_content

        save_notes(notes)

        st.success("Note updated!")

        st.session_state["edit_mode"] = False
        st.rerun()

# ---------------- SEARCH ----------------

elif menu == "Search Notes":

    st.subheader("Search Notes")

    query = st.text_input("Search")

    if query:

        results = [
            note for note in notes
            if query.lower() in note["title"].lower()
            or query.lower() in note["content"].lower()
        ]

        if results:
            for note in results:

                st.write(f"### {note['title']}")
                st.write(note["content"])
                st.caption(note["date"])

        else:
            st.warning("No notes found")