# Transport Management System (TMS) Thesis

# CHAPTER 1: INTRODUCTION

## 1.1 Objectives
The primary objectives of the Transport Management System (TMS) are to revolutionize the inter-city bus transport operations by digitizing and streamlining the end-to-end booking and fleet management workflows. The core objectives include:
1. To provide a centralized web platform that seamlessly connects passengers, transport agencies, and administrators.
2. To enable passengers to easily search for bus trips, interactively select seats, complete secure online payments, and receive verifiable QR-coded digital tickets.
3. To equip transport agencies with a self-service management panel to oversee their fleet, drivers, routes, trip schedules, and booking records effectively.
4. To establish a robust, role-based access control system ensuring data security and operational separation between passengers, agency managers, and super administrators.
5. To eliminate manual scheduling conflicts, reduce reliance on paper-based ticket records, and eliminate double-booking scenarios.
6. To design a scalable, modular architecture capable of supporting multi-agency operations efficiently within a unified database schema.

## 1.2 Background
In many developing regions, including Pakistan, inter-city bus transport serves as a critical and primary mode of travel for millions of citizens. However, despite the rapid global shift towards digital solutions, a significant proportion of bus operators continue to rely heavily on manual, outdated practices. These include physical ticket counters, phone-based bookings, and rudimentary paper-based record keeping. 
This traditional approach introduces numerous inefficiencies. Passengers face considerable difficulties in comparing routes across different agencies, checking real-time seat availability without visiting physical terminals, and obtaining verifiable tickets. On the operational side, transport agencies struggle with coordinating their fleets, managing driver schedules, avoiding booking conflicts, and tracking revenue accurately. The absence of a standardized, integrated digital platform leads to fragmented services, revenue leakage, and a poor overall customer experience. The proposed TMS addresses these fundamental challenges by delivering a cohesive, digitized ecosystem.

## 1.3 Project Structure
The TMS is a full-stack web application designed with a modular monolithic architecture to balance performance and development efficiency. The project is structured as follows:
- **Frontend Presentation Layer:** Developed utilizing the Django framework's templating engine paired with Tailwind CSS for a highly responsive, modern, and user-friendly interface. It handles server-side rendering for the primary user journey.
- **Backend Application Layer:** Powered by Python and the Django 5.x framework, handling all business logic, user authentication, agency management, and booking workflows. 
- **API Layer:** Implemented using Django REST Framework (DRF) to provide lightweight, asynchronous data fetching capabilities, particularly for dynamic UI components like real-time seat availability selection.
- **Data Layer:** Utilizes SQLite (scalable to PostgreSQL for production) to maintain a highly relational database schema supporting complex multi-agency data requirements.

## 1.4 System Salient Features
The salient features of the TMS include:
- **Role-Based Dashboards:** Distinct and secure portals tailored for Passengers, Agency Managers, and Super Administrators.
- **Interactive Seat Selection:** Real-time visual seat mapping allowing passengers to select preferred seating configurations accurately.
- **Digital Ticketing:** Automated generation of verifiable digital tickets featuring scannable QR codes sent directly to the passenger's email.
- **Comprehensive Fleet Management:** Tools for agencies to dynamically add buses, define routes, schedule trips, and assign drivers.
- **Agency Approval Workflow:** Administrative oversight allowing platform owners to vet and approve transport agencies before they commence operations on the platform.
- **Responsive Design:** A mobile-first, highly accessible user interface ensuring seamless usability across desktops, tablets, and smartphones.

---

# CHAPTER 2: SOFTWARE PROJECT PLAN

## 2.1 Introduction
The Software Project Plan for the Transport Management System (TMS) outlines the systematic approach, methodologies, and management strategies employed to successfully develop and deploy the platform. This plan serves as a roadmap for the development lifecycle, defining the scope, resources, schedule, and deliverables required to achieve the project's objectives efficiently.

## 2.2 Project Overview
TMS is an integrated web-based platform designed to automate and centralize inter-city bus transport bookings and fleet management. The project encompasses the development of passenger-facing booking interfaces, agency-facing management portals, and administrative oversight tools. The development follows an agile methodology, ensuring iterative refinement and adaptability to evolving requirements.

