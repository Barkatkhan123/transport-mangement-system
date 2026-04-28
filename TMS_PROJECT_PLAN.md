# Transport Management System (TMS)
### Final Year Project — Full Technical Plan

---

## 1. Project Overview

A full-stack web application that connects **passengers** with **transport agencies**. Passengers can search, book, and pay for bus seats and receive a QR-coded ticket. Agencies manage their fleet, drivers, routes, and trips through a dedicated panel. A super admin oversees the entire platform.

**Tech Stack**

| Layer | Technology |
|---|---|
| Backend Framework | Django 5.x + Django REST Framework |
| Frontend | Django Templates + Tailwind CSS v3 |
| Database | PostgreSQL |
| Authentication | Django Sessions (web) + DRF JWT (API) |
| QR Code | `qrcode[pil]` |
| PDF Tickets | `weasyprint` |
| Payments | Stripe (or Paymob for local markets) |
| Email | Django + SendGrid / Gmail SMTP |
| Media Storage | Cloudinary (production) / local (dev) |
| Deployment | Railway or Render |
| Version Control | Git + GitHub |

---

## 2. User Roles & Permissions

| Role | Description | Key Permissions |
|---|---|---|
| **Super Admin** | Platform owner | Approve agencies, manage all data, view analytics |
| **Agency Manager** | Runs a transport company | Add buses, drivers, routes, trips; view bookings |
| **Passenger** | End user | Search trips, book seats, pay, view QR ticket |

---

## 3. Database Design (Full Models)

### 3.1 `accounts` App

```
User (AbstractBaseUser)
├── id (UUID, PK)
├── email (unique)
├── full_name
├── phone_number
├── profile_photo
├── role (choices: admin | agency | passenger)
├── is_active
├── is_staff
├── date_joined
└── last_login

PassengerProfile
├── user (OneToOne → User)
├── date_of_birth
├── gender (M/F/Other)
├── national_id
└── emergency_contact
```

### 3.2 `agency` App

```
Agency
├── id (UUID, PK)
├── manager (OneToOne → User)
├── name
├── registration_number (unique)
├── logo
├── email
├── phone
├── address
├── city
├── status (choices: pending | approved | suspended)
├── approved_at
├── created_at
└── updated_at

Driver
├── id (UUID, PK)
├── agency (FK → Agency)
├── full_name
├── license_number (unique)
├── license_expiry_date
├── phone_number
├── photo
├── date_of_birth
├── address
├── experience_years
├── status (choices: active | on_leave | terminated)
├── created_at
└── updated_at

Bus
├── id (UUID, PK)
├── agency (FK → Agency)
├── registration_number (unique)
├── bus_type (choices: AC | Non-AC | Sleeper | Mini)
├── total_seats
├── seat_layout (choices: 2x2 | 2x3)
├── model_name
├── year_of_manufacture
├── photo
├── amenities (JSON: wifi, charging, TV)
├── status (choices: active | maintenance | retired)
├── created_at
└── updated_at
```

### 3.3 `trips` App

```
City
├── id
├── name
└── province

Route
├── id (UUID, PK)
├── origin (FK → City)
├── destination (FK → City)
├── distance_km
├── estimated_duration_minutes
└── created_at

Trip
├── id (UUID, PK)
├── agency (FK → Agency)
├── route (FK → Route)
├── bus (FK → Bus)
├── driver (FK → Driver)
├── departure_datetime
├── arrival_datetime
├── base_price (Decimal)
├── status (choices: scheduled | boarding | departed | arrived | cancelled)
├── cancellation_reason
├── created_at
└── updated_at

Seat
├── id (UUID, PK)
├── trip (FK → Trip)
├── seat_number (e.g. A1, A2, B1)
├── row_number
├── column_number
├── seat_type (choices: window | aisle | middle)
├── is_booked (Boolean, default False)
└── gender_restriction (choices: any | male | female)
```

### 3.4 `bookings` App

```
Booking
├── id (UUID, PK)
├── booking_number (auto-generated, human-readable e.g. TMS-2024-0001)
├── passenger (FK → User)
├── trip (FK → Trip)
├── seats (M2M → Seat)
├── total_price (Decimal)
├── status (choices: pending | confirmed | cancelled | refunded)
├── cancellation_reason
├── booked_at
└── updated_at

Payment
├── id (UUID, PK)
├── booking (OneToOne → Booking)
├── amount (Decimal)
├── method (choices: card | mobile_wallet | bank_transfer)
├── transaction_id (from payment gateway)
├── status (choices: pending | successful | failed | refunded)
├── gateway_response (JSON)
├── paid_at
└── created_at

Ticket
├── id (UUID, PK)
├── booking (OneToOne → Booking)
├── ticket_number (UUID, unique)
├── qr_code_image (ImageField)
├── qr_data (JSON stored as text)
├── is_used (Boolean, default False)
├── used_at
└── issued_at
```

