import asyncio
from textual.app import ComposeResult
from textual.containers import VerticalScroll, Container
from textual.widgets import Input, Button, OptionList, Static
import json
import torch
import google.generativeai as gemai
from youtube_search import YoutubeSearch
from youtube_transcript_api import YouTubeTranscriptApi
from transformers import AutoModelForSequenceClassification, AutoTokenizer
from fincept_terminal.FinceptSettingModule.FinceptTerminalSettingUtils import get_settings_path

SETTINGS_FILE = get_settings_path()

# ✅ Load RoBERTa Model & Tokenizer



class YouTubeTranscriptApp(Container):
    """Textual App to search YouTube videos, fetch transcripts, and analyze sentiment."""
    tokenizer = AutoTokenizer.from_pretrained("cardiffnlp/twitter-roberta-base-sentiment")
    model = AutoModelForSequenceClassification.from_pretrained("cardiffnlp/twitter-roberta-base-sentiment")

    def compose(self) -> ComposeResult:
        """Compose the UI layout."""
        yield Static("🔎 Enter Search Keyword:", id="search_label")
        yield Input(placeholder="Enter keyword...", id="search_input")
        yield Button("Search", id="search_button", variant="primary")

        yield Static("🎥 Select a Video:", id="video_label", classes="hidden")
        yield OptionList(id="video_list")

        with VerticalScroll(id="analysis_results", classes="analysis_results"):
            yield Static("Transcript", id="transcript_label", classes="hidden")
            yield Static("", id="transcript_display")

            yield Static("Sentiment Analysis", id="sentiment_label", classes="hidden")
            yield Static("", id="sentiment_display")

    def on_button_pressed(self, event: Button.Pressed):
        """Handle button press events."""
        if event.button.id == "search_button":
            search_input = self.query_one("#search_input", Input)
            search_query = search_input.value.strip()
            if search_query:
                asyncio.create_task(self.fetch_videos(search_query))
            else:
                self.app.notify("⚠ Please enter a search keyword!", severity="warning")

    async def fetch_videos(self, search_query):
        """Fetch YouTube videos based on search query and update the option list."""
        self.app.notify("🔍 Searching YouTube... Please wait.", severity="information")
        video_list_widget = self.query_one("#video_list", OptionList)
        video_list_widget.clear_options()

        try:
            # ✅ Fetch YouTube results
            results = await asyncio.to_thread(YoutubeSearch, search_query, max_results=15)
            results = results.to_json()
            video_data = json.loads(results)["videos"]

            # ✅ Filter videos less than 3 minutes
            filtered_videos = [
                {"id": video["id"], "title": video["title"]}
                for video in video_data if self.duration_to_seconds(video.get("duration", "0")) < 180
            ]

            if not filtered_videos:
                self.app.notify("⚠ No short videos found under 3 minutes!", severity="warning")
                return

            # ✅ Show the video list UI component
            self.query_one("#video_label", Static).remove_class("hidden")

            # ✅ Populate the video list
            for video in filtered_videos:
                video_list_widget.add_option(f"{video['title']} ({video['id']})")

            self.app.notify(f"✅ Found {len(filtered_videos)} short videos!", severity="success")

        except Exception as e:
            self.app.notify(f"❌ Error fetching videos: {e}", severity="error")

    async def on_option_list_option_selected(self, event: OptionList.OptionSelected):
        """Fetch transcript when a video is selected."""
        selected_option = event.option.prompt  # ✅ Get video ID directly from OptionList
        video_id = selected_option.split("(")[-1].strip(")")

        self.app.notify(f"📜 Fetching transcript for Video ID: {video_id}...", severity="information")
        # ✅ Fetch transcript asynchronously
        transcript_text = await asyncio.create_task(self.get_transcript(video_id))

        # ✅ Display transcript using the new method
        self.display_transcript(transcript_text)

        # ✅ Call Sentiment Analysis on the transcript
        await asyncio.create_task(self.display_sentiment_report(transcript_text))

    def display_transcript(self, transcript_text):
        """Handles displaying the transcript UI."""
        self.query_one("#transcript_label", Static).remove_class("hidden")

        # ✅ Update transcript display
        transcript_display = self.query_one("#transcript_display", Static)
        transcript_display.update(transcript_text)

    async def get_transcript(self, video_id):
        """Fetch transcript for a given video ID with enhanced error handling."""
        try:
            # ✅ Fetch transcript asynchronously using a thread
            transcript_data = await asyncio.to_thread(YouTubeTranscriptApi.get_transcript, video_id)

            if not transcript_data:
                self.app.notify("⚠ No transcript data found.", severity="warning")
                return "⚠ Transcript not available."

            # ✅ Convert transcript list to readable text
            transcript_text = " ".join(entry["text"] for entry in transcript_data)
            self.app.notify("✅ Transcript fetched successfully!", severity="success")
            return transcript_text

        except Exception as e:
            # ✅ Catch unexpected errors and notify user
            self.app.notify(f"⚠ Error fetching transcript: {e}", severity="error")
            return "⚠ Transcript not available."

    async def display_sentiment_report(self, text):
        """Perform sentiment analysis and display the results."""
        if not text:
            self.app.notify("⚠ No transcript available for sentiment analysis.", severity="warning")
            return

        # ✅ Run Sentiment Analysis
        sentiment_report = await asyncio.create_task(self.analyze_sentiment(text))

        # ✅ Show sentiment analysis UI component
        self.query_one("#sentiment_label", Static).remove_class("hidden")

        # ✅ Update sentiment display
        sentiment_display = self.query_one("#sentiment_display", Static)
        sentiment_display.update(
            f"🔹 **Sentiment:** {sentiment_report['sentiment']} \n"
            f"🔹 **Confidence:** {sentiment_report['confidence']:.2f} \n\n"
            f"🔹 **Detailed Analysis:** \n{sentiment_report['gemini_report']}"
        )

    async def analyze_sentiment(self, text):
        """Perform sentiment analysis using RoBERTa and Gemini AI."""
        if not text:
            return {"error": "No text provided for sentiment analysis"}

        # ✅ Step 1: Run RoBERTa for Sentiment Prediction
        try:
            inputs = self.tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=512)
            with torch.no_grad():
                outputs = self.model(**inputs)
            scores = outputs.logits.softmax(dim=1).tolist()[0]
            labels = ["Negative", "Neutral", "Positive"]
            sentiment = labels[scores.index(max(scores))]
            confidence = max(scores)
        except Exception as e:
            return {"error": "RoBERTa sentiment analysis failed"}

        # ✅ Step 2: Generate Detailed Report using Gemini AI
        api_key = self.fetch_gemini_api_key()
        if not api_key:
            return {"sentiment": sentiment, "confidence": confidence, "gemini_report": "⚠ Gemini AI Key missing."}

        gemai.configure(api_key=api_key)
        try:
            model = gemai.GenerativeModel("gemini-1.5-flash")
            prompt = f"""
            Perform a detailed sentiment analysis of the following text: 
            "{text}"
            Include sentiment classification, reasoning, tone, and emotional indicators.
            """
            response = await asyncio.to_thread(model.generate_content, prompt)
            gemini_report = response.text
        except Exception as e:
            gemini_report = "⚠ Gemini AI sentiment analysis failed."

        # ✅ Return Combined Sentiment Results
        return {
            "sentiment": sentiment,
            "confidence": confidence,
            "gemini_report": gemini_report
        }

    def fetch_gemini_api_key(self):
        """Fetch Gemini API Key from settings.json file."""

        try:
            with open(SETTINGS_FILE, "r") as f:
                settings = json.load(f)

            # ✅ Navigate to the correct API key location
            api_key = settings.get("data_sources", {}).get("genai_model", {}).get("apikey", None)

            if not api_key:
                self.app.notify("⚠ Gemini API Key not found in settings.", severity="warning")
                return None

            self.app.notify("✅ Gemini API Key retrieved successfully!", severity="information")
            return api_key

        except Exception as e:
            self.app.notify(f"❌ Unexpected error: {e}", severity="error")
            return None

    def duration_to_seconds(self, duration):
        """Convert duration string (MM:SS) to seconds, handling possible integer values."""
        if isinstance(duration, int):
            return duration  # Already in seconds

        if not isinstance(duration, str):
            return 0  # Handle unexpected format

        parts = duration.split(":")
        if len(parts) == 2:
            minutes, seconds = map(int, parts)
            return minutes * 60 + seconds
        return int(parts[0]) if parts[0].isdigit() else 0