## 2.3 Project Deliverables
The key deliverables for the TMS project include:
1. **Requirements Specification Document:** Detailing functional and non-functional requirements.
2. **Design Documentation:** Including architectural diagrams, Entity-Relationship Diagrams (ERDs), and UI mockups.
3. **Source Code:** The complete, commented, and version-controlled Django application codebase.
4. **Compiled/Deployable System:** A fully functional web application ready for deployment on a production server.
5. **Testing Reports:** Comprehensive test cases, execution logs, and validation results.
6. **User Manuals:** Guides for Passengers, Agency Managers, and Administrators detailing system usage.

## 2.4 Software Project Management Plan
The management plan focuses on maintaining strict control over the project's scope, schedule, and quality. It involves continuous monitoring of development milestones, regular code reviews, and iterative testing phases to ensure the final product aligns with the specified requirements and performance standards.

## 2.5 Reference Materials
- Django 5.x Official Documentation
- Django REST Framework Documentation
- Tailwind CSS Official Guidelines
- IEEE Standard for Software Project Management Plans

## 2.6 Definition, Acronyms, or Abbreviations
- **TMS:** Transport Management System
- **DRF:** Django REST Framework
- **QR Code:** Quick Response Code
- **ERD:** Entity-Relationship Diagram
- **UI/UX:** User Interface / User Experience

## 2.1 Project Organization

### 1.1 Gantt-Chart
A Gantt chart has been utilized to track the project's timeline, breaking down the development lifecycle into manageable phases: Requirement Analysis (Weeks 1-2), System Design (Weeks 3-4), Implementation (Weeks 5-10), Testing (Weeks 11-12), and Deployment (Week 13).

### 1.2 Work Products
Work products encompass all tangible outputs generated during the project lifecycle, including requirement documents, design models (Use Cases, Sequence Diagrams), database schemas, application code, test cases, and deployment scripts.

### 1.3 Organizational Structure
The project is executed by a focused development team. The structure involves a Project Manager/Lead Developer overseeing the architecture and backend logic, supported by frontend developers focusing on UI/UX implementation, and a QA tester responsible for system validation.

#### 1.3.1 Organizational Boundaries & Interfaces
The project interfaces primarily with simulated payment gateways and email service providers (e.g., SMTP servers for ticket dispatch). Internal boundaries are defined by the modularity of the Django apps (e.g., separating the 'booking' app from the 'agency' app).

### 1.4 Project Responsibilities (WBS)
The Work Breakdown Structure (WBS) assigns specific responsibilities:
- **Phase 1:** Planning and Requirements Gathering
- **Phase 2:** Database and System Architecture Design
- **Phase 3:** Backend Implementation (Models, Views, APIs)
- **Phase 4:** Frontend Implementation (Templates, Tailwind CSS styling)
- **Phase 5:** Integration, Testing, and Bug Fixing
- **Phase 6:** Documentation and Final Deployment

## 2.2 Managerial Process

### 2.1 Management Objectives and Priorities
The primary managerial objective is to deliver a robust, scalable, and user-friendly system within the stipulated timeframe. Priorities include ensuring high data integrity, secure user authentication, and a seamless booking experience. Quality assurance takes precedence over adding auxiliary features out of the initial scope.

## 2.3 Assumptions, Dependencies and Constrains
- **Assumptions:** Users have access to modern web browsers and stable internet connections. Agencies have the operational capacity to manage digital platforms.
- **Dependencies:** The system relies on third-party libraries (Django, Tailwind) and external email delivery services.
- **Constraints:** The project must be completed within the final year academic timeline. The initial scope does not include live payment gateway integration (simulated instead) or native mobile apps.

## 2.4 Risk Management
*(Detailed extensively in Chapter 3)*. Risk management involves identifying potential technical bottlenecks, scheduling delays, and scope creep, mitigated through agile iterations, regular backups, and strict adherence to the core requirements.

## 2.5 Monitoring and Controlling Mechanics
Progress is monitored via version control commits (Git), milestone tracking, and regular code reviews. Any deviation from the schedule is addressed by reallocating resources or adjusting the scope of non-critical features.

## 2.6 Staff Plan
The staff plan comprises the core academic project team, assuming roles of full-stack developer, database designer, and quality assurance tester, dedicating scheduled weekly hours to meet milestone deadlines.

