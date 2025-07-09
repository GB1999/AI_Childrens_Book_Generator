📚 AI Storybook Generator
A personal project showcasing the creative potential of generative AI to produce illustrated storybooks, complete with AI-generated text, images, audio, and video. This project brings together multiple AI models into a cohesive storytelling pipeline.

🎥 Watch the development journey: YouTube Video

🧠 What It Does
This project generates a short illustrated story using:

✍️ Text generation (e.g. via OpenAI or HuggingFace models)

🎨 AI-generated images per scene

🔊 Voice-over narration using text-to-speech

📹 Automated video assembly that brings the book to life

Each story is saved in a structured folder with:

Generated text (JSON format)

Scene images

Audio clips

Final assembled video

🗂 Project Structure
graphql
Copy
Edit
bookGenerator-master/
│
├── main.py                 # Entry point: runs story, image, and video generation
├── story_generator.py      # Handles story creation and structure
├── audio_generator.py      # Uses TTS to narrate scenes
├── video_generator.py      # Assembles scenes, audio, and visuals into a video
├── imageToSave.png         # Example image output
├── config.json             # Configuration for story themes and paths
├── .idea/                  # Project metadata (IDE-specific)
└── README.md               # ← You’re here!
🛠️ Requirements
Python 3.8+

torch, torchaudio

transformers

Tortoise TTS

FFmpeg (for video generation)

To install dependencies:

bash
Copy
Edit
pip install torch torchaudio transformers
Install FFmpeg and ensure it’s in your system path.

🚀 Usage
Clone the repo and extract:

bash
Copy
Edit
unzip bookGenerator-master.zip
cd bookGenerator-master
Run the generator:

bash
Copy
Edit
python main.py
Outputs will be created under a /Stories/ folder with images, narration, and a video.

Note: Paths are currently hardcoded in main.py and may need to be adjusted based on your environment.

🧪 Demo Output
Here’s a preview of the end-to-end experience, showing AI generating a storybook from scratch and assembling it into video format:

📺 Watch here

✨ Why This Exists
This project was built as a creative coding experiment to explore how far generative AI can go in telling stories. It demonstrates the pipeline from text → image → audio → video, using open-source models and tools.
