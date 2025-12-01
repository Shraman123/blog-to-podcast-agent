import os
import uuid
import streamlit as st
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.eleven_labs import ElevenLabsTools
from agno.tools.firecrawl import FirecrawlTools
from agno.utils.audio import write_audio_to_file

# Page Configuration
st.set_page_config(page_title="Blog to Podcast Agent")
st.title("Blog to podcast Agent")

# Sidebar for API Keys
st.sidebar.header("API Keys")
openai_api_key = st.sidebar.text_input("OpenAI API Key", type="password")
eleven_labs_api_key = st.sidebar.text_input("ElevenLabs API Key", type="password")
firecrawl_api_key = st.sidebar.text_input("Firecrawl API Key", type="password")

# Check if keys are provided
keys_provided = all([openai_api_key, eleven_labs_api_key, firecrawl_api_key])

# Main Interface
url = st.text_input("Enter the URL of the article")
generate_button = st.button("Generate Podcast", disabled=not keys_provided)

if not keys_provided:
    st.warning("Please enter all keys to proceed")

# Logic to run when button is clicked
if generate_button:
    if not url.strip():
        st.warning("Please enter a URL")
    else:
        # Set environment variables for the tools to use
        os.environ["OPENAI_API_KEY"] = openai_api_key
        os.environ["ELEVEN_LABS_API_KEY"] = eleven_labs_api_key
        os.environ["FIRECRAWL_API_KEY"] = firecrawl_api_key

        with st.spinner("Processing... Scraping blog, summarizing, and generating podcast..."):
            try:
                # Initialize the Agent
                blog_to_podcast_agent = Agent(
                    name="Blog to Podcast Agent",
                    model=OpenAIChat(id="gpt-4o"),
                    tools=[
                        ElevenLabsTools(model_id="eleven_multilingual_v2"),
                        FirecrawlTools()
                    ],
                    description="You are an AI agent that can generate audio using the ElevenLabs API.",
                    instructions=[
                        "When the user provides a blog post URL:",
                        "1. Use FirecrawlTools to scrape the blog content.",
                        "2. Create a concise summary of the blog content that is no more than 2000 characters.",
                        "3. Ensure the summary captures the main points while being engaging and conversational (like a podcast).",
                        "4. Use the ElevenLabsTools to convert the summary to audio.",
                        "Ensure the summary is within the 2000 character limit to avoid API limits."
                    ],
                    markdown=True,
                    debug_mode=True
                )

                # Run the agent
                podcast = blog_to_podcast_agent.run(f"Convert the blog content to a podcast: {url}")

                # Save and display audio
                # Check if audio exists in the response
                if hasattr(podcast, 'audio') and podcast.audio:
                    # Create directory if it doesn't exist
                    save_directory = "audio_generations"
                    os.makedirs(save_directory, exist_ok=True)
                    
                    # Generate unique filename
                    file_name = f"{save_directory}/podcast_{uuid.uuid4()}.wav"
                    
                    # Write audio to file (taking the first audio segment)
                    write_audio_to_file(audio=podcast.audio[0], filename=file_name)
                    
                    st.success("Podcast generated successfully!")
                    
                    # Display audio player
                    with open(file_name, "rb") as f:
                        audio_bytes = f.read()
                    
                    st.audio(audio_bytes, format="audio/wav")
                    
                    # Download button
                    st.download_button(
                        label="Download Podcast",
                        data=audio_bytes,
                        file_name="podcast.wav",
                        mime="audio/wav"
                    )
                else:
                    st.error("No audio was generated. Please try again or check the logs.")

            except Exception as e:
                st.error(f"An error occurred: {e}")