## 2.7 Technical Process
### 7.1 Methods, Tools and Techniques
#### 7.1.1 Hardware Environment
- **Development:** Standard modern PCs/Laptops (Minimum 8GB RAM, Multi-core processors).
- **Deployment/Production:** Cloud VPS (e.g., AWS EC2, DigitalOcean Droplet) with minimum 2GB RAM and standard storage for web application hosting.
#### 7.1.2 Operating System
- Development: Windows/Linux/macOS
- Production: Ubuntu Linux 22.04 LTS
#### 7.1.3 S/W Tools & Techniques
- Backend: Python, Django 5.x, Django REST Framework
- Frontend: HTML5, CSS3, Tailwind CSS, JavaScript
- Version Control: Git & GitHub
- Database: SQLite (Development), PostgreSQL (Production)
#### 7.1.4 S/W Documentation
Documentation is maintained in Markdown format within the repository and comprehensive Microsoft Word/PDF documents detailing the thesis according to academic standards.
#### 7.1.5 Project Support Functions
Includes version control repositories, local development servers, database management tools (e.g., DBeaver, pgAdmin), and testing frameworks provided by Django.

## 2.8 Work Packages, Schedule and Budget
### 8.1 Work Packages
#### 8.1.1 Work Products
Deliverables tied to specific milestones, such as the completion of the authentication module, booking engine, agency dashboard, and final integrated system.
#### 8.1.2 Resource Requirements
Requires development workstations, a local network for initial testing, open-source software libraries (zero licensing cost), and minimal budget for cloud hosting and domain registration.

### 8.2 Budget & Resource Allocation
As an academic project, the financial budget is negligible, primarily involving time investment from the development team and minor costs associated with server hosting ($5-$10/month) for deployment.

### 8.3 Schedule
The schedule spans approximately 3 to 4 months, progressing logically from requirements gathering to final testing and deployment, with weekly sprint reviews to ensure adherence to timelines.


# CHAPTER 3: RISK MANAGEMENT PLAN

## Introduction
The Risk Management Plan for the Transport Management System (TMS) identifies, evaluates, and outlines mitigation strategies for potential risks that could negatively impact the project's success. It ensures proactive measures are in place to handle technical, scheduling, and operational uncertainties during the development lifecycle.

## Purpose
The primary purpose of this plan is to establish a systematic framework to foresee potential project hurdles. By defining a clear process for risk identification, assessment, and mitigation, the project team can minimize the impact of adverse events, ensuring the TMS is delivered on time, within budget, and to the required quality standards.

## Roles and Responsibilities
- **Project Manager:** Responsible for overall risk oversight, allocating resources for mitigation, and ensuring risk management activities are executed.
- **Lead Developer:** Identifies technical risks related to the Django framework, database schema, and system architecture.
- **QA Tester:** Identifies risks related to software defects, usability issues, and system performance bottlenecks.

## Risk Documentation
Risk documentation is maintained continuously throughout the project lifecycle. It serves as a historical record and a current tracking mechanism.

### Risk List
1. **R1 (Technical):** Database lockups or performance degradation due to complex multi-agency queries.
2. **R2 (Schedule):** Delays in frontend UI implementation due to the learning curve of Tailwind CSS.
3. **R3 (Scope):** Scope creep from attempting to implement live payment gateways instead of simulated ones.
4. **R4 (Operational):** Inadequate testing leading to critical bugs in the booking workflow.
5. **R5 (Resource):** Unavailability of key team members due to academic or personal reasons.

### Risk Data Items
For each identified risk, the following data items are recorded:
- **Risk ID:** Unique identifier (e.g., R1)
- **Description:** Clear explanation of the risk.
- **Probability:** Likelihood of occurrence (High, Medium, Low).
- **Impact:** Potential damage to the project (Critical, Moderate, Minor).
- **Mitigation Strategy:** Preemptive actions to prevent the risk.
- **Contingency Plan:** Actions to take if the risk materializes.

### Closing Risk
A risk is marked as "Closed" when it has either been successfully mitigated (its probability reduced to zero), or the project phase in which the risk was relevant has concluded without the risk occurring.

## Activities
Risk management involves iterative activities:
1. **Identification:** Brainstorming and analyzing project constraints.
2. **Assessment:** Quantifying the probability and impact of each risk.
3. **Mitigation Planning:** Formulating actionable steps to reduce risk exposure.
4. **Monitoring:** Reviewing risks during weekly sprint meetings.

### Schedules for Risk Management Activities
Risk assessments are conducted at the onset of every major project phase (e.g., before starting Database Design, before starting Frontend Implementation). Weekly status meetings include a mandatory 15-minute review of the Risk List.

