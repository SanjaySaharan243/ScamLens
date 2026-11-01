# 🛡️ ScamLens --- Suspicious Message Pattern Explorer

**ScamLens** is a Streamlit-based message intelligence application that
helps users inspect suspicious SMS messages, emails, and other text
messages. It highlights recognizable warning signs, assigns a rule-based
risk score, explains the signals that matched, and stores analyses in
MongoDB for later review.

> **Live demo:** https://scamlensweb.streamlit.app/
> 
> **Source code:** https://github.com/SanjaySaharan243/ScamLens

------------------------------------------------------------------------

## Table of Contents

-   [Overview](#overview)
-   [Why ScamLens?](#why-scamlens)
-   [Features](#features)
-   [How It Works](#how-it-works)
-   [Risk Scoring](#risk-scoring)
-   [Technology Stack](#technology-stack)
-   [Application Sections](#application-sections)
-   [Database Design](#database-design)
-   [Project Structure](#project-structure)
-   [Run Locally](#run-locally)
-   [Environment Configuration](#environment-configuration)
-   [Deploy on Streamlit Community
    Cloud](#deploy-on-streamlit-community-cloud)
-   [Deploy on Render](#deploy-on-render)
-   [Example Messages to Test](#example-messages-to-test)
-   [Limitations and Responsible Use](#limitations-and-responsible-use)
-   [Future Improvements](#future-improvements)
-   [Author](#author)
-   [License](#license)

------------------------------------------------------------------------

## Overview

ScamLens is an educational cybersecurity project focused on
**explainable message-pattern analysis**. Rather than returning only a
label, it shows the warning signals that contributed to a message's
score so users can review the reasoning.

The current version uses predefined regular-expression rules and
optional custom rules stored in MongoDB. It is **not a trained
machine-learning model** and does not verify whether a sender, website,
phone number, or payment request is genuine.

## Why ScamLens?

Suspicious messages often rely on social-engineering techniques such as
urgency, threats, requests for OTPs or PINs, unexpected fees, prize
claims, fake account-verification links, and requests to install
remote-access applications.

ScamLens brings several common warning patterns into one interface so a
user can:

-   Inspect a message before acting on it.
-   See which warning patterns were detected.
-   Review a heuristic risk score and risk category.
-   Save a record for later review.
-   Explore patterns across saved analyses.

## Features

-   **Message scanner:** Analyze pasted message text.
-   **Explainable warning signals:** Show the built-in or custom
    patterns that matched.
-   **Rule-based risk score:** Calculate a score from matched signal
    weights, capped at 100.
-   **Risk classification:** Categorize results as Low, Medium, or High
    according to the configured thresholds.
-   **URL pattern checks:** Flag links and selected suspicious URL
    structures. This is pattern inspection, not a live reputation or
    ownership check.
-   **Hinglish and selected Hindi indicators:** Recognize a selection of
    common OTP, payment-pressure, KYC, and prize-related phrases.
-   **MongoDB persistence:** Save analyses for later review.
-   **Analysis history:** Browse saved records, filter them, review
    details, and update review status or notes where available in the
    interface.
-   **Pattern Explorer:** Summarize saved records by risk level and
    matched signals using MongoDB aggregation.
-   **Custom rules:** Load active patterns from the MongoDB
    `scam_patterns` collection.
-   **Record management:** Delete saved analysis records.
-   **Dashboard:** View saved-analysis totals and risk distribution.
-   **Dark responsive interface:** Built with Streamlit and custom CSS.

## How It Works

1.  **Input:** The user pastes a suspicious message into the scanner.
2.  **Pattern matching:** ScamLens checks the text against built-in
    regular-expression rules and any valid active custom rules retrieved
    from MongoDB.
3.  **Signal collection:** Each matched rule contributes a named warning
    signal and a configured weight. A signal is counted once even if its
    pattern appears multiple times.
4.  **URL inspection:** The app applies additional checks to URLs found
    in the message, including selected unusual URL structures.
5.  **Score calculation:** Matched weights are added together, and the
    result is capped at 100.
6.  **Risk category:** The score is mapped to Low, Medium, or High.
7.  **Explanation:** The app displays the detected signals and explains
    that the score is heuristic rather than a verified probability of
    fraud.
8.  **Storage and exploration:** When saved, the analysis is written to
    MongoDB and can be reviewed in the history and dashboard sections.

### Built-in pattern families

The current rule set includes examples from these families:

-   Requests for OTPs, PINs, passwords, or banking details
-   KYC and account-verification pressure
-   Account blocking, suspension, or service-disconnection threats
-   UPI requests, QR-code manipulation, and unexpected payment demands
-   Advance, processing, joining, or release fees
-   Urgency, threats, penalties, and legal-action language
-   Lottery, prize, giveaway, and reward claims
-   Suspicious job offers and guaranteed-earnings promises
-   Investment, trading, and cryptocurrency claims
-   Parcel, courier, delivery, and customs-fee messages
-   Links, IP-address URLs, deceptive URL structures, and selected
    suspicious URL wording
-   Remote-access applications and unknown APK installation requests
-   Friend-or-family emergency money requests and impersonation cues
-   Selected Hinglish and Hindi warning phrases
-   Identity-document requests, gift-card payments, and account-recovery
    offers

These are pattern indicators, not proof that a message is fraudulent.

## Risk Scoring

The score is a **heuristic screening score**, not a statistical
probability.

  ------------------------------------------------------------------------
                         Score Category              Interpretation
  ---------------------------- --------------------- ---------------------
                         0--29 Low                   Fewer configured
                                                     warning patterns
                                                     matched

                        30--59 Medium                Several or
                                                     higher-weight warning
                                                     patterns matched;
                                                     review carefully

                       60--100 High                  Multiple or
                                                     high-weight warning
                                                     patterns matched;
                                                     take extra care
  ------------------------------------------------------------------------

The score is capped at 100. Individual rules have configured weights,
and the weights of matched signals are added together.

**Important:** A Low score does not mean a message is safe. A message
can be dangerous even when no known rule matches, and a legitimate
message can contain language that resembles a warning pattern. Always
verify the sender through an independent, trusted channel.

## Technology Stack

  Technology                   Purpose
  ---------------------------- ------------------------------------------------------
  Python                       Application logic and rule-based analysis
  Streamlit                    Interactive web interface and dashboard
  Regular expressions (`re`)   Detect configured message patterns
  pandas                       Prepare tabular data for history and dashboard views
  PyMongo                      Connect to MongoDB and perform database operations
  MongoDB Atlas                Cloud storage for analyses and optional custom rules
  python-dotenv                Load local environment variables from `.env`
  Git and GitHub               Source control and project hosting
  Streamlit Community Cloud    Public Streamlit deployment

## Application Sections

### 1. Overview

Shows saved-analysis totals, counts by risk category, risk distribution,
and quick actions.

### 2. Message Scanner

Accepts message text, checks it against configured rules, displays a
score and risk category, and lists matched warning signals.

### 3. Analysis History

Provides access to previously saved analyses. Available
record-management actions include reviewing records, updating review
status or notes, and deleting records.

### 4. Pattern Explorer

Uses saved analysis data to summarize risk categories and matched
signals. Its results depend on the analyses stored in the database.

### 5. About ScamLens

Explains the project's purpose, rule-based approach, and limitations.

## Database Design

ScamLens connects to MongoDB using PyMongo. The configured database is
`scamlens_db`.

### `analyses` collection

Stores saved analysis records. A record includes information such as:

-   Original message text
-   Risk score
-   Risk level
-   Matched signals
-   Analysis timestamp
-   Review-related fields where applicable

The app creates indexes for fields including analysis timestamp, risk
level, and risk score to support common queries.

### `scam_patterns` collection

Optional collection for custom rules. Active documents use this general
structure:

``` json
{
  "signal": "Custom scam phrase",
  "pattern": "example phrase|another phrase",
  "weight": 25,
  "active": true
}
```

-   `signal`: Label shown when the pattern matches.
-   `pattern`: A Python-compatible regular expression.
-   `weight`: Integer weight from 1 to 40.
-   `active`: Set to `true` to enable the rule.

Only add patterns you trust. Invalid regular expressions are skipped by
the application. If the custom collection is empty or unavailable, the
built-in rules are designed to remain available.

## Project Structure

The repository's main application files are expected to include:

``` text
ScamLens/
├── app.py             # Streamlit interface, rules, analysis, and database operations
├── requirements.txt   # Python dependencies for deployment
├── .env               # Local secrets; do not commit this file
├── .gitignore         # Excludes secrets, virtual environments, and generated files
└── README.md          # Project documentation
```

Your repository may contain additional files depending on your local
setup.

## Run Locally

### Prerequisites

-   Python 3.10 or a compatible Python version supported by your
    dependencies
-   Git
-   A MongoDB Atlas cluster, or another MongoDB deployment reachable
    from your machine

### 1. Clone the repository

``` bash
git clone https://github.com/SanjaySaharan243/ScamLens.git
cd ScamLens
```

### 2. Create and activate a virtual environment

**macOS / Linux**

``` bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows PowerShell**

``` powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

``` bash
pip install -r requirements.txt
```

### 4. Configure MongoDB

Create a `.env` file in the project root and add your connection string:

``` dotenv
MONGODB_URI="your_actual_mongodb_connection_string"
```

Use the connection string provided by MongoDB Atlas. If it includes
query parameters such as `retryWrites=true&w=majority`, preserve them
without duplicating parameters. Make sure special characters in the
database password are URL-encoded.

### 5. Start the app

``` bash
python -m streamlit run app.py
```

Open the local URL printed in the terminal, usually
`http://localhost:8501`.

## Environment Configuration

The application needs the `MONGODB_URI` secret to access MongoDB.

### Local development

Use the `.env` file. Make sure `.env` is listed in `.gitignore`.

### Streamlit Community Cloud

Open the app's settings, find **Secrets**, and add:

``` toml
MONGODB_URI = "your_actual_mongodb_connection_string"
```

Save the settings and reboot or redeploy the app if required.

### Render

In your Render service, open **Environment**, add an environment
variable named `MONGODB_URI`, and set its value to your real MongoDB
Atlas connection string.

### Security reminders

-   Never commit `.env`, database passwords, or connection strings to
    GitHub.
-   Never paste credentials into public issues, screenshots, or README
    files.
-   Use a dedicated database user with only the permissions the
    application needs.
-   Configure MongoDB Atlas Network Access deliberately. Avoid leaving
    `0.0.0.0/0` enabled as a permanent shortcut.
-   If a credential has been exposed, rotate it in MongoDB Atlas
    immediately.

## Deploy on Streamlit Community Cloud

1.  Push the project to GitHub.
2.  Open [Streamlit Community Cloud](https://share.streamlit.io/).
3.  Create an app and select the `SanjaySaharan243/ScamLens` repository.
4.  Select the `main` branch and `app.py` as the main file.
5.  Add `MONGODB_URI` under the app's Secrets settings.
6.  Deploy and inspect the logs if startup or database connectivity
    fails.

Official documentation: [Deploy an
app](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy)
· [Secrets
management](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/secrets-management)

## Deploy on Render

1.  Create a new Web Service and connect the GitHub repository.

2.  Select the `main` branch and Python 3 runtime.

3.  Set the build command:

    ``` bash
    pip install -r requirements.txt
    ```

4.  Set the start command:

    ``` bash
    streamlit run app.py --server.port $PORT --server.address 0.0.0.0
    ```

5.  Add `MONGODB_URI` under Environment Variables.

6.  Deploy and check the logs if the app fails to start or connect to
    MongoDB.

Official documentation: [Render Web
Services](https://render.com/docs/web-services)

**Deployment note:** A successful app build does not guarantee that the
MongoDB connection is working. If the app reports TLS handshake errors
or `ReplicaSetNoPrimary`, check Atlas cluster status, Network Access,
database credentials, and the hosting environment's connectivity. Do not
disable TLS certificate verification as a workaround.

## Example Messages to Test

Use fictional examples only. These examples are illustrative and do not
establish a real-world scam determination.

### Example A --- OTP request

``` text
Your bank account will be blocked today. Share your OTP immediately to verify your account.
```

Potential signals include account-blocking pressure, urgency, and a
request for an OTP.

### Example B --- Unexpected fee

``` text
Congratulations, you won a prize. Pay a processing fee to release your reward.
```

Potential signals include prize bait and an advance or release fee.

### Example C --- Suspicious link

``` text
Your account requires verification: https://example.com/verify-account
```

Potential signals include a link and wording associated with account
verification. The app does not establish whether the domain is
malicious.

### Example D --- Ordinary message

``` text
Hi, our study group meeting is at 4 PM in the library. See you there.
```

Few or no built-in warning patterns may match. That does not prove the
message or sender is safe.

## Limitations and Responsible Use

-   ScamLens uses configured rules; this version does not train or run a
    machine-learning classifier.
-   The risk score is not a calibrated probability, legal determination,
    or guarantee of fraud.
-   A new or sophisticated scam may not match any existing rule.
-   Legitimate messages can produce false positives.
-   URL checks inspect text and structure only; they do not browse the
    destination, query threat-intelligence feeds, or verify website
    ownership.
-   Results depend on the quality and coverage of built-in and custom
    rules.
-   Message text can contain sensitive information. Prefer fictional or
    sanitized examples and avoid storing OTPs, passwords, financial
    details, or unnecessary personal data.
-   ScamLens is an educational screening aid, not a substitute for
    contacting your bank, service provider, or official fraud-reporting
    channel.

If a message asks you to share an OTP/PIN/password, install
remote-access software, transfer money urgently, or pay a fee to receive
a prize/refund, pause and verify the request independently using an
official channel.

## Future Improvements

Possible future extensions include:

-   More multilingual and regional scam-pattern coverage
-   URL reputation and domain-age checks through trusted external
    services
-   A configurable rules-management interface
-   Exportable reports and improved filtering
-   Unit tests and a curated test dataset for measuring false positives
    and false negatives
-   Optional machine-learning classification with transparent evaluation
    and explanations
-   Stronger privacy controls and retention settings

These are potential enhancements, not claims about functionality already
implemented.

## Author

**Sanjay Saharan**

-   GitHub: [@SanjaySaharan243](https://github.com/SanjaySaharan243)
-   Project repository:
    [ScamLens](https://github.com/SanjaySaharan243/ScamLens)
-   Live demo:
    [scamlensweb.streamlit.app](https://scamlensweb.streamlit.app/)

## License

No license has been specified in this README. Unless a license is added
to the repository, do not assume that the project is open-source under a
particular license. If you intend others to reuse, modify, or distribute
the code, consider adding an appropriate `LICENSE` file.
