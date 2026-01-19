# Streamlit Cloud Deployment Guide

## 🚀 Quick Deployment to Streamlit Cloud

### Prerequisites
- GitHub account
- This project pushed to a GitHub repository
- Streamlit Cloud account (free at https://streamlit.io/cloud)

---

## Step-by-Step Deployment

### 1. Prepare Your Repository

Make sure your GitHub repository contains:
- ✅ `app.py`
- ✅ `requirements.txt`
- ✅ All project folders (`sentiment/`, `ui/`)
- ✅ `.gitignore` (to exclude venv, cache, etc.)

### 2. Push to GitHub

```bash
# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit - SentimentScope MVP"

# Add remote repository
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git

# Push to GitHub
git push -u origin main
```

### 3. Deploy on Streamlit Cloud

1. **Go to Streamlit Cloud**
   - Visit: https://streamlit.io/cloud
   - Click "Sign in" (use GitHub account)

2. **Create New App**
   - Click "New app" button
   - Select your repository
   - Choose branch (usually `main`)
   - Set main file path: `app.py`
   - Click "Deploy"

3. **Wait for Deployment**
   - Streamlit Cloud will:
     - Clone your repository
     - Install dependencies from `requirements.txt`
     - Run your app
     - Provide a public URL

4. **Access Your App**
   - Your app will be live at:
     `https://YOUR-APP-NAME.streamlit.app`

---

## ⚙️ Configuration (Optional)

### Custom Domain
1. Go to app settings
2. Click "Custom domain"
3. Follow instructions to set up

### Environment Variables
If you need environment variables:

1. Go to app settings
2. Click "Secrets"
3. Add your variables in TOML format:
```toml
[secrets]
API_KEY = "your-api-key"
```

### Resource Limits
Free tier includes:
- 1 GB RAM
- 1 CPU core
- Public apps only
- Unlimited apps

---

## 🔧 App Settings in Streamlit Cloud

### Access Settings
1. Open your deployed app
2. Click "Manage app" (top right)
3. Go to "Settings"

### Available Options
- **Reboot app**: Restart if frozen
- **Clear cache**: Reset cached data
- **View logs**: Debug issues
- **Delete app**: Remove deployment

---

## 📊 Monitoring Your App

### View Logs
```
Menu → Manage app → Logs
```

Shows:
- Startup logs
- Error messages
- User activity
- Performance metrics

### Analytics (Pro Plan)
- Number of visitors
- Usage patterns
- Performance data

---

## 🐛 Troubleshooting

### App Won't Deploy
**Check:**
- ✅ `requirements.txt` is present
- ✅ All dependencies are listed
- ✅ No local file paths in code
- ✅ Python version compatibility

### Import Errors
**Solution:**
Add missing packages to `requirements.txt`:
```
package-name==version
```

### NLTK Data Not Found
**Solution:**
Add to your `app.py` (at the top):
```python
import nltk
nltk.download('brown', quiet=True)
nltk.download('punkt', quiet=True)
```

### Memory Issues
**Solutions:**
- Use smaller models
- Optimize code
- Upgrade to Streamlit Cloud Pro

---

## 🎯 Best Practices

### 1. Requirements Management
- Pin exact versions: `package==1.2.3`
- Keep requirements minimal
- Test locally first

### 2. Code Optimization
- Cache expensive operations:
  ```python
  @st.cache_data
  def load_model():
      return model
  ```
- Minimize file operations
- Use session state efficiently

### 3. Error Handling
- Add try-except blocks
- Provide user-friendly messages
- Log errors for debugging

### 4. Performance
- Lazy load heavy libraries
- Use caching strategically
- Optimize data processing

---

## 🔄 Update Your App

### Method 1: Git Push (Automatic)
```bash
# Make changes to your code
git add .
git commit -m "Update: description"
git push

# Streamlit Cloud auto-deploys on push
```

### Method 2: Manual Reboot
1. Go to app settings
2. Click "Reboot app"
3. App restarts with latest code

---

## 💰 Pricing Tiers

### Free Tier
- ✅ Public apps
- ✅ 1 GB RAM
- ✅ Community support
- ✅ Unlimited apps

### Pro Tier ($20/month)
- ✅ Private apps
- ✅ 4 GB RAM
- ✅ Priority support
- ✅ Custom domains
- ✅ Analytics

---

## 📱 Sharing Your App

Once deployed, share your app:

### Direct Link
```
https://your-app-name.streamlit.app
```

### Embed in Website
```html
<iframe
  src="https://your-app-name.streamlit.app"
  width="100%"
  height="600px"
></iframe>
```

### Social Media
- Add to LinkedIn projects
- Share on Twitter
- Include in portfolio

---

## 🎨 Custom Branding (Pro)

### App Settings
1. Upload favicon
2. Set app title
3. Customize theme colors
4. Add logo

### Theme Configuration
Create `.streamlit/config.toml`:
```toml
[theme]
primaryColor="#667eea"
backgroundColor="#ffffff"
secondaryBackgroundColor="#f0f2f6"
textColor="#262730"
font="sans serif"
```

---

## 🔒 Security Best Practices

### 1. Secrets Management
- Never commit API keys
- Use Streamlit Secrets
- Rotate keys regularly

### 2. Input Validation
- Sanitize user input
- Limit input size
- Handle edge cases

### 3. Rate Limiting
- Implement usage caps
- Add cooldowns
- Monitor abuse

---

## 📈 Scaling Considerations

### When to Upgrade
- High traffic (>1000 daily users)
- Complex computations
- Large data processing
- Private/commercial use

### Alternative Hosting
For enterprise needs:
- **AWS EC2** with Docker
- **Google Cloud Run**
- **Azure App Service**
- **Heroku** (with custom buildpack)

---

## ✅ Deployment Checklist

Before deploying:
- [ ] Test locally (`streamlit run app.py`)
- [ ] All dependencies in `requirements.txt`
- [ ] No hardcoded paths or secrets
- [ ] README.md is complete
- [ ] .gitignore excludes unnecessary files
- [ ] Code is well-commented
- [ ] Error handling implemented
- [ ] Mobile-responsive design tested
- [ ] About page information is accurate

After deployment:
- [ ] Test all features on live app
- [ ] Check logs for errors
- [ ] Verify analytics tracking
- [ ] Share with test users
- [ ] Gather feedback
- [ ] Update documentation

---

## 🎊 Success!

Your app is now live and accessible to the world!

**Next Steps:**
1. Share with friends/colleagues
2. Gather user feedback
3. Iterate and improve
4. Add to your portfolio
5. Consider adding new features

---

## 📚 Additional Resources

- **Streamlit Docs**: https://docs.streamlit.io/
- **Deployment Guide**: https://docs.streamlit.io/streamlit-cloud
- **Community Forum**: https://discuss.streamlit.io/
- **GitHub Issues**: https://github.com/streamlit/streamlit/issues

---

**Happy Deploying! 🚀**

*Remember: Keep your app updated and responsive to user feedback!*
