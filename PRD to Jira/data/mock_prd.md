# tpm-toolkit

# Product Requirements Document (PRD) Sample Text to paste into PRD to Jira Generator
## Project Name: Project VibeCheck (Next-Gen Visual Social Platform)
## Document Version: 1.2
## Author: Principal Product Manager

### 1. Product Vision & Overview
Project VibeCheck is a mobile-first visual social platform designed to directly compete with Instagram. The platform targets Gen-Z creators by prioritizing real-time authentication, ultra-low latency media feeds, and programmatic privacy guardrails. 

Our core differentiator is "Zero-Friction Discovery," which uses strict metadata tags to aggregate global feeds instantly without heavy client-side processing.

---

### 2. Core Functional Requirements

#### Module 2.1: User Authentication & Database Validation Layer
The onboarding pipeline must balance absolute security with consumer conversion metrics.
* **Functional Spec:** Users must be able to sign up or log in securely using their email or external OAuth 2.0 social handles (Apple and Google accounts).
* **System Constraint:** The authentication engine must validate input credentials against our central distributed database cluster using a cryptographically secure verification layer.
* **Security Guardrail:** To mitigate brute-force and credential-stuffing security risks, the system must detect invalid attempts. Upon exactly the 3rd consecutive failed login attempt, the user's account must immediately transition to a temporary 'Locked' state for 15 minutes. 
* **Audit Compliance:** Every authentication execution (successful or failed) must generate a secure, audited metadata transaction log tracking timestamps, IP mask vectors, and error event codes.

#### Module 2.2: Media Upload, Image Compression, & Asset Delivery
Creators require instant publishing mechanics, which mandates automated background optimization.
* **Functional Spec:** Users can tap an upload interface action to publish a single high-definition photo or video asset directly to their global feed canvas.
* **System Constraint:** The upload pipeline must intercept raw assets and run them through our asynchronous compression worker. Images must automatically resize and compress into an optimized WebP formatting payload to minimize bandwidth overhead.
* **Storage Matrix:** Cleaned compressed assets must stream securely to our cloud object storage buckets. Once written, the system must inject a fresh relational asset reference row linking the media asset URL directly to the user's relational profile table schema.

#### Module 2.3: Zero-Friction Real-Time Media Discovery Feed
The core experience depends entirely on a smooth, uninterrupted browsing canvas.
* **Functional Spec:** The primary application screen displays a vertically scrolling feed showing content from followed users alongside globally trending media recommendations.
* **System Constraint:** To protect consumer engagement scores, the media delivery service must prioritize speed. The feed aggregation query must parse, sort, and serve content assets within a maximum database lookup and compilation latency boundary of 200 milliseconds.
* **Network Playback Guardrail:** The system must pre-fetch the upcoming 2 media assets in the background, ensuring content rendering occurs seamlessly without showing loading stubs or dropped network playback frames during user scroll interactions.

---

### 3. Non-Functional Performance Thresholds
* **Global Latency Boundary:** API network gateways must process standard client requests within 100ms.
* **Database Target Performance:** Media reference compilation arrays must complete lookups in under 200ms.
* **Data Log Capture Velocity:** Automated transaction security metadata records must be written and finalized in storage within exactly 1 second of execution.
