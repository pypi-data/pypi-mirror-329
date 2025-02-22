"""Teams validator module"""

import functools
from collections import Counter
from typing import Dict, List, Set, Tuple, Union

from opendapi.defs import CATEGORIES_SUFFIX, OPENDAPI_SPEC_URL, OpenDAPIEntity
from opendapi.validators.base import BaseValidator, ValidationError
from opendapi.validators.defs import MergeKeyCompositeIDParams


class CategoriesValidator(BaseValidator):
    """
    Validator class for Subjects files
    """

    SUFFIX = CATEGORIES_SUFFIX
    SPEC_VERSION = "0-0-1"
    ENTITY = OpenDAPIEntity.CATEGORIES

    # Paths & keys to use for uniqueness check within a list of dicts when merging
    MERGE_UNIQUE_LOOKUP_KEYS: List[
        Tuple[
            List[Union[str, int, MergeKeyCompositeIDParams.IgnoreListIndex]],
            MergeKeyCompositeIDParams,
        ]
    ] = [(["categories"], MergeKeyCompositeIDParams(required=[["urn"]]))]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @functools.cached_property
    def _category_urn_counts(self) -> Counter:
        """Collect all the category urns"""
        return Counter(
            (
                category.get("urn")
                for _, content in self.merged_file_state.items()
                for category in content.get("categories", [])
            )
        )

    @property
    def category_urns(self) -> Set[str]:
        """Return the available category urns"""
        return set(self._category_urn_counts.keys())

    def _validate_period_delimited_taxonomical_structure(
        self, file: str, content: dict
    ):
        """Validate if the category urns are period delimited"""
        category_urns = self.category_urns
        invalid_categories = {
            category["urn"]
            for category in content.get("categories", [])
            # parent does not exist
            if category["urn"].rsplit(".", 1)[0] not in category_urns
        }
        if invalid_categories:
            raise ValidationError(
                (
                    "Category URNs that do not have parents in the taxonomy as defined by the "
                    f"period delimited structure found in file '{file}': {invalid_categories}"
                )
            )

    def _validate_category_urns_globally_unique(self, file: str, content: dict):
        """Validate if the category urns are globally unique"""
        non_unique_category_urns = {
            category["urn"]
            for category in content.get("categories", [])
            if self._category_urn_counts[category["urn"]] > 1
        }
        if non_unique_category_urns:
            raise ValidationError(
                f"Non-globally-unique category urns in file '{file}': {non_unique_category_urns}"
            )

    def validate_content(self, file: str, content: Dict):
        """Validate the content of the files"""
        super().validate_content(file, content)
        self._validate_period_delimited_taxonomical_structure(file, content)
        self._validate_category_urns_globally_unique(file, content)

    def _get_base_generated_files(self) -> Dict[str, Dict]:
        """Set Autoupdate templates in {file_path: content} format"""
        return {
            f"{self.base_destination_dir}/{self.config.org_name_snakecase}.categories.yaml": {
                "schema": OPENDAPI_SPEC_URL.format(
                    version=self.SPEC_VERSION, entity="categories"
                ),
                "categories": [],
            }
        }