## Risk Management Budget
The budget for risk management is incorporated into the overall project time allocation. Approximately 5-10% of the weekly development hours are reserved as a buffer to address unforeseen technical hurdles or debugging requirements.

## Risk Management Tools
The project utilizes open-source project management tools (e.g., Trello or GitHub Projects) to track risks as actionable cards, allowing the team to assign responsibilities, add comments, and move risks through different resolution stages.

## Introduction, Usability, Strength
The risk management approach emphasizes **usability** by keeping documentation lightweight and integrated into daily workflows, avoiding excessive bureaucratic overhead. Its core **strength** lies in its proactive nature, ensuring the development team remains agile and prepared for challenges, ultimately safeguarding the delivery of the TMS.

---

# CHAPTER 4: REQUIREMENT ANALYSIS & SPECIFICATION

## 1. Introduction
### 1.1 Purpose
This chapter delineates the software requirements for the Transport Management System (TMS). It provides a detailed breakdown of functional and non-functional requirements, acting as a binding agreement between the stakeholders (academic supervisors) and the development team regarding what the system will accomplish.

### 1.2 Scope
The scope encompasses a web-based platform tailored for inter-city bus transport. It covers passenger booking functionalities, agency fleet management, and super-admin oversight. It explicitly excludes native mobile application development and hardware-level integrations (like physical ticket printing kiosks).

### 1.3 Overview
The chapter is structured to first provide a general description of the system's perspective and users, followed by granular functional requirements categorized by user roles, non-functional constraints, and the required project deliverables.

## 2. General Description
### 2.1 Product Perspectives
TMS operates as an independent, monolithic web application hosted on a cloud server. It interfaces with internet browsers on the client side and utilizes a relational database (SQLite/PostgreSQL) on the backend. It represents a shift from decentralized, manual booking methods to a centralized digital hub.

### 2.2 Product Functions
- **Search & Filter:** Find bus trips by origin, destination, and date.
- **Seat Booking:** Interactively select available seats from a visual bus layout.
- **Digital Ticketing:** Generate QR-coded tickets sent via email.
- **Fleet Management:** Add/Edit/Delete buses, routes, and schedules.
- **Platform Administration:** Approve or suspend transport agencies.

### 2.3 User Characteristics
- **Passengers:** General public with basic internet literacy. Require an intuitive, simple interface.
- **Agency Managers:** Transport company staff with moderate technical proficiency. Need robust data management tools.
- **Administrators:** Technically proficient users overseeing platform security and agency vetting.

### 2.4 General Constraints
#### 2.4.1 The Product
The product must operate entirely within a web browser without requiring client-side installations.
#### 2.4.2 Hardware Constraints
The server must support concurrent connections corresponding to expected traffic (initially scaled for hundreds of concurrent users).
#### 2.4.3 Guide Lines
Development must adhere to PEP 8 standards for Python code and semantic HTML guidelines for accessibility.

## 3. Specification Requirements

### 3.1 Functional Requirements

**Functional Requirements of Administrator:**
- **FR_A1:** The admin shall securely log into a superuser dashboard.
- **FR_A2:** The admin shall have the ability to view all registered transport agencies.
- **FR_A3:** The admin shall approve or reject pending agency registration requests.
- **FR_A4:** The admin shall have the authority to suspend active agencies for policy violations.
- **FR_A5:** The admin shall view platform-wide statistics (total bookings, active users, total agencies).

**Functional Requirements of User/Member (Passenger):**
- **FR_U1:** The user shall register an account using an email address and password.
- **FR_U2:** The user shall search for trips specifying origin city, destination city, and travel date.
- **FR_U3:** The user shall view a list of available trips, comparing prices, agency names, and departure times.
- **FR_U4:** The user shall select specific seats from a graphical bus layout.
- **FR_U5:** The user shall complete a simulated payment process to confirm a booking.
- **FR_U6:** The user shall receive a booking confirmation email containing a digital QR ticket.
- **FR_U7:** The user shall view their booking history in their profile dashboard.

**Functional Requirements of Agency Manager:**
- **FR_AG1:** The agency manager shall register their transport company (pending admin approval).
- **FR_AG2:** The agency manager shall manage their fleet (add/edit buses, specify total seats).
- **FR_AG3:** The agency manager shall define routes and scheduled trips.
- **FR_AG4:** The agency manager shall view all bookings made for their agency's trips.
- **FR_AG5:** The agency manager shall assign drivers to specific scheduled trips.

