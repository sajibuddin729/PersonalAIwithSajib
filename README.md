# PersonalAI

![AI Study Tool Banner](/placeholder.svg?height=200&width=600)

An AI-powered educational content processor that automatically generates summaries, flashcards, quizzes, and answers questions about your study materials.

## 🚀 Features

- **Multi-format Content Processing**
  - 📄 PDF documents
  - 🎥 YouTube video transcripts
  - 📝 Direct text input

- **AI-Generated Study Materials**
  - 📋 Smart summaries of content
  - 🗂️ Interactive flashcards with difficulty levels
  - 📝 Multiple-choice quizzes with explanations
  - 💬 Q&A system for content-specific questions

- **Data Visualization**
  - 📊 Key term frequency charts
  - 📈 Content analysis visualizations

## 📋 Requirements

- Python 3.8+
- Django 4.2+
- OpenAI API key
- Other dependencies listed in `requirements.txt`

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/ai-study-tool.git
   cd ai-study-tool

2. **Create a virtual environment**

```shellscript
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```


3. **Install dependencies**

```shellscript
pip install -r requirements.txt
```


4. **Set up environment variables**
Create a `.env` file in the project root:

```plaintext
SECRET_KEY=your-secret-key-here
OPENAI_API_KEY=your-openai-api-key
DEBUG=True
```


5. **Run migrations**

```shellscript
python manage.py migrate
```


6. **Create static directories**

```shellscript
mkdir -p static/css static/js static/images
python manage.py collectstatic
```


7. **Start the development server**

```shellscript
python manage.py runserver
```


8. **Access the application**
Open your browser and go to `http://127.0.0.1:8000/`


## 📖 Usage

1. **Upload Content**

1. Select content type (PDF, YouTube, or text)
2. Upload file or provide URL/text
3. Click "Process Content"



2. **View Summary**

1. Automatically generated summary appears on the material detail page
2. Key terms frequency chart visualizes important concepts



3. **Generate Study Materials**

1. Click "Generate Study Materials" button
2. System creates flashcards and quizzes based on content



4. **Use Flashcards**

1. Navigate through flashcards with previous/next buttons
2. Click cards to flip between question and answer
3. Filter by difficulty level



5. **Take Quizzes**

1. Answer multiple-choice questions
2. Get immediate feedback on answers
3. Review explanations for each question
4. See final score and review answers



6. **Ask Questions**

1. Type questions about the content in the Q&A section
2. Get AI-generated answers based on the uploaded material





## ⚠️ Known Issues & Runtime Problems

### OpenAI API Related Issues

1. **API Key Not Loading**

1. **Symptom**: Error showing "OPENAI_API_KEY is not set in settings"
2. **Cause**: `.env` file not found or improperly formatted
3. **Solution**: Verify .env file is in the same directory as `manage.py` and contains `OPENAI_API_KEY=sk-your-key`



2. **Quota Exceeded Errors**

1. **Symptom**: Error 429 with message about exceeding quota
2. **Cause**: Reaching OpenAI API usage limits
3. **Solution**: Check your OpenAI billing status at [https://platform.openai.com/account/billing](https://platform.openai.com/account/billing) and add credits



3. **Rate Limit Errors**

1. **Symptom**: Error 429 with message about rate limits
2. **Cause**: Too many requests in a short time period
3. **Solution**: Implement backoff strategy or use a paid tier with higher rate limits


## 🔮 Future Enhancements

- User authentication system
- Content organization with folders/tags
- Spaced repetition system for flashcards
- Export functionality for study materials
- Mobile application version
- Support for more file formats (PPTX, DOCX)


## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request


## 🙏 Acknowledgments

- Built with assistance from [v0.dev](https://v0.dev) AI assistant
- Uses [OpenAI API](https://openai.com/api/) for content processing
- Frontend built with [Bootstrap](https://getbootstrap.com/)
- [Chart.js](https://www.chartjs.org/) for data visualization
- [PyPDF2](https://pypdf2.readthedocs.io/) for PDF processing
- [youtube-transcript-api](https://github.com/jdepoix/youtube-transcript-api) for YouTube transcript extraction


## UI and working Images

![image](https://github.com/user-attachments/assets/addc2a5f-c917-4372-b87a-b040bb263744)
![image](https://github.com/user-attachments/assets/94cf84b2-392c-4c1c-ad67-8289baa04d5f)
![image](https://github.com/user-attachments/assets/04805676-5dfc-477c-ac77-f1dc8be921e9)


