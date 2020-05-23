class ListDetailSerializerMixin(object):
    """
    Overrides get_serializer_class to choose the read serializer
    for GET requests and the write serializer for POST requests.

    Set list_serializer_class and detail_serializer_class attributes on a
    viewset.
    """

    list_serializer_class = None
    detail_serializer_class = None

    def get_serializer_class(self):
        if self.action in ["retrieve", "update", "partial_update", "destroy"]:
            return self.get_detail_serializer_class()
        return self.get_list_serializer_class()

    def get_list_serializer_class(self):
        assert self.list_serializer_class is not None, (
            "'%s' should either include a `list_serializer_class` attribute,"
            "or override the `get_read_serializer_class()` method."
            % self.__class__.__name__
        )
        return self.list_serializer_class

    def get_detail_serializer_class(self):
        assert self.detail_serializer_class is not None, (
            "'%s' should either include a `detail_serializer_class` attribute,"
            "or override the `get_write_serializer_class()` method."
            % self.__class__.__name__
        )
        return self.detail_serializer_class