---

## 4. URL Structure

```
/                           → home (search)
/auth/register/             → passenger registration
/auth/login/                → login
/auth/logout/               → logout
/auth/profile/              → view/edit profile

/trips/search/              → search results
/trips/<id>/                → trip detail + seat map
/trips/<id>/book/           → booking form
/trips/<id>/confirm/        → booking confirmation

/payment/<booking_id>/      → payment page
/payment/success/           → payment success + ticket
/payment/failed/            → payment failed

/tickets/<ticket_number>/   → view ticket (QR code)
/bookings/                  → passenger booking history
/bookings/<id>/cancel/      → cancel booking

/agency/register/           → agency registration
/agency/dashboard/          → agency home (stats)
/agency/buses/              → list buses
/agency/buses/add/          → add bus
/agency/buses/<id>/edit/    → edit bus
/agency/drivers/            → list drivers
/agency/drivers/add/        → add driver
/agency/drivers/<id>/edit/  → edit driver
/agency/routes/             → list routes
/agency/trips/              → list trips
/agency/trips/add/          → schedule trip
/agency/trips/<id>/         → trip detail + bookings
/agency/trips/<id>/manifest/→ download passenger manifest PDF

/admin-panel/               → custom admin dashboard (super admin)
/admin-panel/agencies/      → manage agency approvals
/admin-panel/users/         → manage all users

/api/v1/trips/search/       → DRF search endpoint (AJAX)
/api/v1/seats/<trip_id>/    → DRF seat availability (AJAX)
/api/v1/bookings/           → DRF booking endpoint
/api/v1/payment/verify/     → Stripe webhook
```

---

## 5. Detailed Feature Specifications

### 5.1 Trip Search
- Fields: Origin city, Destination city, Travel date, Number of passengers
- Results sorted by departure time (default), filterable by price / bus type
- Shows: agency logo, departure & arrival time, duration, price, seats available, bus type badges
- "No trips found" state with illustration

### 5.2 Seat Map
- Visual grid matching the bus layout (2x2 or 2x3)
- Legend: available (white), booked (red), selected (blue), female-only (pink)
- Real-time seat availability via AJAX call to `/api/v1/seats/<trip_id>/`
- Max seat selection = number of passengers from search
- Seat selection summary panel on the right (selected seats, subtotal)

### 5.3 Booking & Confirmation
- Summary card: trip info, selected seats, passenger details, total price
- Passenger fills: name, CNIC/Passport, phone (pre-filled from profile)
- Terms & conditions checkbox
- "Confirm & Pay" button

### 5.4 Payment
- Stripe Checkout (card) or manual mobile wallet reference
- On successful payment:
  - Booking status → confirmed
  - Seats marked as is_booked = True
  - Ticket record created with UUID + QR code generated
  - Confirmation email sent with QR code attached
- On failure: booking stays pending, seats released after 10 minutes (Celery task or DB check)

### 5.5 QR Code Ticket
- QR encodes JSON: `{ticket_number, passenger_name, trip_id, seats, departure, route}`
- Displayed large on ticket page
- Ticket card includes: TMS logo, booking number, route, date, time, seat numbers, bus info, passenger name
- "Download PDF" button (weasyprint)
- "Send to Email" button

### 5.6 Agency Dashboard
- Stats cards: Total Trips, Total Revenue, Bookings Today, Active Buses
- Charts: weekly bookings bar chart, revenue line chart (Chart.js)
- Recent bookings table
- Upcoming trips list
- Quick action buttons: Schedule Trip, Add Bus, Add Driver

### 5.7 Driver Management
- Add driver form with photo upload and license expiry date
- Status badge (active / on leave / terminated)
- Driver card shows: photo, name, license number, experience, current trip assignment
- Validation: cannot assign driver to two overlapping trips

### 5.8 Bus Management
- Add bus with seat layout preview
- Amenity checkboxes (WiFi, Charging, TV, Toilet)
- Maintenance status toggle
- Cannot schedule a bus that is under maintenance

### 5.9 Trip Scheduling
- Date/time pickers for departure and arrival
- Auto-calculates duration from route
- Conflict detection: blocks scheduling if bus or driver already has a trip at that time
- Seat rows auto-generated when trip is saved based on bus capacity and layout

### 5.10 Passenger Manifest (Agency)
- Accessible at `/agency/trips/<id>/manifest/`
- Table: seat number, passenger name, phone, CNIC, booking status
- Exportable as PDF (weasyprint) and CSV

---

## 6. UI/UX Design System

