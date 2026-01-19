# Assets Folder

This folder contains static assets for the SentimentScope application.

## 📁 Contents

### Recommended Assets to Add:

1. **logo.png** (Optional)
   - App logo for sidebar
   - Recommended size: 200x200px
   - Format: PNG with transparency
   - Usage: Displayed in sidebar

2. **favicon.ico** (Optional)
   - Browser tab icon
   - Size: 16x16 or 32x32px
   - Format: ICO
   - Configuration in `.streamlit/config.toml`

3. **screenshot.png** (For README)
   - App screenshot for documentation
   - Recommended size: 1200x800px
   - Shows main interface

4. **example_results.png** (Optional)
   - Visual of analysis results
   - For documentation/marketing

## 🎨 Adding Assets

### Adding a Logo

1. Place `logo.png` in this folder
2. Update `app.py`:

```python
from PIL import Image

with st.sidebar:
    logo = Image.open("assets/logo.png")
    st.image(logo, width=150)
    st.markdown("### 🧠 SentimentScope")
```

### Adding a Favicon

1. Place `favicon.ico` in `.streamlit/` folder (create if needed)
2. Create `.streamlit/config.toml`:

```toml
[server]
headless = true

[browser]
gatherUsageStats = false

[theme]
primaryColor="#667eea"
backgroundColor="#ffffff"
secondaryBackgroundColor="#f0f2f6"
textColor="#262730"

[ui]
favicon = ".streamlit/favicon.ico"
```

## 🖼️ Image Guidelines

### Logo
- Format: PNG (transparent background)
- Size: 200x200px or larger
- Style: Simple, recognizable
- Colors: Match app theme (#667eea primary)

### Screenshots
- Format: PNG or JPEG
- Size: At least 1200px wide
- Show: Key features in action
- Quality: High resolution, clear text

## 📝 Notes

Currently, this folder is empty. Assets are optional for the MVP but recommended for production deployment.

You can generate a logo using:
- Canva (https://www.canva.com/)
- LogoMakr (https://logomakr.com/)
- AI tools (DALL-E, Midjourney)
- Design software (Figma, Adobe Illustrator)

## 🎯 Quick Logo Idea

For SentimentScope, a good logo could be:
- 🧠 Brain icon with 😊😐😠 sentiment emojis
- Purple/blue gradient theme
- Modern, minimalist style
- Clear at small sizes

---

**Tip**: While the app works without custom assets, adding a logo and favicon makes it look more professional and memorable!
