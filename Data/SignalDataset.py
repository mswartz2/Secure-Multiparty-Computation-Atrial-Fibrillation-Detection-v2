from dataclasses import dataclass, field


@dataclass
class SignalDataset:
    raw_data: list = field(default_factory=list)
    labels: list = field(default_factory=list)
    patient_ids: list = field(default_factory=list)
