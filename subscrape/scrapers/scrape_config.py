__author__ = 'Tommi Enenkel @alice_und_bob'

import copy


class ScrapeConfig:
    def __init__(self, config):
        self.filter = None
        self.processor_name = None
        self.skip = False
        self.params = None
        self.api = None
        self.db_path = None
        self._set_config(config)

    def _set_config(self, config):
        """
        Extract metadata from the config file indicating where filtering or skipping should occur. Use that to generate
        filter methods which will be applied to the list of transactions.

        :param config: JSON dict of the scrape config
        :type config: dict
        """
        if type(config) is list:
            return

        if config is None:
            return

        filter_conditions = config.get("_filter", None)
        if filter_conditions is not None:
            self.filter = self._filter_factory(filter_conditions)

        processor_name = config.get("_processor", None)
        if processor_name is not None:
            self.processor_name = processor_name

        skip = config.get("_skip", None)
        if skip is not None:
            self.skip = skip

        params = config.get("_params", None)
        if params is not None:
            self.params = params

        # _api is only relevant on the chain level
        api = config.get("_api", None)
        if api is not None:
            self.api = api

        # _db_path is only relevant on the chain level
        db_path = config.get("_db_path", None)
        if db_path is not None:
            self.db_path = db_path

    def create_inner_config(self, config):
        """
        creates a config that can be nested to lower layers

        :param config: JSON dict of the scrape config
        :type config: dict
        """
        result = copy.deepcopy(self)
        result._set_config(config)
        return result

    def _filter_factory(self, conditions):
        """
        Generates a filter method based on the conditions passed in (from the config file)

        :param conditions: list of filter conditions to apply
        :type conditions: list
        :returns: filter method that returns true if an extrinsic should be skipped because it hits a
        filter condition
        """
        if conditions is None:
            return None

        def filter(extrinsic):
            """
            :returns: true if the extrinsic should be skipped because it hits a filter condition
            """
            for group in conditions:
                for key in group:
                    if key not in extrinsic:
                        return True
                    actual_value = extrinsic[key]
                    predicates = group[key]
                    for predicate in predicates:
                        if "<" in predicate:
                            value = predicate["<"]
                            if actual_value < value:
                                continue
                            else:
                                return True
            return False
        return filter
