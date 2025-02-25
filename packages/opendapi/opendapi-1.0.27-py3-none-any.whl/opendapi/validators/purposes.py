"""Teams validator module"""

import functools
from collections import Counter
from typing import Dict, List, Tuple, Union

from opendapi.defs import OPENDAPI_SPEC_URL, PURPOSES_SUFFIX, OpenDAPIEntity
from opendapi.validators.base import BaseValidator, ValidationError
from opendapi.validators.defs import MergeKeyCompositeIDParams


class PurposesValidator(BaseValidator):
    """
    Validator class for Purposes files
    """

    SUFFIX = PURPOSES_SUFFIX
    SPEC_VERSION = "0-0-1"
    ENTITY = OpenDAPIEntity.PURPOSES

    # Paths & keys to use for uniqueness check within a list of dicts when merging
    MERGE_UNIQUE_LOOKUP_KEYS: List[
        Tuple[
            List[Union[str, int, MergeKeyCompositeIDParams.IgnoreListIndex]],
            MergeKeyCompositeIDParams,
        ]
    ] = [(["purposes"], MergeKeyCompositeIDParams(required=[["urn"]]))]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @functools.cached_property
    def _purposes_urn_counts(self) -> Counter:
        """Collect all the purposes urns"""
        return Counter(
            (
                p.get("urn")
                for _, content in self.merged_file_state.items()
                for p in content.get("purposes", [])
            )
        )

    @property
    def purposes_urns(self) -> List[str]:
        """Return the purposes urns"""
        return list(self._purposes_urn_counts.keys())

    def _validate_period_delimited_taxonomical_structure(
        self, file: str, content: dict
    ):
        """Validate if the purpose urns are period delimited"""
        purposes_urns = self.purposes_urns
        invalid_purposes = {
            purpose["urn"]
            for purpose in content.get("purposes", [])
            # parent does not exist
            if purpose["urn"].rsplit(".", 1)[0] not in purposes_urns
        }
        if invalid_purposes:
            raise ValidationError(
                (
                    "Purpose URNs that do not have parents in the taxonomy as defined by the "
                    f"period delimited structure found in file '{file}': {invalid_purposes}"
                )
            )

    def _validate_min_max_retention_days_consistency(self, file: str, content: dict):
        """Validate if the min_retention_days is less than or equal to max_retention_days"""
        invalid_purposes = {}
        for purpose in content.get("purposes", []):
            pdp = purpose.get("personal_data_policy", {})
            min_retention_days = (
                float("inf")
                if (min_r := pdp.get("min_retention_days")) is None
                else min_r
            )
            max_retention_days = (
                float("inf")
                if (max_r := pdp.get("max_retention_days")) is None
                else max_r
            )
            if min_retention_days > max_retention_days:
                min_retention_stanza = "null (inf)" if min_r is None else min_r
                invalid_purposes[purpose["urn"]] = (
                    f"min_retention_days: {min_retention_stanza}, max_retention_days: {max_r}"
                )
        if invalid_purposes:
            raise ValidationError(
                (
                    "Purpose URNs that have min_retention_days greater than max_retention_days "
                    f"found in file '{file}': {invalid_purposes}"
                )
            )

    def _validate_purpose_urns_globally_unique(self, file: str, content: dict):
        """Validate if the purpose urns are globally unique"""
        non_unique_purpose_urns = {
            purpose["urn"]
            for purpose in content.get("purposes", [])
            if self._purposes_urn_counts[purpose["urn"]] > 1
        }
        if non_unique_purpose_urns:
            raise ValidationError(
                f"Non-globally-unique purpose urns in file '{file}': {non_unique_purpose_urns}"
            )

    def validate_content(self, file: str, content: Dict):
        """Validate the content of the files"""
        super().validate_content(file, content)
        self._validate_period_delimited_taxonomical_structure(file, content)
        self._validate_purpose_urns_globally_unique(file, content)
        self._validate_min_max_retention_days_consistency(file, content)

    def _get_base_generated_files(self) -> Dict[str, Dict]:
        """Set Autoupdate templates in {file_path: content} format"""
        return {
            f"{self.base_destination_dir}/{self.config.org_name_snakecase}.purposes.yaml": {
                "schema": OPENDAPI_SPEC_URL.format(
                    version=self.SPEC_VERSION, entity="purposes"
                ),
                "purposes": [],
            }
        }