### 3.2 Nonfunctional Requirements

- **Design Constraints:** The UI must be developed using Tailwind CSS to ensure rapid styling and responsiveness. The backend must strictly use the Django framework.
- **Performance Requirements:** The system should load the trip search results within 2 seconds under normal network conditions.
- **Business Process:** The system must enforce the rule that an agency cannot schedule trips until approved by an administrator.
- **Audit Trails:** The database must timestamp all booking creations and modifications.
- **Traceability:** Requirements must be mapped directly to test cases in the testing phase.
- **Consistency:** The UI must maintain a consistent color scheme and typography across all passenger and agency views.
- **Reliability:** The system should achieve 99% uptime during the evaluation phase.
- **Error Tolerance:** The system must gracefully handle invalid user inputs (e.g., booking a past date) with clear error messages rather than crashing.
- **Simplicity:** The passenger booking flow must be completable in under 5 clicks from the search results page.
- **Documentation:** Code must include inline comments (docstrings) for all complex logic and API endpoints.
- **Coding Standards:** Adherence to Python PEP 8.
- **Testing With Code Reviews:** All core modules (booking logic, seat availability calculation) must undergo peer review before integration.
- **Other Requirements:** Passwords must be securely hashed using Django's default PBKDF2 algorithm.

## 4. Required Deliverables
### 4.1 Requirement Specification Document
This document itself serves as the formal specification, outlining the exact parameters of the TMS project.
### 4.2 Installation Software
A `requirements.txt` file detailing Python dependencies, and a `setup.bat` or shell script to automate the initialization of the local environment.
### 4.3 User Training
Given the intuitive design, formal training is minimal. However, contextual tooltips will be provided within the agency dashboard.
### 4.4 User Guide/Manual
A dedicated section detailing how to navigate the system, primarily focused on agency managers learning the fleet management tools.

## General Descriptions & Development Environment
The development environment is configured with Python 3.1x, Django 5.x, SQLite for local storage, and Git for version control.

## Decomposition Descriptions & Use Cases Scenarios

### Real Use Cases
- **Passenger Booking:** Passenger searches for a bus from Lahore to Islamabad, views seat layout, selects Seat 12, proceeds to checkout, and receives a ticket.
- **Agency Scheduling:** Agency manager adds a new "Volvo 9900", creates a route from Karachi to Hyderabad, and schedules it for every Friday at 10:00 AM.

### Use Case Diagrams
*(In a formal document, a graphical UML Use Case Diagram is inserted here, illustrating the actors: Passenger, Agency, Admin, and their respective interactions with the TMS system boundaries).*

### Activity diagram
*(In a formal document, an Activity Diagram is inserted here showing the flow of the booking process: Start -> Search -> View Trips -> Select Seat -> Payment -> Generate Ticket -> End).*


# CHAPTER 5: SOFTWARE DESIGN

## Design Process Activities
The software design process for the Transport Management System (TMS) bridges the gap between the defined requirements and the actual code implementation. It involves systematically translating the functional specifications into a technical blueprint that the development team can build upon. The activities include defining the system architecture, designing the user interfaces, structuring the database, and planning the internal logic flow for complex operations like seat booking.

## Architectural Design
TMS follows a **Modular Monolithic Architecture** based on the Model-View-Template (MVT) pattern inherent to the Django framework. 
- **Model:** Handles data representation and database interactions (SQLite/PostgreSQL).
- **View:** Contains the business logic, processing user requests, interacting with models, and rendering templates.
- **Template:** The presentation layer utilizing HTML and Tailwind CSS to display data to the user.
Certain dynamic components, such as the seat selection grid, interact asynchronously with a lightweight REST API (built with Django REST Framework) to ensure a smooth, non-blocking user experience.

## Abstract Specification
The abstract specification defines the high-level services the system provides without detailing the internal implementation. For TMS, the primary service is the "Booking Engine," which guarantees that a seat selected by a passenger is locked temporarily during the payment process and cannot be booked by another user simultaneously.

## Interface Design
The user interface (UI) is designed with a mobile-first philosophy using Tailwind CSS. 
- **Passenger Interface:** Focuses on simplicity and conversion, featuring a prominent search bar on the homepage, clear trip listings, and intuitive visual seat maps.
- **Agency Dashboard:** A data-heavy interface requiring data tables, forms for scheduling, and analytical charts. It is designed for clarity and efficiency.
- **Admin Panel:** Utilizes Django's built-in, highly secure admin interface customized for agency approval workflows.

