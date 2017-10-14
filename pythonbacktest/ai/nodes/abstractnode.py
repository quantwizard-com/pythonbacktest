import abc


class AbstractNode(object):

    @abc.abstractmethod
    def reset_node(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def inject_data(self, **kwargs):
        raise NotImplementedError()

    @property
    def current_value(self):
        raise NotImplementedError()

    @property
    def all_collected_values(self):
        raise NotImplementedError()
