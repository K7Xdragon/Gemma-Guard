# Gemma-Guard: Chronobiology AI to Prevent Burnout and Track Wellness

[![Releases](https://img.shields.io/badge/Releases-Download-blue?style=for-the-badge&logo=github)](https://github.com/K7Xdragon/Gemma-Guard/releases)

![Wellness time series](https://images.unsplash.com/photo-1505751172876-fa1923c5c528?auto=format&fit=crop&w=1400&q=80)

Table of contents
- What Gemma-Guard does
- Key features
- How it works (system overview)
- Chronobiology and burnout model
- Data sources and signals
- Gemma AI integration
- Architecture and components
- Installation (desktop and server)
- Running the streamlit app
- Command-line tools and examples
- Dataset format and labeling
- Model training and evaluation
- Explainability and outputs
- Privacy and data handling
- Security and operational notes
- Monitoring and metrics
- Tests and CI
- Deployment options
- Contributing guide
- Roadmap and issues
- License
- FAQ
- References and further reading

What Gemma-Guard does
- Gemma-Guard analyzes biometric and behavioral time-series to monitor wellness and detect early markers of burnout.
- It uses chronobiology signals, personality anchors, and machine learning. It integrates with Gemma AI to generate context-aware assessments and nudges.
- It produces a timeline of risk scores, driver attributions, and personalized recommendations that align with a user's chronotype and daily rhythm.

Key features
- Multimodal input: heart rate, HRV, sleep, activity, calendar, self-reports, and device metadata.
- Temporal feature engine: extracts circadian and ultradian patterns, phase shifts, amplitude changes, and regularity metrics.
- Burnout risk model: combines physiological stress, sleep disruption, workload, and personality data.
- Gemma AI integration: context-driven summaries, conversational checks, and behavior-aware nudges.
- Streamlit interface: visual dashboards, interactive timelines, and exportable reports.
- CLI for batch processing and scheduling.
- Extensible Python modules for custom feature extraction and model plugins.
- Privacy-first design: local processing and encryption-ready pipelines.

Badges and links
- Releases: [Download and execute release package](https://github.com/K7Xdragon/Gemma-Guard/releases)  
  The releases page contains packaged builds and installers. Download the release artifact that matches your platform and run the included installer or script.

Repository topics
ai, biometrics, burnout, burnout-prevention-tech, chronotype, gemma, healing, healthcare-ai, machine-learning, ollama, personality-analysis, python, streamlit, stress-monitoring, technology, temporal-analysis, wellness, wellness-app

Why this project
- Burnout harms people and organizations. Early detection improves outcomes.
- Chronobiology reveals when the body and mind handle stress better.
- Combining physiological signals with behavioral context yields robust predictions.
- Gemma AI adds a human-like layer that explains drivers and suggests targeted actions.

Images and visual assets
- Cover and dashboard mockups use public domain and creative commons images. Use them for prototypes. Replace with organization assets for production.
- Example image sources:
  - Dashboard mockup: https://images.unsplash.com/photo-1505751172876-fa1923c5c528
  - Time-series concept art: https://images.unsplash.com/photo-1517245386807-bb43f82c33c4

How it works — system overview
Gemma-Guard follows four steps:
1. Ingest: collect streams and logs from wearables, phone sensors, calendars, and manual entries.
2. Process: normalize timestamps, handle gaps, resample, and compute temporal features.
3. Model: feed features into ensemble models and Gemma AI for blended scoring and explanations.
4. Act: render dashboards, push alerts, and generate personalized behavioral nudges.

Core concepts
- Chronotype: the user’s natural timing preference (morning vs. evening). We infer chronotype from sleep timing, activity peaks, and self-report.
- Circadian regularity: consistency of sleep/wake and activity over days. Lower regularity increases risk.
- HRV baseline and reactivity: baseline HRV tracks long-term resilience. Momentary drops indicate acute stress.
- Recovery windows: periods of parasympathetic dominance that enable recovery. Short or absent windows increase burnout risk.
- Allostatic load: cumulative load from repeated stressors. We estimate load from patterns of sleep debt, HRV suppression, and workload spikes.

Data sources and signals
Supported or easy-to-adapt inputs:
- Wearables: heart rate, HRV, skin temperature, step counts, sleep staging.
- Phone: screen on/off, ambient light, app usage, step counts.
- Calendar: meetings, duration, tags.
- Surveys: daily mood, perceived workload, stress rating.
- Clinical: optional psychometric scales (Maslach Burnout Inventory, PHQ-9).
- Manual logs: caffeine, naps, medication, travel.

Signal preprocessing
- Timestamp alignment: convert to UTC, apply user timezone, align to epoch.
- Resampling: use 1-min or 5-min windows for HR/HRV, hourly windows for activity and calendar.
- Gap handling: mark gaps > 30 min, do not impute physiological gaps. For short gaps, carry forward last known state for contextual features.
- Baseline estimation: use rolling 14-day median for HRV and resting HR.
- Artifact removal: simple heuristics for motion artifacts in HRV and HR (e.g., zero or extreme spikes).

Feature extraction (temporal)
- Circadian phase: compute daily activity peak, sleep midpoint, and phase shift relative to baseline.
- Amplitude features: compute day-to-day amplitude of activity and sleep duration. Low amplitude suggests flattened rhythm.
- Regularity metrics: interdaily stability (IS), intradaily variability (IV).
- Sleep metrics: sleep duration, sleep efficiency, wake after sleep onset (WASO), sleep timing.
- HRV metrics: RMSSD, SDNN, frequency domain features (LF/HF), and recovery index.
- Workload metrics: meeting density, uninterrupted work blocks, calendar burden.
- Behavioral metrics: phone use patterns aligned to bedtime, social activity proxies.

Burnout risk model
- Model structure: ensemble of temporal models and a transformer-style temporal aggregator for longer patterns.
- Inputs: temporal features above plus personality anchors and self-report.
- Output: continuous risk score [0, 1] and categorical label (Low, Moderate, High).
- Driver attribution: Shapley-inspired attribution to allocate score to sleep disruption, physiological strain, workload, or circadian misalignment.
- Calibration: we calibrate risk to base rates using isotonic regression on a labeled cohort.

Gemma AI integration
- Gemma AI acts as the natural-language layer:
  - Summaries: "Your sleep midpoints shifted 1.5 hours later this week."
  - Context: "Your HRV reduced after three consecutive days of long meetings."
  - Nudges: "Shift start time by 30 minutes and schedule a 15-minute low-intensity break after long meetings."
- Integration points:
  - Explainable summaries for each daily report.
  - Conversational check-ins that adapt questions based on recent trend.
  - Recommendation engine that maps drivers to specific interventions.
- Model orchestration:
  - Gemma receives structured model outputs and contextual metadata.
  - Gemma returns plain-language explanations, prioritization, and follow-up actions.
- Offline operation:
  - We ship a local Gemma-compatible model option using Ollama for on-device inference.
  - Server-hosted Gemma option captures richer context for teams.

Architecture and components
- Core modules:
  - ingestion/: adapters for devices and APIs
  - processing/: preprocessing and feature extraction
  - modeling/: model definitions, training scripts, evaluation
  - ui/: Streamlit app and static assets
  - cli/: command-line tools for batch ops
  - examples/: sample scripts and notebooks
- Data flow:
  - Device -> ingestion -> processed events -> feature store -> model engine -> UI/API
- Storage:
  - Feature store: SQLite for local, PostgreSQL for server deployments.
  - Models: versioned with model cards and fingerprints.
  - Logs: structured logs for audits.

Installation and quick start
Supported platforms: macOS, Linux, Windows Subsystem for Linux. We recommend Python 3.10+ and a virtual environment.

1) Clone the repo
```bash
git clone https://github.com/K7Xdragon/Gemma-Guard.git
cd Gemma-Guard
```

2) Create virtual env and install
```bash
python -m venv .venv
source .venv/bin/activate   # on Windows use .venv\Scripts\activate
pip install -r requirements.txt
```

3) Download packaged release and execute
- Visit and download a release artifact from the Releases page: https://github.com/K7Xdragon/Gemma-Guard/releases  
  Pick the artifact that matches your OS. The release contains a setup script or installer. Run the provided script. Example:
```bash
# After downloading the release artifact (example: gemma-guard-linux.tar.gz)
tar -xzf gemma-guard-linux.tar.gz
cd gemma-guard
./install.sh
```
The installer places CLI tools and a local Streamlit app.

If you prefer to run from source, use:
```bash
streamlit run ui/app.py
```

Running the Streamlit app
- Default launch:
```bash
streamlit run ui/app.py --server.port 8501
```
- The app uses a local feature store. To load example data:
```bash
python examples/load_example_dataset.py --target ./data/example.db
```
- The UI shows:
  - Dashboard: timeline with risk bands, HRV and sleep overlays.
  - Driver view: per-driver attributions and recommendations.
  - Timeline: interactive zoom and day-level drilldowns.
  - Export: PDF or CSV reports.

Command-line tools
- Batch processing
```bash
gemma process --input data/raw --output data/features.db
```
- Training
```bash
gemma train --config config/train.yaml --out models/latest
```
- Evaluate
```bash
gemma eval --model models/latest --data data/holdout.db --metrics reports/metrics.json
```
- Export report
```bash
gemma report --user-id 42 --out reports/user42.pdf
```

Example workflows
- Daily local use:
  - Wearable sync -> run gemma process (via scheduled cron) -> streamlit shows latest trends -> Gemma checks in for quick survey.
- Team pilot:
  - Central ingestion from optional cloud sync -> periodic aggregated reports for team leads (de-identified) -> targeted interventions.
- Research:
  - Use provided notebooks in examples/ for protocol replication. The code exports features in standard CSV or parquet.

Data format and labeling
- Internal schema:
  - events table: timestamp, source, metric, value, quality_flag
  - sleep table: start, end, stage_summary, efficiency
  - hr table: timestamp, hr, rr_intervals, quality
  - calendar: start, end, title, tags
  - survey: timestamp, item, value
- Labeling guidance:
  - Use daily labels for burnout risk for supervised tasks.
  - Label scale: 0 (none) - 3 (severe).
  - Align labels to user's local day (midnight to midnight, adjusted to sleep midpoint if needed).

Model training and evaluation
- Training recipe:
  1. Aggregate features per day or sliding-window.
  2. Balance classes by weighted loss or sampling.
  3. Use temporal cross-validation (blocked CV) to avoid leakage.
  4. Train ensemble: gradient-boosted trees + temporal CNN + transformer aggregator.
  5. Calibrate and produce driver attributions.
- Metrics:
  - ROC-AUC, PR-AUC for classification.
  - MAE for continuous risk.
  - Calibration curves and Brier score.
- Explainability:
  - Per-sample SHAP values for feature-level attribution.
  - Driver summaries map feature groups to human labels.
- Reproducibility:
  - Use deterministic seeds.
  - Log hyperparameters and dataset versions.

Outputs and export formats
- Per-day JSON report:
```json
{
  "date": "2025-08-17",
  "risk_score": 0.72,
  "label": "High",
  "drivers": [
    {"name": "Sleep disruption", "impact": 0.35},
    {"name": "Meeting overload", "impact": 0.22},
    {"name": "HRV drop", "impact": 0.15}
  ],
  "recommendation": "Reduce meeting block after 15:00. Aim for 7.5h sleep and a 20-minute low-effort break mid-afternoon."
}
```
- PDF summary: includes charts for HR, HRV, sleep, activity, and annotated risk timeline.
- CSV time-series: feature-level exports for downstream analytics.

Explainability and human-facing language
- Gemma AI translates model outputs to plain language.
- Each recommendation ties to a driver and a rationale. For example:
  - "We see a 20% drop in your 7-day rolling HRV and three nights of short sleep. Short sleep increases physiological load and reduces recovery. Try a 30-minute wind-down before bed and avoid screen exposure 45 minutes before sleep."
- Provide actionability:
  - Behavior changes (shift schedule, microbreaks)
  - Sleep hygiene adjustments
  - Workload design (meeting caps, async strategies)
  - Escalation paths for persistent high risk (seek professional support)

Privacy and data handling
- Default mode: local processing only. Data stays on device unless configured otherwise.
- Optional server sync: encrypt data in transit with TLS and at rest with DB-level encryption.
- Access control: role-based access for team deployments.
- Data retention: configurable retention policies.
- Export controls: users can export or delete their data.
- For research pilots: de-identify data and follow IRB and local regulations.

Security and operational notes
- Package dependencies: pin versions in requirements.txt. Use vulnerability scanning before production use.
- Secrets: store API keys in environment variables or a secure vault.
- Network: limit outbound connections from the processing host. Gemma AI calls are optional and can run locally.
- Backups: enable regular backups for feature store and models.
- Scaling: for larger deployments, use a queue-based ingestion layer (e.g., Kafka) and scale model servers horizontally.

Monitoring and metrics
- Health checks:
  - Data freshness: latency since last sample per source.
  - Ingestion rate: events per minute.
  - Model drift: track distribution shifts in key features and risk score baseline.
- Alerts:
  - Incoming gaps: missing wearable data > 24 hours.
  - Model error rate spike.
- Observability:
  - Use structured logs and traces. Metrics export to Prometheus available.

Tests and continuous integration
- Unit tests for feature extraction and core transformations.
- Integration tests that run small sample datasets through end-to-end pipeline.
- Example CI tasks:
  - linting (flake8)
  - unit tests (pytest)
  - static type checks (mypy)
  - model smoke tests: ensure a trained model produces outputs for sample input.
- Add new adapters under tests/adapters/

Deployment options
- Local desktop: run via Streamlit. Good for pilots and single users.
- Server-hosted: Docker Compose or Kubernetes with a managed Postgres and object store. Use gunicorn or Uvicorn for API endpoints.
- On-device: limited mode for privacy-first users. Use precompiled binaries in releases.
- Cloud pipelines: ingest to a data lake, run scheduled training, and serve model endpoints for real-time risk scoring.

Docker example
```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
EXPOSE 8501
CMD ["streamlit", "run", "ui/app.py", "--server.port=8501", "--server.headless=true"]
```

Extensibility and plugins
- Adapters: implement a simple adapter interface to add new wearables or APIs.
- Feature plugins: drop-in modules that compute custom temporal features.
- Model plugins: provide a model card and wrapper to integrate new models.
- Gemma skilllets: add custom conversational skills to address domain-specific interventions.

Contributing guide
- Fork the repo and create a feature branch.
- Follow naming convention: feature/<short-desc> or fix/<short-desc>.
- Run tests and linters before creating a PR.
- Provide clear descriptions and small, focused changes.
- Document new features in docs/ and update the changelog.
- Use conventional commits for release automation.

Issue types and labels
- bug: reproducible issues with code or processing
- enhancement: feature requests and UX improvements
- adapter: new device or API integration
- docs: documentation updates
- research: experiments and model improvements
- security: vulnerable dependency or security issue

Roadmap
- Short term:
  - Harden ingestion adapters.
  - Add more wearable vendor integrations.
  - Expand Gemma skilllets for personalized interventions.
- Mid term:
  - Validate model in larger pilot cohorts.
  - Add team-level aggregated analytics with privacy-preserving aggregation.
  - Add mobile native client for push nudges.
- Long term:
  - Clinical validation and regulatory pathway for clinical decision support.
  - Multi-modal sensor fusion with continuous context sensing.
  - Enterprise-grade orchestration for large user bases.

License
- MIT License. See LICENSE file.

FAQ
- What data do I need to run the system?
  - At minimum: sleep timing and daily activity. HR/HRV improves sensitivity. Calendar and self-report enhance driver attribution.
- Can Gemma-Guard run offline?
  - Yes. Core processing and local Gemma option run without network access.
- Is this a medical device?
  - The models provide risk estimates and recommendations. Treat outputs as supportive information. For clinical decisions, consult qualified professionals.
- How do I add a new wearable?
  - Add an adapter under ingestion/adapters with read and normalization logic. Follow existing adapter examples.

Developer notes and reproducibility
- Data versioning:
  - Use data snapshots and retain raw inputs. Log preprocessing parameters.
- Model cards:
  - Each model release includes a model card with training data description, metrics, and intended use.
- Experiment tracking:
  - Use MLflow or similar to store runs and artifacts.

Testing datasets and examples
- The repo includes small synthetic datasets for demonstration in examples/data/.
- Example notebooks:
  - examples/notebooks/chronotype_analysis.ipynb
  - examples/notebooks/hrv_trends.ipynb
  - examples/notebooks/driver_attribution.ipynb

Clinical and ethical considerations
- Inputs may reveal sensitive health states. Use policies to control access.
- Avoid automated high-risk recommendations without human review.
- Use consent flows for team deployments.
- Provide clear opt-out paths.

Integrations and ecosystem
- Supported connectors:
  - Fitbit, Oura, Apple Health (via export), Garmin, Google Fit, generic BLE adapters.
- AI connectors:
  - Ollama for local model hosting.
  - Optional cloud Gemma API for richer conversational features.
- Data sinks:
  - CSV, Parquet, Postgres, InfluxDB.

Metrics to track in pilots
- User retention: percent of users who use the app daily after onboarding.
- Agreement: correlation between model risk and self-reported stress.
- Action uptake: percent of recommendations implemented.
- Outcome delta: change in sleep regularity and HRV after recommended interventions.

Example case studies (fictional)
- Case A: Morning chronotype with meeting-heavy schedule
  - Issue: Phase advance mismatch; frequent early calls reduce sleep.
  - Gemma-Guard output: High driver weight to sleep timing and meeting density. Recommendation: Shift nonessential meetings later and enforce a hard no-meet before 08:30 policy twice a week.
  - Outcome: Improved sleep duration and HRV increase after 6 weeks.
- Case B: Shift worker with fragmented sleep
  - Issue: Rotating shifts caused circadian misalignment and flattened activity amplitude.
  - Gemma-Guard output: High risk from circadian disruption and recovery window loss. Suggest controlled light exposure strategy and scheduled naps.
  - Outcome: Re-synchronization of phase and improved daytime alertness metrics in pilot.

Troubleshooting
- If data does not appear in dashboard:
  - Verify ingestion status and last timestamp per source.
  - Check processing logs for errors.
- If model output seems unstable:
  - Check for missing baseline window (needs at least 7 days).
  - Inspect feature distributions for recent shifts.
- If the installer does not run:
  - Ensure the downloaded release matches OS and has execution permissions.

Changelog and releases
- See the releases page for packaged builds and installer artifacts: https://github.com/K7Xdragon/Gemma-Guard/releases  
  Download the matching release file and run the installer script or binary it contains.

Contacts and maintainers
- Maintainer: K7Xdragon
- Create issues for bugs or feature requests.
- For collaboration, open a pull request or start a discussion on GitHub.

Glossary
- HRV: Heart Rate Variability, a measure of autonomic balance.
- Circadian phase: the timing of daily physiological peaks and troughs.
- Chronotype: preference toward morningness or eveningness.
- Allostatic load: cumulative wear and tear from repeated stress.
- Gemma AI: the conversational and explanation engine integrated with the risk model.

References and further reading
- Standard texts on chronobiology and HRV:
  - "Circadian Rhythms: A Very Short Introduction" — general concept primer.
  - "Heart Rate Variability: Standards of Measurement" — HRV definitions and methodology.
- Selected papers on burnout and physiology:
  - Workload stress, sleep disruption, and burnout: empirical studies in occupational health.
  - Temporal patterns in mental health: week-to-week and daily rhythm analyses.

Legal and compliance pointers
- For clinical deployments, follow local medical device regulation.
- For enterprise pilots, consult legal for data sharing and employee consent.

Acknowledgements
- The project builds on public research in chronobiology, stress physiology, and human-centered AI. Contributors and pilot participants shape feature design.

If you need the packaged release for your platform, go to the Releases page, download the artifact that matches your OS, and execute the installer included in that release: https://github.com/K7Xdragon/Gemma-Guard/releases

END