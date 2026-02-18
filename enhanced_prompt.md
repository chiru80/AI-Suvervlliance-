# Enhanced Prompt: Build an App from My GitHub Repository

Use this prompt when the original request is vague (for example: “by using my github repo build an app for it”).

## Prompt
Analyze the GitHub repository I provide and help me build a complete application from it.

Repository URL: `<PASTE_GITHUB_REPO_URL_HERE>`

If the URL is missing or inaccessible, ask for it first before continuing.

### What I want from you
1. **Project Overview**
   - Summarize what the repository appears to do based on `README`, code structure, and configuration files.
   - State the likely end goal of the application.

2. **Repository Analysis**
   - Identify:
     - primary language(s)
     - framework(s)
     - package/dependency managers
     - key entry points (e.g., `app.py`, `main.py`, `index.js`, `src/main.ts`, etc.)
   - List important files/folders and their purpose.

3. **Missing Requirements and Assumptions**
   - Explicitly call out any missing information needed to proceed.
   - For each missing item, provide a reasonable default assumption and mark it as an assumption.

4. **App Definition**
   - Propose the app type that best fits the repo (web app, API service, CLI, mobile backend, etc.).
   - Define an MVP feature set with clear scope.

5. **Local Environment Setup**
   - Provide prerequisites (versions for Node/Python/Java/etc.).
   - Give exact setup commands for macOS/Linux and Windows when possible.
   - Include environment variable setup (`.env`) with placeholders.

6. **Build and Run Guide**
   - Step-by-step commands to install dependencies, run in development mode, and build for production.
   - Include how to run tests and linting (if available).

7. **Architecture Explanation**
   - Explain how major components interact (frontend/backend/database/services).
   - Include a simple text-based architecture diagram.

8. **Deployment Plan**
   - Recommend at least two deployment options (e.g., Vercel/Render/Heroku/AWS/Docker).
   - Provide deployment steps and required environment variables.
   - Include a basic CI/CD suggestion.

9. **Troubleshooting**
   - List common setup/runtime errors likely for this repo and how to fix them.

10. **Next Actions**
   - End with a prioritized checklist of what I should do first, second, and third.

### Output format requirements
- Use clear section headers matching the items above.
- Use commands in fenced code blocks.
- Keep assumptions explicitly labeled.
- If repo contents are ambiguous, provide 2–3 implementation paths and recommend one.
