from plexflow.core.context.partial_context import PartialContext
from plexflow.core.downloads.candidates.download_candidate import DownloadCandidate
from typing import List

class Candidates(PartialContext):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    def all(self) -> List[DownloadCandidate]:
        return self.get("download/candidates")

    def update(self, candidates: List[DownloadCandidate]):
        if len(candidates) == 0:
            return
        self.set("download/candidates", candidates)