## Component Design
The system is divided into several loosely coupled Django apps:
1. **Accounts App:** Manages user authentication, roles (Admin, Passenger, Agency), and profiles.
2. **Agency App:** Handles fleet management, route definitions, and trip scheduling.
3. **Booking App:** Manages the search engine, seat selection logic, payment simulation, and ticket generation.

## Data Structure Design
Data structures in the application layer are primarily Django QuerySets and Python dictionaries. Complex data, such as a bus's seating layout (e.g., 2x2 or 2x1 configuration), is structured using JSON fields or calculated dynamically based on total seat counts and row configurations to render the UI grid.

## Algorithm Design
The core algorithm involves **Seat Availability Calculation**:
1. When a user searches a trip, the system retrieves the `Trip` object and its associated `Bus` capacity.
2. The system queries the `Booking` table for all confirmed bookings linked to that specific trip.
3. An array of booked seat numbers is generated.
4. The UI renders the bus layout, dynamically disabling/graying out the seat numbers present in the booked array.

## UI Design Supported by Possible Model
The UI design is highly responsive. Wireframes were created to model the flow from the "Search View" to the "Results View", and finally to the "Checkout View".

## System Model
### Object Model
The core objects include `User`, `Agency`, `Bus`, `Route`, `Trip`, `Booking`, and `Ticket`. These objects interact through defined Django models with appropriate foreign key relationships.

### Sequence Model
A typical sequence for booking:
1. `Passenger` requests trip search.
2. `System` queries `Trips`.
3. `System` returns available trips.
4. `Passenger` selects a trip and requests seat layout.
5. `System` returns seat map.
6. `Passenger` selects seats and confirms.
7. `System` creates a `Booking` record.

