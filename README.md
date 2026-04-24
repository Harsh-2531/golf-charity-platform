# GolfCharity Platform

## Overview
Play Golf. Win Prizes. Change Lives.

A full-stack platform where golfers can:
- Track Stableford scores
- Compete in monthly draws with real prizes
- Automatically support charities they care about

## Live Demo
- **Frontend**: https://golf-charity-platform-632du0kxb-harsh-2531s-projects.vercel.app
- **Backend API**: https://golf-charity-platform-hqyj.onrender.com

## Tech Stack
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Backend**: Python Flask + Gunicorn
- **Database**: Supabase (PostgreSQL)
- **Payments**: Stripe (test mode)
- **Hosting**: Vercel (frontend), Render (backend)

## Features Implemented
✅ User authentication (Signup/Login)
✅ Score entry and tracking (Stableford system)
✅ Monthly draw engine with winning logic
✅ Subscription management (Monthly/Yearly)
✅ Automatic charity support (10%+ of subscriptions)
✅ Admin panel for draws and payouts
✅ Responsive modern UI design
✅ Stripe payment integration

## Getting Started Locally

### Prerequisites
- Python 3.9+
- Node.js (for local dev if needed)
- Git

### Backend Setup
```bash
cd backend
pip install -r requirements.txt
cp .env.example .env
# Fill in your credentials
python main.py
```

### Frontend Setup
```bash
cd frontend
# Serve with any HTTP server
python -m http.server 8000
# Visit http://localhost:8000
```

## Deployment

### Frontend (Vercel)
```bash
git push origin main
# Vercel auto-deploys from main branch
```

### Backend (Render)
```bash
# Push to GitHub, Render auto-deploys from main branch
# Environment variables configured in Render dashboard
```

## API Endpoints
- `POST /api/auth/signup` - Create new user
- `POST /api/auth/login` - User login
- `POST /api/scores/add` - Add golf score
- `GET /api/user/dashboard` - User dashboard data
- `POST /api/admin/draws/run` - Run monthly draw
- `POST /api/admin/payouts/process` - Process charity payouts

## Testing
Default test account:
- Email: test@test.com
- Password: Test1234

## Future Enhancements
- Social leaderboard
- Email notifications
- SMS reminders for score entry
- Prize fulfillment integration
- Advanced analytics dashboard

## License
All rights reserved © 2024 GolfCharity
