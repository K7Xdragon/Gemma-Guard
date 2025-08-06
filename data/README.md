# 📊 Data Directory

This directory contains data files used by GemmaGuard for logging and storage.

## File Structure

- `inference_log.json` - AI analysis logs (generated during use)
- `signal_log.json` - Biometric signal data logs (generated during use)  
- `user_profile.json` - User profile information (generated during use)
- `test.json` - Test data for development

## Privacy Notice

**🔒 Data files are automatically excluded from Git commits** to protect user privacy.

All personal data remains local and is never transmitted externally.

## File Formats

### inference_log.json
```json
[
    {
        "record_id": "unique-id",
        "timestamp_utc": "2025-08-06T12:00:00Z",
        "user": {
            "nickname": "user_nickname",
            "status": "Student/Working",
            "location": "City, State, Country"
        },
        "trait_profile": { ... },
        "analysis_results": { ... }
    }
]
```

### signal_log.json
```json
[
    {
        "signal_id": "unique-signal-id",
        "timestamp_utc": "2025-08-06T12:00:00Z",
        "skin_conductance": 3.45,
        "environmental_state": "calm/charged/restrictive",
        "record_id": "linked-record-id"
    }
]
```

### user_profile.json
```json
{
    "id": "user_id",
    "name": "User Name",
    "dob": "YYYY-MM-DD",
    "location": {
        "city": "City",
        "state": "State", 
        "country": "Country"
    },
    "demographics": { ... }
}
```
