"""Teams validator module"""

import functools
from collections import Counter
from typing import Dict, List, Tuple, Union

from opendapi.defs import DATASTORES_SUFFIX, OPENDAPI_SPEC_URL, OpenDAPIEntity
from opendapi.validators.base import BaseValidator, ValidationError
from opendapi.validators.defs import MergeKeyCompositeIDParams


class DatastoresValidator(BaseValidator):
    """
    Validator class for datastores files
    """

    SUFFIX = DATASTORES_SUFFIX
    SPEC_VERSION = "0-0-1"
    ENTITY = OpenDAPIEntity.DATASTORES

    # Paths & keys to use for uniqueness check within a list of dicts when merging
    MERGE_UNIQUE_LOOKUP_KEYS: List[
        Tuple[
            List[Union[str, int, MergeKeyCompositeIDParams.IgnoreListIndex]],
            MergeKeyCompositeIDParams,
        ]
    ] = [(["datastores"], MergeKeyCompositeIDParams(required=[["urn"]]))]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @functools.cached_property
    def _datastores_urn_counts(self) -> Counter:
        """Collect all the datastores urns"""
        return Counter(
            (
                dt.get("urn")
                for _, content in self.merged_file_state.items()
                for dt in content.get("datastores", [])
            )
        )

    @property
    def datastores_urns(self) -> List[str]:
        """Return the datastores urns"""
        return list(self._datastores_urn_counts.keys())

    def _validate_datastore_urns_globally_unique(self, file: str, content: dict):
        """Validate if the datastore urns are globally unique"""
        non_unique_datastore_urns = {
            datastore["urn"]
            for datastore in content.get("datastores", [])
            if self._datastores_urn_counts[datastore["urn"]] > 1
        }
        if non_unique_datastore_urns:
            raise ValidationError(
                f"Non-globally-unique datastore urns in file '{file}': {non_unique_datastore_urns}"
            )

    def validate_content(self, file: str, content: Dict):
        """Validate the content of the files"""
        super().validate_content(file, content)
        self._validate_datastore_urns_globally_unique(file, content)

    def _get_base_generated_files(self) -> Dict[str, Dict]:
        """Set Autoupdate templates in {file_path: content} format"""
        return {
            f"{self.base_destination_dir}/{self.config.org_name_snakecase}.datastores.yaml": {
                "schema": OPENDAPI_SPEC_URL.format(
                    version=self.SPEC_VERSION, entity="datastores"
                ),
                "datastores": [],
            }
        }