### Collaboration Diagram
*(In a formal document, this diagram illustrates how the passenger's browser collaborates with the Django backend and the Database to finalize a transaction).*

### State Transition Model
The `Booking` object undergoes several state transitions: 
- `Pending` (seat selected, awaiting payment)
- `Confirmed` (payment successful, ticket generated)
- `Cancelled` (user or agency cancelled).

### Structural Model
The structural model is defined by the Django project layout: project settings root, standard apps (accounts, agency, booking), static files directory (Tailwind CSS, JS), and templates directory.

### Data Flow Model
Data flows from the client (HTML forms/AJAX) -> Django URL Router -> Django View (Validation/Logic) -> Django Model (Database interaction) -> View (Response Generation) -> Client (Rendered Template/JSON).

---

# CHAPTER 6: DATABASE DESIGN

## Conceptual Design
### Business Rules
1. A Passenger can make multiple Bookings.
2. An Agency can own multiple Buses and define multiple Routes.
3. A Trip must be associated with exactly one Route and exactly one Bus.
4. A Booking must be tied to one Passenger and one Trip.
5. Two Bookings on the same Trip cannot reserve the same Seat Number.
6. An Agency must be approved by the Admin before creating Trips.

### Data Dictionary
| Table Name | Field Name | Data Type | Description |
|------------|------------|-----------|-------------|
| **User** | id | Integer (PK) | Unique user identifier |
| | email | Varchar | User's email (login credential) |
| | role | Varchar | Choice: Passenger, Agency, Admin |
| **Agency** | id | Integer (PK) | Unique agency identifier |
| | user_id | Integer (FK) | Link to User account |
| | name | Varchar | Transport company name |
| | is_approved | Boolean | Admin approval status |
| **Bus** | id | Integer (PK) | Unique bus identifier |
| | agency_id | Integer (FK) | Link to owning Agency |
| | reg_number | Varchar | Bus license plate |
| | total_seats | Integer | Seating capacity |
| **Trip** | id | Integer (PK) | Unique trip identifier |
| | bus_id | Integer (FK) | Assigned bus |
| | origin | Varchar | Starting city |
| | destination| Varchar | Ending city |
| | departure | DateTime | Scheduled departure time |
| | price | Decimal | Ticket cost per seat |
| **Booking**| id | Integer (PK) | Unique booking identifier |
| | user_id | Integer (FK) | Passenger who booked |
| | trip_id | Integer (FK) | Associated trip |
| | seat_num | Integer | Reserved seat number |
| | status | Varchar | Pending, Confirmed, Cancelled|

### ERD (Entity Relationship Diagram)
*(In a formal document, a visual ERD created in MS-Visio or similar tool is inserted here. It visually depicts the 1-to-many relationships between User->Booking, Agency->Bus, Agency->Trip, Bus->Trip, and Trip->Booking).*

## Logical Design
### Tool (SQL) Based Design
The logical design is abstracted by Django's Object-Relational Mapping (ORM). The ORM translates Python classes into SQL table creation scripts (migrations). The SQLite backend enforces foreign key constraints and unique constraints (e.g., `unique_together` on `trip` and `seat_num` in the Booking model to prevent double-booking).

## Physical Design
### Space and Size Consideration
The database is initially configured using SQLite for development, which stores data in a single `.sqlite3` file, minimizing configuration overhead. For production deployment, the design is fully compatible with PostgreSQL. Size considerations are minimal for text-based records; a database containing thousands of bookings will consume only a few megabytes. Image storage (e.g., agency logos, QR codes) is handled on the file system (or cloud bucket like AWS S3), storing only file paths in the database to optimize query performance and space.

---

# CHAPTER 7: TOOLS AND TECHNOLOGIES

The Transport Management System utilizes a modern, robust technology stack tailored for rapid development and scalable web deployment.

## 7.1 Backend Technologies
- **Python (3.1x):** The core programming language utilized for its readability and extensive ecosystem.
- **Django (5.x):** A high-level Python web framework that encourages rapid development and clean, pragmatic design. It handles ORM, routing, and authentication out of the box.
- **Django REST Framework (DRF):** A powerful toolkit for building Web APIs, used to serve dynamic data (like seat availability) to the frontend asynchronously.

## 7.2 Frontend Technologies
- **HTML5 & CSS3:** The foundational markup and styling languages.
- **Tailwind CSS:** A utility-first CSS framework used for rapidly building custom, responsive user interfaces directly within HTML templates without writing external CSS files.
- **JavaScript (Vanilla):** Used for client-side interactivity, DOM manipulation (e.g., selecting seats on the grid), and asynchronous API requests (AJAX/Fetch).

## 7.3 Database Technologies
- **SQLite:** A C-language library that implements a small, fast, self-contained SQL database engine. Used as the default database for local development and testing.
- **PostgreSQL (Target Production):** An advanced, enterprise-class open-source relational database, planned for production deployment due to its robustness in handling concurrent transactions.

## 7.4 Development & Management Tools
- **Git & GitHub:** Used for version control, collaborative development, and maintaining the project repository.
- **Visual Studio Code (VS Code):** The primary Integrated Development Environment (IDE) utilized by the development team.
- **pip & virtualenv:** Python tools used for dependency management and creating isolated project environments.
- **qrcode (Python Library):** Used specifically for generating the visual QR code images embedded in the digital tickets.


# CHAPTER 8: TESTING

## Software Test Plan

### Product Visualization
The testing phase evaluates the Transport Management System (TMS) from multiple angles: frontend usability, backend logic accuracy, database integrity, and security (role-based access). The goal is to ensure the product behaves identically to the specifications outlined in Chapter 4 under both normal and edge-case conditions.

### Time Limit
Testing is allocated a dedicated two-week timeframe (Weeks 11-12 of the project lifecycle), allowing iterative cycles of bug discovery, patching, and regression testing.

### Team for Testing
Testing is conducted collaboratively by the development team (peer-testing code modules) and an independent QA tester who approaches the system from an end-user perspective.

### Decomposition Module
The system is tested in isolated modules before integration:
1. **Authentication Module:** Registration, Login, Password Hashing.
2. **Agency Management Module:** Fleet CRUD operations, Trip scheduling.
3. **Booking Engine Module:** Search filtering, Seat availability algorithms, Booking state transitions.
4. **Integration/E2E:** Full flow from passenger login to ticket generation.

### Description of Plan
The test plan relies primarily on manual functional testing and unit testing utilizing Django's built-in `TestCase` framework for critical backend logic (e.g., verifying a seat cannot be double-booked). 

---

## TESTING

### 1. Introduction
#### 1.1 Product Name
Transport Management System (TMS)

#### 1.2 Test Cases Developed by
The TMS QA & Development Team.

#### 1.3 Document Generated by
QA Lead

#### 1.4 Date
[Insert Current Date]

#### 1.5 Test Report Reference Number
TMS-TR-001

### 3. Test Cases

| Test ID | Module | Description | Inputs | Expected Output | Status |
|---------|--------|-------------|--------|-----------------|--------|
| TC-01 | Auth | Passenger Registration | Valid email, password | Account created, redirected to login | Pass |
| TC-02 | Auth | Invalid Login | Wrong password | Error message: "Invalid credentials" | Pass |
| TC-03 | Agency | Add Bus | Reg Num: XYZ-123, Seats: 45 | Bus added to agency fleet | Pass |
| TC-04 | Booking| Search Trip | Origin: LHR, Dest: ISB, Date | List of available trips matching criteria | Pass |
| TC-05 | Booking| Double Booking | User A and B select Seat 10 | First confirms; Second gets "Seat Unavailable" | Pass |
| TC-06 | Admin | Approve Agency | Admin clicks "Approve" | Agency status turns Active, can schedule trips | Pass |

### 4. Test Case Execution
Test cases are executed initially in the local development environment (`DEBUG=True`). Following successful local tests, the system is deployed to a staging server where test cases are re-executed to identify environment-specific bugs.

### 5. Test Case Report
A comprehensive report detailing all failed tests, the severity of the bugs, and the steps taken to resolve them. During the TMS development, a critical bug identified involved time-zone mismatches causing trips to disappear prematurely from search results. This was patched by enforcing UTC standardization across all Django timezone settings.

---

# CHAPTER 9: APPLICATION DEPLOYMENT AND USER GUIDE LINES

## 9.1 Application Deployment Strategy
The deployment strategy for TMS aims to transition the software from a local development environment to a live, publicly accessible cloud server. 

1. **Server Provisioning:** A Linux VPS (Ubuntu) is provisioned.
2. **Environment Setup:** Python, Gunicorn (WSGI server), Nginx (Reverse Proxy), and PostgreSQL are installed.
3. **Code Transfer:** The repository is cloned to the server via Git.
4. **Configuration:** Environment variables (`.env`) are configured for production (e.g., `DEBUG=False`, production database credentials, secret keys).
5. **Static File Gathering:** Django's `collectstatic` command is run to bundle Tailwind CSS and JavaScript for Nginx to serve efficiently.
6. **Database Migration:** Production database schema is applied.
7. **Process Management:** Supervisor or systemd is used to keep the Gunicorn process running continuously.

### 9.1.1 Deployment diagram
*(In a formal document, a UML Deployment Diagram illustrates the physical topology: Client Browser -> Internet -> Nginx (Port 80/443) -> Gunicorn (Port 8000) -> Django Application -> PostgreSQL DB).*

## 9.2 Maintenance Considerations
Post-deployment maintenance involves:
- **Regular Backups:** Automated daily dumps of the PostgreSQL database.
- **Security Updates:** Periodically updating Python packages and the Ubuntu OS to patch vulnerabilities.
- **Monitoring:** Utilizing basic server monitoring tools to track CPU and memory usage, ensuring the server scales if passenger traffic spikes.

## 9.3 User Guide
### Passenger Guide
1. Navigate to the TMS homepage.
2. Use the search bar to enter your departure city, arrival city, and date.
3. Review the available trips and click "Select Seats" on your preferred option.
4. Click on green (available) seats on the bus map. Selected seats turn blue.
5. Click "Proceed to Payment".
6. Complete the (simulated) payment form.
7. Check your email or your Profile Dashboard to view your digital QR ticket.

### Agency Manager Guide
1. Register for an Agency Account (wait for admin approval).
2. Log in and navigate to the Agency Dashboard.
3. Go to "Fleet Management" -> "Add Bus" to register your vehicles.
4. Go to "Routes" to define the cities you operate between.
5. Go to "Schedule Trip" to combine a Route, a Bus, and a Time/Date.
6. Monitor the "Bookings" tab to see real-time passenger reservations for your trips.

---

# APPENDIX

## References
1. Django Software Foundation. (2024). *Django Documentation*. Retrieved from https://docs.djangoproject.com/
2. Tailwind Labs. (2024). *Tailwind CSS Documentation*. Retrieved from https://tailwindcss.com/docs
3. Encode OSS. (2024). *Django REST Framework*. Retrieved from https://www.django-rest-framework.org/
4. Sommerville, I. (2015). *Software Engineering* (10th ed.). Pearson.
5. Pressman, R. S. (2014). *Software Engineering: A Practitioner's Approach* (8th ed.). McGraw-Hill Education.


