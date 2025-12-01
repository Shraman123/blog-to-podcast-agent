# 🎙 Blog to Podcast AI Agent

An end-to-end AI application that turns written blog posts into engaging audio podcasts. This tool utilizes multiple AI agents to scrape content, generate conversational summaries, and synthesize realistic speech.

## 🚀 Features
- *URL Scraping*: Extracts text content from any blog or article URL.
- *AI Summarization*: Converts technical or long-form content into a conversational podcast script.
- *Text-to-Speech*: Generates high-quality audio using ElevenLabs.
- *Audio Player*: Listen to the podcast directly in the browser or download the .wav file.

## 🛠 Tech Stack
- *Framework*: [Agno (formerly Phidata)](https://github.com/phidatahq/agno)
- *Frontend*: [Streamlit](https://streamlit.io/)
- *LLM*: OpenAI GPT-4o
- *Web Scraping*: Firecrawl
- *Audio Synthesis*: ElevenLabs

## ⚙ Prerequisites
To run this project, you need API keys from the following services:
1. *OpenAI API Key*: For summarizing the content.
2. *Firecrawl API Key*: For scraping the website.
3. *ElevenLabs API Key*: For generating the voice.

## 💻 Installation

1. *Clone the repository*
   ```bash
   git clone [https://github.com/Shraman123/blog-to-podcast-agent.git](https://github.com/Shraman123/blog-to-podcast-agent.git)
   cd blog-to-podcast-agent
