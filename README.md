# ⛳ GolfCharity Platform

> Play Golf. Win Prizes. Change Lives.

A full-stack platform where golfers can track Stableford scores, compete in monthly draws with real prizes, and automatically support charities they care about.

---

## 🌐 Live Demo

| Panel | URL |
|---|---|
| Frontend | https://golf-charity-platform-632du0kxb-harsh-2531s-projects.vercel.app |
| Backend API | https://golf-charity-platform-hqyj.onrender.com |

**Test Account:**
- Email: `test@test.com`
- Password: `Test1234`

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend | HTML5, CSS3, Vanilla JavaScript |
| Backend | Python Flask + Gunicorn |
| Database | Supabase (PostgreSQL) |
| Payments | Stripe (test mode) |
| Hosting | Vercel (frontend) · Render (backend) |

---

## ✨ Features Implemented

- ✅ User authentication (Signup / Login)
- ✅ Score entry and tracking (Stableford system, rolling 5-score logic)
- ✅ Monthly draw engine with winning logic (5, 4, 3 number match tiers)
- ✅ Subscription management (Monthly / Yearly plans via Stripe)
- ✅ Automatic charity support (10%+ of subscription fee)
- ✅ Admin panel for draws, winners, and payouts
- ✅ Responsive modern UI design
- ✅ Stripe payment integration

---

## ⚙️ Environment Variables

Create a `.env` file in the `/backend` directory:

```env
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_service_role_key

STRIPE_SECRET_KEY=your_stripe_secret_key
STRIPE_WEBHOOK_SECRET=your_stripe_webhook_secret

FLASK_SECRET_KEY=your_flask_secret_key
FRONTEND_URL=https://your-frontend.vercel.app
```

---

## 🏃 Getting Started Locally

### Prerequisites

- Python 3.9+
- Git

### Backend Setup

```bash
cd backend
pip install -r requirements.txt
cp .env.example .env
# Fill in your Supabase, Stripe, and Flask credentials
python main.py
```

### Frontend Setup

```bash
cd frontend
python -m http.server 8000
# Visit http://localhost:8000
```

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/auth/signup` | Create new user |
| POST | `/api/auth/login` | User login |
| POST | `/api/scores/add` | Add golf score |
| GET | `/api/user/dashboard` | User dashboard data |
| POST | `/api/admin/draws/run` | Run monthly draw |
| POST | `/api/admin/payouts/process` | Process charity payouts |

---

## 🚀 Deployment

### Frontend — Vercel

```bash
git push origin main
# Vercel auto-deploys from the main branch
```

### Backend — Render

```bash
# Push to GitHub — Render auto-deploys from the main branch
# Environment variables configured in the Render dashboard
```

---

## ✅ Testing Checklist

- [x] User signup & login
- [x] Subscription flow (monthly and yearly)
- [x] Score entry — 5-score rolling logic
- [x] Duplicate date rejection + edit/delete existing score
- [x] Draw system logic and simulation
- [x] Charity selection and contribution calculation
- [x] Winner verification flow and payout tracking
- [x] User Dashboard — all modules functional
- [x] Admin Panel — full control and usability
- [x] Responsive design on mobile and desktop
- [x] Error handling and edge cases

---

## 🔮 Future Enhancements

- Social leaderboard
- Email notifications
- SMS reminders for score entry
- Prize fulfillment integration
- Advanced analytics dashboard

---

## 📄 License

All rights reserved © 2026 GolfCharity

---

Built as part of the Full-Stack Development  
PRD version 1.0 — April 2026 · 