### Color Palette
```
Primary:    #1D4ED8  (blue-700)   — buttons, links, headers
Secondary:  #F97316  (orange-500) — accents, badges, CTA
Success:    #16A34A  (green-600)  — confirmed, available
Danger:     #DC2626  (red-600)    — booked, error, cancel
Neutral:    #F1F5F9  (slate-100)  — backgrounds
Text:       #0F172A  (slate-900)  — headings
Muted:      #64748B  (slate-500)  — secondary text
```

### Typography
- Headings: `Inter` (Google Fonts) — bold, clean
- Body: `Inter` regular
- Monospace (ticket numbers): `JetBrains Mono`

### Component Library (custom Tailwind components)
- `BusCard` — trip search result
- `SeatGrid` — interactive seat map
- `BookingSummaryCard` — right-side sticky panel
- `TicketCard` — styled QR ticket
- `StatCard` — agency dashboard metric
- `StatusBadge` — color-coded status pill
- `AlertBanner` — success / error / warning
- `DataTable` — sortable, searchable table for listings

### Responsiveness
- Mobile-first: all pages fully usable on 360px+
- Tablet: side-by-side layouts for seat map + summary
- Desktop: full dashboard with sidebar navigation

### Passenger Navigation
```
Top navbar: Logo | Search | My Bookings | Profile | Login
Mobile: bottom tab bar (Home, Search, Tickets, Profile)
```

### Agency Navigation
```
Left sidebar: Dashboard | Buses | Drivers | Routes | Trips | Bookings | Settings
Collapsible on mobile (hamburger)
```

---

## 7. Security Plan

| Area | Approach |
|---|---|
| Authentication | Django sessions for web; JWT for API |
| Authorization | `@login_required`, role-based middleware, DRF permissions |
| Agency isolation | Every agency query filtered by `agency=request.user.agency` |
| CSRF protection | Django CSRF tokens on all forms |
| Input validation | Django forms + DRF serializers on all inputs |
| SQL injection | Django ORM only (no raw queries) |
| File uploads | Validate mime type + size; store outside web root |
| Payment | Never store card data; use Stripe tokenization |
| Tickets | Ticket validation checks DB, not just QR content |
| Rate limiting | `django-ratelimit` on login and booking endpoints |
| HTTPS | Enforced in production via `SECURE_SSL_REDIRECT` |

---

## 8. Development Roadmap

### Phase 1 — Foundation (Week 1–2)
- [ ] Django project setup, settings split (dev/prod), env vars
- [ ] Custom `User` model with roles
- [ ] Registration, login, logout views + templates
- [ ] Base template with Tailwind CSS, responsive navbar
- [ ] PostgreSQL connection

### Phase 2 — Agency Core (Week 3–4)
- [ ] Agency model + registration form
- [ ] Admin approval workflow (email notification)
- [ ] Bus CRUD (add, edit, list, delete with soft-delete)
- [ ] Driver CRUD with photo upload
- [ ] Agency settings page

### Phase 3 — Trip Scheduling (Week 5)
- [ ] City + Route models + management
- [ ] Trip scheduling form with conflict detection
- [ ] Auto seat generation on trip creation
- [ ] Trip status management

### Phase 4 — Passenger Search & Seat Selection (Week 6)
- [ ] Search form + results page with filters
- [ ] Trip detail page
- [ ] Seat map component (AJAX seat availability)
- [ ] Session-based seat hold (10-minute timer)

### Phase 5 — Booking & Payment (Week 7–8)
- [ ] Booking creation flow
- [ ] Stripe integration (Checkout + webhooks)
- [ ] Payment confirmation handling
- [ ] Seat lock/release logic

### Phase 6 — QR Ticket System (Week 8)
- [ ] Ticket generation on payment success
- [ ] QR code image generation (`qrcode` lib)
- [ ] Ticket page (display + download PDF)
- [ ] Email ticket on booking confirmation

### Phase 7 — Agency Dashboard (Week 9)
- [ ] Dashboard stats + Chart.js graphs
- [ ] Booking list per trip (with search/filter)
- [ ] Passenger manifest (view + PDF + CSV export)
- [ ] Revenue summary

### Phase 8 — Admin Panel (Week 10)
- [ ] Custom Django admin theme
- [ ] Agency approval dashboard
- [ ] Platform-wide analytics
- [ ] User management

### Phase 9 — Polish & Testing (Week 11–12)
- [ ] Full responsive QA on mobile/tablet/desktop
- [ ] Unit tests (models, views)
- [ ] Integration tests (booking flow, payment)
- [ ] Edge cases: duplicate booking, double seat, cancelled trip
- [ ] Performance: add DB indexes, optimize queries with `select_related`/`prefetch_related`
- [ ] Accessibility (ARIA labels, keyboard nav)

