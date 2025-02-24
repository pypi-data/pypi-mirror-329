"""Email analysis functionality."""

import mailbox
from pathlib import Path
from collections import Counter
from datetime import datetime
from email.utils import parsedate_to_datetime
from typing import Dict, List, Any

class EmailAnalyzer:
    """Analyzes email data from mbox files."""

    def __init__(self, mbox_path: Path):
        """Initialize the analyzer with an mbox file path.

        Args:
            mbox_path: Path to the mbox file to analyze
        """
        self.mbox_path = mbox_path

    def analyze(self) -> Dict[str, Any]:
        """Analyze the mbox file and return statistics.

        Returns:
            Dictionary containing email statistics
        """
        mbox = mailbox.mbox(str(self.mbox_path))

        total_messages = len(mbox)
        senders: Counter = Counter()
        dates: List[datetime] = []
        subjects: Counter = Counter()

        for message in mbox:
            # Count senders
            sender = message.get('from', '')
            senders[sender] += 1

            # Parse dates
            date_str = message.get('date')
            if date_str:
                try:
                    date = parsedate_to_datetime(date_str)
                    dates.append(date)
                except (TypeError, ValueError):
                    pass

            # Count subject lines
            subject = message.get('subject', '')
            subjects[subject] += 1

        # Calculate statistics
        stats = {
            'total_messages': total_messages,
            'unique_senders': len(senders),
            'top_senders': dict(senders.most_common(10)),
            'date_range': {
                'start': min(dates).isoformat() if dates else None,
                'end': max(dates).isoformat() if dates else None,
            },
            'top_subjects': dict(subjects.most_common(10)),
        }

        return stats

    def save_report(self, results: Dict[str, Any], output_path: Path) -> None:
        """Save analysis results to a file.

        Args:
            results: Analysis results to save
            output_path: Path where to save the report
        """
        import json

        with open(output_path, 'w') as f:
            json.dump(results, f, indent=2)