### Phase 10 — Deployment (Week 13)
- [ ] Production settings (DEBUG=False, ALLOWED_HOSTS, etc.)
- [ ] Static files via WhiteNoise
- [ ] Media files via Cloudinary
- [ ] Deploy to Railway or Render
- [ ] Custom domain + HTTPS
- [ ] Seed database with demo data

---

## 9. Project File Structure

```
tms/
├── config/
│   ├── settings/
│   │   ├── base.py
│   │   ├── dev.py
│   │   └── prod.py
│   ├── urls.py
│   └── wsgi.py
│
├── apps/
│   ├── accounts/
│   │   ├── models.py         # User, PassengerProfile
│   │   ├── views.py          # register, login, profile
│   │   ├── forms.py
│   │   ├── urls.py
│   │   └── serializers.py
│   │
│   ├── agency/
│   │   ├── models.py         # Agency, Driver, Bus
│   │   ├── views.py          # CRUD views
│   │   ├── forms.py
│   │   ├── urls.py
│   │   └── permissions.py    # IsAgencyManager
│   │
│   ├── trips/
│   │   ├── models.py         # City, Route, Trip, Seat
│   │   ├── views.py          # search, detail, schedule
│   │   ├── forms.py
│   │   ├── urls.py
│   │   ├── serializers.py    # for AJAX seat API
│   │   └── signals.py        # auto-create seats on trip save
│   │
│   ├── bookings/
│   │   ├── models.py         # Booking, Payment, Ticket
│   │   ├── views.py          # booking flow, payment
│   │   ├── forms.py
│   │   ├── urls.py
│   │   ├── serializers.py
│   │   ├── utils.py          # QR generation, PDF generation
│   │   └── webhooks.py       # Stripe webhook handler
│   │
│   └── dashboard/
│       ├── views.py          # agency dashboard, admin dashboard
│       └── urls.py
│
├── templates/
│   ├── base.html
│   ├── components/
│   │   ├── navbar.html
│   │   ├── sidebar.html
│   │   ├── seat_map.html
│   │   ├── bus_card.html
│   │   ├── stat_card.html
│   │   └── ticket_card.html
│   ├── passenger/
│   │   ├── home.html
│   │   ├── search_results.html
│   │   ├── trip_detail.html
│   │   ├── booking_confirm.html
│   │   ├── payment.html
│   │   ├── ticket.html
│   │   └── my_bookings.html
│   ├── agency/
│   │   ├── dashboard.html
│   │   ├── buses/
│   │   ├── drivers/
│   │   ├── trips/
│   │   └── bookings/
│   └── admin_panel/
│       ├── dashboard.html
│       └── agencies.html
│
├── static/
│   ├── css/
│   │   └── main.css          # Tailwind compiled
│   ├── js/
│   │   ├── seat_map.js       # seat selection logic
│   │   ├── search.js         # search AJAX
│   │   └── charts.js         # Chart.js config
│   └── img/
│
├── media/                    # uploaded files (dev only)
├── requirements/
│   ├── base.txt
│   ├── dev.txt
│   └── prod.txt
├── .env.example
├── manage.py
└── README.md
```

---

## 10. Python Dependencies

```
# requirements/base.txt
django>=5.0
djangorestframework
djangorestframework-simplejwt
psycopg2-binary
pillow
qrcode[pil]
weasyprint
stripe
django-environ
django-crispy-forms
crispy-tailwind
django-ratelimit
django-filter
whitenoise
cloudinary
django-cloudinary-storage
sendgrid

# requirements/dev.txt
-r base.txt
django-debug-toolbar
factory-boy
faker

# requirements/prod.txt
-r base.txt
gunicorn
```

---

## 11. Key Business Logic Notes

1. **Seat Hold**: When a passenger selects seats, mark them as temporarily held in the session for 10 minutes. If payment is not completed, seats are released.
2. **Trip Cancellation**: If an agency cancels a trip, all confirmed bookings are automatically refunded and passengers are notified by email.
3. **Agency Approval**: New agencies cannot schedule trips until approved by admin. Show a clear "pending approval" banner on their dashboard.
4. **Booking Number**: Human-readable format `TMS-YYYYMM-XXXX` (e.g. `TMS-202411-0034`) generated on booking creation.
5. **Price per Trip**: Price is set per trip (not per route), allowing agencies to set promotional fares.
6. **Driver Conflict Check**: Before saving a trip, check that the assigned driver has no other trip with overlapping departure/arrival times.
7. **Bus Conflict Check**: Same conflict check for buses.

---

## 12. Demo Data (for Presentation)
- 3 agencies (GreenLine, Daewoo, Faisal Movers style)
- 10 buses of varying types
- 15 drivers
- 20 routes across major cities
- 50 trips over the next 30 days
- 100 sample bookings with varying statuses
- 5 sample passenger accounts

---

*Last updated: April 2026*
*Project: Final Year Project — Transport Management System*
